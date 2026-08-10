# project-path: kanda_reasoner_app/project_fire_shield.py
"""Public fail-closed Fire Shield for governed cross-project operations.

Fire Shield composes existing selected-Project identity, Project Operation
Authority, archive safety, and deterministic provenance checks. It does not
replace those canonical owners.
"""

from __future__ import annotations

import zipfile
from pathlib import Path, PurePosixPath
from typing import Iterable

from kanda_reasoner_app import _project_fire_shield_provenance as _provenance
from kanda_reasoner_app import _project_fire_shield_types as _types
from kanda_reasoner_app.archive_safety import (
    ArchiveSafetyError,
    validate_archive_members,
)
from kanda_reasoner_app.project_selection_registry import (
    ProjectSelectionRegistry,
    ProjectSelectionRegistryError,
)
from kanda_reasoner_app.project_operation_authority import (
    ProjectOperationAuthority,
    ProjectOperationAuthorityError,
    ProjectOperationKind,
    assert_authorized_project_target,
    assert_project_authority_current,
    build_project_operation_authority,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectSelectionMode,
    ProjectToolBoundaryIdentity,
    TOOL_PROJECT_SLUG,
)

FireShieldArchiveReport = _types.FireShieldArchiveReport
FireShieldContext = _types.FireShieldContext
FireShieldError = _types.FireShieldError
FireShieldMode = _types.FireShieldMode
FireShieldPhase = _types.FireShieldPhase
ToolFileState = _types.ToolFileState
ToolSnapshot = _types.ToolSnapshot

assert_existing_destination_not_tool_alias = (
    _provenance.assert_existing_destination_not_tool_alias
)
assert_payload_bytes_not_tool_copy = _provenance.assert_payload_bytes_not_tool_copy
capture_tool_snapshot = _provenance.capture_tool_snapshot
scan_project_python_source = _provenance.scan_project_python_source
verify_project_import_isolation = _provenance.verify_project_import_isolation
verify_tool_snapshot_unchanged = _provenance.verify_tool_snapshot_unchanged

__all__ = [
    "FIRE_SHIELD_FEATURE_ID",
    "FireShieldArchiveReport",
    "FireShieldContext",
    "FireShieldError",
    "FireShieldMode",
    "FireShieldPhase",
    "ToolFileState",
    "ToolSnapshot",
    "assert_fire_shield_context_current",
    "assert_fire_shield_payload_bytes_allowed",
    "assert_fire_shield_source_transfer_allowed",
    "assert_fire_shield_write_allowed",
    "build_current_fire_shield_context",
    "build_fire_shield_context",
    "build_fire_shield_context_from_authority",
    "capture_tool_snapshot",
    "preflight_fire_shield_archive",
    "scan_project_python_source",
    "verify_project_import_isolation",
    "verify_tool_snapshot_unchanged",
]

FIRE_SHIELD_FEATURE_ID = (
    "kanda-reasoner-fire-shield-cross-project-immutability-v1"
)

_DELIVERY_CONTROL_ROOT_FILES = {
    "INSTALL.ps1",
    "INSTALL_MANIFEST.json",
    "KANDA_PATCH_DELIVERY_MANIFEST.json",
    "KANDA_PATCH_TRACE.json",
    "README.md",
    "README.txt",
    "RUN_INSTALL.ps1",
    "RUN_VALIDATE.ps1",
    "VALIDATE.ps1",
}
_DELIVERY_CONTROL_PREFIXES = (
    "scripts/",
    "tools/",
    "validation/",
    "validators/",
)
_EVIDENCE_PREFIXES = (
    "evidence/",
    "validation_evidence/",
)
_SUPPORTED_MUTATIONS = {
    "APPEND",
    "CREATE",
    "DELETE",
    "EXTRACT",
    "MKDIR",
    "MOVE",
    "RENAME",
    "REPLACE",
    "RESTORE",
    "TRUNCATE",
    "WRITE",
}


