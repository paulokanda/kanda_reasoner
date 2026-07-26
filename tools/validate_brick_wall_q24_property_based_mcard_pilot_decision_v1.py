"""Validate Brick Wall Q24 property-based MCard pilot decision governance."""
from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Callable, Sequence

from brick_wall_q24_property_based_mcard_pilot_contract import (
    mutated_record,
    run_bounded_pilot,
    validate_record,
    valid_not_applicable_record,
    valid_rejected_record,
    valid_retained_record,
)

__all__: list[str] = []

FEATURE_ID = "brick-wall-q24-property-based-mcard-pilot-decision-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
BRIDGE_REL = PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
Q23_REL = Path("tools/validate_brick_wall_q23_deterministic_mcard_transition_tests_v1.py")
Q23_CONTRACT_REL = Path("tools/brick_wall_q23_mcard_transition_contract.py")
CONTRACT_REL = Path("tools/brick_wall_q24_property_based_mcard_pilot_contract.py")
VALIDATOR_REL = Path("tools/validate_brick_wall_q24_property_based_mcard_pilot_decision_v1.py")

BRICK_MARKERS = (
    "### Property-based MCard pilot decision (Q24)",
    "PROPERTY-BASED MCARD PILOT DECISION RECORD",
    "optional validation pilot, never a global runtime dependency",
    "unique meaningful defects",
    "PILOT_RETAINED/PILOT_REJECTED/NOT_APPLICABLE/BLOCKED",
    "proceed to Q25 mutation-testing pilot decision YES/NO",
)
BRIDGE_MARKERS = (
    "## Property-based MCard pilot decision gate (Q24)",
    "Q24 property-based MCard pilot decision record complete: YES / NO",
    "Property-based pilot decision: PILOT_RETAINED / PILOT_REJECTED / NOT_APPLICABLE / BLOCKED",
    "May proceed to Q25 mutation-testing pilot decision gate: YES / NO",
    "## Property-based MCard pilot bridge",
    "No broad adoption without unique meaningful defects",
)


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


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
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q24_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q24_ROUTER_BRIDGE_CONTRACT")
    _gate("Q24_BRICK_VERSION", _version(brick_meta.get("version")) >= (3, 4))
    _gate("Q24_BRIDGE_VERSION", _version(bridge_meta.get("version")) >= (3, 8))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q24_METADATA_ALIGNMENT", isinstance(stage, str) and bool(stage.strip()) and stage == updated, label)
    _gate("Q24_FORWARD_COMPATIBLE_Q25_METADATA", all(meta.get("source_stage") == meta.get("updated_for") for meta in (brick_meta, bridge_meta)))
    _gate("Q24_PRECODE_PROGRESSION", _precode_gate_at_least(brick, 24))
    _gate("Q24_FORWARD_COMPATIBLE_Q25_PRECODE_PROGRESSION", _precode_gate_at_least(brick, 25))
    _gate("Q23_FORWARD_COMPATIBLE_Q24_PROGRESSION", "Q23_FORWARD_COMPATIBLE_Q24_PRECODE_PROGRESSION" in _read(root / Q23_REL))
    _require(_read(root / Q23_CONTRACT_REL), ("def expected_blockers", "VALID_TRANSITIONS", "terminal eject lost durable project state"), "Q24_CANONICAL_Q23_OWNER_REUSED")
    for rel in (BRICK_REL, BRIDGE_REL, Q23_REL, Q23_CONTRACT_REL, CONTRACT_REL, VALIDATOR_REL):
        _gate("Q24_MODULE_SIZE", len(_read(root / rel).splitlines()) <= 500, str(rel))


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_contract() -> None:
    validate_record(valid_rejected_record())
    _gate("Q24_PILOT_REJECTED_RECORD_ACCEPTED", True)
    validate_record(valid_retained_record())
    _gate("Q24_PILOT_RETAINED_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q24_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests: list[tuple[str, Callable[[dict[str, object]], None]]] = [
        ("Q24_NEGATIVE_Q23_BASELINE_INCOMPLETE", lambda r: r.update(q23_deterministic_baseline_complete=False)),
        ("Q24_NEGATIVE_GLOBAL_DEPENDENCY", lambda r: r.update(dependency_scope="MANDATORY_GLOBAL_RUNTIME_DEPENDENCY")),
        ("Q24_NEGATIVE_PROPERTY_INVENTORY", lambda r: r["properties"].pop()),
        ("Q24_NEGATIVE_GENERATOR_MISSING", lambda r: r.update(generator_strategy="")),
        ("Q24_NEGATIVE_REPLAY_MISSING", lambda r: r.update(replay_strategy="")),
        ("Q24_NEGATIVE_MINIMIZATION_MISSING", lambda r: r.update(minimization_strategy="")),
        ("Q24_NEGATIVE_UNBOUNDED_CASES", lambda r: r["bounds"].update(max_transition_cases=1_000_000)),
        ("Q24_NEGATIVE_UNBOUNDED_DEPTH", lambda r: r["bounds"].update(max_sequence_depth=100)),
        ("Q24_NEGATIVE_RESULT_OUTSIDE_BOUND", lambda r: r.update(generated_sequences=50_000)),
        ("Q24_NEGATIVE_RETAIN_WITHOUT_UNIQUE_DEFECT", lambda r: r.update(decision="PILOT_RETAINED", broader_adoption_decision="RETAIN_BOUNDED_PILOT")),
        ("Q24_NEGATIVE_REJECT_WITH_DEFECT", lambda r: r.update(unique_meaningful_defects=deepcopy(valid_retained_record()["unique_meaningful_defects"]))),
        ("Q24_NEGATIVE_COST_EVIDENCE_MISSING", lambda r: r.update(operational_cost="")),
        ("Q24_NEGATIVE_Q25_PROGRESSION", lambda r: r.update(may_proceed_to_q25=False)),
        ("Q24_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q24_NEGATIVE_SOURCE_WRITE_AUTHORIZATION", lambda r: r.update(may_write_source=True)),
    ]
    for label, mutate in tests:
        _reject(label, mutate)
    record = valid_not_applicable_record()
    record["no_pilot_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q24_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q24_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q24_PROPERTY_BASED_MCARD_PILOT_DECISION_REGRESSION_SET: PASS")


def validate_runtime_pilot() -> None:
    first = run_bounded_pilot()
    second = run_bounded_pilot()
    _gate("Q24_PROPERTY_PILOT_TRANSITION_CASES", first["transition_cases"] == 21_632)
    _gate("Q24_PROPERTY_PILOT_SEQUENCE_CASES", first["sequences"] == 30_927)
    _gate("Q24_PROPERTY_PILOT_REPLAY_DETERMINISTIC", first == second)
    _gate("Q24_PROPERTY_PILOT_INDEPENDENT_ORACLE", not first["transition_mismatches"] and not first["sequence_mismatches"])
    record = valid_rejected_record()
    validate_record(record)
    _gate("Q24_NO_GLOBAL_PROPERTY_DEPENDENCY", record["dependency_scope"] == "OPTIONAL_VALIDATION_ONLY_NO_GLOBAL_DEPENDENCY")
    _gate("Q24_UNIQUE_MEANINGFUL_DEFECTS_ZERO", len(record["unique_meaningful_defects"]) == 0)
    _gate("Q24_BROADER_ADOPTION_REJECTED", record["broader_adoption_decision"] == "REJECT_BROADER_ADOPTION")
    print("Q24_RUNTIME_PROPERTY_BASED_MCARD_PILOT: PASS")


def run_validation(root: Path) -> None:
    validate_source(root)
    validate_contract()
    validate_runtime_pilot()
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
