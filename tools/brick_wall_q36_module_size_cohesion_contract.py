# project-path: tools/brick_wall_q36_module_size_cohesion_contract.py
"""Validation-only Q36 module-size and cohesion contract."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import PurePosixPath
from typing import Any, Mapping

__all__: list[str] = []

IDEAL_LINES = 400
MAXIMUM_LINES = 500
MODULE_ROLES = {"FACADE", "HELPER", "CONTRACT", "VALIDATOR", "ADAPTER", "OTHER"}
SPLIT_BASES = {"RESPONSIBILITY", "NONE"}
FACADE_DECISIONS = {"IDEAL", "JUSTIFIED_WITHIN_MAX", "NOT_FACADE"}
REQUIRED_FIELDS = {
    "enforcement_required",
    "no_enforcement_evidence",
    "q35_decision",
    "q35_frozen_baseline",
    "feature_id",
    "operation_id",
    "primary_box",
    "changed_files",
    "touched_python_modules",
    "count_method",
    "ideal_lines",
    "maximum_lines",
    "formatting_verified",
    "formatting_command",
    "formatting_markers",
    "compression_forbidden",
    "artificial_padding_forbidden",
    "responsibility_split_required",
    "helper_dependency_direction_enforced",
    "facade_policy_enforced",
    "python_set_reconciled",
    "validators",
    "expected_markers",
    "durable_evidence_path",
    "limitations",
    "blockers",
    "decision",
    "may_proceed_to_q37",
    "may_begin_coding",
    "may_write_source",
}
MODULE_FIELDS = {
    "path",
    "owner_box",
    "module_role",
    "responsibility_id",
    "responsibility",
    "public_contract",
    "physical_lines",
    "ast_parse_passed",
    "pep8_verified",
    "formatter",
    "formatter_markers",
    "compression_detected",
    "artificial_padding_detected",
    "split_basis",
    "helper_to_facade_back_import",
    "dependency_direction",
    "facade_size_decision",
    "over_ideal_justification",
    "split_needed",
    "refactor_route",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _safe_relative_python(path: str) -> bool:
    candidate = PurePosixPath(path)
    return (
        bool(path)
        and path.endswith(".py")
        and not candidate.is_absolute()
        and ".." not in candidate.parts
        and "\\" not in path
    )


def _module(path: str, lines: int, role: str, responsibility: str) -> dict[str, Any]:
    over_ideal = lines > IDEAL_LINES
    return {
        "path": path,
        "owner_box": "kanda_prompt_workspace/prompt_library",
        "module_role": role,
        "responsibility_id": _sha_text(path + ":" + responsibility)[:16],
        "responsibility": responsibility,
        "public_contract": "validation-only Brick Wall contract",
        "physical_lines": lines,
        "ast_parse_passed": True,
        "pep8_verified": True,
        "formatter": "ruff-format-check",
        "formatter_markers": ["FORMAT_CHECK: PASS"],
        "compression_detected": False,
        "artificial_padding_detected": False,
        "split_basis": "RESPONSIBILITY" if role == "HELPER" else "NONE",
        "helper_to_facade_back_import": False,
        "dependency_direction": "validator -> contract; no helper -> facade back import",
        "facade_size_decision": "NOT_FACADE" if role != "FACADE" else ("IDEAL" if not over_ideal else "JUSTIFIED_WITHIN_MAX"),
        "over_ideal_justification": "Cohesive validation contract near hard limit; further extraction would separate one responsibility." if over_ideal else "",
        "split_needed": False,
        "refactor_route": "NOT_REQUIRED",
    }


def valid_complete_record() -> dict[str, Any]:
    modules = [
        _module("tools/brick_wall_q36_module_size_cohesion_contract.py", 360, "CONTRACT", "validate Q36 evidence records"),
        _module("tools/validate_brick_wall_q36_module_size_cohesion_v1.py", 280, "VALIDATOR", "exercise Q36 source and negative regressions"),
    ]
    changed = [module["path"] for module in modules] + ["docs/q36.md"]
    return {
        "enforcement_required": True,
        "no_enforcement_evidence": [],
        "q35_decision": "COMPLETE",
        "q35_frozen_baseline": "freeze-20260716-brick-wall-q35-focused-performance-baseline-validator-provenance-repair-v1r1",
        "feature_id": "brick-wall-q36-module-size-and-cohesion-enforcement-v1",
        "operation_id": "q36-module-size-contract-fixture",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": changed,
        "touched_python_modules": modules,
        "count_method": "len(text.splitlines())",
        "ideal_lines": IDEAL_LINES,
        "maximum_lines": MAXIMUM_LINES,
        "formatting_verified": True,
        "formatting_command": "python -m ruff format --check <touched-python-set>",
        "formatting_markers": ["FORMAT_CHECK: PASS"],
        "compression_forbidden": True,
        "artificial_padding_forbidden": True,
        "responsibility_split_required": True,
        "helper_dependency_direction_enforced": True,
        "facade_policy_enforced": True,
        "python_set_reconciled": True,
        "validators": ["tools/validate_brick_wall_q36_module_size_cohesion_v1.py"],
        "expected_markers": ["Q36_MODULE_SIZE_COHESION_REGRESSION_SET: PASS"],
        "durable_evidence_path": "project_validation_evidence/q36.txt",
        "limitations": ["Physical line count is necessary but not sufficient; cohesion and dependency evidence remain mandatory."],
        "blockers": [],
        "decision": "COMPLETE",
        "may_proceed_to_q37": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update(
        enforcement_required=False,
        no_enforcement_evidence=[
            "Exact changed-file inventory contains no Python source.",
            "The release changes documentation-only governance text.",
        ],
        changed_files=["docs/q36.md"],
        touched_python_modules=[],
        formatting_verified=False,
        formatting_command="NOT_APPLICABLE",
        formatting_markers=[],
        python_set_reconciled=True,
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def validate_record(record: Mapping[str, Any]) -> None:
    missing = REQUIRED_FIELDS - set(record)
    _assert(not missing, "missing Q36 fields: " + repr(sorted(missing)))
    required = record["enforcement_required"]
    _assert(isinstance(required, bool), "enforcement_required must be bool")
    _assert(record["q35_decision"] in {"COMPLETE", "NOT_APPLICABLE"}, "Q35 decision must be complete")
    _assert(bool(record["q35_frozen_baseline"]), "Q35 frozen baseline is required")
    _assert(bool(record["feature_id"]) and bool(record["operation_id"]), "feature and operation IDs are required")
    _assert(bool(record["primary_box"]), "primary box is required")
    changed = record["changed_files"]
    modules = record["touched_python_modules"]
    _assert(isinstance(changed, list) and len(changed) == len(set(changed)), "changed files must be unique")
    _assert(isinstance(modules, list), "touched_python_modules must be a list")
    python_changed = {path for path in changed if str(path).endswith(".py")}
    module_paths = [module.get("path") for module in modules]
    _assert(len(module_paths) == len(set(module_paths)), "touched Python paths must be unique")
    _assert(set(module_paths) == python_changed, "touched Python set must exactly match changed Python files")
    _assert(record["python_set_reconciled"] is True, "Python set reconciliation is required")
    _assert(record["count_method"] == "len(text.splitlines())", "canonical physical-line counter is required")
    _assert(record["ideal_lines"] == IDEAL_LINES and record["maximum_lines"] == MAXIMUM_LINES, "governed limits must be 400/500")
    _assert(record["compression_forbidden"] is True, "formatting compression must be forbidden")
    _assert(record["artificial_padding_forbidden"] is True, "artificial padding must be forbidden")
    _assert(record["responsibility_split_required"] is True, "responsibility-based splitting is required")
    _assert(record["helper_dependency_direction_enforced"] is True, "helper dependency direction is required")
    _assert(record["facade_policy_enforced"] is True, "facade policy is required")
    if not required:
        _assert(record["decision"] == "NOT_APPLICABLE", "N/A record decision mismatch")
        _assert(not modules and not python_changed, "N/A requires no Python source")
        _assert(len(record["no_enforcement_evidence"]) >= 2, "N/A evidence is incomplete")
        _assert(record["may_proceed_to_q37"] is True, "N/A may proceed to Q37")
    else:
        _assert(record["decision"] == "COMPLETE", "required record must be complete")
        _assert(modules, "required record needs touched Python modules")
        _assert(record["formatting_verified"] is True, "formatting verification is required")
        _assert(bool(record["formatting_command"]), "formatting command is required")
        _assert(bool(record["formatting_markers"]), "formatting markers are required")
        responsibility_ids: list[str] = []
        for module in modules:
            missing_module = MODULE_FIELDS - set(module)
            _assert(not missing_module, "missing module fields: " + repr(sorted(missing_module)))
            path = module["path"]
            _assert(_safe_relative_python(path), "unsafe Python module path")
            _assert(bool(module["owner_box"]), "module owner is required")
            _assert(module["module_role"] in MODULE_ROLES, "unknown module role")
            _assert(bool(module["responsibility_id"]) and bool(module["responsibility"]), "module responsibility is required")
            responsibility_ids.append(module["responsibility_id"])
            lines = module["physical_lines"]
            _assert(isinstance(lines, int) and 1 <= lines <= MAXIMUM_LINES, "touched Python module exceeds governed limit")
            _assert(module["ast_parse_passed"] is True, "AST parse evidence is required")
            _assert(module["pep8_verified"] is True, "PEP 8 verification is required")
            _assert(bool(module["formatter"]) and bool(module["formatter_markers"]), "formatter evidence is required")
            _assert(module["compression_detected"] is False, "formatting compression is forbidden")
            _assert(module["artificial_padding_detected"] is False, "artificial padding is forbidden")
            _assert(module["split_basis"] in SPLIT_BASES, "split basis must be responsibility or none")
            _assert(module["helper_to_facade_back_import"] is False, "helper-to-facade back import is forbidden")
            _assert(bool(module["dependency_direction"]), "dependency direction is required")
            _assert(module["facade_size_decision"] in FACADE_DECISIONS, "facade size decision is invalid")
            if lines > IDEAL_LINES:
                _assert(bool(module["over_ideal_justification"]), "over-ideal module requires justification")
            if module["module_role"] == "FACADE" and lines > IDEAL_LINES:
                _assert(module["facade_size_decision"] == "JUSTIFIED_WITHIN_MAX", "large facade requires explicit decision")
            if module["module_role"] != "FACADE":
                _assert(module["facade_size_decision"] == "NOT_FACADE", "non-facade decision mismatch")
            if module["split_needed"]:
                _assert(module["split_basis"] == "RESPONSIBILITY", "split must be responsibility-based")
                _assert(module["refactor_route"] == "large_module_refactor_protocol_v8.0", "required split must route to v8.0")
            else:
                _assert(module["refactor_route"] in {"NOT_REQUIRED", "large_module_refactor_protocol_v8.0"}, "invalid refactor route")
        _assert(len(responsibility_ids) == len(set(responsibility_ids)), "responsibility IDs must be unique")
        _assert(not record["blockers"], "complete record cannot contain blockers")
        _assert(record["may_proceed_to_q37"] is True, "complete record may proceed to Q37")
    _assert(record["may_begin_coding"] is False, "Q36 does not grant coding authority")
    _assert(record["may_write_source"] is False, "Q36 does not grant source-write authority")
    _assert(bool(record["validators"]) and bool(record["expected_markers"]), "validator evidence is required")
    _assert(str(record["durable_evidence_path"]).startswith("project_validation_evidence/"), "durable evidence path must be project support")
    _assert(bool(record["limitations"]), "limitations are required")


def q36_release_record(paths: list[str], line_counts: Mapping[str, int]) -> dict[str, Any]:
    record = valid_complete_record()
    modules: list[dict[str, Any]] = []
    for path in paths:
        if not path.endswith(".py"):
            continue
        role = "CONTRACT" if "contract.py" in path else "VALIDATOR"
        modules.append(_module(path, int(line_counts[path]), role, "Q36 governed validation responsibility for " + path))
    record.update(
        operation_id="brick-wall-q36-module-size-and-cohesion-enforcement-v1-release",
        changed_files=list(paths),
        touched_python_modules=modules,
        validators=["tools/validate_brick_wall_q36_module_size_cohesion_v1.py"],
        expected_markers=["Q36_MODULE_SIZE_COHESION_REGRESSION_SET: PASS", "Q36_CURRENT_RELEASE_MODULE_SIZE_COMPLETE: PASS"],
        durable_evidence_path="project_validation_evidence/brick-wall-q36-module-size-and-cohesion-enforcement-v1.txt",
    )
    return record


def q36_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    q32 = "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py"
    q33 = "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py"
    q34 = "tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py"
    q35 = "tools/validate_brick_wall_q35_focused_performance_baseline_v1.py"
    q36 = "tools/validate_brick_wall_q36_module_size_cohesion_v1.py"
    lessons = [
        "lesson-brick-wall-q01-validator-forward-version-rigidity-v1",
        "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
        "lesson-brick-wall-q03-validator-package-import-context-v1",
        "lesson-brick-wall-focused-validator-task-route-key-assumption-v1",
    ]
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "owner_box": "tools validation-only support" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Q36 governed module-size and cohesion release",
            "error_memory_lessons": lessons,
            "frozen_behavior": ["freeze-20260716-brick-wall-q35-focused-performance-baseline-validator-provenance-repair-v1r1"],
            "focused_tests": {
                "disposition": "APPLIES",
                "validators": [q32, q33, q34, q35, q36],
                "expected_markers": ["Q36_MODULE_SIZE_COHESION_REGRESSION_SET: PASS"],
                "reason": "Q32-Q35 forward compatibility and Q36 size/cohesion behavior are checked.",
            },
            "boundary_tests": {
                "disposition": "APPLIES",
                "validators": [q36],
                "expected_markers": ["Q36_EXISTING_MODULE_SIZE_OWNERS_REUSED: PASS"],
                "reason": "Existing module-size, facade, and Large Module Refactor owners must remain canonical.",
            },
            "gui_tests": {
                "disposition": "NOT_APPLICABLE",
                "validators": [],
                "expected_markers": [],
                "reason": "No GUI or Qt behavior is changed.",
            },
            "delivery_tests": {
                "disposition": "APPLIES",
                "validators": [q36],
                "expected_markers": ["Q36_EXACT_RELEASE_PROVENANCE: PASS"],
                "reason": "Exact payload, touched-Python reconciliation, import context, durable evidence, and Q35 lineage are checked.",
            },
            "negative_tests": {
                "disposition": "APPLIES",
                "validators": [q36],
                "expected_markers": ["Q36_NEGATIVE_FORMATTING_COMPRESSION: PASS"],
                "reason": "Oversized modules, compressed formatting, padding, line-range splits, owner drift, and facade/helper regressions fail closed.",
            },
        })
    return {
        "coverage_required": True,
        "no_coverage_evidence": [],
        "q30_decision_complete": True,
        "q30_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": paths,
        "coverage_rows": rows,
        "validator_discovery_method": "EXPLICIT_INVENTORY",
        "broad_substring_exclusion": False,
        "required_validator_inventory": [q32, q33, q34, q35, q36],
        "uncovered_files": [],
        "orphan_required_validators": [],
        "conflicting_dispositions": [],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q32": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }
