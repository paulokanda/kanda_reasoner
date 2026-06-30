# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/review_queue/active_review_queue.py
"""Pure in-memory active review queue for Adviser Candidate v0 reports.

The queue builder converts a caller-supplied M12-style evaluation report into a
prioritized human-review queue. It never discovers cases, persists queue items,
mutates gold data, registers runs, or grants router authority.

Authority boundary:
- adviser-offline only;
- pure over caller-supplied evaluation report mappings;
- standard library only;
- no file I/O;
- no case discovery;
- no source scanning;
- no prompt auto-loading;
- no artifact generation or persistence;
- no candidate-output persistence;
- no registry writer or scratch writer;
- no model, provider, network, embedding, vector, or dependency behavior;
- no runtime router authority.
"""

from __future__ import annotations


__all__ = ['ActiveReviewQueueItem', 'build_active_review_queue']
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

FEATURE_ID = "routing_signal_scorer_v3_adviser_active_review_queue_v1"
SCHEMA_VERSION = "3.54-adviser-active-review-queue"
AUTHORITY_STATEMENT = "advisory_only"
QUEUE_KIND = "in_memory_human_review_queue_only"
MAX_QUEUE_ITEMS = 500
UNSAFE_PROCEED_VALUES = frozenset({"YES", "YES_UNCONDITIONAL", "PROCEED", "AUTO_PROCEED", "APPROVE", "FINAL"})


@dataclass(frozen=True)
class ActiveReviewQueueItem:
    """Single human-review queue item."""

    queue_item_id: str
    case_id: str
    gold_case_id: str
    case_family: str
    review_priority: str
    reason_codes: tuple[str, ...]
    human_review_status: str
    required_human_decision: str
    promotion_gate: str
    may_promote_candidate: bool
    may_mutate_gold: bool
    candidate_evidence_status: str
    authority_statement: str = AUTHORITY_STATEMENT

    def to_dict(self) -> dict[str, object]:
        """Support to dict behavior.
        
        Returns
        -------
        dict[str, object]
            The mapped values.
        """
        
        return {
            "queue_item_id": self.queue_item_id,
            "case_id": self.case_id,
            "gold_case_id": self.gold_case_id,
            "case_family": self.case_family,
            "review_priority": self.review_priority,
            "reason_codes": list(self.reason_codes),
            "human_review_status": self.human_review_status,
            "required_human_decision": self.required_human_decision,
            "promotion_gate": self.promotion_gate,
            "may_promote_candidate": self.may_promote_candidate,
            "may_mutate_gold": self.may_mutate_gold,
            "candidate_evidence_status": self.candidate_evidence_status,
            "authority_statement": self.authority_statement,
        }


def build_active_review_queue(
    evaluation_report: Mapping[str, Any],
    *,
    queue_id: str = "m13-queue-not-recorded",
    max_items: int = MAX_QUEUE_ITEMS,
) -> dict[str, object]:
    """Build an in-memory human review queue from a supplied report.

    The function treats the supplied report as evidence only. It does not load
    cases, persist queue items, update registries, mutate gold records, or expose
    any runtime routing behavior.
    """

    if not isinstance(evaluation_report, Mapping):
        raise TypeError("evaluation_report must be a mapping")
    if max_items < 0 or max_items > MAX_QUEUE_ITEMS:
        raise ValueError(f"max_items must be between 0 and {MAX_QUEUE_ITEMS}")

    case_results = list(_as_mappings(evaluation_report.get("case_results")))
    queue_items: list[dict[str, object]] = []
    for result in case_results:
        if _needs_review(result):
            queue_items.append(_build_item(result, queue_id=queue_id).to_dict())

    queue_items.sort(key=_sort_key)
    if len(queue_items) > max_items:
        queue_items = queue_items[:max_items]

    aggregate = _aggregate(queue_items=queue_items, total_cases=len(case_results), source_report=evaluation_report)
    return {
        "feature_id": FEATURE_ID,
        "schema_version": SCHEMA_VERSION,
        "authority_statement": AUTHORITY_STATEMENT,
        "queue_kind": QUEUE_KIND,
        "queue_id": str(queue_id),
        "source_report_feature_id": str(evaluation_report.get("feature_id") or "unknown"),
        "source_report_run_id": str(evaluation_report.get("run_id") or "unknown"),
        "source_policy": "caller_supplied_evaluation_report_only_no_discovery",
        "output_policy": "in_memory_queue_only_no_persistence",
        "router_authority": "none",
        "gold_mutation": "forbidden",
        "candidate_promotion": "forbidden_without_later_governed_gate",
        "aggregate": aggregate,
        "queue_items": queue_items,
    }


