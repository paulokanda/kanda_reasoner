"""Manage the local-AI working copy of the complete JSON.

This module is an isolated Project Reasoner box.

The canonical complete JSON is created by the official app workflow:
4. Fourth step: collect project structure.

This module never creates or edits the canonical complete JSON. It only reads it
and creates or refreshes a separate local-AI working copy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    primary_evidence_json_path,
    relative_primary_evidence_json_path,
    relative_working_copy_json_path,
    relative_working_copy_metadata_path,
    working_copy_json_path,
    working_copy_metadata_path,
)

DEFAULT_CANONICAL_RELATIVE_PATH = relative_primary_evidence_json_path()
DEFAULT_LOCAL_AI_RELATIVE_PATH = relative_working_copy_json_path()
DEFAULT_METADATA_RELATIVE_PATH = relative_working_copy_metadata_path()


@dataclass(frozen=True)
class LocalAIJsonPaths:
    """Resolved paths for the canonical JSON and the local-AI working copy."""

    project_root: Path
    canonical_json: Path
    local_ai_json: Path
    metadata_json: Path


@dataclass(frozen=True)
class LocalAIJsonCopyResult:
    """Result returned by local-AI JSON copy operations."""

    action: str
    canonical_json: str
    local_ai_json: str
    metadata_json: str
    canonical_exists: bool
    local_ai_exists: bool
    metadata_exists: bool
    canonical_sha256: str
    local_ai_sha256: str
    metadata_sha256: str
    canonical_size_bytes: int
    local_ai_size_bytes: int
    metadata_size_bytes: int
    hashes_match: bool
    local_is_stale: bool
    bytes_copied: int
    message: str


def build_default_paths(project_root: str | Path) -> LocalAIJsonPaths:
    """Build the default JSON paths for the selected project root."""
    root = Path(project_root).resolve()
    return LocalAIJsonPaths(
        project_root=root,
        canonical_json=primary_evidence_json_path(root).resolve(),
        local_ai_json=working_copy_json_path(root).resolve(),
        metadata_json=working_copy_metadata_path(root).resolve(),
    )


def _paths_from_optional_relatives(
    project_root: str | Path,
    *,
    canonical_relative_path: str | None = None,
    local_ai_relative_path: str | None = None,
    metadata_relative_path: str | None = None,
) -> LocalAIJsonPaths:
    """Resolve explicit relative paths or dynamic project-root defaults."""
    root = Path(project_root).resolve()
    defaults = build_default_paths(root)
    canonical = (
        defaults.canonical_json
        if canonical_relative_path is None
        else (root / canonical_relative_path).resolve()
    )
    local_ai = (
        defaults.local_ai_json
        if local_ai_relative_path is None
        else (root / local_ai_relative_path).resolve()
    )
    metadata = (
        defaults.metadata_json
        if metadata_relative_path is None
        else (root / metadata_relative_path).resolve()
    )
    return LocalAIJsonPaths(
        project_root=root,
        canonical_json=canonical,
        local_ai_json=local_ai,
        metadata_json=metadata,
    )


def _sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for a file, or an empty string if missing."""
    if not path.exists() or not path.is_file():
        return ""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_size(path: Path) -> int:
    """Return file size in bytes, or zero if the file is missing."""
    if not path.exists() or not path.is_file():
        return 0
    return int(path.stat().st_size)


def _validate_paths(paths: LocalAIJsonPaths) -> None:
    """Validate path safety before reading or writing."""
    if not paths.canonical_json.exists():
        raise FileNotFoundError(
            "Canonical complete JSON not found: " + str(paths.canonical_json)
        )

    if not paths.canonical_json.is_file():
        raise ValueError(
            "Canonical complete JSON path is not a file: "
            + str(paths.canonical_json)
        )

    if paths.canonical_json == paths.local_ai_json:
        raise ValueError("Canonical and local-AI JSON paths must be different.")

    if paths.canonical_json == paths.metadata_json:
        raise ValueError("Metadata path must not equal canonical JSON path.")

    try:
        paths.canonical_json.relative_to(paths.project_root)
        paths.local_ai_json.relative_to(paths.project_root)
        paths.metadata_json.relative_to(paths.project_root)
    except ValueError as exc:
        raise ValueError("All JSON paths must remain inside project_root.") from exc


