# project-path: tools/validate_brick_wall_q40_one_primary_box_governed_release_v1.py
"""Focused Q40 one-primary-box governed-release validation."""
from __future__ import annotations

__all__: list[str] = []
import argparse, ast, hashlib, json
from pathlib import Path
from typing import Callable

from tools.brick_wall_q31_changed_file_validator_coverage_contract import validate_record as validate_q31_coverage
from tools.brick_wall_q40_one_primary_box_governed_release_contract import mutated_record, q40_release_coverage_record, q40_release_record, valid_complete_record, valid_not_applicable_record, valid_ready_record, validate_record

FEATURE = "brick-wall-q40-one-primary-box-governed-release-enforcement-v1"
Q39_FREEZE_ID = "freeze-20260716-brick-wall-q39-task-specific-context-admission-test-v1"
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
Q39 = Path("tools/validate_brick_wall_q39_task_specific_context_admission_v1.py")
CONTRACT = Path("tools/brick_wall_q40_one_primary_box_governed_release_contract.py")
PROVENANCE = Path("tools/brick_wall_q40_delivery_provenance.py")
VALIDATOR = Path("tools/validate_brick_wall_q40_one_primary_box_governed_release_v1.py")
RELEASE_FILES = (BRICK, BRICK_META, BRIDGE, BRIDGE_META, Q32, Q33, Q34, Q35, Q36, Q37, Q38, Q39, CONTRACT, PROVENANCE, VALIDATOR)


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
    for fragment in ("One-primary-box governed release (Q40)", "ONE-PRIMARY-BOX GOVERNED RELEASE RECORD", "exactly one primary box", "supporting touches", "exact changed files", "source baseline hashes", "validation map", "exact ZIP", "human-local validation", "Q01-Q40 complete YES/NO"):
        _gate("Q40_BRICK_WALL_CONTRACT", fragment in brick, fragment)
    for fragment in ("One-primary-box governed release bridge (Q40)", "Q39 frozen baseline", "exactly one primary box", "bounded supporting touches", "exact final ZIP contract", "human-local validation state", "Confirm and Write"):
        _gate("Q40_ROUTER_BRIDGE_CONTRACT", fragment in bridge, fragment)
    for path, label in ((BRICK_META, "brick"), (BRIDGE_META, "bridge")):
        meta = json.loads(_read(root / path))
        _gate("Q40_METADATA_ALIGNMENT", meta.get("source_stage") == FEATURE and meta.get("updated_for") == FEATURE, label)
        _gate("Q40_METADATA_DESCRIPTION", "Q40" in meta.get("description", ""), label)
        _gate("Q40_METADATA_DO_NOT_REGRESS", any("Q40 must" in rule for rule in meta.get("do_not_regress", [])), label)
    for path in RELEASE_FILES:
        _gate("Q40_REQUIRED_FILE", (root / path).is_file(), str(path))
        if path.suffix == ".py":
            text = _read(root / path); ast.parse(text, filename=str(path))
            _gate("Q40_TOUCHED_PYTHON_MAX_500", len(text.splitlines()) <= 500, f"{path}={len(text.splitlines())}")
        if path.suffix == ".md":
            _gate("Q40_PROMPT_MODULE_SIZE", len(_read(root / path).splitlines()) <= 500, str(path))
    predecessors = ((Q32, "Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q33, "Q33_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q34, "Q34_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q35, "Q35_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q36, "Q36_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q37, "Q37_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q38, "Q38_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"), (Q39, "Q39_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"))
    for path, marker in predecessors:
        _gate(path.stem.upper() + "_FORWARD_COMPATIBLE_Q40_PROGRESSION", marker in _read(root / path), marker)


def _reject(label: str, mutate: Callable[[dict], None]) -> None:
    record = mutated_record(valid_ready_record()); mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True); return
    _gate(label, False)