def _as_mappings(value: object) -> Iterable[Mapping[str, Any]]:
    """Support as mappings behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    Iterable[Mapping[str, Any]]
        The sequence of values.
    """
    
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray, Mapping)):
        for item in value:
            if isinstance(item, Mapping):
                yield item


def _needs_review(result: Mapping[str, Any]) -> bool:
    """Support needs review behavior.
    
    Parameters
    ----------
    result : Mapping[str, Any]
        The result value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return any(
        (
            bool(result.get("review_required")),
            bool(result.get("promotion_blocker")),
            bool(result.get("critical_failure")),
            not bool(result.get("candidate_guard_ok", True)),
            not bool(result.get("resource_limits_ok", True)),
            str(result.get("candidate_advisory_proceed_recommendation") or "UNKNOWN") in UNSAFE_PROCEED_VALUES,
        )
    )


def _build_item(result: Mapping[str, Any], *, queue_id: str) -> ActiveReviewQueueItem:
    """Support build item behavior.
    
    Parameters
    ----------
    result : Mapping[str, Any]
        The result value.
    queue_id : str
        The queue id value.
    
    Returns
    -------
    ActiveReviewQueueItem
        The active review queue item result.
    """
    
    case_id = str(result.get("case_id") or result.get("gold_case_id") or "case-not-recorded")
    reasons = tuple(_reason_codes(result))
    priority = _priority(result, reasons)
    return ActiveReviewQueueItem(
        queue_item_id=f"{queue_id}:{case_id}",
        case_id=case_id,
        gold_case_id=str(result.get("gold_case_id") or case_id),
        case_family=str(result.get("case_family") or "unknown"),
        review_priority=priority,
        reason_codes=reasons,
        human_review_status="queued",
        required_human_decision="approve_override_or_reject",
        promotion_gate="blocked_until_human_review",
        may_promote_candidate=False,
        may_mutate_gold=False,
        candidate_evidence_status="advisory_evidence_only",
    )


def _reason_codes(result: Mapping[str, Any]) -> list[str]:
    """Support reason codes behavior.
    
    Parameters
    ----------
    result : Mapping[str, Any]
        The result value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    reasons: list[str] = []
    proceed = str(result.get("candidate_advisory_proceed_recommendation") or "UNKNOWN")
    severity = str(result.get("severity") or "P4_INFO")
    if proceed in UNSAFE_PROCEED_VALUES:
        reasons.append("unsafe_proceed_recommendation")
    if bool(result.get("critical_failure")) or severity.startswith("P0"):
        reasons.append("critical_failure")
    if not bool(result.get("candidate_guard_ok", True)):
        reasons.append("candidate_guard_failed")
    if not bool(result.get("resource_limits_ok", True)):
        reasons.append("resource_limits_failed")
    if bool(result.get("promotion_blocker")):
        reasons.append("promotion_blocker")
    if not bool(result.get("must_not_permit_action_alignment", True)):
        reasons.append("must_not_permit_action_alignment_failed")
    if not bool(result.get("path_match", True)):
        reasons.append("path_mismatch")
    if not bool(result.get("required_prompt_groups_match", True)):
        reasons.append("required_prompt_groups_mismatch")
    if not bool(result.get("risk_flag_overlap", True)):
        reasons.append("risk_flags_mismatch")
    if bool(result.get("review_required")) and not reasons:
        reasons.append("review_required_by_evaluation")
    return reasons or ["review_required"]


