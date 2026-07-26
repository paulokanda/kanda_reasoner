# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_execution_feasibility.py
"""Initial Workbench execution-feasibility, fitness, and Compliance Veto contracts."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .models import RefactorPlan, SCHEMA_VERSION
from .module_size_policy import module_size_blockers
from .workbench_execution_basis import (
    WorkbenchExecutionBasisSet,
    execution_basis_is_fresh,
)

__all__ = [
    "WORKBENCH_EXECUTION_FEASIBILITY_FEATURE_ID",
    "WORKBENCH_ARCHITECTURE_CHARACTERISTICS",
    "FitnessFunctionResult",
    "ComplianceVeto",
    "WorkbenchExecutionFeasibilityResult",
    "evaluate_workbench_execution_feasibility",
]

WORKBENCH_EXECUTION_FEASIBILITY_FEATURE_ID = (
    "architecture-review-large-file-refactor-execution-feasibility-v1"
)

WORKBENCH_ARCHITECTURE_CHARACTERISTICS = {
    "SAFETY": "No unjournaled real source mutation is permitted.",
    "RECOVERABILITY": "Every nonterminal real-write transaction must recover or expose conflict.",
    "DETERMINISM": "The same approved basis and transformation version must yield the same payload.",
    "BEHAVIOR_PRESERVATION": "Available behavior evidence must not regress silently.",
    "CONTAINMENT": "Writes must remain inside explicitly authorized project-owned paths.",
    "API_COMPATIBILITY": "Approved public API ownership must remain preserved by default.",
    "OBSERVABILITY": "Every gate, blocker, mutation, and recovery state must emit evidence.",
    "GRANULARITY_COMPLIANCE": "Every resulting Python source file must have 101-499 physical lines.",
}


@dataclass(frozen=True)
class FitnessFunctionResult:
    """One executable architecture fitness result for the Workbench pipeline."""

    fitness_id: str
    status: str
    blockers: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready fitness result."""
        return asdict(self)


