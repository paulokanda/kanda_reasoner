# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_comprehensive_review.py
"""Single explicit local-AI stage for split, ambiguity, and docstring review."""

from __future__ import annotations

from dataclasses import dataclass

from .models import DocstringProposal, ModuleAnalysisReport, RefactorPlan
from .planner_bounded_refinement import attach_docstring_proposals_to_plan
from .planner_local_ai_docstring_review import (
    DocstringAIReviewResult,
    review_docstring_proposals_with_local_ai,
)
from .planner_local_ai_plan_review import (
    PlanAIReviewResult,
    review_and_correct_plan_with_local_ai,
)

__all__ = [
    "ComprehensiveLocalAIReviewResult",
    "review_and_refine_planning_with_local_ai",
]


@dataclass(frozen=True)
class ComprehensiveLocalAIReviewResult:
    """Combined bounded result for the Planner explicit local-AI stage."""

    status: str
    plan: RefactorPlan
    docstring_proposals: tuple[DocstringProposal, ...]
    split_review: PlanAIReviewResult
    docstring_review: DocstringAIReviewResult
    warnings: tuple[str, ...] = ()


def review_and_refine_planning_with_local_ai(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
) -> ComprehensiveLocalAIReviewResult:
    """Run split/ambiguity review then low-confidence docstring review."""

    split = review_and_correct_plan_with_local_ai(
        report,
        plan,
        enabled=True,
    )
    docs = review_docstring_proposals_with_local_ai(
        report,
        proposals,
    )
    status = _combined_status(split, docs)
    warnings = tuple(split.warnings) + tuple(docs.warnings)
    final_plan = attach_docstring_proposals_to_plan(
        split.plan, list(docs.proposals)
    )
    return ComprehensiveLocalAIReviewResult(
        status=status,
        plan=final_plan,
        docstring_proposals=docs.proposals,
        split_review=split,
        docstring_review=docs,
        warnings=warnings,
    )


def _combined_status(
    split: PlanAIReviewResult,
    docs: DocstringAIReviewResult,
) -> str:
    if split.plan.status == "blocked":
        return "blocked"
    statuses = {split.status, docs.status}
    if "failed_fallback" in statuses:
        return "review_partial"
    if statuses == {"skipped_unavailable"}:
        return "skipped_unavailable"
    if "review_incomplete" in statuses or "review_partial" in statuses:
        return "review_partial"
    if split.status == "corrected" or docs.status == "refined":
        return "refined_and_revalidated"
    if split.status == "validated" and docs.status in {
        "validated_no_changes",
        "refined",
    }:
        return "validated"
    if "skipped_unavailable" in statuses:
        return "review_partial"
    return "validated"
