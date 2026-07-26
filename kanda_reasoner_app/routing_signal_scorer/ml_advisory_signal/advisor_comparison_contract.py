# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/advisor_comparison_contract.py
"""Contracts for Phase 4 offline advisor comparison.

The comparison is non-runtime and non-authoritative. It compares bounded
in-memory summaries produced by the Phase 2 harness over Phase 3 synthetic
fixtures. It does not choose routes, rank prompts, read prompt libraries,
read freeze memory, read router canon, call providers, persist reports,
train models, calibrate models, or modify router behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from .offline_evaluation_contract import (
    OfflineEvaluationResult,
    OfflineEvaluationStatus,
    OfflineEvaluationSummary,
)


FEATURE_ID = "rss_ml_adv_phase4_offline_advisor_comparison_contract_v1"


class OfflineAdvisorComparisonStatus(str, Enum):
    """Finite statuses for non-authoritative offline comparison."""

    PASSIVE_COMPARISON_COMPLETED = "PASSIVE_COMPARISON_COMPLETED"
    ROUTE_VARIANCE_REJECTION_OBSERVED = "ROUTE_VARIANCE_REJECTION_OBSERVED"
    ADVISOR_ABSTENTION_OBSERVED = "ADVISOR_ABSTENTION_OBSERVED"


@dataclass(frozen=True)
class OfflineAdvisorComparisonParticipant:
    """One advisor summary included in an offline comparison report."""

    advisor_label: str
    summary: OfflineEvaluationSummary
    non_runtime: bool = True
    non_authoritative: bool = True

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("advisor_label", self.advisor_label)
        if not isinstance(self.summary, OfflineEvaluationSummary):
            raise TypeError("summary must be OfflineEvaluationSummary")
        if self.summary.advisor_label != self.advisor_label:
            raise ValueError("advisor_label must match summary.advisor_label")
        if self.non_runtime is not True:
            raise ValueError("non_runtime must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")


@dataclass(frozen=True)
class OfflineAdvisorComparisonReport:
    """Immutable in-memory report for passive advisor comparison."""

    comparison_id: str
    feature_id: str
    status: OfflineAdvisorComparisonStatus
    participants: Tuple[OfflineAdvisorComparisonParticipant, ...]
    shared_fixture_ids: Tuple[str, ...]
    total_participants: int
    total_fixture_count: int
    total_result_count: int
    invariant_pass_count: int
    advisor_abstention_result_count: int
    route_variance_rejected_count: int
    comparison_notes: Tuple[str, ...]
    non_runtime: bool = True
    non_authoritative: bool = True

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("comparison_id", self.comparison_id)
        _require_text("feature_id", self.feature_id)
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 4 advisor comparison")
        if not isinstance(self.status, OfflineAdvisorComparisonStatus):
            raise TypeError("status must be OfflineAdvisorComparisonStatus")
        _require_tuple_of_type(
            "participants",
            self.participants,
            OfflineAdvisorComparisonParticipant,
        )
        if len(self.participants) < 2:
            raise ValueError("participants must contain at least two summaries")
        _require_tuple_of_text("shared_fixture_ids", self.shared_fixture_ids)
        _require_non_negative_int("total_participants", self.total_participants)
        _require_non_negative_int("total_fixture_count", self.total_fixture_count)
        _require_non_negative_int("total_result_count", self.total_result_count)
        _require_non_negative_int("invariant_pass_count", self.invariant_pass_count)
        _require_non_negative_int(
            "advisor_abstention_result_count",
            self.advisor_abstention_result_count,
        )
        _require_non_negative_int(
            "route_variance_rejected_count",
            self.route_variance_rejected_count,
        )
        _require_tuple_of_text("comparison_notes", self.comparison_notes)
        if self.total_participants != len(self.participants):
            raise ValueError("total_participants must match participants length")
        if self.total_fixture_count != len(self.shared_fixture_ids):
            raise ValueError("total_fixture_count must match shared_fixture_ids length")
        expected_result_count = self.total_participants * self.total_fixture_count
        if self.total_result_count != expected_result_count:
            raise ValueError("total_result_count must match participants times fixtures")
        if self.non_runtime is not True:
            raise ValueError("non_runtime must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")


def compare_offline_advisor_summaries(
    *,
    comparison_id: str,
    summaries: Tuple[OfflineEvaluationSummary, ...],
) -> OfflineAdvisorComparisonReport:
    """Compare offline evaluation summaries without route authority.

    The comparison is passive: it only aggregates already-created harness
    summaries and rejects fixture-set mismatches. It never computes, selects,
    ranks, or modifies a governed route.
    """

    _require_text("comparison_id", comparison_id)
    if not isinstance(summaries, tuple):
        raise TypeError("summaries must be tuple")
    if len(summaries) < 2:
        raise ValueError("summaries must contain at least two items")

    participants = tuple(
        OfflineAdvisorComparisonParticipant(
            advisor_label=summary.advisor_label,
            summary=summary,
        )
        for summary in summaries
    )

    shared_fixture_ids = _require_same_fixture_ids(summaries)
    all_results = tuple(result for summary in summaries for result in summary.results)

    invariant_pass_count = sum(1 for result in all_results if result.route_invariant)
    advisor_abstention_result_count = sum(
        1 for result in all_results if result.advisor_abstained
    )
    route_variance_rejected_count = sum(
        1
        for result in all_results
        if result.status == OfflineEvaluationStatus.REJECTED_ROUTE_VARIANCE
    )

    notes = [
        "offline_comparison_only",
        "no_route_authority",
        "no_prompt_ranking",
        "no_router_prompt_logic_change",
    ]
    status = OfflineAdvisorComparisonStatus.PASSIVE_COMPARISON_COMPLETED
    if route_variance_rejected_count:
        status = OfflineAdvisorComparisonStatus.ROUTE_VARIANCE_REJECTION_OBSERVED
        notes.append("route_variance_rejection_observed")
    elif advisor_abstention_result_count:
        status = OfflineAdvisorComparisonStatus.ADVISOR_ABSTENTION_OBSERVED
        notes.append("advisor_abstention_observed")

    return OfflineAdvisorComparisonReport(
        comparison_id=comparison_id,
        feature_id=FEATURE_ID,
        status=status,
        participants=participants,
        shared_fixture_ids=shared_fixture_ids,
        total_participants=len(participants),
        total_fixture_count=len(shared_fixture_ids),
        total_result_count=len(all_results),
        invariant_pass_count=invariant_pass_count,
        advisor_abstention_result_count=advisor_abstention_result_count,
        route_variance_rejected_count=route_variance_rejected_count,
        comparison_notes=tuple(notes),
    )


def _require_same_fixture_ids(
    summaries: Tuple[OfflineEvaluationSummary, ...],
) -> Tuple[str, ...]:
    """Support require same fixture ids behavior.
    
    Parameters
    ----------
    summaries : Tuple[OfflineEvaluationSummary, ...]
        The summaries value.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    baseline = _fixture_ids(summaries[0].results)
    if not baseline:
        raise ValueError("summaries must contain fixture results")
    for summary in summaries[1:]:
        if _fixture_ids(summary.results) != baseline:
            raise ValueError("all summaries must contain the same fixture IDs")
    return baseline


def _fixture_ids(results: Tuple[OfflineEvaluationResult, ...]) -> Tuple[str, ...]:
    """Support fixture ids behavior.
    
    Parameters
    ----------
    results : Tuple[OfflineEvaluationResult, ...]
        The results value.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return tuple(result.fixture_id for result in results)


def _require_text(name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _require_non_negative_int(name: str, value: int) -> None:
    """Support require non negative int behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : int
        The input value.
    """
    
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be int")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def _require_tuple_of_text(name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple of text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[str, ...]
        The input value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a tuple")
    for item in value:
        _require_text(name, item)


def _require_tuple_of_type(name: str, value: tuple, item_type: type) -> None:
    """Support require tuple of type behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : tuple
        The input value.
    item_type : type
        The item type value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a tuple")
    for item in value:
        if not isinstance(item, item_type):
            raise TypeError(f"{name} contains an invalid item")
