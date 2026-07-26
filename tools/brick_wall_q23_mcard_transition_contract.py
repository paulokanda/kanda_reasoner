"""Validation-only contract for deterministic Brick Wall Q23 MCard tests."""
from __future__ import annotations

from copy import deepcopy
from typing import Mapping

from validate_brick_wall_q11_mcard_applicability_lifecycle_v1 import VALID_TRANSITIONS

__all__: list[str] = []

DURABLE_ARTIFACTS = (
    "project_source_changes",
    "generated_helper_modules",
    "canonical_preview",
    "transaction_records",
    "mutation_lane_state",
    "refactor_receipt",
)

REQUIRED_FIELDS = (
    "tests_required",
    "no_test_evidence",
    "primary_box",
    "canonical_owner",
    "canonical_facade",
    "valid_transitions",
    "invalid_transitions",
    "durable_artifacts",
    "cases",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q24",
    "may_begin_coding",
    "may_write_source",
)

CASE_FIELDS = (
    "case_id",
    "path_kind",
    "from_state",
    "to_state",
    "lifecycle_generation_current",
    "async_generation_current",
    "open_transaction",
    "unresolved_apply_outcome",
    "terminal_verified",
    "rollback_verified",
    "expected_allowed",
    "expected_blockers",
    "tool_memory_before",
    "tool_memory_after",
    "durable_state_before",
    "durable_state_after",
    "validators",
    "expected_markers",
)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object, *, allow_empty: bool = False) -> bool:
    return isinstance(value, list) and (allow_empty or bool(value)) and all(_text(x) for x in value)


def expected_blockers(case: Mapping[str, object]) -> list[str]:
    blockers: list[str] = []
    transition = (str(case.get("from_state")), str(case.get("to_state")))
    if transition not in VALID_TRANSITIONS:
        blockers.append("INVALID_MCARD_TRANSITION")
    if not case.get("lifecycle_generation_current"):
        blockers.append("STALE_LIFECYCLE_GENERATION")
    if not case.get("async_generation_current"):
        blockers.append("STALE_ASYNC_GENERATION")
    target = str(case.get("to_state"))
    if (case.get("open_transaction") or case.get("unresolved_apply_outcome")) and target == "CARD_EJECTED":
        blockers.append("CARD_EJECT_LOCKED")
    if str(case.get("path_kind")) == "DESTRUCTIVE_EJECT":
        blockers.append("DESTRUCTIVE_EJECT_FORBIDDEN")
    if target == "CARD_EJECTED":
        prior = str(case.get("from_state"))
        if prior == "VERIFIED_TERMINAL" and not case.get("terminal_verified"):
            blockers.append("TERMINAL_NOT_VERIFIED")
        if prior == "ROLLBACK_VERIFIED" and not case.get("rollback_verified"):
            blockers.append("ROLLBACK_NOT_VERIFIED")
        if prior not in {"VERIFIED_TERMINAL", "ROLLBACK_VERIFIED"}:
            blockers.append("PREMATURE_CARD_EJECT")
    return sorted(set(blockers))


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise AssertionError("record missing fields: " + ", ".join(missing))
    for field in ("tests_required", "may_proceed_to_q24", "may_begin_coding", "may_write_source"):
        if not isinstance(record[field], bool):
            raise AssertionError("record boolean field invalid: " + field)
    if record["decision"] not in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}:
        raise AssertionError("invalid decision")
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q23 cannot authorize coding or source writes")
    if record["decision"] == "BLOCKED" or record["unresolved_fields"]:
        raise AssertionError("Q23 record remains blocked")
    if not record["may_proceed_to_q24"]:
        raise AssertionError("Q24 progression not approved")
    if not record["tests_required"]:
        if record["decision"] != "NOT_APPLICABLE" or not _texts(record["no_test_evidence"]):
            raise AssertionError("N/A evidence incomplete")
        if record["cases"]:
            raise AssertionError("N/A record contains cases")
        return
    if record["decision"] != "COMPLETE" or record["no_test_evidence"]:
        raise AssertionError("required Q23 record not complete")
    if not all(_text(record[x]) for x in ("primary_box", "canonical_owner", "canonical_facade")):
        raise AssertionError("Q23 owner fields incomplete")
    if set(map(tuple, record["valid_transitions"])) != VALID_TRANSITIONS:
        raise AssertionError("canonical valid transition inventory drift")
    if not _texts(record["invalid_transitions"]):
        raise AssertionError("invalid transition inventory missing")
    if tuple(record["durable_artifacts"]) != DURABLE_ARTIFACTS:
        raise AssertionError("durable artifact inventory drift")
    cases = record["cases"]
    if not isinstance(cases, list) or not cases:
        raise AssertionError("Q23 cases missing")
    ids: set[str] = set()
    kinds: set[str] = set()
    for case in cases:
        if not isinstance(case, Mapping):
            raise AssertionError("case must be a mapping")
        absent = [field for field in CASE_FIELDS if field not in case]
        if absent:
            raise AssertionError("case missing fields: " + ", ".join(absent))
        case_id = str(case["case_id"])
        if not case_id or case_id in ids:
            raise AssertionError("duplicate or empty case ID")
        ids.add(case_id); kinds.add(str(case["path_kind"]))
        for field in ("lifecycle_generation_current", "async_generation_current", "open_transaction", "unresolved_apply_outcome", "terminal_verified", "rollback_verified", "expected_allowed"):
            if not isinstance(case[field], bool):
                raise AssertionError("case boolean field invalid: " + field)
        if not _texts(case["validators"]) or not _texts(case["expected_markers"]):
            raise AssertionError("validator evidence missing")
        actual = expected_blockers(case)
        if sorted(case["expected_blockers"]) != actual:
            raise AssertionError("deterministic blocker mismatch: " + case_id)
        if case["expected_allowed"] != (not actual):
            raise AssertionError("expected outcome mismatch: " + case_id)
        before = case["durable_state_before"]
        after = case["durable_state_after"]
        if not isinstance(before, Mapping) or not isinstance(after, Mapping):
            raise AssertionError("durable state must be mappings")
        if case["expected_allowed"] and case["to_state"] == "CARD_EJECTED":
            if case["tool_memory_after"]:
                raise AssertionError("terminal eject retained Tool card memory")
            if dict(before) != dict(after) or not all(after.get(x) for x in DURABLE_ARTIFACTS):
                raise AssertionError("terminal eject lost durable project state")
        elif not case["expected_allowed"]:
            if case["tool_memory_before"] != case["tool_memory_after"] or dict(before) != dict(after):
                raise AssertionError("blocked transition mutated state")
    required_kinds = {"NORMAL", "ROLLBACK", "SKIPPED", "STALE", "LOCKED", "PREMATURE_EJECT", "DESTRUCTIVE_EJECT"}
    if not required_kinds.issubset(kinds):
        raise AssertionError("Q23 case coverage incomplete")


def _durable() -> dict[str, bool]:
    return {name: True for name in DURABLE_ARTIFACTS}


def _case(case_id: str, kind: str, before: str, after: str, **overrides: object) -> dict[str, object]:
    case: dict[str, object] = {
        "case_id": case_id,
        "path_kind": kind,
        "from_state": before,
        "to_state": after,
        "lifecycle_generation_current": True,
        "async_generation_current": True,
        "open_transaction": False,
        "unresolved_apply_outcome": False,
        "terminal_verified": before == "VERIFIED_TERMINAL",
        "rollback_verified": before == "ROLLBACK_VERIFIED",
        "expected_allowed": True,
        "expected_blockers": [],
        "tool_memory_before": {"card": case_id},
        "tool_memory_after": {"card": case_id, "phase": after},
        "durable_state_before": _durable(),
        "durable_state_after": _durable(),
        "validators": ["tools/validate_architecture_review_project_card_lifecycle_v1.py"],
        "expected_markers": ["ARCHITECTURE_REVIEW_CARD_MACHINE_LIFECYCLE: PASS"],
    }
    case.update(overrides)
    blockers = expected_blockers(case)
    case["expected_blockers"] = blockers
    case["expected_allowed"] = not blockers
    if after == "CARD_EJECTED" and not blockers:
        case["tool_memory_after"] = {}
    if blockers:
        case["tool_memory_after"] = deepcopy(case["tool_memory_before"])
        case["durable_state_after"] = deepcopy(case["durable_state_before"])
    return case


def valid_required_record() -> dict[str, object]:
    cases = [
        _case("normal-apply", "NORMAL", "APPLYING", "VERIFIED_TERMINAL"),
        _case("normal-eject", "NORMAL", "VERIFIED_TERMINAL", "CARD_EJECTED"),
        _case("rollback-request", "ROLLBACK", "APPLIED_NOT_VERIFIED", "ROLLBACK_REQUESTED"),
        _case("rollback-verify", "ROLLBACK", "ROLLBACK_REQUESTED", "ROLLBACK_VERIFIED"),
        _case("rollback-eject", "ROLLBACK", "ROLLBACK_VERIFIED", "CARD_EJECTED"),
        _case("skip-authorization", "SKIPPED", "PREVIEW_VALIDATED", "APPLYING"),
        _case("stale-generation", "STALE", "CARD_READ", "PLAN_READY", lifecycle_generation_current=False),
        _case("open-transaction-eject", "LOCKED", "VERIFIED_TERMINAL", "CARD_EJECTED", open_transaction=True),
        _case("premature-eject", "PREMATURE_EJECT", "APPLYING", "CARD_EJECTED"),
        _case("destructive-eject", "DESTRUCTIVE_EJECT", "VERIFIED_TERMINAL", "CARD_EJECTED"),
    ]
    # Destructive-eject is represented as a valid transition with invalid state effect and rejected by validator.
    cases[-1]["tool_memory_after"] = {}
    cases[-1]["durable_state_after"] = {name: False for name in DURABLE_ARTIFACTS}
    # Keep canonical record valid by converting this case to expected blocked via explicit semantic blocker.
    cases[-1]["expected_blockers"] = ["DESTRUCTIVE_EJECT_FORBIDDEN"]
    cases[-1]["expected_allowed"] = False
    cases[-1]["tool_memory_after"] = deepcopy(cases[-1]["tool_memory_before"])
    cases[-1]["durable_state_after"] = deepcopy(cases[-1]["durable_state_before"])
    return {
        "tests_required": True,
        "no_test_evidence": [],
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "canonical_owner": "architecture_review_project_card_machine_canon",
        "canonical_facade": "Q11 VALID_TRANSITIONS and lifecycle validators",
        "valid_transitions": [list(x) for x in sorted(VALID_TRANSITIONS)],
        "invalid_transitions": ["PREVIEW_VALIDATED->APPLYING", "APPLYING->CARD_EJECTED", "ROLLBACK_REQUESTED->CARD_EJECTED"],
        "durable_artifacts": list(DURABLE_ARTIFACTS),
        "cases": cases,
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q24": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    record = valid_required_record()
    record.update(tests_required=False, no_test_evidence=["No MCard lifecycle behavior is affected."], cases=[], decision="NOT_APPLICABLE")
    return record


def mutated_record() -> dict[str, object]:
    return deepcopy(valid_required_record())
