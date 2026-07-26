"""Validation-only Brick Wall Q24 property-based MCard pilot contract."""
from __future__ import annotations

from copy import deepcopy
from itertools import product
from typing import Mapping

from brick_wall_q23_mcard_transition_contract import expected_blockers
from validate_brick_wall_q11_mcard_applicability_lifecycle_v1 import VALID_TRANSITIONS

__all__: list[str] = []

FEATURE_ID = "brick-wall-q24-property-based-mcard-pilot-decision-enforcement-v1"
PILOT_PROPERTIES = (
    "invalid transitions never advance state",
    "stale lifecycle or async generation always blocks",
    "eject remains locked during open transaction or unresolved apply",
    "only verified terminal or rollback state may eject",
    "blocked transitions preserve Tool and durable project state",
    "terminal eject clears Tool card memory and preserves durable project state",
)
REQUIRED_FIELDS = (
    "pilot_applicable", "no_pilot_evidence", "q23_deterministic_baseline_complete",
    "primary_box", "canonical_owner", "canonical_facade", "pilot_kind",
    "dependency_scope", "properties", "generator_strategy", "replay_strategy",
    "minimization_strategy", "bounds", "generated_transition_cases",
    "generated_sequences", "unique_meaningful_defects", "known_or_duplicate_findings",
    "measurable_gain", "operational_cost", "broader_adoption_decision",
    "unresolved_fields", "decision", "may_proceed_to_q25", "may_begin_coding",
    "may_write_source",
)
DEFECT_FIELDS = ("defect_id", "invariant", "minimal_counterexample", "replay", "owner")


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object, *, allow_empty: bool = False) -> bool:
    return isinstance(value, list) and (allow_empty or bool(value)) and all(_text(x) for x in value)


def _oracle_blockers(case: Mapping[str, object]) -> list[str]:
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


