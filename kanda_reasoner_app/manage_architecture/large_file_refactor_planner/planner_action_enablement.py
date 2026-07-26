"""Pure action-enablement rules for the Large File Refactor Planner GUI."""
from __future__ import annotations

from dataclasses import dataclass

__all__ = ["PlannerActionEnablement", "build_planner_action_enablement"]


@dataclass(frozen=True)
class PlannerActionEnablement:
    """Describe which Planner actions are currently available."""

    generate_split_plan: bool
    generate_docstring_plan: bool
    run_llm_arbitration: bool
    generate_preview: bool
    validate_preview: bool
    create_patch: bool
    prepare_apply_gate: bool


def build_planner_action_enablement(
    *,
    has_analysis: bool,
    has_plan: bool,
    plan_status: str,
    has_preview: bool,
    validation_passed: bool,
    payload_status: str,
    ai_review_running: bool = False,
    has_docstring_plan: bool = False,
    ai_correctable_plan: bool = False,
) -> PlannerActionEnablement:
    """Return prerequisite-based action states without depending on Qt widgets."""
    plan_blocked = has_plan and plan_status == "blocked"
    return PlannerActionEnablement(
        generate_split_plan=has_analysis and not ai_review_running,
        generate_docstring_plan=has_plan and not ai_review_running,
        run_llm_arbitration=has_plan and not ai_review_running,
        generate_preview=has_plan and not plan_blocked and not ai_review_running,
        validate_preview=has_preview,
        create_patch=validation_passed,
        prepare_apply_gate=payload_status == "payload_ready",
    )
