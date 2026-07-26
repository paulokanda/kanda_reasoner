# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_review_models.py
"""Data contracts for staged local-AI architecture review."""
from __future__ import annotations

from dataclasses import dataclass

from .models import RefactorPlan

__all__ = ["PlanAIReviewResult"]


@dataclass(frozen=True)
class PlanAIReviewResult:
    """Outcome of staged bounded local-AI architectural review."""

    status: str
    plan: RefactorPlan
    model_name: str = ""
    rounds: int = 0
    rationale: str = ""
    warnings: tuple[str, ...] = ()
    fallback_used: bool = False
    architecture_answers: tuple[tuple[str, str], ...] = ()
    corrections_applied: int = 0
    stage_evidence: tuple[tuple[str, str], ...] = ()
    selected_candidate_id: str = ""
    baseline_candidate_score: float = 0.0
    selected_candidate_score: float = 0.0
    tournament_evidence: tuple[dict[str, object], ...] = ()
    tournament_selection_reason: str = ""
    tournament_candidate_actions_accepted: int = 0
