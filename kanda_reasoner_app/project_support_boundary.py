# project-path: kanda_reasoner_app/project_support_boundary.py
"""Canonical Tool-versus-Project support-root and identity helpers."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from kanda_reasoner_app.project_root_resolver import (
    find_reasoner_source_root,
    resolve_app_runtime_root,
)
from kanda_reasoner_app.portable_smoke_isolation import (
    resolve_portable_smoke_isolation,
)
from kanda_reasoner_app._project_support_path_contracts import (
    _DELETE_AFTER_DAILY_WORK_SUFFIX,
    _SHOW_PROJECT_TO_AI_SUFFIX,
    _canonical_transient_garbage_root,
    _normalize_project_source_root,
)

__all__ = [
    "ProjectSelectionMode",
    "ProjectSupportBoundaryError",
    "ProjectToolBoundaryIdentity",
    "assert_no_forbidden_nested_support_root",
    "canonical_project_support_root",
    "canonical_tool_support_root",
    "canonical_transient_garbage_root",
    "forbidden_nested_support_root",
    "legacy_physical_project_identity",
    "normalize_project_selection_mode",
    "project_support_root_blockers",
    "resolve_explicit_project_tool_boundary_identity",
    "resolve_project_tool_boundary_identity",
]

SHOW_PROJECT_TO_AI_SUFFIX = _SHOW_PROJECT_TO_AI_SUFFIX
DELETE_AFTER_DAILY_WORK_SUFFIX = _DELETE_AFTER_DAILY_WORK_SUFFIX
TOOL_PROJECT_SLUG = "kanda_reasoner"


class ProjectSupportBoundaryError(RuntimeError):
    """Raised when Tool-versus-Project identity or ownership is unsafe."""


class ProjectSelectionMode(str, Enum):
    """Describe how the active Project gained mutation authority."""

    UNSELECTED = "UNSELECTED"
    EXPLICIT_EXTERNAL_PROJECT = "EXPLICIT_EXTERNAL_PROJECT"
    EXPLICIT_SELF_HOSTING = "EXPLICIT_SELF_HOSTING"


@dataclass(frozen=True)
class ProjectToolBoundaryIdentity:
    """Describe Tool and active Project identities without collapsing them."""

    tool_project_slug: str
    tool_source_root: Path
    active_project_slug: str
    active_project_root: Path
    active_project_support_root: Path
    active_project_daily_work_root: Path
    active_project_id: str
    active_project_root_fingerprint: str
    same_canonical_resolved_root: bool
    self_hosting_mode: bool
    selection_mode: ProjectSelectionMode


def normalize_project_selection_mode(
    value: ProjectSelectionMode | str | None,
) -> ProjectSelectionMode:
    """Return one valid Project selection mode or fail closed."""
    if isinstance(value, ProjectSelectionMode):
        return value
    text = str(value or "").strip().upper()
    try:
        return ProjectSelectionMode(text)
    except ValueError as exc:
        raise ProjectSupportBoundaryError(
            "PROJECT_SELECTION_MODE_INVALID:" + text
        ) from exc


def _normalized_source_root(active_project_root: str | Path) -> Path:
    """Return one normalized active Project source root or fail closed."""
    return _normalize_project_source_root(
        active_project_root,
        error_type=ProjectSupportBoundaryError,
    )


def _normalized_path_key(path: Path) -> str:
    """Return a platform-aware canonical path key."""
    return os.path.normcase(str(path.expanduser().resolve(strict=False)))


def _same_canonical_location(first: Path, second: Path) -> bool:
    """Return whether two roots resolve to the same filesystem location."""
    try:
        return first.samefile(second)
    except OSError:
        return _normalized_path_key(first) == _normalized_path_key(second)


def _project_identity(root: Path) -> tuple[str, str]:
    """Return a legacy physical ID and a canonical-root fingerprint."""
    path_key = _normalized_path_key(root)
    root_fingerprint = hashlib.sha256(path_key.encode("utf-8")).hexdigest()
    try:
        stat = root.stat()
    except OSError:
        identity_basis = "path:" + path_key
    else:
        device = int(getattr(stat, "st_dev", 0) or 0)
        inode = int(getattr(stat, "st_ino", 0) or 0)
        if device or inode:
            identity_basis = f"filesystem:{device}:{inode}"
        else:
            identity_basis = "path:" + path_key
    project_id = hashlib.sha256(identity_basis.encode("utf-8")).hexdigest()
    return project_id, root_fingerprint


def legacy_physical_project_identity(
    active_project_root: str | Path,
) -> tuple[str, str]:
    """Return the retired path/filesystem Project ID and root fingerprint.

    This public compatibility facade exists only for governed migration from
    pre-registry durable owner metadata. It must not grant current Project
    authority or replace the Tool-owned stable Project registry identity.
    """
    root = _normalized_source_root(active_project_root)
    return _project_identity(root)


def canonical_project_support_root(active_project_root: str | Path) -> Path:
    """Return canonical Project Support or a token-bound smoke override."""
    root = _normalized_source_root(active_project_root)
    smoke = resolve_portable_smoke_isolation()
    if smoke is not None:
        return smoke.project_support_root(root)
    folder_name = root.name + SHOW_PROJECT_TO_AI_SUFFIX
    base = Path(root.anchor) if root.drive else root.parent
    return (base / folder_name).resolve(strict=False)


def canonical_tool_support_root(
    tool_source_root: str | Path | None = None,
) -> Path:
    """Return durable Tool Support or a token-bound smoke override."""
    if tool_source_root is None:
        tool_root = find_reasoner_source_root() or resolve_app_runtime_root()
    else:
        tool_root = Path(tool_source_root)
    resolved = Path(tool_root).expanduser().resolve(strict=False)
    smoke = resolve_portable_smoke_isolation()
    if smoke is not None:
        return smoke.tool_support_root(resolved)
    return canonical_project_support_root(resolved)


def canonical_transient_garbage_root(active_project_root: str | Path) -> Path:
    """Return canonical transient storage or a token-bound smoke override."""
    return _canonical_transient_garbage_root(
        active_project_root,
        error_type=ProjectSupportBoundaryError,
    )


def forbidden_nested_support_root(active_project_root: str | Path) -> Path:
    """Return the forbidden in-source support folder for one Project."""
    root = _normalized_source_root(active_project_root)
    return (root / (root.name + SHOW_PROJECT_TO_AI_SUFFIX)).resolve(
        strict=False
    )


def assert_no_forbidden_nested_support_root(
    active_project_root: str | Path,
) -> Path:
    """Fail closed when a nested support root exists under Project source."""
    root = _normalized_source_root(active_project_root)
    forbidden = forbidden_nested_support_root(root)
    if forbidden.exists() or forbidden.is_symlink():
        raise ProjectSupportBoundaryError(
            "FORBIDDEN_NESTED_PROJECT_SUPPORT_ROOT:" + str(forbidden)
        )
    return canonical_project_support_root(root)


def project_support_root_blockers(
    active_project_root: str | Path,
    candidate: str | Path,
) -> tuple[str, ...]:
    """Return deterministic blockers for a proposed Project support root."""
    root = _normalized_source_root(active_project_root)
    path = Path(candidate).expanduser().resolve(strict=False)
    canonical = canonical_project_support_root(root)
    blockers: list[str] = []
    try:
        path.relative_to(root)
    except ValueError:
        pass
    else:
        blockers.append("PROJECT_SUPPORT_ROOT_INSIDE_PROJECT_SOURCE")
    if path != canonical:
        blockers.append("PROJECT_SUPPORT_ROOT_NOT_CANONICAL_EXTERNAL_ROOT")
    return tuple(sorted(set(blockers)))


def _resolved_tool_root(tool_source_root: str | Path | None) -> Path:
    """Return the canonical Tool source or runtime root."""
    if tool_source_root is None:
        tool_root = find_reasoner_source_root() or resolve_app_runtime_root()
    else:
        tool_root = Path(tool_source_root)
    return Path(tool_root).expanduser().resolve(strict=False)


def resolve_explicit_project_tool_boundary_identity(
    active_project_root: str | Path,
    *,
    selection_mode: ProjectSelectionMode | str,
    stable_project_id: str,
    tool_source_root: str | Path | None = None,
) -> ProjectToolBoundaryIdentity:
    """Resolve strict Tool and Project identity after explicit selection."""
    mode = normalize_project_selection_mode(selection_mode)
    if mode is ProjectSelectionMode.UNSELECTED:
        raise ProjectSupportBoundaryError(
            "UNSELECTED_PROJECT_HAS_NO_BOUNDARY_IDENTITY"
        )
    project_id = str(stable_project_id or "").strip()
    if not project_id:
        raise ProjectSupportBoundaryError("STABLE_PROJECT_ID_REQUIRED")

    active_root = _normalized_source_root(active_project_root)
    if not active_root.exists() or not active_root.is_dir():
        raise ProjectSupportBoundaryError(
            "ACTIVE_PROJECT_ROOT_MISSING_OR_NOT_DIRECTORY:" + str(active_root)
        )
    support_root = assert_no_forbidden_nested_support_root(active_root)
    daily_root = canonical_transient_garbage_root(active_root)
    tool_root = _resolved_tool_root(tool_source_root)
    _, root_fingerprint = _project_identity(active_root)
    same_root = _same_canonical_location(tool_root, active_root)

    if same_root and mode is not ProjectSelectionMode.EXPLICIT_SELF_HOSTING:
        raise ProjectSupportBoundaryError(
            "SELF_HOSTING_REQUIRES_EXPLICIT_SELECTION"
        )
    if not same_root and mode is ProjectSelectionMode.EXPLICIT_SELF_HOSTING:
        raise ProjectSupportBoundaryError(
            "SELF_HOSTING_SELECTION_ROOT_MISMATCH"
        )

    return ProjectToolBoundaryIdentity(
        tool_project_slug=TOOL_PROJECT_SLUG,
        tool_source_root=tool_root,
        active_project_slug=active_root.name,
        active_project_root=active_root,
        active_project_support_root=support_root,
        active_project_daily_work_root=daily_root,
        active_project_id=project_id,
        active_project_root_fingerprint=root_fingerprint,
        same_canonical_resolved_root=same_root,
        self_hosting_mode=(
            mode is ProjectSelectionMode.EXPLICIT_SELF_HOSTING
        ),
        selection_mode=mode,
    )


def resolve_project_tool_boundary_identity(
    active_project_root: str | Path,
    *,
    tool_source_root: str | Path | None = None,
) -> ProjectToolBoundaryIdentity:
    """Resolve the legacy inferred identity for compatibility-only callers.

    New mutation-capable callers must use
    ``resolve_explicit_project_tool_boundary_identity`` so self-hosting cannot
    be inferred from path equality. This compatibility facade remains read-only
    until all existing consumers are migrated in later boundary releases.
    """
    active_root = _normalized_source_root(active_project_root)
    legacy_project_id, _ = _project_identity(active_root)
    tool_root = _resolved_tool_root(tool_source_root)
    same_root = _same_canonical_location(tool_root, active_root)
    mode = (
        ProjectSelectionMode.EXPLICIT_SELF_HOSTING
        if same_root
        else ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT
    )
    return resolve_explicit_project_tool_boundary_identity(
        active_root,
        selection_mode=mode,
        stable_project_id=legacy_project_id,
        tool_source_root=tool_root,
    )
