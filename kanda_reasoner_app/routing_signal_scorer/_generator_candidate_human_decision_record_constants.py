# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_human_decision_record_constants.py
"""Constants for generator candidate human decision record contracts."""
from __future__ import annotations

__all__: list[str] = []

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_human_decision_record_design_v1"
)

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION = (
    "3.30-generator-candidate-human-decision-record-design"
)

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS = (
    "generator_candidate_human_decision_record_schema_only_no_decision_recorded_no_candidate_patch_no_generator_authorization"
)

REQUIRED_HUMAN_DECISION_RECORD_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_record_schema_only",
        "human_decision_record_scope",
        "current_human_decision_record_state",
        "current_human_decision_record_effect",
        "current_recorded_decision_value",
        "required_prior_milestones",
        "required_future_recording_inputs",
        "allowed_future_recorded_decision_values",
        "allowed_record_outputs",
        "prohibited_record_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "record_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_HUMAN_DECISION_RECORD_SCOPE = "generator_candidate_human_decision_record_schema_only"

ALLOWED_CURRENT_HUMAN_DECISION_RECORD_STATES = frozenset(
    {
        "human_decision_record_not_recorded",
        "awaiting_explicit_human_decision_recording_patch",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "generator_candidate_human_decision_gate_frozen",
        "generator_candidate_preparation_closure_shield_frozen",
        "generator_candidate_review_bundle_frozen",
        "generator_candidate_side_effect_boundary_frozen",
        "generator_candidate_dependency_boundary_frozen",
        "generator_candidate_patch_file_set_frozen",
        "generator_candidate_patch_skeleton_frozen",
        "generator_candidate_patch_envelope_frozen",
        "generator_candidate_patch_preflight_frozen",
        "actual_human_decision_recording_boundary_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_FUTURE_RECORDING_INPUTS = frozenset(
    {
        "explicit_human_decision_text",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
        "referenced_human_decision_gate_freeze_id",
        "referenced_preparation_closure_freeze_id",
        "referenced_review_bundle_freeze_id",
        "candidate_patch_design_only_scope_acknowledged",
        "generator_non_authorization_acknowledged",
        "artifact_io_non_goals_acknowledged",
        "source_scanning_non_goals_acknowledged",
        "dependency_non_goals_acknowledged",
        "side_effect_non_goals_acknowledged",
        "runtime_router_non_goals_acknowledged",
        "rollback_or_stop_condition_acknowledged",
    }
)

ALLOWED_FUTURE_RECORDED_DECISION_VALUES = frozenset(
    {
        "not_recorded",
        "approve_candidate_patch_design_only",
        "reject_candidate_patch_design",
        "defer_candidate_patch_design",
        "request_more_freeze_context",
        "request_more_architectural_review",
        "stop_after_preparation_closure",
    }
)

REQUIRED_ALLOWED_RECORD_OUTPUTS = frozenset(
    {
        "human_decision_record_schema",
        "future_recording_input_checklist",
        "allowed_future_recorded_decision_values",
        "current_not_recorded_notice",
        "decision_scope_requirements",
        "candidate_patch_stop_conditions",
        "no_real_human_decision_recorded",
        "no_approval_inferred_from_preparation_chain",
        "no_candidate_patch_created",
        "no_candidate_patch_authorized",
        "no_generator_authorized",
        "no_dependency_install_authorized",
        "no_side_effect_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_RECORD_OUTPUTS = frozenset(
    {
        "recorded_human_decision",
        "inferred_human_approval",
        "candidate_patch_approval",
        "candidate_patch_authorization",
        "generator_candidate_patch",
        "generator_implementation",
        "generator_authorization",
        "dependency_install_request",
        "side_effect_authorization",
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
        "human_approval_inference_enabled",
        "candidate_patch_approval_enabled",
        "generator_candidate_patch_creation_enabled",
        "generator_candidate_patch_authorization_enabled",
        "generator_implementation_enabled",
        "dependency_install_enabled",
        "third_party_dependency_enabled",
        "side_effect_authorization_enabled",
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

FORBIDDEN_RECORD_FIELDS = REQUIRED_PROHIBITED_RECORD_OUTPUTS.union(
    {
        "actual_human_decision",
        "approved_by_human",
        "approval_effect",
        "decision_runtime_effect",
        "candidate_patch_payload",
        "artifact_payload",
        "raw_prompt_text",
        "raw_user_query_text",
        "raw_freeze_entry_text",
        "source_text",
        "embedding_values",
        "vector_values",
        "provider_config",
        "model_config",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "record_design_does_not_record_real_human_decision",
        "record_design_does_not_infer_human_approval",
        "record_design_does_not_approve_candidate_patch",
        "record_design_does_not_create_candidate_patch",
        "record_design_does_not_authorize_candidate_patch",
        "record_design_does_not_authorize_generator",
        "record_design_does_not_authorize_dependencies",
        "record_design_does_not_authorize_side_effects",
        "record_design_does_not_authorize_artifact_generation",
        "record_design_does_not_authorize_artifact_reading",
        "record_design_does_not_authorize_artifact_writing",
        "record_design_does_not_authorize_source_scanning",
        "record_design_does_not_authorize_raw_text_materialization",
        "record_design_does_not_authorize_embedding_generation",
        "record_design_does_not_authorize_vector_generation",
        "record_design_does_not_authorize_provider_execution",
        "record_design_does_not_authorize_runtime_semantic_enablement",
        "record_design_does_not_authorize_router_authority",
        "record_design_does_not_write_freeze_memory",
        "record_design_does_not_auto_load_prompts",
    }
)

REQUIRED_RECORD_EFFECT_POLICY = frozenset(
    {
        "schema_only_record_has_no_decision_effect",
        "not_recorded_value_has_no_decision_effect",
        "future_approve_candidate_patch_design_only_allows_only_separate_candidate_patch_design_review",
        "future_approve_candidate_patch_design_only_does_not_authorize_generation",
        "future_reject_value_blocks_candidate_patch_until_new_decision",
        "future_defer_value_blocks_candidate_patch_until_new_decision",
        "future_more_context_value_blocks_candidate_patch_until_context_is_loaded",
        "any_future_recorded_value_requires_separate_governed_recording_patch",
        "any_future_candidate_patch_requires_separate_governed_patch",
        "any_future_generation_requires_separate_governed_patch",
        "any_request_to_use_record_as_runtime_authority_is_blocked",
        "any_request_to_use_record_as_router_authority_is_blocked",
        "any_request_to_use_record_as_artifact_authority_is_blocked",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_explicit_human_decision_is_missing",
        "stop_if_decision_scope_is_ambiguous",
        "stop_if_full_freeze_context_is_required_but_not_loaded",
        "stop_if_decision_recording_is_requested_in_this_schema_patch",
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

TRIGGER_TERMS_REQUIRING_FUTURE_PATCH = frozenset(
    {
        "approve",
        "approved",
        "record decision",
        "actual decision",
        "human decided",
        "permit",
        "authorize",
        "candidate patch now",
        "create candidate patch",
        "generate",
        "generation",
        "artifact",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "startup",
        "background",
        "router",
        "may proceed",
    }
)

SCHEMA_TALK_TERMS = frozenset(
    {
        "schema",
        "design",
        "record shape",
        "decision values",
        "evidence checklist",
        "review only",
        "show checklist",
    }
)
