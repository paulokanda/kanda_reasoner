# project-path: kanda_reasoner_app/reasoner_context_bundle/project_context.py
"""Dynamic registry-backed Project context for the context-bundle box."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
    project_analysis_evidence_root,
    project_name_from_root,
)
from kanda_reasoner_app.project_operation_authority import (
    ProjectOperationAuthorityError,
    resolve_registered_project_boundary,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectToolBoundaryIdentity,
)

from .schema_models import ProjectContext

__all__ = ["resolve_project_context"]


class ProjectContextResolutionError(RuntimeError):
    """Raised when one handoff Project cannot be proven current and explicit."""


def _normalized_project_root(project_root: str | Path) -> Path:
    """Return one absolute Project root or fail before boundary resolution."""
    text = str(project_root or "").strip()
    if not text:
        raise ProjectContextResolutionError("PROJECT_ROOT_REQUIRED")
    root = Path(text).expanduser().resolve(strict=False)
    if not root.exists() or not root.is_dir():
        raise ProjectContextResolutionError(
            "PROJECT_ROOT_MISSING_OR_NOT_DIRECTORY:" + str(root)
        )
    return root


def _resolve_current_boundary(root: Path) -> ProjectToolBoundaryIdentity:
    """Resolve the Tool-owned current registry boundary for one exact root."""
    try:
        return resolve_registered_project_boundary(root)
    except ProjectOperationAuthorityError as exc:
        raise ProjectContextResolutionError(str(exc)) from exc


def _assert_context_alignment(
    root: Path,
    project_slug: str,
    boundary: ProjectToolBoundaryIdentity,
) -> None:
    """Reject internal identity contradictions before generating evidence."""
    if boundary.active_project_root != root:
        raise ProjectContextResolutionError(
            "PROJECT_CONTEXT_BOUNDARY_ROOT_MISMATCH"
        )
    if boundary.active_project_slug != project_slug:
        raise ProjectContextResolutionError(
            "PROJECT_CONTEXT_BOUNDARY_SLUG_MISMATCH"
        )
    if not boundary.active_project_id.strip():
        raise ProjectContextResolutionError(
            "PROJECT_CONTEXT_STABLE_PROJECT_ID_REQUIRED"
        )
    if not boundary.active_project_root_fingerprint.strip():
        raise ProjectContextResolutionError(
            "PROJECT_CONTEXT_ROOT_FINGERPRINT_REQUIRED"
        )


def _build_context(
    root: Path,
    boundary: ProjectToolBoundaryIdentity,
) -> ProjectContext:
    """Build the immutable internal context used by handoff builders."""
    project_slug = project_name_from_root(root)
    _assert_context_alignment(root, project_slug, boundary)
    return ProjectContext(
        root=root,
        project_slug=project_slug,
        evidence_root=project_analysis_evidence_root(root),
        json_complete_dir=analysis_json_complete_dir(root),
        active_project_id=boundary.active_project_id,
        active_project_root_fingerprint=(
            boundary.active_project_root_fingerprint
        ),
        tool_project_slug=boundary.tool_project_slug,
        tool_source_root=boundary.tool_source_root,
        active_project_support_root=boundary.active_project_support_root,
        active_project_daily_work_root=(
            boundary.active_project_daily_work_root
        ),
        selection_mode=boundary.selection_mode.value,
        same_canonical_resolved_root=(
            boundary.same_canonical_resolved_root
        ),
        self_hosting_mode=boundary.self_hosting_mode,
    )


def resolve_project_context(project_root: str | Path) -> ProjectContext:
    """Resolve current explicit Project context without creating any folder.

    The Tool-owned selection registry is the authority. A path-derived legacy
    identity is never accepted. This function is read-only and fails closed if
    there is no current selection or if the selected root differs from the
    requested root.
    """
    root = _normalized_project_root(project_root)
    boundary = _resolve_current_boundary(root)
    return _build_context(root, boundary)