def build_current_fire_shield_context(
    *,
    phase: FireShieldPhase | str,
    operation_id: str,
    tool_source_root: str | Path | None = None,
    registry_path: str | Path | None = None,
) -> FireShieldContext:
    """Build Fire Shield for the currently selected Project only."""
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_source_root,
        registry_path=registry_path,
    )
    try:
        boundary = registry.resolve_current_boundary()
    except ProjectSelectionRegistryError as exc:
        raise FireShieldError("FIRE_SHIELD_UNAVAILABLE:" + str(exc)) from exc
    if boundary is None:
        raise FireShieldError("FIRE_SHIELD_UNAVAILABLE:ACTIVE_PROJECT_SELECTION_REQUIRED")
    return build_fire_shield_context(
        boundary.active_project_root,
        phase=phase,
        operation_id=operation_id,
        tool_source_root=boundary.tool_source_root,
        registry_path=registry.registry_path,
    )


def build_fire_shield_context(
    selected_project_root: str | Path,
    *,
    phase: FireShieldPhase | str,
    operation_id: str,
    tool_source_root: str | Path | None = None,
    registry_path: str | Path | None = None,
) -> FireShieldContext:
    """Resolve current registry identity and build a fail-closed context."""
    normalized_phase = _normalize_phase(phase)
    kind = _operation_kind_for_phase(normalized_phase)
    try:
        authority = build_project_operation_authority(
            selected_project_root,
            operation_kind=kind,
            operation_id=operation_id,
            tool_source_root=tool_source_root,
            registry_path=registry_path,
        )
    except ProjectOperationAuthorityError as exc:
        raise FireShieldError("FIRE_SHIELD_UNAVAILABLE:" + str(exc)) from exc
    return build_fire_shield_context_from_authority(
        authority,
        phase=normalized_phase,
        registry_path=registry_path,
    )


def build_fire_shield_context_from_authority(
    authority: ProjectOperationAuthority,
    *,
    phase: FireShieldPhase | str,
    registry_path: str | Path | None = None,
) -> FireShieldContext:
    """Build Fire Shield from one already-validated Project authority."""
    normalized_phase = _normalize_phase(phase)
    expected_kind = _operation_kind_for_phase(normalized_phase)
    if authority.operation_kind is not expected_kind:
        raise FireShieldError("FIRE_SHIELD_OPERATION_KIND_MISMATCH")
    boundary = authority.boundary
    mode = _resolve_mode(boundary)
    allowed_root, writes_allowed = _phase_write_root(boundary, normalized_phase)
    snapshot = None
    if mode is FireShieldMode.EXTERNAL_PROJECT and writes_allowed:
        snapshot = capture_tool_snapshot(boundary.tool_source_root)
    return FireShieldContext(
        boundary=boundary,
        authority=authority,
        mode=mode,
        phase=normalized_phase,
        operation_id=authority.operation_id,
        allowed_write_root=allowed_root,
        writes_allowed=writes_allowed,
        tool_snapshot=snapshot,
        registry_path=(
            Path(registry_path).expanduser().resolve(strict=False)
            if registry_path is not None
            else None
        ),
    )


def assert_fire_shield_context_current(
    context: FireShieldContext,
) -> None:
    """Recheck selected Project identity immediately before mutation."""
    try:
        assert_project_authority_current(
            context.authority,
            selected_project_root=context.boundary.active_project_root,
            project_epoch=context.authority.project_epoch,
            tool_source_root=context.boundary.tool_source_root,
            registry_path=context.registry_path,
        )
    except ProjectOperationAuthorityError as exc:
        raise FireShieldError(
            "FIRE_SHIELD_PROJECT_IDENTITY_STALE:" + str(exc)
        ) from exc


