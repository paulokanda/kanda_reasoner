# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/gold_set_expansion_plan.py
"""Pure in-memory seed-gold expansion planning for Adviser.

M15 converts caller-supplied summaries into a deterministic expansion plan for
future human-reviewed seed-gold growth. It deliberately does not create new gold
cases, persist plan records, mutate current gold data, run candidates, scan
sources, load prompts, or grant router authority.

Authority boundary:
- adviser-offline only;
- pure over caller-supplied mappings;
- standard library only;
- no file I/O;
- no case discovery;
- no source scanning;
- no prompt loading;
- no artifact generation or persistence;
- no candidate-output persistence;
- no scratch writer, registry writer, or run-record writer;
- no gold mutation;
- no model, provider, network, embedding, vector, or dependency behavior;
- no runtime router authority.
"""

from __future__ import annotations


__all__ = [
    'assert_gold_set_expansion_plan_valid',
    'build_gold_set_expansion_plan',
    'validate_gold_set_expansion_plan',
]
from collections.abc import Mapping
from typing import Any

from ..registry.candidate_registry import AUTHORITY_STATEMENT
from ..registry.hash_utils import hash_record_without_field

FEATURE_ID = "routing_signal_scorer_v3_adviser_gold_set_expansion_plan_v1"
SCHEMA_VERSION = "3.56-adviser-gold-set-expansion-plan"
PLAN_KIND = "in_memory_gold_set_expansion_plan_only"
GOLD_MUTATION_POLICY = "forbidden_until_future_reviewed_gold_patch"
PROMOTION_POLICY = "blocked_until_m16_promotion_criteria_gate"
DEFAULT_TARGET_FAMILIES = (
    "adversarial_bypass",
    "freeze_workflow",
    "patch_delivery",
    "box_boundary",
    "startup_delivery",
    "prompt_library",
    "routing_signal_scorer",
    "ambiguous",
    "false_positive",
    "out_of_scope",
)


def build_gold_set_expansion_plan(
    *,
    current_gold_summary: Mapping[str, Any],
    evaluation_report: Mapping[str, Any] | None = None,
    review_queue: Mapping[str, Any] | None = None,
    registry_record: Mapping[str, Any] | None = None,
    expansion_policy: Mapping[str, Any] | None = None,
    plan_id: str = "gold-expansion-plan-not-persisted",
    planned_by: str = "human-review-pending",
) -> dict[str, object]:
    """Build a deterministic in-memory gold expansion plan.

    All source data is supplied by the caller. The function does not discover
    cases, read/write files, approve records, create gold cases, mutate current
    gold data, persist plan records, or influence runtime routing.
    """

    if not isinstance(current_gold_summary, Mapping):
        raise TypeError("current_gold_summary must be a mapping")
    if evaluation_report is not None and not isinstance(evaluation_report, Mapping):
        raise TypeError("evaluation_report must be a mapping when supplied")
    if review_queue is not None and not isinstance(review_queue, Mapping):
        raise TypeError("review_queue must be a mapping when supplied")
    if registry_record is not None and not isinstance(registry_record, Mapping):
        raise TypeError("registry_record must be a mapping when supplied")
    if expansion_policy is not None and not isinstance(expansion_policy, Mapping):
        raise TypeError("expansion_policy must be a mapping when supplied")

    evaluation_report = evaluation_report or {}
    review_queue = review_queue or {}
    registry_record = registry_record or {}
    expansion_policy = expansion_policy or {}

    gold_summary = _gold_summary(current_gold_summary)
    evaluation_summary = _evaluation_summary(evaluation_report)
    queue_summary = _queue_summary(review_queue)
    registry_summary = _registry_summary(registry_record)
    target_families = _target_families(expansion_policy)
    per_family_target = _positive_int(expansion_policy.get("target_new_cases_per_family"), default=5)
    minimum_total_cases = _positive_int(expansion_policy.get("minimum_total_cases_after_future_expansion"), default=100)

    plan_items = [
        _plan_item(
            family=family,
            target_new_cases=per_family_target,
            gold_summary=gold_summary,
            evaluation_summary=evaluation_summary,
            queue_summary=queue_summary,
        )
        for family in target_families
    ]
    blockers = _blockers(
        gold_summary=gold_summary,
        evaluation_summary=evaluation_summary,
        queue_summary=queue_summary,
        registry_summary=registry_summary,
        plan_items=plan_items,
    )

    planned_new_cases = sum(int(item["target_new_cases"]) for item in plan_items)
    record: dict[str, object] = {
        "feature_id": FEATURE_ID,
        "schema_version": SCHEMA_VERSION,
        "authority_statement": AUTHORITY_STATEMENT,
        "plan_kind": PLAN_KIND,
        "plan_id": str(plan_id),
        "planned_by": str(planned_by),
        "source_policy": "caller_supplied_summaries_only_no_discovery",
        "output_policy": "in_memory_plan_only_no_persistence",
        "gold_mutation_policy": GOLD_MUTATION_POLICY,
        "promotion_policy": PROMOTION_POLICY,
        "router_authority": "none",
        "runtime_integration": "forbidden",
        "may_add_gold_cases": False,
        "may_mutate_gold": False,
        "may_promote_candidate": False,
        "may_persist_plan": False,
        "may_record_registry": False,
        "may_record_run_record": False,
        "human_review_status": "expansion_plan_requires_future_human_review",
        "plan_status": "planned_only_promotion_blocked_no_gold_mutation",
        "promotion_blocked": True,
        "promotion_blockers": blockers,
        "current_gold_summary": gold_summary,
        "evaluation_summary": evaluation_summary,
        "review_queue_summary": queue_summary,
        "candidate_registry_summary": registry_summary,
        "expansion_targets": {
            "target_families": list(target_families),
            "target_new_cases_per_family": per_family_target,
            "minimum_total_cases_after_future_expansion": minimum_total_cases,
            "planned_new_case_count": planned_new_cases,
            "future_total_case_goal": max(int(gold_summary["current_case_count"]) + planned_new_cases, minimum_total_cases),
            "requires_separate_reviewed_gold_patch": True,
        },
        "plan_items": plan_items,
    }
    record["plan_hash"] = hash_record_without_field(record, "plan_hash")
    return record


