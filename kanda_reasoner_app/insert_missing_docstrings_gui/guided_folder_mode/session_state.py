
"""Persistence helpers for guided folder-by-folder docstring sessions."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .models import FolderQueueItem, GuidedFolderSession
from .queue import discover_python_folders


DEFAULT_SESSION_FILENAME = ".docstring_guided_session.json"


def create_guided_session(
    project_root: str | Path,
    settings: dict[str, Any] | None = None,
) -> GuidedFolderSession:
    """Create a guided folder session from the current project tree."""
    root = Path(project_root).resolve()
    queue = discover_python_folders(root)
    return GuidedFolderSession(
        project_root=str(root),
        folder_queue=queue,
        current_index=0,
        settings=dict(settings or {}),
        last_report_path="",
    )


def session_to_dict(session: GuidedFolderSession) -> dict[str, Any]:
    """Convert a guided session to JSON-compatible data."""
    return {
        "project_root": session.project_root,
        "folder_queue": [asdict(item) for item in session.folder_queue],
        "current_index": session.current_index,
        "settings": dict(session.settings),
        "last_report_path": session.last_report_path,
    }


def session_from_dict(data: dict[str, Any]) -> GuidedFolderSession:
    """Create a guided session from JSON-compatible data."""
    queue = tuple(
        FolderQueueItem(
            relative_path=str(item.get("relative_path", ".")),
            python_files=tuple(str(value) for value in item.get("python_files", [])),
            state=str(item.get("state", "not_started")),
            error=str(item.get("error", "")),
        )
        for item in data.get("folder_queue", [])
    )
    return GuidedFolderSession(
        project_root=str(data.get("project_root", "")),
        folder_queue=queue,
        current_index=int(data.get("current_index", 0)),
        settings=dict(data.get("settings", {})),
        last_report_path=str(data.get("last_report_path", "")),
    )


def save_guided_session(
    session: GuidedFolderSession,
    path: str | Path | None = None,
) -> Path:
    """Write a guided session JSON file and return its path."""
    target = Path(path) if path is not None else Path(session.project_root) / DEFAULT_SESSION_FILENAME
    text = json.dumps(session_to_dict(session), indent=2, sort_keys=True)
    target.write_text(text + "\n", encoding="utf-8")
    return target


def load_guided_session(path: str | Path) -> GuidedFolderSession:
    """Load a guided session JSON file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Guided session file must contain a JSON object.")
    return session_from_dict(data)


def with_current_index(session: GuidedFolderSession, current_index: int) -> GuidedFolderSession:
    """Return a session copy with a new current index."""
    return GuidedFolderSession(
        project_root=session.project_root,
        folder_queue=session.folder_queue,
        current_index=current_index,
        settings=dict(session.settings),
        last_report_path=session.last_report_path,
    )


def with_folder_queue(
    session: GuidedFolderSession,
    folder_queue: tuple[FolderQueueItem, ...],
) -> GuidedFolderSession:
    """Return a session copy with an updated folder queue."""
    return GuidedFolderSession(
        project_root=session.project_root,
        folder_queue=folder_queue,
        current_index=session.current_index,
        settings=dict(session.settings),
        last_report_path=session.last_report_path,
    )
