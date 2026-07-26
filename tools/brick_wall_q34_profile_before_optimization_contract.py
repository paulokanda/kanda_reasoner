# project-path: tools/brick_wall_q34_profile_before_optimization_contract.py
"""Validation-only Q34 profile-before-optimization contract."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
import statistics
from typing import Any, Mapping

__all__: list[str] = []

SHA256_HEX_LENGTH = 64
BOTTLENECK_CLASSES = {
    "CPU",
    "MEMORY",
    "IO",
    "LATENCY",
    "LOCK_CONTENTION",
    "ALLOCATION",
    "DATABASE",
    "STARTUP",
    "RENDERING",
}
PROFILER_TOOLS = {
    "cProfile",
    "py-spy",
    "line_profiler",
    "memory_profiler",
    "tracemalloc",
    "timeit",
    "pytest-benchmark",
    "database_explain",
    "instrumented_timer",
}
REQUIRED_FIELDS = {
    "profile_required",
    "no_optimization_evidence",
    "q33_decision_complete",
    "q33_frozen_baseline",
    "feature_id",
    "operation_id",
    "primary_box",
    "slow_path_name",
    "slow_path_owner_box",
    "workload_name",
    "workload_description",
    "workload_representative",
    "workload_inputs",
    "workload_scale",
    "source_fingerprints",
    "environment_fingerprint",
    "profiler_tool",
    "profiling_command",
    "baseline_metric",
    "baseline_unit",
    "warmup_runs",
    "measurement_runs",
    "baseline_measurements",
    "baseline_median",
    "baseline_mean",
    "baseline_stdev",
    "baseline_coefficient_of_variation",
    "variance_acceptance_threshold",
    "variance_accepted",
    "bottleneck_classification",
    "bottleneck_evidence_hash",
    "simpler_alternatives_considered",
    "proposed_optimization",
    "expected_improvement_metric",
    "expected_improvement_target",
    "minimum_acceptable_improvement",
    "complexity_budget",
    "rollback_condition",
    "durable_evidence_path",
    "validators",
    "expected_markers",
    "limitations",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q35",
    "may_begin_coding",
    "may_write_source",
}
COMPLEXITY_FIELDS = {
    "max_added_lines",
    "max_new_modules",
    "max_new_dependencies",
    "allowed_cross_box_touches",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha(value: Any) -> bool:
    text = str(value)
    return len(text) == SHA256_HEX_LENGTH and all(ch in "0123456789abcdef" for ch in text)


def _hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def _fingerprint_rows(rows: Any, label: str) -> None:
    _assert(isinstance(rows, list) and rows, f"Q34 {label} fingerprints are required")
    paths: list[str] = []
    for row in rows:
        _assert(isinstance(row, Mapping), f"Q34 {label} row must be an object")
        _assert(all(field in row for field in ("path", "role", "sha256")), f"Q34 {label} row incomplete")
        path = str(row["path"]).strip()
        _assert(bool(path), f"Q34 {label} path is required")
        _assert(bool(str(row["role"]).strip()), f"Q34 {label} role is required")
        _assert(_sha(row["sha256"]), f"Q34 {label} SHA-256 invalid")
        paths.append(path)
    _assert(len(paths) == len(set(paths)), f"Q34 duplicate {label} path")


def _stats(values: list[float]) -> tuple[float, float, float, float]:
    median = statistics.median(values)
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    coefficient = stdev / mean if mean else math.inf
    return median, mean, stdev, coefficient


def valid_complete_record() -> dict[str, Any]:
    digest = "a" * 64
    measurements = [100.0, 101.0, 99.0, 100.5, 99.5, 100.2, 99.8]
    median, mean, stdev, coefficient = _stats(measurements)
    return {
        "profile_required": True,
        "no_optimization_evidence": [],
        "q33_decision_complete": True,
        "q33_frozen_baseline": True,
        "feature_id": "brick-wall-q34-profile-before-optimization-gate-enforcement-v1",
        "operation_id": "q34-profile-gate-validation",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "slow_path_name": "routing-score-evaluation",
        "slow_path_owner_box": "kanda_reasoner_app/routing_signal_scorer",
        "workload_name": "representative-routing-corpus-v1",
        "workload_description": "Evaluate the frozen representative routing corpus with production-equivalent options.",
        "workload_representative": True,
        "workload_inputs": [{"path": "benchmark_corpus/routes.json", "role": "WORKLOAD", "sha256": digest}],
        "workload_scale": {"cases": 500, "repetitions_per_case": 1},
        "source_fingerprints": [{"path": "kanda_reasoner_app/routing_signal_scorer/scorer.py", "role": "SLOW_PATH_SOURCE", "sha256": digest}],
        "environment_fingerprint": digest,
        "profiler_tool": "cProfile",
        "profiling_command": "python -m cProfile -o routing.prof tools/profile_routing.py",
        "baseline_metric": "wall_clock_latency",
        "baseline_unit": "milliseconds",
        "warmup_runs": 2,
        "measurement_runs": len(measurements),
        "baseline_measurements": measurements,
        "baseline_median": median,
        "baseline_mean": mean,
        "baseline_stdev": stdev,
        "baseline_coefficient_of_variation": coefficient,
        "variance_acceptance_threshold": 0.05,
        "variance_accepted": coefficient <= 0.05,
        "bottleneck_classification": "CPU",
        "bottleneck_evidence_hash": digest,
        "simpler_alternatives_considered": ["Remove duplicate normalization", "Reuse an existing immutable lookup"],
        "proposed_optimization": "Avoid repeated normalization in the measured owner-owned hot path.",
        "expected_improvement_metric": "median_wall_clock_latency_percent",
        "expected_improvement_target": 20.0,
        "minimum_acceptable_improvement": 10.0,
        "complexity_budget": {
            "max_added_lines": 120,
            "max_new_modules": 1,
            "max_new_dependencies": 0,
            "allowed_cross_box_touches": 0,
        },
        "rollback_condition": "Rollback if median gain is below 10% or correctness/regression markers change.",
        "durable_evidence_path": "project_validation_evidence/q34-profile-before-optimization.txt",
        "validators": ["tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py"],
        "expected_markers": ["Q34_PROFILE_BEFORE_OPTIMIZATION_REGRESSION_SET: PASS"],
        "limitations": ["Profile results apply only to the named workload and recorded environment."],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q35": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update({
        "profile_required": False,
        "no_optimization_evidence": [
            "The release changes governance prompts and validation-only tools; it changes no runtime algorithm, cache, concurrency, memory, I/O, database, startup, rendering, or latency path."
        ],
        "slow_path_name": "",
        "slow_path_owner_box": "",
        "workload_name": "",
        "workload_description": "",
        "workload_representative": False,
        "workload_inputs": [],
        "workload_scale": {},
        "source_fingerprints": [],
        "environment_fingerprint": "",
        "profiler_tool": "",
        "profiling_command": "",
        "baseline_metric": "",
        "baseline_unit": "",
        "warmup_runs": 0,
        "measurement_runs": 0,
        "baseline_measurements": [],
        "baseline_median": 0.0,
        "baseline_mean": 0.0,
        "baseline_stdev": 0.0,
        "baseline_coefficient_of_variation": 0.0,
        "variance_acceptance_threshold": 0.0,
        "variance_accepted": False,
        "bottleneck_classification": "",
        "bottleneck_evidence_hash": "",
        "simpler_alternatives_considered": [],
        "proposed_optimization": "",
        "expected_improvement_metric": "",
        "expected_improvement_target": 0.0,
        "minimum_acceptable_improvement": 0.0,
        "complexity_budget": {},
        "rollback_condition": "",
        "durable_evidence_path": "",
        "validators": [],
        "expected_markers": [],
        "limitations": ["No performance-motivated source change exists in this release."],
        "decision": "NOT_APPLICABLE",
    })
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def validate_record(record: Mapping[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS.difference(record))
    _assert(not missing, "Q34 record missing fields: " + ", ".join(missing))
    _assert(record["decision"] in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}, "Invalid Q34 decision")
    _assert(record["q33_decision_complete"] is True, "Q33 decision must be complete")
    _assert(record["q33_frozen_baseline"] is True, "Q33 frozen baseline is required")
    _assert(bool(str(record["feature_id"]).strip()), "Q34 feature ID is required")
    _assert(bool(str(record["operation_id"]).strip()), "Q34 operation ID is required")
    _assert(bool(str(record["primary_box"]).strip()), "Q34 primary box is required")
    _assert(record["may_begin_coding"] is False, "Q34 may not authorize coding")
    _assert(record["may_write_source"] is False, "Q34 may not authorize source writing")
    _assert(bool(record["limitations"]), "Q34 limitations are required")
    _assert(not record["unresolved_fields"], "Q34 unresolved fields remain")

    if record["decision"] == "COMPLETE":
        _assert(record["profile_required"] is True, "Q34 COMPLETE requires profiling")
        _assert(record["may_proceed_to_q35"] is True, "Q34 COMPLETE must permit Q35")
        for field in (
            "slow_path_name", "slow_path_owner_box", "workload_name", "workload_description",
            "environment_fingerprint", "profiler_tool", "profiling_command", "baseline_metric",
            "baseline_unit", "bottleneck_classification", "bottleneck_evidence_hash",
            "proposed_optimization", "expected_improvement_metric", "rollback_condition",
            "durable_evidence_path",
        ):
            _assert(bool(str(record[field]).strip()), f"Q34 field required: {field}")
        _assert(record["workload_representative"] is True, "Q34 workload must be representative")
        _fingerprint_rows(record["workload_inputs"], "workload")
        _fingerprint_rows(record["source_fingerprints"], "source")
        _assert(isinstance(record["workload_scale"], Mapping) and bool(record["workload_scale"]), "Q34 workload scale is required")
        _assert(_sha(record["environment_fingerprint"]), "Q34 environment fingerprint invalid")
        _assert(record["profiler_tool"] in PROFILER_TOOLS, "Q34 profiler tool invalid")
        _assert(int(record["warmup_runs"]) >= 1, "Q34 warmup runs are required")
        _assert(int(record["measurement_runs"]) >= 5, "Q34 repeated measurement count is too small")
        values = record["baseline_measurements"]
        _assert(isinstance(values, list) and len(values) == record["measurement_runs"], "Q34 measurements do not match run count")
        _assert(all(isinstance(value, (int, float)) and value > 0 for value in values), "Q34 measurement invalid")
        median, mean, stdev, coefficient = _stats([float(value) for value in values])
        for field, expected in (
            ("baseline_median", median),
            ("baseline_mean", mean),
            ("baseline_stdev", stdev),
            ("baseline_coefficient_of_variation", coefficient),
        ):
            _assert(math.isclose(float(record[field]), expected, rel_tol=1e-12, abs_tol=1e-12), f"Q34 {field} mismatch")
        threshold = float(record["variance_acceptance_threshold"])
        _assert(threshold > 0, "Q34 variance threshold is required")
        _assert(record["variance_accepted"] is (coefficient <= threshold), "Q34 variance decision mismatch")
        _assert(record["variance_accepted"] is True, "Q34 baseline variance is not accepted")
        _assert(record["bottleneck_classification"] in BOTTLENECK_CLASSES, "Q34 bottleneck classification invalid")
        _assert(_sha(record["bottleneck_evidence_hash"]), "Q34 bottleneck evidence hash invalid")
        _assert(isinstance(record["simpler_alternatives_considered"], list) and bool(record["simpler_alternatives_considered"]), "Q34 simpler alternatives are required")
        target = float(record["expected_improvement_target"])
        minimum = float(record["minimum_acceptable_improvement"])
        _assert(target > 0 and minimum > 0 and target >= minimum, "Q34 improvement targets invalid")
        budget = record["complexity_budget"]
        _assert(isinstance(budget, Mapping) and COMPLEXITY_FIELDS.issubset(budget), "Q34 complexity budget incomplete")
        _assert(all(isinstance(budget[field], int) and budget[field] >= 0 for field in COMPLEXITY_FIELDS), "Q34 complexity budget invalid")
        path = str(record["durable_evidence_path"]).replace("\\", "/")
        _assert(path.startswith("project_validation_evidence/"), "Q34 durable evidence owner invalid")
        _assert("daily_work" not in path and "delete_after" not in path, "Q34 transient evidence cannot be authoritative")
        _assert(bool(record["validators"]), "Q34 validators are required")
        _assert(bool(record["expected_markers"]), "Q34 expected markers are required")
    elif record["decision"] == "NOT_APPLICABLE":
        _assert(record["profile_required"] is False, "Q34 N/A must disable profiling")
        _assert(bool(record["no_optimization_evidence"]), "Q34 N/A evidence is required")
        _assert(record["may_proceed_to_q35"] is True, "Q34 N/A must permit Q35")
        for field in (
            "slow_path_name", "slow_path_owner_box", "workload_name", "workload_description",
            "environment_fingerprint", "profiler_tool", "profiling_command", "baseline_metric",
            "baseline_unit", "bottleneck_classification", "bottleneck_evidence_hash",
            "proposed_optimization", "expected_improvement_metric", "rollback_condition",
            "durable_evidence_path",
        ):
            _assert(not record[field], f"Q34 N/A must not set {field}")
        for field in ("workload_inputs", "source_fingerprints", "baseline_measurements", "validators", "expected_markers", "simpler_alternatives_considered"):
            _assert(not record[field], f"Q34 N/A must not set {field}")
        _assert(not record["workload_scale"] and not record["complexity_budget"], "Q34 N/A must not set workload or complexity")
    else:
        _assert(record["may_proceed_to_q35"] is False, "Blocked Q34 may not proceed")


def q34_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    q32 = "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py"
    q33 = "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py"
    q34 = "tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py"
    lessons = [
        "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
        "lesson-brick-wall-q03-validator-package-import-context-v1",
        "lesson-patch4-regression-validator-required-removed-patch5-placeholder-v1",
    ]
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "owner_box": "tools validation-only support" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Q34 governed profile-before-optimization release",
            "error_memory_lessons": lessons,
            "frozen_behavior": ["freeze-20260716-brick-wall-q33-pinned-local-model-provenance-validator-import-context-repair-v1r2"],
            "focused_tests": {"disposition": "APPLIES", "validators": [q32, q33, q34], "expected_markers": ["Q34_PROFILE_BEFORE_OPTIMIZATION_REGRESSION_SET: PASS"], "reason": "Q32/Q33 forward compatibility and Q34 contract behavior are checked."},
            "boundary_tests": {"disposition": "APPLIES", "validators": [q34], "expected_markers": ["Q34_NO_RUNTIME_PERFORMANCE_OWNER_MODIFIED: PASS"], "reason": "Performance specialists and runtime owners remain outside the governance box."},
            "gui_tests": {"disposition": "NOT_APPLICABLE", "validators": [], "expected_markers": [], "reason": "No GUI or Qt behavior is changed."},
            "delivery_tests": {"disposition": "APPLIES", "validators": [q34], "expected_markers": ["Q34_EXACT_RELEASE_PROVENANCE: PASS"], "reason": "Exact payload, import context, and durable evidence are checked."},
            "negative_tests": {"disposition": "APPLIES", "validators": [q34], "expected_markers": ["Q34_NEGATIVE_SINGLE_MEASUREMENT: PASS"], "reason": "Speculative, single-run, high-variance, and unclassified optimization records fail closed."},
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
        "required_validator_inventory": [q32, q33, q34],
        "uncovered_files": [],
        "orphan_required_validators": [],
        "conflicting_dispositions": [],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q32": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }
