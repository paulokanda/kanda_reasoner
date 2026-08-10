# project-path: kanda_reasoner_app/project_operation_authority.py
"""Registry-backed authority for Tool operations against one selected Project."""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath

from kanda_reasoner_app.project_selection_registry import (
    ProjectSelectionRegistry,
    ProjectSelectionRegistryError,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectToolBoundaryIdentity,
    canonical_tool_support_root,
)

__all__ = [
    "ProjectOperationAuthority",
    "ProjectOperationAuthorityError",
    "ProjectOperationKind",
    "assert_authorized_project_target",
    "assert_project_authority_current",
    "build_project_operation_authority",
    "resolve_registered_project_boundary",
]


class ProjectOperationAuthorityError(RuntimeError):
    """Raised when selected-Project identity or target authority is unsafe."""


class ProjectOperationKind(str, Enum):
    """Consequential operation classes owned by the selected Project."""

    PROJECT_SOURCE_READ = "PROJECT_SOURCE_READ"
    PROJECT_SOURCE_WRITE = "PROJECT_SOURCE_WRITE"
    PROJECT_SUPPORT_READ = "PROJECT_SUPPORT_READ"
    PROJECT_SUPPORT_WRITE = "PROJECT_SUPPORT_WRITE"
    PROJECT_TRANSIENT_WRITE = "PROJECT_TRANSIENT_WRITE"


@dataclass(frozen=True)
class ProjectOperationAuthority:
    """Bind one operation to current registry identity and one allowed root."""

    boundary: ProjectToolBoundaryIdentity
    operation_kind: ProjectOperationKind
    operation_id: str
    project_epoch: int
    source_snapshot_identity: str
    allowed_root: Path
    protected_roots: tuple[Path, ...]

    def record(self) -> dict[str, object]:
        """Return deterministic non-secret authority metadata."""
        return {
            "operation_kind": self.operation_kind.value,
            "operation_id": self.operation_id,
            "project_epoch": self.project_epoch,
            "source_snapshot_identity": self.source_snapshot_identity,
            "stable_project_id": self.boundary.active_project_id,
            "project_slug": self.boundary.active_project_slug,
            "project_root": str(self.boundary.active_project_root),
            "project_root_fingerprint": (
                self.boundary.active_project_root_fingerprint
            ),
            "selection_mode": self.boundary.selection_mode.value,
            "self_hosting_mode": self.boundary.self_hosting_mode,
            "allowed_root": str(self.allowed_root),
            "protected_roots": [str(path) for path in self.protected_roots],
        }


def resolve_registered_project_boundary(
    selected_project_root: str | Path,
    *,
    tool_source_root: str | Path | None = None,
    registry_path: str | Path | None = None,
) -> ProjectToolBoundaryIdentity:
    """Resolve one exact current registry-backed Project boundary."""
    root = _absolute_resolved_path(selected_project_root, "ACTIVE_PROJECT_ROOT")
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_source_root,
        registry_path=registry_path,
    )
    try:
        return registry.resolve_boundary_for_root(root)
    except ProjectSelectionRegistryError as exc:
        raise ProjectOperationAuthorityError(str(exc)) from exc


def build_project_operation_authority(
    selected_project_root: str | Path,
    *,
    operation_kind: ProjectOperationKind | str,
    operation_id: str,
    project_epoch: int = 0,
    source_snapshot_identity: str = "",
    tool_source_root: str | Path | None = None,
    registry_path: str | Path | None = None,
) -> ProjectOperationAuthority:
    """Build one least-authority value from the current explicit selection."""
    boundary = resolve_registered_project_boundary(
        selected_project_root,
        tool_source_root=tool_source_root,
        registry_path=registry_path,
    )
    kind = _normalize_operation_kind(operation_kind)
    normalized_operation_id = str(operation_id or "").strip()
    if not normalized_operation_id:
        raise ProjectOperationAuthorityError("PROJECT_OPERATION_ID_REQUIRED")
    if len(normalized_operation_id) > 160:
        raise ProjectOperationAuthorityError("PROJECT_OPERATION_ID_TOO_LONG")
    epoch = int(project_epoch)
    if epoch < 0:
        raise ProjectOperationAuthorityError("PROJECT_OPERATION_EPOCH_INVALID")
    snapshot = str(source_snapshot_identity or "").strip()
    allowed_root, protected = _roots_for_kind(boundary, kind)
    return ProjectOperationAuthority(
        boundary=boundary,
        operation_kind=kind,
        operation_id=normalized_operation_id,
        project_epoch=epoch,
        source_snapshot_identity=snapshot,
        allowed_root=allowed_root,
        protected_roots=protected,
    )