def _priority(result: Mapping[str, Any], reasons: tuple[str, ...]) -> str:
    """Support priority behavior.
    
    Parameters
    ----------
    result : Mapping[str, Any]
        The result value.
    reasons : tuple[str, ...]
        The reasons value.
    
    Returns
    -------
    str
        The string result.
    """
    
    severity = str(result.get("severity") or "P4_INFO")
    if "unsafe_proceed_recommendation" in reasons or "critical_failure" in reasons or severity.startswith("P0"):
        return "P0_CRITICAL_REVIEW"
    if "candidate_guard_failed" in reasons or "resource_limits_failed" in reasons or "promotion_blocker" in reasons:
        return "P1_HIGH_REVIEW"
    if any(reason.endswith("mismatch") or reason.endswith("failed") for reason in reasons):
        return "P2_STANDARD_REVIEW"
    return "P3_LOW_REVIEW"


def _sort_key(item: Mapping[str, Any]) -> tuple[int, str]:
    """Support sort key behavior.
    
    Parameters
    ----------
    item : Mapping[str, Any]
        The item value.
    
    Returns
    -------
    tuple[int, str]
        The tuple of values.
    """
    
    order = {
        "P0_CRITICAL_REVIEW": 0,
        "P1_HIGH_REVIEW": 1,
        "P2_STANDARD_REVIEW": 2,
        "P3_LOW_REVIEW": 3,
    }
    return (order.get(str(item.get("review_priority")), 9), str(item.get("case_id") or ""))


def _aggregate(*, queue_items: list[Mapping[str, Any]], total_cases: int, source_report: Mapping[str, Any]) -> dict[str, object]:
    """Support aggregate behavior.
    
    Parameters
    ----------
    queue_items : list[Mapping[str, Any]]
        The queue items value.
    total_cases : int
        The total cases value.
    source_report : Mapping[str, Any]
        The source report value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    return {
        "source_total_cases": total_cases,
        "queued_review_items": len(queue_items),
        "p0_items": _count_priority(queue_items, "P0_CRITICAL_REVIEW"),
        "p1_items": _count_priority(queue_items, "P1_HIGH_REVIEW"),
        "p2_items": _count_priority(queue_items, "P2_STANDARD_REVIEW"),
        "p3_items": _count_priority(queue_items, "P3_LOW_REVIEW"),
        "source_promotion_recommendation": str(_source_aggregate(source_report).get("promotion_recommendation") or "unknown"),
        "queue_recommendation": _queue_recommendation(queue_items=queue_items, total_cases=total_cases),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _source_aggregate(source_report: Mapping[str, Any]) -> Mapping[str, Any]:
    """Support source aggregate behavior.
    
    Parameters
    ----------
    source_report : Mapping[str, Any]
        The source report value.
    
    Returns
    -------
    Mapping[str, Any]
        The mapped values.
    """
    
    aggregate = source_report.get("aggregate")
    return aggregate if isinstance(aggregate, Mapping) else {}


def _queue_recommendation(*, queue_items: list[Mapping[str, Any]], total_cases: int) -> str:
    """Support queue recommendation behavior.
    
    Parameters
    ----------
    queue_items : list[Mapping[str, Any]]
        The queue items value.
    total_cases : int
        The total cases value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if total_cases == 0:
        return "blocked_no_cases_supplied"
    if any(str(item.get("review_priority")) == "P0_CRITICAL_REVIEW" for item in queue_items):
        return "blocked_p0_review_items_require_human_review"
    if queue_items:
        return "review_queue_open_human_review_required"
    return "no_active_review_items_continue_to_next_governed_offline_gate"


def _count_priority(items: list[Mapping[str, Any]], priority: str) -> int:
    """Support count priority behavior.
    
    Parameters
    ----------
    items : list[Mapping[str, Any]]
        The item values.
    priority : str
        The priority value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return sum(1 for item in items if item.get("review_priority") == priority)
