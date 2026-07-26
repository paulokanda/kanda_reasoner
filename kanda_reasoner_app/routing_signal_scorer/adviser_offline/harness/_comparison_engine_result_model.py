# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/_comparison_engine_result_model.py
"""Serializable comparison result model and final result construction."""

from __future__ import annotations

from dataclasses import dataclass

from ._comparison_engine_support import (
    AUTHORITY_STATEMENT,
    FEATURE_ID,
    SCHEMA_VERSION,
    _aggregate_severity,
)

__all__ = ()


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
        """Support to dict behavior.
        
        Returns
        -------
        dict[str, object]
            The mapped values.
        """
        
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


def _build_final_result(
    *,
    report_id: str,
    run_id: str,
    case_id: str,
    teacher_ref: str,
    candidate_ref: str,
    disagreements: list[dict[str, object]],
    teacher_review_status: str,
    candidate_guard_ok: bool,
    resource_limits_ok: bool,
) -> dict[str, object]:
    """Support final result behavior.
    
    Parameters
    ----------
    report_id : str
        The report id value.
    run_id : str
        The run id value.
    case_id : str
        The case id value.
    teacher_ref : str
        The teacher ref value.
    candidate_ref : str
        The candidate ref value.
    disagreements : list[dict[str, object]]
        The disagreements value.
    teacher_review_status : str
        The teacher review status value.
    candidate_guard_ok : bool
        The candidate guard ok value.
    resource_limits_ok : bool
        The resource limits ok value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    aggregate = _aggregate_severity(disagreements)
    promotion_blocker = aggregate == "critical" or not candidate_guard_ok or not resource_limits_ok
    review_status = "pending" if disagreements else "reviewed"
    return AdviserComparisonResult(
        ok=not promotion_blocker and not disagreements,
        report_id=report_id,
        run_id=run_id,
        case_id=case_id,
        teacher_answer_ref=teacher_ref,
        candidate_answer_ref=candidate_ref,
        disagreements=tuple(disagreements),
        aggregate_severity=aggregate,
        promotion_blocker=promotion_blocker,
        review_status=review_status,
        teacher_review_status=teacher_review_status,
        candidate_guard_ok=candidate_guard_ok,
        resource_limits_ok=resource_limits_ok,
    ).to_dict()


def _final_result(
    *,
    report_id: str,
    run_id: str,
    case_id: str,
    teacher_ref: str,
    candidate_ref: str,
    disagreements: list[dict[str, object]],
    teacher_review_status: str,
    candidate_guard_ok: bool,
    resource_limits_ok: bool,
) -> dict[str, object]:
    """Compatibility wrapper preserving the historical private call contract."""
    return _build_final_result(
        report_id=report_id,
        run_id=run_id,
        case_id=case_id,
        teacher_ref=teacher_ref,
        candidate_ref=candidate_ref,
        disagreements=disagreements,
        teacher_review_status=teacher_review_status,
        candidate_guard_ok=candidate_guard_ok,
        resource_limits_ok=resource_limits_ok,
    )