def run_bounded_pilot() -> dict[str, object]:
    states = sorted({state for transition in VALID_TRANSITIONS for state in transition} | {"APPLIED_NOT_VERIFIED"})
    transition_mismatches: list[dict[str, object]] = []
    transition_count = 0
    dimensions = product(
        states, states, (False, True), (False, True), (False, True),
        (False, True), (False, True), (False, True), ("NORMAL", "DESTRUCTIVE_EJECT"),
    )
    for from_state, to_state, lifecycle, async_generation, transaction, unresolved, terminal, rollback, path_kind in dimensions:
        case = {
            "from_state": from_state, "to_state": to_state,
            "lifecycle_generation_current": lifecycle,
            "async_generation_current": async_generation,
            "open_transaction": transaction,
            "unresolved_apply_outcome": unresolved,
            "terminal_verified": terminal,
            "rollback_verified": rollback,
            "path_kind": path_kind,
        }
        transition_count += 1
        actual = expected_blockers(case)
        oracle = _oracle_blockers(case)
        if actual != oracle:
            transition_mismatches.append({"case": case, "actual": actual, "oracle": oracle})

    sequence_count = 0
    sequence_mismatches: list[dict[str, object]] = []
    for start in states:
        for depth in (1, 2, 3):
            for targets in product(states, repeat=depth):
                sequence_count += 1
                actual_state = start
                oracle_state = start
                actual_trace: list[str] = []
                oracle_trace: list[str] = []
                for target in targets:
                    actual_case = {
                        "from_state": actual_state, "to_state": target,
                        "lifecycle_generation_current": True,
                        "async_generation_current": True,
                        "open_transaction": False,
                        "unresolved_apply_outcome": False,
                        "terminal_verified": actual_state == "VERIFIED_TERMINAL",
                        "rollback_verified": actual_state == "ROLLBACK_VERIFIED",
                        "path_kind": "NORMAL",
                    }
                    oracle_case = dict(actual_case)
                    oracle_case["from_state"] = oracle_state
                    oracle_case["terminal_verified"] = oracle_state == "VERIFIED_TERMINAL"
                    oracle_case["rollback_verified"] = oracle_state == "ROLLBACK_VERIFIED"
                    actual_blockers = expected_blockers(actual_case)
                    oracle_blockers = _oracle_blockers(oracle_case)
                    actual_trace.append("ALLOW" if not actual_blockers else "+".join(actual_blockers))
                    oracle_trace.append("ALLOW" if not oracle_blockers else "+".join(oracle_blockers))
                    if not actual_blockers:
                        actual_state = target
                    if not oracle_blockers:
                        oracle_state = target
                if actual_state != oracle_state or actual_trace != oracle_trace:
                    sequence_mismatches.append({
                        "start": start, "targets": targets, "actual_state": actual_state,
                        "oracle_state": oracle_state, "actual_trace": actual_trace,
                        "oracle_trace": oracle_trace,
                    })
    return {
        "transition_cases": transition_count,
        "sequences": sequence_count,
        "transition_mismatches": transition_mismatches,
        "sequence_mismatches": sequence_mismatches,
        "unique_meaningful_defects": transition_mismatches + sequence_mismatches,
    }


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise AssertionError("record missing fields: " + ", ".join(missing))
    for field in ("pilot_applicable", "q23_deterministic_baseline_complete", "may_proceed_to_q25", "may_begin_coding", "may_write_source"):
        if not isinstance(record[field], bool):
            raise AssertionError("invalid boolean field: " + field)
    if record["decision"] not in {"PILOT_RETAINED", "PILOT_REJECTED", "NOT_APPLICABLE", "BLOCKED"}:
        raise AssertionError("invalid Q24 decision")
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q24 cannot authorize coding or source writes")
    if record["decision"] == "BLOCKED" or record["unresolved_fields"]:
        raise AssertionError("Q24 remains blocked")
    if not record["may_proceed_to_q25"]:
        raise AssertionError("Q25 progression not approved")
    if not record["pilot_applicable"]:
        if record["decision"] != "NOT_APPLICABLE" or not _texts(record["no_pilot_evidence"]):
            raise AssertionError("Q24 N/A evidence incomplete")
        if record["generated_transition_cases"] or record["generated_sequences"] or record["unique_meaningful_defects"]:
            raise AssertionError("N/A record contains pilot results")
        return
    if not record["q23_deterministic_baseline_complete"]:
        raise AssertionError("Q23 deterministic baseline incomplete")
    if record["decision"] not in {"PILOT_RETAINED", "PILOT_REJECTED"} or record["no_pilot_evidence"]:
        raise AssertionError("applicable pilot decision incomplete")
    if not all(_text(record[field]) for field in ("primary_box", "canonical_owner", "canonical_facade", "pilot_kind", "dependency_scope", "generator_strategy", "replay_strategy", "minimization_strategy", "measurable_gain", "operational_cost")):
        raise AssertionError("Q24 owner, method, or evidence fields incomplete")
    if record["dependency_scope"] != "OPTIONAL_VALIDATION_ONLY_NO_GLOBAL_DEPENDENCY":
        raise AssertionError("property pilot escaped validation-only scope")
    if tuple(record["properties"]) != PILOT_PROPERTIES:
        raise AssertionError("Q24 property inventory drift")
    bounds = record["bounds"]
    if not isinstance(bounds, Mapping):
        raise AssertionError("pilot bounds missing")
    required_bounds = ("max_transition_cases", "max_sequences", "max_sequence_depth", "time_budget_seconds")
    if any(not isinstance(bounds.get(field), int) or int(bounds[field]) <= 0 for field in required_bounds):
        raise AssertionError("pilot bounds invalid")
    if bounds["max_transition_cases"] > 100_000 or bounds["max_sequences"] > 100_000 or bounds["max_sequence_depth"] > 8 or bounds["time_budget_seconds"] > 120:
        raise AssertionError("pilot is not bounded")
    if not isinstance(record["generated_transition_cases"], int) or not isinstance(record["generated_sequences"], int):
        raise AssertionError("pilot result counts invalid")
    if record["generated_transition_cases"] <= 0 or record["generated_transition_cases"] > bounds["max_transition_cases"]:
        raise AssertionError("transition pilot count outside bounds")
    if record["generated_sequences"] <= 0 or record["generated_sequences"] > bounds["max_sequences"]:
        raise AssertionError("sequence pilot count outside bounds")
    defects = record["unique_meaningful_defects"]
    if not isinstance(defects, list):
        raise AssertionError("defect evidence must be a list")
    for defect in defects:
        if not isinstance(defect, Mapping) or any(not _text(defect.get(field)) for field in DEFECT_FIELDS):
            raise AssertionError("meaningful defect evidence incomplete")
    if not _texts(record["known_or_duplicate_findings"], allow_empty=True):
        raise AssertionError("known finding evidence invalid")
    adoption = record["broader_adoption_decision"]
    if record["decision"] == "PILOT_RETAINED":
        if adoption != "RETAIN_BOUNDED_PILOT" or not defects:
            raise AssertionError("pilot retained without unique meaningful defect")
    if record["decision"] == "PILOT_REJECTED":
        if adoption != "REJECT_BROADER_ADOPTION" or defects:
            raise AssertionError("pilot rejection evidence inconsistent")
        gain = str(record["measurable_gain"]).lower()
        if "no unique" not in gain and "zero unique" not in gain:
            raise AssertionError("rejection lacks zero-gain evidence")


