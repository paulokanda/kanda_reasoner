# project-path: tools/brick_wall_q35_focused_performance_baseline_contract.py
"""Validation-only Q35 focused performance baseline contract."""
from __future__ import annotations

from copy import deepcopy
import math
import statistics
from pathlib import PurePosixPath
from typing import Any, Mapping

__all__: list[str] = []

SHA256_HEX_LENGTH = 64
BENCHMARK_SCOPES = {"OWNER_LOCAL", "CROSS_BOX_APPROVED"}
BENCHMARK_TOOLS = {
    "timeit",
    "pytest-benchmark",
    "instrumented_timer",
    "database_explain",
    "cProfile",
    "py-spy",
}
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
ISOLATION_POLICIES = {"READ_ONLY", "DISPOSABLE_FIXTURE", "READ_ONLY_OR_DISPOSABLE"}
REQUIRED_FIELDS = {
    "baseline_required",
    "no_baseline_evidence",
    "q34_decision",
    "q34_frozen_baseline",
    "q34_profile_evidence_hash",
    "feature_id",
    "operation_id",
    "primary_box",
    "bottleneck_name",
    "bottleneck_classification",
    "bottleneck_owner_box",
    "bottleneck_public_contract",
    "benchmark_scope",
    "benchmark_owner_box",
    "benchmark_path",
    "broader_framework_required",
    "broader_framework_necessity_evidence",
    "broader_framework_owner",
    "affected_owner_boxes",
    "workload_name",
    "workload_description",
    "workload_representative",
    "workload_inputs",
    "workload_scale",
    "source_fingerprints",
    "environment_fingerprint",
    "benchmark_tool",
    "benchmark_command",
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
    "correctness_validators",
    "correctness_markers",
    "fixture_isolation_policy",
    "production_write_allowed",
    "baseline_evidence_hash",
    "durable_evidence_path",
    "validators",
    "expected_markers",
    "limitations",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q36",
    "may_begin_coding",
    "may_write_source",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha(value: Any) -> bool:
    text = str(value)
    return len(text) == SHA256_HEX_LENGTH and all(ch in "0123456789abcdef" for ch in text)


def _fingerprint_rows(rows: Any, label: str) -> None:
    _assert(isinstance(rows, list) and rows, f"Q35 {label} fingerprints are required")
    paths: list[str] = []
    for row in rows:
        _assert(isinstance(row, Mapping), f"Q35 {label} row must be an object")
        _assert(all(field in row for field in ("path", "role", "sha256")), f"Q35 {label} row incomplete")
        path = str(row["path"]).strip()
        _assert(bool(path), f"Q35 {label} path is required")
        _assert(bool(str(row["role"]).strip()), f"Q35 {label} role is required")
        _assert(_sha(row["sha256"]), f"Q35 {label} SHA-256 invalid")
        paths.append(path)
    _assert(len(paths) == len(set(paths)), f"Q35 duplicate {label} path")


def _stats(values: list[float]) -> tuple[float, float, float, float]:
    median = statistics.median(values)
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    coefficient = stdev / mean if mean else math.inf
    return median, mean, stdev, coefficient


def _relative_safe(path: str) -> bool:
    candidate = PurePosixPath(path.replace("\\", "/"))
    return bool(path.strip()) and not candidate.is_absolute() and ".." not in candidate.parts


def _under_owner(path: str, owner: str) -> bool:
    normalized_path = path.replace("\\", "/").strip("/")
    normalized_owner = owner.replace("\\", "/").strip("/")
    return normalized_path == normalized_owner or normalized_path.startswith(normalized_owner + "/")


def valid_complete_record() -> dict[str, Any]:
    digest = "a" * 64
    measurements = [48.8, 49.2, 49.0, 48.9, 49.1, 49.0, 48.95]
    median, mean, stdev, coefficient = _stats(measurements)
    owner = "kanda_reasoner_app/routing_signal_scorer"
    return {
        "baseline_required": True,
        "no_baseline_evidence": [],
        "q34_decision": "COMPLETE",
        "q34_frozen_baseline": True,
        "q34_profile_evidence_hash": digest,
        "feature_id": "brick-wall-q35-focused-performance-baseline-enforcement-v1",
        "operation_id": "q35-focused-baseline-validation",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "bottleneck_name": "routing-score-evaluation",
        "bottleneck_classification": "CPU",
        "bottleneck_owner_box": owner,
        "bottleneck_public_contract": "kanda_reasoner_app.routing_signal_scorer.score_routes",
        "benchmark_scope": "OWNER_LOCAL",
        "benchmark_owner_box": owner,
        "benchmark_path": owner + "/benchmarks/benchmark_score_routes.py",
        "broader_framework_required": False,
        "broader_framework_necessity_evidence": [],
        "broader_framework_owner": "",
        "affected_owner_boxes": [owner],
        "workload_name": "representative-routing-corpus-v1",
        "workload_description": "Run the frozen representative route corpus through the owner public contract.",
        "workload_representative": True,
        "workload_inputs": [{"path": "benchmark_corpus/routes.json", "role": "WORKLOAD", "sha256": digest}],
        "workload_scale": {"cases": 500, "repetitions_per_case": 1},
        "source_fingerprints": [{"path": owner + "/scorer.py", "role": "SLOW_PATH_SOURCE", "sha256": digest}],
        "environment_fingerprint": digest,
        "benchmark_tool": "timeit",
        "benchmark_command": "python -m timeit -s 'from benchmark_score_routes import run' 'run()'",
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
        "correctness_validators": ["tools/validate_routing_signal_scorer_v1.py"],
        "correctness_markers": ["ROUTING_SIGNAL_SCORER_BEHAVIOR: PASS"],
        "fixture_isolation_policy": "READ_ONLY_OR_DISPOSABLE",
        "production_write_allowed": False,
        "baseline_evidence_hash": digest,
        "durable_evidence_path": "project_validation_evidence/q35-focused-performance-baseline.txt",
        "validators": ["tools/validate_brick_wall_q35_focused_performance_baseline_v1.py"],
        "expected_markers": ["Q35_FOCUSED_PERFORMANCE_BASELINE_REGRESSION_SET: PASS"],
        "limitations": ["The baseline is authoritative only for the named workload, source fingerprints, and environment."],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q36": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update({
        "baseline_required": False,
        "no_baseline_evidence": [
            "The release changes governance prompts and validation-only tools and Q34 classified the release itself as NOT_APPLICABLE for runtime profiling."
        ],
        "q34_decision": "NOT_APPLICABLE",
        "q34_profile_evidence_hash": "",
        "bottleneck_name": "",
        "bottleneck_classification": "",
        "bottleneck_owner_box": "",
        "bottleneck_public_contract": "",
        "benchmark_scope": "",
        "benchmark_owner_box": "",
        "benchmark_path": "",
        "broader_framework_required": False,
        "broader_framework_necessity_evidence": [],
        "broader_framework_owner": "",
        "affected_owner_boxes": [],
        "workload_name": "",
        "workload_description": "",
        "workload_representative": False,
        "workload_inputs": [],
        "workload_scale": {},
        "source_fingerprints": [],
        "environment_fingerprint": "",
        "benchmark_tool": "",
        "benchmark_command": "",
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
        "correctness_validators": [],
        "correctness_markers": [],
        "fixture_isolation_policy": "",
        "production_write_allowed": False,
        "baseline_evidence_hash": "",
        "durable_evidence_path": "",
        "validators": [],
        "expected_markers": [],
        "limitations": ["No proven runtime bottleneck is being benchmarked by this release."],
        "decision": "NOT_APPLICABLE",
    })
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def validate_record(record: Mapping[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS.difference(record))
    _assert(not missing, "Q35 record missing fields: " + ", ".join(missing))
    _assert(record["decision"] in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}, "Invalid Q35 decision")
    _assert(record["q34_decision"] in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}, "Invalid Q34 decision")
    _assert(record["q34_frozen_baseline"] is True, "Q34 frozen baseline is required")
    _assert(bool(str(record["feature_id"]).strip()), "Q35 feature ID is required")
    _assert(bool(str(record["operation_id"]).strip()), "Q35 operation ID is required")
    _assert(bool(str(record["primary_box"]).strip()), "Q35 primary box is required")
    _assert(record["may_begin_coding"] is False, "Q35 may not authorize coding")
    _assert(record["may_write_source"] is False, "Q35 may not authorize source writing")
    _assert(bool(record["limitations"]), "Q35 limitations are required")
    _assert(not record["unresolved_fields"], "Q35 unresolved fields remain")

    if record["decision"] == "COMPLETE":
        _assert(record["baseline_required"] is True, "Q35 COMPLETE requires a baseline")
        _assert(record["q34_decision"] == "COMPLETE", "Q35 COMPLETE requires Q34 COMPLETE")
        _assert(_sha(record["q34_profile_evidence_hash"]), "Q35 Q34 evidence hash invalid")
        _assert(record["may_proceed_to_q36"] is True, "Q35 COMPLETE must permit Q36")
        for field in (
            "bottleneck_name",
            "bottleneck_classification",
            "bottleneck_owner_box",
            "bottleneck_public_contract",
            "benchmark_scope",
            "benchmark_owner_box",
            "benchmark_path",
            "workload_name",
            "workload_description",
            "environment_fingerprint",
            "benchmark_tool",
            "benchmark_command",
            "baseline_metric",
            "baseline_unit",
            "fixture_isolation_policy",
            "baseline_evidence_hash",
            "durable_evidence_path",
        ):
            _assert(bool(str(record[field]).strip()), f"Q35 field required: {field}")
        _assert(record["bottleneck_classification"] in BOTTLENECK_CLASSES, "Q35 bottleneck classification invalid")
        _assert(record["benchmark_scope"] in BENCHMARK_SCOPES, "Q35 benchmark scope invalid")
        _assert(_relative_safe(record["benchmark_path"]), "Q35 benchmark path must be safe and relative")
        owners = record["affected_owner_boxes"]
        _assert(isinstance(owners, list) and owners and len(owners) == len(set(owners)), "Q35 affected owner boxes invalid")
        if record["benchmark_scope"] == "OWNER_LOCAL":
            _assert(record["broader_framework_required"] is False, "Q35 owner-local scope cannot require a broader framework")
            _assert(record["benchmark_owner_box"] == record["bottleneck_owner_box"], "Q35 benchmark owner must match bottleneck owner")
            _assert(_under_owner(record["benchmark_path"], record["bottleneck_owner_box"]), "Q35 benchmark path must remain under the owner box")
            _assert(owners == [record["bottleneck_owner_box"]], "Q35 owner-local benchmark must list one owner")
            _assert(not record["broader_framework_necessity_evidence"], "Q35 owner-local scope must not invent framework evidence")
            _assert(not str(record["broader_framework_owner"]).strip(), "Q35 owner-local scope must not declare a framework owner")
        else:
            _assert(record["broader_framework_required"] is True, "Q35 cross-box scope requires an explicit broader-framework decision")
            evidence = record["broader_framework_necessity_evidence"]
            _assert(isinstance(evidence, list) and len(evidence) >= 2 and all(str(item).strip() for item in evidence), "Q35 broader-framework necessity evidence is insufficient")
            _assert(bool(str(record["broader_framework_owner"]).strip()), "Q35 broader-framework owner is required")
            _assert(len(owners) >= 2, "Q35 cross-box benchmark must name at least two affected owners")
        _assert(record["workload_representative"] is True, "Q35 workload must be representative")
        _fingerprint_rows(record["workload_inputs"], "workload")
        _fingerprint_rows(record["source_fingerprints"], "source")
        _assert(isinstance(record["workload_scale"], Mapping) and bool(record["workload_scale"]), "Q35 workload scale is required")
        _assert(_sha(record["environment_fingerprint"]), "Q35 environment fingerprint invalid")
        _assert(record["benchmark_tool"] in BENCHMARK_TOOLS, "Q35 benchmark tool invalid")
        _assert(int(record["warmup_runs"]) >= 1, "Q35 warmup runs are required")
        _assert(int(record["measurement_runs"]) >= 5, "Q35 repeated measurement count is too small")
        values = record["baseline_measurements"]
        _assert(isinstance(values, list) and len(values) == record["measurement_runs"], "Q35 measurements do not match run count")
        _assert(all(isinstance(value, (int, float)) and value > 0 for value in values), "Q35 measurement invalid")
        median, mean, stdev, coefficient = _stats([float(value) for value in values])
        for field, expected in (
            ("baseline_median", median),
            ("baseline_mean", mean),
            ("baseline_stdev", stdev),
            ("baseline_coefficient_of_variation", coefficient),
        ):
            _assert(math.isclose(float(record[field]), expected, rel_tol=1e-12, abs_tol=1e-12), f"Q35 {field} mismatch")
        threshold = float(record["variance_acceptance_threshold"])
        _assert(threshold > 0, "Q35 variance threshold is required")
        _assert(record["variance_accepted"] is (coefficient <= threshold), "Q35 variance decision mismatch")
        _assert(record["variance_accepted"] is True, "Q35 baseline variance is not accepted")
        _assert(isinstance(record["correctness_validators"], list) and bool(record["correctness_validators"]), "Q35 correctness validators are required")
        _assert(isinstance(record["correctness_markers"], list) and bool(record["correctness_markers"]), "Q35 correctness markers are required")
        _assert(record["fixture_isolation_policy"] in ISOLATION_POLICIES, "Q35 fixture isolation policy invalid")
        _assert(record["production_write_allowed"] is False, "Q35 benchmark may not mutate production state")
        _assert(_sha(record["baseline_evidence_hash"]), "Q35 baseline evidence hash invalid")
        _assert(record["durable_evidence_path"].startswith("project_validation_evidence/"), "Q35 evidence must be durable project support")
        _assert(bool(record["validators"]), "Q35 validators are required")
        _assert(bool(record["expected_markers"]), "Q35 expected markers are required")
    elif record["decision"] == "NOT_APPLICABLE":
        _assert(record["baseline_required"] is False, "Q35 NOT_APPLICABLE cannot require a baseline")
        _assert(record["q34_decision"] == "NOT_APPLICABLE", "Q35 NOT_APPLICABLE requires Q34 NOT_APPLICABLE")
        _assert(isinstance(record["no_baseline_evidence"], list) and bool(record["no_baseline_evidence"]), "Q35 N/A evidence is required")
        _assert(record["may_proceed_to_q36"] is True, "Q35 N/A must permit Q36")
        for field in (
            "q34_profile_evidence_hash",
            "bottleneck_name",
            "bottleneck_classification",
            "bottleneck_owner_box",
            "bottleneck_public_contract",
            "benchmark_scope",
            "benchmark_owner_box",
            "benchmark_path",
            "broader_framework_owner",
            "workload_name",
            "workload_description",
            "environment_fingerprint",
            "benchmark_tool",
            "benchmark_command",
            "baseline_metric",
            "baseline_unit",
            "fixture_isolation_policy",
            "baseline_evidence_hash",
            "durable_evidence_path",
        ):
            _assert(not str(record[field]).strip(), f"Q35 N/A field must be empty: {field}")
        for field in (
            "broader_framework_necessity_evidence",
            "affected_owner_boxes",
            "workload_inputs",
            "source_fingerprints",
            "baseline_measurements",
            "correctness_validators",
            "correctness_markers",
            "validators",
            "expected_markers",
        ):
            _assert(not record[field], f"Q35 N/A collection must be empty: {field}")
        _assert(record["broader_framework_required"] is False, "Q35 N/A cannot require a framework")
        _assert(record["production_write_allowed"] is False, "Q35 N/A cannot allow production writes")
    else:
        _assert(record["may_proceed_to_q36"] is False, "Q35 BLOCKED cannot permit Q36")


