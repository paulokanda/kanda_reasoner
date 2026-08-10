"""Inventory and PNG-reuse checks for source-tree archive export."""

from __future__ import annotations

__all__: list[str] = []


import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any, Iterable

from .exclusion_provider import load_bundle_exclusion_rules
from .generated_archive_policy import (
    enforce_large_root_archive_preflight,
)
from .hashing import sha256_file
from .path_normalization import safe_resolve
from .schema_models import ProjectContext
from kanda_reasoner_app.source_hygiene.tool_archive_policy import (
    is_kanda_reasoner_tool_root,
    validate_registered_synthetic_fixtures,
)

from .source_archive_routing import (
    SourceArchiveRouteKind,
    route_builtin_source_archive_entry,
    route_source_archive_entry,
)

from .source_tree_exporter_shared import (
    SOURCE_ARCHIVE_MANIFEST_SUFFIX,
    _PNG_ASSET_EXTENSIONS,
    _context,
    _exclusion_record,
    _is_png_asset_record,
    _posix_rel,
)

def _excluded_by_builtin_policy(
    entry: Path,
    context: ProjectContext,
    output_dir: Path,
) -> dict[str, Any] | None:
    """Preserve the legacy exporter facade through the shared router.

    ``source_tree_exporter`` imports this private name as part of its existing
    compatibility surface.  Returning the router's exclusion record preserves
    the established contract without duplicating routing logic.
    """
    route = route_builtin_source_archive_entry(entry, context, output_dir)
    if route is None:
        return None
    return route.exclusion_record


def _file_record(
    path: Path,
    context: ProjectContext,
    previous_png_records: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    stat = path.stat()
    rel_path = _posix_rel(path, context)
    sha256_value = ""
    previous_record = None
    if previous_png_records is not None and path.suffix.lower() in _PNG_ASSET_EXTENSIONS:
        previous_record = previous_png_records.get(rel_path)
    if (
        previous_record is not None
        and int(previous_record.get("size_bytes", -1)) == int(stat.st_size)
        and int(previous_record.get("mtime_ns", -1)) == int(stat.st_mtime_ns)
        and str(previous_record.get("sha256", ""))
    ):
        sha256_value = str(previous_record["sha256"])
    else:
        sha256_value = sha256_file(path)
    return {
        "path": rel_path,
        "absolute_path": str(path),
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": sha256_value,
    }

def _iter_sorted_entries(path: Path) -> Iterable[Path]:
    try:
        entries = list(path.iterdir())
    except OSError:
        return []
    return sorted(entries, key=lambda item: (not item.is_dir(), item.name.lower(), item.name))

def _load_previous_source_archive_manifest(
    previous_output_dir: str | Path | None,
    context: ProjectContext,
) -> dict[str, Any] | None:
    if previous_output_dir is None:
        return None
    previous_dir = Path(previous_output_dir).expanduser().resolve(strict=False)
    manifest_name = context.project_slug + SOURCE_ARCHIVE_MANIFEST_SUFFIX
    loose_manifest = previous_dir / manifest_name
    if loose_manifest.exists():
        try:
            return json.loads(loose_manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
    handoff_zip = previous_dir / (context.project_slug + "__ai_handoff_upload.zip")
    if not handoff_zip.exists():
        return None
    try:
        with zipfile.ZipFile(handoff_zip, "r") as archive:
            for name in archive.namelist():
                if name.endswith("/" + manifest_name) or name == manifest_name:
                    return json.loads(archive.read(name).decode("utf-8"))
    except (OSError, UnicodeDecodeError, zipfile.BadZipFile, json.JSONDecodeError):
        return None
    return None

def _previous_png_record_map(previous_manifest: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(previous_manifest, dict):
        return {}
    records: dict[str, dict[str, Any]] = {}
    for item in previous_manifest.get("included_files", []):
        if not isinstance(item, dict):
            continue
        path_text = str(item.get("path", ""))
        if not path_text or Path(path_text).suffix.lower() not in _PNG_ASSET_EXTENSIONS:
            continue
        if item.get("archive_family") != "png_assets":
            continue
        records[path_text] = item
    return records

def _current_png_signature(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    signature = []
    for record in records:
        if not _is_png_asset_record(record):
            continue
        signature.append(
            {
                "path": str(record.get("path", "")),
                "size_bytes": int(record.get("size_bytes", 0)),
                "sha256": str(record.get("sha256", "")),
            }
        )
    return sorted(signature, key=lambda item: item["path"].lower())

def _previous_png_signature(previous_manifest: dict[str, Any] | None) -> list[dict[str, Any]]:
    records = _previous_png_record_map(previous_manifest)
    signature = []
    for item in records.values():
        signature.append(
            {
                "path": str(item.get("path", "")),
                "size_bytes": int(item.get("size_bytes", 0)),
                "sha256": str(item.get("sha256", "")),
            }
        )
    return sorted(signature, key=lambda item: item["path"].lower())


def _png_signature_sha256(records: list[dict[str, Any]]) -> str:
    """Return a stable content identity for one PNG inventory."""
    digest = hashlib.sha256()
    for item in _current_png_signature(records):
        digest.update(str(item["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(item["size_bytes"]).encode("ascii"))
        digest.update(b"\0")
        digest.update(str(item["sha256"]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _previous_png_signature_sha256(
    previous_manifest: dict[str, Any] | None,
) -> str:
    """Return the prior manifest PNG content identity."""
    if not isinstance(previous_manifest, dict):
        return ""
    contract = previous_manifest.get("png_asset_archive_contract", {})
    if isinstance(contract, dict):
        stored = str(contract.get("content_signature_sha256", "")).strip()
        if stored:
            return stored
    records = list(_previous_png_record_map(previous_manifest).values())
    return _png_signature_sha256(records)


def _zip_structure_matches(
    source_path: Path,
    *,
    expected_file_count: int,
    require_full_test: bool,
) -> bool:
    """Validate ZIP structure, using full CRC reads only when required."""
    try:
        with zipfile.ZipFile(source_path, "r") as archive:
            infos = archive.infolist()
            if expected_file_count > 0 and len(infos) != expected_file_count:
                return False
            if any(info.compress_type != zipfile.ZIP_STORED for info in infos):
                return False
            if require_full_test and archive.testzip() is not None:
                return False
    except (OSError, zipfile.BadZipFile):
        return False
    return True

def _can_reuse_previous_png_assets(
    *,
    context: ProjectContext,
    previous_output_dir: str | Path | None,
    previous_manifest: dict[str, Any] | None,
    png_asset_files: list[dict[str, Any]],
    part_size_mb: int,
    hard_cap: int,
) -> bool:
    if previous_output_dir is None or not previous_manifest or not png_asset_files:
        return False
    contract = previous_manifest.get("png_asset_archive_contract", {})
    if not isinstance(contract, dict):
        return False
    if contract.get("enabled") is not True:
        return False
    if str(contract.get("compression_method", "")) != "ZIP_STORED":
        return False
    if int(contract.get("selected_size_cap_mb", -1)) != int(part_size_mb):
        return False
    if int(contract.get("selected_size_cap_bytes", -1)) != int(hard_cap):
        return False
    current_signature = _png_signature_sha256(png_asset_files)
    previous_signature = _previous_png_signature_sha256(previous_manifest)
    if not current_signature or current_signature != previous_signature:
        return False
    previous_dir = Path(previous_output_dir).expanduser().resolve(strict=False)
    for part in previous_manifest.get("png_asset_parts", []):
        if not isinstance(part, dict):
            return False
        filename = str(part.get("filename", ""))
        if not filename.startswith(context.project_slug + "__png_assets_part") or not filename.endswith(".zip"):
            return False
        source_path = previous_dir / filename
        if not source_path.exists() or not source_path.is_file():
            return False
        try:
            stat = source_path.stat()
        except OSError:
            return False
        if stat.st_size != int(part.get("actual_size_bytes", -1)):
            return False

        expected_mtime_ns = int(part.get("file_mtime_ns", 0) or 0)
        metadata_identity_matches = (
            expected_mtime_ns > 0
            and int(stat.st_mtime_ns) == expected_mtime_ns
        )
        if metadata_identity_matches:
            if not _zip_structure_matches(
                source_path,
                expected_file_count=int(part.get("file_count", 0)),
                require_full_test=False,
            ):
                return False
            continue

        if sha256_file(source_path) != str(part.get("sha256", "")):
            return False
        if not _zip_structure_matches(
            source_path,
            expected_file_count=int(part.get("file_count", 0)),
            require_full_test=True,
        ):
            return False
    return True

def gather_source_archive_inventory(
    project: str | Path | ProjectContext,
    output_dir: str | Path,
    previous_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return included/excluded file inventory for source-archive export."""
    context = _context(project)
    from kanda_reasoner_app.generated_artifact_hygiene import cleanup_project_generated_zip_noise

    cleanup_result = cleanup_project_generated_zip_noise(context.root)
    if cleanup_result.get("errors"):
        raise RuntimeError("Generated ZIP artifact cleanup failed before source archive inventory: " + str(cleanup_result.get("errors")))

    root = safe_resolve(context.root)
    output_path = safe_resolve(output_dir)
    rules = load_bundle_exclusion_rules(context)
    previous_png_records = _previous_png_record_map(previous_manifest)
    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    tool_hygiene_active = is_kanda_reasoner_tool_root(root)
    if tool_hygiene_active:
        validate_registered_synthetic_fixtures(root)

    def walk(current: Path) -> None:
        for entry in _iter_sorted_entries(current):
            route = route_source_archive_entry(
                entry,
                context,
                output_path,
                rules,
                tool_hygiene_active=tool_hygiene_active,
            )
            if route.route is SourceArchiveRouteKind.BLOCK:
                raise RuntimeError(
                    "TOOL_SOURCE_ARCHIVE_HYGIENE_REJECTED:"
                    + route.error
                )
            if route.route is SourceArchiveRouteKind.EXCLUDE:
                if route.exclusion_record is None:
                    raise RuntimeError(
                        "SOURCE_ARCHIVE_EXCLUSION_RECORD_MISSING:"
                        + route.relative_path
                    )
                excluded.append(route.exclusion_record)
                continue
            enforce_large_root_archive_preflight(entry, context)
            if entry.is_dir():
                walk(entry)
            elif entry.is_file():
                try:
                    included.append(_file_record(entry, context, previous_png_records))
                except OSError as exc:
                    excluded.append(
                        _exclusion_record(
                            entry,
                            context,
                            reason_code="unreadable_file",
                            reason="File could not be read during source archive export: " + str(exc),
                            path_type="file",
                        )
                    )

    walk(root)
    included.sort(key=lambda item: str(item["path"]).lower())
    excluded.sort(key=lambda item: str(item["path"]).lower())
    return {
        "context": context,
        "included_files": included,
        "excluded_paths": excluded,
    }
