# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py
"""Record one reviewed Project Web AI proposal without Project source mutation."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from kanda_reasoner_app.project_fire_shield import (
    FireShieldPhase,
    assert_fire_shield_payload_bytes_allowed,
    build_fire_shield_context_from_authority,
)
from kanda_reasoner_app.project_operation_authority import (
    ProjectOperationAuthority,
    ProjectOperationAuthorityError,
    ProjectOperationKind,
    assert_authorized_project_target,
    build_project_operation_authority,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_contracts import (
    ProjectWebAIApplyAuthorization,
    preview_fingerprint,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts import (
    ProjectWebAIApplyReceipt,
    prepare_receipt_root,
    write_apply_receipt,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
    ProjectWebAIChangeOperation,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
    ProjectWebAIShadowPreview,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
    ProjectWebAISessionIdentity,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_write_storage import (
    contained_project_file,
    contained_shadow_file,
    project_web_ai_sha256_bytes,
    require_distinct_apply_roots,
)
from kanda_reasoner_app.web_ai_provider_contracts import ContextSnapshot

__all__ = [
    "ProjectWebAIApplyError",
    "execute_project_web_ai_apply",
]

_MAX_TOUCHED_PYTHON_LINES = 500
_HEX_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")
_PROPOSAL_STATUS = "PROPOSAL_ONLY"


class ProjectWebAIApplyError(RuntimeError):
    """Raised when proposal evidence cannot be validated or recorded."""

    def __init__(
        self,
        message: str,
        *,
        status: str = "REJECTED",
        receipt: ProjectWebAIApplyReceipt | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.receipt = receipt


def execute_project_web_ai_apply(
    *,
    operation: ProjectWebAIChangeOperation,
    preview: ProjectWebAIShadowPreview,
    authorization: ProjectWebAIApplyAuthorization,
    session_identity: ProjectWebAISessionIdentity,
    context: ContextSnapshot,
) -> ProjectWebAIApplyReceipt:
    """Validate one reviewed proposal and persist support-side evidence only."""
    started_at = _utc_now()
    read_authority, support_authority = _validate_proposal_authority(
        operation,
        preview,
        authorization,
        session_identity,
        context,
    )
    read_boundary = read_authority.boundary
    support_boundary = support_authority.boundary
    project_root = read_boundary.active_project_root.resolve(strict=True)
    daily_root = read_boundary.active_project_daily_work_root.resolve(strict=False)
    support_root = support_boundary.active_project_support_root.resolve(strict=False)
    require_distinct_apply_roots(project_root, daily_root, support_root)
    _assert_matching_boundaries(read_authority, support_authority)

    receipt_target = (
        support_root
        / "project_validation_evidence"
        / "project_web_ai_apply_receipts"
        / (authorization.transaction_id + ".json")
    ).resolve(strict=False)
    assert_authorized_project_target(support_authority, receipt_target)
    receipt_root = prepare_receipt_root(support_root)
    receipt_path = receipt_root / (authorization.transaction_id + ".json")
    if receipt_path.exists():
        raise ProjectWebAIApplyError("APPLY_AUTHORIZATION_ALREADY_CONSUMED")

    markers = _validate_proposal_targets(
        read_authority,
        project_root,
        preview,
        authorization,
    )
    operation_class = (
        "SELF_HOSTING_TOOL_PROPOSAL"
        if read_boundary.self_hosting_mode
        else "EXTERNAL_PROJECT_PROPOSAL"
    )
    receipt = _proposal_receipt(
        operation=operation,
        authorization=authorization,
        operation_class=operation_class,
        project_root=project_root,
        validation_markers=markers,
        started_at=started_at,
    )
    try:
        return write_apply_receipt(support_root, receipt)
    except Exception as exc:
        raise ProjectWebAIApplyError(
            "PROJECT_WEB_AI_PROPOSAL_RECEIPT_FAILED:" + str(exc),
            status="REJECTED",
        ) from exc


def _validate_proposal_authority(
    operation: ProjectWebAIChangeOperation,
    preview: ProjectWebAIShadowPreview,
    authorization: ProjectWebAIApplyAuthorization,
    session_identity: ProjectWebAISessionIdentity,
    context: ContextSnapshot,
) -> tuple[ProjectOperationAuthority, ProjectOperationAuthority]:
    """Validate immutable proposal identity and build read/support authority."""
    for label, value in (
        ("AUTHORIZATION", authorization.authorization_id),
        ("TRANSACTION", authorization.transaction_id),
        ("OPERATION", operation.operation_id),
        ("AUTHORIZED_OPERATION", authorization.operation_id),
    ):
        if _HEX_ID_PATTERN.fullmatch(str(value or "")) is None:
            raise ProjectWebAIApplyError("APPLY_UNSAFE_" + label + "_ID")
    if not session_identity.accepts_request(operation.request_identity, context):
        raise ProjectWebAIApplyError("APPLY_CURRENT_SESSION_IDENTITY_MISMATCH")
    if authorization.operation_id != operation.operation_id:
        raise ProjectWebAIApplyError("APPLY_AUTHORIZATION_OPERATION_MISMATCH")
    if authorization.preview_fingerprint != preview_fingerprint(preview):
        raise ProjectWebAIApplyError("APPLY_PREVIEW_FINGERPRINT_MISMATCH")
    identity = operation.request_identity
    expected = (
        identity.project_id,
        identity.project_root_fingerprint,
        identity.project_epoch,
        identity.snapshot_id,
    )
    actual = (
        authorization.project_id,
        authorization.project_root_fingerprint,
        authorization.project_epoch,
        authorization.snapshot_id,
    )
    if actual != expected:
        raise ProjectWebAIApplyError("APPLY_AUTHORIZATION_IDENTITY_MISMATCH")
    target_paths = tuple(item.relative_path for item in preview.targets)
    if target_paths != authorization.target_paths:
        raise ProjectWebAIApplyError("APPLY_AUTHORIZED_TARGET_SET_MISMATCH")
    try:
        read_authority = build_project_operation_authority(
            operation.project_root,
            operation_kind=ProjectOperationKind.PROJECT_SOURCE_READ,
            operation_id=operation.operation_id + "-proposal-read",
            project_epoch=identity.project_epoch,
            source_snapshot_identity=identity.snapshot_id,
        )
        support_authority = build_project_operation_authority(
            operation.project_root,
            operation_kind=ProjectOperationKind.PROJECT_SUPPORT_WRITE,
            operation_id=operation.operation_id + "-proposal-receipt",
            project_epoch=identity.project_epoch,
            source_snapshot_identity=identity.snapshot_id,
        )
    except ProjectOperationAuthorityError as exc:
        raise ProjectWebAIApplyError(str(exc)) from exc
    boundary = read_authority.boundary
    if boundary.active_project_id != identity.project_id:
        raise ProjectWebAIApplyError("APPLY_PROJECT_ID_STALE")
    if boundary.active_project_root_fingerprint != identity.project_root_fingerprint:
        raise ProjectWebAIApplyError("APPLY_PROJECT_ROOT_FINGERPRINT_STALE")
    if str(boundary.active_project_support_root) != identity.support_root:
        raise ProjectWebAIApplyError("APPLY_SUPPORT_ROOT_IDENTITY_MISMATCH")
    if str(boundary.active_project_daily_work_root) != operation.daily_work_root:
        raise ProjectWebAIApplyError("APPLY_DAILY_ROOT_IDENTITY_MISMATCH")
    return read_authority, support_authority


def _assert_matching_boundaries(
    read_authority: ProjectOperationAuthority,
    support_authority: ProjectOperationAuthority,
) -> None:
    """Reject mismatched read and support authority identities."""
    read = read_authority.boundary
    support = support_authority.boundary
    if (
        read.active_project_id != support.active_project_id
        or read.active_project_root_fingerprint
        != support.active_project_root_fingerprint
        or read.active_project_root != support.active_project_root
    ):
        raise ProjectWebAIApplyError("APPLY_PROPOSAL_AUTHORITY_BOUNDARY_MISMATCH")


def _validate_proposal_targets(
    authority: ProjectOperationAuthority,
    project_root: Path,
    preview: ProjectWebAIShadowPreview,
    authorization: ProjectWebAIApplyAuthorization,
) -> tuple[str, ...]:
    """Validate exact source freshness and Shadow proposal bytes read-only."""
    fire_shield = build_fire_shield_context_from_authority(
        authority,
        phase=FireShieldPhase.VALIDATE_READ_ONLY,
    )
    python_seen = False
    for index, item in enumerate(preview.targets):
        source_path = contained_project_file(project_root, item.relative_path)
        assert_authorized_project_target(authority, source_path)
        shadow_path = contained_shadow_file(preview, item.relative_path)
        source_raw = source_path.read_bytes()
        shadow_raw = shadow_path.read_bytes()
        if project_web_ai_sha256_bytes(source_raw) != authorization.source_sha256[index]:
            raise ProjectWebAIApplyError(
                "APPLY_IMMEDIATE_SOURCE_FRESHNESS_MISMATCH:" + item.relative_path
            )
        if project_web_ai_sha256_bytes(shadow_raw) != authorization.proposed_sha256[index]:
            raise ProjectWebAIApplyError(
                "APPLY_SHADOW_PAYLOAD_HASH_MISMATCH:" + item.relative_path
            )
        assert_fire_shield_payload_bytes_allowed(
            fire_shield,
            shadow_raw,
            item.relative_path,
        )
        if item.relative_path.lower().endswith(".py"):
            python_seen = True
            text = shadow_raw.decode("utf-8-sig", errors="strict")
            compile(text, item.relative_path, "exec")
            if len(text.splitlines()) > _MAX_TOUCHED_PYTHON_LINES:
                raise ProjectWebAIApplyError(
                    "APPLY_TOUCHED_PYTHON_MODULE_OVER_500_LINES:"
                    + item.relative_path
                )
    markers = [
        "PROJECT_WEB_AI_PROPOSAL_TARGET_CONTAINMENT: PASS",
        "PROJECT_WEB_AI_SOURCE_FRESHNESS: PASS",
        "PROJECT_WEB_AI_SHADOW_PAYLOAD_VALIDATED: PASS",
        "PROJECT_WEB_AI_PROJECT_SOURCE_WRITE: ABSENT",
        "PROJECT_WEB_AI_PROPOSAL_ONLY: PASS",
    ]
    markers.append(
        "PROJECT_WEB_AI_PROPOSAL_PYTHON_SYNTAX: PASS"
        if python_seen
        else "PROJECT_WEB_AI_PROPOSAL_PYTHON_SYNTAX: NOT_APPLICABLE"
    )
    markers.extend(fire_shield.markers())
    markers.append("FIRE_SHIELD_PROJECT_SOURCE_MUTATION_REQUEST: ABSENT")
    return tuple(markers)


def _proposal_receipt(
    *,
    operation: ProjectWebAIChangeOperation,
    authorization: ProjectWebAIApplyAuthorization,
    operation_class: str,
    project_root: Path,
    validation_markers: tuple[str, ...],
    started_at: str,
) -> ProjectWebAIApplyReceipt:
    """Build one durable proposal-only receipt using the legacy receipt schema."""
    return ProjectWebAIApplyReceipt(
        schema_version="1.1-proposal-only",
        transaction_id=authorization.transaction_id,
        authorization_id=authorization.authorization_id,
        operation_id=authorization.operation_id,
        status=_PROPOSAL_STATUS,
        operation_class=operation_class,
        project_id=authorization.project_id,
        project_root=str(project_root),
        project_root_fingerprint=authorization.project_root_fingerprint,
        project_epoch=authorization.project_epoch,
        snapshot_id=authorization.snapshot_id,
        preview_fingerprint=authorization.preview_fingerprint,
        changed_files=authorization.target_paths,
        source_sha256=authorization.source_sha256,
        installed_sha256=authorization.source_sha256,
        backup_root="",
        validation_markers=validation_markers,
        started_at_utc=started_at,
        completed_at_utc=_utc_now(),
        error="",
    )


def _utc_now() -> str:
    """Return one UTC ISO timestamp."""
    return datetime.now(timezone.utc).isoformat()
