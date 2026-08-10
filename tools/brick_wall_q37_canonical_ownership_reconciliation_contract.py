# project-path: tools/brick_wall_q37_canonical_ownership_reconciliation_contract.py
"""Validation-only Q37 canonical ownership reconciliation contract."""
from __future__ import annotations

from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Mapping

__all__: list[str] = []

DUPLICATE_KINDS = {
    "SCANNER",
    "SCHEMA",
    "REPORT",
    "STATE_OWNER",
    "CONSUMER",
}
DISPOSITIONS = {
    "RETIRED",
    "PUBLIC_ADAPTER",
    "COEXISTENCE_JUSTIFIED",
    "NOT_DUPLICATE",
}
GENERALIZATION_SEQUENCE = (
    "RECONCILE",
    "REPAIR",
    "VALIDATE",
    "SHIELD",
    "FREEZE",
    "EXTRACT",
    "ADOPT",
)
SHIELD_DECISIONS = {
    "COMPLETE",
    "STRENGTHEN_EXISTING",
    "NOT_APPLICABLE",
}
ADOPTION_SCOPE = "BOUNDED_ONE_CONSUMER_AT_A_TIME"
REQUIRED_FIELDS = {
    "reconciliation_required",
    "no_reconciliation_evidence",
    "q36_decision",
    "q36_frozen_baseline",
    "feature_id",
    "operation_id",
    "primary_box",
    "changed_files",
    "responsibility_inventory",
    "duplicate_kind_inventory",
    "canonical_owner_selected",
    "consumer_migration_complete",
    "state_owner_reconciled",
    "new_super_system_created",
    "new_coordination_registry_created",
    "runtime_owner_modified",
    "reusable_contract_extraction_proposed",
    "no_extraction_evidence",
    "strategy_sequence",
    "repair_validated_before_extraction",
    "shield_decision",
    "freeze_baseline_before_extraction",
    "extraction_owner_path",
    "new_owner_created",
    "new_owner_gap_proven",
    "adoption_scope",
    "extraction_blockers",
    "validators",
    "expected_markers",
    "durable_evidence_path",
    "limitations",
    "blockers",
    "decision",
    "may_proceed_to_q38",
    "may_begin_coding",
    "may_write_source",
}
RESPONSIBILITY_FIELDS = {
    "responsibility_id",
    "responsibility",
    "canonical_owner_box",
    "canonical_owner_path",
    "public_contract",
    "source_of_truth",
    "state_mutation_owner",
    "current_consumers",
    "duplicate_candidates",
    "retirement_or_coexistence_complete",
    "consumer_migration_complete",
    "validators",
    "expected_markers",
    "unresolved_fields",
}
CANDIDATE_FIELDS = {
    "path",
    "kind",
    "claimed_responsibility",
    "disposition",
    "reason",
    "public_adapter_contract",
    "migration_target",
    "state_write_disabled",
    "consumer_migration_complete",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _safe_relative(path: str) -> bool:
    candidate = PurePosixPath(path)
    return (
        bool(path)
        and not candidate.is_absolute()
        and ".." not in candidate.parts
        and "\\" not in path
    )


def _candidate(path: str, kind: str, disposition: str) -> dict[str, Any]:
    adapter = disposition == "PUBLIC_ADAPTER"
    migration = disposition in {"RETIRED", "PUBLIC_ADAPTER"}
    return {
        "path": path,
        "kind": kind,
        "claimed_responsibility": "project ownership inventory",
        "disposition": disposition,
        "reason": "Canonical owner retained; competitor is removed or bounded through the public contract.",
        "public_adapter_contract": "canonical_owner.public_contract" if adapter else "NOT_APPLICABLE",
        "migration_target": "kanda_prompt_workspace/prompt_library" if migration else "NOT_APPLICABLE",
        "state_write_disabled": kind != "STATE_OWNER" or disposition != "COEXISTENCE_JUSTIFIED",
        "consumer_migration_complete": disposition != "COEXISTENCE_JUSTIFIED",
    }


def _responsibility() -> dict[str, Any]:
    return {
        "responsibility_id": "canonical-prompt-governance-owner",
        "responsibility": "Own the Brick Wall governance contract and routed implementation bridge.",
        "canonical_owner_box": "kanda_prompt_workspace/prompt_library",
        "canonical_owner_path": "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md",
        "public_contract": "Prompt-library routed governance contract",
        "source_of_truth": "canonical prompt-library source",
        "state_mutation_owner": "NONE_VALIDATION_ONLY",
        "current_consumers": [
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md",
        ],
        "duplicate_candidates": [
            _candidate("legacy/duplicate_owner.py", "SCANNER", "RETIRED"),
            _candidate("legacy/compatibility_facade.py", "CONSUMER", "PUBLIC_ADAPTER"),
        ],
        "retirement_or_coexistence_complete": True,
        "consumer_migration_complete": True,
        "validators": ["tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py"],
        "expected_markers": ["Q37_CANONICAL_OWNERSHIP_RECONCILIATION_REGRESSION_SET: PASS"],
        "unresolved_fields": [],
    }


def valid_complete_record() -> dict[str, Any]:
    return {
        "reconciliation_required": True,
        "no_reconciliation_evidence": [],
        "q36_decision": "COMPLETE",
        "q36_frozen_baseline": "freeze-20260716-brick-wall-q36-module-size-and-cohesion-enforcement-v1",
        "feature_id": "brick-wall-q37-canonical-ownership-reconciliation-enforcement-v1",
        "operation_id": "q37-canonical-owner-fixture",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": ["docs/q37.md", "tools/q37_fixture.py"],
        "responsibility_inventory": [_responsibility()],
        "duplicate_kind_inventory": sorted(DUPLICATE_KINDS),
        "canonical_owner_selected": True,
        "consumer_migration_complete": True,
        "state_owner_reconciled": True,
        "new_super_system_created": False,
        "new_coordination_registry_created": False,
        "runtime_owner_modified": False,
        "reusable_contract_extraction_proposed": True,
        "no_extraction_evidence": [],
        "strategy_sequence": list(GENERALIZATION_SEQUENCE),
        "repair_validated_before_extraction": True,
        "shield_decision": "COMPLETE",
        "freeze_baseline_before_extraction": "freeze-validated-repair-fixture-v1",
        "extraction_owner_path": "kanda_prompt_workspace/prompt_library",
        "new_owner_created": False,
        "new_owner_gap_proven": False,
        "adoption_scope": ADOPTION_SCOPE,
        "extraction_blockers": [],
        "validators": ["tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py"],
        "expected_markers": ["Q37_CANONICAL_OWNERSHIP_RECONCILIATION_REGRESSION_SET: PASS"],
        "durable_evidence_path": "project_validation_evidence/q37.txt",
        "limitations": ["Static ownership reconciliation cannot replace runtime behavior and consumer validation."],
        "blockers": [],
        "decision": "COMPLETE",
        "may_proceed_to_q38": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update(
        reconciliation_required=False,
        no_reconciliation_evidence=[
            "The exact release changes governance prompts and validation-only tools only.",
            "No scanner, schema, report, mutable-state owner, runtime consumer, or public facade is introduced or consolidated.",
        ],
        responsibility_inventory=[],
        canonical_owner_selected=True,
        consumer_migration_complete=True,
        state_owner_reconciled=True,
        reusable_contract_extraction_proposed=False,
        no_extraction_evidence=[
            "The release does not extract a repaired local implementation into reusable infrastructure.",
            "No new reusable owner or cross-box adoption is introduced by this release.",
        ],
        strategy_sequence=[],
        repair_validated_before_extraction=False,
        shield_decision="NOT_APPLICABLE",
        freeze_baseline_before_extraction="NOT_APPLICABLE",
        extraction_owner_path="NOT_APPLICABLE",
        new_owner_created=False,
        new_owner_gap_proven=False,
        adoption_scope="NOT_APPLICABLE",
        extraction_blockers=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def validate_record(record: Mapping[str, Any]) -> None:
    missing = REQUIRED_FIELDS - set(record)
    _assert(not missing, "missing Q37 fields: " + repr(sorted(missing)))
    required = record["reconciliation_required"]
    _assert(isinstance(required, bool), "reconciliation_required must be bool")
    _assert(record["q36_decision"] in {"COMPLETE", "NOT_APPLICABLE"}, "Q36 decision must be complete")
    _assert(bool(record["q36_frozen_baseline"]), "Q36 frozen baseline is required")
    _assert(bool(record["feature_id"]) and bool(record["operation_id"]), "feature and operation IDs are required")
    _assert(bool(record["primary_box"]), "primary box is required")
    changed = record["changed_files"]
    _assert(isinstance(changed, list) and changed and len(changed) == len(set(changed)), "changed files must be unique")
    _assert(all(_safe_relative(str(path)) for path in changed), "changed files must be safe relative paths")
    _assert(set(record["duplicate_kind_inventory"]) == DUPLICATE_KINDS, "all duplicate kinds must be inventoried")
    _assert(record["new_super_system_created"] is False, "new ownership super-system is forbidden")
    _assert(record["new_coordination_registry_created"] is False, "new coordination registry is forbidden")
    _assert(record["runtime_owner_modified"] is False, "governance-only Q37 release may not modify runtime owners")
    extraction = record["reusable_contract_extraction_proposed"]
    _assert(isinstance(extraction, bool), "reusable_contract_extraction_proposed must be bool")
    _assert(isinstance(record["no_extraction_evidence"], list), "no_extraction_evidence must be a list")
    _assert(isinstance(record["strategy_sequence"], list), "strategy_sequence must be a list")
    _assert(isinstance(record["new_owner_created"], bool), "new_owner_created must be bool")
    _assert(isinstance(record["new_owner_gap_proven"], bool), "new_owner_gap_proven must be bool")
    _assert(isinstance(record["extraction_blockers"], list), "extraction_blockers must be a list")
    if extraction:
        _assert(tuple(record["strategy_sequence"]) == GENERALIZATION_SEQUENCE, "reusable extraction sequence is incomplete or out of order")
        _assert(record["repair_validated_before_extraction"] is True, "repair must be validated before extraction")
        _assert(record["shield_decision"] in SHIELD_DECISIONS, "shield decision is invalid")
        _assert(bool(record["freeze_baseline_before_extraction"]), "frozen repair baseline is required before extraction")
        _assert(record["freeze_baseline_before_extraction"] != "NOT_APPLICABLE", "frozen repair baseline cannot be N/A when extracting")
        _assert(_safe_relative(record["extraction_owner_path"]), "extraction owner path is invalid")
        _assert(not record["new_owner_created"] or record["new_owner_gap_proven"], "new owner requires a verified responsibility gap")
        _assert(record["adoption_scope"] == ADOPTION_SCOPE, "reusable adoption must remain bounded")
        _assert(not record["extraction_blockers"], "reusable extraction contains blockers")
    else:
        _assert(len(record["no_extraction_evidence"]) >= 2, "non-extraction disposition requires evidence")
        _assert(not record["strategy_sequence"], "non-extraction record must not claim a strategy sequence")
        _assert(record["shield_decision"] == "NOT_APPLICABLE", "non-extraction shield decision mismatch")
        _assert(record["freeze_baseline_before_extraction"] == "NOT_APPLICABLE", "non-extraction freeze baseline mismatch")
        _assert(record["extraction_owner_path"] == "NOT_APPLICABLE", "non-extraction owner path mismatch")
        _assert(record["new_owner_created"] is False, "non-extraction record cannot create a new owner")
        _assert(record["new_owner_gap_proven"] is False, "non-extraction record cannot claim a new-owner gap")
        _assert(record["adoption_scope"] == "NOT_APPLICABLE", "non-extraction adoption scope mismatch")
        _assert(not record["extraction_blockers"], "non-extraction record cannot contain extraction blockers")
    _assert(record["canonical_owner_selected"] is True, "canonical owner selection must be explicit")
    _assert(record["consumer_migration_complete"] is True, "consumer migration must be complete")
    _assert(record["state_owner_reconciled"] is True, "mutable-state owner reconciliation must be complete")
    responsibilities = record["responsibility_inventory"]
    _assert(isinstance(responsibilities, list), "responsibility inventory must be a list")
    if not required:
        _assert(record["decision"] == "NOT_APPLICABLE", "N/A record decision mismatch")
        _assert(not responsibilities, "N/A record must not invent responsibility rows")
        _assert(len(record["no_reconciliation_evidence"]) >= 2, "N/A evidence is incomplete")
        _assert(record["may_proceed_to_q38"] is True, "N/A may proceed to Q38")
    else:
        _assert(record["decision"] == "COMPLETE", "required reconciliation must be complete")
        _assert(responsibilities, "required reconciliation needs responsibilities")
        ids: list[str] = []
        canonical_paths: list[str] = []
        for row in responsibilities:
            missing_row = RESPONSIBILITY_FIELDS - set(row)
            _assert(not missing_row, "missing responsibility fields: " + repr(sorted(missing_row)))
            _assert(bool(row["responsibility_id"]) and bool(row["responsibility"]), "responsibility identity is required")
            ids.append(row["responsibility_id"])
            _assert(bool(row["canonical_owner_box"]), "canonical owner box is required")
            _assert(_safe_relative(row["canonical_owner_path"]), "canonical owner path is invalid")
            canonical_paths.append(row["canonical_owner_path"])
            _assert(bool(row["public_contract"]) and bool(row["source_of_truth"]), "public contract and source of truth are required")
            _assert(bool(row["state_mutation_owner"]), "state mutation owner is required")
            _assert(isinstance(row["current_consumers"], list), "current consumers must be inventoried")
            _assert(row["retirement_or_coexistence_complete"] is True, "competitor disposition must be complete")
            _assert(row["consumer_migration_complete"] is True, "responsibility consumer migration must be complete")
            _assert(not row["unresolved_fields"], "responsibility contains unresolved fields")
            candidates = row["duplicate_candidates"]
            _assert(isinstance(candidates, list), "duplicate candidates must be a list")
            paths: list[str] = []
            for candidate in candidates:
                missing_candidate = CANDIDATE_FIELDS - set(candidate)
                _assert(not missing_candidate, "missing duplicate-candidate fields: " + repr(sorted(missing_candidate)))
                _assert(_safe_relative(candidate["path"]), "duplicate candidate path is invalid")
                paths.append(candidate["path"])
                _assert(candidate["kind"] in DUPLICATE_KINDS, "unknown duplicate kind")
                _assert(candidate["disposition"] in DISPOSITIONS, "invalid competitor disposition")
                _assert(bool(candidate["reason"]), "competitor disposition reason is required")
                if candidate["disposition"] == "PUBLIC_ADAPTER":
                    _assert(candidate["public_adapter_contract"] != "NOT_APPLICABLE", "public adapter contract is required")
                    _assert(candidate["migration_target"] != "NOT_APPLICABLE", "public adapter migration target is required")
                if candidate["kind"] == "STATE_OWNER":
                    _assert(candidate["state_write_disabled"] is True, "duplicate state writes must be disabled")
                if candidate["disposition"] in {"RETIRED", "PUBLIC_ADAPTER"}:
                    _assert(candidate["consumer_migration_complete"] is True, "consumer migration is incomplete")
                if candidate["disposition"] == "COEXISTENCE_JUSTIFIED":
                    _assert("distinct" in candidate["reason"].lower(), "coexistence requires distinct-responsibility evidence")
            _assert(len(paths) == len(set(paths)), "duplicate candidate paths must be unique")
            _assert(bool(row["validators"]) and bool(row["expected_markers"]), "responsibility validation evidence is required")
        _assert(len(ids) == len(set(ids)), "responsibility IDs must be unique")
        _assert(len(canonical_paths) == len(set(canonical_paths)), "one canonical owner path per responsibility is required")
        _assert(not record["blockers"], "complete record cannot contain blockers")
        _assert(record["may_proceed_to_q38"] is True, "complete record may proceed to Q38")
    _assert(record["may_begin_coding"] is False, "Q37 does not grant coding authority")
    _assert(record["may_write_source"] is False, "Q37 does not grant source-write authority")
    _assert(bool(record["validators"]) and bool(record["expected_markers"]), "validator evidence is required")
    _assert(str(record["durable_evidence_path"]).startswith("project_validation_evidence/"), "durable evidence path must be project support")
    _assert(bool(record["limitations"]), "limitations are required")


def q37_release_record(paths: list[str]) -> dict[str, Any]:
    record = valid_not_applicable_record()
    record.update(
        feature_id="brick-wall-q37-reconcile-repair-shield-extract-sequence-v1",
        operation_id="brick-wall-q37-reconcile-repair-shield-extract-sequence-v1-release",
        changed_files=list(paths),
        validators=["tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py"],
        expected_markers=[
            "Q37_CANONICAL_OWNERSHIP_RECONCILIATION_REGRESSION_SET: PASS",
            "Q37_CURRENT_RELEASE_RECONCILIATION_NOT_APPLICABLE: PASS",
        ],
        durable_evidence_path="project_validation_evidence/brick-wall-q37-reconcile-repair-shield-extract-sequence-v1.txt",
    )
    return record


def q37_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    validators = [
        "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py",
        "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py",
        "tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py",
        "tools/validate_brick_wall_q35_focused_performance_baseline_v1.py",
        "tools/validate_brick_wall_q36_module_size_cohesion_v1.py",
        "tools/validate_brick_wall_q37_canonical_ownership_reconciliation_v1.py",
    ]
    lessons = [
        "lesson-self-hosting-physical-root-equality-validator-false-negative-v1",
        "lesson-no-isolated-zip-delivery-contract-v1",
        "lesson-brick-wall-install-literalpath-null-guard-and-provenance-v1",
        "lesson-validate-freeze-evidence-path-contract-v1",
        "lesson-freeze-hint-no-stale-local-validation-pending-v1",
        "lesson-error-memory-active-ready-regression-check-contract-v1",
    ]
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "owner_box": "tools validation-only support" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Q37 canonical ownership reconciliation governance",
            "error_memory_lessons": lessons,
            "frozen_behavior": ["freeze-20260716-brick-wall-q36-module-size-and-cohesion-enforcement-v1"],
            "focused_tests": {
                "disposition": "APPLIES",
                "validators": validators,
                "expected_markers": ["Q37_CANONICAL_OWNERSHIP_RECONCILIATION_REGRESSION_SET: PASS"],
                "reason": "Q32-Q36 forward compatibility and Q37 ownership behavior are checked.",
            },
            "boundary_tests": {
                "disposition": "APPLIES",
                "validators": [validators[-1]],
                "expected_markers": ["Q37_EXISTING_OWNERSHIP_AUTHORITIES_REUSED: PASS"],
                "reason": "Box, facade, state, and consumer owners remain canonical.",
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
                "expected_markers": ["Q37_EXACT_RELEASE_PROVENANCE: PASS"],
                "reason": "Exact payload, Q36 lineage, import context, and durable evidence are checked.",
            },
            "negative_tests": {
                "disposition": "APPLIES",
                "validators": [validators[-1]],
                "expected_markers": ["Q37_NEGATIVE_SUPER_SYSTEM: PASS"],
                "reason": "Competing owners, unresolved consumers, duplicate state writes, and coordination super-systems fail closed.",
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
