# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_workflow.py
"""No-write completion workflow assembling Patch 1-3 evidence for Patch 4 GUI review."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from kanda_reasoner_app.engineering_safety.project_mutation_lane import ProjectMutationLaneStore

from .workbench_project_support_paths import shadow_runs_root
from .workbench_completion_review import (
    RefactorLargeModuleGate,
    SemanticDiffReview,
    TransactionSummary,
    WarningAcknowledgment,
    build_semantic_diff_review,
    build_text_diff_review,
    build_transaction_summary,
    build_warning_acknowledgment,
    evaluate_refactor_large_module_gate,
)
from .workbench_dynamic_python_risks import DynamicPythonRiskReport, analyze_dynamic_python_risks
from .workbench_execution_basis import WorkbenchExecutionBasisSet, build_workbench_execution_basis_set
from .workbench_execution_contract import WorkbenchExecutionContract, build_workbench_execution_contract
from .workbench_execution_feasibility import WorkbenchExecutionFeasibilityResult, evaluate_workbench_execution_feasibility
from .workbench_plan_snapshot import WorkbenchPlanSnapshot
from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult
from .workbench_refactor_baseline import BehaviorBaselineEvidence, RefactorBaseline, build_refactor_baseline
from .workbench_refactor_transaction import WorkbenchRefactorTransaction, prepare_workbench_refactor_transaction
from .workbench_sealed_payload import WorkbenchSealedPayload, build_and_write_sealed_payload
from .workbench_shadow_backend import ShadowMaterializationResult, choose_shadow_backend
from .workbench_shadow_provenance import ShadowProvenanceResult, prove_shadow_runtime_provenance
from .workbench_shadow_validation import ShadowValidationResult, validate_shadow_refactor
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult
from .workbench_transaction_store import (
    WorkbenchTransactionStore,
    migrate_legacy_workbench_transaction_state,
)
from .workbench_transformation_recipe import TransformationRecipe, build_transformation_recipe
from .cst_real_preview_writer import RealPreviewWriteResult
from .visual_diff_ui import VisualDiffReport

__all__ = [
    "CompletionEvidenceBundle",
    "CompletionTransactionBundle",
    "prepare_completion_evidence",
    "prepare_completion_transaction",
    "refresh_completion_review_state",
]


@dataclass(frozen=True)
class CompletionEvidenceBundle:
    """All immutable/no-write evidence needed before transaction preparation."""

    execution_basis: WorkbenchExecutionBasisSet
    feasibility: WorkbenchExecutionFeasibilityResult
    baseline: RefactorBaseline
    contract: WorkbenchExecutionContract
    dynamic_risks: DynamicPythonRiskReport
    recipe: TransformationRecipe
    sealed_payload: WorkbenchSealedPayload
    shadow_materialization: ShadowMaterializationResult
    provenance: ShadowProvenanceResult
    shadow_validation: ShadowValidationResult
    semantic_review: SemanticDiffReview
    text_diff: VisualDiffReport


@dataclass(frozen=True)
class CompletionTransactionBundle:
    """Prepared durable transaction plus human summary and fail-closed button gate."""

    transaction_store: WorkbenchTransactionStore
    mutation_lane_store: ProjectMutationLaneStore
    transaction: WorkbenchRefactorTransaction
    warning_acknowledgment: WarningAcknowledgment
    transaction_summary: TransactionSummary
    gate: RefactorLargeModuleGate


def prepare_completion_evidence(
    *,
    snapshot: WorkbenchPlanSnapshot,
    preview: RealPreviewWriteResult,
    preflight: WorkbenchPreflightBackupReadinessResult,
    source_payload: SourceApplyPayloadReadinessResult,
    active_project_root: str | Path,
    behavior_baseline: BehaviorBaselineEvidence | None = None,
    validation_basis_paths: Iterable[str | Path] = (),
    shadow_root: str | Path | None = None,
) -> CompletionEvidenceBundle:
    """Build Patch 4 review evidence by composing frozen Patch 1-3 public APIs."""
    root = Path(active_project_root).resolve()
    plan = snapshot.materialize_plan()
    basis = build_workbench_execution_basis_set(
        plan=plan,
        active_project_root=str(root),
        api_basis_paths=[plan.target_file],
        dependency_basis_paths=[plan.target_file],
        validation_basis_paths=validation_basis_paths,
    )
    feasibility = evaluate_workbench_execution_feasibility(
        plan=plan,
        execution_basis=basis,
    )
    baseline = build_refactor_baseline(
        snapshot=snapshot,
        execution_basis=basis,
        behavior_baseline=behavior_baseline,
    )
    contract = build_workbench_execution_contract(
        snapshot=snapshot,
        baseline=baseline,
        execution_basis=basis,
        feasibility=feasibility,
    )
    risks = analyze_dynamic_python_risks(plan.target_file)
    recipe = build_transformation_recipe(
        snapshot=snapshot,
        contract=contract,
        dynamic_risks=risks,
    )
    sealed = build_and_write_sealed_payload(
        contract=contract,
        recipe=recipe,
        preview=preview,
        source_payload=source_payload,
    )
    backend, eligibility = choose_shadow_backend(root)
    chosen_shadow_root = Path(shadow_root).resolve() if shadow_root else _default_shadow_root(root, contract)
    materialization = backend.materialize(
        project_root=root,
        shadow_root=chosen_shadow_root,
        sealed_payload=sealed,
    )
    module_names = _module_names_for_contract(root, contract)
    provenance = prove_shadow_runtime_provenance(
        materialization=materialization,
        module_names=module_names,
    )
    shadow_validation = validate_shadow_refactor(
        contract=contract,
        baseline=baseline,
        sealed_payload=sealed,
        materialization=materialization,
        provenance=provenance,
        dynamic_risks=risks,
    )
    semantic_review = build_semantic_diff_review(
        baseline=baseline,
        contract=contract,
        sealed_payload=sealed,
        shadow_validation=shadow_validation,
        reviewed=False,
    )
    text_diff = build_text_diff_review(
        contract=contract,
        sealed_payload=sealed,
    )
    _require_completion_evidence(
        basis=basis,
        feasibility=feasibility,
        contract=contract,
        recipe=recipe,
        materialization=materialization,
        provenance=provenance,
        shadow_validation=shadow_validation,
        backend_eligible=eligibility.eligible,
        preflight=preflight,
    )
    return CompletionEvidenceBundle(
        execution_basis=basis,
        feasibility=feasibility,
        baseline=baseline,
        contract=contract,
        dynamic_risks=risks,
        recipe=recipe,
        sealed_payload=sealed,
        shadow_materialization=materialization,
        provenance=provenance,
        shadow_validation=shadow_validation,
        semantic_review=semantic_review,
        text_diff=text_diff,
    )


def prepare_completion_transaction(
    *,
    snapshot: WorkbenchPlanSnapshot,
    evidence: CompletionEvidenceBundle,
    preflight: WorkbenchPreflightBackupReadinessResult,
    source_payload: SourceApplyPayloadReadinessResult,
    acknowledged_warning_codes: Iterable[str] = (),
    semantic_review_confirmed: bool = False,
    transaction_summary_confirmed: bool = False,
    tool_root: str | Path | None = None,
    transaction_apply_executor_proven: bool = False,
) -> CompletionTransactionBundle:
    """Prepare durable transaction state and compute a no-write final button gate."""
    root = Path(evidence.contract.active_project_root).resolve()
    transaction_root = migrate_legacy_workbench_transaction_state(root)
    transaction_store = WorkbenchTransactionStore(transaction_root)
    lane_store = ProjectMutationLaneStore(
        transaction_root.parent / "project_mutation_lane.sqlite3"
    )
    transaction = prepare_workbench_refactor_transaction(
        snapshot=snapshot,
        baseline=evidence.baseline,
        execution_basis=evidence.execution_basis,
        contract=evidence.contract,
        transaction_store=transaction_store,
        mutation_lane_store=lane_store,
        tool_root=tool_root,
    )
    review = build_semantic_diff_review(
        baseline=evidence.baseline,
        contract=evidence.contract,
        sealed_payload=evidence.sealed_payload,
        shadow_validation=evidence.shadow_validation,
        reviewed=semantic_review_confirmed,
    )
    acknowledgment = build_warning_acknowledgment(
        review.warnings,
        acknowledged_warning_codes,
    )
    summary = build_transaction_summary(
        transaction=transaction,
        contract=evidence.contract,
        sealed_payload=evidence.sealed_payload,
        shadow_validation=evidence.shadow_validation,
        preflight=preflight,
        confirmed=transaction_summary_confirmed,
    )
    gate = evaluate_refactor_large_module_gate(
        execution_basis=evidence.execution_basis,
        contract=evidence.contract,
        sealed_payload=evidence.sealed_payload,
        shadow_validation=evidence.shadow_validation,
        preflight=preflight,
        source_payload=source_payload,
        semantic_review=review,
        warning_acknowledgment=acknowledgment,
        transaction_summary=summary,
        transaction=transaction,
        transaction_apply_executor_proven=transaction_apply_executor_proven,
    )
    return CompletionTransactionBundle(
        transaction_store=transaction_store,
        mutation_lane_store=lane_store,
        transaction=transaction,
        warning_acknowledgment=acknowledgment,
        transaction_summary=summary,
        gate=gate,
    )


def refresh_completion_review_state(
    *,
    snapshot: WorkbenchPlanSnapshot,
    evidence: CompletionEvidenceBundle,
    transaction_bundle: CompletionTransactionBundle,
    preflight: WorkbenchPreflightBackupReadinessResult,
    source_payload: SourceApplyPayloadReadinessResult,
    semantic_review_confirmed: bool,
    acknowledged_warning_codes: Iterable[str],
    transaction_summary_confirmed: bool,
    transaction_apply_executor_proven: bool = False,
) -> CompletionTransactionBundle:
    """Recompute human-review state without creating another durable transaction."""
    review = build_semantic_diff_review(
        baseline=evidence.baseline,
        contract=evidence.contract,
        sealed_payload=evidence.sealed_payload,
        shadow_validation=evidence.shadow_validation,
        reviewed=semantic_review_confirmed,
    )
    acknowledgment = build_warning_acknowledgment(
        review.warnings,
        acknowledged_warning_codes,
    )
    summary = build_transaction_summary(
        transaction=transaction_bundle.transaction,
        contract=evidence.contract,
        sealed_payload=evidence.sealed_payload,
        shadow_validation=evidence.shadow_validation,
        preflight=preflight,
        confirmed=transaction_summary_confirmed,
    )
    gate = evaluate_refactor_large_module_gate(
        execution_basis=evidence.execution_basis,
        contract=evidence.contract,
        sealed_payload=evidence.sealed_payload,
        shadow_validation=evidence.shadow_validation,
        preflight=preflight,
        source_payload=source_payload,
        semantic_review=review,
        warning_acknowledgment=acknowledgment,
        transaction_summary=summary,
        transaction=transaction_bundle.transaction,
        transaction_apply_executor_proven=transaction_apply_executor_proven,
    )
    return CompletionTransactionBundle(
        transaction_store=transaction_bundle.transaction_store,
        mutation_lane_store=transaction_bundle.mutation_lane_store,
        transaction=transaction_bundle.transaction,
        warning_acknowledgment=acknowledgment,
        transaction_summary=summary,
        gate=gate,
    )


def _default_shadow_root(root: Path, contract: WorkbenchExecutionContract) -> Path:
    """Return governed sibling daily-work Shadow location outside active source."""
    return shadow_runs_root(root) / contract.contract_id


def _module_names_for_contract(
    project_root: Path,
    contract: WorkbenchExecutionContract,
) -> tuple[str, ...]:
    """Derive importable dotted module names from exact contract targets."""
    names: list[str] = []
    for raw in contract.exact_target_files:
        path = Path(raw).resolve()
        try:
            relative = path.relative_to(project_root)
        except ValueError:
            continue
        if path.suffix != ".py":
            continue
        parts = list(relative.with_suffix("").parts)
        if parts and parts[-1] == "__init__":
            parts.pop()
        if parts:
            names.append(".".join(parts))
    return tuple(sorted(set(names), key=str.casefold))


def _require_completion_evidence(
    *,
    basis: WorkbenchExecutionBasisSet,
    feasibility: WorkbenchExecutionFeasibilityResult,
    contract: WorkbenchExecutionContract,
    recipe: TransformationRecipe,
    materialization: ShadowMaterializationResult,
    provenance: ShadowProvenanceResult,
    shadow_validation: ShadowValidationResult,
    backend_eligible: bool,
    preflight: WorkbenchPreflightBackupReadinessResult,
) -> None:
    """Raise explicit fail-closed reasons for incomplete Patch 4 preparation."""
    blockers: list[str] = []
    if basis.status != "execution_basis_ready":
        blockers.extend(basis.blockers or ["EXECUTION_BASIS_NOT_READY"])
    if feasibility.verdict != "EXECUTABLE":
        blockers.extend(feasibility.blockers or ["EXECUTION_FEASIBILITY_NOT_EXECUTABLE"])
    if contract.feasibility_verdict != "EXECUTABLE":
        blockers.extend(contract.blocking_reasons or ["EXECUTION_CONTRACT_NOT_EXECUTABLE"])
    if recipe.blockers:
        blockers.extend(recipe.blockers)
    if not backend_eligible:
        blockers.append("NO_ELIGIBLE_SHADOW_BACKEND")
    if materialization.status != "shadow_materialized":
        blockers.extend(materialization.blockers or ["SHADOW_NOT_MATERIALIZED"])
    if provenance.status != "shadow_provenance_pass":
        blockers.extend(provenance.blockers or ["SHADOW_PROVENANCE_NOT_PROVEN"])
    if shadow_validation.status != "shadow_validation_pass":
        blockers.extend(shadow_validation.blockers or ["SHADOW_VALIDATION_NOT_PASS"])
    if preflight.status != "preflight_backup_ready":
        blockers.extend(preflight.blockers or ["PREFLIGHT_BACKUP_NOT_READY"])
    if blockers:
        raise RuntimeError("PATCH4_COMPLETION_EVIDENCE_BLOCKED:" + "|".join(sorted(set(blockers))))
