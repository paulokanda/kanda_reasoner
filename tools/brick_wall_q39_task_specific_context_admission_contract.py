# project-path: tools/brick_wall_q39_task_specific_context_admission_contract.py
"""Validation-only Q39 task-specific context admission contract."""
from __future__ import annotations
from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Mapping

__all__: list[str] = []

REQUIRED_FIELDS = {
    "new_context_proposed", "no_new_context_evidence", "q38_decision",
    "q38_frozen_baseline", "feature_id", "operation_id", "primary_box",
    "changed_files", "current_context_owners", "representative_tasks",
    "baseline_results", "candidate_results", "comparison_environment_hash",
    "same_task_and_source_snapshot", "baseline_failure_reproduced",
    "metrics", "minimum_gain_threshold", "observed_gain",
    "repeated_trials", "variance_accepted", "simpler_strengthening_options",
    "simpler_existing_owner_fix_sufficient", "unique_bounded_responsibility",
    "candidate_owner_path", "candidate_public_contract", "lifecycle_and_invalidation",
    "new_context_engine_created", "new_intelligence_system_created",
    "new_context_registry_created", "validators", "expected_markers",
    "durable_evidence_path", "limitations", "blockers", "decision",
    "may_proceed_to_q40", "may_begin_coding", "may_write_source",
}
DECISIONS = {"ADMITTED", "REJECTED", "NOT_APPLICABLE", "BLOCKED"}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _safe_relative(path: str) -> bool:
    value = PurePosixPath(path)
    return bool(path) and not value.is_absolute() and ".." not in value.parts and "\\" not in path


def _tasks() -> list[dict[str, str]]:
    return [
        {"task_id": "task-routing", "input_fingerprint": "a" * 64, "expected": "correct owner route"},
        {"task_id": "task-handoff", "input_fingerprint": "b" * 64, "expected": "current source and next action"},
        {"task_id": "task-freeze", "input_fingerprint": "c" * 64, "expected": "latest human-confirmed freeze"},
    ]


