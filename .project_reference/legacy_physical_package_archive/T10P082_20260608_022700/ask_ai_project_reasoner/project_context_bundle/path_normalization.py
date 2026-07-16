"""Path normalization helpers for the project context bundle box."""

from __future__ import annotations

from pathlib import Path

__all__ = ["relative_posix_path", "safe_resolve", "to_posix_path"]


def safe_resolve(path: str | Path) -> Path:
    """Resolve a path without failing on paths that do not yet exist."""
    return Path(path).expanduser().resolve(strict=False)


def to_posix_path(path: str | Path) -> str:
    """Return a stable POSIX-style string for JSON output."""
    return str(path).replace("\\", "/")


def relative_posix_path(path: str | Path, root: str | Path) -> str:
    """Return path relative to root using POSIX separators.

    Raises ValueError when path is outside root. This protects snapshot and
    bundle logic from writing or reporting paths outside the active project.
    """
    resolved_path = safe_resolve(path)
    resolved_root = safe_resolve(root)
    try:
        relative = resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("Path is outside the project root: " + str(path)) from exc
    return relative.as_posix()