@dataclass(frozen=True)
class ComplianceVeto:
    """Structured evidence returned to Planner when execution is not feasible."""

    schema_version: str
    feature_id: str
    plan_status: str
    target_file: str
    plan_hash_hint: str
    reasons: list[str]
    affected_modules: list[str]
    evidence: dict[str, Any]
    planner_action_required: bool = True
    workbench_architecture_mutation_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready Compliance Veto dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class WorkbenchExecutionFeasibilityResult:
    """Initial executable verdict for one immutable Planner plan and basis set."""

    schema_version: str
    feature_id: str
    status: str
    verdict: str
    target_file: str
    architecture_characteristics: dict[str, str]
    fitness_results: list[FitnessFunctionResult]
    compliance_veto: ComplianceVeto | None
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready feasibility result."""
        data = asdict(self)
        data["fitness_results"] = [item.to_dict() for item in self.fitness_results]
        data["compliance_veto"] = self.compliance_veto.to_dict() if self.compliance_veto else None
        return data


def evaluate_workbench_execution_feasibility(
    *,
    plan: RefactorPlan | None,
    execution_basis: WorkbenchExecutionBasisSet | None,
) -> WorkbenchExecutionFeasibilityResult:
    """Evaluate initial Patch-1 fitness gates without redesigning architecture."""
    blockers: list[str] = []
    fitness: list[FitnessFunctionResult] = []

    planner_ownership = _planner_ownership_fitness(plan)
    fitness.append(planner_ownership)
    blockers.extend(planner_ownership.blockers)

    size_result = _module_size_projection_fitness(plan)
    fitness.append(size_result)
    blockers.extend(size_result.blockers)

    no_leak = _no_leak_fitness(execution_basis)
    fitness.append(no_leak)
    blockers.extend(no_leak.blockers)

    source_basis = _source_basis_fitness(execution_basis)
    fitness.append(source_basis)
    blockers.extend(source_basis.blockers)

    unique_blockers = sorted(set(blockers))
    verdict = "EXECUTABLE" if not unique_blockers else "PLAN_CORRECTION_REQUIRED"
    veto = _build_compliance_veto(plan, unique_blockers) if unique_blockers else None
    return WorkbenchExecutionFeasibilityResult(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_EXECUTION_FEASIBILITY_FEATURE_ID,
        status="execution_feasibility_ready" if not unique_blockers else "blocked",
        verdict=verdict,
        target_file=plan.target_file if plan else "",
        architecture_characteristics=dict(WORKBENCH_ARCHITECTURE_CHARACTERISTICS),
        fitness_results=fitness,
        compliance_veto=veto,
        checked_rules=_checked_rules(),
        blockers=unique_blockers,
        warnings=_warnings(),
    )


def _planner_ownership_fitness(plan: RefactorPlan | None) -> FitnessFunctionResult:
    """Prove the Workbench consumes one explicit plan rather than inventing one."""
    blockers: list[str] = []
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
    elif plan.status == "blocked":
        blockers.append("PLANNER_PLAN_BLOCKED")
    return FitnessFunctionResult(
        fitness_id="FF-PLANNER-WORKBENCH-ISOLATION",
        status="PASS" if not blockers else "FAIL",
        blockers=blockers,
        evidence={
            "workbench_architecture_mutation_allowed": False,
            "planner_plan_present": plan is not None,
        },
    )


def _module_size_projection_fitness(plan: RefactorPlan | None) -> FitnessFunctionResult:
    """Apply the strict 101-499 policy to every Planner-projected output module."""
    blockers: list[str] = []
    size_map: dict[str, int] = {}
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
    else:
        for module in plan.proposed_modules:
            count = int(module.estimated_lines)
            size_map[module.filename] = count
            blockers.extend(
                module_size_blockers(
                    count,
                    relative_path=module.filename,
                )
            )
        if not plan.proposed_modules:
            blockers.append("PLANNED_MODULE_SET_EMPTY")
    return FitnessFunctionResult(
        fitness_id="FF-MODULE-SIZE",
        status="PASS" if not blockers else "FAIL",
        blockers=sorted(set(blockers)),
        evidence={
            "projected_physical_lines": size_map,
            "rule": "100 < physical_lines < 500",
        },
    )


def _no_leak_fitness(
    basis: WorkbenchExecutionBasisSet | None,
) -> FitnessFunctionResult:
    """Use execution-basis ownership blockers as the initial No-Leak gate."""
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    if basis is None:
        blockers.append("EXECUTION_BASIS_MISSING")
    else:
        blockers.extend(basis.blockers)
        evidence = {
            "active_project_root": basis.active_project_root,
            "basis_file_count": len(basis.all_basis),
            "mutation_basis_count": len(basis.mutation_basis),
        }
    return FitnessFunctionResult(
        fitness_id="FF-NO-LEAK",
        status="PASS" if not blockers else "FAIL",
        blockers=sorted(set(blockers)),
        evidence=evidence,
    )


def _source_basis_fitness(
    basis: WorkbenchExecutionBasisSet | None,
) -> FitnessFunctionResult:
    """Recheck source basis freshness before later evidence is trusted."""
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    if basis is None:
        blockers.append("EXECUTION_BASIS_MISSING")
    else:
        fresh, freshness_blockers = execution_basis_is_fresh(basis)
        blockers.extend(freshness_blockers)
        evidence = {
            "fresh": fresh,
            "checked_paths": [item.path for item in basis.all_basis],
        }
    return FitnessFunctionResult(
        fitness_id="FF-SOURCE-BASIS",
        status="PASS" if not blockers else "FAIL",
        blockers=sorted(set(blockers)),
        evidence=evidence,
    )


def _build_compliance_veto(
    plan: RefactorPlan | None,
    blockers: list[str],
) -> ComplianceVeto:
    """Build evidence-only Planner correction feedback from deterministic blockers."""
    affected: list[str] = []
    for blocker in blockers:
        parts = blocker.split(":")
        if len(parts) >= 2 and parts[0] in {
            "MODULE_BELOW_MINIMUM",
            "MODULE_ABOVE_MAXIMUM",
        }:
            affected.append(parts[1])
    return ComplianceVeto(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_EXECUTION_FEASIBILITY_FEATURE_ID,
        plan_status=plan.status if plan else "missing",
        target_file=plan.target_file if plan else "",
        plan_hash_hint=plan.source_content_hash if plan else "",
        reasons=blockers,
        affected_modules=sorted(set(affected)),
        evidence={
            "planner_must_reconsider_architecture": True,
            "workbench_performed_symbol_reassignment": False,
            "workbench_performed_module_merge": False,
            "workbench_performed_module_split": False,
        },
        planner_action_required=True,
        workbench_architecture_mutation_allowed=False,
    )


def _checked_rules() -> list[str]:
    """Return stable Patch-1 feasibility rule labels."""
    return [
        "planner_owns_architecture",
        "workbench_does_not_merge_split_or_reassign_symbols",
        "every_projected_output_module_must_be_101_to_499_lines",
        "execution_basis_paths_must_remain_inside_active_project_root",
        "protected_support_roots_must_not_enter_execution_basis",
        "basis_hashes_must_remain_fresh",
        "failed_feasibility_returns_structured_compliance_veto",
    ]


def _warnings() -> list[str]:
    """Return stable warnings for the initial feasibility layer."""
    return [
        "PATCH_1_FEASIBILITY_IS_FOUNDATIONAL_NOT_FINAL_APPLY_AUTHORIZATION",
        "EXACT_PREVIEW_LINE_COUNTS_MUST_BE_RECHECKED_AFTER_TRANSFORMATION",
        "COMPLIANCE_VETO_IS_EVIDENCE_ONLY_AND_CANNOT_REDESIGN_THE_PLAN",
    ]
