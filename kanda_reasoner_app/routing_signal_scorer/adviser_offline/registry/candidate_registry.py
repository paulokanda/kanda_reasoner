"""Pure in-memory candidate registry records for Adviser Candidate v0.

M14 builds deterministic registry records from caller-supplied candidate
metadata, M12 evaluation-report summaries, and M13 review-queue summaries. It is
provenance infrastructure only. It never discovers cases, persists registry
records, mutates gold data, executes candidates, or grants router authority.

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
- no scratch writer or registry writer;
- no gold mutation;
- no model, provider, network, embedding, vector, or dependency behavior;
- no runtime router authority.
"""

from __future__ import annotations


__all__ = [
    'assert_candidate_registry_record_valid',
    'build_candidate_registry_record',
    'validate_candidate_registry_record',
]
from collections.abc import Mapping
from typing import Any

from .hash_utils import hash_record_without_field

FEATURE_ID = "routing_signal_scorer_v3_adviser_candidate_registry_v1"
SCHEMA_VERSION = "3.55-adviser-candidate-registry"
AUTHORITY_STATEMENT = "advisory_only"
REGISTRY_KIND = "in_memory_candidate_registry_record_only"
PROMOTION_GATE = "blocked_until_m16_promotion_criteria_gate"
HEX_DIGITS = frozenset("0123456789abcdef")


def build_candidate_registry_record(
    *,
    candidate_metadata: Mapping[str, Any],
    evaluation_report: Mapping[str, Any] | None = None,
    review_queue: Mapping[str, Any] | None = None,
    registry_record_id: str = "candidate-registry-record-not-persisted",
    recorded_by: str = "human-review-pending",
) -> dict[str, object]:
    """Build one deterministic in-memory candidate registry record.

    All inputs are supplied by the caller. The function does not load cases,
    inspect source trees, persist records, update registries, execute candidates,
    or expose runtime routing behavior.
    """

    if not isinstance(candidate_metadata, Mapping):
        raise TypeError("candidate_metadata must be a mapping")
    if evaluation_report is not None and not isinstance(evaluation_report, Mapping):
        raise TypeError("evaluation_report must be a mapping when supplied")
    if review_queue is not None and not isinstance(review_queue, Mapping):
        raise TypeError("review_queue must be a mapping when supplied")

    evaluation_report = evaluation_report or {}
    review_queue = review_queue or {}

    candidate_id = _required_text(candidate_metadata, "candidate_id")
    candidate_version = _required_text(candidate_metadata, "candidate_version")
    candidate_code_hash = _required_hash(candidate_metadata, "candidate_code_hash")

    evaluation_summary = _evaluation_summary(evaluation_report)
    queue_summary = _queue_summary(review_queue)
    blockers = _blockers(evaluation_summary=evaluation_summary, queue_summary=queue_summary)

    record: dict[str, object] = {
        "feature_id": FEATURE_ID,
        "schema_version": SCHEMA_VERSION,
        "authority_statement": AUTHORITY_STATEMENT,
        "registry_kind": REGISTRY_KIND,
        "registry_record_id": str(registry_record_id),
        "recorded_by": str(recorded_by),
        "candidate_id": candidate_id,
        "candidate_version": candidate_version,
        "candidate_feature_id": str(candidate_metadata.get("candidate_feature_id") or "unknown"),
        "candidate_module_path": str(candidate_metadata.get("candidate_module_path") or "not_recorded"),
        "candidate_code_hash": candidate_code_hash,
        "candidate_contract_schema_version": str(candidate_metadata.get("candidate_contract_schema_version") or "unknown"),
        "gold_set_version": str(candidate_metadata.get("gold_set_version") or "unknown"),
        "source_policy": "caller_supplied_metadata_evaluation_queue_only_no_discovery",
        "output_policy": "in_memory_record_only_no_persistence",
        "router_authority": "none",
        "runtime_integration": "forbidden",
        "gold_mutation": "forbidden",
        "candidate_promotion": "forbidden_until_later_governed_gate",
        "promotion_gate": PROMOTION_GATE,
        "may_promote_candidate": False,
        "may_mutate_gold": False,
        "may_record_registry": False,
        "may_record_run_record": False,
        "human_review_status": "registry_record_requires_human_review",
        "registry_status": _registry_status(blockers),
        "promotion_blocked": True,
        "promotion_blockers": blockers,
        "evaluation_summary": evaluation_summary,
        "review_queue_summary": queue_summary,
    }
    record["record_hash"] = hash_record_without_field(record, "record_hash")
    return record


def validate_candidate_registry_record(record: Mapping[str, Any]) -> dict[str, object]:
    """Validate a supplied candidate registry record."""

    errors: list[str] = []
    if not isinstance(record, Mapping):
        return {"ok": False, "errors": ["record must be a mapping"]}

    for field in (
        "feature_id",
        "schema_version",
        "authority_statement",
        "registry_kind",
        "registry_record_id",
        "candidate_id",
        "candidate_version",
        "candidate_code_hash",
        "router_authority",
        "promotion_gate",
        "may_promote_candidate",
        "may_mutate_gold",
        "may_record_registry",
        "registry_status",
        "promotion_blocked",
        "record_hash",
    ):
        if field not in record:
            errors.append(f"missing {field}")

    if record.get("feature_id") != FEATURE_ID:
        errors.append("feature_id mismatch")
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if record.get("authority_statement") != AUTHORITY_STATEMENT:
        errors.append("authority_statement must be advisory_only")
    if record.get("registry_kind") != REGISTRY_KIND:
        errors.append("registry_kind mismatch")
    if record.get("router_authority") != "none":
        errors.append("router_authority must be none")
    if record.get("may_promote_candidate") is not False:
        errors.append("may_promote_candidate must be false")
    if record.get("may_mutate_gold") is not False:
        errors.append("may_mutate_gold must be false")
    if record.get("may_record_registry") is not False:
        errors.append("may_record_registry must be false")
    if record.get("promotion_blocked") is not True:
        errors.append("promotion_blocked must be true until later promotion gate")

    code_hash = str(record.get("candidate_code_hash") or "")
    if not _is_sha256(code_hash):
        errors.append("candidate_code_hash must be sha256 hex")

    if "record_hash" in record:
        expected = hash_record_without_field(record, "record_hash")
        if record.get("record_hash") != expected:
            errors.append("record_hash mismatch")

    return {"ok": not errors, "errors": errors}


def assert_candidate_registry_record_valid(record: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return record when valid; raise ValueError otherwise."""

    result = validate_candidate_registry_record(record)
    if not result["ok"]:
        raise ValueError("candidate registry record invalid: " + "; ".join(result["errors"]))
    return record


def _evaluation_summary(report: Mapping[str, Any]) -> dict[str, object]:
    aggregate = report.get("aggregate")
    if not isinstance(aggregate, Mapping):
        aggregate = {}
    case_results = report.get("case_results")
    case_count = len(case_results) if isinstance(case_results, list) else int(aggregate.get("total_cases") or aggregate.get("source_total_cases") or 0)
    return {
        "source_report_feature_id": str(report.get("feature_id") or "unknown"),
        "source_report_run_id": str(report.get("run_id") or "unknown"),
        "cases_evaluated": case_count,
        "exact_matches": int(aggregate.get("exact_matches") or 0),
        "mismatches": int(aggregate.get("mismatches") or 0),
        "guard_failures": int(aggregate.get("guard_failures") or 0),
        "resource_failures": int(aggregate.get("resource_failures") or 0),
        "critical_failures": int(aggregate.get("critical_failures") or 0),
        "promotion_recommendation": str(aggregate.get("promotion_recommendation") or "unknown"),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _queue_summary(queue: Mapping[str, Any]) -> dict[str, object]:
    aggregate = queue.get("aggregate")
    if not isinstance(aggregate, Mapping):
        aggregate = {}
    queue_items = queue.get("queue_items")
    queued = len(queue_items) if isinstance(queue_items, list) else int(aggregate.get("queued_review_items") or 0)
    return {
        "source_queue_feature_id": str(queue.get("feature_id") or "unknown"),
        "source_queue_id": str(queue.get("queue_id") or "unknown"),
        "queued_review_items": queued,
        "p0_items": int(aggregate.get("p0_items") or 0),
        "p1_items": int(aggregate.get("p1_items") or 0),
        "queue_recommendation": str(aggregate.get("queue_recommendation") or "unknown"),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _blockers(*, evaluation_summary: Mapping[str, Any], queue_summary: Mapping[str, Any]) -> list[str]:
    blockers = ["m16_promotion_gate_not_yet_run"]
    if int(evaluation_summary.get("cases_evaluated") or 0) == 0:
        blockers.append("no_cases_evaluated")
    if int(evaluation_summary.get("critical_failures") or 0) > 0:
        blockers.append("critical_failures_present")
    if int(evaluation_summary.get("guard_failures") or 0) > 0:
        blockers.append("guard_failures_present")
    if int(evaluation_summary.get("resource_failures") or 0) > 0:
        blockers.append("resource_failures_present")
    if int(evaluation_summary.get("mismatches") or 0) > 0:
        blockers.append("candidate_gold_mismatches_present")
    if int(queue_summary.get("queued_review_items") or 0) > 0:
        blockers.append("human_review_queue_not_empty")
    if int(queue_summary.get("p0_items") or 0) > 0:
        blockers.append("p0_review_items_present")
    return blockers


def _registry_status(blockers: list[str]) -> str:
    if any(blocker in blockers for blocker in ("critical_failures_present", "p0_review_items_present")):
        return "blocked_critical_review_required"
    if len(blockers) > 1:
        return "blocked_human_review_required"
    return "registered_for_later_promotion_gate_review"


def _required_text(mapping: Mapping[str, Any], field: str) -> str:
    value = str(mapping.get(field) or "").strip()
    if not value:
        raise ValueError(f"{field} is required")
    return value


def _required_hash(mapping: Mapping[str, Any], field: str) -> str:
    value = _required_text(mapping, field).lower()
    if not _is_sha256(value):
        raise ValueError(f"{field} must be sha256 hex")
    return value


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in HEX_DIGITS for char in value)
