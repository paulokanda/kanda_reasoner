"""Verified read-only cache for canonical complete-JSON ZIP evidence."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
    project_analysis_evidence_root,
    working_copy_json_path,
)

from .complete_json_artifacts import complete_json_artifact_dir

__all__ = ["resolve_complete_json_evidence"]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Expected JSON object: " + str(path))
    return payload


def _manifest_fingerprint(manifest_path: Path, parts: list[Path]) -> str:
    digest = hashlib.sha256()
    digest.update(manifest_path.read_bytes())
    for part in parts:
        digest.update(part.name.encode("utf-8"))
        digest.update(str(part.stat().st_size).encode("ascii"))
        digest.update(_sha256_file(part).encode("ascii"))
    return digest.hexdigest()


def _validated_manifest_in_dir(
    project_root: Path,
    evidence_dir: Path,
) -> tuple[Path, dict[str, Any], list[Path]] | None:
    evidence_dir = evidence_dir.resolve(strict=False)
    slug = project_root.name
    manifest_path = evidence_dir / (slug + "__complete_json_manifest.json")
    if not manifest_path.is_file():
        return None
    payload = _load_object(manifest_path)
    if payload.get("artifact_type") != "canonical_complete_json_zip_family":
        raise ValueError("Unsupported complete JSON manifest artifact type.")
    if str(payload.get("project_slug") or "") != slug:
        raise ValueError("Complete JSON manifest project slug mismatch.")
    parts_payload = payload.get("parts")
    if not isinstance(parts_payload, list) or not parts_payload:
        raise ValueError("Complete JSON manifest has no parts.")
    parts: list[Path] = []
    for item in parts_payload:
        if not isinstance(item, dict):
            raise ValueError("Complete JSON manifest part is not an object.")
        filename = str(item.get("filename") or "")
        if not filename or Path(filename).name != filename:
            raise ValueError("Unsafe complete JSON ZIP part filename.")
        part_path = evidence_dir / filename
        if not part_path.is_file():
            raise ValueError("Complete JSON ZIP part is missing: " + filename)
        if part_path.stat().st_size != int(item.get("size_bytes") or -1):
            raise ValueError("Complete JSON ZIP part size mismatch: " + filename)
        if _sha256_file(part_path) != str(item.get("sha256") or ""):
            raise ValueError("Complete JSON ZIP part hash mismatch: " + filename)
        parts.append(part_path)
    return manifest_path, payload, parts


def _validated_manifest(
    project_root: Path,
) -> tuple[Path, dict[str, Any], list[Path], str] | None:
    preferred = _validated_manifest_in_dir(
        project_root,
        complete_json_artifact_dir(project_root),
    )
    if preferred is not None:
        return (*preferred, "Project Structure 3D JSON ZIP cache")
    legacy = _validated_manifest_in_dir(
        project_root,
        analysis_json_complete_dir(project_root),
    )
    if legacy is not None:
        return (*legacy, "complete JSON ZIP cache")
    return None


def _cache_paths(project_root: Path) -> tuple[Path, Path, Path]:
    support_root = project_analysis_evidence_root(project_root).resolve(strict=False)
    state_root = support_root / "project_structure_3d_state"
    return (
        state_root / "complete_json_cache",
        state_root / "complete_json_cache_building",
        state_root / "complete_json_cache_previous",
    )


def _cache_is_reusable(
    cache_dir: Path,
    payload: dict[str, Any],
    fingerprint: str,
) -> Path | None:
    cache_manifest = cache_dir / "cache_manifest.json"
    output = cache_dir / str(payload.get("original_filename") or "")
    if not cache_manifest.is_file() or not output.is_file():
        return None
    cached = _load_object(cache_manifest)
    if cached.get("source_fingerprint") != fingerprint:
        return None
    if output.stat().st_size != int(payload.get("original_size_bytes") or -1):
        return None
    if cached.get("original_sha256") != payload.get("original_sha256"):
        return None
    return output


def _extract_member(archive: zipfile.ZipFile, member_name: str, output) -> None:
    names = archive.namelist()
    if names != [member_name]:
        raise ValueError("Complete JSON ZIP must contain exactly the declared member.")
    with archive.open(member_name, "r") as source:
        shutil.copyfileobj(source, output, length=1024 * 1024)


def _reconstruct(
    build_dir: Path,
    payload: dict[str, Any],
    parts: list[Path],
    fingerprint: str,
) -> Path:
    shutil.rmtree(build_dir, ignore_errors=True)
    build_dir.mkdir(parents=True, exist_ok=True)
    output = build_dir / str(payload["original_filename"])
    part_records = payload["parts"]
    with output.open("wb") as destination:
        for part_path, record in zip(parts, part_records):
            member_name = str(record.get("member_name") or "")
            with zipfile.ZipFile(part_path, "r") as archive:
                _extract_member(archive, member_name, destination)
    if output.stat().st_size != int(payload.get("original_size_bytes") or -1):
        raise ValueError("Reconstructed complete JSON size mismatch.")
    if _sha256_file(output) != str(payload.get("original_sha256") or ""):
        raise ValueError("Reconstructed complete JSON hash mismatch.")
    with output.open("r", encoding="utf-8-sig") as handle:
        prefix = handle.read(64).lstrip()
    if not prefix.startswith("{"):
        raise ValueError("Reconstructed complete JSON is not a JSON object.")
    cache_manifest = {
        "schema_version": "1.0",
        "artifact_type": "project_structure_3d_complete_json_cache",
        "source_fingerprint": fingerprint,
        "original_filename": payload["original_filename"],
        "original_size_bytes": payload["original_size_bytes"],
        "original_sha256": payload["original_sha256"],
    }
    (build_dir / "cache_manifest.json").write_text(
        json.dumps(cache_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def _publish_cache(cache_dir: Path, build_dir: Path, previous_dir: Path) -> None:
    shutil.rmtree(previous_dir, ignore_errors=True)
    if cache_dir.exists():
        shutil.move(str(cache_dir), str(previous_dir))
    try:
        shutil.move(str(build_dir), str(cache_dir))
    except Exception:
        if previous_dir.exists() and not cache_dir.exists():
            shutil.move(str(previous_dir), str(cache_dir))
        raise
    shutil.rmtree(previous_dir, ignore_errors=True)


def resolve_complete_json_evidence(
    project_root: str | Path,
) -> tuple[Path | None, str, str]:
    """Return verified complete JSON path, source label, and cache status."""
    root = Path(project_root).expanduser().resolve()
    manifest_result = _validated_manifest(root)
    if manifest_result is not None:
        manifest_path, payload, parts, source_label = manifest_result
        fingerprint = _manifest_fingerprint(manifest_path, parts)
        cache_dir, build_dir, previous_dir = _cache_paths(root)
        reusable = _cache_is_reusable(cache_dir, payload, fingerprint)
        if reusable is not None:
            return reusable, source_label, "reused"
        _reconstruct(build_dir, payload, parts, fingerprint)
        _publish_cache(cache_dir, build_dir, previous_dir)
        return (
            cache_dir / str(payload["original_filename"]),
            source_label,
            "rebuilt",
        )

    evidence_dir = analysis_json_complete_dir(root).resolve(strict=False)
    legacy = evidence_dir / (root.name + "__complete.json")
    legacy_error: ValueError | None = None
    if legacy.is_file():
        try:
            _load_object(legacy)
        except ValueError as exc:
            legacy_error = exc
        else:
            return legacy, "legacy loose complete JSON", "legacy"

    # Show Project to AI refreshes this exact local copy before it removes the
    # loose canonical complete JSON from second_prompt_files after ZIP export.
    # Project Structure 3D is a read-only consumer of that preserved evidence.
    local_copy = working_copy_json_path(root).resolve(strict=False)
    if local_copy.is_file():
        try:
            _load_object(local_copy)
        except ValueError:
            if legacy_error is not None:
                raise legacy_error
            raise
        return (
            local_copy,
            "Show Project to AI local complete JSON",
            "show_project_local",
        )

    if legacy_error is not None:
        raise legacy_error
    return None, "", "missing"
