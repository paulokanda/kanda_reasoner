# project-path: tools/validate_brick_wall_q31_changed_file_validator_coverage_map_v1.py
"""Focused Q31 changed-file-to-validator coverage-map validation."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from brick_wall_q31_changed_file_validator_coverage_contract import (
    COVERAGE_KINDS,
    mutated_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

BRICK = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "brick_wall_comprehensive_quality_gate.meta.json"
)
BRIDGE = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)
Q30 = Path(
    "tools/validate_brick_wall_q30_human_confirmation_"
    "freeze_protection_v1.py"
)
CONTRACT = Path(
    "tools/brick_wall_q31_changed_file_validator_coverage_contract.py"
)
SELF = Path(
    "tools/validate_brick_wall_q31_changed_file_validator_"
    "coverage_map_v1.py"
)
FEATURE = "brick-wall-q31-changed-file-validator-coverage-map-enforcement-v1"
Q30_FREEZE_ID = (
    "freeze-20260716-brick-wall-q30-human-confirmation-freeze-"
    "protection-validator-discovery-repair-v1r2"
)
LESSON_REQUIRED_VALIDATOR = (
    "lesson-patch4-regression-validator-required-removed-"
    "patch5-placeholder-v1"
)
LESSON_ROUTE_SCHEMA = (
    "lesson-brick-wall-focused-validator-task-route-key-assumption-v1"
)
LESSON_REAL_WIDGET_IMPORT = (
    "lesson-real-widget-validator-package-root-import-regression-v1"
)

RELEASE_FILES = (
    BRICK,
    BRICK_META,
    BRIDGE,
    BRIDGE_META,
    Q30,
    CONTRACT,
    SELF,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _gate(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _applies(
    validators: list[str],
    markers: list[str],
    reason: str,
) -> dict[str, Any]:
    return {
        "disposition": "APPLIES",
        "validators": validators,
        "expected_markers": markers,
        "reason": reason,
    }


def _not_applicable(reason: str) -> dict[str, Any]:
    return {
        "disposition": "NOT_APPLICABLE",
        "validators": [],
        "expected_markers": [],
        "reason": reason,
    }


def _release_row(
    path: Path,
    *,
    owner_box: str,
    public_contract: str,
    error_memory_lessons: list[str],
    frozen_behavior: list[str],
    focused_markers: list[str],
    boundary: dict[str, Any] | None = None,
    gui: dict[str, Any] | None = None,
    delivery_markers: list[str] | None = None,
    negative_markers: list[str] | None = None,
) -> dict[str, Any]:
    validator = str(SELF).replace("\\", "/")
    return {
        "path": str(path).replace("\\", "/"),
        "owner_box": owner_box,
        "public_contract": public_contract,
        "error_memory_lessons": error_memory_lessons,
        "frozen_behavior": frozen_behavior,
        "focused_tests": _applies(
            [validator],
            focused_markers,
            "The Q31 focused validator checks the current source and release row.",
        ),
        "boundary_tests": boundary
        or _not_applicable(
            "This file does not create cross-box runtime communication; owner and contract are checked statically."
        ),
        "gui_tests": gui
        or _not_applicable(
            "This file changes no GUI or Qt behavior."
        ),
        "delivery_tests": _applies(
            [validator],
            delivery_markers or ["Q31_EXACT_RELEASE_COVERAGE_MAP: PASS"],
            "The exact release matrix and installed payload are checked before delivery.",
        ),
        "negative_tests": _applies(
            [validator],
            negative_markers or ["Q31_NEGATIVE_UNCOVERED_FILE: PASS"],
            "Mutation cases prove missing or conflicting coverage fails closed.",
        ),
    }


def q31_release_record() -> dict[str, Any]:
    validator = str(SELF).replace("\\", "/")
    common_frozen = [Q30_FREEZE_ID]
    rows = [
        _release_row(
            BRICK,
            owner_box="kanda_prompt_workspace/prompt_library",
            public_contract="KPR-03-001 brick_wall_comprehensive_quality_gate",
            error_memory_lessons=[LESSON_REQUIRED_VALIDATOR, LESSON_ROUTE_SCHEMA],
            frozen_behavior=common_frozen,
            focused_markers=["Q31_BRICK_WALL_CONTRACT: PASS"],
        ),
        _release_row(
            BRICK_META,
            owner_box="kanda_prompt_workspace/prompt_library",
            public_contract="brick_wall_comprehensive_quality_gate metadata identity",
            error_memory_lessons=[LESSON_ROUTE_SCHEMA],
            frozen_behavior=common_frozen,
            focused_markers=["Q31_BRICK_METADATA_ALIGNMENT: PASS"],
        ),
        _release_row(
            BRIDGE,
            owner_box="kanda_prompt_workspace/prompt_library",
            public_contract="router_bridge_governed_implementation",
            error_memory_lessons=[LESSON_REQUIRED_VALIDATOR, LESSON_ROUTE_SCHEMA],
            frozen_behavior=common_frozen,
            focused_markers=["Q31_ROUTER_BRIDGE_CONTRACT: PASS"],
        ),
        _release_row(
            BRIDGE_META,
            owner_box="kanda_prompt_workspace/prompt_library",
            public_contract="router_bridge_governed_implementation metadata identity",
            error_memory_lessons=[LESSON_ROUTE_SCHEMA],
            frozen_behavior=common_frozen,
            focused_markers=["Q31_BRIDGE_METADATA_ALIGNMENT: PASS"],
        ),
        _release_row(
            Q30,
            owner_box="tools validation-only support",
            public_contract="Q30 focused validator CLI and markers",
            error_memory_lessons=[LESSON_REQUIRED_VALIDATOR, LESSON_REAL_WIDGET_IMPORT],
            frozen_behavior=common_frozen,
            focused_markers=["Q30_FORWARD_COMPATIBLE_Q31_PROGRESSION: PASS"],
            gui=_not_applicable(
                "The touched Q30 file is the non-Qt focused validator; the frozen real-Qt Q30 validator remains unchanged and required in the cumulative Windows chain."
            ),
        ),
        _release_row(
            CONTRACT,
            owner_box="tools validation-only support",
            public_contract="Q31 validation-only coverage record contract",
            error_memory_lessons=[LESSON_REQUIRED_VALIDATOR],
            frozen_behavior=common_frozen,
            focused_markers=["Q31_COMPLETE_RECORD_ACCEPTED: PASS"],
        ),
        _release_row(
            SELF,
            owner_box="tools validation-only support",
            public_contract="Q31 focused validator CLI and markers",
            error_memory_lessons=[LESSON_REQUIRED_VALIDATOR, LESSON_ROUTE_SCHEMA],
            frozen_behavior=common_frozen,
            focused_markers=["Q31_CHANGED_FILE_VALIDATOR_COVERAGE_REGRESSION_SET: PASS"],
            delivery_markers=[
                "Q31_EXACT_RELEASE_COVERAGE_MAP: PASS",
                "VALIDATION OK: " + FEATURE,
            ],
            negative_markers=[
                "Q31_NEGATIVE_UNCOVERED_FILE: PASS",
                "Q31_NEGATIVE_ORPHAN_VALIDATOR: PASS",
            ],
        ),
    ]
    return {
        "coverage_required": True,
        "no_coverage_evidence": [],
        "q30_decision_complete": True,
        "q30_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": [str(path).replace("\\", "/") for path in RELEASE_FILES],
        "coverage_rows": rows,
        "validator_discovery_method": "EXPLICIT_INVENTORY",
        "broad_substring_exclusion": False,
        "required_validator_inventory": [validator],
        "uncovered_files": [],
        "orphan_required_validators": [],
        "conflicting_dispositions": [],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q32": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK)
    bridge = _read(root / BRIDGE)
    brick_meta = json.loads(_read(root / BRICK_META))
    bridge_meta = json.loads(_read(root / BRIDGE_META))
    q30 = _read(root / Q30)
    for marker in (
        "Changed-file-to-validator coverage map (Q31)",
        "CHANGED-FILE-TO-VALIDATOR COVERAGE MAP",
        "every changed file exactly once",
        "no broad substring exclusion",
        "proceed to Q32 validation and evidence provenance YES/NO",
        "may begin coding NO",
        "may write source NO",
    ):
        _gate("Q31_BRICK_WALL_CONTRACT", marker in brick, marker)
    for marker in (
        "Changed-file-to-validator coverage bridge (Q31)",
        "one row per file",
        "explicit validator inventory",
        "no broad substring exclusion",
        "proceed Q32 YES/NO",
    ):
        _gate("Q31_ROUTER_BRIDGE_CONTRACT", marker in bridge, marker)
    _gate(
        "Q31_BRICK_VERSION",
        tuple(map(int, brick_meta["version"].split("."))) >= (3, 14),
    )
    _gate(
        "Q31_BRIDGE_VERSION",
        tuple(map(int, bridge_meta["version"].split("."))) >= (4, 8),
    )
    _gate(
        "Q31_BRICK_HEADER_METADATA_VERSION_ALIGNMENT",
        f"version: {brick_meta['version']}" in brick,
    )
    _gate(
        "Q31_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT",
        f"version: {bridge_meta['version']}" in bridge,
    )
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        _gate(
            "Q31_METADATA_ALIGNMENT",
            meta.get("source_stage") == meta.get("updated_for")
            and bool(meta.get("source_stage")),
            label,
        )
        _gate(
            "Q31_METADATA_DO_NOT_REGRESS",
            any("Q31 must reuse current manifests" in rule for rule in meta.get("do_not_regress", [])),
            label,
        )
    _gate(
        "Q30_FORWARD_COMPATIBLE_Q31_PROGRESSION",
        "Q30_FORWARD_COMPATIBLE_Q31_PROGRESSION" in q30,
    )
    for relative in RELEASE_FILES:
        path = root / relative
        _gate("Q31_REQUIRED_FILE", path.is_file(), str(relative))
        if path.suffix == ".py" or path.name.endswith(".md"):
            _gate(
                "Q31_MODULE_SIZE",
                len(_read(path).splitlines()) <= 500,
                f"{relative}={len(_read(path).splitlines())}",
            )


def _reject(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    record = mutated_record(valid_complete_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_record_contract() -> None:
    validate_record(valid_complete_record())
    _gate("Q31_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q31_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
        ("Q31_NEGATIVE_Q30_DECISION", lambda r: r.update(q30_decision_complete=False)),
        ("Q31_NEGATIVE_Q30_FROZEN_BASELINE", lambda r: r.update(q30_frozen_baseline=False)),
        ("Q31_NEGATIVE_DISCOVERY_METHOD", lambda r: r.update(validator_discovery_method="GLOB")),
        ("Q31_NEGATIVE_BROAD_SUBSTRING_EXCLUSION", lambda r: r.update(broad_substring_exclusion=True)),
        ("Q31_NEGATIVE_UNCOVERED_FILE", lambda r: r["uncovered_files"].append("missing.py")),
        ("Q31_NEGATIVE_ORPHAN_VALIDATOR", lambda r: r["orphan_required_validators"].append("orphan.py")),
        ("Q31_NEGATIVE_CONFLICTING_DISPOSITION", lambda r: r["conflicting_dispositions"].append("file.py/gui")),
        ("Q31_NEGATIVE_UNRESOLVED_FIELD", lambda r: r["unresolved_fields"].append("owner")),
        ("Q31_NEGATIVE_DUPLICATE_CHANGED_FILE", lambda r: r["changed_files"].append(r["changed_files"][0])),
        ("Q31_NEGATIVE_MISSING_COVERAGE_ROW", lambda r: r["coverage_rows"].pop()),
        ("Q31_NEGATIVE_DUPLICATE_COVERAGE_ROW", lambda r: r["coverage_rows"].append(r["coverage_rows"][0])),
        ("Q31_NEGATIVE_MISSING_OWNER_BOX", lambda r: r["coverage_rows"][0].update(owner_box="")),
        ("Q31_NEGATIVE_MISSING_PUBLIC_CONTRACT", lambda r: r["coverage_rows"][0].update(public_contract="")),
        ("Q31_NEGATIVE_MISSING_ERROR_MEMORY", lambda r: r["coverage_rows"][0].update(error_memory_lessons=[])),
        ("Q31_NEGATIVE_MISSING_FROZEN_BEHAVIOR", lambda r: r["coverage_rows"][0].update(frozen_behavior=[])),
        ("Q31_NEGATIVE_APPLIES_WITHOUT_VALIDATOR", lambda r: r["coverage_rows"][0]["focused_tests"].update(validators=[])),
        ("Q31_NEGATIVE_APPLIES_WITHOUT_MARKER", lambda r: r["coverage_rows"][0]["focused_tests"].update(expected_markers=[])),
        ("Q31_NEGATIVE_NA_WITH_VALIDATOR", lambda r: r["coverage_rows"][0]["gui_tests"].update(validators=[r["required_validator_inventory"][0]])),
        ("Q31_NEGATIVE_MISSING_REASON", lambda r: r["coverage_rows"][0]["boundary_tests"].update(reason="")),
        ("Q31_NEGATIVE_INVENTORY_VALIDATOR_UNMAPPED", lambda r: r["required_validator_inventory"].append("tools/orphan.py")),
        ("Q31_NEGATIVE_Q32_PROGRESSION", lambda r: r.update(may_proceed_to_q32=False)),
        ("Q31_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q31_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    record = valid_not_applicable_record()
    record["no_coverage_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q31_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q31_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q31_CHANGED_FILE_VALIDATOR_COVERAGE_REGRESSION_SET: PASS")
    print("Q31_FORWARD_COMPATIBLE_Q32_PROGRESSION: PASS")


def validate_exact_release_map(root: Path) -> None:
    record = q31_release_record()
    validate_record(record)
    expected_paths = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    row_paths = {row["path"] for row in record["coverage_rows"]}
    _gate("Q31_EXACT_CHANGED_FILE_SET", set(record["changed_files"]) == expected_paths)
    _gate("Q31_ONE_ROW_PER_CHANGED_FILE", row_paths == expected_paths)
    _gate("Q31_EXPLICIT_VALIDATOR_INVENTORY", record["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q31_BROAD_SUBSTRING_EXCLUSION_ABSENT", record["broad_substring_exclusion"] is False)
    _gate("Q31_NO_UNCOVERED_FILES", not record["uncovered_files"])
    _gate("Q31_NO_ORPHAN_REQUIRED_VALIDATORS", not record["orphan_required_validators"])
    _gate("Q31_NO_CONFLICTING_DISPOSITIONS", not record["conflicting_dispositions"])
    _gate("Q31_RELEASE_OWNER_BOX", record["primary_box"] == "kanda_prompt_workspace/prompt_library")
    _gate(
        "Q31_ALL_COVERAGE_KINDS_CLASSIFIED",
        all(
            all(row[kind]["disposition"] in {"APPLIES", "NOT_APPLICABLE"} for kind in COVERAGE_KINDS)
            for row in record["coverage_rows"]
        ),
    )
    _gate(
        "Q31_CURRENT_FILES_EXIST",
        all((root / path).is_file() for path in expected_paths),
    )
    _gate("Q31_EXACT_RELEASE_COVERAGE_MAP", True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    validate_record_contract()
    validate_exact_release_map(root)
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
