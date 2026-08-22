"""Validation-only contract for deterministic observer MCard transitions."""
from __future__ import annotations

from copy import deepcopy
from typing import Mapping

from validate_brick_wall_q11_mcard_applicability_lifecycle_v1 import VALID_TRANSITIONS

__all__: list[str] = []

DURABLE_ARTIFACTS = (
    "project_source", "project_validation_evidence", "project_release_artifacts",
    "project_freeze_memory", "project_support_evidence",
)
REQUIRED_FIELDS = (
    "tests_required", "no_test_evidence", "primary_box", "canonical_owner",
    "canonical_facade", "valid_transitions", "invalid_transitions",
    "durable_artifacts", "cases", "unresolved_fields", "decision",
    "may_proceed_to_q24", "may_begin_coding", "may_write_source",
)
CASE_FIELDS = (
    "case_id", "path_kind", "from_state", "to_state",
    "lifecycle_generation_current", "async_generation_current",
    "project_source_write_requested", "kanda_dependency_required",
    "expected_allowed", "expected_blockers", "tool_memory_before",
    "tool_memory_after", "durable_state_before", "durable_state_after",
    "validators", "expected_markers",
)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object, allow_empty: bool = False) -> bool:
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
    if case.get("project_source_write_requested"):
        blockers.append("PROJECT_SOURCE_WRITE_UNSUPPORTED")
    if case.get("kanda_dependency_required"):
        blockers.append("KANDA_DEPENDENCY_FOR_EXTERNAL_PROJECT_FORBIDDEN")
    if str(case.get("path_kind")) == "DESTRUCTIVE_EJECT":
        blockers.append("DESTRUCTIVE_EJECT_FORBIDDEN")
    return sorted(set(blockers))


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise AssertionError("record missing fields: " + ", ".join(missing))
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
        return
    if set(map(tuple, record["valid_transitions"])) != VALID_TRANSITIONS:
        raise AssertionError("canonical valid transition inventory drift")
    if tuple(record["durable_artifacts"]) != DURABLE_ARTIFACTS:
        raise AssertionError("durable artifact inventory drift")
    cases = record["cases"]
    if not isinstance(cases, list) or not cases:
        raise AssertionError("Q23 cases missing")
    kinds: set[str] = set()
    ids: set[str] = set()
    for case in cases:
        if not isinstance(case, Mapping):
            raise AssertionError("case must be mapping")
        absent = [field for field in CASE_FIELDS if field not in case]
        if absent:
            raise AssertionError("case missing fields: " + ", ".join(absent))
        case_id = str(case["case_id"])
        if not case_id or case_id in ids:
            raise AssertionError("duplicate or empty case ID")
        ids.add(case_id)
        kinds.add(str(case["path_kind"]))
        blockers = expected_blockers(case)
        if sorted(case["expected_blockers"]) != blockers:
            raise AssertionError("deterministic blocker mismatch: " + case_id)
        if bool(case["expected_allowed"]) != (not blockers):
            raise AssertionError("expected outcome mismatch: " + case_id)
        if not _texts(case["validators"]) or not _texts(case["expected_markers"]):
            raise AssertionError("validator evidence missing")
        before = case["durable_state_before"]
        after = case["durable_state_after"]
        if not isinstance(before, Mapping) or not isinstance(after, Mapping):
            raise AssertionError("durable state must be mappings")
        if not blockers and case["to_state"] == "CARD_EJECTED":
            if case["tool_memory_after"]:
                raise AssertionError("eject retained target-specific Tool memory")
            if dict(before) != dict(after):
                raise AssertionError("eject changed Project-owned durable state")
        if blockers and (case["tool_memory_before"] != case["tool_memory_after"] or dict(before) != dict(after)):
            raise AssertionError("blocked transition mutated state")
    required = {"NORMAL", "STALE", "INVALID", "SOURCE_WRITE", "KANDA_DEPENDENCY", "DESTRUCTIVE_EJECT"}
    if not required.issubset(kinds):
        raise AssertionError("Q23 case coverage incomplete")


def _durable() -> dict[str, bool]:
    return {name: True for name in DURABLE_ARTIFACTS}


def _case(case_id: str, kind: str, before: str, after: str, **overrides: object) -> dict[str, object]:
    case: dict[str, object] = {
        "case_id": case_id, "path_kind": kind, "from_state": before,
        "to_state": after, "lifecycle_generation_current": True,
        "async_generation_current": True, "project_source_write_requested": False,
        "kanda_dependency_required": False, "expected_allowed": True,
        "expected_blockers": [], "tool_memory_before": {"card": case_id},
        "tool_memory_after": {"card": case_id, "phase": after},
        "durable_state_before": _durable(), "durable_state_after": _durable(),
        "validators": ["tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py"],
        "expected_markers": ["MCARD_OBSERVER_LIFECYCLE: PASS"],
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
        _case("normal-read", "NORMAL", "CARD_INSERTED", "CARD_READ"),
        _case("normal-observe", "NORMAL", "CARD_READ", "OBSERVED"),
        _case("normal-analyze", "NORMAL", "OBSERVED", "ANALYSIS_READY"),
        _case("normal-report", "NORMAL", "ANALYSIS_READY", "REPORT_READY"),
        _case("normal-eject", "NORMAL", "REPORT_READY", "CARD_EJECTED"),
        _case("stale-generation", "STALE", "CARD_READ", "OBSERVED", lifecycle_generation_current=False),
        _case("invalid-skip", "INVALID", "CARD_READ", "REPORT_READY"),
        _case("source-write", "SOURCE_WRITE", "OBSERVED", "ANALYSIS_READY", project_source_write_requested=True),
        _case("kanda-dependency", "KANDA_DEPENDENCY", "OBSERVED", "ANALYSIS_READY", kanda_dependency_required=True),
        _case("destructive-eject", "DESTRUCTIVE_EJECT", "REPORT_READY", "CARD_EJECTED"),
    ]
    return {
        "tests_required": True, "no_test_evidence": [],
        "primary_box": "architecture_review_project_card_machine_canon",
        "canonical_owner": "KPR-12-005",
        "canonical_facade": "tools/brick_wall_q23_mcard_transition_contract.py",
        "valid_transitions": [list(item) for item in sorted(VALID_TRANSITIONS)],
        "invalid_transitions": ["CARD_READ -> REPORT_READY", "OBSERVED -> APPLYING"],
        "durable_artifacts": list(DURABLE_ARTIFACTS), "cases": cases,
        "unresolved_fields": [], "decision": "COMPLETE",
        "may_proceed_to_q24": True, "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    record = valid_required_record()
    record.update(tests_required=False, no_test_evidence=["MCard observer lifecycle is not in scope."], cases=[], decision="NOT_APPLICABLE")
    return record


def mutated_record() -> dict[str, object]:
    return deepcopy(valid_required_record())
