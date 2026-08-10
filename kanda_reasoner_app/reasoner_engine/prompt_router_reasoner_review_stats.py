# project-path: kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_review_stats.py
"""Statistics and pilot-readiness metrics for Prompt Router Reasoner reviews."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping, Sequence

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_models import (
    AGREEMENT_AGREE,
    AGREEMENT_DISAGREE,
    LABEL_BOTH_ACCEPTABLE_UNCLEAR,
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    STATUS_REVIEWED,
)


@dataclass(frozen=True)
class PilotReadinessThresholds:
    """Conservative thresholds for automatic ML pilot activation.

    The defaults intentionally use lower confidence bounds and minimum
    evidence counts rather than raw accuracy. They are local project policy,
    based on risk-management guidance that validates the human-AI workflow and
    on Wilson binomial confidence bounds for uncertain proportions.
    """

    minimum_reviewed_total: int = 500
    minimum_non_ambiguous_disagreements: int = 100
    minimum_ml_strict_lower_bound: float = 0.95
    minimum_ml_disagreement_lower_bound: float = 0.55
    minimum_rolling_strict_ml_score: float = 0.90
    rolling_window_size: int = 100


def wilson_lower_bound(successes: int, trials: int, *, z_value: float = 1.96) -> float:
    """Return the Wilson lower confidence bound for a binomial proportion."""
    if trials <= 0:
        return 0.0
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between zero and trials")
    p_hat = successes / trials
    denominator = 1.0 + (z_value * z_value) / trials
    center = p_hat + (z_value * z_value) / (2.0 * trials)
    spread = z_value * math.sqrt(
        (p_hat * (1.0 - p_hat) + (z_value * z_value) / (4.0 * trials)) / trials
    )
    return max(0.0, (center - spread) / denominator)


def compute_prompt_router_reasoner_stats(
    review_items: Sequence[Mapping[str, Any]],
    *,
    thresholds: PilotReadinessThresholds | None = None,
) -> dict[str, Any]:
    """Compute friendly scores, strict scores, and pilot-readiness metrics."""
    active_thresholds = thresholds or PilotReadinessThresholds()
    reviewed_items = [dict(item) for item in review_items if item.get("review_status") == STATUS_REVIEWED]
    pending_reviews = sum(1 for item in review_items if item.get("review_status") != STATUS_REVIEWED)

    reviewed_total = len(reviewed_items)
    heuristics_correct_count = 0
    ml_correct_count = 0
    both_acceptable_count = 0
    agreement_count = 0
    disagreement_count = 0
    non_ambiguous_disagreement_count = 0
    ml_wins_in_disagreements = 0
    heuristic_wins_in_disagreements = 0
    ambiguous_disagreements = 0
    safety_violation_count = 0

    for item in reviewed_items:
        label = item.get("human_label")
        agreement = item.get("agreement_status")
        if item.get("safety_violation") is True:
            safety_violation_count += 1
        if label == LABEL_BOTH_ACCEPTABLE_UNCLEAR:
            both_acceptable_count += 1
        if agreement == AGREEMENT_AGREE:
            agreement_count += 1
            if label in (LABEL_HEURISTICS_CORRECT, LABEL_ML_CORRECT):
                heuristics_correct_count += 1
                ml_correct_count += 1
            continue
        if agreement == AGREEMENT_DISAGREE:
            disagreement_count += 1
            if label == LABEL_HEURISTICS_CORRECT:
                heuristics_correct_count += 1
                heuristic_wins_in_disagreements += 1
                non_ambiguous_disagreement_count += 1
            elif label == LABEL_ML_CORRECT:
                ml_correct_count += 1
                ml_wins_in_disagreements += 1
                non_ambiguous_disagreement_count += 1
            elif label == LABEL_BOTH_ACCEPTABLE_UNCLEAR:
                ambiguous_disagreements += 1
            continue
        if label == LABEL_HEURISTICS_CORRECT:
            heuristics_correct_count += 1
        elif label == LABEL_ML_CORRECT:
            ml_correct_count += 1

    strict_non_ambiguous_total = reviewed_total - both_acceptable_count
    friendly_heuristic_score = _safe_ratio(
        heuristics_correct_count + both_acceptable_count,
        reviewed_total,
    )
    friendly_ml_score = _safe_ratio(
        ml_correct_count + both_acceptable_count,
        reviewed_total,
    )
    strict_heuristic_score = _safe_ratio(heuristics_correct_count, strict_non_ambiguous_total)
    strict_ml_score = _safe_ratio(ml_correct_count, strict_non_ambiguous_total)
    ml_disagreement_win_rate = _safe_ratio(
        ml_wins_in_disagreements,
        non_ambiguous_disagreement_count,
    )
    heuristic_disagreement_win_rate = _safe_ratio(
        heuristic_wins_in_disagreements,
        non_ambiguous_disagreement_count,
    )
    ml_strict_wilson_lower_bound = wilson_lower_bound(
        ml_correct_count,
        strict_non_ambiguous_total,
    )
    ml_disagreement_wilson_lower_bound = wilson_lower_bound(
        ml_wins_in_disagreements,
        non_ambiguous_disagreement_count,
    )
    rolling_stats = _compute_rolling_stats(reviewed_items, active_thresholds.rolling_window_size)

    blocking_reasons: list[str] = []
    if reviewed_total < active_thresholds.minimum_reviewed_total:
        blocking_reasons.append(
            "reviewed_total_below_minimum: "
            + str(reviewed_total)
            + " < "
            + str(active_thresholds.minimum_reviewed_total)
        )
    if non_ambiguous_disagreement_count < active_thresholds.minimum_non_ambiguous_disagreements:
        blocking_reasons.append(
            "non_ambiguous_disagreements_below_minimum: "
            + str(non_ambiguous_disagreement_count)
            + " < "
            + str(active_thresholds.minimum_non_ambiguous_disagreements)
        )
    if ml_strict_wilson_lower_bound < active_thresholds.minimum_ml_strict_lower_bound:
        blocking_reasons.append(
            "ml_strict_wilson_lower_bound_below_threshold: "
            + _format_ratio(ml_strict_wilson_lower_bound)
        )
    if ml_disagreement_wilson_lower_bound < active_thresholds.minimum_ml_disagreement_lower_bound:
        blocking_reasons.append(
            "ml_disagreement_wilson_lower_bound_below_threshold: "
            + _format_ratio(ml_disagreement_wilson_lower_bound)
        )
    if rolling_stats["rolling_strict_ml_score"] < active_thresholds.minimum_rolling_strict_ml_score:
        blocking_reasons.append(
            "rolling_strict_ml_score_below_threshold: "
            + _format_ratio(rolling_stats["rolling_strict_ml_score"])
        )
    if safety_violation_count > 0:
        blocking_reasons.append("safety_violations_present: " + str(safety_violation_count))

    pilot_threshold_met = not blocking_reasons
    pilot_readiness_percent = _readiness_percent(
        reviewed_total=reviewed_total,
        non_ambiguous_disagreement_count=non_ambiguous_disagreement_count,
        ml_strict_wilson_lower_bound=ml_strict_wilson_lower_bound,
        ml_disagreement_wilson_lower_bound=ml_disagreement_wilson_lower_bound,
        safety_violation_count=safety_violation_count,
        thresholds=active_thresholds,
    )

    return {
        "pilot_activation_policy": "conservative_wilson_lcb_auto_ml_pilot_v1",
        "pilot_activation_policy_basis": [
            "No universal ML pilot threshold exists for this app domain.",
            "Use minimum sample counts before promotion decisions.",
            "Use Wilson lower confidence bounds instead of raw percentages.",
            "Require clean rolling-window performance and zero safety violations.",
        ],
        "pilot_activation_thresholds": {
            "minimum_reviewed_total": active_thresholds.minimum_reviewed_total,
            "minimum_non_ambiguous_disagreements": active_thresholds.minimum_non_ambiguous_disagreements,
            "minimum_ml_strict_lower_bound": active_thresholds.minimum_ml_strict_lower_bound,
            "minimum_ml_disagreement_lower_bound": active_thresholds.minimum_ml_disagreement_lower_bound,
            "minimum_rolling_strict_ml_score": active_thresholds.minimum_rolling_strict_ml_score,
            "rolling_window_size": active_thresholds.rolling_window_size,
        },
        "auto_ml_pilot_activation_eligible": pilot_threshold_met,
        "pending_reviews": pending_reviews,
        "reviewed_total": reviewed_total,
        "heuristics_correct_count": heuristics_correct_count,
        "ml_correct_count": ml_correct_count,
        "both_acceptable_count": both_acceptable_count,
        "agreement_count": agreement_count,
        "disagreement_count": disagreement_count,
        "non_ambiguous_disagreement_count": non_ambiguous_disagreement_count,
        "ml_wins_in_disagreements": ml_wins_in_disagreements,
        "heuristic_wins_in_disagreements": heuristic_wins_in_disagreements,
        "ambiguous_disagreements": ambiguous_disagreements,
        "ml_disagreement_win_rate": ml_disagreement_win_rate,
        "heuristic_disagreement_win_rate": heuristic_disagreement_win_rate,
        "friendly_heuristic_score": friendly_heuristic_score,
        "friendly_ml_score": friendly_ml_score,
        "strict_heuristic_score": strict_heuristic_score,
        "strict_ml_score": strict_ml_score,
        "strict_non_ambiguous_total": strict_non_ambiguous_total,
        "ml_strict_wilson_lower_bound": ml_strict_wilson_lower_bound,
        "ml_disagreement_wilson_lower_bound": ml_disagreement_wilson_lower_bound,
        "rolling_window_size": active_thresholds.rolling_window_size,
        "rolling_strict_ml_score": rolling_stats["rolling_strict_ml_score"],
        "rolling_strict_heuristic_score": rolling_stats["rolling_strict_heuristic_score"],
        "rolling_non_ambiguous_total": rolling_stats["rolling_non_ambiguous_total"],
        "safety_violation_count": safety_violation_count,
        "pilot_readiness_percent": pilot_readiness_percent,
        "pilot_threshold_met": pilot_threshold_met,
        "pilot_blocking_reasons": blocking_reasons,
    }


def _compute_rolling_stats(items: Sequence[Mapping[str, Any]], window_size: int) -> dict[str, Any]:
    """Support compute rolling stats behavior.
    
    Parameters
    ----------
    items : Sequence[Mapping[str, Any]]
        The item values.
    window_size : int
        The window size value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    recent = list(items)[-max(1, int(window_size)) :]
    ml_correct = 0
    heur_correct = 0
    ambiguous = 0
    for item in recent:
        label = item.get("human_label")
        agreement = item.get("agreement_status")
        if label == LABEL_BOTH_ACCEPTABLE_UNCLEAR:
            ambiguous += 1
        elif agreement == AGREEMENT_AGREE and label in (LABEL_HEURISTICS_CORRECT, LABEL_ML_CORRECT):
            ml_correct += 1
            heur_correct += 1
        elif agreement == AGREEMENT_DISAGREE and label == LABEL_ML_CORRECT:
            ml_correct += 1
        elif agreement == AGREEMENT_DISAGREE and label == LABEL_HEURISTICS_CORRECT:
            heur_correct += 1
        elif label == LABEL_ML_CORRECT:
            ml_correct += 1
        elif label == LABEL_HEURISTICS_CORRECT:
            heur_correct += 1
    denominator = len(recent) - ambiguous
    return {
        "rolling_strict_ml_score": _safe_ratio(ml_correct, denominator),
        "rolling_strict_heuristic_score": _safe_ratio(heur_correct, denominator),
        "rolling_non_ambiguous_total": denominator,
    }


def _readiness_percent(
    *,
    reviewed_total: int,
    non_ambiguous_disagreement_count: int,
    ml_strict_wilson_lower_bound: float,
    ml_disagreement_wilson_lower_bound: float,
    safety_violation_count: int,
    thresholds: PilotReadinessThresholds,
) -> float:
    """Support readiness percent behavior.
    
    Parameters
    ----------
    reviewed_total : int
        The reviewed total value.
    non_ambiguous_disagreement_count : int
        The non ambiguous disagreement count value.
    ml_strict_wilson_lower_bound : float
        The ml strict wilson lower bound value.
    ml_disagreement_wilson_lower_bound : float
        The ml disagreement wilson lower bound value.
    safety_violation_count : int
        The safety violation count value.
    thresholds : PilotReadinessThresholds
        The thresholds value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    if safety_violation_count > 0:
        return 0.0
    sample_component = min(1.0, _safe_ratio(reviewed_total, thresholds.minimum_reviewed_total))
    disagreement_component = min(
        1.0,
        _safe_ratio(non_ambiguous_disagreement_count, thresholds.minimum_non_ambiguous_disagreements),
    )
    strict_component = min(
        1.0,
        _safe_ratio(ml_strict_wilson_lower_bound, thresholds.minimum_ml_strict_lower_bound),
    )
    disagreement_score_component = min(
        1.0,
        _safe_ratio(
            ml_disagreement_wilson_lower_bound,
            thresholds.minimum_ml_disagreement_lower_bound,
        ),
    )
    return round(
        100.0
        * min(
            sample_component,
            disagreement_component,
            strict_component,
            disagreement_score_component,
        ),
        2,
    )


def _safe_ratio(numerator: float, denominator: float) -> float:
    """Support safe ratio behavior.
    
    Parameters
    ----------
    numerator : float
        The numerator value.
    denominator : float
        The denominator value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    if denominator <= 0:
        return 0.0
    return float(numerator) / float(denominator)


def _format_ratio(value: float) -> str:
    """Support format ratio behavior.
    
    Parameters
    ----------
    value : float
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return f"{value:.4f}"
