"""Inactive reference-folder policy for Project Symbol Atlas.

Reference folders contain memos, comments, historical notes, archived
material, or migration-only evidence. They are not active project source and
must not become edit targets, main/helper paths, related active files, or test
recommendations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS = (
    ".project_reference",
    "_project_reference",
    "project_freeze_ledger",
)
_CANONICAL_EVIDENCE_FOLDER_NAME = "project_analysis_evidence"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS",
    "build_reasoner_symbol_atlas_reference_path_markers",
    "is_reasoner_symbol_atlas_reference_path",
    "iter_reasoner_symbol_atlas_reference_evidence_dirs",
    "normalize_reasoner_symbol_atlas_policy_path",
]


def normalize_reasoner_symbol_atlas_policy_path(value: str | Path) -> str:
    """Return a normalized path-like string for reference-folder checks."""

    return str(value or "").strip().strip("`\"'").replace("\\", "/")


def build_reasoner_symbol_atlas_reference_path_markers(
    folder_names: Iterable[str] | None = None,
) -> tuple[str, ...]:
    """Return path markers that identify inactive reference folders."""

    markers: list[str] = []
    for folder in folder_names or PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS:
        cleaned = str(folder or "").strip().strip("/\\")
        if not cleaned:
            continue
        markers.append(cleaned + "/")
        markers.append(cleaned + "\\")
    return tuple(markers)


def is_reasoner_symbol_atlas_reference_path(value: str | Path) -> bool:
    """Return True when a value points inside an inactive reference folder."""

    normalized = normalize_reasoner_symbol_atlas_policy_path(value).lower().strip("/")
    if not normalized:
        return False
    parts = [part for part in normalized.split("/") if part]
    inactive_names = {
        folder.lower() for folder in PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS
    }
    return any(part in inactive_names for part in parts)


def iter_reasoner_symbol_atlas_reference_evidence_dirs(
    project_root: str | Path,
) -> tuple[Path, ...]:
    """Return all known inactive reference evidence directories for a root."""

    root = Path(project_root).expanduser().resolve(strict=False)
    return tuple(
        root / folder / _CANONICAL_EVIDENCE_FOLDER_NAME
        for folder in PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS
    )