def assert_fire_shield_write_allowed(
    context: FireShieldContext,
    destination: str | Path,
    *,
    operation: str,
) -> Path:
    """Return one authorized destination or reject the mutation."""
    if not context.writes_allowed:
        raise FireShieldError("FIRE_SHIELD_READ_ONLY_PHASE")
    assert_fire_shield_context_current(context)
    operation_name = str(operation or "").strip().upper()
    if operation_name not in _SUPPORTED_MUTATIONS:
        raise FireShieldError(
            "FIRE_SHIELD_OPERATION_UNSUPPORTED:" + operation_name
        )
    target = Path(destination).expanduser().resolve(strict=False)
    if (
        context.mode is FireShieldMode.EXTERNAL_PROJECT
        and _is_within(target, context.boundary.tool_source_root)
    ):
        raise FireShieldError("FIRE_SHIELD_TOOL_WRITE_BLOCKED:" + str(target))
    try:
        authorized = assert_authorized_project_target(
            context.authority,
            target,
        )
    except ProjectOperationAuthorityError as exc:
        marker = "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE:"
        raise FireShieldError(marker + str(target) + ":" + str(exc)) from exc
    if not _is_within(authorized, context.allowed_write_root):
        raise FireShieldError(
            "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE:" + str(authorized)
        )
    if context.mode is FireShieldMode.EXTERNAL_PROJECT:
        assert_existing_destination_not_tool_alias(context, authorized)
    return authorized


def assert_fire_shield_payload_bytes_allowed(
    context: FireShieldContext,
    raw: bytes,
    relative_path: str,
) -> None:
    """Reject exact Tool copies and private Tool Python dependencies."""
    assert_payload_bytes_not_tool_copy(context, raw, relative_path)
    if str(relative_path).lower().endswith(".py"):
        scan_project_python_source(context, raw, relative_path)


def assert_fire_shield_source_transfer_allowed(
    context: FireShieldContext,
    source: str | Path,
    destination: str | Path,
) -> Path:
    """Reject Tool-owned source becoming external Project payload/source."""
    target = assert_fire_shield_write_allowed(
        context,
        destination,
        operation="WRITE",
    )
    if context.mode is FireShieldMode.KANDA_SELF_HOSTING:
        return target
    source_path = Path(source).expanduser().resolve(strict=False)
    if _is_within(source_path, context.boundary.tool_source_root):
        raise FireShieldError(
            "FIRE_SHIELD_TOOL_SOURCE_IN_PROJECT_PAYLOAD:" + str(source_path)
        )
    if source_path.is_file():
        assert_fire_shield_payload_bytes_allowed(
            context,
            source_path.read_bytes(),
            str(source_path),
        )
    return target


def preflight_fire_shield_archive(
    context: FireShieldContext,
    archive_path: str | Path,
) -> FireShieldArchiveReport:
    """Preflight every package member before any external Project write."""
    archive_file = Path(archive_path).expanduser().resolve(strict=True)
    counts = {
        "PROJECT_PAYLOAD": 0,
        "DELIVERY_CONTROL": 0,
        "FREEZE_HINT": 0,
        "TRANSIENT_EVIDENCE": 0,
    }
    try:
        with zipfile.ZipFile(archive_file, "r") as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise FireShieldError(
                    "FIRE_SHIELD_ARCHIVE_CRC_FAILED:" + bad_member
                )
            plans = validate_archive_members(
                archive,
                context.boundary.active_project_root,
                require_single_top_level=False,
                reject_windows_ambiguous_names=True,
            )
            for plan in plans:
                role = _archive_member_role(plan.normalized_name)
                if role == "AMBIGUOUS":
                    raise FireShieldError(
                        "FIRE_SHIELD_ARCHIVE_MEMBER_ROLE_AMBIGUOUS:"
                        + plan.normalized_name
                    )
                if plan.is_directory:
                    continue
                counts[role] += 1
                if role != "PROJECT_PAYLOAD":
                    continue
                relative = plan.normalized_name[len("payload/") :]
                destination = context.boundary.active_project_root.joinpath(
                    *PurePosixPath(relative).parts
                )
                assert_fire_shield_write_allowed(
                    context,
                    destination,
                    operation="EXTRACT",
                )
                assert_fire_shield_payload_bytes_allowed(
                    context,
                    archive.read(plan.info),
                    relative,
                )
    except ArchiveSafetyError as exc:
        raise FireShieldError(str(exc)) from exc
    return FireShieldArchiveReport(
        archive_path=archive_file,
        member_count=sum(counts.values()),
        project_payload_count=counts["PROJECT_PAYLOAD"],
        delivery_control_count=counts["DELIVERY_CONTROL"],
        freeze_hint_count=counts["FREEZE_HINT"],
        transient_evidence_count=counts["TRANSIENT_EVIDENCE"],
        tool_source_transfer_count=0,
        private_tool_import_count=0,
    )


