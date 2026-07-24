# project-path: kanda_reasoner_app/reasoner_context_bundle/project_context.py
"""Dynamic project context resolution for the reasoner context bundle box."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
    project_analysis_evidence_root,
    project_name_from_root,
)
from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)

from .schema_models import ProjectContext

__all__ = ["resolve_project_context"]


def resolve_project_context(project_root: str | Path) -> ProjectContext:
    """Resolve dynamic context for one active project.

    This function does not create folders and does not hardcode any drive or
    project name. The caller provides the selected project root.
    """
    root = Path(project_root).expanduser()
    if not str(root).strip():
        raise ValueError("project_root is required")

    identity = resolve_project_tool_boundary_identity(root)
    project_slug = project_name_from_root(root)
    evidence_root = project_analysis_evidence_root(root)
    json_complete_dir = analysis_json_complete_dir(root)
    return ProjectContext(
        root=root,
        project_slug=project_slug,
        evidence_root=evidence_root,
        json_complete_dir=json_complete_dir,
        active_project_id=identity.active_project_id,
        active_project_root_fingerprint=identity.active_project_root_fingerprint,
    )
