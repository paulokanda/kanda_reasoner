"""Validate Brick Wall Q28 structured exception provenance."""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Callable, Sequence

from brick_wall_q28_structured_exception_provenance_contract import (
    FAILURE_CLASSES,
    capture_exception_provenance,
    mutated_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

__all__: list[str] = []
FEATURE_ID = "brick-wall-q28-structured-exception-provenance-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / (
    "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRIDGE_REL = PLIB / (
    "ACTIVE_PROMPTS/05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
Q27_REL = Path("tools/validate_brick_wall_q27_control_byte_encoding_guards_v1.py")
CONTRACT_REL = Path("tools/brick_wall_q28_structured_exception_provenance_contract.py")
VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q28_structured_exception_provenance_v1.py"
)
BRICK_MARKERS = (
    "### Structured exception provenance (Q28)",
    "STRUCTURED EXCEPTION PROVENANCE RECORD",
    "last successful marker",
    "SETUP/BEHAVIOR/CLEANUP/EVIDENCE",
    "proceed to Q29 NO-LEAK runtime trace pilot decision YES/NO",
)
BRIDGE_MARKERS = (
    "## Structured exception provenance gate (Q28)",
    "Q28 structured exception provenance record complete: YES / NO",
    "May proceed to Q29 NO-LEAK runtime trace pilot decision: YES / NO",
    "## Structured exception provenance bridge",
)


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


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
        return tuple(int(item) for item in str(value).split("."))
    except ValueError:
        return ()


def _precode(text: str, minimum: int) -> bool:
    match = re.search(
        r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO",
        text,
        re.DOTALL,
    )
    return bool(
        match
        and match.group(1) == match.group(2)
        and int(match.group(1)) >= minimum
    )


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    q27 = _read(root / Q27_REL)
    _require(brick, BRICK_MARKERS, "Q28_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q28_ROUTER_BRIDGE_CONTRACT")
    _gate("Q28_BRICK_VERSION", _version(brick_meta.get("version")) >= (3, 8))
    _gate("Q28_BRIDGE_VERSION", _version(bridge_meta.get("version")) >= (4, 2))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        _gate(
            "Q28_METADATA_ALIGNMENT",
            meta.get("source_stage") == meta.get("updated_for")
            and re.fullmatch(r"brick-wall-q(\d+)-.+", str(meta.get("source_stage") or "")) is not None
            and int(re.fullmatch(r"brick-wall-q(\d+)-.+", str(meta.get("source_stage") or "")).group(1)) >= 28,
            label,
        )
    _gate("Q28_PRECODE_PROGRESSION", _precode(brick, 28))
    _gate(
        "Q28_FORWARD_COMPATIBLE_Q29_PROGRESSION",
        "### NO-LEAK runtime trace pilot decision (Q29)" in brick
        and "## NO-LEAK runtime trace pilot decision gate (Q29)" in bridge,
    )
    _gate(
        "Q27_FORWARD_COMPATIBLE_Q28_PROGRESSION",
        "Q27_FORWARD_COMPATIBLE_Q28_PROGRESSION" in q27,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q27_REL,
        CONTRACT_REL,
        VALIDATOR_REL,
    ):
        _gate("Q28_MODULE_SIZE", len(_read(root / rel).splitlines()) <= 500, str(rel))


