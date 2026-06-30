# project-path: kanda_reasoner_app/routing_signal_scorer/generator_candidate_patch_skeleton_design.py
"""Generator candidate patch skeleton design for routing scorer v3.

This module is intentionally standard-library-only and skeleton-design-only. It
models the metadata skeleton that a future, separately governed generator
candidate patch would have to provide. It does not create a generator candidate
patch, does not authorize a generator, does not record a human decision, does
not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors,
does not instantiate providers, does not run semantic scoring, does not modify
router authority, and does not change runtime behavior.
"""

from __future__ import annotations


__all__ = [
    'build_generator_candidate_patch_skeleton_contract',
    'classify_generator_candidate_patch_skeleton_request',
    'validate_generator_candidate_patch_skeleton_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_PATCH_SKELETON_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_patch_skeleton_design_v1"
)
GENERATOR_CANDIDATE_PATCH_SKELETON_SCHEMA_VERSION = (
    "3.23-generator-candidate-patch-skeleton-design"
)
GENERATOR_CANDIDATE_PATCH_SKELETON_STATUS = (
    "generator_candidate_patch_skeleton_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_SKELETON_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_patch_skeleton_only",
        "skeleton_scope",
        "current_skeleton_state",
        "current_skeleton_effect",
        "required_prior_milestones",
        "required_skeleton_sections",
        "required_candidate_patch_declarations",
        "required_boundary_declarations",
        "required_validation_declarations",
        "allowed_future_skeleton_outcomes",
        "allowed_skeleton_outputs",
        "prohibited_skeleton_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "skeleton_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_SKELETON_SCOPE = "generator_candidate_patch_skeleton_only"
ALLOWED_CURRENT_SKELETON_STATES = frozenset(
    {
        "not_skeletoned",
        "skeleton_schema_only",
        "awaiting_separate_preflight_acceptance",
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
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_SKELETON_SECTIONS = frozenset(
    {
        "candidate_patch_identity",
        "candidate_patch_scope",
        "candidate_patch_non_goals",
        "candidate_patch_touched_paths",
        "candidate_patch_dependency_budget",
        "candidate_patch_privacy_boundary",
        "candidate_patch_source_boundary",
        "candidate_patch_raw_text_boundary",
        "candidate_patch_artifact_lifecycle_boundary",
        "candidate_patch_runtime_boundary",
        "candidate_patch_router_authority_boundary",
        "candidate_patch_public_contract_boundary",
        "candidate_patch_validation_plan",
        "candidate_patch_rollback_plan",
        "candidate_patch_kbsc_shielding_plan",
        "candidate_patch_freeze_plan",
        "candidate_patch_stop_conditions",
    }
)

REQUIRED_CANDIDATE_PATCH_DECLARATIONS = frozenset(
    {
        "candidate_patch_is_separate_future_patch",
        "candidate_patch_is_not_created_by_this_skeleton",
        "candidate_patch_is_not_authorized_by_this_skeleton",
        "candidate_patch_requires_recorded_human_decision_reference",
        "candidate_patch_requires_preflight_reference",
        "candidate_patch_requires_review_evidence_reference",
        "candidate_patch_requires_explicit_touched_paths",
        "candidate_patch_requires_no_public_runtime_export_by_default",
        "candidate_patch_requires_no_router_authority_by_default",
        "candidate_patch_requires_kbsc_before_merge",
    }
)

REQUIRED_BOUNDARY_DECLARATIONS = frozenset(
    {
        "no_generation_in_skeleton",
        "no_artifact_write_in_skeleton",
        "no_artifact_read_in_skeleton",
        "no_source_scan_in_skeleton",
        "no_raw_text_materialization_in_skeleton",
        "no_embedding_generation_in_skeleton",
        "no_vector_materialization_in_skeleton",
        "no_provider_execution_in_skeleton",
        "no_network_access_in_skeleton",
        "no_credential_loading_in_skeleton",
        "no_model_loading_in_skeleton",
        "no_runtime_semantic_enablement_in_skeleton",
        "no_router_authority_change_in_skeleton",
        "no_prompt_auto_loading_in_skeleton",
        "no_freeze_memory_write_from_skeleton_output",
    }
)

REQUIRED_VALIDATION_DECLARATIONS = frozenset(
    {
        "candidate_patch_must_have_static_validation",
        "candidate_patch_must_have_contract_tests",
        "candidate_patch_must_have_regression_tests",
        "candidate_patch_must_have_no_public_export_test",
        "candidate_patch_must_have_no_forbidden_runtime_paths_test",
        "candidate_patch_must_have_ascii_test",
        "candidate_patch_must_have_freeze_hint",
        "candidate_patch_must_have_install_validation_commands",
        "candidate_patch_must_have_rollback_boundary",
        "candidate_patch_must_have_kbsc_shield_test",
    }
)

ALLOWED_FUTURE_SKELETON_OUTCOMES = frozenset(
    {
        "reject_candidate_patch_skeleton",
        "defer_candidate_patch_skeleton",
        "request_more_preflight_evidence",
        "request_more_human_decision_evidence",
        "permit_separate_governed_generator_candidate_patch_design_only",
    }
)

REQUIRED_ALLOWED_SKELETON_OUTPUTS = frozenset(
    {
        "candidate_patch_skeleton_schema",
        "candidate_patch_required_sections",
        "candidate_patch_required_declarations",
        "candidate_patch_boundary_declarations",
        "candidate_patch_validation_declarations",
        "future_skeleton_outcome_vocabulary",
        "skeleton_effect_policy_summary",
        "stop_conditions_list",
        "skeleton_evidence_only",
        "no_generator_candidate_patch_created",
        "no_generator_candidate_authorized",
        "no_generator_implementation_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_SKELETON_OUTPUTS = frozenset(
    {
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generator_implementation",
        "artifact_generator",
        "generated_artifact",
        "written_artifact",
        "loaded_artifact",
        "read_artifact",
        "raw_prompt_text",
        "raw_user_query_text",
        "raw_freeze_entry_text",
        "raw_source_text",
        "embedding_values",
        "vector_values",
        "vector_index",
        "provider_config",
        "model_config",
        "runtime_semantic_score",
        "final_route",
        "required_prompts",
        "missing_context_decision",
        "missing_behavior_decision",
        "may_proceed_now",
        "prompt_auto_load_list",
        "freeze_memory_write",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "real_human_decision_recorded_by_skeleton",
        "generator_candidate_patch_created",
        "generator_candidate_patch_authorized",
        "generator_implementation_authorized",
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_overwrite_enabled",
        "artifact_reader_enabled",
        "artifact_loading_enabled",
        "source_scanning_enabled",
        "raw_text_materialization_enabled",
        "embedding_generation_enabled",
        "vector_materialization_enabled",
        "vector_index_generation_enabled",
        "provider_execution_enabled",
        "network_access_enabled",
        "credential_loading_enabled",
        "model_loading_enabled",
        "startup_generation_enabled",
        "runtime_generation_enabled",
        "background_generation_enabled",
        "file_watcher_generation_enabled",
        "semantic_runtime_enabled",
        "router_authority_enabled",
        "prompt_auto_load_enabled",
        "freeze_memory_write_enabled",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "skeleton_does_not_decide_routes",
        "skeleton_does_not_decide_required_prompts",
        "skeleton_does_not_decide_missing_context",
        "skeleton_does_not_decide_missing_behavior",
        "skeleton_does_not_decide_may_proceed_now",
        "skeleton_does_not_load_prompts",
        "skeleton_does_not_write_freeze_memory",
        "skeleton_does_not_authorize_generation",
        "skeleton_does_not_create_candidate_patch",
    }
)

REQUIRED_SKELETON_EFFECT_POLICY = frozenset(
    {
        "schema_only_current_effect",
        "no_candidate_patch_created",
        "no_generator_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_behavior_change",
        "future_candidate_patch_requires_separate_governed_patch",
        "future_generation_requires_separate_governed_patch",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_request_asks_to_create_candidate_patch_now",
        "stop_if_request_asks_to_authorize_generator_now",
        "stop_if_request_asks_to_generate_artifact_now",
        "stop_if_request_asks_to_write_or_read_artifact_now",
        "stop_if_request_asks_to_scan_sources_now",
        "stop_if_request_asks_to_materialize_raw_text_now",
        "stop_if_request_asks_to_generate_embeddings_or_vectors_now",
        "stop_if_request_asks_to_add_provider_network_credentials_or_model_now",
        "stop_if_request_asks_to_enable_runtime_semantics_now",
        "stop_if_request_asks_to_change_router_authority_now",
    }
)

FORBIDDEN_SKELETON_FIELDS = REQUIRED_PROHIBITED_SKELETON_OUTPUTS


def _sorted_tuple(values: frozenset[str]) -> tuple[str, ...]:
    """Support sorted tuple behavior.
    
    Parameters
    ----------
    values : frozenset[str]
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return tuple(sorted(values))


def build_generator_candidate_patch_skeleton_contract() -> dict[str, Any]:
    """Return the frozen design contract for generator candidate patch skeleton."""

    return {
        "schema_id": GENERATOR_CANDIDATE_PATCH_SKELETON_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_PATCH_SKELETON_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_PATCH_SKELETON_STATUS,
        "declared_generator_candidate_patch_skeleton_only": True,
        "skeleton_scope": REQUIRED_SKELETON_SCOPE,
        "current_skeleton_state": "not_skeletoned",
        "current_skeleton_effect": "no_effect_schema_only_not_skeletoned",
        "required_prior_milestones": _sorted_tuple(REQUIRED_PRIOR_MILESTONES),
        "required_skeleton_sections": _sorted_tuple(REQUIRED_SKELETON_SECTIONS),
        "required_candidate_patch_declarations": _sorted_tuple(REQUIRED_CANDIDATE_PATCH_DECLARATIONS),
        "required_boundary_declarations": _sorted_tuple(REQUIRED_BOUNDARY_DECLARATIONS),
        "required_validation_declarations": _sorted_tuple(REQUIRED_VALIDATION_DECLARATIONS),
        "allowed_future_skeleton_outcomes": _sorted_tuple(ALLOWED_FUTURE_SKELETON_OUTCOMES),
        "allowed_skeleton_outputs": _sorted_tuple(REQUIRED_ALLOWED_SKELETON_OUTPUTS),
        "prohibited_skeleton_outputs": _sorted_tuple(REQUIRED_PROHIBITED_SKELETON_OUTPUTS),
        "disabled_flags": {key: False for key in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted_tuple(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "skeleton_effect_policy": _sorted_tuple(REQUIRED_SKELETON_EFFECT_POLICY),
        "stop_conditions": _sorted_tuple(REQUIRED_STOP_CONDITIONS),
    }


def _as_set(value: object) -> set[str]:
    """Support as set behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    if isinstance(value, str) or not isinstance(value, Sequence):
        return set()
    return {item for item in value if isinstance(item, str)}


def validate_generator_candidate_patch_skeleton_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a candidate skeleton design contract without side effects."""

    errors: list[str] = []
    for field in sorted(REQUIRED_SKELETON_FIELDS):
        if field not in candidate:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_SKELETON_FIELDS):
        if field in candidate:
            errors.append(f"forbidden skeleton field present: {field}")

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_PATCH_SKELETON_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_PATCH_SKELETON_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_PATCH_SKELETON_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_patch_skeleton_only") is not True:
        errors.append("contract must declare skeleton-only mode")
    if candidate.get("skeleton_scope") != REQUIRED_SKELETON_SCOPE:
        errors.append("skeleton_scope mismatch")
    if candidate.get("current_skeleton_state") not in ALLOWED_CURRENT_SKELETON_STATES:
        errors.append("current_skeleton_state is not allowed")
    if candidate.get("current_skeleton_effect") != "no_effect_schema_only_not_skeletoned":
        errors.append("current_skeleton_effect must remain schema-only/no-effect")

    required_sets = {
        "required_prior_milestones": REQUIRED_PRIOR_MILESTONES,
        "required_skeleton_sections": REQUIRED_SKELETON_SECTIONS,
        "required_candidate_patch_declarations": REQUIRED_CANDIDATE_PATCH_DECLARATIONS,
        "required_boundary_declarations": REQUIRED_BOUNDARY_DECLARATIONS,
        "required_validation_declarations": REQUIRED_VALIDATION_DECLARATIONS,
        "allowed_future_skeleton_outcomes": ALLOWED_FUTURE_SKELETON_OUTCOMES,
        "allowed_skeleton_outputs": REQUIRED_ALLOWED_SKELETON_OUTPUTS,
        "prohibited_skeleton_outputs": REQUIRED_PROHIBITED_SKELETON_OUTPUTS,
        "no_authority_assertions": REQUIRED_NO_AUTHORITY_ASSERTIONS,
        "skeleton_effect_policy": REQUIRED_SKELETON_EFFECT_POLICY,
        "stop_conditions": REQUIRED_STOP_CONDITIONS,
    }
    for field, required in required_sets.items():
        actual = _as_set(candidate.get(field))
        missing = sorted(required.difference(actual))
        if missing:
            errors.append(f"{field} missing required values: {missing}")

    disabled_flags = candidate.get("disabled_flags")
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
    else:
        for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
            if disabled_flags.get(flag) is not False:
                errors.append(f"disabled flag must be false: {flag}")

    ok = not errors
    return {
        "ok": ok,
        "errors": tuple(errors),
        "schema_id": candidate.get("schema_id"),
        "schema_version": candidate.get("schema_version"),
        "current_skeleton_state": candidate.get("current_skeleton_state"),
        "real_human_decision_recorded_by_skeleton": False,
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
        "requires_prior_recorded_human_decision": True,
        "requires_prior_generator_candidate_patch_preflight": True,
        "requires_prior_generator_candidate_patch_envelope": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_patch_skeleton_request(action: str) -> dict[str, Any]:
    """Classify whether an action is allowed by this design-only skeleton."""

    lowered = action.lower()
    unsafe_terms = (
        "create candidate patch",
        "candidate patch now",
        "authorize generator",
        "implement generator",
        "generate artifact",
        "write artifact",
        "read artifact",
        "load artifact",
        "scan source",
        "scan prompt",
        "raw text",
        "embedding",
        "vector",
        "provider",
        "model",
        "network",
        "credential",
        "runtime semantic",
        "router authority",
        "may proceed",
        "auto-load",
        "freeze memory write",
    )
    safe_terms = (
        "show",
        "view",
        "schema",
        "checklist",
        "skeleton",
        "sections",
        "declarations",
    )
    allowed_now = any(term in lowered for term in safe_terms) and not any(
        term in lowered for term in unsafe_terms
    )
    return {
        "allowed_now": allowed_now,
        "permitted_output": "generator_candidate_patch_skeleton_schema" if allowed_now else None,
        "current_skeleton_state": "not_skeletoned",
        "real_human_decision_recorded_by_skeleton": False,
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
        "requires_prior_recorded_human_decision": True,
        "requires_prior_generator_candidate_patch_preflight": True,
        "requires_prior_generator_candidate_patch_envelope": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
