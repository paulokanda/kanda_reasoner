# project-path: tools/brick_wall_q38_handoff_freshness_provenance_contract.py
"""Validation-only Q38 handoff freshness and provenance contract."""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import PurePosixPath
from typing import Any, Mapping

__all__: list[str] = []

REQUIRED_FIELDS = {
    "freshness_required", "no_handoff_evidence", "q37_decision",
    "q37_frozen_baseline", "feature_id", "operation_id", "primary_box",
    "changed_files", "current_source_fingerprints", "handoff_artifact",
    "manifest", "validation_evidence", "error_memory", "freeze_context",
    "source_archive", "freshness_checks", "stale_artifacts",
    "runtime_handoff_owner_modified", "new_context_engine_created",
    "new_freshness_registry_created", "validators", "expected_markers",
    "durable_evidence_path", "limitations", "blockers", "decision",
    "may_proceed_to_q39", "may_begin_coding", "may_write_source",
}
FRESHNESS_KEYS = {
    "generation_time", "source_fingerprint", "manifest", "validation",
    "error_memory", "freeze_context", "source_archive",
}
ARTIFACT_FIELDS = {"path", "sha256", "generated_at_utc", "source_set_hash", "status"}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _safe_relative(path: str) -> bool:
    candidate = PurePosixPath(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts and "\\" not in path


def _utc(value: str) -> datetime:
    _assert(isinstance(value, str) and value.endswith("Z"), "timestamp must be UTC Z form")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise AssertionError("invalid timestamp") from exc
    _assert(parsed.tzinfo is not None, "timestamp must carry timezone")
    return parsed.astimezone(timezone.utc)


def _artifact(path: str, generated: str, source_set_hash: str, status: str = "CURRENT") -> dict[str, Any]:
    return {
        "path": path,
        "sha256": "a" * 64,
        "generated_at_utc": generated,
        "source_set_hash": source_set_hash,
        "status": status,
    }


def valid_complete_record() -> dict[str, Any]:
    source_set_hash = "b" * 64
    generated = "2026-07-16T20:00:00Z"
    validation = "2026-07-16T20:05:00Z"
    freeze = "2026-07-16T20:10:00Z"
    return {
        "freshness_required": True,
        "no_handoff_evidence": [],
        "q37_decision": "COMPLETE",
        "q37_frozen_baseline": "freeze-20260716-brick-wall-q37-canonical-ownership-reconciliation-v1",
        "feature_id": "brick-wall-q38-handoff-freshness-provenance-enforcement-v1",
        "operation_id": "q38-handoff-freshness-fixture",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": ["docs/q38.md", "tools/q38_fixture.py"],
        "current_source_fingerprints": [
            {"path": "docs/q38.md", "sha256": "c" * 64},
            {"path": "tools/q38_fixture.py", "sha256": "d" * 64},
        ],
        "handoff_artifact": _artifact("project_freeze_after_update/frozen_features_memory/entries/q37.md", generated, source_set_hash),
        "manifest": _artifact("second_prompt_files/bundle_manifest.json", generated, source_set_hash),
        "validation_evidence": _artifact("project_validation_evidence/q37.txt", validation, source_set_hash),
        "error_memory": _artifact("error_memory/error_memory_manifest.json", validation, source_set_hash),
        "freeze_context": {
            **_artifact("first_prompt_files/09_active_project_freeze_context.md", freeze, source_set_hash),
            "latest_freeze_id": "freeze-20260716-brick-wall-q37-canonical-ownership-reconciliation-v1",
        },
        "source_archive": {
            **_artifact("second_prompt_files/source_archive_manifest.json", generated, source_set_hash, "GENERATED_EVIDENCE_ONLY"),
            "authoritative_current_source": False,
        },
        "freshness_checks": {key: "PASS" for key in sorted(FRESHNESS_KEYS)},
        "stale_artifacts": [],
        "runtime_handoff_owner_modified": False,
        "new_context_engine_created": False,
        "new_freshness_registry_created": False,
        "validators": ["tools/validate_brick_wall_q38_handoff_freshness_provenance_v1.py"],
        "expected_markers": ["Q38_HANDOFF_FRESHNESS_PROVENANCE_REGRESSION_SET: PASS"],
        "durable_evidence_path": "project_validation_evidence/q38.txt",
        "limitations": ["Generated handoff and archives remain evidence only; exact current source remains authoritative."],
        "blockers": [],
        "decision": "COMPLETE",
        "may_proceed_to_q39": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update(
        freshness_required=False,
        no_handoff_evidence=[
            "No handoff, source archive, manifest, validation, Error Memory, or Freeze-context artifact is consumed or produced by this task.",
            "The task is non-governed and cannot use generated artifacts as current-source authority.",
        ],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def validate_record(record: Mapping[str, Any]) -> None:
    missing = REQUIRED_FIELDS - set(record)
    _assert(not missing, "missing Q38 fields: " + repr(sorted(missing)))
    required = record["freshness_required"]
    _assert(isinstance(required, bool), "freshness_required must be bool")
    _assert(record["q37_decision"] in {"COMPLETE", "NOT_APPLICABLE"}, "Q37 decision must be complete")
    _assert(bool(record["q37_frozen_baseline"]), "Q37 frozen baseline is required")
    _assert(bool(record["feature_id"]) and bool(record["operation_id"]), "feature and operation IDs are required")
    _assert(bool(record["primary_box"]), "primary box is required")
    changed = record["changed_files"]
    _assert(isinstance(changed, list) and changed and len(changed) == len(set(changed)), "changed files must be unique")
    _assert(all(_safe_relative(str(path)) for path in changed), "changed files must be safe relative paths")
    fingerprints = record["current_source_fingerprints"]
    _assert(isinstance(fingerprints, list) and fingerprints, "source fingerprints are required")
    _assert({row["path"] for row in fingerprints} == set(changed), "source fingerprint set must match changed files")
    _assert(all(len(row["sha256"]) == 64 for row in fingerprints), "source hashes must be sha256")
    for name in ("handoff_artifact", "manifest", "validation_evidence", "error_memory"):
        artifact = record[name]
        _assert(ARTIFACT_FIELDS <= set(artifact), name + " fields incomplete")
        _assert(_safe_relative(artifact["path"]), name + " path invalid")
        _assert(len(artifact["sha256"]) == 64, name + " hash invalid")
        _utc(artifact["generated_at_utc"])
        _assert(len(artifact["source_set_hash"]) == 64, name + " source set hash invalid")
        _assert(artifact["status"] == "CURRENT", name + " must be current")
    freeze = record["freeze_context"]
    _assert(ARTIFACT_FIELDS <= set(freeze), "freeze context fields incomplete")
    _assert(bool(freeze.get("latest_freeze_id")), "latest freeze ID is required")
    _assert(freeze["latest_freeze_id"] == record["q37_frozen_baseline"], "freeze context must expose Q37 as latest")
    _assert(freeze["status"] == "CURRENT", "freeze context must be current")
    archive = record["source_archive"]
    _assert(ARTIFACT_FIELDS <= set(archive), "source archive fields incomplete")
    _assert(archive.get("authoritative_current_source") is False, "source archive cannot be current-source authority")
    _assert(archive["status"] == "GENERATED_EVIDENCE_ONLY", "source archive authority classification invalid")
    source_set = record["handoff_artifact"]["source_set_hash"]
    for name in ("manifest", "validation_evidence", "error_memory", "freeze_context", "source_archive"):
        _assert(record[name]["source_set_hash"] == source_set, name + " source linkage mismatch")
    handoff_time = _utc(record["handoff_artifact"]["generated_at_utc"])
    _assert(_utc(record["manifest"]["generated_at_utc"]) >= handoff_time, "manifest older than handoff")
    _assert(_utc(record["validation_evidence"]["generated_at_utc"]) >= handoff_time, "validation older than handoff")
    _assert(_utc(record["error_memory"]["generated_at_utc"]) >= handoff_time, "Error Memory older than handoff")
    _assert(_utc(freeze["generated_at_utc"]) >= _utc(record["validation_evidence"]["generated_at_utc"]), "Freeze context older than validation")
    checks = record["freshness_checks"]
    _assert(set(checks) == FRESHNESS_KEYS, "freshness-check inventory mismatch")
    _assert(all(value == "PASS" for value in checks.values()), "all freshness checks must pass")
    _assert(not record["stale_artifacts"], "stale artifacts must be invalidated or regenerated")
    _assert(record["runtime_handoff_owner_modified"] is False, "governance-only Q38 may not modify runtime handoff owner")
    _assert(record["new_context_engine_created"] is False, "new context engine is forbidden")
    _assert(record["new_freshness_registry_created"] is False, "new freshness registry is forbidden")
    _assert(record["validators"] and record["expected_markers"], "validators and markers are required")
    _assert(_safe_relative(record["durable_evidence_path"]), "durable evidence path invalid")
    _assert(record["limitations"], "limitations are required")
    _assert(not record["blockers"], "blockers remain")
    if required:
        _assert(record["decision"] == "COMPLETE", "required Q38 decision must be complete")
    else:
        _assert(record["decision"] == "NOT_APPLICABLE", "N/A decision mismatch")
        _assert(len(record["no_handoff_evidence"]) >= 2, "N/A evidence is incomplete")
    _assert(record["may_proceed_to_q39"] is True, "Q39 progression must be explicit")
    _assert(record["may_begin_coding"] is False, "Q38 cannot authorize coding")
    _assert(record["may_write_source"] is False, "Q38 cannot authorize source writes")


def q38_release_record(changed_files: list[str], source_fingerprints: list[dict[str, str]], source_set_hash: str) -> dict[str, Any]:
    record = valid_complete_record()
    record.update(
        operation_id="brick-wall-q38-handoff-freshness-provenance-enforcement-v1-local-release",
        changed_files=list(changed_files),
        current_source_fingerprints=deepcopy(source_fingerprints),
    )
    for key in ("handoff_artifact", "manifest", "validation_evidence", "error_memory", "freeze_context", "source_archive"):
        record[key]["source_set_hash"] = source_set_hash
    return record


def q38_release_coverage_record(changed_files: list[str]) -> dict[str, Any]:
    validators = [
        "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py",
        "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py",
        "tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py",
        "tools/validate_brick_wall_q35_focused_performance_baseline_v1.py",
        "tools/validate_brick_wall_q36_module_size_cohesion_v1.py",
        "tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py",
        "tools/validate_brick_wall_q38_handoff_freshness_provenance_v1.py",
    ]
    lessons = [
        "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
        "lesson-brick-wall-q03-validator-package-import-context-v1",
        "lesson-powershell-captured-lines-nested-array-marker-gate-v1",
        "lesson-powershell-required-line-array-collapse-v1",
    ]
    rows = []
    for path in changed_files:
        rows.append({
            "path": path,
            "owner_box": (
                "tools validation-only support"
                if path.startswith("tools/")
                else "kanda_prompt_workspace/prompt_library"
            ),
            "public_contract": "Brick Wall Q38 handoff freshness and provenance gate",
            "error_memory_lessons": lessons,
            "frozen_behavior": [
                "freeze-20260716-brick-wall-q37-canonical-ownership-reconciliation-v1"
            ],
            "focused_tests": {
                "disposition": "APPLIES",
                "validators": validators,
                "expected_markers": [
                    "Q38_HANDOFF_FRESHNESS_PROVENANCE_REGRESSION_SET: PASS"
                ],
                "reason": "Q32-Q37 forward compatibility and Q38 freshness behavior are checked.",
            },
            "boundary_tests": {
                "disposition": "APPLIES",
                "validators": [validators[-1]],
                "expected_markers": [
                    "Q38_EXISTING_HANDOFF_AUTHORITIES_REUSED: PASS"
                ],
                "reason": "Existing handoff, startup, Error Memory, and Freeze-context owners remain canonical.",
            },
            "gui_tests": {
                "disposition": "NOT_APPLICABLE",
                "validators": [],
                "expected_markers": [],
                "reason": "No GUI or Qt behavior is changed.",
            },
            "delivery_tests": {
                "disposition": "APPLIES",
                "validators": [validators[-1]],
                "expected_markers": ["Q38_EXACT_RELEASE_PROVENANCE: PASS"],
                "reason": "Exact payload, Q37 lineage, import context, source fingerprints, and durable evidence are checked.",
            },
            "negative_tests": {
                "disposition": "APPLIES",
                "validators": [validators[-1]],
                "expected_markers": ["Q38_NEGATIVE_STALE_ARTIFACT: PASS"],
                "reason": "Stale manifests, evidence, Error Memory, Freeze context, and generated-source authority fail closed.",
            },
        })
    return {
        "coverage_required": True,
        "no_coverage_evidence": [],
        "q30_decision_complete": True,
        "q30_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": list(changed_files),
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
