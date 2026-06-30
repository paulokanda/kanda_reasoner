# project-path: kanda_reasoner_app/reasoner_symbol_atlas/evidence_paths.py
"""Project Analysis Evidence path resolution for Project Symbol Atlas.

This module owns only path normalization for the Project Symbol Atlas box.
It does not migrate, copy, delete, parse, or generate evidence files.
All paths are derived from the supplied project_root argument.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .reference_folder_policy import (
    PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS,
    iter_reasoner_symbol_atlas_reference_evidence_dirs,
)

PROJECT_SYMBOL_ATLAS_CANONICAL_EVIDENCE_FOLDER_NAME = "project_analysis_evidence"
PROJECT_SYMBOL_ATLAS_LEGACY_REFERENCE_FOLDER_NAME = "_project_reference"
PROJECT_SYMBOL_ATLAS_LEGACY_REFERENCE_FOLDER_NAMES = (
    PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS
)
PROJECT_SYMBOL_ATLAS_STATUS_CANONICAL_READY = "canonical_ready"
PROJECT_SYMBOL_ATLAS_STATUS_DUAL_EVIDENCE = "dual_evidence"
PROJECT_SYMBOL_ATLAS_STATUS_MIGRATION_AVAILABLE = "migration_available"
PROJECT_SYMBOL_ATLAS_STATUS_MISSING_EVIDENCE = "missing_evidence"


@dataclass(frozen=True)
class ProjectAnalysisEvidencePaths:
    """Resolved Project Analysis Evidence paths for one project root."""

    project_root: str
    canonical_evidence_dir: str
    legacy_evidence_dir: str
    canonical_exists: bool
    legacy_exists: bool
    migration_needed: bool
    status: str
    notes: tuple[str, ...] = field(default_factory=tuple)
    reference_evidence_dirs: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "project_root": self.project_root,
            "canonical_evidence_dir": self.canonical_evidence_dir,
            "legacy_evidence_dir": self.legacy_evidence_dir,
            "canonical_exists": self.canonical_exists,
            "legacy_exists": self.legacy_exists,
            "migration_needed": self.migration_needed,
            "status": self.status,
            "notes": list(self.notes),
            "reference_evidence_dirs": list(self.reference_evidence_dirs),
        }


def normalize_reasoner_symbol_atlas_root(project_root: str | Path) -> Path:
    """Normalize a project root path without requiring it to exist."""

    if project_root is None:
        raise ValueError("project_root is required")
    root_text = str(project_root).strip()
    if not root_text:
        raise ValueError("project_root must not be empty")
    return Path(root_text).expanduser().resolve(strict=False)


def get_reasoner_symbol_atlas_canonical_evidence_dir(project_root: str | Path) -> Path:
    """Return the canonical active evidence directory for a project root."""

    root = normalize_reasoner_symbol_atlas_root(project_root)
    return root / PROJECT_SYMBOL_ATLAS_CANONICAL_EVIDENCE_FOLDER_NAME


def get_reasoner_symbol_atlas_legacy_evidence_dir(project_root: str | Path) -> Path:
    """Return the backward-compatible legacy reference evidence directory."""

    root = normalize_reasoner_symbol_atlas_root(project_root)
    return (
        root
        / PROJECT_SYMBOL_ATLAS_LEGACY_REFERENCE_FOLDER_NAME
        / PROJECT_SYMBOL_ATLAS_CANONICAL_EVIDENCE_FOLDER_NAME
    )


def get_reasoner_symbol_atlas_reference_evidence_dirs(
    project_root: str | Path,
) -> tuple[Path, ...]:
    """Return all supported inactive reference evidence directories."""

    root = normalize_reasoner_symbol_atlas_root(project_root)
    return iter_reasoner_symbol_atlas_reference_evidence_dirs(root)


def _select_legacy_evidence_dir(reference_dirs: tuple[Path, ...]) -> Path:
    """Select the reference evidence dir used by legacy single-dir callers."""

    for candidate in reference_dirs:
        if candidate.is_dir():
            return candidate
    return reference_dirs[0]


def resolve_project_analysis_evidence_paths(
    project_root: str | Path,
) -> ProjectAnalysisEvidencePaths:
    """Resolve canonical and inactive reference Project Analysis Evidence paths.

    The canonical active folder is always project_analysis_evidence under the
    supplied project root. Reference folders are only reported so migration
    logic can decide what to copy. This function performs no writes.
    """

    root = normalize_reasoner_symbol_atlas_root(project_root)
    canonical_dir = get_reasoner_symbol_atlas_canonical_evidence_dir(root)
    reference_dirs = get_reasoner_symbol_atlas_reference_evidence_dirs(root)
    legacy_dir = _select_legacy_evidence_dir(reference_dirs)
    canonical_exists = canonical_dir.is_dir()
    existing_reference_dirs = tuple(path for path in reference_dirs if path.is_dir())
    legacy_exists = bool(existing_reference_dirs)
    migration_needed = legacy_exists and not canonical_exists

    notes: list[str] = []
    if canonical_exists and legacy_exists:
        status = PROJECT_SYMBOL_ATLAS_STATUS_DUAL_EVIDENCE
        notes.append("Canonical and reference evidence folders both exist.")
        notes.append("Prefer canonical evidence for active project analysis.")
    elif canonical_exists:
        status = PROJECT_SYMBOL_ATLAS_STATUS_CANONICAL_READY
        notes.append("Canonical evidence folder exists.")
    elif legacy_exists:
        status = PROJECT_SYMBOL_ATLAS_STATUS_MIGRATION_AVAILABLE
        notes.append("Reference evidence folder exists but canonical folder is missing.")
        notes.append("A later explicit migration step can copy evidence safely.")
    else:
        status = PROJECT_SYMBOL_ATLAS_STATUS_MISSING_EVIDENCE
        notes.append("No Project Analysis Evidence folder was found.")

    notes.append(
        "Inactive reference folders are memo/comment folders, not active source: "
        + ", ".join(PROJECT_SYMBOL_ATLAS_LEGACY_REFERENCE_FOLDER_NAMES)
        + "."
    )

    return ProjectAnalysisEvidencePaths(
        project_root=str(root),
        canonical_evidence_dir=str(canonical_dir),
        legacy_evidence_dir=str(legacy_dir),
        canonical_exists=canonical_exists,
        legacy_exists=legacy_exists,
        migration_needed=migration_needed,
        status=status,
        notes=tuple(notes),
        reference_evidence_dirs=tuple(str(path) for path in reference_dirs),
    )


def build_project_analysis_evidence_path_summary(project_root: str | Path) -> str:
    """Return a compact human-readable path summary."""

    paths = resolve_project_analysis_evidence_paths(project_root)
    lines = [
        "# Project Analysis Evidence Paths",
        "",
        f"Project root: {paths.project_root}",
        f"Status: {paths.status}",
        f"Canonical evidence: {paths.canonical_evidence_dir}",
        f"Canonical exists: {paths.canonical_exists}",
        f"Legacy evidence: {paths.legacy_evidence_dir}",
        f"Legacy exists: {paths.legacy_exists}",
        f"Migration needed: {paths.migration_needed}",
        "",
        "## Reference evidence dirs",
    ]
    for path in paths.reference_evidence_dirs:
        lines.append(f"- {path}")
    lines.extend(["", "## Notes"])
    for note in paths.notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


__all__ = [
    "PROJECT_SYMBOL_ATLAS_CANONICAL_EVIDENCE_FOLDER_NAME",
    "PROJECT_SYMBOL_ATLAS_LEGACY_REFERENCE_FOLDER_NAME",
    "PROJECT_SYMBOL_ATLAS_LEGACY_REFERENCE_FOLDER_NAMES",
    "PROJECT_SYMBOL_ATLAS_STATUS_CANONICAL_READY",
    "PROJECT_SYMBOL_ATLAS_STATUS_DUAL_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_STATUS_MIGRATION_AVAILABLE",
    "PROJECT_SYMBOL_ATLAS_STATUS_MISSING_EVIDENCE",
    "ProjectAnalysisEvidencePaths",
    "build_project_analysis_evidence_path_summary",
    "get_reasoner_symbol_atlas_canonical_evidence_dir",
    "get_reasoner_symbol_atlas_legacy_evidence_dir",
    "get_reasoner_symbol_atlas_reference_evidence_dirs",
    "normalize_reasoner_symbol_atlas_root",
    "resolve_project_analysis_evidence_paths",
]