def valid_rejected_record() -> dict[str, object]:
    result = run_bounded_pilot()
    return {
        "pilot_applicable": True,
        "no_pilot_evidence": [],
        "q23_deterministic_baseline_complete": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "canonical_owner": "KPR-12-005 and Q11",
        "canonical_facade": "tools/brick_wall_q23_mcard_transition_contract.py",
        "pilot_kind": "STANDARD_LIBRARY_BOUNDED_EXHAUSTIVE",
        "dependency_scope": "OPTIONAL_VALIDATION_ONLY_NO_GLOBAL_DEPENDENCY",
        "properties": list(PILOT_PROPERTIES),
        "generator_strategy": "Cartesian transition inputs plus state-target sequences through depth three",
        "replay_strategy": "Exact serialized case or start/target sequence; exhaustive order is deterministic",
        "minimization_strategy": "First lexicographic mismatch is retained as the minimal counterexample",
        "bounds": {"max_transition_cases": 25_000, "max_sequences": 35_000, "max_sequence_depth": 3, "time_budget_seconds": 120},
        "generated_transition_cases": result["transition_cases"],
        "generated_sequences": result["sequences"],
        "unique_meaningful_defects": [],
        "known_or_duplicate_findings": ["All generated cases reproduced the deterministic Q23 invariants; no independent mismatch was found."],
        "measurable_gain": "Zero unique meaningful defects beyond deterministic Q23 coverage.",
        "operational_cost": "A global property-testing dependency or broader suite would add maintenance cost without demonstrated defect yield.",
        "broader_adoption_decision": "REJECT_BROADER_ADOPTION",
        "unresolved_fields": [],
        "decision": "PILOT_REJECTED",
        "may_proceed_to_q25": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_retained_record() -> dict[str, object]:
    record = valid_rejected_record()
    record.update(
        unique_meaningful_defects=[{
            "defect_id": "mcard-property-unique-001",
            "invariant": PILOT_PROPERTIES[0],
            "minimal_counterexample": "CARD_READ -> CARD_EJECTED",
            "replay": "Replay serialized case mcard-property-unique-001",
            "owner": "KPR-12-005 and Q11",
        }],
        measurable_gain="One unique meaningful defect not represented by deterministic Q23 cases.",
        operational_cost="Bounded validation-only retention has lower cost than the demonstrated defect risk.",
        broader_adoption_decision="RETAIN_BOUNDED_PILOT",
        decision="PILOT_RETAINED",
    )
    return record


def valid_not_applicable_record() -> dict[str, object]:
    record = valid_rejected_record()
    record.update(
        pilot_applicable=False,
        no_pilot_evidence=["No MCard lifecycle behavior or state-machine surface is in scope."],
        generated_transition_cases=0,
        generated_sequences=0,
        unique_meaningful_defects=[],
        known_or_duplicate_findings=[],
        broader_adoption_decision="NOT_APPLICABLE",
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    return deepcopy(valid_rejected_record())
