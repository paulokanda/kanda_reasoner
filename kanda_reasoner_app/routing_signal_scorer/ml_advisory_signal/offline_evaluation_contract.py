# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_evaluation_contract.py
"""Offline evaluation contracts for Phase 2 advisory harness.

These contracts are still non-runtime and non-authoritative. They only compare
caller-supplied, already-governed decisions before and after advisory telemetry.
They do not compute routes, load prompts, read project canon, persist reports,
or call providers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from .contract import AdvisoryInput, AdvisoryOutput


class OfflineEvaluationStatus(str, Enum):
    """Finite statuses for the in-memory offline harness."""

    PASSED = "PASSED"
    FAIL_OPEN_ABSTAINED = "FAIL_OPEN_ABSTAINED"
    REJECTED_ROUTE_VARIANCE = "REJECTED_ROUTE_VARIANCE"


@dataclass(frozen=True)
class OfflineEvaluationFixture:
    """Caller-supplied, in-memory fixture for advisory evaluation.

    The governed decision values are supplied by the caller. The harness only
    compares equality to prove advisory telemetry did not change the final
    governed decision.
    """

    fixture_id: str
    advisory_input: AdvisoryInput
    governed_decision_before_advisory: str
    governed_decision_after_advisory: str
    expected_invariant: bool = True

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("fixture_id", self.fixture_id)
        if not isinstance(self.advisory_input, AdvisoryInput):
            raise TypeError("advisory_input must be AdvisoryInput")
        _require_text(
            "governed_decision_before_advisory",
            self.governed_decision_before_advisory,
        )
        _require_text(
            "governed_decision_after_advisory",
            self.governed_decision_after_advisory,
        )
        if not isinstance(self.expected_invariant, bool):
            raise TypeError("expected_invariant must be bool")


@dataclass(frozen=True)
class OfflineEvaluationResult:
    """Single fixture result from the offline harness."""

    fixture_id: str
    advisor_label: str
    status: OfflineEvaluationStatus
    route_invariant: bool
    advisor_abstained: bool
    advisory_output: AdvisoryOutput

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("fixture_id", self.fixture_id)
        _require_text("advisor_label", self.advisor_label)
        if not isinstance(self.status, OfflineEvaluationStatus):
            raise TypeError("status must be OfflineEvaluationStatus")
        if not isinstance(self.route_invariant, bool):
            raise TypeError("route_invariant must be bool")
        if not isinstance(self.advisor_abstained, bool):
            raise TypeError("advisor_abstained must be bool")
        if not isinstance(self.advisory_output, AdvisoryOutput):
            raise TypeError("advisory_output must be AdvisoryOutput")


@dataclass(frozen=True)
class OfflineEvaluationSummary:
    """Immutable in-memory summary for a complete offline evaluation."""

    feature_id: str
    advisor_label: str
    total_fixtures: int
    invariant_pass_count: int
    fail_open_count: int
    rejected_variance_count: int
    results: Tuple[OfflineEvaluationResult, ...]

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("feature_id", self.feature_id)
        _require_text("advisor_label", self.advisor_label)
        _require_non_negative_int("total_fixtures", self.total_fixtures)
        _require_non_negative_int("invariant_pass_count", self.invariant_pass_count)
        _require_non_negative_int("fail_open_count", self.fail_open_count)
        _require_non_negative_int("rejected_variance_count", self.rejected_variance_count)
        if not isinstance(self.results, tuple):
            raise TypeError("results must be tuple")
        for item in self.results:
            if not isinstance(item, OfflineEvaluationResult):
                raise TypeError("results contains invalid item")
        if self.total_fixtures != len(self.results):
            raise ValueError("total_fixtures must match results length")


FEATURE_ID = "rss_ml_adv_phase2_offline_evaluation_harness_contract_v1"


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
