# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py
"""Execute one explicit Project Web AI source-write transaction with rollback.

This deterministic local broker is the only Phase 3 owner allowed to mutate the
selected active Project. The remote AI never receives or invokes this API.
"""

from __future__ import annotations

import re
import stat
from datetime import datetime, timezone
from pathlib import Path

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
    atomic_replace_source,
    contained_project_file,
    contained_shadow_file,
    exclusive_apply_lock,
    require_distinct_apply_roots,
    project_web_ai_sha256_bytes,
    write_source_backups,
    write_transaction_state,
)
from kanda_reasoner_app.web_ai_provider_contracts import ContextSnapshot

__all__ = [
    "ProjectWebAIApplyError",
    "execute_project_web_ai_apply",
]

_MAX_TOUCHED_PYTHON_LINES = 500
_HEX_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")


class ProjectWebAIApplyError(RuntimeError):
    """Raised when apply is rejected, rolled back, or unresolved."""

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
    """Apply one exact authorized Preview and return a durable receipt."""
    started_at = _utc_now()
    authority = _validate_authority(
        operation,
        preview,
        authorization,
        session_identity,
        context,
    )
    boundary = authority.boundary
    project_root = boundary.active_project_root.resolve(strict=True)
    daily_root = boundary.active_project_daily_work_root.resolve(strict=False)
    support_root = boundary.active_project_support_root.resolve(strict=False)
    require_distinct_apply_roots(project_root, daily_root, support_root)
    receipt_root = prepare_receipt_root(support_root)
    receipt_path = receipt_root / (authorization.transaction_id + ".json")

    operation_class = (
        "SELF_HOSTING_TOOL_CHANGE"
        if boundary.self_hosting_mode
        else "EXTERNAL_PROJECT_CHANGE"
    )
    transaction_root = (
        daily_root
        / "project_web_ai_apply_transactions"
        / authorization.transaction_id
    ).resolve(strict=False)
    backup_root = (transaction_root / "backups").resolve(strict=False)
    state_path = (transaction_root / "transaction_state.json").resolve(strict=False)
    if receipt_path.exists() or transaction_root.exists():
        raise ProjectWebAIApplyError("APPLY_AUTHORIZATION_ALREADY_CONSUMED")
    lock_root = daily_root / "project_web_ai_apply_transactions" / "locks"
    lock_path = lock_root / (operation.operation_id + ".lock")
    source_before: dict[str, bytes] = {}
    source_modes: dict[str, int] = {}

    with exclusive_apply_lock(lock_path, authorization.transaction_id):
        try:
            transaction_root.mkdir(parents=True, exist_ok=False)
            backup_root.mkdir(parents=True, exist_ok=False)
            write_transaction_state(
                state_path,
                authorization,
                status="APPLYING",
                error="",
                updated_at_utc=_utc_now(),
            )
            source_before, source_modes = _preflight_targets(
                authority,
                project_root,
                preview,
                authorization,
            )
            write_source_backups(backup_root, source_before)
            for item in preview.targets:
                source_path = contained_project_file(
                    project_root,
                    item.relative_path,
                )
                shadow_path = contained_shadow_file(
                    preview,
                    item.relative_path,
                )
                proposed = shadow_path.read_bytes()
                atomic_replace_source(
                    source_path,
                    proposed,
                    source_modes[item.relative_path],
                    authorization.transaction_id,
                )
            markers = _validate_installed_source(
                project_root,
                preview,
                authorization,
            )
            receipt = _receipt(
                operation=operation,
                authorization=authorization,
                status="APPLIED_SOURCE_VERIFIED",
                operation_class=operation_class,
                project_root=project_root,
                backup_root=backup_root,
                validation_markers=markers,
                started_at=started_at,
                error="",
            )
            receipt = write_apply_receipt(support_root, receipt)
            try:
                write_transaction_state(
                    state_path,
                    authorization,
                    status=receipt.status,
                    error="",
                    updated_at_utc=_utc_now(),
                    receipt_path=receipt.receipt_path,
                )
            except OSError:
                pass
            return receipt
        except Exception as exc:
            rollback_error = ""
            try:
                rollback_markers = _rollback(
                    project_root,
                    backup_root,
                    source_before,
                    source_modes,
                )
                status = "ROLLED_BACK"
            except Exception as rollback_exc:
                rollback_markers = ("PROJECT_WEB_AI_ROLLBACK_FAILED",)
                rollback_error = str(rollback_exc)
                status = "UNRESOLVED"
            receipt = _receipt(
                operation=operation,
                authorization=authorization,
                status=status,
                operation_class=operation_class,
                project_root=project_root,
                backup_root=backup_root,
                validation_markers=rollback_markers,
                started_at=started_at,
                error=str(exc) + (" | rollback: " + rollback_error if rollback_error else ""),
            )
            try:
                receipt = write_apply_receipt(support_root, receipt)
            except Exception:
                write_transaction_state(
                    state_path,
                    authorization,
                    status=status,
                    error=receipt.error,
                    updated_at_utc=_utc_now(),
                )
            else:
                try:
                    write_transaction_state(
                        state_path,
                        authorization,
                        status=status,
                        error=receipt.error,
                        updated_at_utc=_utc_now(),
                        receipt_path=receipt.receipt_path,
                    )
                except OSError:
                    pass
            raise ProjectWebAIApplyError(
                "PROJECT_WEB_AI_APPLY_" + status + ":" + str(exc),
                status=status,
                receipt=receipt,
            ) from exc


def _validate_authority(
    operation: ProjectWebAIChangeOperation,
    preview: ProjectWebAIShadowPreview,
    authorization: ProjectWebAIApplyAuthorization,
    session_identity: ProjectWebAISessionIdentity,
    context: ContextSnapshot,
):
    """Validate immutable operation, Preview, session, and boundary identity."""
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
    try:
        authority = build_project_operation_authority(
            operation.project_root,
            operation_kind=ProjectOperationKind.PROJECT_SOURCE_WRITE,
            operation_id=operation.operation_id,
            project_epoch=identity.project_epoch,
            source_snapshot_identity=identity.snapshot_id,
        )
    except ProjectOperationAuthorityError as exc:
        raise ProjectWebAIApplyError(str(exc)) from exc
    boundary = authority.boundary
    if boundary.active_project_id != identity.project_id:
        raise ProjectWebAIApplyError("APPLY_PROJECT_ID_STALE")
    if boundary.active_project_root_fingerprint != identity.project_root_fingerprint:
        raise ProjectWebAIApplyError("APPLY_PROJECT_ROOT_FINGERPRINT_STALE")
    if str(boundary.active_project_support_root) != identity.support_root:
        raise ProjectWebAIApplyError("APPLY_SUPPORT_ROOT_IDENTITY_MISMATCH")
    if str(boundary.active_project_daily_work_root) != operation.daily_work_root:
        raise ProjectWebAIApplyError("APPLY_DAILY_ROOT_IDENTITY_MISMATCH")
    target_paths = tuple(item.relative_path for item in preview.targets)
    if target_paths != authorization.target_paths:
        raise ProjectWebAIApplyError("APPLY_AUTHORIZED_TARGET_SET_MISMATCH")
    return authority


def _preflight_targets(
    authority: ProjectOperationAuthority,
    project_root: Path,
    preview: ProjectWebAIShadowPreview,
    authorization: ProjectWebAIApplyAuthorization,
) -> tuple[dict[str, bytes], dict[str, int]]:
    """Recheck exact disk bytes and Shadow payload immediately before write."""
    source_before: dict[str, bytes] = {}
    source_modes: dict[str, int] = {}
    for index, item in enumerate(preview.targets):
        source_path = contained_project_file(project_root, item.relative_path)
        assert_authorized_project_target(authority, source_path)
        shadow_path = contained_shadow_file(preview, item.relative_path)
        source_raw = source_path.read_bytes()
        shadow_raw = shadow_path.read_bytes()
        if (
            project_web_ai_sha256_bytes(source_raw)
            != authorization.source_sha256[index]
        ):
            raise ProjectWebAIApplyError(
                "APPLY_IMMEDIATE_SOURCE_FRESHNESS_MISMATCH:" + item.relative_path
            )
        if (
            project_web_ai_sha256_bytes(shadow_raw)
            != authorization.proposed_sha256[index]
        ):
            raise ProjectWebAIApplyError(
                "APPLY_SHADOW_PAYLOAD_HASH_MISMATCH:" + item.relative_path
            )
        source_before[item.relative_path] = source_raw
        source_modes[item.relative_path] = stat.S_IMODE(source_path.stat().st_mode)
    return source_before, source_modes


