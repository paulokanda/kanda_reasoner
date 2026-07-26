# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui_progression.py
"""Pure fail-closed progression model for the Workbench GUI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = [
    "WorkbenchGuiProgression",
    "build_workbench_gui_progression",
    "preview_validation_guidance",
]


@dataclass(frozen=True)
class WorkbenchGuiProgression:
    """Read-only projection of which sequential Workbench actions are available."""

    plan_loaded: bool
    dependency_analysis_enabled: bool
    dependency_ready: bool
    real_preview_enabled: bool
    real_preview_ready: bool
    structural_validation_enabled: bool
    structural_validation_ready: bool
    advanced_quality_review_enabled: bool
    advanced_quality_review_ready: bool
    preflight_enabled: bool
    preflight_ready: bool
    source_payload_enabled: bool
    source_payload_ready: bool
    completion_evidence_enabled: bool
    completion_evidence_ready: bool
    transaction_summary_enabled: bool
    human_review_enabled: bool
    transaction_confirmation_enabled: bool
    refactor_large_module_enabled: bool
    journaled_rollback_enabled: bool
    current_stage: str
    next_action: str


def build_workbench_gui_progression(
    *,
    intake: Any = None,
    dependency_readiness: Any = None,
    preview: Any = None,
    structural_validation: Any = None,
    advanced_quality_review: Any = None,
    preflight: Any = None,
    source_payload: Any = None,
    completion_evidence: Any = None,
    completion_transaction: Any = None,
    completion_outcome: Any = None,
) -> WorkbenchGuiProgression:
    """Return deterministic GUI availability from durable/public evidence only."""
    plan_loaded = _is_ready_intake(intake)
    dependency_ready = _is_ready_dependency(dependency_readiness)
    preview_ready = _is_ready_preview(preview)
    structural_ready = _is_ready_structural(structural_validation)
    advanced_quality_review_ready = _is_ready_advanced_quality_review(advanced_quality_review)
    preflight_ready = _status(preflight) == "preflight_backup_ready"
    payload_ready = _status(source_payload) == "source_apply_payload_ready"
    evidence_ready = completion_evidence is not None
    transaction_ready = completion_transaction is not None
    final_enabled = bool(
        transaction_ready
        and getattr(getattr(completion_transaction, "gate", None), "enabled", False)
    )
    rollback_enabled = _status(completion_outcome) in {
        "RECOVERY_PENDING",
        "APPLIED_VALIDATION_FAILED",
    } or getattr(completion_outcome, "final_transaction_state", "") in {
        "RECOVERY_PENDING",
        "APPLIED_VALIDATION_FAILED",
    }
    current_stage, next_action = _stage_and_next_action(
        plan_loaded=plan_loaded,
        dependency_ready=dependency_ready,
        preview_ready=preview_ready,
        structural_ready=structural_ready,
        advanced_quality_review_ready=advanced_quality_review_ready,
        preflight_ready=preflight_ready,
        payload_ready=payload_ready,
        evidence_ready=evidence_ready,
        transaction_ready=transaction_ready,
        final_enabled=final_enabled,
    )
    return WorkbenchGuiProgression(
        plan_loaded=plan_loaded,
        dependency_analysis_enabled=plan_loaded,
        dependency_ready=dependency_ready,
        real_preview_enabled=dependency_ready,
        real_preview_ready=preview_ready,
        structural_validation_enabled=preview_ready,
        structural_validation_ready=structural_ready,
        advanced_quality_review_enabled=structural_ready,
        advanced_quality_review_ready=advanced_quality_review_ready,
        preflight_enabled=advanced_quality_review_ready,
        preflight_ready=preflight_ready,
        source_payload_enabled=preflight_ready,
        source_payload_ready=payload_ready,
        completion_evidence_enabled=payload_ready,
        completion_evidence_ready=evidence_ready,
        transaction_summary_enabled=evidence_ready,
        human_review_enabled=evidence_ready,
        transaction_confirmation_enabled=transaction_ready,
        refactor_large_module_enabled=final_enabled,
        journaled_rollback_enabled=rollback_enabled,
        current_stage=current_stage,
        next_action=next_action,
    )


def preview_validation_guidance(preview: Any) -> str:
    """Explain why Structural Validation is available or blocked after Preview."""
    if preview is None:
        return (
            "Generate Real Preview first. Structural Validation becomes available "
            "only after the Preview result is successfully written."
        )
    if _is_ready_preview(preview):
        return (
            "Real Preview is ready. Click Validate Real Preview to run Structural "
            "Validation. Active project source is still unchanged."
        )
    blockers = tuple(getattr(preview, "blockers", ()) or ())
    lines = [
        "Structural Validation is unavailable because Generate Real Preview did not "
        "produce a successful real_preview_written result.",
        f"Preview status: {_status(preview) or '<missing>'}",
        "Blockers:",
    ]
    lines.extend(f"- {item}" for item in blockers)
    if not blockers:
        lines.append("- PREVIEW_RESULT_NOT_READY")
    lines.append("Resolve the Preview blocker, then run Generate Real Preview again.")
    return "\n".join(lines)


def _is_ready_intake(value: Any) -> bool:
    return bool(
        value
        and _status(value) == "plan_intake_ready"
        and getattr(value, "ready_for_real_preview", False)
        and getattr(value, "source_hash_fresh", False)
    )


def _is_ready_dependency(value: Any) -> bool:
    return bool(
        value
        and _status(value) == "dependency_readiness_ready"
        and getattr(value, "ready_for_real_preview_writer", False)
    )


def _is_ready_preview(value: Any) -> bool:
    return bool(
        value
        and _status(value) == "real_preview_written"
        and getattr(value, "files", None)
        and getattr(value, "written_files", None)
        and not getattr(value, "blockers", ())
    )


def _is_ready_structural(value: Any) -> bool:
    return bool(
        value
        and _status(value).startswith("passed")
        and getattr(value, "structural_status", "") != "STRUCTURAL_FAIL"
        and not getattr(value, "blockers", ())
    )


def _is_ready_advanced_quality_review(value: Any) -> bool:
    """Return whether fresh AQR evidence may open Preflight."""
    if value is None:
        return False
    report = getattr(value, "cross_check_report", None)
    decision = str(getattr(getattr(report, "quality_decision", None), "value", "") or "")
    execution = str(getattr(getattr(value, "run_record", None), "execution_status", "") or "")
    if hasattr(getattr(value, "run_record", None), "execution_status"):
        execution_value = getattr(value.run_record.execution_status, "value", value.run_record.execution_status)
        execution = str(execution_value or "")
    return decision in {"PASS", "PASS_WITH_WARNINGS"} and execution == "SUCCEEDED"


def _status(value: Any) -> str:
    return str(getattr(value, "status", "") or "")


def _stage_and_next_action(
    *,
    plan_loaded: bool,
    dependency_ready: bool,
    preview_ready: bool,
    structural_ready: bool,
    advanced_quality_review_ready: bool,
    preflight_ready: bool,
    payload_ready: bool,
    evidence_ready: bool,
    transaction_ready: bool,
    final_enabled: bool,
) -> tuple[str, str]:
    ordered = (
        (not plan_loaded, "PLAN_INTAKE", "Load Latest Planner Plan"),
        (not dependency_ready, "DEPENDENCY_READINESS", "Analyze Dependency Readiness"),
        (not preview_ready, "REAL_PREVIEW", "Generate Real Preview"),
        (not structural_ready, "STRUCTURAL_VALIDATION", "Validate Real Preview"),
        (not advanced_quality_review_ready, "ADVANCED_QUALITY_REVIEW", "Run Advanced Quality Review"),
        (not preflight_ready, "PREFLIGHT_BACKUP", "Prepare Preflight Backup Readiness"),
        (not payload_ready, "SOURCE_PAYLOAD", "Build Source Apply Payload"),
        (not evidence_ready, "COMPLETION_EVIDENCE", "Prepare Completion Evidence"),
        (not transaction_ready, "HUMAN_REVIEW", "Review diffs and Prepare Transaction Summary"),
        (not final_enabled, "TRANSACTION_CONFIRMATION", "Confirm review and transaction summary"),
    )
    for condition, stage, action in ordered:
        if condition:
            return stage, action
    return "READY_TO_REFACTOR", "Refactor Large Module"
