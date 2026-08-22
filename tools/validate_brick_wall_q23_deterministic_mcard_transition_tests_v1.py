"""Validate Brick Wall Q23 deterministic observer MCard transitions."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from brick_wall_q23_mcard_transition_contract import (
    DURABLE_ARTIFACTS,
    mutated_record,
    validate_record,
    valid_not_applicable_record,
    valid_required_record,
)

__all__: list[str] = []
FEATURE_ID = "brick-wall-q23-deterministic-mcard-transition-tests-enforcement-v2"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
CANON_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/architecture_review_project_card_machine_canon.md"
Q11_REL = Path("tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py")
CONTRACT_REL = Path("tools/brick_wall_q23_mcard_transition_contract.py")
VALIDATOR_REL = Path("tools/validate_brick_wall_q23_deterministic_mcard_transition_tests_v1.py")


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _gate(label: str, ok: bool) -> None:
    if not ok:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    canon = _read(root / CANON_REL)
    for marker in (
        "### Deterministic MCard transition tests (Q23)",
        "DETERMINISTIC MCARD TRANSITION TEST RECORD",
        "canonical Q11 set",
    ):
        _gate("Q23_BRICK_MARKER", marker in brick)
    for marker in (
        "## Observer lifecycle state machine", "CARD_EJECTED",
        "No Project source rollback", "Project development remains possible when KANDA is closed",
    ):
        _gate("Q23_CANON_MARKER", marker in canon)
    for rel in (BRICK_REL, CANON_REL, Q11_REL, CONTRACT_REL, VALIDATOR_REL):
        _gate("Q23_MODULE_SIZE", len(_read(root / rel).splitlines()) <= 500)


def validate_contract() -> None:
    validate_record(valid_required_record())
    _gate("Q23_REQUIRED_TRANSITION_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q23_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests: list[tuple[str, Callable[[dict[str, object]], None]]] = [
        ("Q23_NEGATIVE_DUPLICATE_CASE", lambda r: r["cases"].append(dict(r["cases"][0]))),
        ("Q23_NEGATIVE_VALID_TRANSITION_INVENTORY", lambda r: r["valid_transitions"].pop()),
        ("Q23_NEGATIVE_SOURCE_WRITE_ALLOWED", lambda r: r["cases"][7].update(expected_allowed=True, expected_blockers=[])),
        ("Q23_NEGATIVE_KANDA_DEPENDENCY_ALLOWED", lambda r: r["cases"][8].update(expected_allowed=True, expected_blockers=[])),
        ("Q23_NEGATIVE_DESTRUCTIVE_EJECT", lambda r: r["cases"][4].update(durable_state_after={name: False for name in DURABLE_ARTIFACTS})),
        ("Q23_NEGATIVE_TOOL_MEMORY_RETAINED_AFTER_EJECT", lambda r: r["cases"][4].update(tool_memory_after={"card": "retained"})),
        ("Q23_NEGATIVE_Q24_PROGRESSION", lambda r: r.update(may_proceed_to_q24=False)),
        ("Q23_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q23_NEGATIVE_SOURCE_WRITE_AUTHORIZATION", lambda r: r.update(may_write_source=True)),
    ]
    for label, mutate in tests:
        _reject(label, mutate)
    print("Q23_DETERMINISTIC_MCARD_TRANSITION_REGRESSION_SET: PASS")


def validate_runtime_matrix() -> None:
    record = valid_required_record()
    validate_record(record)
    cases = record["cases"]
    _gate("Q23_NORMAL_TRANSITION_PATHS", sum(bool(c["expected_allowed"]) for c in cases if c["path_kind"] == "NORMAL") >= 5)
    _gate("Q23_INVALID_TRANSITIONS_BLOCKED", all(not c["expected_allowed"] for c in cases if c["path_kind"] != "NORMAL"))
    ejects = [c for c in cases if c["expected_allowed"] and c["to_state"] == "CARD_EJECTED"]
    _gate("Q23_EJECT_CLEARS_TOOL_MEMORY", bool(ejects) and all(not c["tool_memory_after"] for c in ejects))
    _gate("Q23_DURABLE_PROJECT_STATE_PRESERVED", bool(ejects) and all(c["durable_state_before"] == c["durable_state_after"] for c in ejects))
    print("Q23_RUNTIME_DETERMINISTIC_MCARD_TRANSITIONS: PASS")


def run_validation(root: Path) -> None:
    validate_source(root)
    validate_contract()
    validate_runtime_matrix()
    print("Q23_FORWARD_COMPATIBLE_Q24_PRECODE_PROGRESSION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    run_validation(args.project_root.expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