def assert_project_authority_current(
    authority: ProjectOperationAuthority,
    *,
    selected_project_root: str | Path,
    project_epoch: int,
    tool_source_root: str | Path | None = None,
    registry_path: str | Path | None = None,
) -> ProjectToolBoundaryIdentity:
    """Recheck registry identity and epoch immediately before mutation."""
    current = resolve_registered_project_boundary(
        selected_project_root,
        tool_source_root=tool_source_root,
        registry_path=registry_path,
    )
    expected = authority.boundary
    checks = (
        (
            current.active_project_id,
            expected.active_project_id,
            "PROJECT_AUTHORITY_STABLE_ID_STALE",
        ),
        (
            current.active_project_root_fingerprint,
            expected.active_project_root_fingerprint,
            "PROJECT_AUTHORITY_ROOT_FINGERPRINT_STALE",
        ),
        (
            _path_key(current.active_project_root),
            _path_key(expected.active_project_root),
            "PROJECT_AUTHORITY_ROOT_STALE",
        ),
        (
            current.selection_mode.value,
            expected.selection_mode.value,
            "PROJECT_AUTHORITY_SELECTION_MODE_STALE",
        ),
    )
    for actual, wanted, marker in checks:
        if actual != wanted:
            raise ProjectOperationAuthorityError(marker)
    if int(project_epoch) != authority.project_epoch:
        raise ProjectOperationAuthorityError("PROJECT_AUTHORITY_EPOCH_STALE")
    return current


def assert_authorized_project_target(
    authority: ProjectOperationAuthority,
    target_path: str | Path,
    *,
    operation_kind: ProjectOperationKind | str | None = None,
) -> Path:
    """Return one canonical target or reject cross-root and reparse access."""
    kind = (
        authority.operation_kind
        if operation_kind is None
        else _normalize_operation_kind(operation_kind)
    )
    if kind is not authority.operation_kind:
        raise ProjectOperationAuthorityError(
            "PROJECT_OPERATION_KIND_AUTHORITY_MISMATCH"
        )
    target = _absolute_resolved_path(target_path, "PROJECT_OPERATION_TARGET")
    allowed = authority.allowed_root.resolve(strict=False)
    if not _is_within(target, allowed):
        raise ProjectOperationAuthorityError(
            "PROJECT_OPERATION_TARGET_OUTSIDE_ALLOWED_ROOT:" + str(target)
        )
    for protected in authority.protected_roots:
        if _is_within(target, protected.resolve(strict=False)):
            raise ProjectOperationAuthorityError(
                "PROJECT_OPERATION_TARGET_PROTECTED_ROOT:" + str(protected)
            )
    _reject_existing_reparse_components(target, allowed)
    return target


def authorized_relative_project_target(
    authority: ProjectOperationAuthority,
    relative_path: str,
) -> Path:
    """Resolve one safe POSIX-style relative path under the authority root."""
    text = str(relative_path or "").strip()
    pure = PurePosixPath(text)
    if not text or pure.is_absolute() or ".." in pure.parts or "\\" in text:
        raise ProjectOperationAuthorityError(
            "PROJECT_OPERATION_RELATIVE_TARGET_UNSAFE:" + text
        )
    target = authority.allowed_root.joinpath(*pure.parts)
    return assert_authorized_project_target(authority, target)


