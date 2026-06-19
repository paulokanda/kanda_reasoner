"""Generator candidate dependency boundary design for routing scorer v3.

This module is intentionally standard-library-only and dependency_boundary-design-only. It
models the dependency boundary metadata that a future, separately governed generator
candidate patch would have to satisfy before any dependency can be introduced. It does not create a generator candidate
patch, does not authorize a generator, does not record a human decision, does
not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors,
does not instantiate providers, does not run semantic scoring, does not modify
router authority, and does not change runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_dependency_boundary_design_v1"
)
GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_SCHEMA_VERSION = (
    "3.25-generator-candidate-dependency-boundary-design"
)
GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_STATUS = (
    "generator_candidate_dependency_boundary_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_DEPENDENCY_BOUNDARY_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_dependency_boundary_only",
        "dependency_boundary_scope",
        "current_dependency_boundary_state",
        "current_dependency_boundary_effect",
        "required_prior_milestones",
        "required_dependency_boundary_sections",
        "required_candidate_patch_declarations",
        "required_boundary_declarations",
        "required_validation_declarations",
        "allowed_future_dependency_boundary_outcomes",
        "allowed_dependency_boundary_outputs",
        "prohibited_dependency_boundary_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "dependency_boundary_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_DEPENDENCY_BOUNDARY_SCOPE = "generator_candidate_dependency_boundary_only"
ALLOWED_CURRENT_DEPENDENCY_BOUNDARY_STATES = frozenset(
    {
        "not_dependency_boundary_defined",
        "dependency_boundary_schema_only",
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
        "generator_candidate_patch_skeleton_frozen",
        "generator_candidate_patch_file_set_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_DEPENDENCY_BOUNDARY_SECTIONS = frozenset(
    {
        "candidate_patch_identity",
        "candidate_patch_scope",
        "candidate_patch_non_goals",
        "candidate_patch_touched_paths",
        "candidate_patch_allowed_dependency_boundary",
        "candidate_patch_forbidden_dependency_boundary",
        "candidate_patch_standard_library_only_default",
        "candidate_patch_forbidden_dependency_classes",
        "candidate_patch_dependency_exception_process",
        "candidate_patch_dependency_budget",
        "candidate_patch_standard_library_only_default",
        "candidate_patch_forbidden_dependency_classes",
        "candidate_patch_dependency_exception_process",
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
        "candidate_patch_is_not_created_by_this_dependency_boundary",
        "candidate_patch_is_not_authorized_by_this_dependency_boundary",
        "candidate_patch_requires_recorded_human_decision_reference",
        "candidate_patch_requires_preflight_reference",
        "candidate_patch_requires_review_evidence_reference",
        "candidate_patch_requires_explicit_touched_paths",
        "candidate_patch_requires_declared_allowed_dependencies",
        "candidate_patch_requires_declared_forbidden_dependencies",
        "candidate_patch_requires_no_dependency_installation_by_default",
        "candidate_patch_requires_no_public_runtime_export_by_default",
        "candidate_patch_requires_no_router_authority_by_default",
        "candidate_patch_requires_kbsc_before_merge",
    }
)

REQUIRED_BOUNDARY_DECLARATIONS = frozenset(
    {
        "standard_library_only_by_default",
        "no_dependency_installation_in_dependency_boundary",
        "no_third_party_dependency_addition_in_dependency_boundary",
        "no_generation_in_dependency_boundary",
        "no_artifact_write_in_dependency_boundary",
        "no_artifact_read_in_dependency_boundary",
        "no_source_scan_in_dependency_boundary",
        "no_raw_text_materialization_in_dependency_boundary",
        "no_embedding_generation_in_dependency_boundary",
        "no_vector_materialization_in_dependency_boundary",
        "no_provider_execution_in_dependency_boundary",
        "no_network_access_in_dependency_boundary",
        "no_credential_loading_in_dependency_boundary",
        "no_model_loading_in_dependency_boundary",
        "no_embedding_library_dependency_in_dependency_boundary",
        "no_vector_store_dependency_in_dependency_boundary",
        "no_ml_runtime_dependency_in_dependency_boundary",
        "no_runtime_semantic_enablement_in_dependency_boundary",
        "no_router_authority_change_in_dependency_boundary",
        "no_prompt_auto_loading_in_dependency_boundary",
        "no_freeze_memory_write_from_dependency_boundary_output",
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

ALLOWED_FUTURE_DEPENDENCY_BOUNDARY_OUTCOMES = frozenset(
    {
        "reject_candidate_patch_dependency_boundary",
        "defer_candidate_patch_dependency_boundary",
        "request_more_preflight_evidence",
        "request_more_human_decision_evidence",
        "permit_separate_governed_generator_candidate_patch_design_only",
    }
)

REQUIRED_ALLOWED_DEPENDENCY_BOUNDARY_OUTPUTS = frozenset(
    {
        "candidate_patch_dependency_boundary_schema",
        "candidate_patch_allowed_dependency_boundary",
        "candidate_patch_forbidden_dependency_boundary",
        "candidate_patch_standard_library_only_default",
        "candidate_patch_forbidden_dependency_classes",
        "candidate_patch_dependency_exception_process",
        "candidate_patch_required_dependency_boundary",
        "candidate_patch_dependency_boundary_schema",
        "candidate_patch_allowed_dependencies",
        "candidate_patch_forbidden_dependencies",
        "candidate_patch_required_sections",
        "candidate_patch_allowed_files",
        "candidate_patch_forbidden_files",
        "candidate_patch_required_declarations",
        "candidate_patch_boundary_declarations",
        "candidate_patch_validation_declarations",
        "future_dependency_boundary_outcome_vocabulary",
        "dependency_boundary_effect_policy_summary",
        "stop_conditions_list",
        "dependency_boundary_evidence_only",
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

REQUIRED_PROHIBITED_DEPENDENCY_BOUNDARY_OUTPUTS = frozenset(
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
        "dependency_install_plan",
        "third_party_dependency",
        "embedding_library_dependency",
        "vector_store_dependency",
        "ml_runtime_dependency",
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
        "real_human_decision_recorded_by_dependency_boundary",
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
        "dependency_installation_enabled",
        "third_party_dependency_enabled",
        "embedding_library_dependency_enabled",
        "vector_store_dependency_enabled",
        "ml_runtime_dependency_enabled",
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
        "dependency_boundary_does_not_decide_routes",
        "dependency_boundary_does_not_decide_required_prompts",
        "dependency_boundary_does_not_decide_missing_context",
        "dependency_boundary_does_not_decide_missing_behavior",
        "dependency_boundary_does_not_decide_may_proceed_now",
        "dependency_boundary_does_not_load_prompts",
        "dependency_boundary_does_not_write_freeze_memory",
        "dependency_boundary_does_not_authorize_generation",
        "dependency_boundary_does_not_create_candidate_patch",
    }
)

REQUIRED_DEPENDENCY_BOUNDARY_EFFECT_POLICY = frozenset(
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

FORBIDDEN_DEPENDENCY_BOUNDARY_FIELDS = REQUIRED_PROHIBITED_DEPENDENCY_BOUNDARY_OUTPUTS


def _sorted_tuple(values: frozenset[str]) -> tuple[str, ...]:
    return tuple(sorted(values))


def build_generator_candidate_dependency_boundary_contract() -> dict[str, Any]:
    """Return the frozen design contract for generator candidate dependency boundary."""

    return {
        "schema_id": GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_STATUS,
        "declared_generator_candidate_dependency_boundary_only": True,
        "dependency_boundary_scope": REQUIRED_DEPENDENCY_BOUNDARY_SCOPE,
        "current_dependency_boundary_state": "not_dependency_boundary_defined",
        "current_dependency_boundary_effect": "no_effect_schema_only_not_dependency_boundary_defined",
        "required_prior_milestones": _sorted_tuple(REQUIRED_PRIOR_MILESTONES),
        "required_dependency_boundary_sections": _sorted_tuple(REQUIRED_DEPENDENCY_BOUNDARY_SECTIONS),
        "required_candidate_patch_declarations": _sorted_tuple(REQUIRED_CANDIDATE_PATCH_DECLARATIONS),
        "required_boundary_declarations": _sorted_tuple(REQUIRED_BOUNDARY_DECLARATIONS),
        "required_validation_declarations": _sorted_tuple(REQUIRED_VALIDATION_DECLARATIONS),
        "allowed_future_dependency_boundary_outcomes": _sorted_tuple(ALLOWED_FUTURE_DEPENDENCY_BOUNDARY_OUTCOMES),
        "allowed_dependency_boundary_outputs": _sorted_tuple(REQUIRED_ALLOWED_DEPENDENCY_BOUNDARY_OUTPUTS),
        "prohibited_dependency_boundary_outputs": _sorted_tuple(REQUIRED_PROHIBITED_DEPENDENCY_BOUNDARY_OUTPUTS),
        "disabled_flags": {key: False for key in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted_tuple(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "dependency_boundary_effect_policy": _sorted_tuple(REQUIRED_DEPENDENCY_BOUNDARY_EFFECT_POLICY),
        "stop_conditions": _sorted_tuple(REQUIRED_STOP_CONDITIONS),
    }


def _as_set(value: object) -> set[str]:
    if isinstance(value, str) or not isinstance(value, Sequence):
        return set()
    return {item for item in value if isinstance(item, str)}


def validate_generator_candidate_dependency_boundary_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a candidate dependency_boundary design contract without side effects."""

    errors: list[str] = []
    for field in sorted(REQUIRED_DEPENDENCY_BOUNDARY_FIELDS):
        if field not in candidate:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_DEPENDENCY_BOUNDARY_FIELDS):
        if field in candidate:
            errors.append(f"forbidden dependency_boundary field present: {field}")

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_DEPENDENCY_BOUNDARY_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_dependency_boundary_only") is not True:
        errors.append("contract must declare dependency_boundary-only mode")
    if candidate.get("dependency_boundary_scope") != REQUIRED_DEPENDENCY_BOUNDARY_SCOPE:
        errors.append("dependency_boundary_scope mismatch")
    if candidate.get("current_dependency_boundary_state") not in ALLOWED_CURRENT_DEPENDENCY_BOUNDARY_STATES:
        errors.append("current_dependency_boundary_state is not allowed")
    if candidate.get("current_dependency_boundary_effect") != "no_effect_schema_only_not_dependency_boundary_defined":
        errors.append("current_dependency_boundary_effect must remain schema-only/no-effect")

    required_sets = {
        "required_prior_milestones": REQUIRED_PRIOR_MILESTONES,
        "required_dependency_boundary_sections": REQUIRED_DEPENDENCY_BOUNDARY_SECTIONS,
        "required_candidate_patch_declarations": REQUIRED_CANDIDATE_PATCH_DECLARATIONS,
        "required_boundary_declarations": REQUIRED_BOUNDARY_DECLARATIONS,
        "required_validation_declarations": REQUIRED_VALIDATION_DECLARATIONS,
        "allowed_future_dependency_boundary_outcomes": ALLOWED_FUTURE_DEPENDENCY_BOUNDARY_OUTCOMES,
        "allowed_dependency_boundary_outputs": REQUIRED_ALLOWED_DEPENDENCY_BOUNDARY_OUTPUTS,
        "prohibited_dependency_boundary_outputs": REQUIRED_PROHIBITED_DEPENDENCY_BOUNDARY_OUTPUTS,
        "no_authority_assertions": REQUIRED_NO_AUTHORITY_ASSERTIONS,
        "dependency_boundary_effect_policy": REQUIRED_DEPENDENCY_BOUNDARY_EFFECT_POLICY,
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
        "current_dependency_boundary_state": candidate.get("current_dependency_boundary_state"),
        "real_human_decision_recorded_by_dependency_boundary": False,
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
        "requires_prior_generator_candidate_patch_skeleton": True,
        "requires_prior_generator_candidate_patch_file_set": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_dependency_boundary_request(action: str) -> dict[str, Any]:
    """Classify whether an action is allowed by this design-only dependency_boundary."""

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
        "dependency_boundary",
        "sections",
        "declarations",
    )
    allowed_now = any(term in lowered for term in safe_terms) and not any(
        term in lowered for term in unsafe_terms
    )
    return {
        "allowed_now": allowed_now,
        "permitted_output": "generator_candidate_dependency_boundary_schema" if allowed_now else None,
        "current_dependency_boundary_state": "not_dependency_boundary_defined",
        "real_human_decision_recorded_by_dependency_boundary": False,
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
        "requires_prior_generator_candidate_patch_skeleton": True,
        "requires_prior_generator_candidate_patch_file_set": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
