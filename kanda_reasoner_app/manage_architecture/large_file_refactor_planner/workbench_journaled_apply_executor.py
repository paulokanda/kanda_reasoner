# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_executor.py
"""Journaled exact-payload executor for the final Refactor Large Module action."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from kanda_reasoner_app.engineering_safety.project_mutation_lane import ProjectMutationLaneStore

from .workbench_execution_basis import WorkbenchExecutionBasisSet
from .workbench_journaled_apply_models import (
    JOURNALED_APPLY_EXECUTOR_FEATURE_ID,
    JournaledApplyAuthorization,
    JournaledApplyResult,
    build_blocked_apply_result,
)
from .workbench_journaled_apply_support import (
    build_applied_result,
    build_recovery_result,
    checked_rules,
    entry_blockers,
    load_or_prepare_operations,
    load_persisted_operation_plan,
    write_execution_manifest,
)
from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult
from .workbench_refactor_transaction import WorkbenchRefactorTransaction, reserve_workbench_project_lane
from .workbench_sealed_payload import WorkbenchSealedPayload
from .workbench_source_mutation_primitives import (
    SourceMutationOperation,
    apply_source_mutation_operation,
    current_file_hash,
    verify_source_mutation_operation,
)
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult
from .workbench_transaction_store import WorkbenchTransactionStore

__all__ = [
    "execute_journaled_refactor_apply",
    "resume_journaled_refactor_apply",
    "finalize_journaled_refactor_transaction",
]

_APPLY_AUTH_ARTIFACT = "JOURNALED_APPLY_AUTHORIZATION"
_APPLY_RESULT_ARTIFACT = "JOURNALED_APPLY_RESULT"


def execute_journaled_refactor_apply(
    *,
    transaction: WorkbenchRefactorTransaction,
    authorization: JournaledApplyAuthorization,
    execution_basis: WorkbenchExecutionBasisSet,
    sealed_payload: WorkbenchSealedPayload,
    source_payload: SourceApplyPayloadReadinessResult,
    preflight_backup: WorkbenchPreflightBackupReadinessResult,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
    failure_injection: str = "",
) -> JournaledApplyResult:
    """Reserve lane and execute exact sealed bytes through durable operation journal."""
    blockers = entry_blockers(
        transaction=transaction,
        authorization=authorization,
        execution_basis=execution_basis,
        sealed_payload=sealed_payload,
        source_payload=source_payload,
        preflight_backup=preflight_backup,
    )
    if blockers:
        return build_blocked_apply_result(
            transaction_id=transaction.transaction_id,
            target_file=source_payload.target_file,
            source_hash_before=source_payload.source_content_hash,
            preview_root=source_payload.preview_root,
            transaction_root=transaction.durable_transaction_root,
            lane_state=transaction.lane_state,
            transaction_state=transaction.transaction_state,
            blockers=blockers,
            checked_rules=checked_rules(),
        )
    reserved = reserve_workbench_project_lane(
        transaction=transaction,
        transaction_store=transaction_store,
        mutation_lane_store=mutation_lane_store,
    )
    mutation_lane_store.transition(reserved.mutation_request_id, "EXECUTING")
    transaction_store.transition_transaction(reserved.transaction_id, "EXECUTING")
    _store_authorization(reserved.transaction_id, authorization, transaction_store)
    operations = load_or_prepare_operations(
        transaction=reserved,
        source_payload=source_payload,
        sealed_payload=sealed_payload,
        transaction_store=transaction_store,
    )
    return _execute_operation_sequence(
        transaction_id=reserved.transaction_id,
        mutation_request_id=reserved.mutation_request_id,
        target_file=source_payload.target_file,
        source_hash_before=source_payload.source_content_hash,
        preview_root=source_payload.preview_root,
        operations=operations,
        transaction_store=transaction_store,
        mutation_lane_store=mutation_lane_store,
        failure_injection=failure_injection,
    )


def resume_journaled_refactor_apply(
    *,
    transaction_id: str,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
    failure_injection: str = "",
) -> JournaledApplyResult:
    """Resume one durable recovery-pending transaction without live Planner state."""
    tx = transaction_store.get_transaction(transaction_id)
    if tx is None:
        raise KeyError("WORKBENCH_TRANSACTION_NOT_FOUND")
    operations, metadata = load_persisted_operation_plan(
        transaction_id=transaction_id,
        transaction_store=transaction_store,
    )
    request_id = str(tx["mutation_request_id"])
    request = mutation_lane_store.get_request(request_id)
    if request is None:
        raise RuntimeError("MUTATION_REQUEST_NOT_FOUND")
    state = str(request["state"])
    if state == "RECOVERY_PENDING":
        mutation_lane_store.transition(request_id, "EXECUTING", reason="RESUME_JOURNALED_APPLY")
    elif state not in {"EXECUTING", "VALIDATING"}:
        raise RuntimeError("MUTATION_REQUEST_NOT_RESUMABLE:" + state)
    transaction_store.transition_transaction(
        transaction_id,
        "EXECUTING",
        recovery_state="RESUME_IN_PROGRESS",
    )
    return _execute_operation_sequence(
        transaction_id=transaction_id,
        mutation_request_id=request_id,
        target_file=str(metadata.get("target_file", "")),
        source_hash_before=str(metadata.get("source_hash_before", "")),
        preview_root=str(metadata.get("preview_root", "")),
        operations=operations,
        transaction_store=transaction_store,
        mutation_lane_store=mutation_lane_store,
        failure_injection=failure_injection,
    )


def finalize_journaled_refactor_transaction(
    *,
    result: JournaledApplyResult,
    structural_pass: bool,
    behavior_status: str,
    behavior_risk_accepted: bool,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
) -> str:
    """Finalize or hold recovery based on post-apply and behavior evidence."""
    if result.status != "applied":
        raise ValueError("JOURNALED_APPLY_NOT_READY_FOR_FINALIZATION")
    request_id = _request_id_for(transaction_store, result.transaction_id)
    if not structural_pass or behavior_status == "BEHAVIOR_VALIDATION_FAILED":
        _hold_recovery(
            transaction_id=result.transaction_id,
            request_id=request_id,
            reason="POST_APPLY_VALIDATION_FAILED",
            transaction_store=transaction_store,
            mutation_lane_store=mutation_lane_store,
        )
        return "APPLIED_VALIDATION_FAILED"
    if behavior_status == "BEHAVIOR_VALIDATED_PASS":
        terminal = "COMPLETED_VALIDATED"
    elif behavior_risk_accepted:
        terminal = "COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED"
    else:
        _hold_recovery(
            transaction_id=result.transaction_id,
            request_id=request_id,
            reason="BEHAVIOR_EVIDENCE_INCOMPLETE",
            transaction_store=transaction_store,
            mutation_lane_store=mutation_lane_store,
        )
        return "RECOVERY_PENDING"
    transaction_store.transition_transaction(
        result.transaction_id,
        terminal,
        recovery_state="NONE",
        rollback_state="ROLLBACK_AVAILABLE",
    )
    mutation_lane_store.transition(request_id, "COMPLETED", reason=terminal)
    return terminal


def _execute_operation_sequence(
    *,
    transaction_id: str,
    mutation_request_id: str,
    target_file: str,
    source_hash_before: str,
    preview_root: str,
    operations: tuple[SourceMutationOperation, ...],
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
    failure_injection: str,
) -> JournaledApplyResult:
    written: list[str] = []
    try:
        for operation in operations:
            operation_id = f"{transaction_id}-op-{operation.sequence_no:04d}"
            state = _operation_state(transaction_store, transaction_id, operation_id)
            if state == "PENDING":
                transaction_store.record_operation_intent(operation_id)
                _inject_failure(failure_injection, "after_intent", operation.sequence_no)
                state = "INTENT_RECORDED"
            if state == "INTENT_RECORDED":
                current = current_file_hash(operation.destination_path)
                if current == operation.payload_hash:
                    transaction_store.record_operation_applied(operation_id)
                elif _precondition_still_holds(operation):
                    apply_source_mutation_operation(operation, operation_id=operation_id)
                    _inject_failure(failure_injection, "after_write", operation.sequence_no)
                    transaction_store.record_operation_applied(operation_id)
                else:
                    raise RuntimeError("RECOVERY_CONFLICT_AFTER_INTENT:" + operation.destination_path)
                _inject_failure(failure_injection, "after_applied", operation.sequence_no)
                state = "APPLIED"
            if state == "APPLIED":
                valid, reason = verify_source_mutation_operation(operation)
                if not valid:
                    raise RuntimeError(reason)
                transaction_store.record_operation_verified(operation_id)
                state = "VERIFIED"
            if state == "VERIFIED":
                valid, reason = verify_source_mutation_operation(operation)
                if not valid:
                    raise RuntimeError("VERIFIED_OPERATION_DRIFT:" + reason)
            if state != "VERIFIED":
                raise RuntimeError("UNEXPECTED_OPERATION_STATE:" + state)
            written.append(operation.destination_path)
        transaction_store.transition_transaction(transaction_id, "VALIDATING")
        request = mutation_lane_store.get_request(mutation_request_id)
        if request and request["state"] == "EXECUTING":
            mutation_lane_store.transition(mutation_request_id, "VALIDATING")
        result = build_applied_result(
            transaction_id=transaction_id,
            target_file=target_file,
            source_hash_before=source_hash_before,
            preview_root=preview_root,
            operations=operations,
            written=written,
            feature_id=JOURNALED_APPLY_EXECUTOR_FEATURE_ID,
            checked=checked_rules(),
        )
        transaction_store.store_artifact(transaction_id, _APPLY_RESULT_ARTIFACT, result.to_dict())
        write_execution_manifest(result, transaction_store)
        return result
    except BaseException as exc:
        if isinstance(exc, SystemExit):
            raise
        _hold_recovery(
            transaction_id=transaction_id,
            request_id=mutation_request_id,
            reason="JOURNALED_APPLY_INTERRUPTED:" + str(exc),
            transaction_store=transaction_store,
            mutation_lane_store=mutation_lane_store,
        )
        result = build_recovery_result(
            transaction_id=transaction_id,
            target_file=target_file,
            source_hash_before=source_hash_before,
            preview_root=preview_root,
            operations=operations,
            written=written,
            error=str(exc),
            transaction_store=transaction_store,
            feature_id=JOURNALED_APPLY_EXECUTOR_FEATURE_ID,
            checked=checked_rules(),
        )
        transaction_store.store_artifact(transaction_id, _APPLY_RESULT_ARTIFACT, result.to_dict())
        write_execution_manifest(result, transaction_store)
        return result


def _hold_recovery(
    *,
    transaction_id: str,
    request_id: str,
    reason: str,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
) -> None:
    transaction_store.transition_transaction(
        transaction_id,
        "RECOVERY_PENDING",
        recovery_state=reason,
        rollback_state="ROLLBACK_AVAILABLE",
    )
    request = mutation_lane_store.get_request(request_id)
    if request and request["state"] in {"RESERVED", "EXECUTING", "VALIDATING"}:
        mutation_lane_store.transition(request_id, "RECOVERY_PENDING", reason=reason)


def _store_authorization(
    transaction_id: str,
    authorization: JournaledApplyAuthorization,
    store: WorkbenchTransactionStore,
) -> None:
    digest = store.store_artifact(transaction_id, _APPLY_AUTH_ARTIFACT, authorization.to_dict())
    canonical = json.dumps(
        authorization.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    if digest != hashlib.sha256(canonical.encode("utf-8")).hexdigest():
        raise RuntimeError("AUTHORIZATION_ARTIFACT_HASH_MISMATCH")


def _operation_state(
    store: WorkbenchTransactionStore,
    transaction_id: str,
    operation_id: str,
) -> str:
    for item in store.list_operations(transaction_id):
        if item["operation_id"] == operation_id:
            return str(item["state"])
    raise KeyError("TRANSACTION_OPERATION_NOT_FOUND:" + operation_id)


def _precondition_still_holds(operation: SourceMutationOperation) -> bool:
    destination = Path(operation.destination_path)
    if operation.operation_type == "CREATE_FILE":
        return not destination.exists()
    return current_file_hash(destination) == operation.precondition_hash


def _inject_failure(spec: str, point: str, sequence_no: int) -> None:
    normalized = str(spec).strip().lower()
    if normalized == f"{point}:{sequence_no}":
        raise RuntimeError(f"INJECTED_FAILURE:{point}:{sequence_no}")
    if normalized == f"hard_exit_{point}:{sequence_no}":
        os._exit(97)


def _request_id_for(store: WorkbenchTransactionStore, transaction_id: str) -> str:
    record = store.get_transaction(transaction_id)
    if record is None:
        raise KeyError("WORKBENCH_TRANSACTION_NOT_FOUND")
    return str(record["mutation_request_id"])
