# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_plan_review.py
"""Public Local AI plan-review facade backed by deterministic candidate tournament."""
from __future__ import annotations

from .models import ModuleAnalysisReport, RefactorPlan
from .planner_local_ai_review_models import PlanAIReviewResult
from .planner_local_ai_tournament import review_plan_with_local_ai_tournament

__all__ = ["review_and_correct_plan_with_local_ai"]


def review_and_correct_plan_with_local_ai(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    *,
    enabled: bool = True,
    model_selection: str = "",
    max_rounds: int = 4,
) -> PlanAIReviewResult:
    """Generate AI alternatives and let deterministic KANDA scoring select the winner."""
    return review_plan_with_local_ai_tournament(
        report,
        plan,
        enabled=enabled,
        model_selection=model_selection,
        max_rounds=max_rounds,
    )
