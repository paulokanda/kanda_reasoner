# project-path: kanda_reasoner_app/project_support_boundary.py
"""Canonical Tool-versus-Project support-root and identity helpers."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.project_root_resolver import (
    find_reasoner_source_root,
    resolve_app_runtime_root,
)

__all__ = [
    "ProjectSupportBoundaryError",
    "ProjectToolBoundaryIdentity",
    "assert_no_forbidden_nested_support_root",
    "canonical_project_support_root",
    "canonical_transient_garbage_root",
    "forbidden_nested_support_root",
    "project_support_root_blockers",
    "resolve_project_tool_boundary_identity",
]

SHOW_PROJECT_TO_AI_SUFFIX = "_show_project_to_AI"
DELETE_AFTER_DAILY_WORK_SUFFIX = "_delete_after_daily_work"
TOOL_PROJECT_SLUG = "kanda_reasoner"


class ProjectSupportBoundaryError(RuntimeError):
    """Raised when Tool-versus-Project identity or support ownership is unsafe."""


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


def _normalized_source_root(active_project_root: str | Path) -> Path:
    """Return one normalized active Project source root or fail closed."""
    root = Path(active_project_root).expanduser().resolve(strict=False)
    if root.name.endswith(SHOW_PROJECT_TO_AI_SUFFIX):
        raise ProjectSupportBoundaryError(
            "ACTIVE_PROJECT_ROOT_IS_PROJECT_SUPPORT_ROOT:" + str(root)
        )
    if root.name.endswith(DELETE_AFTER_DAILY_WORK_SUFFIX):
        raise ProjectSupportBoundaryError(
            "ACTIVE_PROJECT_ROOT_IS_TRANSIENT_GARBAGE_ROOT:" + str(root)
        )
    return root


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
    """Return a physical identity and a canonical-root fingerprint."""
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


def canonical_project_support_root(active_project_root: str | Path) -> Path:
    """Return the selected Project's external sibling/drive-root support root."""
    root = _normalized_source_root(active_project_root)
    folder_name = root.name + SHOW_PROJECT_TO_AI_SUFFIX
    base = Path(root.anchor) if root.drive else root.parent
    return (base / folder_name).resolve(strict=False)


def canonical_transient_garbage_root(active_project_root: str | Path) -> Path:
    """Return the external ownership-free transient garbage root."""
    root = _normalized_source_root(active_project_root)
    folder_name = root.name + DELETE_AFTER_DAILY_WORK_SUFFIX
    base = Path(root.anchor) if root.drive else root.parent
    return (base / folder_name).resolve(strict=False)


def forbidden_nested_support_root(active_project_root: str | Path) -> Path:
    """Return the forbidden in-source support folder for one active Project."""
    root = _normalized_source_root(active_project_root)
    return (root / (root.name + SHOW_PROJECT_TO_AI_SUFFIX)).resolve(strict=False)


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


def resolve_project_tool_boundary_identity(
    active_project_root: str | Path,
    *,
    tool_source_root: str | Path | None = None,
) -> ProjectToolBoundaryIdentity:
    """Resolve separate Tool and active Project identities for one operation."""
    active_root = _normalized_source_root(active_project_root)
    if not active_root.exists() or not active_root.is_dir():
        raise ProjectSupportBoundaryError(
            "ACTIVE_PROJECT_ROOT_MISSING_OR_NOT_DIRECTORY:" + str(active_root)
        )
    support_root = assert_no_forbidden_nested_support_root(active_root)
    daily_root = canonical_transient_garbage_root(active_root)
    if tool_source_root is None:
        tool_root = find_reasoner_source_root() or resolve_app_runtime_root()
    else:
        tool_root = Path(tool_source_root)
    tool_root = Path(tool_root).expanduser().resolve(strict=False)
    project_id, root_fingerprint = _project_identity(active_root)
    same_root = _same_canonical_location(tool_root, active_root)
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
        self_hosting_mode=same_root,
    )
