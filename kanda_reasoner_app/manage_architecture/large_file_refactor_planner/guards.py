# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/guards.py
"""No-leak write and staleness gates for the large-file planner."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

from .models import FEATURE_ID, SCHEMA_VERSION, SourceSnapshot

__all__ = [
    "FORBIDDEN_PATH_FRAGMENTS",
    "NoLeakWriteError",
    "StaleSourceError",
    "assert_source_fresh",
    "assert_within_allowed_roots",
    "compute_content_hash",
    "make_source_snapshot",
    "safe_mkdir",
    "safe_write_bytes",
    "safe_write_text",
]


class NoLeakWriteError(ValueError):
    """Raised when a planner write would leave an allowed root."""


class StaleSourceError(RuntimeError):
    """Raised when a source file changed after analysis."""


FORBIDDEN_PATH_FRAGMENTS = (
    "first_prompts_to_ai.zip",
    "prompt_library.zip",
    "project_freeze_after_update/frozen_features_memory",
    "project_freeze_ledger",
    "show_project_to_AI/project_error_memory",
)


def compute_content_hash(path: Path) -> str:
    """Compute a SHA-256 hash for a source file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_source_snapshot(path: Path) -> SourceSnapshot:
    """Create a source snapshot for later staleness checks."""
    resolved = path.expanduser().resolve()
    stat = resolved.stat()
    return SourceSnapshot(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        source_path=str(resolved),
        source_size=stat.st_size,
        source_mtime_ns=stat.st_mtime_ns,
        source_content_hash=compute_content_hash(resolved),
    )


def assert_source_fresh(path: Path, expected: SourceSnapshot) -> None:
    """Raise when the current source fingerprint no longer matches."""
    current = make_source_snapshot(path)
    if current.source_content_hash != expected.source_content_hash:
        raise StaleSourceError("Source hash changed after analysis.")
    if current.source_size != expected.source_size:
        raise StaleSourceError("Source size changed after analysis.")
    if current.source_mtime_ns != expected.source_mtime_ns:
        raise StaleSourceError("Source modified time changed after analysis.")


def assert_within_allowed_roots(
    path: Path,
    allowed_roots: Iterable[Path],
    purpose: str,
) -> Path:
    """Validate that a write path remains inside one allowed root."""
    resolved = path.expanduser().resolve()
    normalized = str(resolved).replace("\\", "/")
    lowered = normalized.lower()
    for fragment in FORBIDDEN_PATH_FRAGMENTS:
        if fragment.lower() in lowered:
            raise NoLeakWriteError(
                f"Blocked generated/evidence path for {purpose}: {resolved}"
            )
    roots = [root.expanduser().resolve() for root in allowed_roots]
    for root in roots:
        try:
            resolved.relative_to(root)
        except ValueError:
            continue
        return resolved
    root_text = ", ".join(str(root) for root in roots) or "<none>"
    raise NoLeakWriteError(
        f"Path is outside allowed roots for {purpose}: {resolved}; roots={root_text}"
    )


def safe_mkdir(path: Path, allowed_roots: Iterable[Path], purpose: str) -> Path:
    """Create a directory after applying the no-leak write gate."""
    resolved = assert_within_allowed_roots(path, allowed_roots, purpose)
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def safe_write_text(
    path: Path,
    text: str,
    allowed_roots: Iterable[Path],
    purpose: str,
) -> Path:
    """Write UTF-8 text after applying the no-leak write gate."""
    resolved = assert_within_allowed_roots(path, allowed_roots, purpose)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(text, encoding="utf-8")
    return resolved


def safe_write_bytes(
    path: Path,
    data: bytes,
    allowed_roots: Iterable[Path],
    purpose: str,
) -> Path:
    """Write bytes after applying the no-leak write gate."""
    resolved = assert_within_allowed_roots(path, allowed_roots, purpose)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_bytes(data)
    return resolved