def valid_admitted_record() -> dict[str, Any]:
    tasks = _tasks()
    return {
        "new_context_proposed": True,
        "no_new_context_evidence": [],
        "q38_decision": "COMPLETE",
        "q38_frozen_baseline": "freeze-20260716-brick-wall-q38-handoff-freshness-and-provenance-v1",
        "feature_id": "brick-wall-q39-task-specific-context-admission-enforcement-v1",
        "operation_id": "q39-controlled-comparison-fixture",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": ["docs/q39.md", "tools/q39_fixture.py"],
        "current_context_owners": [
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/handoff_at_end_of_work.md",
            "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json",
            "kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json",
        ],
        "representative_tasks": tasks,
        "baseline_results": [{"task_id": row["task_id"], "passed": False, "score": 0.55} for row in tasks],
        "candidate_results": [{"task_id": row["task_id"], "passed": True, "score": 0.90} for row in tasks],
        "comparison_environment_hash": "d" * 64,
        "same_task_and_source_snapshot": True,
        "baseline_failure_reproduced": True,
        "metrics": ["correctness", "coverage", "staleness", "latency", "token_cost"],
        "minimum_gain_threshold": 0.20,
        "observed_gain": 0.35,
        "repeated_trials": 5,
        "variance_accepted": True,
        "simpler_strengthening_options": ["strengthen current handoff", "add manifest field", "tighten route"],
        "simpler_existing_owner_fix_sufficient": False,
        "unique_bounded_responsibility": "Task-specific comparison summary for one proven failure class only.",
        "candidate_owner_path": "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/task_specific_context.md",
        "candidate_public_contract": "read-only task comparison summary generated from current source and invalidated on source change",
        "lifecycle_and_invalidation": ["invalidate on source hash change", "invalidate on route change", "invalidate on newer freeze"],
        "new_context_engine_created": False,
        "new_intelligence_system_created": False,
        "new_context_registry_created": False,
        "validators": ["tools/validate_brick_wall_q39_task_specific_context_admission_v1.py"],
        "expected_markers": ["Q39_TASK_SPECIFIC_CONTEXT_ADMISSION_REGRESSION_SET: PASS"],
        "durable_evidence_path": "project_validation_evidence/q39.txt",
        "limitations": ["Admission applies only to the measured task set and exact source snapshot."],
        "blockers": [],
        "decision": "ADMITTED",
        "may_proceed_to_q40": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_rejected_record() -> dict[str, Any]:
    record = valid_admitted_record()
    record.update(decision="REJECTED", observed_gain=0.05, simpler_existing_owner_fix_sufficient=True, unique_bounded_responsibility="", candidate_owner_path="", candidate_public_contract="", lifecycle_and_invalidation=[])
    return record


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_admitted_record()
    record.update(
        new_context_proposed=False,
        no_new_context_evidence=[
            "This release changes governance prompts and validation-only tools; it creates no task-specific context artifact.",
            "Current handoff, manifest, routing, Error Memory, and Freeze-context owners remain unchanged.",
        ],
        representative_tasks=[], baseline_results=[], candidate_results=[],
        comparison_environment_hash="", same_task_and_source_snapshot=False,
        baseline_failure_reproduced=False, metrics=[], minimum_gain_threshold=0.0,
        observed_gain=0.0, repeated_trials=0, variance_accepted=False,
        simpler_strengthening_options=["reuse current handoff and routes"],
        simpler_existing_owner_fix_sufficient=True,
        unique_bounded_responsibility="", candidate_owner_path="",
        candidate_public_contract="", lifecycle_and_invalidation=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def validate_record(record: Mapping[str, Any]) -> None:
    missing = REQUIRED_FIELDS - set(record)
    _assert(not missing, "missing Q39 fields: " + repr(sorted(missing)))
    _assert(record["q38_decision"] in {"COMPLETE", "NOT_APPLICABLE"}, "Q38 decision must be complete")
    _assert(bool(record["q38_frozen_baseline"]), "Q38 frozen baseline required")
    _assert(bool(record["feature_id"]) and bool(record["operation_id"]), "feature and operation IDs required")
    _assert(bool(record["primary_box"]), "primary box required")
    changed = record["changed_files"]
    _assert(isinstance(changed, list) and changed and len(changed) == len(set(changed)), "changed files must be unique")
    _assert(all(_safe_relative(str(path)) for path in changed), "changed files must be safe relative paths")
    owners = record["current_context_owners"]
    _assert(isinstance(owners, list) and len(owners) >= 3 and all(_safe_relative(str(path)) for path in owners), "current context owners incomplete")
    _assert(record["decision"] in DECISIONS, "invalid Q39 decision")
    _assert(record["new_context_engine_created"] is False, "parallel context engine forbidden")
    _assert(record["new_intelligence_system_created"] is False, "parallel intelligence system forbidden")
    _assert(record["new_context_registry_created"] is False, "context registry forbidden")
    _assert(record["may_begin_coding"] is False and record["may_write_source"] is False, "Q39 cannot authorize coding or source writes")
    _assert(record["may_proceed_to_q40"] is (record["decision"] != "BLOCKED"), "Q40 progression mismatch")
    _assert(isinstance(record["validators"], list) and record["validators"], "validators required")
    _assert(isinstance(record["expected_markers"], list) and record["expected_markers"], "markers required")
    _assert(_safe_relative(record["durable_evidence_path"]), "durable evidence path invalid")
    _assert(isinstance(record["limitations"], list) and record["limitations"], "limitations required")
    if not record["new_context_proposed"]:
        _assert(record["decision"] == "NOT_APPLICABLE", "no proposal requires NOT_APPLICABLE")
        _assert(isinstance(record["no_new_context_evidence"], list) and len(record["no_new_context_evidence"]) >= 2, "N/A evidence required")
        _assert(not record["representative_tasks"] and not record["baseline_results"] and not record["candidate_results"], "N/A cannot claim comparison")
        return
    tasks = record["representative_tasks"]
    _assert(isinstance(tasks, list) and len(tasks) >= 3, "at least three representative tasks required")
    task_ids = [row.get("task_id") for row in tasks]
    _assert(len(task_ids) == len(set(task_ids)) and all(task_ids), "task IDs must be unique")
    _assert(all(len(row.get("input_fingerprint", "")) == 64 and row.get("expected") for row in tasks), "task fingerprints/expectations incomplete")
    for result_name in ("baseline_results", "candidate_results"):
        rows = record[result_name]
        _assert({row.get("task_id") for row in rows} == set(task_ids), result_name + " task set mismatch")
        _assert(all(isinstance(row.get("passed"), bool) and isinstance(row.get("score"), (int, float)) for row in rows), result_name + " incomplete")
    _assert(len(record["comparison_environment_hash"]) == 64, "comparison environment hash required")
    _assert(record["same_task_and_source_snapshot"] is True, "comparison must use identical task/source snapshot")
    _assert(record["baseline_failure_reproduced"] is True, "baseline failure must be reproduced")
    _assert(set(record["metrics"]) >= {"correctness", "coverage", "staleness"}, "core metrics missing")
    _assert(record["repeated_trials"] >= 3 and record["variance_accepted"] is True, "repeated stable trials required")
    _assert(isinstance(record["simpler_strengthening_options"], list) and len(record["simpler_strengthening_options"]) >= 2, "simpler alternatives required")
    if record["decision"] == "ADMITTED":
        _assert(record["observed_gain"] >= record["minimum_gain_threshold"] > 0, "thresholded gain not proven")
        _assert(record["simpler_existing_owner_fix_sufficient"] is False, "simpler existing-owner fix must be insufficient")
        _assert(bool(record["unique_bounded_responsibility"]), "unique bounded responsibility required")
        _assert(_safe_relative(record["candidate_owner_path"]), "candidate owner path invalid")
        _assert(bool(record["candidate_public_contract"]), "candidate public contract required")
        _assert(len(record["lifecycle_and_invalidation"]) >= 2, "lifecycle/invalidation required")
    if record["decision"] == "REJECTED":
        _assert(record["observed_gain"] < record["minimum_gain_threshold"] or record["simpler_existing_owner_fix_sufficient"] is True, "rejection requires failed gain or simpler fix")


def q39_release_record(paths: list[str], fingerprints: list[dict[str, str]], source_set_hash: str) -> dict[str, Any]:
    record = valid_not_applicable_record()
    record.update(changed_files=list(paths), current_context_owners=[
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/handoff_at_end_of_work.md",
        "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json",
        "kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/governed_architecture_companion_handoff.md",
    ])
    record["limitations"] = ["Current release records an admission gate only; no new context summary or intelligence layer is proposed.", "Exact release source-set hash: " + source_set_hash]
    return record


def q39_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    validators = [
        "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py",
        "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py",
        "tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py",
        "tools/validate_brick_wall_q35_focused_performance_baseline_v1.py",
        "tools/validate_brick_wall_q36_module_size_cohesion_v1.py",
        "tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py",
        "tools/validate_brick_wall_q38_handoff_freshness_provenance_v1.py",
        "tools/validate_brick_wall_q39_task_specific_context_admission_v1.py",
    ]
    lessons = [
        "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
        "lesson-brick-wall-q03-validator-package-import-context-v1",
        "lesson-powershell-continuation-prompt-concatenated-scriptblock-v1",
    ]
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "owner_box": "tools validation-only support" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Brick Wall Q39 task-specific context admission gate",
            "error_memory_lessons": lessons,
            "frozen_behavior": ["freeze-20260716-brick-wall-q38-handoff-freshness-and-provenance-v1"],
            "focused_tests": {
                "disposition": "APPLIES", "validators": validators,
                "expected_markers": ["Q39_TASK_SPECIFIC_CONTEXT_ADMISSION_REGRESSION_SET: PASS"],
                "reason": "Q32-Q38 forward compatibility and Q39 admission behavior are checked.",
            },
            "boundary_tests": {
                "disposition": "APPLIES", "validators": [validators[-1]],
                "expected_markers": ["Q39_EXISTING_CONTEXT_AUTHORITIES_REUSED: PASS"],
                "reason": "Existing handoff, startup, route, and context owners remain canonical.",
            },
            "gui_tests": {
                "disposition": "NOT_APPLICABLE", "validators": [], "expected_markers": [],
                "reason": "No GUI or Qt behavior is changed.",
            },
            "delivery_tests": {
                "disposition": "APPLIES", "validators": [validators[-1]],
                "expected_markers": ["Q39_EXACT_RELEASE_PROVENANCE: PASS"],
                "reason": "Exact payload, Q38 lineage, import context, source fingerprints, and durable evidence are checked.",
            },
            "negative_tests": {
                "disposition": "APPLIES", "validators": [validators[-1]],
                "expected_markers": ["Q39_NEGATIVE_CONTEXT_ENGINE: PASS"],
                "reason": "Uncontrolled comparisons, weak gains, simpler fixes, and new context systems fail closed.",
            },
        })
    return {
        "coverage_required": True,
        "no_coverage_evidence": [],
        "q30_decision_complete": True,
        "q30_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": list(paths),
        "coverage_rows": rows,
        "validator_discovery_method": "EXPLICIT_INVENTORY",
        "broad_substring_exclusion": False,
        "required_validator_inventory": validators,
        "uncovered_files": [],
        "orphan_required_validators": [],
        "conflicting_dispositions": [],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q32": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }
