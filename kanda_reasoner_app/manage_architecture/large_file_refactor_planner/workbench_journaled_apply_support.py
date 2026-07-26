# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_support.py
"""Durable operation planning and evidence helpers for journaled Workbench apply."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .workbench_execution_basis import WorkbenchExecutionBasisSet, execution_basis_is_fresh
from .workbench_journaled_apply_models import JournaledApplyAuthorization, JournaledApplyResult
from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult
from .workbench_refactor_transaction import WorkbenchRefactorTransaction
from .workbench_sealed_payload import WorkbenchSealedPayload, verify_sealed_payload
from .workbench_source_mutation_primitives import (
    SourceMutationOperation,
    build_source_mutation_operations,
    copy_operations_with_payload_root,
    current_file_hash,
)
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult
from .workbench_transaction_store import WorkbenchTransactionStore

__all__ = [
    "entry_blockers",
    "load_or_prepare_operations",
    "write_execution_manifest",
    "checked_rules",
]

_OPERATION_PLAN_ARTIFACT = "JOURNALED_OPERATION_PLAN"
_EXECUTION_MANIFEST = "JOURNALED_APPLY_EXECUTION.json"
_ROLLBACK_MANIFEST = "JOURNALED_ROLLBACK_MANIFEST.json"


def entry_blockers(
    *,
    transaction: WorkbenchRefactorTransaction,
    authorization: JournaledApplyAuthorization,
    execution_basis: WorkbenchExecutionBasisSet,
    sealed_payload: WorkbenchSealedPayload,
    source_payload: SourceApplyPayloadReadinessResult,
    preflight_backup: WorkbenchPreflightBackupReadinessResult,
) -> list[str]:
    """Return all fail-closed blockers before project lane reservation."""
    blockers: list[str] = []
    if transaction.transaction_state != "PREPARED":
        blockers.append("WORKBENCH_TRANSACTION_NOT_PREPARED")
    if not authorization.authorized:
        blockers.append("JOURNALED_APPLY_AUTHORIZATION_NOT_VALID")
    if authorization.transaction_id != transaction.transaction_id:
        blockers.append("AUTHORIZATION_TRANSACTION_ID_MISMATCH")
    if authorization.contract_hash != transaction.contract_hash:
        blockers.append("AUTHORIZATION_CONTRACT_HASH_MISMATCH")
    if authorization.payload_hash != sealed_payload.payload_hash:
        blockers.append("AUTHORIZATION_PAYLOAD_HASH_MISMATCH")
    fresh, basis_blockers = execution_basis_is_fresh(execution_basis)
    if not fresh:
        blockers.extend(basis_blockers)
    valid_payload, payload_blockers = verify_sealed_payload(sealed_payload)
    if not valid_payload:
        blockers.extend(payload_blockers)
    if source_payload.status != "source_apply_payload_ready":
        blockers.append("SOURCE_APPLY_PAYLOAD_NOT_READY")
    if preflight_backup.status != "preflight_backup_ready":
        blockers.append("PREFLIGHT_BACKUP_NOT_READY")
    blockers.extend(_sealed_source_payload_mismatches(sealed_payload, source_payload))
    return sorted(set(blockers))


def load_or_prepare_operations(
    *,
    transaction: WorkbenchRefactorTransaction,
    source_payload: SourceApplyPayloadReadinessResult,
    sealed_payload: WorkbenchSealedPayload,
    transaction_store: WorkbenchTransactionStore,
) -> tuple[SourceMutationOperation, ...]:
    """Load durable operation plan or create it before first source mutation."""
    existing = transaction_store.list_operations(transaction.transaction_id)
    saved = transaction_store.load_artifact(transaction.transaction_id, _OPERATION_PLAN_ARTIFACT)
    if existing or saved:
        if not existing or saved is None:
            raise RuntimeError("JOURNAL_OPERATION_PLAN_PARTIAL_STATE")
        operations = tuple(SourceMutationOperation(**item) for item in saved.get("operations", []))
        if not operations:
            raise RuntimeError("JOURNALED_OPERATION_PLAN_EMPTY")
        return operations
    operations, blockers = build_source_mutation_operations(
        source_payload=source_payload,
        active_project_root=transaction.project_root,
    )
    if blockers:
        raise RuntimeError("SOURCE_MUTATION_OPERATION_PLAN_BLOCKED:" + "|".join(blockers))
    tx_root = Path(transaction.durable_transaction_root).resolve()
    payload_root = tx_root / "payload"
    backups_root = tx_root / "backups"
    payload_root.mkdir(parents=True, exist_ok=True)
    backups_root.mkdir(parents=True, exist_ok=True)
    _stage_payload_copies(operations, payload_root)
    rebound = copy_operations_with_payload_root(operations, payload_root=payload_root)
    operation_items: list[dict[str, Any]] = []
    for operation in rebound:
        backup_path = _stage_backup(operation, backups_root)
        transaction_store.register_operation(
            transaction_id=transaction.transaction_id,
            sequence_no=operation.sequence_no,
            operation_type=operation.operation_type,
            target_path=operation.destination_path,
            precondition_hash=operation.precondition_hash,
            payload_hash=operation.payload_hash,
            backup_path=backup_path,
        )
        operation_items.append(operation.to_dict())
    _write_rollback_manifest(transaction, transaction_store)
    transaction_store.store_artifact(
        transaction.transaction_id,
        _OPERATION_PLAN_ARTIFACT,
        {
            "operations": operation_items,
            "metadata": {
                "target_file": source_payload.target_file,
                "source_hash_before": source_payload.source_content_hash,
                "preview_root": source_payload.preview_root,
                "sealed_payload_hash": sealed_payload.payload_hash,
            },
        },
    )
    return rebound


def load_persisted_operation_plan(
    *,
    transaction_id: str,
    transaction_store: WorkbenchTransactionStore,
) -> tuple[tuple[SourceMutationOperation, ...], dict[str, Any]]:
    """Load exact durable operation and metadata evidence for restart recovery."""
    saved = transaction_store.load_artifact(transaction_id, _OPERATION_PLAN_ARTIFACT)
    if saved is None:
        raise RuntimeError("JOURNALED_OPERATION_PLAN_MISSING")
    operations = tuple(SourceMutationOperation(**item) for item in saved.get("operations", []))
    if not operations:
        raise RuntimeError("JOURNALED_OPERATION_PLAN_EMPTY")
    metadata = saved.get("metadata", {})
    if not isinstance(metadata, dict):
        raise RuntimeError("JOURNALED_OPERATION_PLAN_METADATA_INVALID")
    return operations, metadata


def build_applied_result(
    *,
    transaction_id: str,
    target_file: str,
    source_hash_before: str,
    preview_root: str,
    operations: tuple[SourceMutationOperation, ...],
    written: list[str],
    feature_id: str,
    checked: list[str],
) -> JournaledApplyResult:
    """Build successful write result while transaction awaits validation."""
    tx_root = Path(operations[0].payload_path).resolve().parents[1]
    return JournaledApplyResult(
        schema_version="1.0",
        feature_id=feature_id,
        status="applied",
        transaction_id=transaction_id,
        target_file=target_file,
        source_content_hash_before=source_hash_before,
        source_content_hash_after=current_file_hash(target_file),
        preview_root=preview_root,
        rollback_manifest_path=str(tx_root / _ROLLBACK_MANIFEST),
        execution_manifest_path=str(tx_root / _EXECUTION_MANIFEST),
        source_mutation_enabled=True,
        import_rewrite_enabled=False,
        lane_state="VALIDATING",
        transaction_state="VALIDATING",
        written_files=sorted(written),
        generated_files=sorted(
            operation.destination_path
            for operation in operations
            if operation.operation_type == "CREATE_FILE"
        ),
        operations_verified=len(operations),
        blockers=[],
        warnings=[
            "JOURNALED_APPLY_REQUIRES_POST_APPLY_VALIDATION_BEFORE_COMPLETION",
            "ROLLBACK_REMAINS_AVAILABLE_UNTIL_TERMINAL_RECOVERY_DECISION",
        ],
        checked_rules=checked,
    )


def build_recovery_result(
    *,
    transaction_id: str,
    target_file: str,
    source_hash_before: str,
    preview_root: str,
    operations: tuple[SourceMutationOperation, ...],
    written: list[str],
    error: str,
    transaction_store: WorkbenchTransactionStore,
    feature_id: str,
    checked: list[str],
) -> JournaledApplyResult:
    """Build recovery-pending result after an interrupted journaled apply."""
    tx = transaction_store.get_transaction(transaction_id) or {}
    tx_root = Path(str(tx.get("transaction_root", "."))).resolve()
    return JournaledApplyResult(
        schema_version="1.0",
        feature_id=feature_id,
        status="recovery_pending",
        transaction_id=transaction_id,
        target_file=target_file,
        source_content_hash_before=source_hash_before,
        source_content_hash_after=current_file_hash(target_file),
        preview_root=preview_root,
        rollback_manifest_path=str(tx_root / _ROLLBACK_MANIFEST),
        execution_manifest_path=str(tx_root / _EXECUTION_MANIFEST),
        source_mutation_enabled=bool(written),
        import_rewrite_enabled=False,
        lane_state="RECOVERY_PENDING",
        transaction_state="RECOVERY_PENDING",
        written_files=sorted(written),
        generated_files=sorted(
            operation.destination_path
            for operation in operations
            if operation.operation_type == "CREATE_FILE" and Path(operation.destination_path).exists()
        ),
        operations_verified=sum(
            1 for item in transaction_store.list_operations(transaction_id) if item["state"] == "VERIFIED"
        ),
        blockers=["JOURNALED_APPLY_INTERRUPTED:" + error],
        warnings=["PROJECT_MUTATION_LANE_REMAINS_CLOSED"],
        checked_rules=checked,
    )


def write_execution_manifest(
    result: JournaledApplyResult,
    transaction_store: WorkbenchTransactionStore,
) -> None:
    """Write durable human-readable execution evidence beside transaction state."""
    tx = transaction_store.get_transaction(result.transaction_id)
    if tx is None:
        raise RuntimeError("TRANSACTION_MISSING_WHILE_WRITING_EXECUTION_MANIFEST")
    path = Path(str(tx["transaction_root"])) / _EXECUTION_MANIFEST
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def checked_rules() -> list[str]:
    """Return stable safety claims exercised by the journaled executor."""
    return [
        "immutable_authorization_hash_valid",
        "semantic_review_warning_acknowledgment_and_summary_confirmation_required",
        "canonical_executor_freeze_proof_required",
        "execution_basis_rechecked_immediately_before_lane_reservation",
        "sealed_payload_verified_immediately_before_apply",
        "source_payload_destination_and_hash_set_matches_seal",
        "serial_project_lane_reserved_before_first_write",
        "durable_payload_copy_verified_before_first_write",
        "per_file_backup_verified_before_replace",
        "operation_intent_durable_before_physical_write",
        "physical_write_uses_shared_exact_byte_mutation_primitive",
        "result_hash_verified_before_operation_verified_state",
        "interruption_keeps_lane_recovery_pending",
        "post_apply_validation_required_before_terminal_completion",
    ]


def _stage_payload_copies(
    operations: tuple[SourceMutationOperation, ...],
    payload_root: Path,
) -> None:
    for operation in operations:
        raw = Path(operation.payload_path).read_bytes()
        durable = payload_root / operation.relative_path
        durable.parent.mkdir(parents=True, exist_ok=True)
        durable.write_bytes(raw)
        if current_file_hash(durable) != operation.payload_hash:
            raise RuntimeError("DURABLE_PAYLOAD_COPY_HASH_MISMATCH:" + operation.relative_path)


def _stage_backup(operation: SourceMutationOperation, backups_root: Path) -> str:
    if operation.operation_type != "REPLACE_FILE":
        return ""
    destination = Path(operation.destination_path)
    backup = backups_root / operation.relative_path
    backup.parent.mkdir(parents=True, exist_ok=True)
    backup.write_bytes(destination.read_bytes())
    if current_file_hash(backup) != operation.precondition_hash:
        raise RuntimeError("OPERATION_BACKUP_HASH_MISMATCH:" + operation.relative_path)
    return str(backup.resolve())


def _write_rollback_manifest(
    transaction: WorkbenchRefactorTransaction,
    transaction_store: WorkbenchTransactionStore,
) -> None:
    path = Path(transaction.durable_transaction_root) / _ROLLBACK_MANIFEST
    path.write_text(
        json.dumps(
            {
                "transaction_id": transaction.transaction_id,
                "operations": transaction_store.list_operations(transaction.transaction_id),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _sealed_source_payload_mismatches(
    sealed_payload: WorkbenchSealedPayload,
    source_payload: SourceApplyPayloadReadinessResult,
) -> list[str]:
    sealed = {
        str(Path(item.destination_path).resolve()): item.content_hash
        for item in sealed_payload.files
    }
    source = {
        str(Path(item.destination_path).resolve()): item.content_hash
        for item in source_payload.files
    }
    blockers: list[str] = []
    if set(sealed) != set(source):
        blockers.append("SOURCE_PAYLOAD_DESTINATION_SET_DIFFERS_FROM_SEAL")
    for path in sorted(set(sealed) & set(source), key=str.casefold):
        if sealed[path] != source[path]:
            blockers.append("SOURCE_PAYLOAD_HASH_DIFFERS_FROM_SEAL:" + path)
    return blockers
