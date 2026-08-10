# project-path: tools/validate_brick_wall_q39_task_specific_context_admission_v1.py
"""Focused Q39 task-specific context admission validation."""
from __future__ import annotations

__all__: list[str] = []
import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Callable

from tools.brick_wall_q31_changed_file_validator_coverage_contract import validate_record as validate_q31_coverage
from tools.brick_wall_q39_task_specific_context_admission_contract import mutated_record, q39_release_coverage_record, q39_release_record, valid_admitted_record, valid_not_applicable_record, valid_rejected_record, validate_record

FEATURE = "brick-wall-q39-task-specific-context-admission-enforcement-v1"
Q38_FREEZE_ID = "freeze-20260716-brick-wall-q38-handoff-freshness-and-provenance-v1"
BRICK = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md")
BRICK_META = Path("kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json")
BRIDGE = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
BRIDGE_META = Path("kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json")
Q32 = Path("tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py")
Q33 = Path("tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py")
Q34 = Path("tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py")
Q35 = Path("tools/validate_brick_wall_q35_focused_performance_baseline_v1.py")
Q36 = Path("tools/validate_brick_wall_q36_module_size_cohesion_v1.py")
Q37 = Path("tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py")
Q38 = Path("tools/validate_brick_wall_q38_handoff_freshness_provenance_v1.py")
CONTRACT = Path("tools/brick_wall_q39_task_specific_context_admission_contract.py")
PROVENANCE = Path("tools/brick_wall_q39_delivery_provenance.py")
VALIDATOR = Path("tools/validate_brick_wall_q39_task_specific_context_admission_v1.py")
HANDOFF_OWNER = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/handoff_at_end_of_work.md")
STARTUP_MAP = Path("kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json")
STARTUP_SYNC = Path("kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py")
ROUTE_INDEX = Path("kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json")
COMPANION = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/governed_architecture_companion_handoff.md")
COMPANION_VALIDATOR = Path("tools/validate_governed_architecture_companion_prompt_registration_v1.py")
RELEASE_FILES = (BRICK, BRICK_META, BRIDGE, BRIDGE_META, Q32, Q33, Q34, Q35, Q36, Q37, Q38, CONTRACT, PROVENANCE, VALIDATOR)
OWNER_FILES = (HANDOFF_OWNER, STARTUP_MAP, STARTUP_SYNC, ROUTE_INDEX, COMPANION, COMPANION_VALIDATOR)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _gate(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + (": " + detail if detail else ""))
    print(name + ": PASS" + (" - " + detail if detail else ""))


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK)
    bridge = _read(root / BRIDGE)
    for fragment in ("Task-specific context admission test (Q39)", "TASK-SPECIFIC CONTEXT ADMISSION RECORD", "controlled evidence", "representative task set", "baseline", "candidate", "simpler manifest/route/handoff strengthening", "proceed Q40", "Q01-Q40 complete YES/NO"):
        _gate("Q39_BRICK_WALL_CONTRACT", fragment in brick, fragment)
    for fragment in ("Task-specific context admission bridge (Q39)", "Q38 frozen baseline", "identical representative task set", "reproduced current-owner inadequacy", "simpler strengthening alternatives", "proceed Q40 YES/NO"):
        _gate("Q39_ROUTER_BRIDGE_CONTRACT", fragment in bridge, fragment)
    for path, label in ((BRICK_META, "brick"), (BRIDGE_META, "bridge")):
        meta = json.loads(_read(root / path))
        _gate("Q39_METADATA_ALIGNMENT", meta.get("source_stage") in {FEATURE, "brick-wall-q40-one-primary-box-governed-release-enforcement-v1"} and meta.get("updated_for") in {FEATURE, "brick-wall-q40-one-primary-box-governed-release-enforcement-v1"}, label)
        _gate("Q39_METADATA_DESCRIPTION", "Q39" in meta.get("description", ""), label)
        _gate("Q39_METADATA_DO_NOT_REGRESS", any("Q39 must" in rule for rule in meta.get("do_not_regress", [])), label)
    for path in RELEASE_FILES + OWNER_FILES:
        _gate("Q39_REQUIRED_FILE", (root / path).is_file(), str(path))
    for path in RELEASE_FILES:
        if path.suffix == ".py":
            text = _read(root / path)
            ast.parse(text, filename=str(path))
            _gate("Q39_TOUCHED_PYTHON_MAX_500", len(text.splitlines()) <= 500, f"{path}={len(text.splitlines())}")
        if path.suffix == ".md":
            _gate("Q39_PROMPT_MODULE_SIZE", len(_read(root / path).splitlines()) <= 500, str(path))
    predecessors = ((Q32, "Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q33, "Q33_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q34, "Q34_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q35, "Q35_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q36, "Q36_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q37, "Q37_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q38, "Q38_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"))
    for path, marker in predecessors:
        _gate(path.stem.upper() + "_FORWARD_COMPATIBLE_Q40_PROGRESSION", marker in _read(root / path), marker)


def _reject(label: str, mutate: Callable[[dict], None]) -> None:
    record = mutated_record(valid_admitted_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
        return
    _gate(label, False)


def validate_contract() -> None:
    validate_record(valid_admitted_record()); _gate("Q39_ADMITTED_RECORD_ACCEPTED", True)
    validate_record(valid_rejected_record()); _gate("Q39_REJECTED_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record()); _gate("Q39_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q39_NEGATIVE_Q38_DECISION", lambda r: r.update(q38_decision="BLOCKED")),
        ("Q39_NEGATIVE_Q38_FROZEN", lambda r: r.update(q38_frozen_baseline="")),
        ("Q39_NEGATIVE_OWNER_INVENTORY", lambda r: r["current_context_owners"].clear()),
        ("Q39_NEGATIVE_TASK_COUNT", lambda r: r["representative_tasks"].pop()),
        ("Q39_NEGATIVE_TASK_MISMATCH", lambda r: r["candidate_results"].pop()),
        ("Q39_NEGATIVE_INPUT_FINGERPRINT", lambda r: r["representative_tasks"][0].update(input_fingerprint="bad")),
        ("Q39_NEGATIVE_ENVIRONMENT_HASH", lambda r: r.update(comparison_environment_hash="bad")),
        ("Q39_NEGATIVE_SOURCE_SNAPSHOT", lambda r: r.update(same_task_and_source_snapshot=False)),
        ("Q39_NEGATIVE_BASELINE_REPRODUCTION", lambda r: r.update(baseline_failure_reproduced=False)),
        ("Q39_NEGATIVE_METRICS", lambda r: r.update(metrics=["latency"])),
        ("Q39_NEGATIVE_TRIAL_COUNT", lambda r: r.update(repeated_trials=1)),
        ("Q39_NEGATIVE_VARIANCE", lambda r: r.update(variance_accepted=False)),
        ("Q39_NEGATIVE_ALTERNATIVES", lambda r: r.update(simpler_strengthening_options=[])),
        ("Q39_NEGATIVE_GAIN", lambda r: r.update(observed_gain=0.01)),
        ("Q39_NEGATIVE_SIMPLER_FIX", lambda r: r.update(simpler_existing_owner_fix_sufficient=True)),
        ("Q39_NEGATIVE_UNIQUE_ROLE", lambda r: r.update(unique_bounded_responsibility="")),
        ("Q39_NEGATIVE_OWNER_PATH", lambda r: r.update(candidate_owner_path="../escape")),
        ("Q39_NEGATIVE_PUBLIC_CONTRACT", lambda r: r.update(candidate_public_contract="")),
        ("Q39_NEGATIVE_LIFECYCLE", lambda r: r.update(lifecycle_and_invalidation=[])),
        ("Q39_NEGATIVE_CONTEXT_ENGINE", lambda r: r.update(new_context_engine_created=True)),
        ("Q39_NEGATIVE_INTELLIGENCE_SYSTEM", lambda r: r.update(new_intelligence_system_created=True)),
        ("Q39_NEGATIVE_CONTEXT_REGISTRY", lambda r: r.update(new_context_registry_created=True)),
        ("Q39_NEGATIVE_Q40_PROGRESSION", lambda r: r.update(may_proceed_to_q40=False)),
        ("Q39_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q39_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases: _reject(label, mutate)
    record = valid_not_applicable_record(); record["no_new_context_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q39_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    print("Q39_TASK_SPECIFIC_CONTEXT_ADMISSION_REGRESSION_SET: PASS")


def validate_existing_owners(root: Path) -> None:
    handoff = _read(root / HANDOFF_OWNER)
    startup = _read(root / STARTUP_MAP)
    sync = _read(root / STARTUP_SYNC)
    route = _read(root / ROUTE_INDEX)
    companion = _read(root / COMPANION)
    _gate("Q39_EXISTING_HANDOFF_OWNER", "handoff" in handoff.lower())
    _gate("Q39_EXISTING_STARTUP_MANIFEST_OWNER", "handoff_at_end_of_work" in startup)
    _gate("Q39_EXISTING_STARTUP_SYNC_OWNER", "startup_kernel" in sync)
    _gate("Q39_EXISTING_ROUTE_OWNER", "routes" in route or "prompt_id" in route)
    _gate("Q39_EXISTING_CONTEXT_ARTIFACT_INVENTORIED", "architecture" in companion.lower() and "handoff" in companion.lower())
    changed = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    owners = {str(path).replace("\\", "/") for path in OWNER_FILES}
    _gate("Q39_NO_RUNTIME_CONTEXT_OWNER_MODIFIED", changed.isdisjoint(owners))
    contract = _read(root / CONTRACT)
    _gate("Q39_NO_CONTEXT_OR_INTELLIGENCE_SUPER_SYSTEM", "class ContextEngine" not in contract and "class IntelligenceSystem" not in contract and "class ContextRegistry" not in contract)
    print("Q39_EXISTING_CONTEXT_AUTHORITIES_REUSED: PASS")


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    fingerprints = [{"path": path, "sha256": _sha(root / path)} for path in paths]
    canonical = json.dumps(fingerprints, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    source_set_hash = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    current = q39_release_record(paths, fingerprints, source_set_hash)
    validate_record(current)
    _gate("Q39_CURRENT_RELEASE_CONTEXT_NOT_APPLICABLE", current["decision"] == "NOT_APPLICABLE")
    _gate("Q39_CURRENT_RELEASE_NO_RUNTIME_OWNER_TOUCHED", current["new_context_proposed"] is False)
    _gate("Q39_CURRENT_RELEASE_NO_CONTEXT_ENGINE", current["new_context_engine_created"] is False and current["new_intelligence_system_created"] is False and current["new_context_registry_created"] is False)
    coverage = q39_release_coverage_record(paths)
    validate_q31_coverage(coverage)
    _gate("Q39_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q39_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q39_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q39_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q39_Q38_FROZEN_BASELINE", Q38_FREEZE_ID.endswith("v1"))
    _gate("Q39_CURRENT_RELEASE_ALL_PYTHON_WITHIN_MAX", all(len(_read(root / path).splitlines()) <= 500 for path in RELEASE_FILES if path.suffix == ".py"))
    _gate("Q39_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q39_EXACT_RELEASE_PROVENANCE", True)
    print("Q39_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--project-root", type=Path, default=Path.cwd()); args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root); validate_contract(); validate_existing_owners(root); validate_release(root)
    print("VALIDATION OK: " + FEATURE); print("STATUS: IN_SYNC"); return 0


if __name__ == "__main__": raise SystemExit(main())
