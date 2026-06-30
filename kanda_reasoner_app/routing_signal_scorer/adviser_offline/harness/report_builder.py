
"""Offline Adviser comparison report builder.

The report builder summarizes already-produced comparison results. It is pure and
side-effect free: no files are read or written, no candidates are executed, and
no routing behavior is changed.
"""

from __future__ import annotations


__all__ = [
    'AdviserHarnessRunSummary',
    'assert_summary_has_no_critical_failures',
    'build_run_summary',
]
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

FEATURE_ID = "routing_signal_scorer_v3_adviser_pure_comparison_harness_v1"
SCHEMA_VERSION = "3.44-adviser-pure-comparison-harness"
AUTHORITY_STATEMENT = "advisory_only"
SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(frozen=True)
class AdviserHarnessRunSummary:
    """Serializable pure-harness run summary."""

    schema_version: str
    run_id: str
    timestamp: str
    candidate_id: str
    candidate_version: str
    candidate_code_hash: str
    gold_set_version: str
    gold_manifest_hash: str
    cases_run: int
    critical_failures: int
    promotion_blockers: int
    aggregate_severity: str
    status: str
    authority_statement: str = AUTHORITY_STATEMENT
    feature_id: str = FEATURE_ID

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "candidate_id": self.candidate_id,
            "candidate_version": self.candidate_version,
            "candidate_code_hash": self.candidate_code_hash,
            "gold_set_version": self.gold_set_version,
            "gold_manifest_hash": self.gold_manifest_hash,
            "cases_run": self.cases_run,
            "critical_failures": self.critical_failures,
            "promotion_blockers": self.promotion_blockers,
            "aggregate_severity": self.aggregate_severity,
            "status": self.status,
            "authority_statement": self.authority_statement,
            "feature_id": self.feature_id,
        }


def build_run_summary(
    comparisons: Sequence[Mapping[str, Any]],
    *,
    run_id: str,
    candidate_id: str,
    candidate_version: str,
    candidate_code_hash: str = "not_applicable_no_candidate_in_m5",
    gold_set_version: str = "not_applicable_no_gold_set_in_m5",
    gold_manifest_hash: str = "not_applicable_no_gold_manifest_in_m5",
    timestamp: str = "not_recorded_pure_harness_no_clock_read",
) -> dict[str, object]:
    """Build a run summary from supplied comparison dictionaries.

    The caller supplies all metadata. This function intentionally does not read
    the clock, filesystem, git state, registry, or gold manifests.
    """

    cases_run = len(comparisons)
    critical_failures = 0
    promotion_blockers = 0
    highest = 0
    for comparison in comparisons:
        if not isinstance(comparison, Mapping):
            promotion_blockers += 1
            critical_failures += 1
            highest = max(highest, SEVERITY_ORDER["critical"])
            continue
        severity = str(comparison.get("aggregate_severity", "none"))
        highest = max(highest, SEVERITY_ORDER.get(severity, 0))
        if severity == "critical":
            critical_failures += 1
        if bool(comparison.get("promotion_blocker")):
            promotion_blockers += 1

    aggregate = _severity_from_rank(highest)
    status = "blocked" if critical_failures or promotion_blockers else "eligible_for_review"
    return AdviserHarnessRunSummary(
        schema_version=SCHEMA_VERSION,
        run_id=run_id,
        timestamp=timestamp,
        candidate_id=candidate_id,
        candidate_version=candidate_version,
        candidate_code_hash=candidate_code_hash,
        gold_set_version=gold_set_version,
        gold_manifest_hash=gold_manifest_hash,
        cases_run=cases_run,
        critical_failures=critical_failures,
        promotion_blockers=promotion_blockers,
        aggregate_severity=aggregate,
        status=status,
    ).to_dict()


def assert_summary_has_no_critical_failures(summary: Mapping[str, Any]) -> Mapping[str, Any]:
    """Raise when a pure-harness summary contains critical failures."""

    if int(summary.get("critical_failures", 0)) > 0 or str(summary.get("status")) == "blocked":
        raise ValueError("pure Adviser comparison harness summary contains promotion blockers")
    return summary


def _severity_from_rank(rank: int) -> str:
    for severity, value in SEVERITY_ORDER.items():
        if value == rank:
            return severity
    return "none"
