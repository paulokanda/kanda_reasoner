# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_refactor_transaction.py
"""Canonical no-write Workbench transaction preparation and recovery ownership."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import uuid
from pathlib import Path
from typing import Any

from kanda_reasoner_app.engineering_safety.project_mutation_lane import (
    ProjectMutationLaneStore,
    build_mutation_request,
    physical_project_id as resolve_physical_project_id,
)

from .models import SCHEMA_VERSION
from .workbench_execution_basis import (
    WorkbenchExecutionBasisSet,
    execution_basis_is_fresh,
)
from .workbench_execution_contract import WorkbenchExecutionContract
from .workbench_plan_snapshot import WorkbenchPlanSnapshot, write_workbench_plan_snapshot
from .workbench_refactor_baseline import RefactorBaseline
from .workbench_transaction_store import WorkbenchTransactionStore

__all__ = [
    "WORKBENCH_REFACTOR_TRANSACTION_FEATURE_ID",
    "WorkbenchRefactorTransaction",
    "prepare_workbench_refactor_transaction",
    "reserve_workbench_project_lane",
    "mark_workbench_transaction_recovery_pending",
    "discover_workbench_recovery_pending",
    "detect_self_hosted_refactor",
]

WORKBENCH_REFACTOR_TRANSACTION_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-refactor-transaction-v1"
)
_OWNER_BOX = "large_file_refactor_workbench"
_OPERATION_FAMILY = "LARGE_MODULE_REFACTOR"


def _utc_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass(frozen=True)
class WorkbenchRefactorTransaction:
    """Prepared transaction identity before any real source mutation is authorized."""

    schema_version: str
    feature_id: str
    transaction_id: str
    contract_hash: str
    snapshot_hash: str
    baseline_hash: str
    execution_basis_hash: str
    project_root: str
    physical_project_id: str
    durable_transaction_root: str
    mutation_request_id: str
    lane_state: str
    transaction_state: str
    source_mutation_enabled: bool = False
    apply_authorized: bool = False
    self_hosted_refactor: bool = False
    blockers: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data


def prepare_workbench_refactor_transaction(
    *,
    snapshot: WorkbenchPlanSnapshot,
    baseline: RefactorBaseline,
    execution_basis: WorkbenchExecutionBasisSet,
    contract: WorkbenchExecutionContract,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
    tool_root: str | Path | None = None,
) -> WorkbenchRefactorTransaction:
    """Persist transaction evidence and queue a data-only mutation request."""
    blockers = _preparation_blockers(snapshot, baseline, execution_basis, contract)
    project_root = Path(contract.active_project_root).resolve()
    project_id = resolve_physical_project_id(project_root)
    self_hosted = detect_self_hosted_refactor(project_root, tool_root)
    transaction_id = _transaction_id(contract.contract_hash)
    request_id = transaction_id + "-mutation-request"
    if blockers:
        return _blocked_transaction(
            transaction_id=transaction_id,
            contract=contract,
            baseline=baseline,
            execution_basis=execution_basis,
            project_root=project_root,
            project_id=project_id,
            request_id=request_id,
            blockers=blockers,
            self_hosted=self_hosted,
        )

    request = build_mutation_request(
        request_id=request_id,
        project_root=project_root,
        owner_box=_OWNER_BOX,
        operation_family=_OPERATION_FAMILY,
        transaction_id=transaction_id,
        mutation_paths=contract.exact_target_files,
        basis_paths=[item.path for item in execution_basis.all_basis],
    )
    tx_root = transaction_store.create_transaction(
        transaction_id=transaction_id,
        contract_hash=contract.contract_hash,
        snapshot_hash=snapshot.snapshot_hash,
        baseline_hash=baseline.baseline_hash,
        physical_project_id=project_id,
        project_root=str(project_root),
        owner_box=_OWNER_BOX,
        mutation_request_id=request_id,
    )
    write_workbench_plan_snapshot(snapshot, tx_root / "planner_snapshot.json")
    transaction_store.store_artifact(transaction_id, "REFRACTOR_BASELINE", baseline.to_dict())
    transaction_store.store_artifact(transaction_id, "EXECUTION_BASIS", execution_basis.to_dict())
    transaction_store.store_artifact(transaction_id, "EXECUTION_CONTRACT", contract.to_dict())
    transaction_store.store_artifact(transaction_id, "MUTATION_REQUEST", request.to_dict())
    lane_port = mutation_lane_store.port(_OWNER_BOX)
    try:
        lane_port.submit(request)
    except Exception:
        transaction_store.transition_transaction(
            transaction_id,
            "RECOVERY_PENDING",
            recovery_state="MUTATION_REQUEST_QUEUE_SUBMISSION_FAILED",
        )
        raise
    transaction = WorkbenchRefactorTransaction(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_REFACTOR_TRANSACTION_FEATURE_ID,
        transaction_id=transaction_id,
        contract_hash=contract.contract_hash,
        snapshot_hash=snapshot.snapshot_hash,
        baseline_hash=baseline.baseline_hash,
        execution_basis_hash=contract.execution_basis_hash,
        project_root=str(project_root),
        physical_project_id=project_id,
        durable_transaction_root=str(tx_root),
        mutation_request_id=request_id,
        lane_state="QUEUED",
        transaction_state="PREPARED",
        source_mutation_enabled=False,
        apply_authorized=False,
        self_hosted_refactor=self_hosted,
        blockers=(),
        warnings=tuple(
            [
                "PATCH_2_TRANSACTION_PREPARES_DURABLE_STATE_BUT_DOES_NOT_APPLY_SOURCE",
                "REAL_MUTATION_REQUIRES_LATER_PAYLOAD_SHADOW_REVIEW_AND_AUTHORIZATION_GATES",
            ]
            + (["SELF_HOSTED_REFACTOR_REQUIRES_OUT_OF_PROCESS_VALIDATION"] if self_hosted else [])
        ),
    )
    transaction_store.store_artifact(transaction_id, "TRANSACTION_PREPARED", transaction.to_dict())
    return transaction


def reserve_workbench_project_lane(
    *,
    transaction: WorkbenchRefactorTransaction,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
    tool_root: str | Path | None = None,
) -> WorkbenchRefactorTransaction:
    """Reserve the serial project lane for the oldest queued mutation request."""
    if transaction.blockers:
        return transaction
    reserved = mutation_lane_store.reserve_next(transaction.physical_project_id)
    if reserved is None:
        raise RuntimeError("PROJECT_MUTATION_LANE_NOT_AVAILABLE")
    if reserved["request_id"] != transaction.mutation_request_id:
        raise RuntimeError("PROJECT_MUTATION_LANE_RESERVED_BY_EARLIER_REQUEST")
    transaction_store.transition_transaction(transaction.transaction_id, "LANE_RESERVED")
    return WorkbenchRefactorTransaction(
        **{
            **transaction.__dict__,
            "lane_state": "RESERVED",
            "transaction_state": "LANE_RESERVED",
        }
    )


def mark_workbench_transaction_recovery_pending(
    *,
    transaction: WorkbenchRefactorTransaction,
    reason: str,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
    tool_root: str | Path | None = None,
) -> WorkbenchRefactorTransaction:
    """Keep the project lane closed while an interrupted transaction needs recovery."""
    mutation_lane_store.transition(
        transaction.mutation_request_id,
        "RECOVERY_PENDING",
        reason=reason,
    )
    transaction_store.transition_transaction(
        transaction.transaction_id,
        "RECOVERY_PENDING",
        recovery_state="RECOVERY_PENDING",
    )
    return WorkbenchRefactorTransaction(
        **{
            **transaction.__dict__,
            "lane_state": "RECOVERY_PENDING",
            "transaction_state": "RECOVERY_PENDING",
        }
    )


def discover_workbench_recovery_pending(
    *,
    project_root: str | Path,
    transaction_store: WorkbenchTransactionStore,
    mutation_lane_store: ProjectMutationLaneStore,
) -> dict[str, Any]:
    """Return durable restart evidence from transaction and mutation-lane stores."""
    root = Path(project_root).resolve()
    project_id = resolve_physical_project_id(root)
    return {
        "schema_version": SCHEMA_VERSION,
        "feature_id": WORKBENCH_REFACTOR_TRANSACTION_FEATURE_ID,
        "project_root": str(root),
        "physical_project_id": project_id,
        "transactions": transaction_store.discover_recovery_pending(project_root=root),
        "lane_recovery_requests": mutation_lane_store.recovery_pending(project_id),
        "active_lane": mutation_lane_store.active_owner(project_id),
    }



def detect_self_hosted_refactor(
    project_root: str | Path,
    tool_root: str | Path | None,
) -> bool:
    """Return whether KANDA is preparing a transaction against its own source root."""
    if tool_root is None or not str(tool_root).strip():
        return False
    return Path(project_root).resolve() == Path(tool_root).resolve()

def _preparation_blockers(
    snapshot: WorkbenchPlanSnapshot,
    baseline: RefactorBaseline,
    execution_basis: WorkbenchExecutionBasisSet,
    contract: WorkbenchExecutionContract,
) -> list[str]:
    blockers: list[str] = []
    if not snapshot.integrity_valid():
        blockers.append("WORKBENCH_SNAPSHOT_HASH_MISMATCH")
    if not baseline.integrity_valid():
        blockers.append("REFACTOR_BASELINE_HASH_MISMATCH")
    if not contract.integrity_valid():
        blockers.append("EXECUTION_CONTRACT_HASH_MISMATCH")
    if contract.feasibility_verdict != "EXECUTABLE":
        blockers.append("EXECUTION_CONTRACT_NOT_EXECUTABLE")
    if contract.blocking_reasons:
        blockers.extend(contract.blocking_reasons)
    if baseline.snapshot_hash != snapshot.snapshot_hash:
        blockers.append("BASELINE_SNAPSHOT_HASH_MISMATCH")
    if contract.snapshot_hash != snapshot.snapshot_hash:
        blockers.append("CONTRACT_SNAPSHOT_HASH_MISMATCH")
    if contract.baseline_hash != baseline.baseline_hash:
        blockers.append("CONTRACT_BASELINE_HASH_MISMATCH")
    if execution_basis.status != "execution_basis_ready":
        blockers.append("EXECUTION_BASIS_NOT_READY")
    fresh, freshness_blockers = execution_basis_is_fresh(execution_basis)
    if not fresh:
        blockers.append("STALE_AFTER_EXTERNAL_SOURCE_MUTATION")
        blockers.extend(freshness_blockers)
    return sorted(set(blockers))


def _blocked_transaction(
    *,
    transaction_id: str,
    contract: WorkbenchExecutionContract,
    baseline: RefactorBaseline,
    execution_basis: WorkbenchExecutionBasisSet,
    project_root: Path,
    project_id: str,
    request_id: str,
    blockers: list[str],
    self_hosted: bool,
) -> WorkbenchRefactorTransaction:
    return WorkbenchRefactorTransaction(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_REFACTOR_TRANSACTION_FEATURE_ID,
        transaction_id=transaction_id,
        contract_hash=contract.contract_hash,
        snapshot_hash=contract.snapshot_hash,
        baseline_hash=baseline.baseline_hash,
        execution_basis_hash=contract.execution_basis_hash,
        project_root=str(project_root),
        physical_project_id=project_id,
        durable_transaction_root="",
        mutation_request_id=request_id,
        lane_state="NOT_QUEUED",
        transaction_state="BLOCKED",
        source_mutation_enabled=False,
        apply_authorized=False,
        self_hosted_refactor=self_hosted,
        blockers=tuple(sorted(set(blockers))),
        warnings=("BLOCKED_TRANSACTION_CREATED_NO_DURABLE_SOURCE_MUTATION_STATE",),
    )


def _transaction_id(contract_hash: str) -> str:
    stamp = _utc_compact()
    nonce = uuid.uuid4().hex[:12]
    digest = hashlib.sha256(f"{contract_hash}|{stamp}|{nonce}".encode("utf-8")).hexdigest()[:12]
    return f"tx-{stamp}-{digest}"
