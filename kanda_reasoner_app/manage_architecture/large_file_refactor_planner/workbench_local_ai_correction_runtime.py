"""Bounded Local AI correction runtime for Workbench recovery lanes."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .ast_analysis import analyze_python_file
from .planner_bounded_refinement import attach_docstring_proposals_to_plan
from .planner_local_ai_staged_protocol import review_plan_with_staged_local_ai
from .workbench_local_ai_correction_models import (
    LocalAIWorkbenchCorrectionCandidate,
)
from .workbench_correction_candidate_guard import plans_materially_different
from .workbench_stage_correction_context import WorkbenchStageCorrectionContext

__all__ = ["build_bounded_local_ai_workbench_correction_candidate"]

ProgressCallback = Callable[[str], None]
InterruptionCheck = Callable[[], None]


def build_bounded_local_ai_workbench_correction_candidate(
    *,
    plan: Any,
    proposals: list[Any],
    context: WorkbenchStageCorrectionContext,
    progress_callback: ProgressCallback | None = None,
    interruption_check: InterruptionCheck | None = None,
) -> LocalAIWorkbenchCorrectionCandidate:
    """Build one bounded single-track Local AI correction candidate."""
    if plan is None or not context.target_file:
        return LocalAIWorkbenchCorrectionCandidate(
            False,
            "Local AI correction blocked: Workbench plan or target file is missing.",
        )

    progress = progress_callback or (lambda _phase: None)
    interrupt = interruption_check or (lambda: None)

    try:
        interrupt()
        progress("ANALYZE_SOURCE")
        report = analyze_python_file(context.target_file)

        interrupt()
        progress("BOUNDED_LOCAL_AI_STAGED_REVIEW")
        result = review_plan_with_staged_local_ai(
            report,
            plan,
            enabled=True,
            max_rounds=2,
            strategy_instruction=context.prompt_text(),
            force_exploration=True,
            progress_callback=progress,
            interruption_check=interrupt,
            include_naming_review=False,
            include_final_audit=False,
        )

        interrupt()
        progress("VALIDATE_CORRECTED_PLAN")
        corrected_plan = attach_docstring_proposals_to_plan(
            result.plan,
            proposals,
        )
    except Exception as exc:
        return LocalAIWorkbenchCorrectionCandidate(
            False,
            "Local AI correction failed without bypassing the gate: " + str(exc),
        )

    if str(getattr(corrected_plan, "status", "")) != "planned":
        return LocalAIWorkbenchCorrectionCandidate(
            False,
            "Local AI correction returned a non-planned candidate; current Workbench evidence remains unchanged.",
            report=report,
            corrected_plan=corrected_plan,
            proposals=tuple(proposals),
            review_status=str(getattr(result, "status", "")),
            corrections_applied=int(getattr(result, "corrections_applied", 0) or 0),
            model_name=str(getattr(result, "model_name", "")),
        )

    action_count = int(getattr(result, "corrections_applied", 0) or 0)
    if action_count <= 0 or not plans_materially_different(plan, result.plan):
        return LocalAIWorkbenchCorrectionCandidate(
            False,
            "Local AI correction produced no material plan change. The current AQR blocker remains active and all correction routes remain reusable.",
            report=report,
            corrected_plan=corrected_plan,
            proposals=tuple(proposals),
            review_status=str(getattr(result, "status", "")),
            corrections_applied=action_count,
            model_name=str(getattr(result, "model_name", "")),
        )

    progress("CANDIDATE_READY")
    return LocalAIWorkbenchCorrectionCandidate(
        True,
        "Local AI returned a materially changed bounded correction candidate.",
        report=report,
        corrected_plan=corrected_plan,
        proposals=tuple(proposals),
        review_status=str(getattr(result, "status", "")),
        corrections_applied=int(getattr(result, "corrections_applied", 0) or 0),
        model_name=str(getattr(result, "model_name", "")),
    )
