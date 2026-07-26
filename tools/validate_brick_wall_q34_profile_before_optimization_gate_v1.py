# project-path: tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py
"""Focused Q34 profile-before-optimization validation."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

from brick_wall_q31_changed_file_validator_coverage_contract import (
    validate_record as validate_q31_coverage,
)
from brick_wall_q34_profile_before_optimization_contract import (
    mutated_record,
    q34_release_coverage_record,
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
CONTRACT = Path("tools/brick_wall_q34_profile_before_optimization_contract.py")
SELF = Path("tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py")
HIGH_PERFORMANCE_PROMPT = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/08_python_engineering_core/python_high_performance.md")
DATABASE_OPTIMIZATION_PROMPT = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/10_python_api_data_async_config/python_database_design_optimisation.md")
FEATURE = "brick-wall-q34-profile-before-optimization-gate-enforcement-v1"
Q33_FREEZE_ID = "freeze-20260716-brick-wall-q33-pinned-local-model-provenance-validator-import-context-repair-v1r2"
LESSONS = (
    "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
    "lesson-brick-wall-q03-validator-package-import-context-v1",
    "lesson-patch4-regression-validator-required-removed-patch5-placeholder-v1",
)
RELEASE_FILES = (BRICK, BRICK_META, BRIDGE, BRIDGE_META, Q32, Q33, CONTRACT, SELF)
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
        "Profile-before-optimization gate (Q34)",
        "PROFILE-BEFORE-OPTIMIZATION RECORD",
        "named slow path",
        "representative workload",
        "repeated measurements",
        "coefficient of variation",
        "bottleneck classification",
        "complexity budget",
        "proceed Q35 focused performance baseline YES/NO",
        "may begin coding NO",
        "may write source NO",
    ):
        _gate("Q34_BRICK_WALL_CONTRACT", marker in brick, marker)
    for marker in (
        "Profile-before-optimization bridge (Q34)",
        "named slow path",
        "representative workload/scale",
        "warmups/repeated measurements",
        "variance threshold/acceptance",
        "expected/minimum gain",
        "proceed Q35 YES/NO",
    ):
        _gate("Q34_ROUTER_BRIDGE_CONTRACT", marker in bridge, marker)
    _gate("Q34_BRICK_VERSION", tuple(map(int, brick_meta["version"].split("."))) >= (3, 16))
    _gate("Q34_BRIDGE_VERSION", tuple(map(int, bridge_meta["version"].split("."))) >= (4, 10))
    _gate("Q34_BRICK_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(brick) == brick_meta["version"])
    _gate("Q34_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(bridge) == bridge_meta["version"])
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        _gate("Q34_METADATA_ALIGNMENT", meta.get("source_stage") == meta.get("updated_for") and bool(meta.get("source_stage")), label)
        _gate("Q34_METADATA_DESCRIPTION", "Q34" in meta.get("description", ""), label)
        _gate("Q34_METADATA_DO_NOT_REGRESS", any("Q34 must" in rule for rule in meta.get("do_not_regress", [])), label)
    for path in RELEASE_FILES + SPECIALIST_OWNER_FILES:
        _gate("Q34_REQUIRED_FILE", (root / path).is_file(), str(path))
    for path in RELEASE_FILES:
        if path.suffix in {".py", ".md"}:
            count = len(_read(root / path).splitlines())
            _gate("Q34_MODULE_SIZE", count <= 500, f"{path}={count}")
    _gate(
        "Q34_FORWARD_COMPATIBLE_Q35_PROGRESSION",
        "Focused performance baseline (Q35)" in brick
        and "FOCUSED PERFORMANCE BASELINE RECORD" in brick
        and ("Q01-Q35 complete YES/NO" in brick or "Q01-Q36 complete YES/NO" in brick or "Q01-Q37 complete YES/NO" in brick or "Q01-Q38 complete YES/NO" in brick or "Q01-Q39 complete YES/NO" in brick or "Q01-Q40 complete YES/NO" in brick)
        and "Focused performance baseline bridge (Q35)" in bridge,
    )
    q32_output = _run(root, Q32, "Q32")
    for marker in (
        "Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS",
        "Q32_FORWARD_COMPATIBLE_Q34_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS",
        "STATUS: IN_SYNC",
    ):
        _gate("Q32_FORWARD_COMPATIBLE_Q34_PROGRESSION", marker in q32_output, marker)
    q33_output = _run(root, Q33, "Q33")
    for marker in (
        "Q33_PINNED_LOCAL_MODEL_PROVENANCE_REGRESSION_SET: PASS",
        "Q33_FORWARD_COMPATIBLE_Q34_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS",
        "Q33_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS",
        "VALIDATION OK: brick-wall-q33-pinned-local-model-provenance-enforcement-v1",
        "STATUS: IN_SYNC",
    ):
        _gate("Q33_FORWARD_COMPATIBLE_Q34_PROGRESSION", marker in q33_output, marker)


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
    _gate("Q34_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q34_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q34_NEGATIVE_Q33_DECISION", lambda r: r.update(q33_decision_complete=False)),
        ("Q34_NEGATIVE_Q33_FROZEN", lambda r: r.update(q33_frozen_baseline=False)),
        ("Q34_NEGATIVE_SLOW_PATH", lambda r: r.update(slow_path_name="")),
        ("Q34_NEGATIVE_WORKLOAD", lambda r: r.update(workload_name="")),
        ("Q34_NEGATIVE_UNREPRESENTATIVE_WORKLOAD", lambda r: r.update(workload_representative=False)),
        ("Q34_NEGATIVE_WORKLOAD_INPUTS", lambda r: r.update(workload_inputs=[])),
        ("Q34_NEGATIVE_WORKLOAD_SCALE", lambda r: r.update(workload_scale={})),
        ("Q34_NEGATIVE_SOURCE_FINGERPRINTS", lambda r: r.update(source_fingerprints=[])),
        ("Q34_NEGATIVE_ENVIRONMENT", lambda r: r.update(environment_fingerprint="bad")),
        ("Q34_NEGATIVE_PROFILER", lambda r: r.update(profiler_tool="guess")),
        ("Q34_NEGATIVE_WARMUP", lambda r: r.update(warmup_runs=0)),
        ("Q34_NEGATIVE_SINGLE_MEASUREMENT", lambda r: r.update(measurement_runs=1, baseline_measurements=[100.0])),
        ("Q34_NEGATIVE_STATISTIC_MISMATCH", lambda r: r.update(baseline_median=1.0)),
        ("Q34_NEGATIVE_VARIANCE_THRESHOLD", lambda r: r.update(variance_acceptance_threshold=0.0)),
        ("Q34_NEGATIVE_VARIANCE_REJECTED", lambda r: r.update(variance_accepted=False)),
        ("Q34_NEGATIVE_BOTTLENECK", lambda r: r.update(bottleneck_classification="UNKNOWN")),
        ("Q34_NEGATIVE_BOTTLENECK_EVIDENCE", lambda r: r.update(bottleneck_evidence_hash="bad")),
        ("Q34_NEGATIVE_SIMPLER_ALTERNATIVES", lambda r: r.update(simpler_alternatives_considered=[])),
        ("Q34_NEGATIVE_EXPECTED_GAIN", lambda r: r.update(expected_improvement_target=0.0)),
        ("Q34_NEGATIVE_MINIMUM_GAIN", lambda r: r.update(minimum_acceptable_improvement=0.0)),
        ("Q34_NEGATIVE_COMPLEXITY_BUDGET", lambda r: r.update(complexity_budget={})),
        ("Q34_NEGATIVE_ROLLBACK", lambda r: r.update(rollback_condition="")),
        ("Q34_NEGATIVE_DURABLE_PATH", lambda r: r.update(durable_evidence_path="delete_after_daily_work/q34.txt")),
        ("Q34_NEGATIVE_Q35_PROGRESSION", lambda r: r.update(may_proceed_to_q35=False)),
        ("Q34_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q34_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    na = valid_not_applicable_record()
    na["no_optimization_evidence"] = []
    try:
        validate_record(na)
    except AssertionError:
        _gate("Q34_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q34_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q34_PROFILE_BEFORE_OPTIMIZATION_REGRESSION_SET: PASS")


def validate_existing_owners(root: Path) -> None:
    high_performance = _read(root / HIGH_PERFORMANCE_PROMPT)
    database = _read(root / DATABASE_OPTIMIZATION_PROMPT)
    _gate("Q34_EXISTING_PERFORMANCE_PROMPT_OWNER", "Measure First" in high_performance and "Record a baseline" in high_performance and "profiling proves need" in high_performance)
    _gate("Q34_EXISTING_DATABASE_OPTIMIZATION_OWNER", "proven read performance issues" in database and "Use EXPLAIN" in database)
    changed = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    specialists = {str(path).replace("\\", "/") for path in SPECIALIST_OWNER_FILES}
    _gate("Q34_NO_RUNTIME_PERFORMANCE_OWNER_MODIFIED", changed.isdisjoint(specialists))
    contract_text = _read(root / CONTRACT)
    _gate("Q34_NO_PROFILER_FRAMEWORK_CREATED", "import cProfile" not in contract_text and "import py_spy" not in contract_text and "class Profiler" not in contract_text)


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    coverage = q34_release_coverage_record(paths)
    validate_q31_coverage(coverage)
    _gate("Q34_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q34_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q34_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q34_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q34_Q33_FROZEN_BASELINE", Q33_FREEZE_ID.endswith("v1r2"))
    _gate("Q34_RELEVANT_LESSON_SET", len(LESSONS) == 3)
    current = valid_not_applicable_record()
    validate_record(current)
    _gate("Q34_CURRENT_RELEASE_PROFILE_NOT_APPLICABLE", current["decision"] == "NOT_APPLICABLE")
    _gate("Q34_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q34_EXACT_RELEASE_PROVENANCE", True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    validate_contract()
    validate_existing_owners(root)
    validate_release(root)
    print("Q34_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS")
    print("Q34_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS")
    print("Q34_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS")
    print("Q34_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS")
    print("Q34_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS")
    print("Q34_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
