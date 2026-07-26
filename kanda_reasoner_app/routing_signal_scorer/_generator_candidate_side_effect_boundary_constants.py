# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_side_effect_boundary_constants.py
"""Constants for generator candidate side-effect boundary contracts."""
from __future__ import annotations

__all__: list[str] = []

GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_side_effect_boundary_design_v1"
)

GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_SCHEMA_VERSION = (
    "3.26-generator-candidate-side-effect-boundary-design"
)

GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_STATUS = (
    "generator_candidate_side_effect_boundary_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_SIDE_EFFECT_BOUNDARY_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_side_effect_boundary_only",
        "side_effect_boundary_scope",
        "current_side_effect_boundary_state",
        "current_side_effect_boundary_effect",
        "required_prior_milestones",
        "required_side_effect_boundary_sections",
        "required_candidate_patch_declarations",
        "required_boundary_declarations",
        "required_validation_declarations",
        "allowed_future_side_effect_boundary_outcomes",
        "allowed_side_effect_boundary_outputs",
        "prohibited_side_effect_boundary_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "side_effect_boundary_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_SIDE_EFFECT_BOUNDARY_SCOPE = "generator_candidate_side_effect_boundary_only"

ALLOWED_CURRENT_SIDE_EFFECT_BOUNDARY_STATES = frozenset(
    {
        "not_side_effect_boundary_defined",
        "side_effect_boundary_schema_only",
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
        "generator_candidate_dependency_boundary_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_SIDE_EFFECT_BOUNDARY_SECTIONS = frozenset(
    {
        "candidate_patch_identity",
        "candidate_patch_scope",
        "candidate_patch_non_goals",
        "candidate_patch_touched_paths",
        "candidate_patch_allowed_side_effect_boundary",
        "candidate_patch_forbidden_side_effect_boundary",
        "candidate_patch_standard_library_only_default",
        "candidate_patch_forbidden_side_effect_classes",
        "candidate_patch_side_effect_exception_process",
        "candidate_patch_forbidden_write_operations",
        "candidate_patch_forbidden_read_operations",
        "candidate_patch_forbidden_scan_operations",
        "candidate_patch_side-effect_budget",
        "candidate_patch_standard_library_only_default",
        "candidate_patch_forbidden_side_effect_classes",
        "candidate_patch_side_effect_exception_process",
        "candidate_patch_forbidden_write_operations",
        "candidate_patch_forbidden_read_operations",
        "candidate_patch_forbidden_scan_operations",
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
        "candidate_patch_is_not_created_by_this_side_effect_boundary",
        "candidate_patch_is_not_authorized_by_this_side_effect_boundary",
        "candidate_patch_requires_recorded_human_decision_reference",
        "candidate_patch_requires_preflight_reference",
        "candidate_patch_requires_review_evidence_reference",
        "candidate_patch_requires_explicit_touched_paths",
        "candidate_patch_requires_declared_allowed_side_effects",
        "candidate_patch_requires_declared_forbidden_side_effects",
        "candidate_patch_requires_no_side_effects_by_default",
        "candidate_patch_requires_no_public_runtime_export_by_default",
        "candidate_patch_requires_no_router_authority_by_default",
        "candidate_patch_requires_kbsc_before_merge",
    }
)

REQUIRED_BOUNDARY_DECLARATIONS = frozenset(
    {
        "standard_library_only_by_default",
        "no_side_effect_authorization_in_side_effect_boundary",
        "no_third_party_side_effect_addition_in_side_effect_boundary",
        "no_generation_in_side_effect_boundary",
        "no_artifact_write_in_side_effect_boundary",
        "no_artifact_read_in_side_effect_boundary",
        "no_source_scan_in_side_effect_boundary",
        "no_raw_text_materialization_in_side_effect_boundary",
        "no_embedding_generation_in_side_effect_boundary",
        "no_vector_materialization_in_side_effect_boundary",
        "no_provider_execution_in_side_effect_boundary",
        "no_network_access_in_side_effect_boundary",
        "no_credential_loading_in_side_effect_boundary",
        "no_model_loading_in_side_effect_boundary",
        "no_embedding_library_dependency_in_side_effect_boundary",
        "no_vector_store_dependency_in_side_effect_boundary",
        "no_ml_runtime_dependency_in_side_effect_boundary",
        "no_runtime_semantic_enablement_in_side_effect_boundary",
        "no_router_authority_change_in_side_effect_boundary",
        "no_prompt_auto_loading_in_side_effect_boundary",
        "no_freeze_memory_write_from_side_effect_boundary_output",
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

ALLOWED_FUTURE_SIDE_EFFECT_BOUNDARY_OUTCOMES = frozenset(
    {
        "reject_candidate_patch_side_effect_boundary",
        "defer_candidate_patch_side_effect_boundary",
        "request_more_preflight_evidence",
        "request_more_human_decision_evidence",
        "permit_separate_governed_generator_candidate_patch_design_only",
    }
)

REQUIRED_ALLOWED_SIDE_EFFECT_BOUNDARY_OUTPUTS = frozenset(
    {
        "candidate_patch_side_effect_boundary_schema",
        "candidate_patch_allowed_side_effect_boundary",
        "candidate_patch_forbidden_side_effect_boundary",
        "candidate_patch_standard_library_only_default",
        "candidate_patch_forbidden_side_effect_classes",
        "candidate_patch_side_effect_exception_process",
        "candidate_patch_forbidden_write_operations",
        "candidate_patch_forbidden_read_operations",
        "candidate_patch_forbidden_scan_operations",
        "candidate_patch_required_side_effect_boundary",
        "candidate_patch_side_effect_boundary_schema",
        "candidate_patch_allowed_side_effects",
        "candidate_patch_forbidden_side_effects",
        "candidate_patch_required_sections",
        "candidate_patch_allowed_files",
        "candidate_patch_forbidden_files",
        "candidate_patch_required_declarations",
        "candidate_patch_boundary_declarations",
        "candidate_patch_validation_declarations",
        "future_side_effect_boundary_outcome_vocabulary",
        "side_effect_boundary_effect_policy_summary",
        "stop_conditions_list",
        "side_effect_boundary_evidence_only",
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

REQUIRED_PROHIBITED_SIDE_EFFECT_BOUNDARY_OUTPUTS = frozenset(
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
        "artifact_write_plan",
        "artifact_read_plan",
        "source_scan_plan",
        "raw_text_materialization_plan",
        "vector_index_write_plan",
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
        "real_human_decision_recorded_by_side_effect_boundary",
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
        "artifact_write_enabled",
        "artifact_read_enabled",
        "source_scan_enabled",
        "raw_text_materialization_enabled",
        "vector_index_write_enabled",
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
        "side_effect_boundary_does_not_decide_routes",
        "side_effect_boundary_does_not_decide_required_prompts",
        "side_effect_boundary_does_not_decide_missing_context",
        "side_effect_boundary_does_not_decide_missing_behavior",
        "side_effect_boundary_does_not_decide_may_proceed_now",
        "side_effect_boundary_does_not_load_prompts",
        "side_effect_boundary_does_not_write_freeze_memory",
        "side_effect_boundary_does_not_authorize_generation",
        "side_effect_boundary_does_not_create_candidate_patch",
    }
)

REQUIRED_SIDE_EFFECT_BOUNDARY_EFFECT_POLICY = frozenset(
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

FORBIDDEN_SIDE_EFFECT_BOUNDARY_FIELDS = REQUIRED_PROHIBITED_SIDE_EFFECT_BOUNDARY_OUTPUTS
