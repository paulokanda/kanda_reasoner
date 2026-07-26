# project-path: tools/brick_wall_q40_one_primary_box_governed_release_contract.py
"""Validation-only Q40 one-primary-box governed-release contract."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import PurePosixPath
from typing import Any, Mapping

__all__: list[str] = []

DECISIONS = {"READY_FOR_LOCAL_VALIDATION", "VALIDATED_READY_FOR_FREEZE", "COMPLETE", "NOT_APPLICABLE", "BLOCKED"}
VALIDATION_STATES = {"PENDING", "COMPLETE", "FAILED"}
REQUIRED_FIELDS = {
    "release_applicable", "not_applicable_evidence", "q39_decision", "q39_frozen_baseline",
    "feature_id", "operation_id", "release_id", "primary_box", "supporting_touches",
    "changed_files", "source_baselines", "source_fingerprint_set_hash", "regression_obligations",
    "validation_map", "exact_zip_contract", "freeze_evidence", "human_local_validation_state",
    "durable_evidence_path", "generated_artifacts_authority", "transient_artifacts_authority",
    "project_freeze_memory_root", "project_freeze_ledger_used", "release_registry_created",
    "coordination_super_system_created", "limitations", "blockers", "decision",
    "may_deliver_patch", "may_claim_validation_passed", "may_freeze",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _safe_relative(path: str) -> bool:
    value = PurePosixPath(path)
    return bool(path) and not value.is_absolute() and ".." not in value.parts and "\\" not in path


def _hash_rows(rows: list[dict[str, str]]) -> str:
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


def valid_ready_record() -> dict[str, Any]:
    changed = ["docs/q40.md", "tools/q40_validator.py"]
    baselines = [{"path": path, "baseline_sha256": ("a" if index == 0 else "b") * 64, "payload_sha256": ("c" if index == 0 else "d") * 64} for index, path in enumerate(changed)]
    validation_map = [
        {"path": "docs/q40.md", "owner_box": "docs", "public_contract": "governed release record", "disposition": "APPLIES", "validators": ["tools/q40_validator.py"], "expected_markers": ["Q40_DOC: PASS"]},
        {"path": "tools/q40_validator.py", "owner_box": "tools", "public_contract": "focused Q40 validator", "disposition": "APPLIES", "validators": ["tools/q40_validator.py"], "expected_markers": ["Q40_VALIDATOR: PASS"]},
    ]
    return {
        "release_applicable": True,
        "not_applicable_evidence": [],
        "q39_decision": "NOT_APPLICABLE",
        "q39_frozen_baseline": "freeze-20260716-brick-wall-q39-task-specific-context-admission-test-v1",
        "feature_id": "brick-wall-q40-one-primary-box-governed-release-enforcement-v1",
        "operation_id": "q40-governed-release-fixture",
        "release_id": "q40-release-fixture-v1",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "supporting_touches": [
            {"path": "tools/q40_validator.py", "owner_box": "tools", "reason": "focused validation", "public_contract": "validator CLI", "bounded": True},
        ],
        "changed_files": changed,
        "source_baselines": baselines,
        "source_fingerprint_set_hash": _hash_rows([{"path": row["path"], "sha256": row["payload_sha256"]} for row in baselines]),
        "regression_obligations": [
            {"obligation_id": "one-primary-box", "source": "Q40", "disposition": "EXECUTABLE", "validator": "tools/q40_validator.py", "expected_marker": "Q40_PRIMARY_BOX: PASS"},
            {"obligation_id": "human-freeze", "source": "Q30", "disposition": "EXECUTABLE", "validator": "tools/q40_validator.py", "expected_marker": "Q40_HUMAN_FREEZE: PASS"},
        ],
        "validation_map": validation_map,
        "exact_zip_contract": {"patch_zip_name": "q40.zip", "canonical_validator": "scripts/validate_patch_zip.py", "root_member_count": 8, "root_freeze_hint_count": 1, "external_delivery_sha256_state": "PENDING", "payload_manifest_exact": True},
        "freeze_evidence": {"root_freeze_hint_count": 1, "evidence_path": "project_validation_evidence/q40.txt", "preview_read_only": True, "human_confirmation_required": True, "automatic_frozen_memory_write": False, "startup_refresh_required": True},
        "human_local_validation_state": "PENDING",
        "durable_evidence_path": "project_validation_evidence/q40.txt",
        "generated_artifacts_authority": "EVIDENCE_ONLY",
        "transient_artifacts_authority": "NON_AUTHORITATIVE",
        "project_freeze_memory_root": "<project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory",
        "project_freeze_ledger_used": False,
        "release_registry_created": False,
        "coordination_super_system_created": False,
        "limitations": ["Human-local validation and freeze confirmation remain pending."],
        "blockers": ["USER_LOCAL_VALIDATION_PENDING", "HUMAN_CONFIRMATION_PENDING"],
        "decision": "READY_FOR_LOCAL_VALIDATION",
        "may_deliver_patch": True,
        "may_claim_validation_passed": False,
        "may_freeze": False,
    }


def valid_complete_record() -> dict[str, Any]:
    record = valid_ready_record()
    record.update(
        human_local_validation_state="COMPLETE",
        decision="COMPLETE",
        may_claim_validation_passed=True,
        may_freeze=True,
        blockers=[],
        limitations=["Freeze still requires explicit human Confirm and Write."],
    )
    record["exact_zip_contract"]["external_delivery_sha256_state"] = "VERIFIED"
    return record


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_ready_record()
    record.update(
        release_applicable=False,
        not_applicable_evidence=["No installable or freezeable release is being produced.", "No source or generated deliverable is being changed."],
        supporting_touches=[], changed_files=[], source_baselines=[], source_fingerprint_set_hash="",
        regression_obligations=[], validation_map=[], human_local_validation_state="PENDING",
        decision="NOT_APPLICABLE", may_deliver_patch=False, may_claim_validation_passed=False, may_freeze=False,
        blockers=[], limitations=["Q40 is not applicable because no release exists."],
    )
    record["exact_zip_contract"] = {}
    record["freeze_evidence"] = {}
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def validate_record(record: Mapping[str, Any]) -> None:
    missing = REQUIRED_FIELDS - set(record)
    _assert(not missing, "missing Q40 fields: " + repr(sorted(missing)))
    _assert(record["decision"] in DECISIONS, "invalid Q40 decision")
    _assert(record["human_local_validation_state"] in VALIDATION_STATES, "invalid human-local validation state")
    _assert(record["q39_decision"] in {"ADMITTED", "REJECTED", "NOT_APPLICABLE"}, "Q39 decision incomplete")
    _assert(bool(record["q39_frozen_baseline"]), "Q39 frozen baseline required")
    _assert(bool(record["feature_id"]) and bool(record["operation_id"]) and bool(record["release_id"]), "release identities required")
    _assert(record["release_registry_created"] is False, "release registry forbidden")
    _assert(record["coordination_super_system_created"] is False, "coordination super-system forbidden")
    _assert(record["generated_artifacts_authority"] == "EVIDENCE_ONLY", "generated artifacts cannot be source authority")
    _assert(record["transient_artifacts_authority"] == "NON_AUTHORITATIVE", "transient artifacts cannot own durable truth")
    _assert(record["project_freeze_ledger_used"] is False, "project-specific freeze memory cannot use project_freeze_ledger")
    _assert(record["project_freeze_memory_root"].endswith("project_freeze_after_update/frozen_features_memory"), "project freeze-memory root invalid")
    _assert(_safe_relative(record["durable_evidence_path"]), "durable evidence path invalid")
    _assert(isinstance(record["limitations"], list) and record["limitations"], "limitations required")
    if not record["release_applicable"]:
        _assert(record["decision"] == "NOT_APPLICABLE", "N/A release requires NOT_APPLICABLE")
        _assert(isinstance(record["not_applicable_evidence"], list) and len(record["not_applicable_evidence"]) >= 2, "N/A evidence required")
        _assert(not record["changed_files"] and not record["source_baselines"] and not record["validation_map"], "N/A release cannot claim changed files")
        _assert(record["may_deliver_patch"] is False and record["may_claim_validation_passed"] is False and record["may_freeze"] is False, "N/A authorization mismatch")
        return
    _assert(isinstance(record["primary_box"], str) and bool(record["primary_box"].strip()), "exactly one primary box required")
    _assert(not isinstance(record["primary_box"], list), "primary box cannot be multiple")
    touches = record["supporting_touches"]
    _assert(isinstance(touches, list), "supporting touches must be a list")
    for row in touches:
        _assert(set(row) >= {"path", "owner_box", "reason", "public_contract", "bounded"}, "supporting touch incomplete")
        _assert(_safe_relative(str(row["path"])) and bool(row["owner_box"]) and bool(row["reason"]) and bool(row["public_contract"]) and row["bounded"] is True, "supporting touch unbounded")
    changed = record["changed_files"]
    _assert(isinstance(changed, list) and changed and len(changed) == len(set(changed)), "changed files must be unique and non-empty")
    _assert(all(_safe_relative(str(path)) for path in changed), "changed files must be safe relative paths")
    baselines = record["source_baselines"]
    _assert(isinstance(baselines, list) and {row.get("path") for row in baselines} == set(changed), "source baseline coverage mismatch")
    for row in baselines:
        _assert(len(row.get("baseline_sha256", "")) == 64 or row.get("baseline_sha256") == "NEW_FILE", "baseline hash invalid")
        _assert(len(row.get("payload_sha256", "")) == 64, "payload hash invalid")
    rows = [{"path": row["path"], "sha256": row["payload_sha256"]} for row in baselines]
    _assert(record["source_fingerprint_set_hash"] == _hash_rows(rows), "source fingerprint set hash mismatch")
    obligations = record["regression_obligations"]
    _assert(isinstance(obligations, list) and obligations, "regression obligations required")
    ids = [row.get("obligation_id") for row in obligations]
    _assert(all(ids) and len(ids) == len(set(ids)), "regression obligations must be unique")
    _assert(all(row.get("disposition") in {"EXECUTABLE", "NOT_APPLICABLE"} and row.get("validator") and row.get("expected_marker") for row in obligations), "regression obligation incomplete")
    validation_map = record["validation_map"]
    _assert(isinstance(validation_map, list) and len(validation_map) == len(changed), "validation map size mismatch")
    _assert([row.get("path") for row in validation_map] == changed, "validation map must follow exact changed-file order")
    for row in validation_map:
        _assert(row.get("owner_box") and row.get("public_contract"), "validation-map ownership incomplete")
        _assert(row.get("disposition") in {"APPLIES", "NOT_APPLICABLE"}, "validation-map disposition invalid")
        _assert(isinstance(row.get("validators"), list) and row["validators"], "validation-map validators required")
        _assert(isinstance(row.get("expected_markers"), list) and row["expected_markers"], "validation-map markers required")
    zip_contract = record["exact_zip_contract"]
    _assert(zip_contract.get("patch_zip_name", "").endswith(".zip"), "exact ZIP name required")
    _assert(zip_contract.get("canonical_validator") == "scripts/validate_patch_zip.py", "canonical ZIP validator required")
    _assert(zip_contract.get("root_member_count") == 8 and zip_contract.get("root_freeze_hint_count") == 1, "ZIP root contract invalid")
    _assert(zip_contract.get("payload_manifest_exact") is True, "payload/manifest exactness required")
    _assert(zip_contract.get("external_delivery_sha256_state") in {"PENDING", "VERIFIED"}, "external delivery SHA state invalid")
    freeze = record["freeze_evidence"]
    _assert(freeze.get("root_freeze_hint_count") == 1, "freeze hint count invalid")
    _assert(_safe_relative(freeze.get("evidence_path", "")), "freeze evidence path invalid")
    _assert(freeze.get("preview_read_only") is True and freeze.get("human_confirmation_required") is True, "human freeze protection required")
    _assert(freeze.get("automatic_frozen_memory_write") is False and freeze.get("startup_refresh_required") is True, "freeze workflow invalid")
    state = record["human_local_validation_state"]
    if state != "COMPLETE":
        _assert(record["may_claim_validation_passed"] is False and record["may_freeze"] is False, "pending validation cannot authorize claims or freeze")
    if record["decision"] == "READY_FOR_LOCAL_VALIDATION":
        _assert(state == "PENDING" and record["may_deliver_patch"] is True, "ready decision mismatch")
    if record["decision"] == "COMPLETE":
        _assert(state == "COMPLETE" and record["may_claim_validation_passed"] is True and record["may_freeze"] is True, "complete decision mismatch")


def q40_release_record(changed_files: list[str], fingerprints: list[dict[str, str]], source_set_hash: str) -> dict[str, Any]:
    record = valid_ready_record()
    record.update(
        feature_id="brick-wall-q40-one-primary-box-governed-release-enforcement-v1", operation_id="brick-wall-q40-one-primary-box-governed-release-enforcement-v1-package", release_id="kanda_brick_wall_q40_one_primary_box_governed_release_v1", primary_box="kanda_prompt_workspace/prompt_library",
        supporting_touches=[{"path": path, "owner_box": "validation-only supporting tools", "reason": "Q40 contract, provenance, or forward-compatible validation", "public_contract": "validator CLI and governed prompt contract", "bounded": True} for path in changed_files if path.startswith("tools/")],
        changed_files=list(changed_files),
        source_baselines=[{"path": row["path"], "baseline_sha256": "NEW_FILE" if "q40" in row["path"] else "0" * 64, "payload_sha256": row["sha256"]} for row in fingerprints],
        source_fingerprint_set_hash=source_set_hash,
        regression_obligations=[
            {"obligation_id": "q40-one-primary-box", "source": "Q40", "disposition": "EXECUTABLE", "validator": "tools/validate_brick_wall_q40_one_primary_box_governed_release_v1.py", "expected_marker": "Q40_CURRENT_RELEASE_PRIMARY_BOX_UNIQUE: PASS"},
            {"obligation_id": "q40-no-else-elseif", "source": "Error Memory", "disposition": "EXECUTABLE", "validator": "VALIDATE_PACKAGE.py", "expected_marker": "Q40_NO_USER_FACING_POWERSHELL_ELSE_OR_ELSEIF: PASS"},
            {"obligation_id": "q40-human-confirmed-freeze", "source": "Q30", "disposition": "EXECUTABLE", "validator": "tools/validate_brick_wall_q40_one_primary_box_governed_release_v1.py", "expected_marker": "Q40_CURRENT_RELEASE_FREEZE_EVIDENCE_DECLARED: PASS"},
        ],
        validation_map=[{"path": path, "owner_box": "kanda_prompt_workspace/prompt_library" if path.startswith("kanda_prompt_workspace/") else "validation-only supporting tools", "public_contract": "governed prompt metadata" if path.endswith((".md", ".json")) and path.startswith("kanda_prompt_workspace/") else "focused validator/provenance CLI", "disposition": "APPLIES", "validators": ["tools/validate_brick_wall_q40_one_primary_box_governed_release_v1.py"], "expected_markers": ["Q40_Q31_EXACT_CHANGED_FILE_COVERAGE: PASS"]} for path in changed_files],
        exact_zip_contract={"patch_zip_name": "kanda_brick_wall_q40_one_primary_box_governed_release_v1.zip", "canonical_validator": "scripts/validate_patch_zip.py", "root_member_count": 8, "root_freeze_hint_count": 1, "external_delivery_sha256_state": "PENDING", "payload_manifest_exact": True},
        freeze_evidence={"root_freeze_hint_count": 1, "evidence_path": "project_validation_evidence/brick-wall-q40-one-primary-box-governed-release-enforcement-v1.txt", "preview_read_only": True, "human_confirmation_required": True, "automatic_frozen_memory_write": False, "startup_refresh_required": True},
        durable_evidence_path="project_validation_evidence/brick-wall-q40-one-primary-box-governed-release-enforcement-v1.txt",
        limitations=["User-local Q19/Q30 real-Qt validation, durable evidence write, Preview, Confirm and Write, and startup refresh remain pending at package build time."],
        blockers=["USER_LOCAL_VALIDATION_PENDING", "HUMAN_CONFIRMATION_PENDING"],
    )
    return record


def q40_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    validators = [
        "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py",
        "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py",
        "tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py",
        "tools/validate_brick_wall_q35_focused_performance_baseline_v1.py",
        "tools/validate_brick_wall_q36_module_size_cohesion_v1.py",
        "tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py",
        "tools/validate_brick_wall_q38_handoff_freshness_provenance_v1.py",
        "tools/validate_brick_wall_q39_task_specific_context_admission_v1.py",
        "tools/validate_brick_wall_q40_one_primary_box_governed_release_v1.py",
    ]
    lessons = [
        "lesson-brick-wall-q03-validator-package-import-context-v1",
        "lesson-powershell-continuation-prompt-concatenated-scriptblock-v1",
        "lesson-powershell-required-line-array-collapse-v1",
    ]
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "owner_box": "validation-only supporting tools" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Brick Wall Q40 one-primary-box governed-release gate",
            "error_memory_lessons": lessons,
            "frozen_behavior": ["freeze-20260716-brick-wall-q39-task-specific-context-admission-test-v1"],
            "focused_tests": {
                "disposition": "APPLIES", "validators": validators,
                "expected_markers": ["Q40_ONE_PRIMARY_BOX_GOVERNED_RELEASE_REGRESSION_SET: PASS"],
                "reason": "Q32-Q39 forward compatibility and Q40 release behavior are checked.",
            },
            "boundary_tests": {
                "disposition": "APPLIES", "validators": [validators[-1]],
                "expected_markers": ["Q40_CURRENT_RELEASE_PRIMARY_BOX_UNIQUE: PASS"],
                "reason": "One primary box and bounded supporting touches are enforced.",
            },
            "gui_tests": {
                "disposition": "NOT_APPLICABLE", "validators": [], "expected_markers": [],
                "reason": "No GUI or Qt source is changed.",
            },
            "delivery_tests": {
                "disposition": "APPLIES", "validators": [validators[-1]],
                "expected_markers": ["Q40_CURRENT_RELEASE_EXACT_ZIP_CONTRACT_DECLARED: PASS"],
                "reason": "Exact payload, Q39 lineage, source baselines, ZIP, and freeze evidence are checked.",
            },
            "negative_tests": {
                "disposition": "APPLIES", "validators": [validators[-1]],
                "expected_markers": ["Q40_NEGATIVE_MULTIPLE_PRIMARY_BOXES: PASS"],
                "reason": "Multi-primary-box, unbounded touch, incomplete coverage, stale authority, and automatic freeze cases fail closed.",
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