def _resolve_mode(boundary: ProjectToolBoundaryIdentity) -> FireShieldMode:
    if boundary.self_hosting_mode:
        valid = (
            boundary.selection_mode is ProjectSelectionMode.EXPLICIT_SELF_HOSTING
            and boundary.same_canonical_resolved_root
            and boundary.active_project_slug == TOOL_PROJECT_SLUG
        )
        if not valid:
            raise FireShieldError("FIRE_SHIELD_IDENTITY_AMBIGUOUS")
        return FireShieldMode.KANDA_SELF_HOSTING
    valid_external = (
        boundary.selection_mode
        is ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT
        and not boundary.same_canonical_resolved_root
        and boundary.active_project_slug != TOOL_PROJECT_SLUG
    )
    if not valid_external:
        raise FireShieldError("FIRE_SHIELD_IDENTITY_AMBIGUOUS")
    return FireShieldMode.EXTERNAL_PROJECT


def _phase_write_root(
    boundary: ProjectToolBoundaryIdentity,
    phase: FireShieldPhase,
) -> tuple[Path, bool]:
    if phase is FireShieldPhase.PROJECT_SOURCE_MUTATION:
        return boundary.active_project_root.resolve(strict=False), True
    if phase is FireShieldPhase.PROJECT_TRANSIENT_WRITE:
        return boundary.active_project_daily_work_root.resolve(strict=False), True
    if phase is FireShieldPhase.FREEZE_WRITE:
        return (
            boundary.active_project_support_root / "project_freeze_after_update",
            True,
        )
    if phase is FireShieldPhase.ERROR_MEMORY_WRITE:
        return boundary.active_project_support_root / "project_error_memory", True
    if phase is FireShieldPhase.VALIDATE_READ_ONLY:
        return boundary.active_project_root.resolve(strict=False), False
    raise FireShieldError("FIRE_SHIELD_PHASE_UNSUPPORTED:" + phase.value)


def _operation_kind_for_phase(phase: FireShieldPhase) -> ProjectOperationKind:
    if phase is FireShieldPhase.PROJECT_SOURCE_MUTATION:
        return ProjectOperationKind.PROJECT_SOURCE_WRITE
    if phase is FireShieldPhase.PROJECT_TRANSIENT_WRITE:
        return ProjectOperationKind.PROJECT_TRANSIENT_WRITE
    if phase in {FireShieldPhase.FREEZE_WRITE, FireShieldPhase.ERROR_MEMORY_WRITE}:
        return ProjectOperationKind.PROJECT_SUPPORT_WRITE
    if phase is FireShieldPhase.VALIDATE_READ_ONLY:
        return ProjectOperationKind.PROJECT_SOURCE_READ
    raise FireShieldError("FIRE_SHIELD_PHASE_UNSUPPORTED:" + phase.value)


def _normalize_phase(value: FireShieldPhase | str) -> FireShieldPhase:
    if isinstance(value, FireShieldPhase):
        return value
    text = str(value or "").strip().upper()
    try:
        return FireShieldPhase(text)
    except ValueError as exc:
        raise FireShieldError("FIRE_SHIELD_PHASE_INVALID:" + text) from exc


def _archive_member_role(name: str) -> str:
    normalized = name.rstrip("/")
    if normalized == "KANDA_FREEZE_HINT.json":
        return "FREEZE_HINT"
    if normalized.startswith("payload/"):
        return "PROJECT_PAYLOAD"
    if normalized in _DELIVERY_CONTROL_ROOT_FILES:
        return "DELIVERY_CONTROL"
    if any(normalized.startswith(prefix) for prefix in _DELIVERY_CONTROL_PREFIXES):
        return "DELIVERY_CONTROL"
    if any(normalized.startswith(prefix) for prefix in _EVIDENCE_PREFIXES):
        return "TRANSIENT_EVIDENCE"
    return "AMBIGUOUS"


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False