def _copy_file_atomic(source: Path, destination: Path) -> int:
    """Copy source to destination using a temporary file and atomic replace."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = destination.with_name(destination.name + ".tmp_copy")

    if temp_path.exists():
        temp_path.unlink()

    try:
        shutil.copy2(source, temp_path)
        size = temp_path.stat().st_size
        temp_path.replace(destination)
        return size
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _result(
    *,
    action: str,
    paths: LocalAIJsonPaths,
    bytes_copied: int,
    message: str,
) -> LocalAIJsonCopyResult:
    """Build a structured operation result."""
    canonical_sha256 = _sha256_file(paths.canonical_json)
    local_ai_sha256 = _sha256_file(paths.local_ai_json)
    metadata_sha256 = _sha256_file(paths.metadata_json)

    canonical_exists = paths.canonical_json.exists()
    local_ai_exists = paths.local_ai_json.exists()
    metadata_exists = paths.metadata_json.exists()

    hashes_match = (
        bool(canonical_sha256)
        and bool(local_ai_sha256)
        and canonical_sha256 == local_ai_sha256
    )
    local_is_stale = (
        canonical_exists
        and local_ai_exists
        and bool(canonical_sha256)
        and bool(local_ai_sha256)
        and canonical_sha256 != local_ai_sha256
    )

    return LocalAIJsonCopyResult(
        action=action,
        canonical_json=str(paths.canonical_json),
        local_ai_json=str(paths.local_ai_json),
        metadata_json=str(paths.metadata_json),
        canonical_exists=canonical_exists,
        local_ai_exists=local_ai_exists,
        metadata_exists=metadata_exists,
        canonical_sha256=canonical_sha256,
        local_ai_sha256=local_ai_sha256,
        metadata_sha256=metadata_sha256,
        canonical_size_bytes=_file_size(paths.canonical_json),
        local_ai_size_bytes=_file_size(paths.local_ai_json),
        metadata_size_bytes=_file_size(paths.metadata_json),
        hashes_match=hashes_match,
        local_is_stale=local_is_stale,
        bytes_copied=bytes_copied,
        message=message,
    )


def write_local_ai_copy_metadata(
    paths: LocalAIJsonPaths,
    result: LocalAIJsonCopyResult,
) -> None:
    """Write sidecar metadata for the local-AI working copy.

    The metadata is separate from the local-AI JSON so this gate does not change
    the JSON schema.
    """
    paths.metadata_json.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "box": "Local-AI JSON Working Copy Box",
        "created_by": (
            "kanda_reasoner_app.local_ai_json_working_copy.copy_manager"
        ),
        "timestamp_utc_seconds": time.time(),
        "canonical_json": result.canonical_json,
        "local_ai_json": result.local_ai_json,
        "canonical_sha256": result.canonical_sha256,
        "local_ai_sha256": result.local_ai_sha256,
        "canonical_size_bytes": result.canonical_size_bytes,
        "local_ai_size_bytes": result.local_ai_size_bytes,
        "hashes_match": result.hashes_match,
        "local_is_stale": result.local_is_stale,
        "action": result.action,
        "message": result.message,
        "rule": (
            "Canonical complete JSON is created only by the official app "
            "workflow. Local AI uses this parallel working copy."
        ),
    }
    paths.metadata_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def ensure_local_ai_copy(
    project_root: str | Path,
    *,
    canonical_relative_path: str | None = None,
    local_ai_relative_path: str | None = None,
    metadata_relative_path: str | None = None,
) -> LocalAIJsonCopyResult:
    """Create the local-AI working copy only when it is missing."""
    paths = _paths_from_optional_relatives(
        project_root,
        canonical_relative_path=canonical_relative_path,
        local_ai_relative_path=local_ai_relative_path,
        metadata_relative_path=metadata_relative_path,
    )
    _validate_paths(paths)

    if paths.local_ai_json.exists():
        result = _result(
            action="status",
            paths=paths,
            bytes_copied=0,
            message="Local-AI JSON already exists. No copy performed.",
        )
        write_local_ai_copy_metadata(paths, result)
        return result

    copied = _copy_file_atomic(paths.canonical_json, paths.local_ai_json)
    result = _result(
        action="created",
        paths=paths,
        bytes_copied=copied,
        message="Created local-AI working JSON from canonical complete JSON.",
    )
    write_local_ai_copy_metadata(paths, result)
    return result


def refresh_local_ai_copy(
    project_root: str | Path,
    *,
    canonical_relative_path: str | None = None,
    local_ai_relative_path: str | None = None,
    metadata_relative_path: str | None = None,
) -> LocalAIJsonCopyResult:
    """Explicitly refresh the local-AI copy from the canonical complete JSON."""
    paths = _paths_from_optional_relatives(
        project_root,
        canonical_relative_path=canonical_relative_path,
        local_ai_relative_path=local_ai_relative_path,
        metadata_relative_path=metadata_relative_path,
    )
    _validate_paths(paths)

    copied = _copy_file_atomic(paths.canonical_json, paths.local_ai_json)
    result = _result(
        action="refreshed",
        paths=paths,
        bytes_copied=copied,
        message="Refreshed local-AI working JSON from canonical complete JSON.",
    )
    write_local_ai_copy_metadata(paths, result)
    return result


def get_local_ai_copy_status(
    project_root: str | Path,
    *,
    canonical_relative_path: str | None = None,
    local_ai_relative_path: str | None = None,
    metadata_relative_path: str | None = None,
) -> LocalAIJsonCopyResult:
    """Return status for the canonical JSON and local-AI working copy."""
    paths = _paths_from_optional_relatives(
        project_root,
        canonical_relative_path=canonical_relative_path,
        local_ai_relative_path=local_ai_relative_path,
        metadata_relative_path=metadata_relative_path,
    )

    if paths.canonical_json == paths.local_ai_json:
        raise ValueError("Canonical and local-AI JSON paths must be different.")

    return _result(
        action="status",
        paths=paths,
        bytes_copied=0,
        message="Local-AI JSON copy status only. No file copied.",
    )


def _print_result(result: LocalAIJsonCopyResult) -> None:
    """Print a plain text operation result."""
    print("LOCAL-AI JSON COPY RESULT")
    print("action:", result.action)
    print("message:", result.message)
    print("canonical_json:", result.canonical_json)
    print("local_ai_json:", result.local_ai_json)
    print("metadata_json:", result.metadata_json)
    print("canonical_exists:", result.canonical_exists)
    print("local_ai_exists:", result.local_ai_exists)
    print("metadata_exists:", result.metadata_exists)
    print("canonical_sha256:", result.canonical_sha256)
    print("local_ai_sha256:", result.local_ai_sha256)
    print("metadata_sha256:", result.metadata_sha256)
    print("canonical_size_bytes:", result.canonical_size_bytes)
    print("local_ai_size_bytes:", result.local_ai_size_bytes)
    print("metadata_size_bytes:", result.metadata_size_bytes)
    print("hashes_match:", result.hashes_match)
    print("local_is_stale:", result.local_is_stale)
    print("bytes_copied:", result.bytes_copied)


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point for the Local-AI JSON Working Copy Box."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root. Default: current directory.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print status without copying.",
    )
    parser.add_argument(
        "--ensure",
        action="store_true",
        help="Create local-AI JSON only if it is missing.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Explicitly refresh local-AI JSON from canonical JSON.",
    )
    args = parser.parse_args(argv)

    selected = sum(bool(item) for item in (args.status, args.ensure, args.refresh))
    if selected != 1:
        print("Choose exactly one action: --status, --ensure, or --refresh")
        return 2

    try:
        if args.status:
            result = get_local_ai_copy_status(args.project_root)
        elif args.ensure:
            result = ensure_local_ai_copy(args.project_root)
        else:
            result = refresh_local_ai_copy(args.project_root)
    except Exception as exc:
        print("LOCAL-AI JSON COPY ERROR")
        print(type(exc).__name__ + ": " + str(exc))
        return 1

    _print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
