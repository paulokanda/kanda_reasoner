# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_evaluation_harness.py
"""Offline in-memory evaluation harness for Phase 2.

This module is still not runtime integration. It only accepts caller-supplied
fixtures and an AdvisorProtocol implementation. It does not load prompts, read
router canon, read freeze memory, persist reports, call providers, compute final
routes, or mutate any registry.
"""

from __future__ import annotations

from typing import Iterable

from .advisor_interface import AdvisorProtocol
from .contract import build_abstain_output
from .offline_evaluation_contract import (
    FEATURE_ID,
    OfflineEvaluationFixture,
    OfflineEvaluationResult,
    OfflineEvaluationStatus,
    OfflineEvaluationSummary,
)
from .output_firewall import validate_advisory_output


def run_offline_evaluation(
    *,
    advisor: AdvisorProtocol,
    fixtures: Iterable[OfflineEvaluationFixture],
    advisor_label: str,
) -> OfflineEvaluationSummary:
    """Run advisory telemetry against caller-supplied in-memory fixtures.

    The route invariant is calculated only by comparing caller-supplied governed
    decision strings before and after advisory. The harness never computes or
    selects the governed decision itself.
    """

    if not isinstance(advisor_label, str) or not advisor_label.strip():
        raise ValueError("advisor_label must be a non-empty string")

    results = []
    invariant_pass_count = 0
    fail_open_count = 0
    rejected_variance_count = 0

    for fixture in tuple(fixtures):
        if not isinstance(fixture, OfflineEvaluationFixture):
            raise TypeError("fixtures must contain OfflineEvaluationFixture items")

        route_invariant = (
            fixture.governed_decision_before_advisory
            == fixture.governed_decision_after_advisory
        )

        try:
            advisory_output = advisor.advise(fixture.advisory_input)
            validate_advisory_output(advisory_output)
        except Exception:
            advisory_output = build_abstain_output(is_mock=False)
            validate_advisory_output(advisory_output)
            status = OfflineEvaluationStatus.FAIL_OPEN_ABSTAINED
            fail_open_count += 1
        else:
            if fixture.expected_invariant and not route_invariant:
                status = OfflineEvaluationStatus.REJECTED_ROUTE_VARIANCE
                rejected_variance_count += 1
            else:
                status = OfflineEvaluationStatus.PASSED
                if route_invariant:
                    invariant_pass_count += 1

        results.append(
            OfflineEvaluationResult(
                fixture_id=fixture.fixture_id,
                advisor_label=advisor_label,
                status=status,
                route_invariant=route_invariant,
                advisor_abstained=advisory_output.advisory_should_abstain,
                advisory_output=advisory_output,
            )
        )

    return OfflineEvaluationSummary(
        feature_id=FEATURE_ID,
        advisor_label=advisor_label,
        total_fixtures=len(results),
        invariant_pass_count=invariant_pass_count,
        fail_open_count=fail_open_count,
        rejected_variance_count=rejected_variance_count,
        results=tuple(results),
    )
