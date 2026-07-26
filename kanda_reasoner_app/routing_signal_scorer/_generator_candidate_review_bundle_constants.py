# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_review_bundle_constants.py
"""Constants for generator candidate review bundle contracts."""
from __future__ import annotations

__all__: list[str] = []

GENERATOR_CANDIDATE_REVIEW_BUNDLE_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_review_bundle_design_v1"
)

GENERATOR_CANDIDATE_REVIEW_BUNDLE_SCHEMA_VERSION = (
    "3.27-generator-candidate-review-bundle-design"
)

GENERATOR_CANDIDATE_REVIEW_BUNDLE_STATUS = (
    "generator_candidate_review_bundle_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_REVIEW_BUNDLE_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_review_bundle_only",
        "review_bundle_scope",
        "current_review_bundle_state",
        "current_review_bundle_effect",
        "required_prior_milestones",
        "required_review_bundle_sections",
        "required_bundle_inputs",
        "required_candidate_patch_declarations",
        "required_boundary_declarations",
        "required_validation_declarations",
        "allowed_future_review_bundle_outcomes",
        "allowed_review_bundle_outputs",
        "prohibited_review_bundle_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "review_bundle_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_REVIEW_BUNDLE_SCOPE = "generator_candidate_review_bundle_only"

ALLOWED_CURRENT_REVIEW_BUNDLE_STATES = frozenset(
    {
        "not_review_bundle_defined",
        "review_bundle_schema_only",
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
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_REVIEW_BUNDLE_SECTIONS = frozenset(
    {
        "candidate_patch_identity",
        "candidate_patch_scope",
        "candidate_patch_non_goals",
        "candidate_patch_file_set_summary",
        "candidate_patch_dependency_boundary_summary",
        "candidate_patch_side_effect_boundary_summary",
        "candidate_patch_preflight_summary",
        "candidate_patch_envelope_summary",
        "candidate_patch_skeleton_summary",
        "candidate_patch_human_decision_summary",
        "candidate_patch_validation_summary",
        "candidate_patch_public_contract_boundary",
        "candidate_patch_router_authority_boundary",
        "candidate_patch_runtime_boundary",
        "candidate_patch_artifact_lifecycle_boundary",
        "candidate_patch_source_boundary",
        "candidate_patch_raw_text_boundary",
        "candidate_patch_kbsc_shielding_plan",
        "candidate_patch_freeze_plan",
        "candidate_patch_stop_conditions",
    }
)

REQUIRED_BUNDLE_INPUTS = frozenset(
    {
        "frozen_proposal_schema_reference",
        "frozen_proposal_review_reference",
        "frozen_preflight_reference",
        "frozen_envelope_reference",
        "frozen_skeleton_reference",
        "frozen_file_set_reference",
        "frozen_dependency_boundary_reference",
        "frozen_side_effect_boundary_reference",
        "recorded_human_decision_reference_required_for_future_patch",
        "kbsc_shielding_evidence_required_for_future_patch",
        "validation_evidence_required_for_future_patch",
        "freeze_hint_required_for_future_patch",
    }
)

REQUIRED_CANDIDATE_PATCH_DECLARATIONS = frozenset(
    {
        "candidate_patch_is_separate_future_patch",
        "candidate_patch_is_not_created_by_this_review_bundle",
        "candidate_patch_is_not_authorized_by_this_review_bundle",
        "candidate_patch_requires_recorded_human_decision_reference",
        "candidate_patch_requires_preflight_reference",
        "candidate_patch_requires_envelope_reference",
        "candidate_patch_requires_skeleton_reference",
        "candidate_patch_requires_file_set_reference",
        "candidate_patch_requires_dependency_boundary_reference",
        "candidate_patch_requires_side_effect_boundary_reference",
        "candidate_patch_requires_explicit_touched_paths",
        "candidate_patch_requires_no_public_runtime_export_by_default",
        "candidate_patch_requires_no_router_authority_by_default",
        "candidate_patch_requires_kbsc_before_merge",
    }
)

REQUIRED_BOUNDARY_DECLARATIONS = frozenset(
    {
        "review_bundle_does_not_create_candidate_patch",
        "review_bundle_does_not_authorize_candidate_patch",
        "review_bundle_does_not_authorize_generator",
        "review_bundle_does_not_authorize_dependencies",
        "review_bundle_does_not_authorize_side_effects",
        "review_bundle_does_not_authorize_artifact_generation",
        "review_bundle_does_not_authorize_artifact_reading",
        "review_bundle_does_not_authorize_artifact_writing",
        "review_bundle_does_not_authorize_source_scanning",
        "review_bundle_does_not_authorize_raw_text_materialization",
        "review_bundle_does_not_authorize_embedding_generation",
        "review_bundle_does_not_authorize_vector_generation",
        "review_bundle_does_not_authorize_provider_execution",
        "review_bundle_does_not_authorize_runtime_semantic_enablement",
        "review_bundle_does_not_authorize_router_authority",
        "review_bundle_does_not_write_freeze_memory",
        "review_bundle_does_not_auto_load_prompts",
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

ALLOWED_FUTURE_REVIEW_BUNDLE_OUTCOMES = frozenset(
    {
        "reject_generator_candidate_patch_readiness",
        "defer_generator_candidate_patch_readiness",
        "request_more_preflight_evidence",
        "request_more_human_decision_evidence",
        "request_more_boundary_evidence",
        "permit_separate_governed_generator_candidate_patch_design_only",
    }
)

REQUIRED_ALLOWED_REVIEW_BUNDLE_OUTPUTS = frozenset(
    {
        "generator_candidate_review_bundle_schema",
        "candidate_patch_readiness_checklist",
        "candidate_patch_required_inputs",
        "candidate_patch_required_boundaries",
        "candidate_patch_required_validation_summary",
        "candidate_patch_stop_conditions",
        "future_review_bundle_outcome_vocabulary",
        "review_bundle_effect_policy_summary",
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

REQUIRED_PROHIBITED_REVIEW_BUNDLE_OUTPUTS = frozenset(
    {
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generator_implementation",
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
        "generator_candidate_patch_creation_enabled",
        "generator_candidate_patch_authorization_enabled",
        "generator_implementation_enabled",
        "dependency_install_enabled",
        "side_effect_authorization_enabled",
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_reading_enabled",
        "source_scanning_enabled",
        "raw_text_materialization_enabled",
        "embedding_generation_enabled",
        "vector_index_generation_enabled",
        "provider_execution_enabled",
        "semantic_runtime_enabled",
        "router_authority_enabled",
        "startup_generation_enabled",
        "background_generation_enabled",
        "public_runtime_export_enabled",
        "freeze_memory_write_enabled",
        "prompt_auto_loading_enabled",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "review_bundle_cannot_record_real_human_decision",
        "review_bundle_cannot_create_candidate_patch",
        "review_bundle_cannot_authorize_candidate_patch",
        "review_bundle_cannot_authorize_generator_implementation",
        "review_bundle_cannot_authorize_dependency_install",
        "review_bundle_cannot_authorize_side_effects",
        "review_bundle_cannot_authorize_artifact_generation",
        "review_bundle_cannot_authorize_artifact_io",
        "review_bundle_cannot_authorize_source_scanning",
        "review_bundle_cannot_authorize_raw_text_materialization",
        "review_bundle_cannot_authorize_runtime_semantic_scoring",
        "review_bundle_cannot_authorize_router_changes",
        "review_bundle_cannot_write_project_freeze_memory",
        "review_bundle_cannot_decide_may_proceed_now",
    }
)

REQUIRED_REVIEW_BUNDLE_EFFECT_POLICY = frozenset(
    {
        "schema_only_current_effect_is_no_effect",
        "review_bundle_output_is_review_readiness_metadata_only",
        "review_bundle_output_has_no_runtime_effect",
        "review_bundle_output_has_no_router_effect",
        "review_bundle_output_has_no_freeze_memory_effect",
        "review_bundle_output_has_no_candidate_patch_authority",
        "review_bundle_output_has_no_generation_authority",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_real_human_decision_would_be_recorded",
        "stop_if_candidate_patch_would_be_created",
        "stop_if_candidate_patch_would_be_authorized",
        "stop_if_generator_would_be_implemented",
        "stop_if_dependency_would_be_installed",
        "stop_if_side_effect_would_be_authorized",
        "stop_if_artifact_would_be_generated_written_or_read",
        "stop_if_source_would_be_scanned",
        "stop_if_raw_text_would_be_materialized",
        "stop_if_embedding_or_vector_would_be_generated",
        "stop_if_provider_or_model_would_be_loaded",
        "stop_if_runtime_or_startup_behavior_would_change",
        "stop_if_router_authority_would_change",
        "stop_if_public_runtime_contract_would_change",
        "stop_if_other_box_logic_would_be_modified",
    }
)

FORBIDDEN_REVIEW_BUNDLE_FIELDS = frozenset(
    {
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generator_implementation",
        "artifact_payload",
        "artifact_output_path",
        "artifact_input_path",
        "source_text",
        "raw_prompt_text",
        "raw_freeze_text",
        "embedding_values",
        "vector_values",
        "provider_name",
        "model_name",
        "runtime_route_signal",
        "may_proceed_now",
    }
)
