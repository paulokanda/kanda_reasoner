"""Validation-only Brick Wall Q28 exception provenance contract."""
from __future__ import annotations

from copy import deepcopy
from typing import Mapping

__all__: list[str] = []
FEATURE_ID = "brick-wall-q28-structured-exception-provenance-enforcement-v1"
FAILURE_CLASSES = ("SETUP", "BEHAVIOR", "CLEANUP", "EVIDENCE")
ROOT_CLASSIFICATIONS = (
    "TOOL_SOURCE",
    "ACTIVE_PROJECT_SOURCE",
    "PROJECT_SUPPORT",
    "TRANSIENT_GARBAGE",
    "EXTERNAL",
    "NONE",
)
REQUIRED_FIELDS = (
    "provenance_required",
    "no_provenance_evidence",
    "q27_decision_complete",
    "primary_box",
    "canonical_owners",
    "cases",
    "validators",
    "expected_markers",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q29",
    "may_begin_coding",
    "may_write_source",
)
CASE_FIELDS = (
    "case_id",
    "operation_phase",
    "operation_id",
    "target",
    "root_classification",
    "last_successful_marker",
    "failure_class",
    "exception_type",
    "exception_message",
    "original_cause_type",
    "original_cause_message",
    "invocation_position",
    "validators",
    "expected_markers",
)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object, *, empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (empty or bool(value))
        and all(_text(item) for item in value)
    )


def _validate_case(case: Mapping[str, object]) -> None:
    missing = [field for field in CASE_FIELDS if field not in case]
    if missing:
        raise AssertionError("Q28 case missing fields: " + ", ".join(missing))
    for field in CASE_FIELDS:
        if field in {"validators", "expected_markers"}:
            if not _texts(case[field]):
                raise AssertionError("Q28 case evidence incomplete: " + field)
        elif not _text(case[field]):
            raise AssertionError("Q28 case text incomplete: " + field)
    if case["failure_class"] not in FAILURE_CLASSES:
        raise AssertionError("Q28 invalid failure class")
    if case["root_classification"] not in ROOT_CLASSIFICATIONS:
        raise AssertionError("Q28 invalid root classification")


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise AssertionError("Q28 record missing fields: " + ", ".join(missing))
    for field in (
        "provenance_required",
        "q27_decision_complete",
        "may_proceed_to_q29",
        "may_begin_coding",
        "may_write_source",
    ):
        if not isinstance(record[field], bool):
            raise AssertionError("Q28 invalid boolean field: " + field)
    if record["decision"] not in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}:
        raise AssertionError("Q28 invalid decision")
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q28 cannot authorize coding or source writes")
    if record["decision"] == "BLOCKED" or record["unresolved_fields"]:
        raise AssertionError("Q28 remains blocked")
    if not record["may_proceed_to_q29"]:
        raise AssertionError("Q29 progression not approved")
    if not record["provenance_required"]:
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("Q28 N/A decision incomplete")
        if not _texts(record["no_provenance_evidence"]):
            raise AssertionError("Q28 N/A evidence incomplete")
        return
    if record["decision"] != "COMPLETE" or record["no_provenance_evidence"]:
        raise AssertionError("Q28 applicable decision incomplete")
    if not record["q27_decision_complete"]:
        raise AssertionError("Q27 baseline incomplete")
    if not _text(record["primary_box"]):
        raise AssertionError("Q28 primary box incomplete")
    owners = record["canonical_owners"]
    if not _texts(owners) or set(owners) != {
        "Error Memory lesson schema",
        "governed delivery wrappers",
    }:
        raise AssertionError("Q28 canonical owner inventory incomplete")
    cases = record["cases"]
    if not isinstance(cases, list) or not cases:
        raise AssertionError("Q28 case inventory incomplete")
    seen_ids: set[str] = set()
    seen_classes: set[str] = set()
    for case in cases:
        if not isinstance(case, Mapping):
            raise AssertionError("Q28 case must be a mapping")
        _validate_case(case)
        case_id = str(case["case_id"])
        if case_id in seen_ids:
            raise AssertionError("Q28 duplicate case id")
        seen_ids.add(case_id)
        seen_classes.add(str(case["failure_class"]))
    if seen_classes != set(FAILURE_CLASSES):
        raise AssertionError("Q28 failure class inventory incomplete")
    if not _texts(record["validators"]) or not _texts(record["expected_markers"]):
        raise AssertionError("Q28 validator evidence incomplete")


