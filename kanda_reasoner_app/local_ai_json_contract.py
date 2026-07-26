# project-path: kanda_reasoner_app/local_ai_json_contract.py
"""Canonical Local-AI JSON working-copy contract.

This module owns the local-only working copy of the generated complete JSON.
The canonical web-AI JSON remains the source artifact generated for the selected
project root.  The local-AI JSON may be created or refreshed from that canonical
file, but the canonical file is never overwritten by this module.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    ensure_project_analysis_evidence_dirs,
    primary_evidence_json_path,
    working_copy_json_path,
    working_copy_metadata_path,
)

__all__ = [
    "LocalAIJsonCopyPaths",
    "LocalAIJsonCopyResult",
    "build_default_paths",
    "ensure_local_ai_copy",
    "refresh_local_ai_copy",
]


@dataclass(frozen=True)
class LocalAIJsonCopyPaths:
    """Resolved canonical and local-AI JSON paths for one project root."""

    project_root: Path
    canonical_json: Path
    local_ai_json: Path
    metadata_json: Path


@dataclass(frozen=True)
class LocalAIJsonCopyResult:
    """Result returned by local-AI JSON copy operations."""

    action: str
    project_root: str
    canonical_json: str
    local_ai_json: str
    metadata_json: str
    canonical_sha256: str
    local_ai_sha256: str
    hashes_match: bool
    local_is_stale: bool
    bytes_copied: int
    message: str


def _sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_default_paths(project_root: str | Path) -> LocalAIJsonCopyPaths:
    """Return the canonical/local-AI JSON paths for project_root."""
    root = Path(project_root).expanduser().resolve(strict=False)
    ensure_project_analysis_evidence_dirs(root)
    return LocalAIJsonCopyPaths(
        project_root=root,
        canonical_json=primary_evidence_json_path(root),
        local_ai_json=working_copy_json_path(root),
        metadata_json=working_copy_metadata_path(root),
    )


def _validate_source(paths: LocalAIJsonCopyPaths) -> None:
    """Validate that the canonical JSON exists and paths are distinct."""
    if paths.canonical_json == paths.local_ai_json:
        raise ValueError("Canonical and local-AI JSON paths must be different.")
    if not paths.canonical_json.exists() or not paths.canonical_json.is_file():
        raise FileNotFoundError(
            "Canonical complete JSON not found: " + str(paths.canonical_json)
        )


def _write_metadata(paths: LocalAIJsonCopyPaths, result: LocalAIJsonCopyResult) -> None:
    """Write local-AI copy metadata next to the local-AI JSON file."""
    payload = asdict(result)
    payload["schema_version"] = "1.0"
    payload["kind"] = "local_ai_json_copy_metadata"
    payload["updated_utc_seconds"] = time.time()
    paths.metadata_json.parent.mkdir(parents=True, exist_ok=True)
    paths.metadata_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _build_result(
    paths: LocalAIJsonCopyPaths,
    *,
    action: str,
    bytes_copied: int,
    message: str,
) -> LocalAIJsonCopyResult:
    """Build a result object after a copy or no-op decision."""
    canonical_hash = _sha256_file(paths.canonical_json)
    local_hash = _sha256_file(paths.local_ai_json) if paths.local_ai_json.exists() else ""
    hashes_match = bool(local_hash) and canonical_hash == local_hash
    return LocalAIJsonCopyResult(
        action=action,
        project_root=str(paths.project_root),
        canonical_json=str(paths.canonical_json),
        local_ai_json=str(paths.local_ai_json),
        metadata_json=str(paths.metadata_json),
        canonical_sha256=canonical_hash,
        local_ai_sha256=local_hash,
        hashes_match=hashes_match,
        local_is_stale=not hashes_match,
        bytes_copied=bytes_copied,
        message=message,
    )


def _copy_canonical_to_local(paths: LocalAIJsonCopyPaths, *, action: str) -> LocalAIJsonCopyResult:
    """Atomically copy canonical JSON bytes to the local-AI JSON path."""
    _validate_source(paths)
    paths.local_ai_json.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb",
            delete=False,
            dir=str(paths.local_ai_json.parent),
            prefix=paths.local_ai_json.name + ".",
            suffix=".tmp",
        ) as handle:
            temp_path = Path(handle.name)
            with paths.canonical_json.open("rb") as source:
                shutil.copyfileobj(source, handle, length=1024 * 1024)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, paths.local_ai_json)
        temp_path = None
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)
    size_bytes = paths.local_ai_json.stat().st_size
    result = _build_result(
        paths,
        action=action,
        bytes_copied=size_bytes,
        message="Local-AI JSON copy refreshed from canonical complete JSON.",
    )
    _write_metadata(paths, result)
    return result


def ensure_local_ai_copy(project_root: str | Path) -> LocalAIJsonCopyResult:
    """Create the local-AI JSON copy when it is missing.

    Existing local-AI JSON is preserved so local-only enrichment is not lost.
    Use refresh_local_ai_copy when an explicit overwrite is intended.
    """
    paths = build_default_paths(project_root)
    _validate_source(paths)
    if paths.local_ai_json.exists() and paths.local_ai_json.is_file():
        result = _build_result(
            paths,
            action="unchanged",
            bytes_copied=0,
            message="Local-AI JSON copy already exists; no overwrite performed.",
        )
        _write_metadata(paths, result)
        return result
    return _copy_canonical_to_local(paths, action="created")


def refresh_local_ai_copy(project_root: str | Path) -> LocalAIJsonCopyResult:
    """Overwrite the local-AI JSON copy from the canonical complete JSON."""
    paths = build_default_paths(project_root)
    return _copy_canonical_to_local(paths, action="refreshed")
