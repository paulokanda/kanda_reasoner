# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_transaction_rollback.py
"""Hash-verified reverse rollback for journaled Workbench refactor transactions."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.engineering_safety.project_mutation_lane import ProjectMutationLaneStore

from .models import SCHEMA_VERSION
from .workbench_journaled_apply_support import load_persisted_operation_plan
from .workbench_source_mutation_primitives import (
    SourceMutationOperation,
    apply_source_mutation_operation,
    current_file_hash,
)
from .workbench_transaction_store import WorkbenchTransactionStore

__all__ = [
    "TRANSACTION_ROLLBACK_FEATURE_ID",
    "JournaledRollbackResult",
    "rollback_journaled_refactor_transaction",
]

TRANSACTION_ROLLBACK_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-patch5-transaction-rollback-v1"
)
_ROLLBACK_RESULT_ARTIFACT = "JOURNALED_ROLLBACK_RESULT"
_ROLLBACK_REPORT = "JOURNALED_ROLLBACK_EXECUTION.json"


@dataclass(frozen=True)
class JournaledRollbackResult:
    """Durable rollback outcome with exact restoration and conflict evidence."""

    schema_version: str
    feature_id: str
    status: str
    transaction_id: str
    transaction_state: str
    lane_state: str
    restored_files: tuple[str, ...] = field(default_factory=tuple)
    removed_files: tuple[str, ...] = field(default_factory=tuple)
    already_restored: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in ("restored_files", "removed_files", "already_restored", "blockers", "warnings"):
            data[key] = list(getattr(self, key))
        return data


def rollback_journaled_refactor_transaction(
    *,
    transaction_id: str,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
) -> JournaledRollbackResult:
    """Rollback verified/applied operations in reverse order or report conflict."""
    tx = transaction_store.get_transaction(transaction_id)
    if tx is None:
        raise KeyError("WORKBENCH_TRANSACTION_NOT_FOUND")
    request_id = str(tx["mutation_request_id"])
    request = mutation_lane_store.get_request(request_id)
    if request is None:
        raise RuntimeError("MUTATION_REQUEST_NOT_FOUND")
    if request["state"] not in {"EXECUTING", "VALIDATING", "RECOVERY_PENDING", "ROLLBACK_PENDING"}:
        raise RuntimeError("TRANSACTION_NOT_ROLLBACKABLE_FROM_LANE_STATE:" + str(request["state"]))
    if request["state"] != "ROLLBACK_PENDING":
        mutation_lane_store.transition(request_id, "ROLLBACK_PENDING", reason="ROLLBACK_REQUESTED")
    transaction_store.transition_transaction(
        transaction_id,
        "ROLLBACK_PENDING",
        recovery_state="ROLLBACK_IN_PROGRESS",
        rollback_state="ROLLBACK_IN_PROGRESS",
    )
    operations, _metadata = load_persisted_operation_plan(
        transaction_id=transaction_id,
        transaction_store=transaction_store,
    )
    rows = {item["sequence_no"]: item for item in transaction_store.list_operations(transaction_id)}
    conflicts = _detect_conflicts(operations, rows)
    if conflicts:
        return _conflict_result(
            transaction_id=transaction_id,
            request_id=request_id,
            conflicts=conflicts,
            transaction_store=transaction_store,
            mutation_lane_store=mutation_lane_store,
        )
    restored: list[str] = []
    removed: list[str] = []
    already: list[str] = []
    for operation in sorted(operations, key=lambda item: item.sequence_no, reverse=True):
        row = rows[operation.sequence_no]
        destination = Path(operation.destination_path).resolve()
        current = current_file_hash(destination)
        if operation.operation_type == "CREATE_FILE":
            if not destination.exists():
                already.append(str(destination))
                continue
            destination.unlink()
            if destination.exists():
                raise RuntimeError("ROLLBACK_CREATE_DELETE_FAILED:" + str(destination))
            removed.append(str(destination))
            continue
        backup_path = Path(str(row["backup_path"])).resolve()
        if current == operation.precondition_hash:
            already.append(str(destination))
            continue
        restore_operation = SourceMutationOperation(
            schema_version=operation.schema_version,
            feature_id=operation.feature_id,
            sequence_no=operation.sequence_no,
            operation_type="REPLACE_FILE",
            relative_path=operation.relative_path,
            payload_path=str(backup_path),
            destination_path=str(destination),
            payload_hash=operation.precondition_hash,
            precondition_hash=operation.payload_hash,
            destination_existed=True,
            byte_size=backup_path.stat().st_size,
        )
        apply_source_mutation_operation(
            restore_operation,
            operation_id=f"{transaction_id}-rollback-{operation.sequence_no:04d}",
        )
        if current_file_hash(destination) != operation.precondition_hash:
            raise RuntimeError("ROLLBACK_RESTORE_HASH_MISMATCH:" + str(destination))
        restored.append(str(destination))
    final_blockers = _verify_original_state(operations)
    if final_blockers:
        return _conflict_result(
            transaction_id=transaction_id,
            request_id=request_id,
            conflicts=final_blockers,
            transaction_store=transaction_store,
            mutation_lane_store=mutation_lane_store,
            restored=restored,
            removed=removed,
            already=already,
        )
    transaction_store.transition_transaction(
        transaction_id,
        "ROLLBACK_VERIFIED",
        recovery_state="NONE",
        rollback_state="ROLLBACK_VERIFIED",
    )
    mutation_lane_store.transition(request_id, "ROLLED_BACK", reason="ROLLBACK_VERIFIED")
    result = JournaledRollbackResult(
        schema_version=SCHEMA_VERSION,
        feature_id=TRANSACTION_ROLLBACK_FEATURE_ID,
        status="rollback_verified",
        transaction_id=transaction_id,
        transaction_state="ROLLBACK_VERIFIED",
        lane_state="ROLLED_BACK",
        restored_files=tuple(sorted(restored)),
        removed_files=tuple(sorted(removed)),
        already_restored=tuple(sorted(already)),
        blockers=(),
        warnings=(),
    )
    _persist_result(result, transaction_store)
    return result


def _detect_conflicts(
    operations: tuple[SourceMutationOperation, ...],
    rows: dict[int, dict[str, Any]],
) -> list[str]:
    """Return external-drift or backup-integrity conflicts before rollback writes."""
    conflicts: list[str] = []
    for operation in operations:
        destination = Path(operation.destination_path).resolve()
        current = current_file_hash(destination)
        allowed = {operation.payload_hash, operation.precondition_hash}
        if operation.operation_type == "CREATE_FILE":
            allowed.add("")
        if current not in allowed:
            conflicts.append("ROLLBACK_CONFLICT_EXTERNAL_DRIFT:" + str(destination))
        if operation.operation_type == "REPLACE_FILE":
            backup = Path(str(rows[operation.sequence_no]["backup_path"])).resolve()
            if not backup.is_file():
                conflicts.append("ROLLBACK_BACKUP_MISSING:" + str(destination))
            elif current_file_hash(backup) != operation.precondition_hash:
                conflicts.append("ROLLBACK_BACKUP_HASH_MISMATCH:" + str(destination))
    return sorted(set(conflicts))


def _verify_original_state(operations: tuple[SourceMutationOperation, ...]) -> list[str]:
    blockers: list[str] = []
    for operation in operations:
        destination = Path(operation.destination_path).resolve()
        if operation.operation_type == "CREATE_FILE":
            if destination.exists():
                blockers.append("ROLLBACK_CREATED_FILE_STILL_PRESENT:" + str(destination))
        elif current_file_hash(destination) != operation.precondition_hash:
            blockers.append("ROLLBACK_ORIGINAL_HASH_NOT_RESTORED:" + str(destination))
    return blockers


def _conflict_result(
    *,
    transaction_id: str,
    request_id: str,
    conflicts: list[str],
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
    restored: list[str] | None = None,
    removed: list[str] | None = None,
    already: list[str] | None = None,
) -> JournaledRollbackResult:
    transaction_store.transition_transaction(
        transaction_id,
        "RECOVERY_PENDING",
        recovery_state="ROLLBACK_CONFLICT",
        rollback_state="ROLLBACK_CONFLICT",
    )
    request = mutation_lane_store.get_request(request_id)
    if request and request["state"] == "ROLLBACK_PENDING":
        mutation_lane_store.transition(request_id, "RECOVERY_PENDING", reason="ROLLBACK_CONFLICT")
    result = JournaledRollbackResult(
        schema_version=SCHEMA_VERSION,
        feature_id=TRANSACTION_ROLLBACK_FEATURE_ID,
        status="rollback_conflict",
        transaction_id=transaction_id,
        transaction_state="RECOVERY_PENDING",
        lane_state="RECOVERY_PENDING",
        restored_files=tuple(sorted(restored or [])),
        removed_files=tuple(sorted(removed or [])),
        already_restored=tuple(sorted(already or [])),
        blockers=tuple(sorted(set(conflicts))),
        warnings=("PROJECT_MUTATION_LANE_REMAINS_CLOSED",),
    )
    _persist_result(result, transaction_store)
    return result


def _persist_result(
    result: JournaledRollbackResult,
    store: WorkbenchTransactionStore,
) -> None:
    store.store_artifact(result.transaction_id, _ROLLBACK_RESULT_ARTIFACT, result.to_dict())
    tx = store.get_transaction(result.transaction_id)
    if tx is None:
        raise RuntimeError("WORKBENCH_TRANSACTION_NOT_FOUND")
    path = Path(str(tx["transaction_root"])) / _ROLLBACK_REPORT
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