def capture_exception_provenance(
    exc: BaseException,
    *,
    operation_phase: str,
    operation_id: str,
    target: str,
    root_classification: str,
    last_successful_marker: str,
    failure_class: str,
    invocation_position: str,
) -> dict[str, str]:
    """Capture deterministic provenance without replacing the original cause."""
    values = {
        "operation_phase": operation_phase,
        "operation_id": operation_id,
        "target": target,
        "root_classification": root_classification,
        "last_successful_marker": last_successful_marker,
        "failure_class": failure_class,
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "invocation_position": invocation_position,
    }
    cause = exc.__cause__ or exc.__context__
    values["original_cause_type"] = type(cause).__name__ if cause else "NONE"
    values["original_cause_message"] = str(cause) if cause else "NONE"
    case = {
        "case_id": "runtime-capture",
        **values,
        "validators": ["runtime fixture"],
        "expected_markers": ["Q28_RUNTIME_STRUCTURED_EXCEPTION_PROVENANCE: PASS"],
    }
    _validate_case(case)
    return values


def _case(failure_class: str, suffix: str) -> dict[str, object]:
    return {
        "case_id": "q28-" + suffix,
        "operation_phase": suffix + "_phase",
        "operation_id": "operation-q28-" + suffix,
        "target": "tools/q28_" + suffix + "_fixture.py",
        "root_classification": "TOOL_SOURCE",
        "last_successful_marker": "Q28_" + suffix.upper() + "_PRECONDITION: PASS",
        "failure_class": failure_class,
        "exception_type": "RuntimeError",
        "exception_message": suffix + " failure",
        "original_cause_type": "ValueError",
        "original_cause_message": suffix + " original cause",
        "invocation_position": "fixture.py:10",
        "validators": [
            "tools/validate_brick_wall_q28_structured_exception_provenance_v1.py"
        ],
        "expected_markers": ["Q28_" + failure_class + "_FAILURE_CLASS: PASS"],
    }


def valid_complete_record() -> dict[str, object]:
    return {
        "provenance_required": True,
        "no_provenance_evidence": [],
        "q27_decision_complete": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "canonical_owners": [
            "Error Memory lesson schema",
            "governed delivery wrappers",
        ],
        "cases": [
            _case("SETUP", "setup"),
            _case("BEHAVIOR", "behavior"),
            _case("CLEANUP", "cleanup"),
            _case("EVIDENCE", "evidence"),
        ],
        "validators": [
            "tools/validate_brick_wall_q28_structured_exception_provenance_v1.py",
            "tools/validate_brick_wall_q27_control_byte_encoding_guards_v1.py",
        ],
        "expected_markers": [
            "Q28_ORIGINAL_CAUSE_CHAIN_PRESERVED: PASS",
            "Q28_OPERATION_PHASE_PROVENANCE: PASS",
            "Q28_FAILURE_CLASS_DISTINCTION: PASS",
            "Q28_RUNTIME_STRUCTURED_EXCEPTION_PROVENANCE: PASS",
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q29": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    record = valid_complete_record()
    record.update(
        provenance_required=False,
        no_provenance_evidence=[
            "The task has no material exception, operational failure, or evidence path."
        ],
        canonical_owners=[],
        cases=[],
        validators=[],
        expected_markers=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    return deepcopy(valid_complete_record())
