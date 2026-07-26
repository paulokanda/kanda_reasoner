# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_tournament.py
"""Multi-candidate Local AI architecture tournament with deterministic selection."""
from __future__ import annotations

from dataclasses import replace

from .models import ModuleAnalysisReport, RefactorPlan
from .planner_local_ai_candidate_scoring import LocalAICandidateScore, score_local_ai_candidate
from .planner_local_ai_review_models import PlanAIReviewResult
from .planner_local_ai_staged_protocol import review_plan_with_staged_local_ai

__all__ = ["review_plan_with_local_ai_tournament"]

_MINIMUM_IMPROVEMENT = 0.005
_STRATEGIES = (
    (
        "candidate_a",
        "conservative_minimal_change",
        "Prefer the smallest safe bounded change. Preserve the current partition unless one clear correction improves quality.",
    ),
    (
        "candidate_b",
        "responsibility_cohesion",
        "Prioritize responsibility cohesion. Separate clear outlier responsibilities using only bounded known-symbol moves or safe merges.",
    ),
    (
        "candidate_c",
        "topology_boundary_safety",
        "Prioritize dependency topology and boundary safety. Reduce avoidable helper coupling or facade back-reference pressure without cycles.",
    ),
)


def review_plan_with_local_ai_tournament(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    *,
    enabled: bool = True,
    model_selection: str = "",
    max_rounds: int = 4,
) -> PlanAIReviewResult:
    """Generate bounded alternatives, score them, and let KANDA select the winner."""
    baseline_helper_count = len([m for m in plan.proposed_modules if m.role != "public_facade"])
    baseline_score = score_local_ai_candidate(
        report,
        plan,
        candidate_id="baseline_control",
        strategy="deterministic_heuristic",
        baseline_helper_count=baseline_helper_count,
        corrections_applied=0,
    )
    candidate_results: list[tuple[PlanAIReviewResult, LocalAICandidateScore]] = []
    evidence: list[dict[str, object]] = [baseline_score.to_dict()]

    for candidate_id, strategy, strategy_instruction in _STRATEGIES:
        result = review_plan_with_staged_local_ai(
            report,
            plan,
            enabled=enabled,
            model_selection=model_selection,
            max_rounds=max_rounds,
            candidate_strategy=strategy,
            strategy_instruction=strategy_instruction,
            force_exploration=True,
        )
        score = score_local_ai_candidate(
            report,
            result.plan,
            candidate_id=candidate_id,
            strategy=strategy,
            baseline_helper_count=baseline_helper_count,
            corrections_applied=result.corrections_applied,
        )
        record = score.to_dict()
        record["review_status"] = result.status
        record["review_rationale"] = result.rationale
        record["stage_evidence"] = [list(item) for item in result.stage_evidence]
        evidence.append(record)
        candidate_results.append((result, score))

    exploration_actions = sum(result.corrections_applied for result, _score in candidate_results)
    valid = [item for item in candidate_results if item[1].status == "valid"]
    ranked = sorted(
        valid,
        key=lambda item: (
            item[1].total_score,
            -item[1].corrections_applied,
            item[1].candidate_id,
        ),
        reverse=True,
    )
    if ranked and ranked[0][1].total_score >= baseline_score.total_score + _MINIMUM_IMPROVEMENT:
        selected_result, selected_score = ranked[0]
        selection_reason = (
            "KANDA selected " + selected_score.candidate_id
            + " because its deterministic score " + f"{selected_score.total_score:.6f}"
            + " exceeded baseline " + f"{baseline_score.total_score:.6f}" + "."
        )
        return replace(
            selected_result,
            selected_candidate_id=selected_score.candidate_id,
            baseline_candidate_score=baseline_score.total_score,
            selected_candidate_score=selected_score.total_score,
            tournament_evidence=tuple(evidence),
            tournament_selection_reason=selection_reason,
            stage_evidence=selected_result.stage_evidence + (("candidate_tournament", "selected_by_kanda"),),
            tournament_candidate_actions_accepted=exploration_actions,
        )

    warnings = tuple(
        ["No validated Local AI candidate exceeded the deterministic baseline score."]
        + [warning for result, _score in candidate_results for warning in result.warnings]
    )
    return PlanAIReviewResult(
        status="validated_no_improvement" if baseline_score.status == "valid" else "review_incomplete",
        plan=plan,
        model_name=next((result.model_name for result, _score in candidate_results if result.model_name), ""),
        rounds=sum(result.rounds for result, _score in candidate_results),
        rationale="KANDA preserved the deterministic baseline because no valid AI candidate improved its score.",
        warnings=warnings,
        fallback_used=baseline_score.status != "valid",
        corrections_applied=0,
        stage_evidence=(("candidate_tournament", "baseline_preserved"),),
        selected_candidate_id="baseline_control",
        baseline_candidate_score=baseline_score.total_score,
        selected_candidate_score=baseline_score.total_score,
        tournament_evidence=tuple(evidence),
        tournament_selection_reason="No valid AI candidate cleared the minimum deterministic improvement threshold.",
        tournament_candidate_actions_accepted=exploration_actions,
    )