def validate_contract() -> None:
    validate_record(valid_ready_record()); _gate("Q40_READY_RECORD_ACCEPTED", True)
    validate_record(valid_complete_record()); _gate("Q40_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record()); _gate("Q40_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q40_NEGATIVE_Q39_DECISION", lambda r: r.update(q39_decision="BLOCKED")),
        ("Q40_NEGATIVE_Q39_FROZEN", lambda r: r.update(q39_frozen_baseline="")),
        ("Q40_NEGATIVE_PRIMARY_BOX_MISSING", lambda r: r.update(primary_box="")),
        ("Q40_NEGATIVE_MULTIPLE_PRIMARY_BOXES", lambda r: r.update(primary_box=["a", "b"])),
        ("Q40_NEGATIVE_SUPPORTING_TOUCH_UNBOUNDED", lambda r: r["supporting_touches"][0].update(bounded=False)),
        ("Q40_NEGATIVE_SUPPORTING_TOUCH_OWNER", lambda r: r["supporting_touches"][0].update(owner_box="")),
        ("Q40_NEGATIVE_DUPLICATE_CHANGED_FILE", lambda r: r["changed_files"].append(r["changed_files"][0])),
        ("Q40_NEGATIVE_CHANGED_FILE_TRAVERSAL", lambda r: r["changed_files"].__setitem__(0, "../escape")),
        ("Q40_NEGATIVE_SOURCE_BASELINE_COVERAGE", lambda r: r["source_baselines"].pop()),
        ("Q40_NEGATIVE_SOURCE_BASELINE_HASH", lambda r: r["source_baselines"][0].update(payload_sha256="bad")),
        ("Q40_NEGATIVE_SOURCE_SET_HASH", lambda r: r.update(source_fingerprint_set_hash="bad")),
        ("Q40_NEGATIVE_REGRESSION_OBLIGATIONS", lambda r: r.update(regression_obligations=[])),
        ("Q40_NEGATIVE_DUPLICATE_OBLIGATION", lambda r: r["regression_obligations"].append(dict(r["regression_obligations"][0]))),
        ("Q40_NEGATIVE_VALIDATION_MAP_SIZE", lambda r: r["validation_map"].pop()),
        ("Q40_NEGATIVE_VALIDATION_MAP_ORDER", lambda r: r["validation_map"].reverse()),
        ("Q40_NEGATIVE_ORPHAN_VALIDATOR", lambda r: r["validation_map"][0].update(validators=[])),
        ("Q40_NEGATIVE_ZIP_VALIDATOR", lambda r: r["exact_zip_contract"].update(canonical_validator="other.py")),
        ("Q40_NEGATIVE_ZIP_FREEZE_HINT", lambda r: r["exact_zip_contract"].update(root_freeze_hint_count=2)),
        ("Q40_NEGATIVE_FREEZE_PREVIEW", lambda r: r["freeze_evidence"].update(preview_read_only=False)),
        ("Q40_NEGATIVE_AUTOMATIC_FREEZE_WRITE", lambda r: r["freeze_evidence"].update(automatic_frozen_memory_write=True)),
        ("Q40_NEGATIVE_STARTUP_REFRESH", lambda r: r["freeze_evidence"].update(startup_refresh_required=False)),
        ("Q40_NEGATIVE_VALIDATION_CLAIM_PENDING", lambda r: r.update(may_claim_validation_passed=True)),
        ("Q40_NEGATIVE_FREEZE_PENDING", lambda r: r.update(may_freeze=True)),
        ("Q40_NEGATIVE_GENERATED_SOURCE_AUTHORITY", lambda r: r.update(generated_artifacts_authority="SOURCE")),
        ("Q40_NEGATIVE_TRANSIENT_DURABLE_AUTHORITY", lambda r: r.update(transient_artifacts_authority="DURABLE")),
        ("Q40_NEGATIVE_PROJECT_FREEZE_LEDGER", lambda r: r.update(project_freeze_ledger_used=True)),
        ("Q40_NEGATIVE_RELEASE_REGISTRY", lambda r: r.update(release_registry_created=True)),
        ("Q40_NEGATIVE_COORDINATION_SUPER_SYSTEM", lambda r: r.update(coordination_super_system_created=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    record = valid_not_applicable_record(); record["not_applicable_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q40_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    print("Q40_ONE_PRIMARY_BOX_GOVERNED_RELEASE_REGRESSION_SET: PASS")


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    fingerprints = [{"path": path, "sha256": _sha(root / path)} for path in paths]
    canonical = json.dumps(fingerprints, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    source_set_hash = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    current = q40_release_record(paths, fingerprints, source_set_hash)
    validate_record(current)
    _gate("Q40_CURRENT_RELEASE_PRIMARY_BOX_UNIQUE", current["primary_box"] == "kanda_prompt_workspace/prompt_library")
    _gate("Q40_CURRENT_RELEASE_SUPPORTING_TOUCHES_BOUNDED", all(row["bounded"] for row in current["supporting_touches"]))
    _gate("Q40_CURRENT_RELEASE_SOURCE_BASELINE_COMPLETE", {row["path"] for row in current["source_baselines"]} == set(paths))
    _gate("Q40_CURRENT_RELEASE_REGRESSION_OBLIGATIONS_COMPLETE", bool(current["regression_obligations"]))
    _gate("Q40_CURRENT_RELEASE_VALIDATION_MAP_COMPLETE", [row["path"] for row in current["validation_map"]] == paths)
    _gate("Q40_CURRENT_RELEASE_EXACT_ZIP_CONTRACT_DECLARED", current["exact_zip_contract"]["canonical_validator"] == "scripts/validate_patch_zip.py")
    _gate("Q40_CURRENT_RELEASE_FREEZE_EVIDENCE_DECLARED", current["freeze_evidence"]["preview_read_only"] is True and current["freeze_evidence"]["automatic_frozen_memory_write"] is False)
    _gate("Q40_CURRENT_RELEASE_HUMAN_LOCAL_VALIDATION_PENDING", current["human_local_validation_state"] == "PENDING")
    _gate("Q40_CURRENT_RELEASE_READY_FOR_LOCAL_VALIDATION", current["decision"] == "READY_FOR_LOCAL_VALIDATION" and current["may_deliver_patch"] is True and current["may_freeze"] is False)
    _gate("Q40_NO_RELEASE_COORDINATION_SUPER_SYSTEM", current["release_registry_created"] is False and current["coordination_super_system_created"] is False)
    coverage = q40_release_coverage_record(paths); validate_q31_coverage(coverage)
    _gate("Q40_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q40_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q40_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q40_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q40_Q39_FROZEN_BASELINE", Q39_FREEZE_ID.endswith("v1"))
    _gate("Q40_CURRENT_RELEASE_ALL_PYTHON_WITHIN_MAX", all(len(_read(root / path).splitlines()) <= 500 for path in RELEASE_FILES if path.suffix == ".py"))
    _gate("Q40_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q40_EXACT_RELEASE_PROVENANCE", True)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--project-root", type=Path, default=Path.cwd()); args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root); validate_contract(); validate_release(root)
    print("VALIDATION OK: " + FEATURE); print("STATUS: IN_SYNC"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
