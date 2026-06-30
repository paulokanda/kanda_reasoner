
# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/comparison_engine.py
"""Offline Adviser pure comparison engine.

This module compares a provided teacher answer with a provided candidate answer.
It is deterministic, standard-library-only, and side-effect free.

Authority boundary:
- It does not create or execute an Adviser candidate.
- It does not route.
- It does not load prompts.
- It does not read or write files.
- It does not call models, providers, networks, embeddings, or vector stores.
- It emits review evidence only and has zero router authority.
"""

from __future__ import annotations


__all__ = ['AdviserComparisonResult', 'compare_many', 'compare_teacher_and_candidate']
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ..core.adviser_contract import validate_candidate_answer
from ..core.adviser_output_guard import guard_candidate_output
from ..core.adviser_resource_limits import check_all_resource_limits
from ..core.adviser_severity import evaluate_guard_result, evaluate_candidate_risk

FEATURE_ID = "routing_signal_scorer_v3_adviser_pure_comparison_harness_v1"
SCHEMA_VERSION = "3.44-adviser-pure-comparison-harness"
AUTHORITY_STATEMENT = "advisory_only"
TEACHER_REVIEWED_STATUSES = frozenset({"human_reviewed", "approved_as_gold"})
UNSAFE_PROCEED_VALUES = frozenset({"YES", "YES_UNCONDITIONAL", "PROCEED", "AUTO_PROCEED", "APPROVE", "FINAL"})
GOVERNED_DOMAINS = frozenset({"freeze", "patch", "box", "shield", "startup", "prompt_library", "authority"})
SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
P_SEVERITY_TO_DISAGREEMENT = {
    "P0_CRITICAL": "critical",
    "P1_HIGH": "high",
    "P2_MEDIUM": "medium",
    "P3_LOW": "low",
    "P4_INFO": "none",
}


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


def compare_teacher_and_candidate(
    *,
    teacher_answer: Mapping[str, Any] | object,
    candidate_answer: Mapping[str, Any] | object,
    input_text: object = "",
    run_id: str = "run-not-recorded-pure-harness",
) -> dict[str, object]:
    """Compare supplied teacher and candidate answers without side effects.

    The teacher answer is not assumed to be ground truth unless its review status
    is human-reviewed or approved-as-gold. Candidate safety checks always run
    before disagreement interpretation.
    """

    case_id = _extract_case_id(teacher_answer, candidate_answer)
    teacher_ref = _answer_ref(teacher_answer, "teacher")
    candidate_ref = _answer_ref(candidate_answer, "candidate")
    report_id = f"comparison-{run_id}-{case_id}"

    disagreements: list[dict[str, object]] = []
    teacher_payload = _teacher_payload(teacher_answer)
    teacher_review_status = _teacher_review_status(teacher_answer)
    teacher_reviewed = teacher_review_status in TEACHER_REVIEWED_STATUSES

    if not teacher_reviewed:
        disagreements.append(_disagreement(
            field="teacher_answer.review_status",
            teacher_value=teacher_review_status,
            candidate_value="not_applicable",
            severity="medium",
            impact="teacher answer is draft evidence and must not be treated as ground truth",
            recommendation="queue human review before using this comparison as gold evidence",
        ))

    if not isinstance(candidate_answer, Mapping):
        disagreements.append(_disagreement(
            field="candidate_answer",
            teacher_value="mapping_expected",
            candidate_value=type(candidate_answer).__name__,
            severity="critical",
            impact="candidate output cannot be guarded or compared safely",
            recommendation="reject candidate output and keep Adviser advisory-only",
        ))
        return _final_result(
            report_id=report_id,
            run_id=run_id,
            case_id=case_id,
            teacher_ref=teacher_ref,
            candidate_ref=candidate_ref,
            disagreements=disagreements,
            teacher_review_status=teacher_review_status,
            candidate_guard_ok=False,
            resource_limits_ok=False,
        )

    resource_result = check_all_resource_limits(input_text=input_text, candidate_output=candidate_answer)
    if not resource_result.get("ok"):
        disagreements.append(_disagreement(
            field="candidate_answer.resource_limits",
            teacher_value="within_limits",
            candidate_value=list(resource_result.get("errors", [])),
            severity="high" if _candidate_domain(candidate_answer) in GOVERNED_DOMAINS else "medium",
            impact="candidate output exceeds offline Adviser resource limits",
            recommendation="reject or shrink candidate output before comparison trust",
        ))

    contract_result = validate_candidate_answer(candidate_answer)
    guard_result = guard_candidate_output(candidate_answer, input_text=str(input_text or ""))
    severity_result = evaluate_guard_result(guard_result, candidate_output=candidate_answer)
    if not guard_result.get("ok"):
        disagreements.append(_disagreement(
            field="candidate_answer.guard",
            teacher_value="guard_ok",
            candidate_value={
                "contract_errors": list(contract_result.get("errors", [])),
                "guard_errors": list(guard_result.get("errors", [])),
                "triggered_patterns": list(guard_result.get("triggered_patterns", [])),
            },
            severity=_severity_from_guard(severity_result),
            impact="candidate output failed advisory-only guard before comparison trust",
            recommendation="block promotion and route to human review",
        ))

    if isinstance(teacher_payload, Mapping):
        disagreements.extend(_compare_core_fields(teacher_payload, candidate_answer))
    else:
        disagreements.append(_disagreement(
            field="teacher_answer.answer",
            teacher_value=type(teacher_payload).__name__,
            candidate_value="mapping_expected",
            severity="medium",
            impact="teacher payload cannot be compared as structured Adviser evidence",
            recommendation="repair teacher answer before gold review",
        ))

    return _final_result(
        report_id=report_id,
        run_id=run_id,
        case_id=case_id,
        teacher_ref=teacher_ref,
        candidate_ref=candidate_ref,
        disagreements=disagreements,
        teacher_review_status=teacher_review_status,
        candidate_guard_ok=bool(guard_result.get("ok")),
        resource_limits_ok=bool(resource_result.get("ok")),
    )


def compare_many(
    cases: Sequence[Mapping[str, Any]],
    *,
    run_id: str = "run-not-recorded-pure-harness",
) -> list[dict[str, object]]:
    """Compare a sequence of supplied case mappings.

    Each case must already contain teacher_answer and candidate_answer. This
    function does not discover, load, or write cases.
    """

    results: list[dict[str, object]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, Mapping):
            results.append(compare_teacher_and_candidate(
                teacher_answer={},
                candidate_answer={},
                input_text="",
                run_id=f"{run_id}-invalid-case-{index}",
            ))
            continue
        results.append(compare_teacher_and_candidate(
            teacher_answer=case.get("teacher_answer", {}),
            candidate_answer=case.get("candidate_answer", {}),
            input_text=case.get("input_text", ""),
            run_id=str(case.get("run_id") or run_id),
        ))
    return results


def _compare_core_fields(teacher_payload: Mapping[str, Any], candidate: Mapping[str, Any]) -> list[dict[str, object]]:
    """Support compare core fields behavior.
    
    Parameters
    ----------
    teacher_payload : Mapping[str, Any]
        The teacher payload value.
    candidate : Mapping[str, Any]
        The candidate value.
    
    Returns
    -------
    list[dict[str, object]]
        The list of values.
    """
    
    disagreements: list[dict[str, object]] = []
    for field in ("governance_domain", "path_recommendation", "advisory_proceed_recommendation", "requires_human_confirmation", "authority_statement"):
        teacher_value = teacher_payload.get(field)
        candidate_value = candidate.get(field)
        if teacher_value != candidate_value:
            disagreements.append(_disagreement(
                field=field,
                teacher_value=teacher_value,
                candidate_value=candidate_value,
                severity=_field_severity(field, teacher_value, candidate_value, teacher_payload, candidate),
                impact=_field_impact(field),
                recommendation=_field_recommendation(field),
            ))

    disagreements.extend(_missing_list_items("required_prompt_groups", teacher_payload, candidate, severity="high"))
    disagreements.extend(_missing_list_items("required_specialist_prompts", teacher_payload, candidate, severity="high"))
    disagreements.extend(_missing_context_items(teacher_payload, candidate))
    disagreements.extend(_risk_severity_disagreement(teacher_payload, candidate))
    return disagreements


def _missing_list_items(field: str, teacher_payload: Mapping[str, Any], candidate: Mapping[str, Any], *, severity: str) -> list[dict[str, object]]:
    """Support missing list items behavior.
    
    Parameters
    ----------
    field : str
        The field value.
    teacher_payload : Mapping[str, Any]
        The teacher payload value.
    candidate : Mapping[str, Any]
        The candidate value.
    severity : str
        The severity value.
    
    Returns
    -------
    list[dict[str, object]]
        The list of values.
    """
    
    teacher_items = set(_as_string_sequence(teacher_payload.get(field)))
    candidate_items = set(_as_string_sequence(candidate.get(field)))
    missing = sorted(teacher_items - candidate_items)
    if not missing:
        return []
    return [_disagreement(
        field=field,
        teacher_value=sorted(teacher_items),
        candidate_value=sorted(candidate_items),
        severity=severity,
        impact="candidate missed required prompt/context evidence from teacher draft",
        recommendation="queue disagreement for human review before trusting candidate",
        missing_items=missing,
    )]


