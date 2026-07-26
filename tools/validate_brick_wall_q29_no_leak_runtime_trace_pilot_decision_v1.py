"""Validate Brick Wall Q29 NO-LEAK runtime trace pilot decision."""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from brick_wall_q29_no_leak_runtime_trace_pilot_contract import (
    ACTIONS,
    classify_relative_path_attribution,
    mutated_record,
    run_bounded_pilot,
    valid_not_applicable_record,
    valid_rejected_record,
    valid_retained_record,
    validate_record,
)

__all__: list[str] = []
FEATURE_ID = "brick-wall-q29-no-leak-runtime-trace-pilot-decision-enforcement-v1"
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
Q28_REL = Path("tools/validate_brick_wall_q28_structured_exception_provenance_v1.py")
PROBE_REL = Path("tools/brick_wall_q29_runtime_trace_probe.py")
CONTRACT_REL = Path(
    "tools/brick_wall_q29_no_leak_runtime_trace_pilot_contract.py"
)
VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q29_no_leak_runtime_trace_pilot_decision_v1.py"
)
BRICK_MARKERS = (
    "### NO-LEAK runtime trace pilot decision (Q29)",
    "NO-LEAK RUNTIME TRACE PILOT DECISION RECORD",
    "writes/deletes/replacements/archive operations/subprocesses/imports",
    "never claim a security sandbox",
    "proceed to Q30 human confirmation and freeze protection YES/NO",
)
BRIDGE_MARKERS = (
    "## NO-LEAK runtime trace pilot decision gate (Q29)",
    "Q29 NO-LEAK runtime trace pilot decision record complete: YES / NO",
    "May proceed to Q30 human confirmation and freeze protection gate: YES / NO",
    "## NO-LEAK runtime trace pilot bridge",
)


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        suffix = " - " + detail if detail else ""
        raise AssertionError(label + ": FAIL" + suffix)
    suffix = " - " + detail if detail else ""
    print(label + ": PASS" + suffix)


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(item) for item in str(value).split("."))
    except ValueError:
        return ()


def _metadata_is_current(meta: Mapping[str, object], minimum_q: int) -> bool:
    stage = str(meta.get("source_stage") or "")
    updated_for = str(meta.get("updated_for") or "")
    match = re.fullmatch(r"brick-wall-q(\d+)-.+", stage)
    return bool(match and stage == updated_for and int(match.group(1)) >= minimum_q)


