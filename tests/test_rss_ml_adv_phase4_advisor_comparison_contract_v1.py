from __future__ import annotations

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.advisor_comparison_contract import (
    FEATURE_ID,
    OfflineAdvisorComparisonReport,
    OfflineAdvisorComparisonStatus,
    compare_offline_advisor_summaries,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.fixture_catalog_contract import catalog_fixtures
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.mock_advisor import MockAdvisor
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.null_advisor import NullAdvisor
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_advisor_comparison import (
    COMPARISON_ID,
    run_phase4_null_vs_mock_offline_comparison,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_evaluation_harness import run_offline_evaluation
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_fixture_catalog import build_phase3_synthetic_fixture_catalog


def test_phase4_null_vs_mock_comparison_is_passive_and_bounded() -> None:
    report = run_phase4_null_vs_mock_offline_comparison()

    assert isinstance(report, OfflineAdvisorComparisonReport)
    assert report.comparison_id == COMPARISON_ID
    assert report.feature_id == FEATURE_ID
    assert report.status == OfflineAdvisorComparisonStatus.ROUTE_VARIANCE_REJECTION_OBSERVED
    assert report.total_participants == 2
    assert report.total_fixture_count == 5
    assert report.total_result_count == 10
    assert report.invariant_pass_count == 8
    assert report.route_variance_rejected_count == 2
    assert report.advisor_abstention_result_count == 5
    assert report.non_runtime is True
    assert report.non_authoritative is True
    assert "no_route_authority" in report.comparison_notes
    assert "no_prompt_ranking" in report.comparison_notes

    labels = tuple(participant.advisor_label for participant in report.participants)
    assert labels == ("null_advisor", "mock_advisor")


def test_phase4_rejects_mismatched_fixture_sets() -> None:
    catalog = build_phase3_synthetic_fixture_catalog()
    fixtures = catalog_fixtures(catalog)
    null_summary = run_offline_evaluation(
        advisor=NullAdvisor(),
        fixtures=fixtures,
        advisor_label="null_advisor",
    )
    mock_summary = run_offline_evaluation(
        advisor=MockAdvisor(),
        fixtures=fixtures[:-1],
        advisor_label="mock_advisor",
    )

    try:
        compare_offline_advisor_summaries(
            comparison_id="mismatch_should_fail",
            summaries=(null_summary, mock_summary),
        )
    except ValueError as exc:
        assert "same fixture IDs" in str(exc)
    else:
        raise AssertionError("mismatched fixtures must be rejected")


if __name__ == "__main__":
    test_phase4_null_vs_mock_comparison_is_passive_and_bounded()
    test_phase4_rejects_mismatched_fixture_sets()
