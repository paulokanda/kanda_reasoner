from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_stats import (
    PilotReadinessThresholds,
    compute_prompt_router_reasoner_stats,
    wilson_lower_bound,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    AGREEMENT_AGREE,
    AGREEMENT_DISAGREE,
    LABEL_BOTH_ACCEPTABLE_UNCLEAR,
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    STATUS_PENDING,
    STATUS_REVIEWED,
)


def _item(label: str | None, agreement: str, *, safety: bool = False) -> dict:
    return {
        "review_status": STATUS_REVIEWED if label is not None else STATUS_PENDING,
        "human_label": label,
        "agreement_status": agreement,
        "safety_violation": safety,
    }


def test_wilson_lower_bound_penalizes_small_samples() -> None:
    small = wilson_lower_bound(9, 10)
    larger = wilson_lower_bound(180, 200)
    assert small < 0.90
    assert larger > small


def test_stats_separate_friendly_and_strict_scores() -> None:
    items = [
        _item(LABEL_HEURISTICS_CORRECT, AGREEMENT_AGREE),
        _item(LABEL_ML_CORRECT, AGREEMENT_AGREE),
        _item(LABEL_HEURISTICS_CORRECT, AGREEMENT_DISAGREE),
        _item(LABEL_ML_CORRECT, AGREEMENT_DISAGREE),
        _item(LABEL_BOTH_ACCEPTABLE_UNCLEAR, AGREEMENT_DISAGREE),
        _item(None, AGREEMENT_DISAGREE),
    ]
    stats = compute_prompt_router_reasoner_stats(items)
    assert stats["pending_reviews"] == 1
    assert stats["reviewed_total"] == 5
    assert stats["heuristics_correct_count"] == 3
    assert stats["ml_correct_count"] == 3
    assert stats["both_acceptable_count"] == 1
    assert stats["friendly_heuristic_score"] == 4 / 5
    assert stats["friendly_ml_score"] == 4 / 5
    assert stats["strict_non_ambiguous_total"] == 4
    assert stats["strict_heuristic_score"] == 3 / 4
    assert stats["strict_ml_score"] == 3 / 4
    assert stats["disagreement_count"] == 3
    assert stats["non_ambiguous_disagreement_count"] == 2
    assert stats["ambiguous_disagreements"] == 1
    assert stats["ml_wins_in_disagreements"] == 1
    assert stats["heuristic_wins_in_disagreements"] == 1


def test_ambiguous_cases_do_not_unlock_pilot_readiness() -> None:
    items = [_item(LABEL_BOTH_ACCEPTABLE_UNCLEAR, AGREEMENT_DISAGREE) for _ in range(300)]
    stats = compute_prompt_router_reasoner_stats(
        items,
        thresholds=PilotReadinessThresholds(
            minimum_reviewed_total=10,
            minimum_non_ambiguous_disagreements=5,
            minimum_ml_strict_lower_bound=0.50,
            minimum_ml_disagreement_lower_bound=0.50,
            minimum_rolling_strict_ml_score=0.50,
            rolling_window_size=10,
        ),
    )
    assert stats["reviewed_total"] == 300
    assert stats["strict_non_ambiguous_total"] == 0
    assert stats["non_ambiguous_disagreement_count"] == 0
    assert stats["pilot_threshold_met"] is False


def test_raw_percentage_cannot_unlock_with_tiny_sample() -> None:
    items = [_item(LABEL_ML_CORRECT, AGREEMENT_DISAGREE) for _ in range(5)]
    stats = compute_prompt_router_reasoner_stats(
        items,
        thresholds=PilotReadinessThresholds(
            minimum_reviewed_total=200,
            minimum_non_ambiguous_disagreements=50,
            minimum_ml_strict_lower_bound=0.90,
            minimum_ml_disagreement_lower_bound=0.50,
            minimum_rolling_strict_ml_score=0.85,
            rolling_window_size=5,
        ),
    )
    assert stats["strict_ml_score"] == 1.0
    assert stats["ml_disagreement_win_rate"] == 1.0
    assert stats["pilot_threshold_met"] is False
    assert stats["pilot_readiness_percent"] < 100.0
    assert any("reviewed_total_below_minimum" in reason for reason in stats["pilot_blocking_reasons"])


def test_safety_violation_blocks_pilot_readiness() -> None:
    items = [_item(LABEL_ML_CORRECT, AGREEMENT_DISAGREE) for _ in range(80)]
    items.append(_item(LABEL_ML_CORRECT, AGREEMENT_DISAGREE, safety=True))
    stats = compute_prompt_router_reasoner_stats(
        items,
        thresholds=PilotReadinessThresholds(
            minimum_reviewed_total=10,
            minimum_non_ambiguous_disagreements=10,
            minimum_ml_strict_lower_bound=0.50,
            minimum_ml_disagreement_lower_bound=0.50,
            minimum_rolling_strict_ml_score=0.50,
            rolling_window_size=10,
        ),
    )
    assert stats["safety_violation_count"] == 1
    assert stats["pilot_threshold_met"] is False
    assert stats["pilot_readiness_percent"] == 0.0


def test_readiness_can_pass_only_with_enough_clean_evidence() -> None:
    items = [_item(LABEL_ML_CORRECT, AGREEMENT_DISAGREE) for _ in range(80)]
    stats = compute_prompt_router_reasoner_stats(
        items,
        thresholds=PilotReadinessThresholds(
            minimum_reviewed_total=20,
            minimum_non_ambiguous_disagreements=20,
            minimum_ml_strict_lower_bound=0.80,
            minimum_ml_disagreement_lower_bound=0.80,
            minimum_rolling_strict_ml_score=0.80,
            rolling_window_size=20,
        ),
    )
    assert stats["pilot_threshold_met"] is True
    assert stats["pilot_readiness_percent"] == 100.0


if __name__ == "__main__":
    test_wilson_lower_bound_penalizes_small_samples()
    test_stats_separate_friendly_and_strict_scores()
    test_ambiguous_cases_do_not_unlock_pilot_readiness()
    test_raw_percentage_cannot_unlock_with_tiny_sample()
    test_safety_violation_blocks_pilot_readiness()
    test_readiness_can_pass_only_with_enough_clean_evidence()
    print("VALIDATION OK: prompt router reasoner review stats")
