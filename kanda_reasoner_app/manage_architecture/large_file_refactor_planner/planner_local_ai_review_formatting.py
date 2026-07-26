"""Formatting for optional local-AI split-plan review results."""
from __future__ import annotations

from .planner_local_ai_plan_review import PlanAIReviewResult

__all__ = ["format_plan_ai_review_result"]


def format_plan_ai_review_result(result: PlanAIReviewResult) -> str:
    """Return readable Planner text for one optional local-AI review result."""
    lines = [
        "LOCAL AI PLAN REVIEW",
        "Status: " + result.status,
        "Model: " + (result.model_name or "none - heuristic fallback"),
        "Rounds: " + str(result.rounds),
        "Final plan status: " + result.plan.status,
        "Fallback used: " + ("yes" if result.fallback_used else "no"),
        "Rationale: " + (result.rationale or "No rationale returned."),
    ]
    if result.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    return "\n".join(lines)
