# project-path: kanda_reasoner_app/routing_signal_scorer/generator_candidate_preparation_closure_shield.py
"""Generator candidate preparation closure shield for routing scorer v3.

This module is intentionally standard-library-only and closure-shield-only.
It closes the preparatory generator-candidate runway after the review bundle
without creating or authorizing a generator candidate patch. It does not record
a human decision, does not install dependencies, does not authorize side
effects, does not generate, write, read, load, or discover semantic artifacts,
does not scan sources, does not materialize raw text, does not generate
embeddings or vectors, does not instantiate providers, does not run semantic
scoring, does not modify router authority, and does not change runtime behavior.
"""

from __future__ import annotations

__all__ = ['build_generator_candidate_preparation_closure_shield_contract', 'classify_generator_candidate_preparation_closure_shield_request', 'validate_generator_candidate_preparation_closure_shield_contract']
from collections.abc import Mapping, Sequence
from typing import Any

GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_preparation_closure_shield_v1"
)
GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_SCHEMA_VERSION = (
    "3.28-generator-candidate-preparation-closure-shield"
)
GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_STATUS = (
    "generator_candidate_preparation_closure_shield_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_PREPARATION_CLOSURE_SHIELD_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_preparation_closure_shield_only",
        "preparation_closure_scope",
        "current_preparation_closure_state",
        "current_preparation_closure_effect",
        "required_prior_milestones",
        "protected_preparation_chain_milestones",
        "kbsc_closure_dimensions",
        "required_closure_checks",
        "allowed_future_closure_outcomes",
        "allowed_closure_outputs",
        "prohibited_closure_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "closure_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_PREPARATION_CLOSURE_SCOPE = "generator_candidate_preparation_closure_shield_only"
ALLOWED_CURRENT_PREPARATION_CLOSURE_STATES = frozenset(
    {
        "preparation_closure_shield_schema_only",
        "preparation_chain_closed_for_current_phase",
        "awaiting_separate_human_review",
        "awaiting_separate_recorded_human_decision",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "v3_closure_shield_frozen",
        "disabled_generation_boundary_frozen",
        "dry_run_artifact_generation_plan_frozen",
        "local_generator_candidate_review_gate_frozen",
        "human_architectural_review_record_frozen",
        "human_decision_intake_frozen",
        "actual_human_decision_record_design_frozen",
        "actual_human_decision_recording_boundary_frozen",
        "generator_candidate_proposal_schema_frozen",
        "generator_candidate_proposal_review_frozen",
        "generator_candidate_patch_preflight_frozen",
        "generator_candidate_patch_envelope_frozen",
        "generator_candidate_patch_skeleton_frozen",
        "generator_candidate_patch_file_set_frozen",
        "generator_candidate_dependency_boundary_frozen",
        "generator_candidate_side_effect_boundary_frozen",
        "generator_candidate_review_bundle_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

PROTECTED_PREPARATION_CHAIN_MILESTONES = frozenset(
    {
        "proposal_schema_design",
        "proposal_review_design",
        "candidate_patch_preflight_design",
        "candidate_patch_envelope_design",
        "candidate_patch_skeleton_design",
        "candidate_patch_file_set_design",
        "dependency_boundary_design",
        "side_effect_boundary_design",
        "review_bundle_design",
    }
)

REQUIRED_KBSC_CLOSURE_DIMENSIONS = frozenset(
    {
        "authority_boundary_protected",
        "dependency_direction_protected",
        "truth_source_priority_protected",
        "public_contract_protected",
        "side_effect_boundary_protected",
        "regression_critical_outputs_protected",
        "do_not_invade_other_box_logic_protected",
        "future_phase_requires_new_governed_patch",
    }
)

REQUIRED_CLOSURE_CHECKS = frozenset(
    {
        "review_bundle_is_frozen_before_closure",
        "side_effect_boundary_is_frozen_before_closure",
        "dependency_boundary_is_frozen_before_closure",
        "file_set_boundary_is_frozen_before_closure",
        "skeleton_boundary_is_frozen_before_closure",
        "envelope_boundary_is_frozen_before_closure",
        "preflight_boundary_is_frozen_before_closure",
        "no_generator_candidate_patch_exists_from_preparation_chain",
        "no_generator_authorization_exists_from_preparation_chain",
        "no_dependency_install_exists_from_preparation_chain",
        "no_side_effect_authorization_exists_from_preparation_chain",
        "no_artifact_io_exists_from_preparation_chain",
        "no_source_scanning_exists_from_preparation_chain",
        "no_runtime_enablement_exists_from_preparation_chain",
        "no_router_authority_exists_from_preparation_chain",
        "future_candidate_patch_requires_separate_governed_patch",
        "future_generation_requires_separate_governed_patch",
    }
)

ALLOWED_FUTURE_CLOSURE_OUTCOMES = frozenset(
    {
        "stop_after_preparation_chain",
        "request_explicit_human_decision_review",
        "request_full_freeze_entry_context_before_candidate_patch",
        "permit_separate_governed_generator_candidate_patch_design_only",
        "reject_generator_candidate_patch_readiness",
        "defer_generator_candidate_patch_readiness",
    }
)

REQUIRED_ALLOWED_CLOSURE_OUTPUTS = frozenset(
    {
        "generator_candidate_preparation_closure_shield_schema",
        "preparation_chain_closure_summary",
        "protected_preparation_milestone_list",
        "kbsc_closure_dimension_summary",
        "candidate_patch_stop_conditions",
        "future_phase_requirements_summary",
        "no_generator_candidate_patch_created",
        "no_generator_candidate_authorized",
        "no_generator_implementation_authorized",
        "no_dependency_install_authorized",
        "no_side_effect_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_CLOSURE_OUTPUTS = frozenset(
    {
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generator_implementation",
        "dependency_install_request",
        "third_party_dependency_request",
        "side_effect_authorization",
        "artifact_generation_plan_authorization",
        "artifact_generation_execution",
        "artifact_write_request",
        "artifact_read_request",
        "source_scan_request",
        "raw_text_materialization_request",
        "embedding_generation_request",
        "vector_index_generation_request",
        "provider_execution_request",
        "runtime_semantic_signal",
        "router_authority_signal",
        "may_proceed_now_signal",
        "freeze_memory_write_request",
        "prompt_auto_load_request",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "real_human_decision_recording_enabled",
        "dependency_install_enabled",
        "third_party_dependency_enabled",
        "side_effect_authorization_enabled",
        "generator_candidate_patch_creation_enabled",
        "generator_candidate_patch_authorization_enabled",
        "generator_implementation_enabled",
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_reading_enabled",
        "artifact_loading_enabled",
        "artifact_discovery_enabled",
        "source_scanning_enabled",
        "prompt_library_scanning_enabled",
        "freeze_entry_scanning_enabled",
        "project_source_scanning_enabled",
        "runtime_query_scanning_enabled",
        "raw_text_materialization_enabled",
        "embedding_generation_enabled",
        "vector_generation_enabled",
        "vector_index_writing_enabled",
        "provider_execution_enabled",
        "network_access_enabled",
        "credential_loading_enabled",
        "model_loading_enabled",
        "semantic_runtime_scoring_enabled",
        "startup_generation_enabled",
        "background_generation_enabled",
        "file_watcher_generation_enabled",
        "router_authority_enabled",
        "public_runtime_export_enabled",
        "freeze_memory_writing_enabled",
        "prompt_auto_loading_enabled",
    }
)

FORBIDDEN_CLOSURE_FIELDS = REQUIRED_PROHIBITED_CLOSURE_OUTPUTS

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "closure_shield_does_not_record_real_human_decision",
        "closure_shield_does_not_create_candidate_patch",
        "closure_shield_does_not_authorize_candidate_patch",
        "closure_shield_does_not_authorize_generator",
        "closure_shield_does_not_authorize_dependencies",
        "closure_shield_does_not_authorize_side_effects",
        "closure_shield_does_not_authorize_artifact_generation",
        "closure_shield_does_not_authorize_artifact_reading",
        "closure_shield_does_not_authorize_artifact_writing",
        "closure_shield_does_not_authorize_source_scanning",
        "closure_shield_does_not_authorize_raw_text_materialization",
        "closure_shield_does_not_authorize_embedding_generation",
        "closure_shield_does_not_authorize_vector_generation",
        "closure_shield_does_not_authorize_provider_execution",
        "closure_shield_does_not_authorize_runtime_semantic_enablement",
        "closure_shield_does_not_authorize_router_authority",
        "closure_shield_does_not_write_freeze_memory",
        "closure_shield_does_not_auto_load_prompts",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_human_decision_is_missing",
        "stop_if_full_freeze_context_is_required_but_not_loaded",
        "stop_if_candidate_patch_creation_is_requested",
        "stop_if_generator_authorization_is_requested",
        "stop_if_dependency_install_is_requested",
        "stop_if_side_effect_authorization_is_requested",
        "stop_if_artifact_generation_is_requested",
        "stop_if_artifact_read_or_write_is_requested",
        "stop_if_source_scanning_is_requested",
        "stop_if_raw_text_materialization_is_requested",
        "stop_if_embedding_or_vector_generation_is_requested",
        "stop_if_provider_or_model_execution_is_requested",
        "stop_if_runtime_or_router_authority_is_requested",
        "stop_if_other_box_logic_would_be_modified",
    }
)

def _as_set(value: Any) -> set[Any]:
    """Support as set behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    set[Any]
        The set result.
    """
    
    if isinstance(value, str):
        return {value}
    if isinstance(value, Sequence):
        return set(value)
    return set()

def _false_flags() -> dict[str, bool]:
    """Support false flags behavior.
    
    Returns
    -------
    dict[str, bool]
        The mapped values.
    """
    
    return {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)}

def build_generator_candidate_preparation_closure_shield_contract() -> dict[str, Any]:
    """Return the schema-only closure shield for the preparation chain."""
    return {
        "schema_id": GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_STATUS,
        "declared_generator_candidate_preparation_closure_shield_only": True,
        "preparation_closure_scope": REQUIRED_PREPARATION_CLOSURE_SCOPE,
        "current_preparation_closure_state": "preparation_closure_shield_schema_only",
        "current_preparation_closure_effect": "no_effect_schema_only_preparation_closure_shield",
        "required_prior_milestones": sorted(REQUIRED_PRIOR_MILESTONES),
        "protected_preparation_chain_milestones": sorted(PROTECTED_PREPARATION_CHAIN_MILESTONES),
        "kbsc_closure_dimensions": sorted(REQUIRED_KBSC_CLOSURE_DIMENSIONS),
        "required_closure_checks": sorted(REQUIRED_CLOSURE_CHECKS),
        "allowed_future_closure_outcomes": sorted(ALLOWED_FUTURE_CLOSURE_OUTCOMES),
        "allowed_closure_outputs": sorted(REQUIRED_ALLOWED_CLOSURE_OUTPUTS),
        "prohibited_closure_outputs": sorted(REQUIRED_PROHIBITED_CLOSURE_OUTPUTS),
        "disabled_flags": _false_flags(),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "closure_effect_policy": (
            "This closure shield only protects the completed generator-candidate "
            "preparation chain. It cannot create or authorize a candidate patch, "
            "generation, dependency installation, side effects, artifact IO, source "
            "scanning, runtime behavior, router authority, prompt loading, or freeze writes."
        ),
        "stop_conditions": sorted(REQUIRED_STOP_CONDITIONS),
    }

def validate_generator_candidate_preparation_closure_shield_contract(
    contract: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the schema-only closure shield without enabling behavior."""
    errors: list[str] = []

    for field in sorted(REQUIRED_PREPARATION_CLOSURE_SHIELD_FIELDS):
        if field not in contract:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_CLOSURE_FIELDS):
        if field in contract:
            errors.append(f"forbidden closure field present: {field}")

    if contract.get("schema_id") != GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_FEATURE_ID:
        errors.append("schema_id mismatch")
    if contract.get("schema_version") != GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if contract.get("preparation_closure_scope") != REQUIRED_PREPARATION_CLOSURE_SCOPE:
        errors.append("preparation_closure_scope mismatch")
    if contract.get("current_preparation_closure_state") not in ALLOWED_CURRENT_PREPARATION_CLOSURE_STATES:
        errors.append("current_preparation_closure_state is not allowed")
    if contract.get("declared_generator_candidate_preparation_closure_shield_only") is not True:
        errors.append("closure shield must be declared schema-only")

    subset_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("protected_preparation_chain_milestones", PROTECTED_PREPARATION_CHAIN_MILESTONES),
        ("kbsc_closure_dimensions", REQUIRED_KBSC_CLOSURE_DIMENSIONS),
        ("required_closure_checks", REQUIRED_CLOSURE_CHECKS),
        ("allowed_future_closure_outcomes", ALLOWED_FUTURE_CLOSURE_OUTCOMES),
        ("allowed_closure_outputs", REQUIRED_ALLOWED_CLOSURE_OUTPUTS),
        ("prohibited_closure_outputs", REQUIRED_PROHIBITED_CLOSURE_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for field, required in subset_checks:
        actual = _as_set(contract.get(field, []))
        missing = required - actual
        if missing:
            errors.append(f"{field} missing required values: {sorted(missing)}")

    disabled_flags = contract.get("disabled_flags", {})
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
    else:
        for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
            if flag not in disabled_flags:
                errors.append(f"missing disabled flag: {flag}")
            elif disabled_flags[flag] is not False:
                errors.append(f"disabled flag must be false: {flag}")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "schema_id": contract.get("schema_id"),
        "schema_version": contract.get("schema_version"),
        "current_preparation_closure_state": contract.get("current_preparation_closure_state"),
        "real_human_decision_recorded_by_preparation_closure_shield": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_implementation_authorized": False,
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reading_authorized": False,
        "artifact_loading_authorized": False,
        "artifact_discovery_authorized": False,
        "source_scanning_authorized": False,
        "raw_text_materialization_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_generation_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "router_authority_authorized": False,
        "public_runtime_export_authorized": False,
        "freeze_memory_writing_authorized": False,
        "prompt_auto_loading_authorized": False,
        "requires_prior_recorded_human_decision": True,
        "requires_prior_generator_candidate_review_bundle": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
        "kbsc_preparation_chain_closure_declared": ok,
        "preparation_chain_closed_for_current_phase": ok,
    }

def classify_generator_candidate_preparation_closure_shield_request(request_text: str) -> dict[str, Any]:
    """Classify closure-shield requests without enabling candidate patch work."""
    text = request_text.lower()
    forbidden_markers = (
        "approve",
        "authorize",
        "create candidate patch",
        "implement generator",
        "generate artifact",
        "write artifact",
        "read artifact",
        "scan source",
        "scan prompt",
        "materialize raw text",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "router authority",
        "may proceed",
        "install dependency",
        "side effect",
        "freeze write",
        "auto load",
    )
    allowed_markers = (
        "schema",
        "checklist",
        "closure",
        "shield",
        "kbsc",
        "summary",
        "show",
        "review",
    )
    blocked = any(marker in text for marker in forbidden_markers)
    allowed_schema_view = any(marker in text for marker in allowed_markers)
    allowed_now = allowed_schema_view and not blocked
    return {
        "allowed_now": allowed_now,
        "permitted_output": (
            "generator_candidate_preparation_closure_shield_schema" if allowed_now else None
        ),
        "current_preparation_closure_state": "preparation_closure_shield_schema_only",
        "real_human_decision_recorded_by_preparation_closure_shield": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_implementation_authorized": False,
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reading_authorized": False,
        "source_scanning_authorized": False,
        "raw_text_materialization_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_generation_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "router_authority_authorized": False,
        "freeze_memory_writing_authorized": False,
        "prompt_auto_loading_authorized": False,
        "requires_prior_recorded_human_decision": True,
        "requires_prior_generator_candidate_review_bundle": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