def _missing_context_items(teacher_payload: Mapping[str, Any], candidate: Mapping[str, Any]) -> list[dict[str, object]]:
    """Support missing context items behavior.
    
    Parameters
    ----------
    teacher_payload : Mapping[str, Any]
        The teacher payload value.
    candidate : Mapping[str, Any]
        The candidate value.
    
    Returns
    -------
    list[dict[str, object]]
        The list of values.
    """
    
    teacher_context = teacher_payload.get("context_requirements")
    candidate_context = candidate.get("context_requirements")
    if not isinstance(teacher_context, Mapping) or not isinstance(candidate_context, Mapping):
        return []
    disagreements: list[dict[str, object]] = []
    for bucket, severity in (("required", "high"), ("missing_required", "high"), ("recommended", "medium"), ("missing_recommended", "medium")):
        teacher_items = set(_as_string_sequence(teacher_context.get(bucket)))
        candidate_items = set(_as_string_sequence(candidate_context.get(bucket)))
        missing = sorted(teacher_items - candidate_items)
        if missing:
            disagreements.append(_disagreement(
                field=f"context_requirements.{bucket}",
                teacher_value=sorted(teacher_items),
                candidate_value=sorted(candidate_items),
                severity=severity,
                impact="candidate missed teacher context requirement evidence",
                recommendation="review context mismatch before using candidate evidence",
                missing_items=missing,
            ))
    return disagreements


def _risk_severity_disagreement(teacher_payload: Mapping[str, Any], candidate: Mapping[str, Any]) -> list[dict[str, object]]:
    """Support risk severity disagreement behavior.
    
    Parameters
    ----------
    teacher_payload : Mapping[str, Any]
        The teacher payload value.
    candidate : Mapping[str, Any]
        The candidate value.
    
    Returns
    -------
    list[dict[str, object]]
        The list of values.
    """
    
    teacher_risk = teacher_payload.get("risk_assessment")
    candidate_risk = candidate.get("risk_assessment")
    if not isinstance(teacher_risk, Mapping) or not isinstance(candidate_risk, Mapping):
        return []
    teacher_sev = str(teacher_risk.get("severity", "none"))
    candidate_sev = str(candidate_risk.get("severity", "none"))
    if teacher_sev == candidate_sev:
        return []
    teacher_rank = SEVERITY_ORDER.get(teacher_sev, 0)
    candidate_rank = SEVERITY_ORDER.get(candidate_sev, 0)
    if teacher_rank >= 4 and candidate_rank <= 2:
        severity = "critical"
    elif candidate_rank < teacher_rank:
        severity = "high"
    else:
        severity = "low"
    return [_disagreement(
        field="risk_assessment.severity",
        teacher_value=teacher_sev,
        candidate_value=candidate_sev,
        severity=severity,
        impact="candidate risk severity differs from teacher draft evidence",
        recommendation="review severity mismatch before promotion decisions",
    )]


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


def _field_severity(field: str, teacher_value: object, candidate_value: object, teacher_payload: Mapping[str, Any], candidate: Mapping[str, Any]) -> str:
    """Support field severity behavior.
    
    Parameters
    ----------
    field : str
        The field value.
    teacher_value : object
        The teacher value value.
    candidate_value : object
        The candidate value value.
    teacher_payload : Mapping[str, Any]
        The teacher payload value.
    candidate : Mapping[str, Any]
        The candidate value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if field == "authority_statement":
        return "critical"
    if field == "advisory_proceed_recommendation":
        candidate_text = str(candidate_value)
        teacher_text = str(teacher_value)
        if candidate_text in UNSAFE_PROCEED_VALUES:
            return "critical"
        if teacher_text in {"NO", "ABSTAIN", "UNKNOWN"} and candidate_text != teacher_text:
            return "high"
        return "medium"
    if field in {"governance_domain", "path_recommendation"}:
        if str(teacher_payload.get("governance_domain")) in GOVERNED_DOMAINS or str(candidate.get("governance_domain")) in GOVERNED_DOMAINS:
            return "high"
        return "medium"
    if field == "requires_human_confirmation":
        if str(teacher_value) == "true" and str(candidate_value) != "true":
            return "critical"
        return "medium"
    return "medium"


def _field_impact(field: str) -> str:
    """Support field impact behavior.
    
    Parameters
    ----------
    field : str
        The field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    impacts = {
        "governance_domain": "candidate may classify the governed domain differently from teacher draft evidence",
        "path_recommendation": "candidate may choose the wrong Fast Path or Routed Work posture",
        "advisory_proceed_recommendation": "candidate may give an unsafe or mismatched proceed recommendation",
        "requires_human_confirmation": "candidate may miss a required human-confirmation gate",
        "authority_statement": "candidate may violate advisory-only authority boundary",
    }
    return impacts.get(field, "candidate differs from teacher draft evidence")


