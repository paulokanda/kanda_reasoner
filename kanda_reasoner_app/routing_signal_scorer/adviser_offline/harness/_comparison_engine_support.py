# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/_comparison_engine_support.py
"""Pure normalization and evidence support for the offline comparison engine."""

from __future__ import annotations

from typing import Mapping, Sequence

__all__ = ()

FEATURE_ID = "routing_signal_scorer_v3_adviser_pure_comparison_harness_v1"
SCHEMA_VERSION = "3.44-adviser-pure-comparison-harness"
AUTHORITY_STATEMENT = "advisory_only"
TEACHER_REVIEWED_STATUSES = frozenset({"human_reviewed", "approved_as_gold"})
UNSAFE_PROCEED_VALUES = frozenset(
    {"YES", "YES_UNCONDITIONAL", "PROCEED", "AUTO_PROCEED", "APPROVE", "FINAL"}
)
GOVERNED_DOMAINS = frozenset(
    {"freeze", "patch", "box", "shield", "startup", "prompt_library", "authority"}
)
SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
P_SEVERITY_TO_DISAGREEMENT = {
    "P0_CRITICAL": "critical",
    "P1_HIGH": "high",
    "P2_MEDIUM": "medium",
    "P3_LOW": "low",
    "P4_INFO": "none",
}


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


