"""Validate Brick Wall Q23 deterministic MCard transition governance."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Callable, Sequence

from brick_wall_q23_mcard_transition_contract import (
    DURABLE_ARTIFACTS,
    mutated_record,
    validate_record,
    valid_not_applicable_record,
    valid_required_record,
)

__all__: list[str] = []

FEATURE_ID = "brick-wall-q23-deterministic-mcard-transition-tests-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
BRIDGE_REL = PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
CANON_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/architecture_review_project_card_machine_canon.md"
Q11_REL = Path("tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py")
Q22_REL = Path("tools/validate_brick_wall_q22_public_facade_contract_drift_v1.py")
LIFECYCLE_REL = Path("tools/validate_architecture_review_project_card_lifecycle_v1.py")
CANON_ROUTER_REL = Path("tools/validate_architecture_review_project_card_machine_canon_router_v1.py")
CONTRACT_REL = Path("tools/brick_wall_q23_mcard_transition_contract.py")
VALIDATOR_REL = Path("tools/validate_brick_wall_q23_deterministic_mcard_transition_tests_v1.py")

BRICK_MARKERS = (
    "### Deterministic MCard transition tests (Q23)",
    "DETERMINISTIC MCARD TRANSITION TEST RECORD",
    "normal and rollback paths complete",
    "premature-eject",
    "terminal eject clears target-specific Tool memory only",
    "proceed to Q24 property-based MCard pilot decision YES/NO",
)
BRIDGE_MARKERS = (
    "## Deterministic MCard transition tests gate (Q23)",
    "Q23 deterministic MCard transition test record complete: YES / NO",
    "May proceed to Q24 property-based MCard pilot decision gate: YES / NO",
    "## Deterministic MCard transition bridge",
    "Terminal eject clears target-specific Tool memory only",
)
CANON_MARKERS = (
    "## Lifecycle state machine",
    "Rollback path:",
    "Open transactions block switch, snapshot replacement, and eject.",
    "### Terminal eject",
    "retain project-owned source changes",
    "retain generated helper files",
    "retain canonical Preview/evidence",
    "retain transaction records",
    "retain mutation-lane state",
    "retain RefactorReceipt",
)
OWNER_MARKERS = {
    Q11_REL: ("VALID_TRANSITIONS =", "premature card eject", "terminal eject destroyed Project results"),
    LIFECYCLE_REL: ("OPEN_TRANSACTION_BLOCKS_CARD_EJECTION: PASS", "COMPLETED_REFACTOR_RELEASES_TOOL_CARD_MEMORY: PASS", "WORKBENCH_TRANSACTION_STATE_PROJECT_SUPPORT_ONLY: PASS"),
    CANON_ROUTER_REL: ("CARD_MACHINE_CANON_PRINCIPLE: PASS", "CARD_MACHINE_AND_TOOL_PROJECT_CANONS_COMPLEMENTARY: PASS"),
}


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError:
        return ()


def _precode_gate_at_least(text: str, minimum_gate: int) -> bool:
    match = re.search(r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO", text, re.DOTALL)
    return bool(match and match.group(1) == match.group(2) and int(match.group(1)) >= minimum_gate)


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL); bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL); bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q23_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q23_ROUTER_BRIDGE_CONTRACT")
    _require(_read(root / CANON_REL), CANON_MARKERS, "Q23_CANONICAL_MCARD_OWNER")
    _gate("Q23_BRICK_VERSION", _version(brick_meta.get("version")) >= (3, 3))
    _gate("Q23_BRIDGE_VERSION", _version(bridge_meta.get("version")) >= (3, 7))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = str(meta.get("source_stage", ""))
        updated = str(meta.get("updated_for", ""))
        match = re.search(r"brick-wall-q(\d+)-", stage)
        _gate("Q23_METADATA_ALIGNMENT", stage == updated and bool(match) and int(match.group(1)) >= 23, label)
    _gate("Q23_PRECODE_PROGRESSION", _precode_gate_at_least(brick, 23))
    _gate("Q23_FORWARD_COMPATIBLE_Q24_PRECODE_PROGRESSION", _precode_gate_at_least(brick, 24))
    _gate("Q22_FORWARD_COMPATIBLE_Q23_PROGRESSION", "Q22_FORWARD_COMPATIBLE_Q23_PRECODE_PROGRESSION" in _read(root / Q22_REL))
    for rel, markers in OWNER_MARKERS.items():
        _require(_read(root / rel), markers, "Q23_EXISTING_MCARD_VALIDATOR_OWNER")
    for rel in (BRICK_REL, BRIDGE_REL, Q11_REL, Q22_REL, LIFECYCLE_REL, CANON_ROUTER_REL, CONTRACT_REL, VALIDATOR_REL):
        _gate("Q23_MODULE_SIZE", len(_read(root / rel).splitlines()) <= 500, f"{rel}")


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record(); mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_contract() -> None:
    validate_record(valid_required_record()); _gate("Q23_REQUIRED_TRANSITION_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record()); _gate("Q23_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests: list[tuple[str, Callable[[dict[str, object]], None]]] = [
        ("Q23_NEGATIVE_DUPLICATE_CASE", lambda r: r["cases"].append(dict(r["cases"][0]))),
        ("Q23_NEGATIVE_VALID_TRANSITION_INVENTORY", lambda r: r["valid_transitions"].pop()),
        ("Q23_NEGATIVE_NORMAL_PATH_MISSING", lambda r: r.update(cases=[c for c in r["cases"] if c["path_kind"] != "NORMAL"])),
        ("Q23_NEGATIVE_ROLLBACK_PATH_MISSING", lambda r: r.update(cases=[c for c in r["cases"] if c["path_kind"] != "ROLLBACK"])),
        ("Q23_NEGATIVE_SKIPPED_TRANSITION_ALLOWED", lambda r: r["cases"][5].update(expected_allowed=True, expected_blockers=[])),
        ("Q23_NEGATIVE_STALE_GENERATION_ALLOWED", lambda r: r["cases"][6].update(expected_allowed=True, expected_blockers=[])),
        ("Q23_NEGATIVE_TRANSACTION_EJECT_UNLOCKED", lambda r: r["cases"][7].update(open_transaction=False, expected_allowed=True, expected_blockers=[])),
        ("Q23_NEGATIVE_PREMATURE_EJECT_ALLOWED", lambda r: r["cases"][8].update(expected_allowed=True, expected_blockers=[])),
        ("Q23_NEGATIVE_DESTRUCTIVE_EJECT", lambda r: r["cases"][1].update(durable_state_after={name: False for name in DURABLE_ARTIFACTS})),
        ("Q23_NEGATIVE_TOOL_MEMORY_RETAINED_AFTER_EJECT", lambda r: r["cases"][1].update(tool_memory_after={"card": "retained"})),
        ("Q23_NEGATIVE_Q24_PROGRESSION", lambda r: r.update(may_proceed_to_q24=False)),
        ("Q23_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q23_NEGATIVE_SOURCE_WRITE_AUTHORIZATION", lambda r: r.update(may_write_source=True)),
    ]
    for label, mutate in tests:
        _reject(label, mutate)
    record = valid_not_applicable_record(); record["no_test_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q23_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q23_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q23_DETERMINISTIC_MCARD_TRANSITION_REGRESSION_SET: PASS")


def validate_runtime_matrix() -> None:
    record = valid_required_record(); validate_record(record)
    cases = record["cases"]
    _gate("Q23_NORMAL_TRANSITION_PATHS", sum(c["expected_allowed"] for c in cases if c["path_kind"] == "NORMAL") >= 2)
    _gate("Q23_ROLLBACK_TRANSITION_PATHS", sum(c["expected_allowed"] for c in cases if c["path_kind"] == "ROLLBACK") >= 3)
    _gate("Q23_INVALID_TRANSITIONS_BLOCKED", all(not c["expected_allowed"] for c in cases if c["path_kind"] in {"SKIPPED", "STALE", "LOCKED", "PREMATURE_EJECT", "DESTRUCTIVE_EJECT"}))
    ejects = [c for c in cases if c["expected_allowed"] and c["to_state"] == "CARD_EJECTED"]
    _gate("Q23_TERMINAL_EJECT_CLEARS_TOOL_MEMORY", bool(ejects) and all(not c["tool_memory_after"] for c in ejects))
    _gate("Q23_DURABLE_PROJECT_STATE_PRESERVED", bool(ejects) and all(c["durable_state_before"] == c["durable_state_after"] for c in ejects))
    print("Q23_RUNTIME_DETERMINISTIC_MCARD_TRANSITIONS: PASS")


def run_validation(root: Path) -> None:
    validate_source(root); validate_contract(); validate_runtime_matrix()
    print("VALIDATION OK: " + FEATURE_ID); print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--project-root", type=Path, default=Path.cwd()); args = parser.parse_args()
    run_validation(args.project_root.expanduser().resolve()); return 0


if __name__ == "__main__":
    raise SystemExit(main())
