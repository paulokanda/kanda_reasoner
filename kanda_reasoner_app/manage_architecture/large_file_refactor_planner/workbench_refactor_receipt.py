# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_refactor_receipt.py
"""Machine-readable RefactorReceipt emitted from durable Workbench transaction truth."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION
from .workbench_transaction_store import WorkbenchTransactionStore

__all__ = [
    "REFACTOR_RECEIPT_FEATURE_ID",
    "RefactorReceipt",
    "build_and_write_refactor_receipt",
]

REFACTOR_RECEIPT_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-refactor-receipt-v1"
)
_RECEIPT_NAME = "REFACTOR_RECEIPT.json"


@dataclass(frozen=True)
class RefactorReceipt:
    """Read-only completion receipt derived from transaction and evidence stores."""

    schema_version: str
    feature_id: str
    transaction_id: str
    transaction_state: str
    recovery_state: str
    rollback_state: str
    contract_hash: str
    snapshot_hash: str
    baseline_hash: str
    project_root: str
    operations: tuple[dict[str, Any], ...]
    artifact_hashes: tuple[tuple[str, str], ...]
    before_hashes: tuple[tuple[str, str], ...]
    after_hashes: tuple[tuple[str, str], ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    receipt_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["operations"] = [dict(item) for item in self.operations]
        for key in ("artifact_hashes", "before_hashes", "after_hashes"):
            data[key] = [list(item) for item in getattr(self, key)]
        data["warnings"] = list(self.warnings)
        data["blockers"] = list(self.blockers)
        return data

    def integrity_valid(self) -> bool:
        return bool(self.receipt_hash and self.receipt_hash == _receipt_hash(self))


def build_and_write_refactor_receipt(
    *,
    transaction_id: str,
    transaction_store: WorkbenchTransactionStore,
) -> RefactorReceipt:
    """Build and persist a receipt only from durable transaction evidence."""
    tx = transaction_store.get_transaction(transaction_id)
    if tx is None:
        raise KeyError("WORKBENCH_TRANSACTION_NOT_FOUND")
    operations = tuple(transaction_store.list_operations(transaction_id))
    artifact_kinds = (
        "REFRACTOR_BASELINE",
        "EXECUTION_BASIS",
        "EXECUTION_CONTRACT",
        "MUTATION_REQUEST",
        "JOURNALED_APPLY_AUTHORIZATION",
        "JOURNALED_OPERATION_PLAN",
        "JOURNALED_APPLY_RESULT",
        "JOURNALED_ROLLBACK_RESULT",
    )
    artifact_hashes: list[tuple[str, str]] = []
    for kind in artifact_kinds:
        payload = transaction_store.load_artifact(transaction_id, kind)
        if payload is None:
            continue
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        artifact_hashes.append((kind, hashlib.sha256(canonical.encode("utf-8")).hexdigest()))
    before_hashes = tuple(
        sorted(
            (str(item["target_path"]), str(item["precondition_hash"]))
            for item in operations
        )
    )
    after_hashes = tuple(
        sorted(
            (str(item["target_path"]), str(item["payload_hash"]))
            for item in operations
        )
    )
    blockers = _receipt_blockers(str(tx["state"]), operations)
    warnings = _receipt_warnings(str(tx["state"]), str(tx["rollback_state"]))
    provisional = RefactorReceipt(
        schema_version=SCHEMA_VERSION,
        feature_id=REFACTOR_RECEIPT_FEATURE_ID,
        transaction_id=transaction_id,
        transaction_state=str(tx["state"]),
        recovery_state=str(tx["recovery_state"]),
        rollback_state=str(tx["rollback_state"]),
        contract_hash=str(tx["contract_hash"]),
        snapshot_hash=str(tx["snapshot_hash"]),
        baseline_hash=str(tx["baseline_hash"]),
        project_root=str(tx["project_root"]),
        operations=operations,
        artifact_hashes=tuple(sorted(artifact_hashes)),
        before_hashes=before_hashes,
        after_hashes=after_hashes,
        warnings=warnings,
        blockers=blockers,
        receipt_hash="",
    )
    receipt = RefactorReceipt(
        **{**provisional.__dict__, "receipt_hash": _receipt_hash(provisional)}
    )
    tx_root = Path(str(tx["transaction_root"])).resolve()
    path = tx_root / _RECEIPT_NAME
    path.write_text(json.dumps(receipt.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(path.read_text(encoding="utf-8"))
    reloaded = RefactorReceipt(
        **{
            **saved,
            "operations": tuple(saved["operations"]),
            "artifact_hashes": tuple(tuple(item) for item in saved["artifact_hashes"]),
            "before_hashes": tuple(tuple(item) for item in saved["before_hashes"]),
            "after_hashes": tuple(tuple(item) for item in saved["after_hashes"]),
            "warnings": tuple(saved["warnings"]),
            "blockers": tuple(saved["blockers"]),
        }
    )
    if not reloaded.integrity_valid():
        raise RuntimeError("REFACTOR_RECEIPT_HASH_MISMATCH")
    return receipt


def _receipt_blockers(
    state: str,
    operations: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    blockers: list[str] = []
    if state not in {
        "COMPLETED_VALIDATED",
        "COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED",
        "ROLLBACK_VERIFIED",
        "RECOVERY_PENDING",
    }:
        blockers.append("TRANSACTION_STATE_NOT_RECEIPT_READY:" + state)
    if not operations:
        blockers.append("TRANSACTION_OPERATION_EVIDENCE_MISSING")
    return tuple(sorted(set(blockers)))


def _receipt_warnings(state: str, rollback_state: str) -> tuple[str, ...]:
    warnings: list[str] = []
    if state == "COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED":
        warnings.append("COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED")
    if rollback_state == "ROLLBACK_CONFLICT":
        warnings.append("ROLLBACK_CONFLICT_REQUIRES_HUMAN_RECOVERY")
    if state == "RECOVERY_PENDING":
        warnings.append("PROJECT_MUTATION_LANE_MAY_REMAIN_CLOSED")
    return tuple(sorted(set(warnings)))


def _receipt_hash(receipt: RefactorReceipt) -> str:
    body = receipt.to_dict()
    body["receipt_hash"] = ""
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