def _field_recommendation(field: str) -> str:
    """Support field recommendation behavior.
    
    Parameters
    ----------
    field : str
        The field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if field in {"authority_statement", "advisory_proceed_recommendation", "requires_human_confirmation"}:
        return "block promotion and queue human review"
    return "queue human review before using candidate evidence"


def _teacher_payload(teacher_answer: Mapping[str, Any] | object) -> object:
    """Support teacher payload behavior.
    
    Parameters
    ----------
    teacher_answer : Mapping[str, Any] | object
        The teacher answer value.
    
    Returns
    -------
    object
        The object result.
    """
    
    if not isinstance(teacher_answer, Mapping):
        return None
    return teacher_answer.get("answer", teacher_answer)


def _teacher_review_status(teacher_answer: Mapping[str, Any] | object) -> str:
    """Support teacher review status behavior.
    
    Parameters
    ----------
    teacher_answer : Mapping[str, Any] | object
        The teacher answer value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not isinstance(teacher_answer, Mapping):
        return "missing"
    return str(teacher_answer.get("review_status", "draft"))


def _extract_case_id(teacher_answer: Mapping[str, Any] | object, candidate_answer: Mapping[str, Any] | object) -> str:
    """Support extract case id behavior.
    
    Parameters
    ----------
    teacher_answer : Mapping[str, Any] | object
        The teacher answer value.
    candidate_answer : Mapping[str, Any] | object
        The candidate answer value.
    
    Returns
    -------
    str
        The string result.
    """
    
    for value in (teacher_answer, candidate_answer):
        if isinstance(value, Mapping) and value.get("case_id"):
            return str(value.get("case_id"))
    return "case-not-recorded"


def _answer_ref(answer: Mapping[str, Any] | object, prefix: str) -> str:
    """Support answer ref behavior.
    
    Parameters
    ----------
    answer : Mapping[str, Any] | object
        The answer value.
    prefix : str
        The prefix value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not isinstance(answer, Mapping):
        return f"{prefix}:not-mapping"
    for key in ("answer_id", "candidate_id", "teacher_id"):
        if answer.get(key):
            return f"{prefix}:{answer.get(key)}"
    case_id = str(answer.get("case_id") or "case-not-recorded")
    return f"{prefix}:{case_id}"


def _candidate_domain(candidate: Mapping[str, Any]) -> str:
    """Support candidate domain behavior.
    
    Parameters
    ----------
    candidate : Mapping[str, Any]
        The candidate value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(candidate.get("governance_domain", "unknown"))


def _severity_from_guard(severity_result: Mapping[str, Any]) -> str:
    """Support severity from guard behavior.
    
    Parameters
    ----------
    severity_result : Mapping[str, Any]
        The severity result value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return P_SEVERITY_TO_DISAGREEMENT.get(str(severity_result.get("severity", "")), "medium")


def _aggregate_severity(disagreements: Sequence[Mapping[str, Any]]) -> str:
    """Support aggregate severity behavior.
    
    Parameters
    ----------
    disagreements : Sequence[Mapping[str, Any]]
        The disagreements value.
    
    Returns
    -------
    str
        The string result.
    """
    
    highest = 0
    for item in disagreements:
        highest = max(highest, SEVERITY_ORDER.get(str(item.get("severity", "none")), 0))
    for label, value in SEVERITY_ORDER.items():
        if value == highest:
            return label
    return "none"


def _disagreement(
    *,
    field: str,
    teacher_value: object,
    candidate_value: object,
    severity: str,
    impact: str,
    recommendation: str,
    missing_items: Sequence[str] = (),
) -> dict[str, object]:
    """Support disagreement behavior.
    
    Parameters
    ----------
    field : str
        The field value.
    teacher_value : object
        The teacher value value.
    candidate_value : object
        The candidate value value.
    severity : str
        The severity value.
    impact : str
        The impact value.
    recommendation : str
        The recommendation value.
    missing_items : Sequence[str], optional
        The optional missing items value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    data: dict[str, object] = {
        "field": field,
        "teacher_value": teacher_value,
        "candidate_value": candidate_value,
        "severity": severity,
        "impact": impact,
        "recommendation": recommendation,
    }
    if missing_items:
        data["missing_items"] = list(missing_items)
    return data


def _as_string_sequence(value: object) -> list[str]:
    """Support as string sequence behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return []
    return [str(item) for item in value]
