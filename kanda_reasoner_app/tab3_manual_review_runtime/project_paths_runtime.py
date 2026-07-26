# project-path: kanda_reasoner_app/tab3_manual_review_runtime/project_paths_runtime.py
"""Dynamic active-Project paths for Docstring Assistant support state."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    ProjectSupportBoundaryError,
    ProjectToolBoundaryIdentity,
    resolve_project_tool_boundary_identity,
)

__all__ = [
    "DOCSTRING_SUPPORT_FOLDER",
    "active_project_identity",
    "active_project_root",
    "docstring_support_root",
    "manual_review_export_root",
    "manual_review_state_path",
    "legacy_manual_review_state_path",
    "run_report_path",
    "scan_report_folder",
]

DOCSTRING_SUPPORT_FOLDER = "docstring_assistant"


def active_project_root(owner: object) -> Path:
    """Return the exact selected active-Project source root."""
    for attribute in ("_root_path_edit", "project_root_edit"):
        edit = getattr(owner, attribute, None)
        text_method = getattr(edit, "text", None)
        if not callable(text_method):
            continue
        text = str(text_method() or "").strip()
        if text:
            return Path(text).expanduser().resolve(strict=False)
    raise ProjectSupportBoundaryError("ACTIVE_PROJECT_ROOT_NOT_SELECTED")


def active_project_identity(owner: object) -> ProjectToolBoundaryIdentity:
    """Resolve canonical Tool and selected active-Project identities."""
    return resolve_project_tool_boundary_identity(active_project_root(owner))


def docstring_support_root(owner: object) -> Path:
    """Return external durable support root for Docstring Assistant state."""
    identity = active_project_identity(owner)
    return identity.active_project_support_root / DOCSTRING_SUPPORT_FOLDER


def run_report_path(owner: object) -> Path:
    """Return the default Project-specific run report path."""
    identity = active_project_identity(owner)
    filename = identity.active_project_slug + "_docstring_run_report.jsonl"
    return docstring_support_root(owner) / "reports" / filename


def scan_report_folder(owner: object) -> Path:
    """Return the default external folder for timestamped scan reports."""
    return docstring_support_root(owner) / "reports"


def manual_review_state_path(owner: object) -> Path:
    """Return external durable manual-review state path."""
    return docstring_support_root(owner) / "manual_review_state.json"


def manual_review_export_root(owner: object) -> Path:
    """Return external durable folder for explicit review exports."""
    return docstring_support_root(owner) / "manual_review_exports"


def legacy_manual_review_state_path(owner: object) -> Path:
    """Return old in-source state path for read-only compatibility."""
    return (
        active_project_root(owner)
        / "project_freeze_ledger"
        / "manual_docstring_review_state.json"
    )
