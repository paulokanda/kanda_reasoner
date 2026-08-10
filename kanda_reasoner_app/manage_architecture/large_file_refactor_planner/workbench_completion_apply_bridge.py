# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_apply_bridge.py
"""Bridge Patch 4 human review state into the proven Patch 5 transaction executor."""
from __future__ import annotations

from .workbench_journaled_apply_models import (
    JournaledApplyResult,
    build_journaled_apply_authorization,
)
from dataclasses import dataclass
from typing import Any

from .workbench_behavior_validation import WorkbenchBehaviorValidationResult, run_workbench_behavior_validation
from .workbench_completion_workflow import CompletionEvidenceBundle, CompletionTransactionBundle
from .workbench_journaled_apply_executor import (
    execute_journaled_refactor_apply,
    finalize_journaled_refactor_transaction,
)
from .workbench_post_apply_validator import PostApplyValidationResult, validate_and_write_post_apply
from .workbench_refactor_receipt import RefactorReceipt, build_and_write_refactor_receipt
from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult
from .workbench_transaction_rollback import JournaledRollbackResult, rollback_journaled_refactor_transaction

__all__ = [
    "CompletionApplyOutcome",
    "execute_completion_transaction",
    "rollback_completion_transaction",
]


@dataclass(frozen=True)
class CompletionApplyOutcome:
    """Combined apply, validation, behavior, and terminal transaction evidence."""

    status: str
    apply_result: JournaledApplyResult
    post_apply: PostApplyValidationResult | None
    behavior: WorkbenchBehaviorValidationResult | None
    final_transaction_state: str
    receipt: RefactorReceipt | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "apply_result": self.apply_result.to_dict(),
            "post_apply": self.post_apply.to_dict() if self.post_apply else None,
            "behavior": self.behavior.to_dict() if self.behavior else None,
            "final_transaction_state": self.final_transaction_state,
            "receipt": self.receipt.to_dict() if self.receipt else None,
        }


def execute_completion_transaction(
    *,
    evidence: CompletionEvidenceBundle,
    transaction_bundle: CompletionTransactionBundle,
    preflight: WorkbenchPreflightBackupReadinessResult,
    source_payload: SourceApplyPayloadReadinessResult,
    executor_proof_available: bool,
    behavior_test_command: str = "",
    failure_injection: str = "",
) -> CompletionApplyOutcome:
    """Execute the exact reviewed transaction and finalize from live validation evidence."""
    if not transaction_bundle.gate.enabled:
        raise RuntimeError(
            "REFACTOR_LARGE_MODULE_GATE_BLOCKED:"
            + "|".join(transaction_bundle.gate.blockers)
        )
    authorization = build_journaled_apply_authorization(
        transaction_id=transaction_bundle.transaction.transaction_id,
        contract_hash=evidence.contract.contract_hash,
        payload_hash=evidence.sealed_payload.payload_hash,
        semantic_reviewed="SEMANTIC_DIFF_REVIEW_NOT_CONFIRMED" not in transaction_bundle.gate.blockers,
        warnings_acknowledged=transaction_bundle.warning_acknowledgment.complete,
        transaction_summary_confirmed=transaction_bundle.transaction_summary.confirmed,
        executor_proof_available=executor_proof_available,
    )
    apply_result = execute_journaled_refactor_apply(
        transaction=transaction_bundle.transaction,
        authorization=authorization,
        execution_basis=evidence.execution_basis,
        sealed_payload=evidence.sealed_payload,
        source_payload=source_payload,
        preflight_backup=preflight,
        transaction_store=transaction_bundle.transaction_store,
        mutation_lane_store=transaction_bundle.mutation_lane_store,
        failure_injection=failure_injection,
    )
    if apply_result.status != "applied":
        return CompletionApplyOutcome(
            status=apply_result.status,
            apply_result=apply_result,
            post_apply=None,
            behavior=None,
            final_transaction_state=apply_result.transaction_state,
            receipt=build_and_write_refactor_receipt(
                transaction_id=apply_result.transaction_id,
                transaction_store=transaction_bundle.transaction_store,
            ),
        )
    post_apply = validate_and_write_post_apply(
        apply_result=apply_result,
        source_payload=source_payload,
        active_project_root=evidence.contract.active_project_root,
    )
    behavior = run_workbench_behavior_validation(
        apply_result=apply_result,
        post_apply_validation=post_apply,
        source_payload=source_payload,
        active_project_root=evidence.contract.active_project_root,
        test_command=behavior_test_command,
    )
    final_state = finalize_journaled_refactor_transaction(
        result=apply_result,
        structural_pass=post_apply.status == "post_apply_validated",
        behavior_status=behavior.behavior_status,
        behavior_risk_accepted=(
            transaction_bundle.transaction_summary.confirmed
            and behavior.behavior_status == "BEHAVIOR_VALIDATION_NOT_RUN"
        ),
        transaction_store=transaction_bundle.transaction_store,
        mutation_lane_store=transaction_bundle.mutation_lane_store,
    )
    receipt = build_and_write_refactor_receipt(
        transaction_id=apply_result.transaction_id,
        transaction_store=transaction_bundle.transaction_store,
    )
    return CompletionApplyOutcome(
        status="completed" if final_state.startswith("COMPLETED_") else "recovery_pending",
        apply_result=apply_result,
        post_apply=post_apply,
        behavior=behavior,
        final_transaction_state=final_state,
        receipt=receipt,
    )


def rollback_completion_transaction(
    transaction_bundle: CompletionTransactionBundle,
) -> JournaledRollbackResult:
    """Rollback the current completion transaction through journaled recovery ownership."""
    return rollback_journaled_refactor_transaction(
        transaction_id=transaction_bundle.transaction.transaction_id,
        transaction_store=transaction_bundle.transaction_store,
        mutation_lane_store=transaction_bundle.mutation_lane_store,
    )


def format_completion_apply_outcome(outcome: CompletionApplyOutcome) -> str:
    """Render concise execution outcome for GUI projection only."""
    lines = [
        "Refactor Large Module Result",
        "============================",
        f"status: {outcome.status}",
        f"apply_status: {outcome.apply_result.status}",
        f"transaction_state: {outcome.final_transaction_state}",
        f"operations_verified: {outcome.apply_result.operations_verified}",
    ]
    if outcome.post_apply is not None:
        lines.append(f"post_apply: {outcome.post_apply.status}")
    if outcome.behavior is not None:
        lines.append(f"behavior: {outcome.behavior.behavior_status}")
    if outcome.apply_result.blockers:
        lines.extend(["", "Blockers:"])
        lines.extend(f"- {item}" for item in outcome.apply_result.blockers)
    return "\n".join(lines)