def validate_gold_set_expansion_plan(plan: Mapping[str, Any]) -> dict[str, object]:
    """Validate a supplied gold expansion plan."""

    errors: list[str] = []
    if not isinstance(plan, Mapping):
        return {"ok": False, "errors": ["plan must be a mapping"]}

    for field in (
        "feature_id",
        "schema_version",
        "authority_statement",
        "plan_kind",
        "plan_id",
        "gold_mutation_policy",
        "promotion_policy",
        "router_authority",
        "may_add_gold_cases",
        "may_mutate_gold",
        "may_promote_candidate",
        "may_persist_plan",
        "plan_status",
        "promotion_blocked",
        "promotion_blockers",
        "expansion_targets",
        "plan_items",
        "plan_hash",
    ):
        if field not in plan:
            errors.append(f"missing {field}")

    if plan.get("feature_id") != FEATURE_ID:
        errors.append("feature_id mismatch")
    if plan.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if plan.get("authority_statement") != AUTHORITY_STATEMENT:
        errors.append("authority_statement must be advisory_only")
    if plan.get("plan_kind") != PLAN_KIND:
        errors.append("plan_kind mismatch")
    if plan.get("gold_mutation_policy") != GOLD_MUTATION_POLICY:
        errors.append("gold_mutation_policy mismatch")
    if plan.get("promotion_policy") != PROMOTION_POLICY:
        errors.append("promotion_policy mismatch")
    if plan.get("router_authority") != "none":
        errors.append("router_authority must be none")

    for flag in (
        "may_add_gold_cases",
        "may_mutate_gold",
        "may_promote_candidate",
        "may_persist_plan",
        "may_record_registry",
        "may_record_run_record",
    ):
        if plan.get(flag) is not False:
            errors.append(f"{flag} must be false")

    if plan.get("promotion_blocked") is not True:
        errors.append("promotion_blocked must be true")

    items = plan.get("plan_items")
    if not isinstance(items, list) or not items:
        errors.append("plan_items must be a non-empty list")
    elif any(not _valid_plan_item(item) for item in items):
        errors.append("all plan_items must remain planned-only and human-review-required")

    targets = plan.get("expansion_targets")
    if not isinstance(targets, Mapping):
        errors.append("expansion_targets must be a mapping")
    elif targets.get("requires_separate_reviewed_gold_patch") is not True:
        errors.append("expansion_targets must require a separate reviewed gold patch")

    if "plan_hash" in plan:
        expected = hash_record_without_field(plan, "plan_hash")
        if plan.get("plan_hash") != expected:
            errors.append("plan_hash mismatch")

    return {"ok": not errors, "errors": errors}


def assert_gold_set_expansion_plan_valid(plan: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return plan when valid; raise ValueError otherwise."""

    result = validate_gold_set_expansion_plan(plan)
    if not result["ok"]:
        raise ValueError("gold set expansion plan invalid: " + "; ".join(result["errors"]))
    return plan


def _gold_summary(summary: Mapping[str, Any]) -> dict[str, object]:
    """Support gold summary behavior.
    
    Parameters
    ----------
    summary : Mapping[str, Any]
        The summary value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    case_count = _positive_int(summary.get("case_count") or summary.get("gold_case_count") or summary.get("current_case_count"), default=0, allow_zero=True)
    version = str(summary.get("gold_set_version") or summary.get("version") or "unknown")
    families = summary.get("families")
    family_counts = families if isinstance(families, Mapping) else summary.get("family_counts")
    if not isinstance(family_counts, Mapping):
        family_counts = {}
    return {
        "gold_set_version": version,
        "current_case_count": case_count,
        "family_counts": {str(key): _positive_int(value, default=0, allow_zero=True) for key, value in family_counts.items()},
        "authority_statement": AUTHORITY_STATEMENT,
        "gold_mutation": "not_performed",
    }


def _evaluation_summary(report: Mapping[str, Any]) -> dict[str, object]:
    """Support evaluation summary behavior.
    
    Parameters
    ----------
    report : Mapping[str, Any]
        The report value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    aggregate = report.get("aggregate")
    if not isinstance(aggregate, Mapping):
        aggregate = {}
    case_results = report.get("case_results")
    case_count = len(case_results) if isinstance(case_results, list) else _positive_int(aggregate.get("total_cases") or aggregate.get("source_total_cases"), default=0, allow_zero=True)
    return {
        "source_report_feature_id": str(report.get("feature_id") or "unknown"),
        "cases_evaluated": case_count,
        "mismatches": _positive_int(aggregate.get("mismatches"), default=0, allow_zero=True),
        "guard_failures": _positive_int(aggregate.get("guard_failures"), default=0, allow_zero=True),
        "resource_failures": _positive_int(aggregate.get("resource_failures"), default=0, allow_zero=True),
        "critical_failures": _positive_int(aggregate.get("critical_failures"), default=0, allow_zero=True),
        "promotion_recommendation": str(aggregate.get("promotion_recommendation") or "unknown"),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _queue_summary(queue: Mapping[str, Any]) -> dict[str, object]:
    """Support queue summary behavior.
    
    Parameters
    ----------
    queue : Mapping[str, Any]
        The queue value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    aggregate = queue.get("aggregate")
    if not isinstance(aggregate, Mapping):
        aggregate = {}
    queue_items = queue.get("queue_items")
    queued = len(queue_items) if isinstance(queue_items, list) else _positive_int(aggregate.get("queued_review_items"), default=0, allow_zero=True)
    return {
        "source_queue_feature_id": str(queue.get("feature_id") or "unknown"),
        "queued_review_items": queued,
        "p0_items": _positive_int(aggregate.get("p0_items"), default=0, allow_zero=True),
        "p1_items": _positive_int(aggregate.get("p1_items"), default=0, allow_zero=True),
        "queue_recommendation": str(aggregate.get("queue_recommendation") or "unknown"),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _registry_summary(registry_record: Mapping[str, Any]) -> dict[str, object]:
    """Support registry summary behavior.
    
    Parameters
    ----------
    registry_record : Mapping[str, Any]
        The registry record value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    blockers = registry_record.get("promotion_blockers")
    if not isinstance(blockers, list):
        blockers = []
    return {
        "source_registry_feature_id": str(registry_record.get("feature_id") or "unknown"),
        "candidate_id": str(registry_record.get("candidate_id") or "unknown"),
        "candidate_version": str(registry_record.get("candidate_version") or "unknown"),
        "promotion_blocked": registry_record.get("promotion_blocked") is True,
        "promotion_blockers": [str(item) for item in blockers],
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _target_families(policy: Mapping[str, Any]) -> tuple[str, ...]:
    """Support target families behavior.
    
    Parameters
    ----------
    policy : Mapping[str, Any]
        The policy value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    raw = policy.get("target_families")
    if isinstance(raw, (list, tuple)):
        values = tuple(str(item).strip() for item in raw if str(item).strip())
        if values:
            return values
    return DEFAULT_TARGET_FAMILIES


def _plan_item(
    *,
    family: str,
    target_new_cases: int,
    gold_summary: Mapping[str, Any],
    evaluation_summary: Mapping[str, Any],
    queue_summary: Mapping[str, Any],
) -> dict[str, object]:
    """Support plan item behavior.
    
    Parameters
    ----------
    family : str
        The family value.
    target_new_cases : int
        The target new cases value.
    gold_summary : Mapping[str, Any]
        The gold summary value.
    evaluation_summary : Mapping[str, Any]
        The evaluation summary value.
    queue_summary : Mapping[str, Any]
        The queue summary value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    family_counts = gold_summary.get("family_counts")
    current_family_count = 0
    if isinstance(family_counts, Mapping):
        current_family_count = _positive_int(family_counts.get(family), default=0, allow_zero=True)
    reasons = ["balance_seed_gold_family_coverage"]
    if int(evaluation_summary.get("mismatches") or 0) > 0:
        reasons.append("candidate_gold_mismatches_need_reviewed_examples")
    if int(queue_summary.get("queued_review_items") or 0) > 0:
        reasons.append("active_review_queue_has_pending_items")
    if current_family_count == 0:
        reasons.append("family_currently_missing_or_unreported")
    return {
        "family": str(family),
        "current_family_case_count": current_family_count,
        "target_new_cases": int(target_new_cases),
        "future_case_source": "future_human_reviewed_records_only",
        "review_status": "planned_requires_human_review",
        "may_create_gold_case_now": False,
        "may_mutate_gold_now": False,
        "requires_future_governed_patch": True,
        "rationale_codes": reasons,
    }


def _blockers(
    *,
    gold_summary: Mapping[str, Any],
    evaluation_summary: Mapping[str, Any],
    queue_summary: Mapping[str, Any],
    registry_summary: Mapping[str, Any],
    plan_items: list[Mapping[str, Any]],
) -> list[str]:
    """Support blockers behavior.
    
    Parameters
    ----------
    gold_summary : Mapping[str, Any]
        The gold summary value.
    evaluation_summary : Mapping[str, Any]
        The evaluation summary value.
    queue_summary : Mapping[str, Any]
        The queue summary value.
    registry_summary : Mapping[str, Any]
        The registry summary value.
    plan_items : list[Mapping[str, Any]]
        The plan items value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    blockers = ["future_human_review_required", "future_governed_gold_patch_required", "m16_promotion_gate_not_yet_run"]
    if int(gold_summary.get("current_case_count") or 0) == 0:
        blockers.append("current_gold_summary_empty_or_unreported")
    if int(evaluation_summary.get("mismatches") or 0) > 0:
        blockers.append("candidate_gold_mismatches_require_review")
    if int(evaluation_summary.get("critical_failures") or 0) > 0:
        blockers.append("critical_failures_present")
    if int(evaluation_summary.get("guard_failures") or 0) > 0:
        blockers.append("guard_failures_present")
    if int(evaluation_summary.get("resource_failures") or 0) > 0:
        blockers.append("resource_failures_present")
    if int(queue_summary.get("queued_review_items") or 0) > 0:
        blockers.append("active_review_queue_not_empty")
    if registry_summary.get("promotion_blocked") is True:
        blockers.append("candidate_registry_promotion_blocked")
    if any(item.get("requires_future_governed_patch") is True for item in plan_items):
        blockers.append("planned_items_not_gold_cases")
    return sorted(set(blockers))


def _valid_plan_item(item: object) -> bool:
    """Support valid plan item behavior.
    
    Parameters
    ----------
    item : object
        The item value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        isinstance(item, Mapping)
        and bool(str(item.get("family") or ""))
        and item.get("review_status") == "planned_requires_human_review"
        and item.get("may_create_gold_case_now") is False
        and item.get("may_mutate_gold_now") is False
        and item.get("requires_future_governed_patch") is True
    )


def _positive_int(value: object, *, default: int, allow_zero: bool = False) -> int:
    """Support positive int behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    default : int
        The default value.
    allow_zero : bool, optional
        The optional allow zero value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    try:
        number = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        number = int(default)
    floor = 0 if allow_zero else 1
    return max(floor, number)
