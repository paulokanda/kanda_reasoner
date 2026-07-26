"""Semantic record contract for Brick Wall Q18 stale-result rejection."""

from __future__ import annotations

from copy import deepcopy
from typing import Mapping, Sequence

__all__: list[str] = []

RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "async_work_required",
    "no_async_evidence",
    "routes",
    "unresolved_routes",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_q19",
    "may_begin_coding",
    "may_write_source",
)
ROUTE_FIELDS = (
    "route_id",
    "owner_box",
    "controller_or_receiver",
    "request_identity_fields",
    "result_identity_fields",
    "operation_id",
    "active_project_root",
    "target_identity",
    "source_fingerprint",
    "lifecycle_generation",
    "worker_generation",
    "acceptance_predicate",
    "cancellation_revokes_authority",
    "timeout_revokes_authority",
    "thread_settlement_tracked",
    "late_result_action",
    "stale_effects_blocked",
    "authorized_effects",
    "tests",
)
REQUIRED_IDENTITY_FIELDS = {
    "operation_id",
    "active_project_root",
    "target_identity",
    "source_fingerprint",
    "lifecycle_generation",
    "worker_generation",
}
REQUIRED_STALE_BLOCKS = {
    "state_mutation",
    "gate_open",
    "source_write",
    "durable_evidence_write",
    "current_ui_repopulation",
}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _fields(record: Mapping[str, object], fields: Sequence[str]) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise AssertionError("missing fields: " + ", ".join(missing))


def _validate_route(route: Mapping[str, object]) -> str:
    _fields(route, ROUTE_FIELDS)
    for field in (
        "route_id",
        "owner_box",
        "controller_or_receiver",
        "operation_id",
        "active_project_root",
        "target_identity",
        "source_fingerprint",
        "acceptance_predicate",
        "late_result_action",
    ):
        if not _nonempty(route[field]):
            raise AssertionError("empty route field: " + field)
    for field in (
        "lifecycle_generation",
        "worker_generation",
    ):
        if not isinstance(route[field], int) or route[field] < 1:
            raise AssertionError("invalid generation field: " + field)
    request_fields = set(_text_list(route["request_identity_fields"]))
    result_fields = set(_text_list(route["result_identity_fields"]))
    if not REQUIRED_IDENTITY_FIELDS.issubset(request_fields):
        raise AssertionError("request identity is incomplete")
    if not REQUIRED_IDENTITY_FIELDS.issubset(result_fields):
        raise AssertionError("result identity is incomplete")
    for field in (
        "cancellation_revokes_authority",
        "timeout_revokes_authority",
        "thread_settlement_tracked",
    ):
        if route[field] is not True:
            raise AssertionError("async lifecycle gate failed: " + field)
    if route["late_result_action"] not in {
        "DISCARD",
        "QUARANTINE_NO_AUTHORITY",
    }:
        raise AssertionError("late result action is not fail-closed")
    blocked = set(_text_list(route["stale_effects_blocked"]))
    if not REQUIRED_STALE_BLOCKS.issubset(blocked):
        raise AssertionError("stale-result effects are not fully blocked")
    if not _text_list(route["authorized_effects"]):
        raise AssertionError("authorized effects are missing")
    if not _text_list(route["tests"]):
        raise AssertionError("route tests are missing")
    predicate = str(route["acceptance_predicate"])
    for token in (
        "operation_id",
        "active_project_root",
        "target_identity",
        "source_fingerprint",
        "lifecycle_generation",
        "worker_generation",
        "accept_result",
    ):
        if token not in predicate:
            raise AssertionError("acceptance predicate missing: " + token)
    return str(route["route_id"])


def validate_record(record: Mapping[str, object]) -> None:
    """Validate one complete Q18 stale-result rejection record."""
    _fields(record, RECORD_FIELDS)
    if not _nonempty(record["identity_basis"]):
        raise AssertionError("identity basis missing")
    if not _nonempty(record["primary_box"]):
        raise AssertionError("primary box missing")
    if not isinstance(record["async_work_required"], bool):
        raise AssertionError("async_work_required must be boolean")
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q18 cannot authorize coding")
    if record["may_write_source"] is not False:
        raise AssertionError("Q18 cannot authorize source writes")
    if _text_list(record["unresolved_routes"]):
        raise AssertionError("unresolved async routes remain")
    if _text_list(record["blockers"]):
        raise AssertionError("async blockers remain")
    if not _text_list(record["tests"]):
        raise AssertionError("Q18 tests are missing")
    if record["async_work_required"] is False:
        if not _text_list(record["no_async_evidence"]):
            raise AssertionError("not-applicable evidence missing")
        if record["routes"] not in ([], None):
            raise AssertionError("not-applicable record carries routes")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("not-applicable decision invalid")
        if record["may_proceed_to_q19"] is not True:
            raise AssertionError("not-applicable record cannot progress")
        return
    routes = record["routes"]
    if not isinstance(routes, list) or not routes:
        raise AssertionError("required async routes are missing")
    seen: set[str] = set()
    for route in routes:
        if not isinstance(route, Mapping):
            raise AssertionError("async route is not a mapping")
        route_id = _validate_route(route)
        if route_id in seen:
            raise AssertionError("duplicate async route")
        seen.add(route_id)
    if record["decision"] != "COMPLETE":
        raise AssertionError("required async decision is not COMPLETE")
    if record["may_proceed_to_q19"] is not True:
        raise AssertionError("Q19 progression missing")


def _route(route_id: str, generation: int) -> dict[str, object]:
    identity = sorted(REQUIRED_IDENTITY_FIELDS)
    return {
        "route_id": route_id,
        "owner_box": "architecture_review_workbench",
        "controller_or_receiver": "canonical_qt_controller_or_gui_receiver",
        "request_identity_fields": identity,
        "result_identity_fields": identity,
        "operation_id": "operation-q18",
        "active_project_root": r"E:\sample_project",
        "target_identity": "module.py:sha256-current",
        "source_fingerprint": "a" * 64,
        "lifecycle_generation": 7,
        "worker_generation": generation,
        "acceptance_predicate": (
            "operation_id and active_project_root and target_identity and "
            "source_fingerprint and lifecycle_generation and worker_generation "
            "match current identity and accept_result is true"
        ),
        "cancellation_revokes_authority": True,
        "timeout_revokes_authority": True,
        "thread_settlement_tracked": True,
        "late_result_action": "DISCARD",
        "stale_effects_blocked": sorted(REQUIRED_STALE_BLOCKS),
        "authorized_effects": [
            "apply result through current public GUI receiver only",
        ],
        "tests": [
            "generation mismatch rejection",
            "cancel and timeout late-result discard",
        ],
    }


def valid_required_record() -> dict[str, object]:
    """Return a complete required Q18 fixture."""
    return {
        "identity_basis": "current Q12 operation and Q14 freshness evidence",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "async_work_required": True,
        "no_async_evidence": [],
        "routes": [
            _route("main_workbench_pipeline", 11),
            _route("local_ai_correction", 12),
            _route("completion_diff_review", 13),
        ],
        "unresolved_routes": [],
        "blockers": [],
        "tests": [
            "stale identity matrix",
            "late result cannot mutate or authorize",
        ],
        "decision": "COMPLETE",
        "may_proceed_to_q19": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    """Return an evidence-backed not-applicable Q18 fixture."""
    record = valid_required_record()
    record.update(
        async_work_required=False,
        no_async_evidence=[
            "bounded prompt-only task has no worker, callback, or queued result",
        ],
        routes=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    """Return an independent required fixture for negative tests."""
    return deepcopy(valid_required_record())