def _validate_installed_source(
    project_root: Path,
    preview: ProjectWebAIShadowPreview,
    authorization: ProjectWebAIApplyAuthorization,
) -> tuple[str, ...]:
    """Verify installed hashes, Python syntax, and module-size limits."""
    markers = [
        "PROJECT_WEB_AI_APPLY_TARGET_CONTAINMENT: PASS",
        "PROJECT_WEB_AI_APPLY_INSTALLED_HASHES: PASS",
    ]
    python_seen = False
    for index, item in enumerate(preview.targets):
        path = contained_project_file(project_root, item.relative_path)
        raw = path.read_bytes()
        if (
            project_web_ai_sha256_bytes(raw)
            != authorization.proposed_sha256[index]
        ):
            raise ProjectWebAIApplyError(
                "APPLY_INSTALLED_HASH_MISMATCH:" + item.relative_path
            )
        if item.relative_path.lower().endswith(".py"):
            python_seen = True
            text = raw.decode("utf-8-sig", errors="strict")
            compile(text, item.relative_path, "exec")
            if len(text.splitlines()) > _MAX_TOUCHED_PYTHON_LINES:
                raise ProjectWebAIApplyError(
                    "APPLY_TOUCHED_PYTHON_MODULE_OVER_500_LINES:"
                    + item.relative_path
                )
    markers.append(
        "PROJECT_WEB_AI_APPLY_PYTHON_SYNTAX: PASS"
        if python_seen
        else "PROJECT_WEB_AI_APPLY_PYTHON_SYNTAX: NOT_APPLICABLE"
    )
    markers.extend(
        (
            "PROJECT_WEB_AI_APPLY_SOURCE_VERIFICATION: PASS",
            "PROJECT_WEB_AI_APPLY_RECEIPT_REQUIRED: PASS",
        )
    )
    return tuple(markers)


def _rollback(
    project_root: Path,
    backup_root: Path,
    source_before: dict[str, bytes],
    source_modes: dict[str, int],
) -> tuple[str, ...]:
    """Restore every original file and verify exact source hashes."""
    for relative_path, original in reversed(tuple(source_before.items())):
        backup = (backup_root / relative_path).resolve(strict=True)
        if backup.read_bytes() != original:
            raise ProjectWebAIApplyError("APPLY_ROLLBACK_BACKUP_HASH_MISMATCH")
        target = contained_project_file(project_root, relative_path)
        atomic_replace_source(
            target,
            original,
            source_modes[relative_path],
            "rollback",
        )
    for relative_path, original in source_before.items():
        target = contained_project_file(project_root, relative_path)
        if target.read_bytes() != original:
            raise ProjectWebAIApplyError(
                "APPLY_ROLLBACK_SOURCE_HASH_MISMATCH:" + relative_path
            )
    return (
        "PROJECT_WEB_AI_APPLY_ROLLBACK_COMPLETED: PASS",
        "PROJECT_WEB_AI_APPLY_ORIGINAL_HASHES_RESTORED: PASS",
    )


def _receipt(
    *,
    operation: ProjectWebAIChangeOperation,
    authorization: ProjectWebAIApplyAuthorization,
    status: str,
    operation_class: str,
    project_root: Path,
    backup_root: Path,
    validation_markers: tuple[str, ...],
    started_at: str,
    error: str,
) -> ProjectWebAIApplyReceipt:
    """Build one terminal receipt from exact transaction identity."""
    return ProjectWebAIApplyReceipt(
        schema_version="1.0",
        transaction_id=authorization.transaction_id,
        authorization_id=authorization.authorization_id,
        operation_id=authorization.operation_id,
        status=status,
        operation_class=operation_class,
        project_id=authorization.project_id,
        project_root=str(project_root),
        project_root_fingerprint=authorization.project_root_fingerprint,
        project_epoch=authorization.project_epoch,
        snapshot_id=authorization.snapshot_id,
        preview_fingerprint=authorization.preview_fingerprint,
        changed_files=authorization.target_paths,
        source_sha256=authorization.source_sha256,
        installed_sha256=authorization.proposed_sha256,
        backup_root=str(backup_root),
        validation_markers=validation_markers,
        started_at_utc=started_at,
        completed_at_utc=_utc_now(),
        error=error,
    )


def _utc_now() -> str:
    """Return one UTC ISO timestamp."""
    return datetime.now(timezone.utc).isoformat()
