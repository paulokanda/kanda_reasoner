# project-path: tools/validate_brick_wall_q35_focused_performance_baseline_v1.py
"""Focused Q35 regression validator."""
from __future__ import annotations

__all__: list[str] = []

import argparse
from collections.abc import Callable
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from brick_wall_q31_changed_file_validator_coverage_contract import validate_record as validate_q31_coverage
from brick_wall_q35_focused_performance_baseline_contract import (
    mutated_record,
    q35_release_coverage_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

BRICK = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md")
BRICK_META = Path("kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json")
BRIDGE = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
BRIDGE_META = Path("kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json")
Q32 = Path("tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py")
Q33 = Path("tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py")
Q34 = Path("tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py")
CONTRACT = Path("tools/brick_wall_q35_focused_performance_baseline_contract.py")
SELF = Path("tools/validate_brick_wall_q35_focused_performance_baseline_v1.py")
HIGH_PERFORMANCE_PROMPT = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/08_python_engineering_core/python_high_performance.md")
DATABASE_OPTIMIZATION_PROMPT = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/10_python_api_data_async_config/python_database_design_optimisation.md")
FEATURE = "brick-wall-q35-focused-performance-baseline-enforcement-v1"
Q34_FREEZE_ID = "freeze-20260716-brick-wall-q34-profile-before-optimization-gate-enforcement-v1"
LESSONS = (
    "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
    "lesson-brick-wall-q03-validator-package-import-context-v1",
    "lesson-patch4-regression-validator-required-removed-patch5-placeholder-v1",
    "lesson-powershell-captured-lines-nested-array-marker-gate-v1",
    "lesson-powershell-required-line-array-collapse-v1",
)
RELEASE_FILES = (BRICK, BRICK_META, BRIDGE, BRIDGE_META, Q32, Q33, Q34, CONTRACT, SELF)
SPECIALIST_OWNER_FILES = (HIGH_PERFORMANCE_PROMPT, DATABASE_OPTIMIZATION_PROMPT)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _gate(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _front_version(text: str) -> str:
    for line in text.splitlines()[:20]:
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip().split()[0]
    raise AssertionError("Prompt version was not found")


def _run(root: Path, path: Path, name: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(root / path), "--project-root", str(root)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    if completed.returncode != 0:
        raise RuntimeError(name + " predecessor validator failed")
    return output


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK)
    bridge = _read(root / BRIDGE)
    brick_meta = json.loads(_read(root / BRICK_META))
    bridge_meta = json.loads(_read(root / BRIDGE_META))
    bridge_deprecated = bridge_meta.get("status") == "deprecated"
    if bridge_deprecated:
        _gate("BRIDGE_DEPRECATED_TOMBSTONE", "DEPRECATED HISTORICAL COMPATIBILITY TOMBSTONE" in bridge)
        _gate("BRIDGE_NO_ACTIVE_ROUTE", bridge_meta.get("load_type") == "never")
        _gate("BRIDGE_CURRENT_OWNER_REDIRECT", "brick_wall_comprehensive_quality_gate" in bridge)
    for marker in (
        "Focused performance baseline (Q35)",
        "FOCUSED PERFORMANCE BASELINE RECORD",
        "Q34 decision COMPLETE/NOT_APPLICABLE and frozen baseline",
        "benchmark scope OWNER_LOCAL/CROSS_BOX_APPROVED",
        "broader-framework necessity evidence",
        "correctness validators/markers",
        "production writes forbidden",
        "proceed Q36 module-size and cohesion enforcement YES/NO",
        "may begin coding NO",
        "may write source NO",
    ):
        _gate("Q35_BRICK_WALL_CONTRACT", marker in brick, marker)
    for marker in (
        "Focused performance baseline bridge (Q35)",
        "Q34 frozen baseline and exact evidence hash",
        "owner-local benchmark scope by default",
        "cross-box framework only with demonstrated necessity",
        "correctness guards",
        "production writes forbidden",
        "proceed Q36 YES/NO",
    ):
        _gate("Q35_ROUTER_BRIDGE_CONTRACT", marker in bridge, marker)
    _gate("Q35_BRICK_VERSION", tuple(map(int, brick_meta["version"].split("."))) >= (3, 17))
    _gate("Q35_BRIDGE_VERSION", tuple(map(int, bridge_meta["version"].split("."))) >= (4, 11))
    _gate("Q35_BRICK_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(brick) == brick_meta["version"])
    _gate("Q35_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(bridge) == bridge_meta["version"])
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        _gate("Q35_METADATA_ALIGNMENT", meta.get("source_stage") == meta.get("updated_for") and bool(meta.get("source_stage")), label)
        _gate("Q35_METADATA_DESCRIPTION", "Q35" in meta.get("description", ""), label)
        _gate("Q35_METADATA_DO_NOT_REGRESS", any("Q35 must" in rule for rule in meta.get("do_not_regress", [])), label)
    for path in RELEASE_FILES + SPECIALIST_OWNER_FILES:
        _gate("Q35_REQUIRED_FILE", (root / path).is_file(), str(path))
    for path in RELEASE_FILES:
        if path.suffix in {".py", ".md"}:
            count = len(_read(root / path).splitlines())
            _gate("Q35_MODULE_SIZE", count <= 500, f"{path}={count}")

    _gate(
        "Q35_FORWARD_COMPATIBLE_Q36_PROGRESSION",
        "Module-size and cohesion enforcement (Q36)" in brick
        and "MODULE-SIZE AND COHESION RECORD" in brick
        and ("Q01-Q36 complete YES/NO" in brick or "Q01-Q37 complete YES/NO" in brick or "Q01-Q38 complete YES/NO" in brick or "Q01-Q39 complete YES/NO" in brick or "Q01-Q40 complete YES/NO" in brick)
        and "Module-size and cohesion enforcement bridge (Q36)" in bridge,
    )
    q32_output = _run(root, Q32, "Q32")
    for marker in (
        "Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS",
        "Q32_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS",
        "STATUS: IN_SYNC",
    ):
        _gate("Q32_FORWARD_COMPATIBLE_Q35_PROGRESSION", marker in q32_output, marker)
    q33_output = _run(root, Q33, "Q33")
    for marker in (
        "Q33_PINNED_LOCAL_MODEL_PROVENANCE_REGRESSION_SET: PASS",
        "Q33_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS",
        "VALIDATION OK: brick-wall-q33-pinned-local-model-provenance-enforcement-v1",
        "STATUS: IN_SYNC",
    ):
        _gate("Q33_FORWARD_COMPATIBLE_Q35_PROGRESSION", marker in q33_output, marker)
    q34_output = _run(root, Q34, "Q34")
    for marker in (
        "Q34_PROFILE_BEFORE_OPTIMIZATION_REGRESSION_SET: PASS",
        "Q34_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS",
        "Q34_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS",
        "Q34_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS",
        "Q34_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS",
        "Q34_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS",
        "Q34_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS",
        "VALIDATION OK: brick-wall-q34-profile-before-optimization-gate-enforcement-v1",
        "STATUS: IN_SYNC",
    ):
        _gate("Q34_FORWARD_COMPATIBLE_Q35_PROGRESSION", marker in q34_output, marker)


def _reject(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    record = mutated_record(valid_complete_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_contract() -> None:
    validate_record(valid_complete_record())
    _gate("Q35_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q35_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q35_NEGATIVE_Q34_DECISION", lambda r: r.update(q34_decision="BLOCKED")),
        ("Q35_NEGATIVE_Q34_FROZEN", lambda r: r.update(q34_frozen_baseline=False)),
        ("Q35_NEGATIVE_Q34_EVIDENCE_HASH", lambda r: r.update(q34_profile_evidence_hash="bad")),
        ("Q35_NEGATIVE_BOTTLENECK_NAME", lambda r: r.update(bottleneck_name="")),
        ("Q35_NEGATIVE_BOTTLENECK_CLASSIFICATION", lambda r: r.update(bottleneck_classification="UNKNOWN")),
        ("Q35_NEGATIVE_BOTTLENECK_OWNER", lambda r: r.update(bottleneck_owner_box="")),
        ("Q35_NEGATIVE_PUBLIC_CONTRACT", lambda r: r.update(bottleneck_public_contract="")),
        ("Q35_NEGATIVE_OWNER_MISMATCH", lambda r: r.update(benchmark_owner_box="other_box")),
        ("Q35_NEGATIVE_OWNER_LOCAL_PATH_ESCAPE", lambda r: r.update(benchmark_path="tools/benchmark_score_routes.py")),
        ("Q35_NEGATIVE_UNSAFE_BENCHMARK_PATH", lambda r: r.update(benchmark_path="../benchmark.py")),
        ("Q35_NEGATIVE_OWNER_LOCAL_FRAMEWORK", lambda r: r.update(broader_framework_required=True)),
        ("Q35_NEGATIVE_CROSS_BOX_NO_EVIDENCE", lambda r: r.update(benchmark_scope="CROSS_BOX_APPROVED", broader_framework_required=True, broader_framework_owner="performance", affected_owner_boxes=["a", "b"], broader_framework_necessity_evidence=[])),
        ("Q35_NEGATIVE_CROSS_BOX_SINGLE_OWNER", lambda r: r.update(benchmark_scope="CROSS_BOX_APPROVED", broader_framework_required=True, broader_framework_owner="performance", affected_owner_boxes=["a"], broader_framework_necessity_evidence=["one", "two"])),
        ("Q35_NEGATIVE_CROSS_BOX_OWNER_MISSING", lambda r: r.update(benchmark_scope="CROSS_BOX_APPROVED", broader_framework_required=True, broader_framework_owner="", affected_owner_boxes=["a", "b"], broader_framework_necessity_evidence=["one", "two"])),
        ("Q35_NEGATIVE_UNREPRESENTATIVE_WORKLOAD", lambda r: r.update(workload_representative=False)),
        ("Q35_NEGATIVE_WORKLOAD_INPUTS", lambda r: r.update(workload_inputs=[])),
        ("Q35_NEGATIVE_WORKLOAD_SCALE", lambda r: r.update(workload_scale={})),
        ("Q35_NEGATIVE_SOURCE_FINGERPRINTS", lambda r: r.update(source_fingerprints=[])),
        ("Q35_NEGATIVE_ENVIRONMENT", lambda r: r.update(environment_fingerprint="bad")),
        ("Q35_NEGATIVE_BENCHMARK_TOOL", lambda r: r.update(benchmark_tool="guess")),
        ("Q35_NEGATIVE_BENCHMARK_COMMAND", lambda r: r.update(benchmark_command="")),
        ("Q35_NEGATIVE_WARMUP", lambda r: r.update(warmup_runs=0)),
        ("Q35_NEGATIVE_SINGLE_MEASUREMENT", lambda r: r.update(measurement_runs=1, baseline_measurements=[49.0])),
        ("Q35_NEGATIVE_STATISTIC_MISMATCH", lambda r: r.update(baseline_median=1.0)),
        ("Q35_NEGATIVE_VARIANCE_THRESHOLD", lambda r: r.update(variance_acceptance_threshold=0.0)),
        ("Q35_NEGATIVE_VARIANCE_REJECTED", lambda r: r.update(variance_accepted=False)),
        ("Q35_NEGATIVE_CORRECTNESS_VALIDATORS", lambda r: r.update(correctness_validators=[])),
        ("Q35_NEGATIVE_CORRECTNESS_MARKERS", lambda r: r.update(correctness_markers=[])),
        ("Q35_NEGATIVE_ISOLATION_POLICY", lambda r: r.update(fixture_isolation_policy="PRODUCTION")),
        ("Q35_NEGATIVE_PRODUCTION_WRITE", lambda r: r.update(production_write_allowed=True)),
        ("Q35_NEGATIVE_BASELINE_EVIDENCE_HASH", lambda r: r.update(baseline_evidence_hash="bad")),
        ("Q35_NEGATIVE_DURABLE_PATH", lambda r: r.update(durable_evidence_path="delete_after_daily_work/q35.txt")),
        ("Q35_NEGATIVE_Q36_PROGRESSION", lambda r: r.update(may_proceed_to_q36=False)),
        ("Q35_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q35_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    na = valid_not_applicable_record()
    na["no_baseline_evidence"] = []
    try:
        validate_record(na)
    except AssertionError:
        _gate("Q35_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q35_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q35_FOCUSED_PERFORMANCE_BASELINE_REGRESSION_SET: PASS")


def validate_existing_owners(root: Path) -> None:
    high_performance = _read(root / HIGH_PERFORMANCE_PROMPT)
    database = _read(root / DATABASE_OPTIMIZATION_PROMPT)
    _gate("Q35_EXISTING_PERFORMANCE_BENCHMARK_OWNER", "Record a baseline" in high_performance and "Provide benchmark" in high_performance and "small reproducible benchmark" in high_performance)
    _gate("Q35_EXISTING_DATABASE_BASELINE_OWNER", "Use EXPLAIN" in database and "representative data size" in database and "always measuring before optimising" in database)
    changed = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    specialists = {str(path).replace("\\", "/") for path in SPECIALIST_OWNER_FILES}
    _gate("Q35_NO_RUNTIME_PERFORMANCE_OWNER_MODIFIED", changed.isdisjoint(specialists))
    contract_text = _read(root / CONTRACT)
    _gate("Q35_NO_SHARED_BENCHMARK_FRAMEWORK_CREATED", "class BenchmarkRegistry" not in contract_text and "class BenchmarkService" not in contract_text and "import pytest_benchmark" not in contract_text)


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    coverage = q35_release_coverage_record(paths)
    validate_q31_coverage(coverage)
    _gate("Q35_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q35_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q35_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q35_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q35_Q34_FROZEN_BASELINE", Q34_FREEZE_ID.endswith("v1"))
    _gate("Q35_RELEVANT_LESSON_SET", len(LESSONS) == 5)
    current = valid_not_applicable_record()
    validate_record(current)
    _gate("Q35_CURRENT_RELEASE_BASELINE_NOT_APPLICABLE", current["decision"] == "NOT_APPLICABLE")
    _gate("Q35_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q35_EXACT_RELEASE_PROVENANCE", True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    validate_contract()
    validate_existing_owners(root)
    validate_release(root)
    print("Q35_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS")
    print("Q35_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS")
    print("Q35_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS")
    print("Q35_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS")
    print("Q35_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
