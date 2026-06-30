"""Pure in-memory Adviser promotion criteria gate.

M16 is the final Adviser-phase gate. It evaluates caller-supplied summaries from
M12/M13/M14/M15 and returns a deterministic advisory gate report. The report may
mark a candidate as blocked or eligible for a future separately governed
shadow-mode design review, but it never promotes a candidate, writes state,
mutates gold, imports runtime router behavior, or grants router authority.

Authority boundary:
- adviser-offline only;
- pure over caller-supplied mappings;
- standard library only;
- no file I/O;
- no case discovery;
- no source scanning;
- no prompt loading;
- no artifact generation or persistence;
- no registry writer, run-record writer, or gate writer;
- no candidate-output persistence;
- no scratch writer;
- no gold mutation;
- no actual candidate promotion;
- no model, provider, network, embedding, vector, or dependency behavior;
- no runtime router authority.
"""

from __future__ import annotations


__all__ = [
    'assert_promotion_criteria_gate_report_valid',
    'build_promotion_criteria_gate_report',
    'validate_promotion_criteria_gate_report',
]
from collections.abc import Mapping
from typing import Any

from ..registry.candidate_registry import AUTHORITY_STATEMENT
from ..registry.hash_utils import hash_record_without_field

FEATURE_ID = "routing_signal_scorer_v3_adviser_promotion_criteria_gate_v1"
SCHEMA_VERSION = "3.57-adviser-promotion-criteria-gate"
GATE_KIND = "in_memory_promotion_criteria_gate_only"
OUTPUT_POLICY = "advisory_gate_report_only_no_persistence_no_runtime_promotion"
RUNTIME_POLICY = "runtime_integration_forbidden"
DEFAULT_MINIMUM_CASES = 50
DEFAULT_REQUIRED_GOLD_VERSION = "seed_gold_set_v1"
ELIGIBLE_REVIEW_ONLY = "eligible_for_future_shadow_mode_design_review_only"
BLOCKED = "blocked_human_review_or_evidence_required"


def build_promotion_criteria_gate_report(
    *,
    candidate_registry_record: Mapping[str, Any],
    evaluation_report: Mapping[str, Any] | None = None,
    review_queue: Mapping[str, Any] | None = None,
    gold_expansion_plan: Mapping[str, Any] | None = None,
    gate_policy: Mapping[str, Any] | None = None,
    gate_id: str = "promotion-criteria-gate-not-persisted",
    evaluated_by: str = "human-review-pending",
) -> dict[str, object]:
    """Build a deterministic in-memory promotion criteria gate report.

    All data is supplied by the caller. This function does not discover cases,
    read/write files, mutate current gold, persist records, execute candidates,
    modify registries, or expose runtime routing behavior.
    """

    if not isinstance(candidate_registry_record, Mapping):
        raise TypeError("candidate_registry_record must be a mapping")
    if evaluation_report is not None and not isinstance(evaluation_report, Mapping):
        raise TypeError("evaluation_report must be a mapping when supplied")
    if review_queue is not None and not isinstance(review_queue, Mapping):
        raise TypeError("review_queue must be a mapping when supplied")
    if gold_expansion_plan is not None and not isinstance(gold_expansion_plan, Mapping):
        raise TypeError("gold_expansion_plan must be a mapping when supplied")
    if gate_policy is not None and not isinstance(gate_policy, Mapping):
        raise TypeError("gate_policy must be a mapping when supplied")

    evaluation_report = evaluation_report or {}
    review_queue = review_queue or {}
    gold_expansion_plan = gold_expansion_plan or {}
    gate_policy = gate_policy or {}

    policy = _policy_summary(gate_policy)
    registry_summary = _registry_summary(candidate_registry_record)
    evaluation_summary = _evaluation_summary(evaluation_report, candidate_registry_record)
    queue_summary = _queue_summary(review_queue, candidate_registry_record)
    expansion_summary = _expansion_summary(gold_expansion_plan)
    blockers = _gate_blockers(
        policy=policy,
        registry_summary=registry_summary,
        evaluation_summary=evaluation_summary,
        queue_summary=queue_summary,
        expansion_summary=expansion_summary,
    )
    gate_decision = ELIGIBLE_REVIEW_ONLY if not blockers else BLOCKED

    report: dict[str, object] = {
        "feature_id": FEATURE_ID,
        "schema_version": SCHEMA_VERSION,
        "authority_statement": AUTHORITY_STATEMENT,
        "gate_kind": GATE_KIND,
        "gate_id": str(gate_id),
        "evaluated_by": str(evaluated_by),
        "source_policy": "caller_supplied_registry_evaluation_queue_expansion_only_no_discovery",
        "output_policy": OUTPUT_POLICY,
        "runtime_policy": RUNTIME_POLICY,
        "router_authority": "none",
        "runtime_integration": "forbidden",
        "candidate_promotion": "not_performed_by_this_gate",
        "shadow_mode_authority": "not_granted_requires_future_governed_design",
        "may_promote_candidate": False,
        "may_enable_shadow_mode": False,
        "may_mutate_gold": False,
        "may_persist_gate": False,
        "may_record_registry": False,
        "may_record_run_record": False,
        "human_review_status": "gate_report_requires_human_review_before_any_future_phase",
        "gate_decision": gate_decision,
        "promotion_blocked": True,
        "promotion_blockers": blockers or ["future_shadow_mode_design_review_required"],
        "next_allowed_step": _next_allowed_step(gate_decision),
        "policy_summary": policy,
        "candidate_registry_summary": registry_summary,
        "evaluation_summary": evaluation_summary,
        "review_queue_summary": queue_summary,
        "gold_expansion_plan_summary": expansion_summary,
        "closure_statement": "adviser_phase_gate_complete_no_runtime_enablement",
    }
    report["gate_hash"] = hash_record_without_field(report, "gate_hash")
    return report


def validate_promotion_criteria_gate_report(report: Mapping[str, Any]) -> dict[str, object]:
    """Validate a supplied promotion criteria gate report."""

    errors: list[str] = []
    if not isinstance(report, Mapping):
        return {"ok": False, "errors": ["report must be a mapping"]}

    for field in (
        "feature_id",
        "schema_version",
        "authority_statement",
        "gate_kind",
        "gate_id",
        "output_policy",
        "runtime_policy",
        "router_authority",
        "candidate_promotion",
        "shadow_mode_authority",
        "may_promote_candidate",
        "may_enable_shadow_mode",
        "may_mutate_gold",
        "may_persist_gate",
        "may_record_registry",
        "may_record_run_record",
        "gate_decision",
        "promotion_blocked",
        "promotion_blockers",
        "next_allowed_step",
        "gate_hash",
    ):
        if field not in report:
            errors.append(f"missing {field}")

    if report.get("feature_id") != FEATURE_ID:
        errors.append("feature_id mismatch")
    if report.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if report.get("authority_statement") != AUTHORITY_STATEMENT:
        errors.append("authority_statement must be advisory_only")
    if report.get("gate_kind") != GATE_KIND:
        errors.append("gate_kind mismatch")
    if report.get("router_authority") != "none":
        errors.append("router_authority must be none")
    if report.get("runtime_integration") != "forbidden":
        errors.append("runtime_integration must be forbidden")
    if report.get("candidate_promotion") != "not_performed_by_this_gate":
        errors.append("candidate_promotion must not be performed by this gate")
    if report.get("shadow_mode_authority") != "not_granted_requires_future_governed_design":
        errors.append("shadow_mode_authority must not be granted")

    for flag in (
        "may_promote_candidate",
        "may_enable_shadow_mode",
        "may_mutate_gold",
        "may_persist_gate",
        "may_record_registry",
        "may_record_run_record",
    ):
        if report.get(flag) is not False:
            errors.append(f"{flag} must be false")

    if report.get("promotion_blocked") is not True:
        errors.append("promotion_blocked must remain true because this gate does not promote")

    decision = report.get("gate_decision")
    if decision not in (BLOCKED, ELIGIBLE_REVIEW_ONLY):
        errors.append("gate_decision mismatch")
    blockers = report.get("promotion_blockers")
    if not isinstance(blockers, list) or not blockers:
        errors.append("promotion_blockers must be a non-empty list")
    elif decision == ELIGIBLE_REVIEW_ONLY and blockers != ["future_shadow_mode_design_review_required"]:
        errors.append("eligible reports must only allow a future shadow-mode design review")

    if report.get("next_allowed_step") not in (
        "future_governed_shadow_mode_design_review_only",
        "resolve_blockers_with_human_review_before_future_phase",
    ):
        errors.append("next_allowed_step mismatch")

    if "gate_hash" in report:
        expected = hash_record_without_field(report, "gate_hash")
        if report.get("gate_hash") != expected:
            errors.append("gate_hash mismatch")

    return {"ok": not errors, "errors": errors}


def assert_promotion_criteria_gate_report_valid(report: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return report when valid; raise ValueError otherwise."""

    result = validate_promotion_criteria_gate_report(report)
    if not result["ok"]:
        raise ValueError("promotion criteria gate report invalid: " + "; ".join(result["errors"]))
    return report


def _policy_summary(policy: Mapping[str, Any]) -> dict[str, object]:
    return {
        "minimum_cases": _nonnegative_int(policy.get("minimum_cases"), default=DEFAULT_MINIMUM_CASES),
        "maximum_mismatches": _nonnegative_int(policy.get("maximum_mismatches"), default=0),
        "maximum_guard_failures": _nonnegative_int(policy.get("maximum_guard_failures"), default=0),
        "maximum_resource_failures": _nonnegative_int(policy.get("maximum_resource_failures"), default=0),
        "maximum_critical_failures": _nonnegative_int(policy.get("maximum_critical_failures"), default=0),
        "maximum_p0_review_items": _nonnegative_int(policy.get("maximum_p0_review_items"), default=0),
        "maximum_p1_review_items": _nonnegative_int(policy.get("maximum_p1_review_items"), default=0),
        "maximum_queued_review_items": _nonnegative_int(policy.get("maximum_queued_review_items"), default=0),
        "required_gold_set_version": str(policy.get("required_gold_set_version") or DEFAULT_REQUIRED_GOLD_VERSION),
        "require_registry_record_promotion_blocked": bool(policy.get("require_registry_record_promotion_blocked", True)),
        "require_gold_expansion_plan_reviewed_separately": bool(policy.get("require_gold_expansion_plan_reviewed_separately", True)),
    }


def _registry_summary(record: Mapping[str, Any]) -> dict[str, object]:
    return {
        "source_registry_feature_id": str(record.get("feature_id") or "unknown"),
        "registry_record_id": str(record.get("registry_record_id") or "unknown"),
        "candidate_id": str(record.get("candidate_id") or "unknown"),
        "candidate_version": str(record.get("candidate_version") or "unknown"),
        "candidate_code_hash_present": bool(str(record.get("candidate_code_hash") or "").strip()),
        "registry_status": str(record.get("registry_status") or "unknown"),
        "promotion_blocked": bool(record.get("promotion_blocked", True)),
        "router_authority": str(record.get("router_authority") or "unknown"),
        "may_promote_candidate": bool(record.get("may_promote_candidate", False)),
        "authority_statement": str(record.get("authority_statement") or "unknown"),
    }


def _evaluation_summary(report: Mapping[str, Any], registry_record: Mapping[str, Any]) -> dict[str, object]:
    aggregate = report.get("aggregate")
    if not isinstance(aggregate, Mapping):
        aggregate = {}
    registry_eval = registry_record.get("evaluation_summary")
    if not isinstance(registry_eval, Mapping):
        registry_eval = {}
    case_results = report.get("case_results")
    case_count = len(case_results) if isinstance(case_results, list) else _nonnegative_int(aggregate.get("total_cases") or registry_eval.get("cases_evaluated"), default=0)
    return {
        "source_report_feature_id": str(report.get("feature_id") or registry_eval.get("source_report_feature_id") or "unknown"),
        "cases_evaluated": case_count,
        "exact_matches": _nonnegative_int(aggregate.get("exact_matches") or registry_eval.get("exact_matches"), default=0),
        "mismatches": _nonnegative_int(aggregate.get("mismatches") or registry_eval.get("mismatches"), default=0),
        "guard_failures": _nonnegative_int(aggregate.get("guard_failures") or registry_eval.get("guard_failures"), default=0),
        "resource_failures": _nonnegative_int(aggregate.get("resource_failures") or registry_eval.get("resource_failures"), default=0),
        "critical_failures": _nonnegative_int(aggregate.get("critical_failures") or registry_eval.get("critical_failures"), default=0),
        "promotion_recommendation": str(aggregate.get("promotion_recommendation") or registry_eval.get("promotion_recommendation") or "unknown"),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _queue_summary(queue: Mapping[str, Any], registry_record: Mapping[str, Any]) -> dict[str, object]:
    aggregate = queue.get("aggregate")
    if not isinstance(aggregate, Mapping):
        aggregate = {}
    registry_queue = registry_record.get("review_queue_summary")
    if not isinstance(registry_queue, Mapping):
        registry_queue = {}
    queue_items = queue.get("queue_items")
    queued = len(queue_items) if isinstance(queue_items, list) else _nonnegative_int(aggregate.get("queued_review_items") or registry_queue.get("queued_review_items"), default=0)
    return {
        "source_queue_feature_id": str(queue.get("feature_id") or registry_queue.get("source_queue_feature_id") or "unknown"),
        "queued_review_items": queued,
        "p0_items": _nonnegative_int(aggregate.get("p0_items") or registry_queue.get("p0_items"), default=0),
        "p1_items": _nonnegative_int(aggregate.get("p1_items") or registry_queue.get("p1_items"), default=0),
        "queue_recommendation": str(aggregate.get("queue_recommendation") or registry_queue.get("queue_recommendation") or "unknown"),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _expansion_summary(plan: Mapping[str, Any]) -> dict[str, object]:
    targets = plan.get("expansion_targets")
    if not isinstance(targets, Mapping):
        targets = {}
    return {
        "source_plan_feature_id": str(plan.get("feature_id") or "unknown"),
        "plan_status": str(plan.get("plan_status") or "unknown"),
        "gold_mutation_policy": str(plan.get("gold_mutation_policy") or "unknown"),
        "planned_new_case_count": _nonnegative_int(targets.get("planned_new_case_count"), default=0),
        "requires_separate_reviewed_gold_patch": bool(targets.get("requires_separate_reviewed_gold_patch", True)),
        "may_add_gold_cases": bool(plan.get("may_add_gold_cases", False)),
        "may_mutate_gold": bool(plan.get("may_mutate_gold", False)),
        "may_promote_candidate": bool(plan.get("may_promote_candidate", False)),
        "authority_statement": str(plan.get("authority_statement") or "unknown"),
    }


def _gate_blockers(
    *,
    policy: Mapping[str, Any],
    registry_summary: Mapping[str, Any],
    evaluation_summary: Mapping[str, Any],
    queue_summary: Mapping[str, Any],
    expansion_summary: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if registry_summary.get("authority_statement") != AUTHORITY_STATEMENT:
        blockers.append("registry_authority_statement_not_advisory_only")
    if registry_summary.get("router_authority") != "none":
        blockers.append("registry_router_authority_not_none")
    if registry_summary.get("may_promote_candidate") is not False:
        blockers.append("registry_may_promote_candidate_not_false")
    if policy.get("require_registry_record_promotion_blocked") and registry_summary.get("promotion_blocked") is not True:
        blockers.append("registry_record_not_promotion_blocked")
    if not registry_summary.get("candidate_code_hash_present"):
        blockers.append("candidate_code_hash_missing")

    if int(evaluation_summary.get("cases_evaluated") or 0) < int(policy.get("minimum_cases") or 0):
        blockers.append("minimum_cases_not_met")
    if int(evaluation_summary.get("mismatches") or 0) > int(policy.get("maximum_mismatches") or 0):
        blockers.append("candidate_gold_mismatches_present")
    if int(evaluation_summary.get("guard_failures") or 0) > int(policy.get("maximum_guard_failures") or 0):
        blockers.append("guard_failures_present")
    if int(evaluation_summary.get("resource_failures") or 0) > int(policy.get("maximum_resource_failures") or 0):
        blockers.append("resource_failures_present")
    if int(evaluation_summary.get("critical_failures") or 0) > int(policy.get("maximum_critical_failures") or 0):
        blockers.append("critical_failures_present")

    if int(queue_summary.get("queued_review_items") or 0) > int(policy.get("maximum_queued_review_items") or 0):
        blockers.append("human_review_queue_not_empty")
    if int(queue_summary.get("p0_items") or 0) > int(policy.get("maximum_p0_review_items") or 0):
        blockers.append("p0_review_items_present")
    if int(queue_summary.get("p1_items") or 0) > int(policy.get("maximum_p1_review_items") or 0):
        blockers.append("p1_review_items_present")

    if expansion_summary.get("source_plan_feature_id") == "unknown":
        blockers.append("gold_expansion_plan_missing")
    if expansion_summary.get("may_add_gold_cases") is not False:
        blockers.append("gold_expansion_plan_may_add_gold_cases_not_false")
    if expansion_summary.get("may_mutate_gold") is not False:
        blockers.append("gold_expansion_plan_may_mutate_gold_not_false")
    if expansion_summary.get("may_promote_candidate") is not False:
        blockers.append("gold_expansion_plan_may_promote_candidate_not_false")
    if policy.get("require_gold_expansion_plan_reviewed_separately") and expansion_summary.get("requires_separate_reviewed_gold_patch") is not True:
        blockers.append("gold_expansion_plan_does_not_require_separate_reviewed_patch")

    return blockers


def _next_allowed_step(gate_decision: str) -> str:
    if gate_decision == ELIGIBLE_REVIEW_ONLY:
        return "future_governed_shadow_mode_design_review_only"
    return "resolve_blockers_with_human_review_before_future_phase"


def _nonnegative_int(value: Any, *, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(0, parsed)
