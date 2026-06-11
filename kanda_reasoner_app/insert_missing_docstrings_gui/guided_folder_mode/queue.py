
"""Folder discovery and queue creation for guided docstring sessions."""

from __future__ import annotations

from pathlib import Path

from .models import FolderQueueItem


DEFAULT_EXCLUDED_DIR_NAMES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "site-packages",
    "venv",
}


def _is_excluded_dir(path: Path, excluded_dir_names: set[str]) -> bool:
    """Return True when path should not be scanned as a guided folder."""
    return any(part in excluded_dir_names for part in path.parts)


def _relative_posix(root: Path, path: Path) -> str:
    """Return a stable project-relative path string."""
    rel = path.relative_to(root)
    value = rel.as_posix()
    return "." if value == "." else value


def discover_python_folders(
    project_root: str | Path,
    excluded_dir_names: set[str] | None = None,
) -> tuple[FolderQueueItem, ...]:
    """Discover folders that contain Python source files.

    The returned queue is deterministic and contains one item per folder that
    directly contains at least one Python file. Excluded directories are skipped
    before file collection.
    """
    root = Path(project_root).resolve()
    excluded = set(DEFAULT_EXCLUDED_DIR_NAMES)
    if excluded_dir_names:
        excluded.update(excluded_dir_names)

    folder_to_files: dict[Path, list[str]] = {}

    for path in sorted(root.rglob("*.py")):
        if _is_excluded_dir(path.relative_to(root).parent, excluded):
            continue
        if path.name.startswith("."):
            continue
        folder = path.parent
        folder_to_files.setdefault(folder, []).append(_relative_posix(root, path))

    queue: list[FolderQueueItem] = []
    for folder in sorted(folder_to_files):
        queue.append(
            FolderQueueItem(
                relative_path=_relative_posix(root, folder),
                python_files=tuple(sorted(folder_to_files[folder])),
            )
        )

    return tuple(queue)


def get_current_item(queue: tuple[FolderQueueItem, ...], current_index: int) -> FolderQueueItem | None:
    """Return the current queue item when current_index is valid."""
    if current_index < 0 or current_index >= len(queue):
        return None
    return queue[current_index]


def replace_queue_item(
    queue: tuple[FolderQueueItem, ...],
    index: int,
    item: FolderQueueItem,
) -> tuple[FolderQueueItem, ...]:
    """Return a queue copy with one item replaced."""
    if index < 0 or index >= len(queue):
        raise IndexError("Folder queue index is out of range.")
    items = list(queue)
    items[index] = item
    return tuple(items)


def mark_folder_state(
    queue: tuple[FolderQueueItem, ...],
    index: int,
    state: str,
    error: str = "",
) -> tuple[FolderQueueItem, ...]:
    """Return a queue copy with the indexed folder state changed."""
    current = get_current_item(queue, index)
    if current is None:
        raise IndexError("Folder queue index is out of range.")

    updated = FolderQueueItem(
        relative_path=current.relative_path,
        python_files=current.python_files,
        state=state,
        error=error,
    )
    return replace_queue_item(queue, index, updated)
