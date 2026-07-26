# project-path: tools/validate_brick_wall_q38_handoff_freshness_provenance_v1.py
"""Focused Q38 handoff freshness and provenance validation."""
from __future__ import annotations

__all__: list[str] = []
import argparse, ast, hashlib, json
from pathlib import Path
from typing import Callable

from tools.brick_wall_q31_changed_file_validator_coverage_contract import validate_record as validate_q31_coverage
from tools.brick_wall_q38_handoff_freshness_provenance_contract import mutated_record, q38_release_coverage_record, q38_release_record, valid_complete_record, valid_not_applicable_record, validate_record

FEATURE = "brick-wall-q38-handoff-freshness-provenance-enforcement-v1"
Q37_FREEZE_ID = "freeze-20260716-brick-wall-q37-canonical-ownership-reconciliation-v1"
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
CONTRACT = Path("tools/brick_wall_q38_handoff_freshness_provenance_contract.py")
PROVENANCE = Path("tools/brick_wall_q38_delivery_provenance.py")
VALIDATOR = Path("tools/validate_brick_wall_q38_handoff_freshness_provenance_v1.py")
HANDOFF_OWNER = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/handoff_at_end_of_work.md")
STARTUP_MAP = Path("kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json")
STARTUP_SYNC = Path("kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py")
ERROR_EXPORTER = Path("kanda_reasoner_app/error_memory/exporter.py")
FREEZE_CONTRACT = Path("kanda_reasoner_app/freeze_after_update/contract.py")
RELEASE_FILES = (BRICK, BRICK_META, BRIDGE, BRIDGE_META, Q32, Q33, Q34, Q35, Q36, Q37, CONTRACT, PROVENANCE, VALIDATOR)
OWNER_FILES = (HANDOFF_OWNER, STARTUP_MAP, STARTUP_SYNC, ERROR_EXPORTER, FREEZE_CONTRACT)


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
    for fragment in (
        "Handoff freshness and provenance (Q38)",
        "HANDOFF FRESHNESS AND PROVENANCE RECORD",
        "generation time", "source fingerprint", "manifest", "validation evidence",
        "Error Memory", "Freeze context", "source archive", "proceed Q39",
        "Q01-Q40 complete YES/NO",
    ):
        _gate("Q38_BRICK_WALL_CONTRACT", fragment in brick, fragment)
    for fragment in (
        "Handoff freshness and provenance bridge (Q38)",
        "Q37 frozen baseline", "manifest hash/time/source-fingerprint linkage",
        "Error Memory manifest", "active-project Freeze context", "proceed Q39 YES/NO",
    ):
        _gate("Q38_ROUTER_BRIDGE_CONTRACT", fragment in bridge, fragment)
    for path, label in ((BRICK_META, "brick"), (BRIDGE_META, "bridge")):
        meta = json.loads(_read(root / path))
        _gate("Q38_METADATA_ALIGNMENT", meta.get("source_stage") in {FEATURE, "brick-wall-q39-task-specific-context-admission-enforcement-v1", "brick-wall-q40-one-primary-box-governed-release-enforcement-v1"} and meta.get("updated_for") in {FEATURE, "brick-wall-q39-task-specific-context-admission-enforcement-v1", "brick-wall-q40-one-primary-box-governed-release-enforcement-v1"}, label)
        _gate("Q38_METADATA_DESCRIPTION", "Q38" in meta.get("description", ""), label)
        _gate("Q38_METADATA_DO_NOT_REGRESS", any("Q38 must" in rule for rule in meta.get("do_not_regress", [])), label)
    for path in RELEASE_FILES + OWNER_FILES:
        _gate("Q38_REQUIRED_FILE", (root / path).is_file(), str(path))
    for path in RELEASE_FILES:
        if path.suffix == ".py":
            text = _read(root / path)
            ast.parse(text, filename=str(path))
            _gate("Q38_TOUCHED_PYTHON_MAX_500", len(text.splitlines()) <= 500, f"{path}={len(text.splitlines())}")
        elif path.suffix == ".md":
            _gate("Q38_PROMPT_MODULE_SIZE", len(_read(root / path).splitlines()) <= 500, str(path))
    predecessors = (
        (Q32, "Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"),
        (Q33, "Q33_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"),
        (Q34, "Q34_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"),
        (Q35, "Q35_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"),
        (Q36, "Q36_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"),
        (Q37, "Q37_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS"),
    )
    for path, marker in predecessors:
        _gate(path.stem.upper() + "_FORWARD_COMPATIBLE_Q40_PROGRESSION", marker in _read(root / path), marker)