def _precode(text: str, minimum: int) -> bool:
    match = re.search(
        r"After Q(\d+), all applicable pre-code items.*?"
        r"Q01-Q(\d+) complete YES/NO",
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
    q28 = _read(root / Q28_REL)
    _require(brick, BRICK_MARKERS, "Q29_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q29_ROUTER_BRIDGE_CONTRACT")
    _gate("Q29_BRICK_VERSION", _version(brick_meta.get("version")) >= (3, 9))
    _gate("Q29_BRIDGE_VERSION", _version(bridge_meta.get("version")) >= (4, 3))
    _gate(
        "Q29_BRICK_HEADER_METADATA_VERSION_ALIGNMENT",
        f"version: {brick_meta.get('version')}" in brick,
    )
    _gate(
        "Q29_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT",
        f"version: {bridge_meta.get('version')}" in bridge,
    )
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        _gate(
            "Q29_METADATA_ALIGNMENT",
            _metadata_is_current(meta, 29),
            label,
        )
    _gate("Q29_PRECODE_PROGRESSION", _precode(brick, 29))
    _gate(
        "Q29_FORWARD_COMPATIBLE_Q30_PROGRESSION",
        "Human confirmation and freeze protection (Q30)" in brick
        and "May proceed to Q31" in bridge,
    )
    _gate(
        "Q28_FORWARD_COMPATIBLE_Q29_PROGRESSION",
        "Q28_FORWARD_COMPATIBLE_Q29_PROGRESSION" in q28,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q28_REL,
        PROBE_REL,
        CONTRACT_REL,
        VALIDATOR_REL,
    ):
        _gate(
            "Q29_MODULE_SIZE",
            len(_read(root / rel).splitlines()) <= 500,
            str(rel),
        )


def _reject_record(
    label: str,
    result: Mapping[str, object],
    mutate: Callable[[dict[str, object]], None],
) -> None:
    record = mutated_record(result)
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_governance_record(result: Mapping[str, object]) -> None:
    validate_record(valid_rejected_record(result))
    _gate("Q29_PILOT_REJECTED_RECORD_ACCEPTED", True)
    validate_record(valid_retained_record(result))
    _gate("Q29_PILOT_RETAINED_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record(result))
    _gate("Q29_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests = (
        ("Q29_NEGATIVE_Q28_BASELINE", lambda r: r.update(q28_decision_complete=False)),
        ("Q29_NEGATIVE_OWNER_INVENTORY", lambda r: r.update(canonical_owners=[])),
        (
            "Q29_NEGATIVE_RUNTIME_INTEGRATION",
            lambda r: r.update(application_runtime_integration=True),
        ),
        (
            "Q29_NEGATIVE_SECURITY_SANDBOX_CLAIM",
            lambda r: r.update(security_sandbox_claimed=True),
        ),
        (
            "Q29_NEGATIVE_ACTION_INVENTORY",
            lambda r: r.update(observed_actions=list(ACTIONS[:-1])),
        ),
        (
            "Q29_NEGATIVE_UNBOUNDED_EVENTS",
            lambda r: r["bounds"].update(max_events=50001),
        ),
        (
            "Q29_NEGATIVE_RETAIN_WITHOUT_DEFECT",
            lambda r: r.update(
                decision="PILOT_RETAINED",
                broader_adoption_decision="RETAIN_BOUNDED_HIGH_RISK_VALIDATION_ONLY",
                false_assurance_risks=[],
            ),
        ),
        (
            "Q29_NEGATIVE_REJECT_WITH_DEFECT",
            lambda r: r.update(unique_meaningful_defects=["unresolved defect"]),
        ),
        (
            "Q29_NEGATIVE_REJECT_WITHOUT_LIMITATIONS",
            lambda r: r.update(false_assurance_risks=[]),
        ),
        (
            "Q29_NEGATIVE_ATTRIBUTION_MODEL_MISSING",
            lambda r: r.update(relative_path_attribution_unresolved=False),
        ),
        (
            "Q29_NEGATIVE_Q30_PROGRESSION",
            lambda r: r.update(may_proceed_to_q30=False),
        ),
        ("Q29_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q29_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in tests:
        _reject_record(label, result, mutate)
    record = deepcopy(valid_not_applicable_record(result))
    record["no_pilot_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q29_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q29_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q29_NO_LEAK_RUNTIME_TRACE_PILOT_DECISION_REGRESSION_SET: PASS")


def _decision_projection(result: Mapping[str, object]) -> dict[str, object]:
    keys = (
        "synthetic_categories",
        "q20_categories",
        "relative_path_attribution_unresolved",
        "relative_path_attribution_runtime_observed",
        "relative_path_attribution_evidence_mode",
        "child_process_side_effects_unobserved",
        "unique_meaningful_defects",
        "known_or_duplicate_findings",
        "false_assurance_risks",
    )
    return {key: result[key] for key in keys}


def validate_runtime(root: Path, first: Mapping[str, object]) -> None:
    second = run_bounded_pilot(root)
    _gate("Q29_PILOT_REPLAY_DETERMINISTIC", _decision_projection(first) == _decision_projection(second))
    _gate(
        "Q29_SYNTHETIC_ACTION_COVERAGE",
        set(first["synthetic_categories"]) == set(ACTIONS),
    )
    _gate(
        "Q29_Q20_KNOWN_SIDE_EFFECTS_OBSERVED",
        {"writes", "deletes", "imports"}.issubset(set(first["q20_categories"])),
    )
    _gate(
        "Q29_RELATIVE_PATH_ATTRIBUTION_LIMITATION",
        bool(first["relative_path_attribution_unresolved"]),
    )
    runtime_status = (
        "OBSERVED"
        if first["relative_path_attribution_runtime_observed"]
        else "NOT_OBSERVED_PLATFORM_DEPENDENT"
    )
    _gate(
        "Q29_RELATIVE_PATH_ATTRIBUTION_RUNTIME_STATUS",
        runtime_status in {"OBSERVED", "NOT_OBSERVED_PLATFORM_DEPENDENT"},
        runtime_status,
    )
    _gate(
        "Q29_RELATIVE_PATH_ATTRIBUTION_EVIDENCE_MODE",
        first["relative_path_attribution_evidence_mode"] in {
            "RUNTIME_AND_DETERMINISTIC_MODEL",
            "DETERMINISTIC_MODEL_ONLY_PLATFORM_DEPENDENT_RUNTIME",
        },
        str(first["relative_path_attribution_evidence_mode"]),
    )
    modeled, runtime_observed, evidence_mode = classify_relative_path_attribution(
        [],
        [
            {
                "path_attribution": "DIR_FD_RELATIVE_UNRESOLVED",
            }
        ],
    )
    _gate(
        "Q29_PLATFORM_NO_RUNTIME_DIR_FD_ACCEPTED",
        modeled
        and not runtime_observed
        and evidence_mode
        == "DETERMINISTIC_MODEL_ONLY_PLATFORM_DEPENDENT_RUNTIME",
    )
    _gate(
        "Q29_CHILD_PROCESS_VISIBILITY_LIMITATION",
        bool(first["child_process_side_effects_unobserved"]),
    )
    _gate("Q29_UNIQUE_MEANINGFUL_DEFECTS_ZERO", not first["unique_meaningful_defects"])
    _gate("Q29_KNOWN_OR_DUPLICATE_FINDINGS_ONLY", bool(first["known_or_duplicate_findings"]))
    _gate("Q29_FALSE_ASSURANCE_RISKS_RECORDED", bool(first["false_assurance_risks"]))
    rejected = valid_rejected_record(first)
    validate_record(rejected)
    _gate("Q29_BROADER_ADOPTION_REJECTED", rejected["decision"] == "PILOT_REJECTED")
    _gate("Q29_NO_APPLICATION_RUNTIME_INTEGRATION", not rejected["application_runtime_integration"])
    _gate("Q29_NO_SECURITY_SANDBOX_CLAIM", not rejected["security_sandbox_claimed"])
    print("Q29_RUNTIME_NO_LEAK_TRACE_PILOT: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    result = run_bounded_pilot(root)
    validate_governance_record(result)
    validate_runtime(root, result)
    print(
        "VALIDATION OK: "
        "brick-wall-q29-no-leak-runtime-trace-pilot-decision-enforcement-v1"
    )
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