def _roots_for_kind(
    boundary: ProjectToolBoundaryIdentity,
    kind: ProjectOperationKind,
) -> tuple[Path, tuple[Path, ...]]:
    """Return one allowed root and protected roots for an operation class."""
    project_root = boundary.active_project_root.resolve(strict=False)
    support_root = boundary.active_project_support_root.resolve(strict=False)
    transient_root = boundary.active_project_daily_work_root.resolve(strict=False)
    tool_root = boundary.tool_source_root.resolve(strict=False)
    tool_support = canonical_tool_support_root(tool_root).resolve(strict=False)
    if kind in {
        ProjectOperationKind.PROJECT_SOURCE_READ,
        ProjectOperationKind.PROJECT_SOURCE_WRITE,
    }:
        protected = [support_root, transient_root]
        if not boundary.self_hosting_mode:
            protected.extend((tool_root, tool_support))
        return project_root, _unique_paths(protected)
    if kind in {
        ProjectOperationKind.PROJECT_SUPPORT_READ,
        ProjectOperationKind.PROJECT_SUPPORT_WRITE,
    }:
        return support_root, _unique_paths((project_root, transient_root))
    if kind is ProjectOperationKind.PROJECT_TRANSIENT_WRITE:
        return transient_root, _unique_paths((project_root, support_root))
    raise ProjectOperationAuthorityError(
        "PROJECT_OPERATION_KIND_UNSUPPORTED:" + kind.value
    )


def _normalize_operation_kind(
    value: ProjectOperationKind | str,
) -> ProjectOperationKind:
    """Return one supported operation kind or fail closed."""
    if isinstance(value, ProjectOperationKind):
        return value
    text = str(value or "").strip().upper()
    try:
        return ProjectOperationKind(text)
    except ValueError as exc:
        raise ProjectOperationAuthorityError(
            "PROJECT_OPERATION_KIND_INVALID:" + text
        ) from exc


def _absolute_resolved_path(value: str | Path, label: str) -> Path:
    """Return an absolute canonical path without accepting blank values."""
    text = str(value or "").strip()
    if not text:
        raise ProjectOperationAuthorityError(label + "_REQUIRED")
    path = Path(text).expanduser()
    if not path.is_absolute():
        raise ProjectOperationAuthorityError(label + "_MUST_BE_ABSOLUTE")
    return path.resolve(strict=False)


def _path_key(path: Path) -> str:
    """Return a platform-aware canonical path comparison key."""
    return os.path.normcase(str(path.expanduser().resolve(strict=False)))


def _is_within(path: Path, root: Path) -> bool:
    """Return whether one canonical path is root or a component child."""
    try:
        return os.path.commonpath((_path_key(path), _path_key(root))) == _path_key(root)
    except (OSError, ValueError):
        return False


def _unique_paths(paths: tuple[Path, ...] | list[Path]) -> tuple[Path, ...]:
    """Return canonical paths without duplicate physical spellings."""
    unique: dict[str, Path] = {}
    for path in paths:
        resolved = path.resolve(strict=False)
        unique.setdefault(_path_key(resolved), resolved)
    return tuple(unique.values())


def _reject_existing_reparse_components(target: Path, allowed_root: Path) -> None:
    """Reject symlink or Windows reparse components below the owner root."""
    try:
        relative = target.relative_to(allowed_root)
    except ValueError as exc:
        raise ProjectOperationAuthorityError(
            "PROJECT_OPERATION_TARGET_OUTSIDE_ALLOWED_ROOT:" + str(target)
        ) from exc
    current = allowed_root
    for part in relative.parts:
        current = current / part
        if not current.exists() and not current.is_symlink():
            continue
        try:
            info = current.lstat()
        except OSError as exc:
            raise ProjectOperationAuthorityError(
                "PROJECT_OPERATION_TARGET_COMPONENT_UNREADABLE:" + str(current)
            ) from exc
        attributes = int(getattr(info, "st_file_attributes", 0) or 0)
        is_reparse = bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
        if current.is_symlink() or is_reparse:
            raise ProjectOperationAuthorityError(
                "PROJECT_OPERATION_REPARSE_COMPONENT_REJECTED:" + str(current)
            )