def q35_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    q32 = "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py"
    q33 = "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py"
    q34 = "tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py"
    q35 = "tools/validate_brick_wall_q35_focused_performance_baseline_v1.py"
    lessons = [
        "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
        "lesson-brick-wall-q03-validator-package-import-context-v1",
        "lesson-patch4-regression-validator-required-removed-patch5-placeholder-v1",
        "lesson-powershell-captured-lines-nested-array-marker-gate-v1",
        "lesson-powershell-required-line-array-collapse-v1",
    ]
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "owner_box": "tools validation-only support" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Q35 governed focused performance baseline release",
            "error_memory_lessons": lessons,
            "frozen_behavior": ["freeze-20260716-brick-wall-q34-profile-before-optimization-gate-enforcement-v1"],
            "focused_tests": {
                "disposition": "APPLIES",
                "validators": [q32, q33, q34, q35],
                "expected_markers": ["Q35_FOCUSED_PERFORMANCE_BASELINE_REGRESSION_SET: PASS"],
                "reason": "Q32-Q34 forward compatibility and Q35 owner-local baseline behavior are checked.",
            },
            "boundary_tests": {
                "disposition": "APPLIES",
                "validators": [q35],
                "expected_markers": ["Q35_NO_SHARED_BENCHMARK_FRAMEWORK_CREATED: PASS"],
                "reason": "The release must not modify runtime owners or create a shared benchmark service.",
            },
            "gui_tests": {
                "disposition": "NOT_APPLICABLE",
                "validators": [],
                "expected_markers": [],
                "reason": "No GUI or Qt behavior is changed.",
            },
            "delivery_tests": {
                "disposition": "APPLIES",
                "validators": [q35],
                "expected_markers": ["Q35_EXACT_RELEASE_PROVENANCE: PASS"],
                "reason": "Exact payload, import context, durable evidence, and Q34 frozen lineage are checked.",
            },
            "negative_tests": {
                "disposition": "APPLIES",
                "validators": [q35],
                "expected_markers": ["Q35_NEGATIVE_OWNER_LOCAL_PATH_ESCAPE: PASS"],
                "reason": "Owner drift, unstable timing, missing correctness guards, production writes, and unjustified shared frameworks fail closed.",
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
        "required_validator_inventory": [q32, q33, q34, q35],
        "uncovered_files": [],
        "orphan_required_validators": [],
        "conflicting_dispositions": [],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q32": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }
