"""Hydrate loose runtime files from a committed exact path-and-hash allowlist."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import uuid
from copy import deepcopy
from pathlib import Path, PurePosixPath

from portable.constants import (
    BUILDER_VERSION,
    FEATURE_ID,
    PORTABLE_HARDENING_FEATURES,
)
from portable.errors import PortableBuildError
from portable.policy import is_non_runtime_debris_path


__all__ = [
    "RUNTIME_MANIFEST_RELATIVE",
    "RUNTIME_ALLOWLIST_FEATURE_ID",
    "REQUIRED_RUNTIME_ROLES",
    "validate_runtime_allowlist_payload",
    "load_runtime_allowlist",
    "validate_runtime_allowlist_sources",
    "hydrate_physical_runtime",
    "validate_physical_runtime",
]

RUNTIME_ALLOWLIST_RELATIVE = Path("PORTABLE_RUNTIME_ALLOWLIST.json")
RUNTIME_MANIFEST_RELATIVE = (
    Path("_internal")
    / "kanda_portable_runtime"
    / "physical_runtime_manifest.json"
)
RUNTIME_ALLOWLIST_FEATURE_ID = (
    "kanda-reasoner-portable-runtime-path-hash-allowlist-v1r5"
)
REQUIRED_RUNTIME_ROLES = frozenset(
    {
        "architecture_worker",
        "workflows_worker",
        "docstrings_worker",
        "architecture_grimp_probe",
        "collector_source_parts",
        "prompt_tools",
        "prompt_library",
        "freeze_blueprint_tools",
    }
)
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _allowlist_path() -> Path:
    return Path(__file__).resolve().with_name(
        RUNTIME_ALLOWLIST_RELATIVE.name
    )


def _safe_relative(value: object, label: str) -> str:
    text = str(value or "")
    if not text or "\\" in text or "\x00" in text:
        raise PortableBuildError(
            f"Runtime allowlist {label} is invalid: {text!r}"
        )
    pure = PurePosixPath(text)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise PortableBuildError(
            f"Runtime allowlist {label} escaped its root: {text!r}"
        )
    return pure.as_posix()


def validate_runtime_allowlist_payload(
    payload: object,
) -> dict[str, object]:
    """Validate an in-memory exact runtime allowlist object."""

    if not isinstance(payload, dict):
        raise PortableBuildError("Runtime allowlist is not a JSON object.")
    if payload.get("schema_version") != "1.0":
        raise PortableBuildError("Runtime allowlist schema mismatch.")
    if payload.get("feature_id") != RUNTIME_ALLOWLIST_FEATURE_ID:
        raise PortableBuildError("Runtime allowlist feature identity mismatch.")
    if payload.get("builder_feature_id") != FEATURE_ID:
        raise PortableBuildError("Runtime allowlist builder feature mismatch.")
    if payload.get("builder_version") != BUILDER_VERSION:
        raise PortableBuildError("Runtime allowlist builder version mismatch.")
    if payload.get("hardening_features") != list(PORTABLE_HARDENING_FEATURES):
        raise PortableBuildError("Runtime allowlist hardening features mismatch.")
    if payload.get("contract") != (
        "committed_exact_source_archive_path_sha256_allowlist"
    ):
        raise PortableBuildError("Runtime allowlist contract mismatch.")

    required_roles = payload.get("required_roles")
    if (
        not isinstance(required_roles, list)
        or set(map(str, required_roles)) != set(REQUIRED_RUNTIME_ROLES)
    ):
        raise PortableBuildError("Runtime allowlist required roles mismatch.")

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        raise PortableBuildError("Runtime allowlist has no items.")
    if int(payload.get("item_count", -1)) != len(items):
        raise PortableBuildError("Runtime allowlist item count mismatch.")

    normalized: list[dict[str, object]] = []
    seen_sources: set[str] = set()
    seen_archives: set[str] = set()
    roles: set[str] = set()
    for raw in items:
        if not isinstance(raw, dict):
            raise PortableBuildError("Runtime allowlist item is not an object.")
        role = str(raw.get("role") or "")
        source_relative = _safe_relative(
            raw.get("source_relative"), "source path"
        )
        archive_relative = _safe_relative(
            raw.get("archive_relative"), "archive path"
        )
        if (
            is_non_runtime_debris_path(source_relative)
            or is_non_runtime_debris_path(archive_relative)
        ):
            raise PortableBuildError(
                "Runtime allowlist contains non-runtime debris: "
                f"{source_relative}"
            )
        expected_hash = str(raw.get("sha256") or "").casefold()
        try:
            size_bytes = int(raw.get("size_bytes", -1))
        except (TypeError, ValueError) as exc:
            raise PortableBuildError(
                f"Runtime allowlist size is invalid: {source_relative}"
            ) from exc

        if role not in REQUIRED_RUNTIME_ROLES:
            raise PortableBuildError(
                f"Runtime allowlist role is invalid: {role}"
            )
        if source_relative in seen_sources:
            raise PortableBuildError(
                f"Runtime allowlist source is duplicated: {source_relative}"
            )
        if archive_relative in seen_archives:
            raise PortableBuildError(
                f"Runtime allowlist archive path is duplicated: {archive_relative}"
            )
        if not _HASH_RE.fullmatch(expected_hash):
            raise PortableBuildError(
                f"Runtime allowlist SHA-256 is invalid: {source_relative}"
            )
        if size_bytes < 0:
            raise PortableBuildError(
                f"Runtime allowlist size is invalid: {source_relative}"
            )

        seen_sources.add(source_relative)
        seen_archives.add(archive_relative)
        roles.add(role)
        normalized.append(
            {
                "role": role,
                "source_relative": source_relative,
                "archive_relative": archive_relative,
                "sha256": expected_hash,
                "size_bytes": size_bytes,
            }
        )

    missing_roles = sorted(REQUIRED_RUNTIME_ROLES - roles)
    if missing_roles:
        raise PortableBuildError(
            f"Runtime allowlist roles are missing: {missing_roles}"
        )

    expected_order = sorted(
        normalized,
        key=lambda item: (
            str(item["role"]),
            str(item["archive_relative"]),
        ),
    )
    if normalized != expected_order:
        raise PortableBuildError("Runtime allowlist item order mismatch.")

    result = deepcopy(payload)
    result["items"] = normalized
    return result


def load_runtime_allowlist() -> dict[str, object]:
    """Load the committed exact runtime allowlist."""

    path = _allowlist_path()
    if not path.is_file():
        raise PortableBuildError(
            f"Committed runtime allowlist is missing: {path}"
        )
    if path.is_symlink():
        raise PortableBuildError(
            f"Committed runtime allowlist is a symlink: {path}"
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PortableBuildError(
            f"Committed runtime allowlist is unreadable: {path}"
        ) from exc
    return validate_runtime_allowlist_payload(payload)


def validate_runtime_allowlist_sources(
    project_root: Path,
) -> dict[str, object]:
    """Require every allowlisted source path and SHA-256 to match live source."""

    project = project_root.resolve()
    payload = load_runtime_allowlist()
    for item in payload["items"]:
        source_relative = Path(str(item["source_relative"]))
        source = (project / source_relative).resolve()
        try:
            source.relative_to(project)
        except ValueError as exc:
            raise PortableBuildError(
                f"Runtime allowlist source escaped project: {source}"
            ) from exc
        if not source.is_file():
            raise PortableBuildError(
                f"Runtime allowlist source is missing: {source_relative.as_posix()}"
            )
        if source.is_symlink():
            raise PortableBuildError(
                f"Runtime allowlist source is a symlink: {source_relative.as_posix()}"
            )
        if source.stat().st_size != int(item["size_bytes"]):
            raise PortableBuildError(
                f"Runtime allowlist source size mismatch: {source_relative.as_posix()}"
            )
        if _sha256(source) != str(item["sha256"]):
            raise PortableBuildError(
                f"Runtime allowlist source SHA-256 mismatch: {source_relative.as_posix()}"
            )
    return payload


def _write_atomic_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.partial")
    try:
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        json.loads(temporary.read_text(encoding="utf-8"))
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _copy_allowlisted_item(
    *,
    project_root: Path,
    stage_app: Path,
    item: dict[str, object],
) -> dict[str, object]:
    source_relative = Path(str(item["source_relative"]))
    archive_relative = Path(str(item["archive_relative"]))
    source = (project_root / source_relative).resolve()
    try:
        source.relative_to(project_root)
    except ValueError as exc:
        raise PortableBuildError(
            f"Runtime allowlist source escaped project: {source}"
        ) from exc
    if not source.is_file():
        raise PortableBuildError(
            f"Runtime allowlist source is missing: {source_relative.as_posix()}"
        )
    if source.is_symlink():
        raise PortableBuildError(
            f"Runtime allowlist source is a symlink: {source_relative.as_posix()}"
        )
    if source.stat().st_size != int(item["size_bytes"]):
        raise PortableBuildError(
            f"Runtime allowlist source size mismatch: {source_relative.as_posix()}"
        )
    if _sha256(source) != str(item["sha256"]):
        raise PortableBuildError(
            f"Runtime allowlist source SHA-256 mismatch: {source_relative.as_posix()}"
        )

    destination = stage_app / archive_relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if destination.stat().st_size != int(item["size_bytes"]):
        raise PortableBuildError(
            f"Physical runtime destination size mismatch: {archive_relative.as_posix()}"
        )
    if _sha256(destination) != str(item["sha256"]):
        raise PortableBuildError(
            f"Physical runtime destination SHA-256 mismatch: {archive_relative.as_posix()}"
        )
    return dict(item)


def hydrate_physical_runtime(
    project_root: Path,
    stage_app: Path,
) -> Path:
    """Copy only committed allowlisted runtime files into the one-folder app."""

    project = project_root.resolve()
    payload = validate_runtime_allowlist_sources(project)
    items = [
        _copy_allowlisted_item(
            project_root=project,
            stage_app=stage_app,
            item=item,
        )
        for item in payload["items"]
    ]

    manifest_path = stage_app / RUNTIME_MANIFEST_RELATIVE
    manifest: dict[str, object] = {
        "schema_version": "1.0",
        "builder_version": BUILDER_VERSION,
        "feature_id": FEATURE_ID,
        "runtime_allowlist_feature_id": RUNTIME_ALLOWLIST_FEATURE_ID,
        "runtime_allowlist_sha256": _sha256(_allowlist_path()),
        "required_roles": sorted(REQUIRED_RUNTIME_ROLES),
        "item_count": len(items),
        "items": items,
    }
    _write_atomic_json(manifest_path, manifest)
    validate_physical_runtime(stage_app)

    print(f"PORTABLE PHYSICAL RUNTIME FILE COUNT: {len(items)}")
    print("PORTABLE RUNTIME ALLOWLIST EXACT SOURCE PATHS: PASS")
    print("PORTABLE RUNTIME ALLOWLIST EXACT ARCHIVE PATHS: PASS")
    print("PORTABLE RUNTIME ALLOWLIST EXACT SHA-256: PASS")
    print("PORTABLE ARCHITECTURE WORKER PHYSICAL FILE: PASS")
    print("PORTABLE WORKFLOWS WORKER PHYSICAL FILE: PASS")
    print("PORTABLE DOCSTRINGS WORKER PHYSICAL FILE: PASS")
    print("PORTABLE COLLECTOR SOURCE PARTS PHYSICAL FILES: PASS")
    print("PORTABLE GRIMP PROBE PHYSICAL FILE: PASS")
    print("PORTABLE FREEZE BLUEPRINT TOOLS PHYSICAL FILES: PASS")
    print("PORTABLE PROMPT WORKSPACE PHYSICAL FILES: PASS")
    return manifest_path


def validate_physical_runtime(stage_app: Path) -> dict[str, object]:
    """Validate staged files against the committed runtime allowlist."""

    allowlist = load_runtime_allowlist()
    manifest_path = stage_app / RUNTIME_MANIFEST_RELATIVE
    if not manifest_path.is_file():
        raise PortableBuildError(
            f"Physical runtime manifest is missing: {manifest_path}"
        )
    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8-sig")
    )
    if manifest.get("builder_version") != BUILDER_VERSION:
        raise PortableBuildError(
            "Physical runtime manifest builder version mismatch."
        )
    if manifest.get("feature_id") != FEATURE_ID:
        raise PortableBuildError(
            "Physical runtime manifest feature identity mismatch."
        )
    if manifest.get("runtime_allowlist_feature_id") != (
        RUNTIME_ALLOWLIST_FEATURE_ID
    ):
        raise PortableBuildError(
            "Physical runtime manifest allowlist identity mismatch."
        )
    if manifest.get("runtime_allowlist_sha256") != _sha256(
        _allowlist_path()
    ):
        raise PortableBuildError(
            "Physical runtime manifest allowlist SHA-256 mismatch."
        )
    if manifest.get("required_roles") != sorted(REQUIRED_RUNTIME_ROLES):
        raise PortableBuildError(
            "Physical runtime manifest roles mismatch."
        )
    items = manifest.get("items")
    if items != allowlist["items"]:
        raise PortableBuildError(
            "Physical runtime manifest does not exactly match the allowlist."
        )
    if int(manifest.get("item_count", -1)) != len(items):
        raise PortableBuildError(
            "Physical runtime manifest item count mismatch."
        )

    for item in items:
        archive_relative = Path(str(item["archive_relative"]))
        path = stage_app / archive_relative
        if not path.is_file():
            raise PortableBuildError(
                f"Physical runtime file is missing: {archive_relative.as_posix()}"
            )
        if path.is_symlink():
            raise PortableBuildError(
                f"Physical runtime file is a symlink: {archive_relative.as_posix()}"
            )
        if path.stat().st_size != int(item["size_bytes"]):
            raise PortableBuildError(
                f"Physical runtime file size mismatch: {archive_relative.as_posix()}"
            )
        if _sha256(path) != str(item["sha256"]):
            raise PortableBuildError(
                f"Physical runtime file hash mismatch: {archive_relative.as_posix()}"
            )

    print("PORTABLE PHYSICAL RUNTIME MANIFEST: PASS")
    print("PORTABLE PHYSICAL RUNTIME EXACT HASHES: PASS")
    print("PORTABLE PHYSICAL RUNTIME REQUIRED ROLES: PASS")
    print("PORTABLE RUNTIME COMMITTED ALLOWLIST: PASS")
    return manifest
