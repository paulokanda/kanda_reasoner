"""Resolve the Project Q&A JSON path from the selected project root.

This helper belongs to the Project Q&A path-selection box.  It may use the
shared evidence-path contract, but it must not derive project artifacts from the
tool package root.  The selected project root is the only source of truth.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    primary_evidence_json_path,
    project_analysis_evidence_root,
    working_copy_json_path,
)

__all__ = [
    "ProjectJsonPathResolution",
    "current_project_root_from_window",
    "is_deprecated_project_json_path",
    "resolve_project_json_path",
    "should_replace_project_json_path",
]


_DEPRECATED_DEVELOPER_TOOLS_JSON_DIR = (
    "developer_tools/dev_tools_docs/json_complete"
)
_DEPRECATED_DEVELOPER_TOOLS_JSON_FILENAMES = {
    "developer_tools__complete.json",
    "developer_tools__complete_local_ai.json",
}


@dataclass(frozen=True)
class ProjectJsonPathResolution:
    """Resolved Project Q&A JSON paths for one selected project."""

    project_root: Path
    evidence_root: Path
    canonical_json: Path
    local_ai_json: Path
    selected_json: Path
    selected_kind: str


def _widget_text(widget: Any) -> str:
    """Return stripped text from a Qt-like widget or plain value."""
    if widget is None:
        return ""
    text_attr = getattr(widget, "text", None)
    if callable(text_attr):
        return str(text_attr()).strip()
    return str(widget).strip()


def _normalize_for_compare(path: str | Path) -> str:
    """Return a stable path string for equality checks without requiring files."""
    raw = str(path or "").strip()
    if not raw:
        return ""
    resolved = Path(raw).expanduser().resolve(strict=False)
    return os.path.normcase(os.path.normpath(str(resolved)))


def _same_path(first: str | Path, second: str | Path) -> bool:
    """Return True when two path strings resolve to the same location."""
    return _normalize_for_compare(first) == _normalize_for_compare(second)


def current_project_root_from_window(window: Any) -> Path | None:
    """Return the selected project root from the Project Q&A window, if any."""
    direct_text = _widget_text(getattr(window, "project_root_edit", None))
    if direct_text:
        return Path(direct_text).expanduser().resolve(strict=False)

    project_index = getattr(window, "project_index", None)
    indexed_root = str(getattr(project_index, "project_root", "") or "").strip()
    if indexed_root:
        return Path(indexed_root).expanduser().resolve(strict=False)

    return None


def is_deprecated_project_json_path(path_text: str) -> bool:
    """Return True for the old developer_tools Project Q&A JSON path."""
    normalized = str(path_text or "").replace("\\", "/").strip().lower()
    if not normalized:
        return False
    name = normalized.rsplit("/", 1)[-1]
    return (
        _DEPRECATED_DEVELOPER_TOOLS_JSON_DIR in normalized
        or (
            "/dev_tools_docs/json_complete/" in normalized
            and name in _DEPRECATED_DEVELOPER_TOOLS_JSON_FILENAMES
        )
    )


def resolve_project_json_path(project_root: str | Path) -> ProjectJsonPathResolution:
    """Resolve the JSON path that Project Q&A should show for project_root."""
    root = Path(project_root).expanduser().resolve(strict=False)
    canonical_json = primary_evidence_json_path(root)
    local_ai_json = working_copy_json_path(root)
    evidence_root = project_analysis_evidence_root(root)

    if local_ai_json.is_file():
        selected_json = local_ai_json
        selected_kind = "local-ai"
    elif canonical_json.is_file():
        selected_json = canonical_json
        selected_kind = "canonical"
    else:
        selected_json = local_ai_json
        selected_kind = "expected-local-ai"

    return ProjectJsonPathResolution(
        project_root=root,
        evidence_root=evidence_root,
        canonical_json=canonical_json,
        local_ai_json=local_ai_json,
        selected_json=selected_json,
        selected_kind=selected_kind,
    )


def _is_project_expected_json_path(
    current_path: str,
    resolution: ProjectJsonPathResolution,
) -> bool:
    """Return True if current_path is one of this project's expected JSON files."""
    return _same_path(current_path, resolution.canonical_json) or _same_path(
        current_path,
        resolution.local_ai_json,
    )


def should_replace_project_json_path(
    current_path: str,
    resolution: ProjectJsonPathResolution,
    *,
    force: bool = False,
) -> bool:
    """Return True when the JSON field should be reset for this project."""
    current = str(current_path or "").strip()
    if force:
        return True
    if not current:
        return True
    if is_deprecated_project_json_path(current):
        return True
    if not Path(current).expanduser().is_file():
        return not _same_path(current, resolution.selected_json)
    if not _is_project_expected_json_path(current, resolution):
        return True
    if resolution.local_ai_json.is_file() and not _same_path(
        current,
        resolution.local_ai_json,
    ):
        return True
    return False
