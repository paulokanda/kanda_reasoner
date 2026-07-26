# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_execution_contract.py
"""Canonical executable contract between PlannerSnapshot and physical transaction state."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION
from .workbench_execution_basis import WorkbenchExecutionBasisSet, execution_basis_is_fresh
from .workbench_execution_feasibility import WorkbenchExecutionFeasibilityResult
from .workbench_plan_snapshot import WorkbenchPlanSnapshot
from .workbench_refactor_baseline import RefactorBaseline

__all__ = [
    "WORKBENCH_EXECUTION_CONTRACT_FEATURE_ID",
    "WorkbenchExecutionContract",
    "build_workbench_execution_contract",
    "execution_contract_integrity_valid",
]

WORKBENCH_EXECUTION_CONTRACT_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-execution-contract-v1"
)


@dataclass(frozen=True)
class WorkbenchExecutionContract:
    """Exact no-write contract describing what may later be physically executed."""

    schema_version: str
    feature_id: str
    contract_id: str
    snapshot_hash: str
    baseline_hash: str
    execution_basis_hash: str
    active_project_root: str
    target_file: str
    exact_target_files: tuple[str, ...]
    final_size_map: dict[str, int]
    symbol_movement_map: dict[str, str]
    import_synthesis_plan: dict[str, list[str]]
    public_api_preservation_map: dict[str, Any]
    consumer_rewrite_plan: dict[str, Any]
    runtime_validation_targets: tuple[str, ...]
    test_targets: tuple[str, ...]
    feasibility_verdict: str
    blocking_reasons: tuple[str, ...]
    contract_hash: str
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["exact_target_files"] = list(self.exact_target_files)
        data["runtime_validation_targets"] = list(self.runtime_validation_targets)
        data["test_targets"] = list(self.test_targets)
        data["blocking_reasons"] = list(self.blocking_reasons)
        data["warnings"] = list(self.warnings)
        return data

    def integrity_valid(self) -> bool:
        return execution_contract_integrity_valid(self)


def build_workbench_execution_contract(
    *,
    snapshot: WorkbenchPlanSnapshot,
    baseline: RefactorBaseline,
    execution_basis: WorkbenchExecutionBasisSet,
    feasibility: WorkbenchExecutionFeasibilityResult,
) -> WorkbenchExecutionContract:
    """Build one immutable execution contract without enabling source mutation."""
    blockers: list[str] = []
    if not snapshot.integrity_valid():
        blockers.append("WORKBENCH_SNAPSHOT_HASH_MISMATCH")
    if not baseline.integrity_valid():
        blockers.append("REFACTOR_BASELINE_HASH_MISMATCH")
    if baseline.snapshot_hash != snapshot.snapshot_hash:
        blockers.append("BASELINE_SNAPSHOT_HASH_MISMATCH")
    fresh, freshness_blockers = execution_basis_is_fresh(execution_basis)
    if not fresh:
        blockers.extend(freshness_blockers)
    if execution_basis.status != "execution_basis_ready":
        blockers.append("EXECUTION_BASIS_NOT_READY")
    if feasibility.verdict != "EXECUTABLE":
        blockers.append("EXECUTION_FEASIBILITY_NOT_EXECUTABLE")
        blockers.extend(feasibility.blockers)

    plan = snapshot.materialize_plan()
    basis_hash = _canonical_hash(execution_basis.to_dict())
    if basis_hash != baseline.execution_basis_hash:
        blockers.append("BASELINE_EXECUTION_BASIS_HASH_MISMATCH")

    exact_targets = tuple(
        sorted(
            {str(Path(item.path).resolve()) for item in execution_basis.mutation_basis},
            key=str.casefold,
        )
    )
    final_size_map = {
        str((Path(plan.target_file).resolve().parent / module.filename).resolve()): int(module.estimated_lines)
        for module in plan.proposed_modules
    }
    symbol_movement_map = _symbol_movement_map(plan)
    import_synthesis_plan = {
        module.filename: list(module.imports)
        for module in plan.proposed_modules
    }
    api_map = {
        "before": list(plan.public_api_before),
        "expected_after": list(plan.public_api_after_expected),
        "baseline_manifest": dict(baseline.public_api_manifest),
        "preservation_required": True,
    }
    consumer_plan = dict(plan.import_migration)
    runtime_targets = tuple(sorted(exact_targets, key=str.casefold))
    test_targets = tuple(sorted(baseline.related_tests, key=str.casefold))
    unique_blockers = tuple(sorted(set(blockers)))
    contract_id = "contract-" + hashlib.sha256(
        f"{snapshot.snapshot_hash}|{baseline.baseline_hash}|{basis_hash}".encode("utf-8")
    ).hexdigest()[:20]
    provisional = WorkbenchExecutionContract(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_EXECUTION_CONTRACT_FEATURE_ID,
        contract_id=contract_id,
        snapshot_hash=snapshot.snapshot_hash,
        baseline_hash=baseline.baseline_hash,
        execution_basis_hash=basis_hash,
        active_project_root=execution_basis.active_project_root,
        target_file=plan.target_file,
        exact_target_files=exact_targets,
        final_size_map=final_size_map,
        symbol_movement_map=symbol_movement_map,
        import_synthesis_plan=import_synthesis_plan,
        public_api_preservation_map=api_map,
        consumer_rewrite_plan=consumer_plan,
        runtime_validation_targets=runtime_targets,
        test_targets=test_targets,
        feasibility_verdict="EXECUTABLE" if not unique_blockers else "BLOCKED",
        blocking_reasons=unique_blockers,
        contract_hash="",
        warnings=(
            "EXECUTION_CONTRACT_IS_NO_WRITE_EVIDENCE_ONLY",
            "REAL_SOURCE_MUTATION_REQUIRES_LATER_TRANSACTION_AUTHORIZATION",
        ),
    )
    return WorkbenchExecutionContract(
        **{
            **provisional.__dict__,
            "contract_hash": _contract_hash(provisional),
        }
    )


def execution_contract_integrity_valid(contract: WorkbenchExecutionContract) -> bool:
    return bool(contract.contract_hash) and contract.contract_hash == _contract_hash(contract)


def _symbol_movement_map(plan: object) -> dict[str, str]:
    movement: dict[str, str] = {}
    for module in getattr(plan, "proposed_modules", []):
        for symbol in getattr(module, "symbols", []):
            name = str(symbol)
            if name in movement and movement[name] != module.filename:
                raise ValueError("SYMBOL_ASSIGNED_TO_MULTIPLE_MODULES:" + name)
            movement[name] = module.filename
    return dict(sorted(movement.items()))


def _contract_hash(contract: WorkbenchExecutionContract) -> str:
    payload = {
        "schema_version": contract.schema_version,
        "feature_id": contract.feature_id,
        "contract_id": contract.contract_id,
        "snapshot_hash": contract.snapshot_hash,
        "baseline_hash": contract.baseline_hash,
        "execution_basis_hash": contract.execution_basis_hash,
        "active_project_root": contract.active_project_root,
        "target_file": contract.target_file,
        "exact_target_files": list(contract.exact_target_files),
        "final_size_map": contract.final_size_map,
        "symbol_movement_map": contract.symbol_movement_map,
        "import_synthesis_plan": contract.import_synthesis_plan,
        "public_api_preservation_map": contract.public_api_preservation_map,
        "consumer_rewrite_plan": contract.consumer_rewrite_plan,
        "runtime_validation_targets": list(contract.runtime_validation_targets),
        "test_targets": list(contract.test_targets),
        "feasibility_verdict": contract.feasibility_verdict,
        "blocking_reasons": list(contract.blocking_reasons),
        "warnings": list(contract.warnings),
    }
    return _canonical_hash(payload)


def _canonical_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
