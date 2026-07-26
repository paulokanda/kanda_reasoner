# project-path: tools/brick_wall_q31_changed_file_validator_coverage_contract.py
"""Validation-only Q31 changed-file-to-validator coverage contract."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

__all__: list[str] = []

COVERAGE_KINDS = (
    "focused_tests",
    "boundary_tests",
    "gui_tests",
    "delivery_tests",
    "negative_tests",
)

REQUIRED_FIELDS = (
    "coverage_required",
    "no_coverage_evidence",
    "q30_decision_complete",
    "q30_frozen_baseline",
    "primary_box",
    "changed_files",
    "coverage_rows",
    "validator_discovery_method",
    "broad_substring_exclusion",
    "required_validator_inventory",
    "uncovered_files",
    "orphan_required_validators",
    "conflicting_dispositions",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q32",
    "may_begin_coding",
    "may_write_source",
)

ROW_REQUIRED_FIELDS = (
    "path",
    "owner_box",
    "public_contract",
    "error_memory_lessons",
    "frozen_behavior",
) + COVERAGE_KINDS


def _applies(validator: str, marker: str, reason: str) -> dict[str, Any]:
    return {
        "disposition": "APPLIES",
        "validators": [validator],
        "expected_markers": [marker],
        "reason": reason,
    }


def _not_applicable(reason: str) -> dict[str, Any]:
    return {
        "disposition": "NOT_APPLICABLE",
        "validators": [],
        "expected_markers": [],
        "reason": reason,
    }


def _row(path: str, owner_box: str, public_contract: str) -> dict[str, Any]:
    validator = "tools/validate_brick_wall_q31_changed_file_validator_coverage_map_v1.py"
    return {
        "path": path,
        "owner_box": owner_box,
        "public_contract": public_contract,
        "error_memory_lessons": [
            "lesson-patch4-regression-validator-required-removed-patch5-placeholder-v1"
        ],
        "frozen_behavior": [
            "freeze-20260716-brick-wall-q30-human-confirmation-freeze-protection-validator-discovery-repair-v1r2"
        ],
        "focused_tests": _applies(
            validator,
            "Q31_CHANGED_FILE_VALIDATOR_COVERAGE_REGRESSION_SET: PASS",
            "The Q31 focused validator protects the exact coverage record.",
        ),
        "boundary_tests": _not_applicable(
            "The sample file introduces no cross-box runtime communication."
        ),
        "gui_tests": _not_applicable(
            "The sample file changes no GUI or Qt behavior."
        ),
        "delivery_tests": _applies(
            validator,
            "Q31_EXACT_RELEASE_COVERAGE_MAP: PASS",
            "The final release validator checks installed payload and delivery mapping.",
        ),
        "negative_tests": _applies(
            validator,
            "Q31_NEGATIVE_UNCOVERED_FILE: PASS",
            "Negative records prove uncovered files fail closed.",
        ),
    }


def valid_complete_record() -> dict[str, Any]:
    validator = "tools/validate_brick_wall_q31_changed_file_validator_coverage_map_v1.py"
    changed_files = [
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md",
        "tools/brick_wall_q31_changed_file_validator_coverage_contract.py",
    ]
    return {
        "coverage_required": True,
        "no_coverage_evidence": [],
        "q30_decision_complete": True,
        "q30_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": changed_files,
        "coverage_rows": [
            _row(
                changed_files[0],
                "kanda_prompt_workspace/prompt_library",
                "KPR-03-001 brick_wall_comprehensive_quality_gate",
            ),
            _row(
                changed_files[1],
                "tools validation-only support",
                "Q31 validation-only record contract",
            ),
        ],
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


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update(
        coverage_required=False,
        no_coverage_evidence=[
            "The audited activity changes no source, prompt, metadata, validator, GUI, or delivery file."
        ],
        changed_files=[],
        coverage_rows=[],
        required_validator_inventory=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_test_disposition(
    item: Mapping[str, Any],
    *,
    path: str,
    kind: str,
    inventory: set[str],
) -> set[str]:
    required = {"disposition", "validators", "expected_markers", "reason"}
    _assert(required.issubset(item), f"Q31 {path} {kind} fields incomplete")
    disposition = item["disposition"]
    _assert(disposition in {"APPLIES", "NOT_APPLICABLE"}, f"Q31 {path} {kind} disposition invalid")
    validators = item["validators"]
    markers = item["expected_markers"]
    reason = str(item["reason"]).strip()
    _assert(isinstance(validators, list), f"Q31 {path} {kind} validators must be a list")
    _assert(isinstance(markers, list), f"Q31 {path} {kind} markers must be a list")
    _assert(bool(reason), f"Q31 {path} {kind} reason is required")
    if disposition == "APPLIES":
        _assert(bool(validators), f"Q31 {path} {kind} requires validators")
        _assert(bool(markers), f"Q31 {path} {kind} requires markers")
        _assert(all(v in inventory for v in validators), f"Q31 {path} {kind} validator missing from inventory")
        return set(validators)
    _assert(not validators, f"Q31 {path} {kind} N/A must not list validators")
    _assert(not markers, f"Q31 {path} {kind} N/A must not list markers")
    return set()


def validate_record(record: Mapping[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    _assert(not missing, "Q31 record missing fields: " + ", ".join(missing))
    _assert(record["decision"] in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}, "Invalid Q31 decision")
    _assert(record["may_begin_coding"] is False, "Q31 may not directly authorize coding")
    _assert(record["may_write_source"] is False, "Q31 may not directly authorize source writing")
    _assert(bool(record["primary_box"]), "Q31 primary box is required")
    _assert(record["q30_decision_complete"] is True, "Q30 decision must be complete")
    _assert(record["q30_frozen_baseline"] is True, "Q30 frozen baseline is required")
    _assert(record["validator_discovery_method"] == "EXPLICIT_INVENTORY", "Q31 requires explicit validator inventory")
    _assert(record["broad_substring_exclusion"] is False, "Broad substring validator exclusion is forbidden")
    _assert(not record["uncovered_files"], "Q31 uncovered files remain")
    _assert(not record["orphan_required_validators"], "Q31 orphan required validators remain")
    _assert(not record["conflicting_dispositions"], "Q31 conflicting dispositions remain")
    _assert(not record["unresolved_fields"], "Q31 unresolved fields remain")

    changed_files = record["changed_files"]
    rows = record["coverage_rows"]
    inventory_list = record["required_validator_inventory"]
    _assert(isinstance(changed_files, list), "Q31 changed_files must be a list")
    _assert(isinstance(rows, list), "Q31 coverage_rows must be a list")
    _assert(isinstance(inventory_list, list), "Q31 validator inventory must be a list")
    _assert(len(changed_files) == len(set(changed_files)), "Q31 duplicate changed file")
    _assert(len(inventory_list) == len(set(inventory_list)), "Q31 duplicate validator inventory entry")
    inventory = set(inventory_list)

    if record["decision"] == "COMPLETE":
        _assert(record["coverage_required"] is True, "COMPLETE requires coverage")
        _assert(bool(changed_files), "Q31 COMPLETE requires changed files")
        _assert(bool(inventory), "Q31 COMPLETE requires validator inventory")
        _assert(record["may_proceed_to_q32"] is True, "Q31 COMPLETE must permit Q32 progression")
        paths: list[str] = []
        used_validators: set[str] = set()
        for row in rows:
            _assert(isinstance(row, Mapping), "Q31 coverage row must be an object")
            row_missing = [field for field in ROW_REQUIRED_FIELDS if field not in row]
            _assert(not row_missing, "Q31 coverage row missing fields: " + ", ".join(row_missing))
            path = str(row["path"]).strip()
            _assert(bool(path), "Q31 coverage row path is required")
            _assert(bool(str(row["owner_box"]).strip()), f"Q31 {path} owner box is required")
            _assert(bool(str(row["public_contract"]).strip()), f"Q31 {path} public contract is required")
            _assert(bool(row["error_memory_lessons"]), f"Q31 {path} Error Memory disposition is required")
            _assert(bool(row["frozen_behavior"]), f"Q31 {path} frozen behavior disposition is required")
            paths.append(path)
            row_validators: set[str] = set()
            for kind in COVERAGE_KINDS:
                row_validators.update(
                    _validate_test_disposition(
                        row[kind],
                        path=path,
                        kind=kind,
                        inventory=inventory,
                    )
                )
            _assert(bool(row_validators), f"Q31 {path} has no applicable validator")
            used_validators.update(row_validators)
        _assert(len(paths) == len(set(paths)), "Q31 duplicate coverage row")
        _assert(set(paths) == set(changed_files), "Q31 coverage rows do not match changed files")
        _assert(used_validators == inventory, "Q31 validator inventory has orphan or unmapped entries")
    elif record["decision"] == "NOT_APPLICABLE":
        _assert(record["coverage_required"] is False, "N/A must not claim required coverage")
        _assert(bool(record["no_coverage_evidence"]), "Q31 N/A requires evidence")
        _assert(not changed_files, "Q31 N/A must not list changed files")
        _assert(not rows, "Q31 N/A must not list coverage rows")
        _assert(not inventory, "Q31 N/A must not list validators")
        _assert(record["may_proceed_to_q32"] is True, "Evidence-backed N/A may proceed to Q32")
    else:
        _assert(record["may_proceed_to_q32"] is False, "BLOCKED may not proceed")
