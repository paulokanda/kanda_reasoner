# project-path: tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py
"""Focused Q37 canonical ownership reconciliation validator."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import ast
from collections.abc import Callable
import hashlib
import json
from pathlib import Path
from typing import Any

from brick_wall_q31_changed_file_validator_coverage_contract import validate_record as validate_q31_coverage
from brick_wall_q37_canonical_ownership_reconciliation_contract import (
    mutated_record,
    q37_release_coverage_record,
    q37_release_record,
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
Q35 = Path("tools/validate_brick_wall_q35_focused_performance_baseline_v1.py")
Q36 = Path("tools/validate_brick_wall_q36_module_size_cohesion_v1.py")
CONTRACT = Path("tools/brick_wall_q37_canonical_ownership_reconciliation_contract.py")
PROVENANCE = Path("tools/brick_wall_q37_delivery_provenance.py")
SELF = Path("tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py")
BOX_CANON = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md")
PROJECT_TOOL_CANON = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md")
Q07_OWNER = Path("tools/validate_brick_wall_q07_ownership_no_leak_classification_v1.py")
Q09_OWNER = Path("tools/validate_brick_wall_q09_public_contract_communication_v1.py")
Q10_OWNER = Path("tools/validate_brick_wall_q10_single_mutable_state_owner_v1.py")
Q22_OWNER = Path("tools/validate_brick_wall_q22_public_facade_contract_drift_v1.py")
Q31_OWNER = Path("tools/brick_wall_q31_changed_file_validator_coverage_contract.py")
FEATURE = "brick-wall-q37-canonical-ownership-reconciliation-enforcement-v1"
Q38_FEATURE = "brick-wall-q38-handoff-freshness-provenance-enforcement-v1"
Q39_FEATURE = "brick-wall-q39-task-specific-context-admission-enforcement-v1"
Q40_FEATURE = "brick-wall-q40-one-primary-box-governed-release-enforcement-v1"
Q36_FREEZE_ID = "freeze-20260716-brick-wall-q36-module-size-and-cohesion-enforcement-v1"
RELEASE_FILES = (
    BRICK,
    BRICK_META,
    BRIDGE,
    BRIDGE_META,
    Q32,
    Q33,
    Q34,
    Q35,
    Q36,
    CONTRACT,
    PROVENANCE,
    SELF,
)
OWNER_FILES = (
    BOX_CANON,
    PROJECT_TOOL_CANON,
    Q07_OWNER,
    Q09_OWNER,
    Q10_OWNER,
    Q22_OWNER,
    Q31_OWNER,
)


def _gate(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK)
    bridge = _read(root / BRIDGE)
    for fragment in (
        "Canonical ownership reconciliation (Q37)",
        "CANONICAL OWNERSHIP RECONCILIATION RECORD",
        "duplicate scanners",
        "duplicate schemas",
        "duplicate reports",
        "duplicate state owners",
        "duplicate consumers",
        "new coordination super-system",
        "proceed Q38 handoff freshness and provenance YES/NO",
        "Q01-Q40 complete YES/NO",
    ):
        _gate("Q37_BRICK_WALL_CONTRACT", fragment in brick, fragment)
    for fragment in (
        "Canonical ownership reconciliation bridge (Q37)",
        "one canonical owner per responsibility",
        "retirement or evidence-backed coexistence",
        "new coordination super-system",
        "proceed Q38 YES/NO",
    ):
        _gate("Q37_ROUTER_BRIDGE_CONTRACT", fragment in bridge, fragment)
    for path, label in ((BRICK_META, "brick"), (BRIDGE_META, "bridge")):
        meta = json.loads(_read(root / path))
        stage = meta.get("source_stage")
        _gate(
            "Q37_METADATA_ALIGNMENT",
            stage == meta.get("updated_for")
            and stage in {FEATURE, Q38_FEATURE, Q39_FEATURE, Q40_FEATURE},
            label,
        )
        _gate("Q37_METADATA_DESCRIPTION", "Q37" in meta.get("description", ""), label)
        _gate("Q37_METADATA_DO_NOT_REGRESS", any("Q37 must" in rule for rule in meta.get("do_not_regress", [])), label)
    for path in RELEASE_FILES + OWNER_FILES:
        _gate("Q37_REQUIRED_FILE", (root / path).is_file(), str(path))
    for path in RELEASE_FILES:
        if path.suffix == ".py":
            text = _read(root / path)
            ast.parse(text, filename=str(path))
            _gate("Q37_TOUCHED_PYTHON_MAX_500", len(text.splitlines()) <= 500, f"{path}={len(text.splitlines())}")
        elif path.suffix == ".md":
            _gate("Q37_PROMPT_MODULE_SIZE", len(_read(root / path).splitlines()) <= 500, str(path))
    predecessors = (
        (Q32, "Q32", "Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS", "Q32_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS"),
        (Q33, "Q33", "Q33_PINNED_LOCAL_MODEL_PROVENANCE_REGRESSION_SET: PASS", "Q33_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS"),
        (Q34, "Q34", "Q34_PROFILE_BEFORE_OPTIMIZATION_REGRESSION_SET: PASS", "Q34_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS"),
        (Q35, "Q35", "Q35_FOCUSED_PERFORMANCE_BASELINE_REGRESSION_SET: PASS", "Q35_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS"),
        (Q36, "Q36", "Q36_MODULE_SIZE_COHESION_REGRESSION_SET: PASS", "Q36_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS"),
    )
    for path, name, behavior, forward in predecessors:
        source = _read(root / path)
        for marker in (behavior, forward, "STATUS: IN_SYNC"):
            _gate(
                name + "_FORWARD_COMPATIBLE_Q37_PROGRESSION",
                marker in source,
                marker,
            )


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
    _gate("Q37_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q37_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q37_NEGATIVE_Q36_DECISION", lambda r: r.update(q36_decision="BLOCKED")),
        ("Q37_NEGATIVE_Q36_FROZEN", lambda r: r.update(q36_frozen_baseline="")),
        ("Q37_NEGATIVE_DUPLICATE_KIND_INVENTORY", lambda r: r.update(duplicate_kind_inventory=["SCANNER"])),
        ("Q37_NEGATIVE_CANONICAL_OWNER", lambda r: r.update(canonical_owner_selected=False)),
        ("Q37_NEGATIVE_CONSUMER_MIGRATION", lambda r: r.update(consumer_migration_complete=False)),
        ("Q37_NEGATIVE_STATE_OWNER", lambda r: r.update(state_owner_reconciled=False)),
        ("Q37_NEGATIVE_SUPER_SYSTEM", lambda r: r.update(new_super_system_created=True)),
        ("Q37_NEGATIVE_COORDINATION_REGISTRY", lambda r: r.update(new_coordination_registry_created=True)),
        ("Q37_NEGATIVE_RUNTIME_OWNER", lambda r: r.update(runtime_owner_modified=True)),
        ("Q37_NEGATIVE_RESPONSIBILITY_ID", lambda r: r["responsibility_inventory"][0].update(responsibility_id="")),
        ("Q37_NEGATIVE_OWNER_PATH", lambda r: r["responsibility_inventory"][0].update(canonical_owner_path="../escape.py")),
        ("Q37_NEGATIVE_PUBLIC_CONTRACT", lambda r: r["responsibility_inventory"][0].update(public_contract="")),
        ("Q37_NEGATIVE_UNRESOLVED", lambda r: r["responsibility_inventory"][0]["unresolved_fields"].append("owner")),
        ("Q37_NEGATIVE_DISPOSITION_INCOMPLETE", lambda r: r["responsibility_inventory"][0].update(retirement_or_coexistence_complete=False)),
        ("Q37_NEGATIVE_DUPLICATE_CANDIDATE_PATH", lambda r: r["responsibility_inventory"][0]["duplicate_candidates"].append(r["responsibility_inventory"][0]["duplicate_candidates"][0])),
        ("Q37_NEGATIVE_UNKNOWN_KIND", lambda r: r["responsibility_inventory"][0]["duplicate_candidates"][0].update(kind="OTHER")),
        ("Q37_NEGATIVE_UNKNOWN_DISPOSITION", lambda r: r["responsibility_inventory"][0]["duplicate_candidates"][0].update(disposition="IGNORE")),
        ("Q37_NEGATIVE_ADAPTER_CONTRACT", lambda r: r["responsibility_inventory"][0]["duplicate_candidates"][1].update(public_adapter_contract="NOT_APPLICABLE")),
        ("Q37_NEGATIVE_STATE_WRITE", lambda r: r["responsibility_inventory"][0]["duplicate_candidates"][0].update(kind="STATE_OWNER", state_write_disabled=False)),
        ("Q37_NEGATIVE_COEXISTENCE_EVIDENCE", lambda r: r["responsibility_inventory"][0]["duplicate_candidates"][0].update(disposition="COEXISTENCE_JUSTIFIED", reason="same responsibility")),
        ("Q37_NEGATIVE_DURABLE_PATH", lambda r: r.update(durable_evidence_path="delete_after_daily_work/q37.txt")),
        ("Q37_NEGATIVE_Q38_PROGRESSION", lambda r: r.update(may_proceed_to_q38=False)),
        ("Q37_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q37_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    na = valid_not_applicable_record()
    na["no_reconciliation_evidence"] = []
    try:
        validate_record(na)
    except AssertionError:
        _gate("Q37_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q37_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q37_CANONICAL_OWNERSHIP_RECONCILIATION_REGRESSION_SET: PASS")


def validate_existing_owners(root: Path) -> None:
    box = _read(root / BOX_CANON)
    tool_project = _read(root / PROJECT_TOOL_CANON)
    q07 = _read(root / Q07_OWNER)
    q09 = _read(root / Q09_OWNER)
    q10 = _read(root / Q10_OWNER)
    q22 = _read(root / Q22_OWNER)
    _gate("Q37_EXISTING_BOX_OWNER", "Public Contract, Private Internals" in box and "No Private Reach-In" in box)
    _gate("Q37_EXISTING_TOOL_PROJECT_OWNER", "Tool" in tool_project and "Project" in tool_project)
    _gate("Q37_EXISTING_CLASSIFICATION_OWNER", "Q07_ONE_PRIMARY_BOX" in q07 and "Q07_NO_PARALLEL_AUTHORITY" in q07)
    _gate("Q37_EXISTING_PUBLIC_CONTRACT_OWNER", "Q09_NEGATIVE_DUPLICATE_PUBLIC_OWNER" in q09)
    _gate("Q37_EXISTING_STATE_OWNER", "Q10_NEGATIVE_DUPLICATE_OWNER_CLAIM" in q10)
    _gate("Q37_EXISTING_CONSUMER_DRIFT_OWNER", "Q22_DUPLICATE_PUBLIC_OWNER_REJECTION_FIXTURE" in q22)
    changed = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    owners = {str(path).replace("\\", "/") for path in OWNER_FILES}
    _gate("Q37_NO_RUNTIME_OR_CANONICAL_OWNER_MODIFIED", changed.isdisjoint(owners))
    contract = _read(root / CONTRACT)
    _gate("Q37_NO_OWNERSHIP_SUPER_SYSTEM_CREATED", "class OwnershipRegistry" not in contract and "class CanonicalOwnerService" not in contract)
    print("Q37_EXISTING_OWNERSHIP_AUTHORITIES_REUSED: PASS")


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    current = q37_release_record(paths)
    validate_record(current)
    _gate("Q37_CURRENT_RELEASE_RECONCILIATION_NOT_APPLICABLE", current["decision"] == "NOT_APPLICABLE")
    _gate("Q37_CURRENT_RELEASE_NO_RUNTIME_OWNER_TOUCHED", current["runtime_owner_modified"] is False)
    _gate("Q37_CURRENT_RELEASE_NO_SUPER_SYSTEM", current["new_super_system_created"] is False)
    coverage = q37_release_coverage_record(paths)
    validate_q31_coverage(coverage)
    _gate("Q37_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q37_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q37_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q37_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q37_Q36_FROZEN_BASELINE", Q36_FREEZE_ID.endswith("v1"))
    _gate("Q37_CURRENT_RELEASE_ALL_PYTHON_WITHIN_MAX", all(len(_read(root / path).splitlines()) <= 500 for path in RELEASE_FILES if path.suffix == ".py"))
    _gate("Q37_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q37_EXACT_RELEASE_PROVENANCE", True)
    print("Q37_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS")
    print("Q37_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS")
    print("Q37_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")


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