def _reject_record(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_governance_record() -> None:
    validate_record(valid_complete_record())
    _gate("Q28_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q28_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests = (
        ("Q28_NEGATIVE_Q27_BASELINE", lambda r: r.update(q27_decision_complete=False)),
        ("Q28_NEGATIVE_OWNER_INVENTORY", lambda r: r.update(canonical_owners=["other"])),
        ("Q28_NEGATIVE_PHASE_MISSING", lambda r: r["cases"][0].update(operation_phase="")),
        ("Q28_NEGATIVE_OPERATION_ID", lambda r: r["cases"][0].update(operation_id="")),
        ("Q28_NEGATIVE_TARGET", lambda r: r["cases"][0].update(target="")),
        (
            "Q28_NEGATIVE_ROOT_CLASSIFICATION",
            lambda r: r["cases"][0].update(root_classification="UNKNOWN"),
        ),
        (
            "Q28_NEGATIVE_LAST_SUCCESSFUL_MARKER",
            lambda r: r["cases"][0].update(last_successful_marker=""),
        ),
        (
            "Q28_NEGATIVE_FAILURE_CLASS",
            lambda r: r["cases"][0].update(failure_class="OTHER"),
        ),
        (
            "Q28_NEGATIVE_ORIGINAL_CAUSE",
            lambda r: r["cases"][0].update(original_cause_message=""),
        ),
        (
            "Q28_NEGATIVE_INVOCATION_POSITION",
            lambda r: r["cases"][0].update(invocation_position=""),
        ),
        ("Q28_NEGATIVE_Q29_PROGRESSION", lambda r: r.update(may_proceed_to_q29=False)),
        ("Q28_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q28_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in tests:
        _reject_record(label, mutate)
    incomplete = mutated_record()
    incomplete["cases"] = incomplete["cases"][:-1]
    try:
        validate_record(incomplete)
    except AssertionError:
        _gate("Q28_NEGATIVE_FAILURE_CLASS_INVENTORY", True)
    else:
        _gate("Q28_NEGATIVE_FAILURE_CLASS_INVENTORY", False)
    duplicate = mutated_record()
    duplicate["cases"][1]["case_id"] = duplicate["cases"][0]["case_id"]
    try:
        validate_record(duplicate)
    except AssertionError:
        _gate("Q28_NEGATIVE_DUPLICATE_CASE", True)
    else:
        _gate("Q28_NEGATIVE_DUPLICATE_CASE", False)
    record = deepcopy(valid_not_applicable_record())
    record["no_provenance_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q28_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q28_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q28_STRUCTURED_EXCEPTION_PROVENANCE_REGRESSION_SET: PASS")


def _raise_chained_failure() -> None:
    try:
        raise FileNotFoundError("missing payload fixture")
    except FileNotFoundError as exc:
        raise RuntimeError("install behavior failed") from exc


def validate_runtime() -> None:
    try:
        _raise_chained_failure()
    except RuntimeError as exc:
        captured = capture_exception_provenance(
            exc,
            operation_phase="install_payload",
            operation_id="operation-q28-runtime",
            target="payload/tools/example.py",
            root_classification="TOOL_SOURCE",
            last_successful_marker="Q28_SETUP_PRECONDITION: PASS",
            failure_class="BEHAVIOR",
            invocation_position="INSTALL.py:120",
        )
    else:
        raise AssertionError("Q28 runtime fixture did not fail")
    _gate(
        "Q28_ORIGINAL_CAUSE_CHAIN_PRESERVED",
        captured["original_cause_type"] == "FileNotFoundError"
        and captured["original_cause_message"] == "missing payload fixture",
    )
    _gate("Q28_OPERATION_PHASE_PROVENANCE", captured["operation_phase"] == "install_payload")
    _gate("Q28_OPERATION_ID_PROVENANCE", captured["operation_id"] == "operation-q28-runtime")
    _gate(
        "Q28_TARGET_AND_ROOT_CLASSIFICATION",
        captured["target"] == "payload/tools/example.py"
        and captured["root_classification"] == "TOOL_SOURCE",
    )
    _gate(
        "Q28_LAST_SUCCESSFUL_MARKER_PRESERVED",
        captured["last_successful_marker"] == "Q28_SETUP_PRECONDITION: PASS",
    )
    _gate(
        "Q28_FAILURE_CLASS_DISTINCTION",
        set(FAILURE_CLASSES) == {"SETUP", "BEHAVIOR", "CLEANUP", "EVIDENCE"},
    )
    _gate(
        "Q28_INVOCATION_POSITION_PRESERVED",
        captured["invocation_position"] == "INSTALL.py:120",
    )
    print("Q28_RUNTIME_STRUCTURED_EXCEPTION_PROVENANCE: PASS")


def run_validation(root: Path) -> None:
    validate_source(root)
    validate_governance_record()
    validate_runtime()
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