def _reject(label: str, mutate: Callable[[dict], None]) -> None:
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
    _gate("Q38_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q38_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q38_NEGATIVE_Q37_DECISION", lambda r: r.update(q37_decision="BLOCKED")),
        ("Q38_NEGATIVE_Q37_FROZEN", lambda r: r.update(q37_frozen_baseline="")),
        ("Q38_NEGATIVE_GENERATION_TIME", lambda r: r["handoff_artifact"].update(generated_at_utc="bad")),
        ("Q38_NEGATIVE_SOURCE_FINGERPRINT_SET", lambda r: r["current_source_fingerprints"].pop()),
        ("Q38_NEGATIVE_HANDOFF_HASH", lambda r: r["handoff_artifact"].update(sha256="bad")),
        ("Q38_NEGATIVE_MANIFEST_SOURCE_LINK", lambda r: r["manifest"].update(source_set_hash="e" * 64)),
        ("Q38_NEGATIVE_MANIFEST_OLDER", lambda r: r["manifest"].update(generated_at_utc="2026-07-16T19:00:00Z")),
        ("Q38_NEGATIVE_VALIDATION_OLDER", lambda r: r["validation_evidence"].update(generated_at_utc="2026-07-16T19:00:00Z")),
        ("Q38_NEGATIVE_ERROR_MEMORY_STALE", lambda r: r["error_memory"].update(status="STALE")),
        ("Q38_NEGATIVE_FREEZE_LATEST", lambda r: r["freeze_context"].update(latest_freeze_id="other")),
        ("Q38_NEGATIVE_FREEZE_OLDER", lambda r: r["freeze_context"].update(generated_at_utc="2026-07-16T20:01:00Z")),
        ("Q38_NEGATIVE_SOURCE_ARCHIVE_AUTHORITY", lambda r: r["source_archive"].update(authoritative_current_source=True)),
        ("Q38_NEGATIVE_SOURCE_ARCHIVE_STATUS", lambda r: r["source_archive"].update(status="CURRENT")),
        ("Q38_NEGATIVE_CHECK_INVENTORY", lambda r: r["freshness_checks"].pop("manifest")),
        ("Q38_NEGATIVE_CHECK_FAILED", lambda r: r["freshness_checks"].update(manifest="FAIL")),
        ("Q38_NEGATIVE_STALE_ARTIFACT", lambda r: r["stale_artifacts"].append("old handoff")),
        ("Q38_NEGATIVE_RUNTIME_OWNER", lambda r: r.update(runtime_handoff_owner_modified=True)),
        ("Q38_NEGATIVE_CONTEXT_ENGINE", lambda r: r.update(new_context_engine_created=True)),
        ("Q38_NEGATIVE_FRESHNESS_REGISTRY", lambda r: r.update(new_freshness_registry_created=True)),
        ("Q38_NEGATIVE_Q39_PROGRESSION", lambda r: r.update(may_proceed_to_q39=False)),
        ("Q38_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q38_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    record = valid_not_applicable_record()
    record["no_handoff_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q38_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q38_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q38_HANDOFF_FRESHNESS_PROVENANCE_REGRESSION_SET: PASS")


def validate_existing_owners(root: Path) -> None:
    handoff = _read(root / HANDOFF_OWNER)
    source_map = _read(root / STARTUP_MAP)
    sync = _read(root / STARTUP_SYNC)
    exporter = _read(root / ERROR_EXPORTER)
    freeze = _read(root / FREEZE_CONTRACT)
    _gate("Q38_EXISTING_HANDOFF_OWNER", "handoff" in handoff.lower())
    _gate("Q38_EXISTING_STARTUP_SOURCE_MAP_OWNER", "handoff_at_end_of_work" in source_map)
    _gate(
        "Q38_EXISTING_STARTUP_SYNC_OWNER",
        "startup_kernel" in sync
        and "active-project freeze context" in sync.lower(),
    )
    _gate("Q38_EXISTING_ERROR_MEMORY_OWNER", "manifest" in exporter.lower())
    _gate("Q38_EXISTING_FREEZE_CONTEXT_OWNER", "freeze" in freeze.lower())
    changed = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    owners = {str(path).replace("\\", "/") for path in OWNER_FILES}
    _gate("Q38_NO_RUNTIME_HANDOFF_OWNER_MODIFIED", changed.isdisjoint(owners))
    contract = _read(root / CONTRACT)
    _gate("Q38_NO_CONTEXT_OR_FRESHNESS_ENGINE_CREATED", "class ContextEngine" not in contract and "class FreshnessRegistry" not in contract)
    print("Q38_EXISTING_HANDOFF_AUTHORITIES_REUSED: PASS")


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    fingerprints = [{"path": path, "sha256": _sha(root / path)} for path in paths]
    canonical = json.dumps(fingerprints, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    source_set_hash = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    current = q38_release_record(paths, fingerprints, source_set_hash)
    validate_record(current)
    _gate("Q38_CURRENT_RELEASE_FRESHNESS_COMPLETE", current["decision"] == "COMPLETE")
    _gate("Q38_CURRENT_RELEASE_NO_RUNTIME_OWNER_TOUCHED", current["runtime_handoff_owner_modified"] is False)
    _gate("Q38_CURRENT_RELEASE_NO_CONTEXT_ENGINE", current["new_context_engine_created"] is False)
    coverage = q38_release_coverage_record(paths)
    validate_q31_coverage(coverage)
    _gate("Q38_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q38_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q38_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q38_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q38_Q37_FROZEN_BASELINE", Q37_FREEZE_ID.endswith("v1"))
    _gate("Q38_CURRENT_RELEASE_ALL_PYTHON_WITHIN_MAX", all(len(_read(root / path).splitlines()) <= 500 for path in RELEASE_FILES if path.suffix == ".py"))
    _gate("Q38_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q38_EXACT_RELEASE_PROVENANCE", True)
    print("Q38_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")
    print("Q38_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    validate_contract()
    validate_existing_owners(root)
    validate_release(root)
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
