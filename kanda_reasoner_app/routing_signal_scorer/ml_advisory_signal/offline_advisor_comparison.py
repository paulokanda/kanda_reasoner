# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_advisor_comparison.py
"""Phase 4 offline advisor comparison helpers.

This module uses only existing null/mock advisors, the synthetic Phase 3
fixture catalog, and the Phase 2 offline harness. It is not runtime ML, does
not call providers, does not read prompt libraries or freeze memory, does not
persist reports, and does not modify router decisions.
"""

from __future__ import annotations

from .advisor_comparison_contract import (
    OfflineAdvisorComparisonReport,
    compare_offline_advisor_summaries,
)
from .fixture_catalog_contract import catalog_fixtures
from .mock_advisor import MockAdvisor
from .null_advisor import NullAdvisor
from .offline_evaluation_harness import run_offline_evaluation
from .offline_fixture_catalog import build_phase3_synthetic_fixture_catalog


COMPARISON_ID = "phase4_null_vs_mock_offline_comparison_v1"


def run_phase4_null_vs_mock_offline_comparison() -> OfflineAdvisorComparisonReport:
    """Run a passive offline comparison between NullAdvisor and MockAdvisor."""

    catalog = build_phase3_synthetic_fixture_catalog()
    fixtures = catalog_fixtures(catalog)
    null_summary = run_offline_evaluation(
        advisor=NullAdvisor(),
        fixtures=fixtures,
        advisor_label="null_advisor",
    )
    mock_summary = run_offline_evaluation(
        advisor=MockAdvisor(),
        fixtures=fixtures,
        advisor_label="mock_advisor",
    )
    return compare_offline_advisor_summaries(
        comparison_id=COMPARISON_ID,
        summaries=(null_summary, mock_summary),
    )
