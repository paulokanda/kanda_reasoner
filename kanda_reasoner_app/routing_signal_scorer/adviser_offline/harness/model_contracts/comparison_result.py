# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/model_contracts/comparison_result.py
"""Stable public comparison result model contract."""

from __future__ import annotations

from dataclasses import dataclass

from .._comparison_engine_support import (
    AUTHORITY_STATEMENT,
    FEATURE_ID,
    SCHEMA_VERSION,
)

__all__ = ["AdviserComparisonResult"]


@dataclass(frozen=True)
class AdviserComparisonResult:
    """Serializable comparison result."""

    ok: bool
    report_id: str
    run_id: str
    case_id: str
    teacher_answer_ref: str
    candidate_answer_ref: str
    disagreements: tuple[dict[str, object], ...]
    aggregate_severity: str
    promotion_blocker: bool
    review_status: str
    teacher_review_status: str
    candidate_guard_ok: bool
    resource_limits_ok: bool
    authority_statement: str = AUTHORITY_STATEMENT
    feature_id: str = FEATURE_ID
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        """Return the JSON-serializable result payload."""
        return {
            "ok": self.ok,
            "report_id": self.report_id,
            "run_id": self.run_id,
            "case_id": self.case_id,
            "teacher_answer_ref": self.teacher_answer_ref,
            "candidate_answer_ref": self.candidate_answer_ref,
            "disagreements": [dict(item) for item in self.disagreements],
            "aggregate_severity": self.aggregate_severity,
            "promotion_blocker": self.promotion_blocker,
            "review_status": self.review_status,
            "teacher_review_status": self.teacher_review_status,
            "candidate_guard_ok": self.candidate_guard_ok,
            "resource_limits_ok": self.resource_limits_ok,
            "authority_statement": self.authority_statement,
            "feature_id": self.feature_id,
            "schema_version": self.schema_version,
        }
