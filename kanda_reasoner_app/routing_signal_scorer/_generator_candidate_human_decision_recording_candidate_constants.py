# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_human_decision_recording_candidate_constants.py
"""Constants for generator candidate human decision recording candidate contracts."""
from __future__ import annotations

__all__: list[str] = []

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_human_decision_recording_candidate_design_v1"
)

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_SCHEMA_VERSION = (
    "3.32-generator-candidate-human-decision-recording-candidate-design"
)

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_STATUS = (
    "generator_candidate_human_decision_recording_candidate_schema_only_no_decision_write_no_candidate_patch_no_generator_authorization"
)

REQUIRED_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_recording_candidate_schema_only",
        "human_decision_recording_candidate_scope",
        "current_human_decision_recording_candidate_state",
        "current_human_decision_recording_candidate_effect",
        "current_recorded_decision_value",
        "required_prior_milestones",
        "required_future_candidate_evidence",
        "allowed_future_recording_candidate_actions",
        "allowed_candidate_outputs",
        "prohibited_candidate_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "candidate_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_SCOPE = "generator_candidate_human_decision_recording_candidate_schema_only"

ALLOWED_CURRENT_STATES = frozenset(
    {
        "decision_recording_candidate_not_created",
        "awaiting_explicit_human_decision_recording_candidate_patch",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "generator_candidate_human_decision_recording_boundary_frozen",
        "generator_candidate_human_decision_record_frozen",
        "generator_candidate_human_decision_gate_frozen",
        "generator_candidate_preparation_closure_shield_frozen",
        "generator_candidate_review_bundle_frozen",
        "generator_candidate_side_effect_boundary_frozen",
        "generator_candidate_dependency_boundary_frozen",
        "generator_candidate_patch_file_set_frozen",
        "generator_candidate_patch_skeleton_frozen",
        "generator_candidate_patch_envelope_frozen",
        "generator_candidate_patch_preflight_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_FUTURE_CANDIDATE_EVIDENCE = frozenset(
    {
        "explicit_human_decision_text",
        "explicit_human_confirmation_to_prepare_recording_candidate",
        "explicit_non_runtime_scope_acknowledged",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
        "referenced_human_decision_recording_boundary_freeze_id",
        "referenced_human_decision_record_freeze_id",
        "referenced_human_decision_gate_freeze_id",
        "referenced_preparation_closure_freeze_id",
        "candidate_patch_design_only_scope_acknowledged",
        "decision_recording_candidate_has_no_write_effect_acknowledged",
        "generator_non_authorization_acknowledged",
        "artifact_io_non_goals_acknowledged",
        "source_scanning_non_goals_acknowledged",
        "dependency_non_goals_acknowledged",
        "side_effect_non_goals_acknowledged",
        "runtime_router_non_goals_acknowledged",
        "rollback_or_stop_condition_acknowledged",
    }
)

ALLOWED_FUTURE_RECORDING_CANDIDATE_ACTIONS = frozenset(
    {
        "prepare_decision_recording_candidate_for_review_only",
        "reject_decision_recording_candidate",
        "defer_decision_recording_candidate",
        "request_more_freeze_context",
        "request_more_architectural_review",
        "stop_before_decision_recording_candidate",
    }
)

REQUIRED_ALLOWED_CANDIDATE_OUTPUTS = frozenset(
    {
        "human_decision_recording_candidate_schema",
        "future_recording_candidate_evidence_checklist",
        "allowed_future_recording_candidate_actions",
        "current_not_recorded_notice",
        "current_candidate_not_created_notice",
        "decision_scope_requirements",
        "candidate_patch_stop_conditions",
        "no_real_human_decision_recorded",
        "no_decision_write_performed",
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

REQUIRED_PROHIBITED_CANDIDATE_OUTPUTS = frozenset(
    {
        "recorded_human_decision",
        "decision_write",
        "decision_recording_candidate_patch",
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
        "human_decision_write_enabled",
        "human_decision_recording_candidate_creation_enabled",
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

FORBIDDEN_FIELDS = REQUIRED_PROHIBITED_CANDIDATE_OUTPUTS.union(
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
        "route_decision",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "recording_candidate_does_not_record_real_human_decision",
        "recording_candidate_does_not_write_human_decision",
        "recording_candidate_does_not_create_recording_patch",
        "recording_candidate_does_not_infer_human_approval",
        "recording_candidate_does_not_approve_candidate_patch",
        "recording_candidate_does_not_create_candidate_patch",
        "recording_candidate_does_not_authorize_candidate_patch",
        "recording_candidate_does_not_authorize_generator",
        "recording_candidate_does_not_authorize_dependencies",
        "recording_candidate_does_not_authorize_side_effects",
        "recording_candidate_does_not_authorize_artifact_generation",
        "recording_candidate_does_not_authorize_artifact_reading",
        "recording_candidate_does_not_authorize_artifact_writing",
        "recording_candidate_does_not_authorize_source_scanning",
        "recording_candidate_does_not_authorize_raw_text_materialization",
        "recording_candidate_does_not_authorize_embedding_generation",
        "recording_candidate_does_not_authorize_vector_generation",
        "recording_candidate_does_not_authorize_provider_execution",
        "recording_candidate_does_not_authorize_runtime_semantic_enablement",
        "recording_candidate_does_not_authorize_router_authority",
        "recording_candidate_does_not_write_freeze_memory",
        "recording_candidate_does_not_auto_load_prompts",
    }
)

REQUIRED_CANDIDATE_EFFECT_POLICY = frozenset(
    {
        "schema_only_candidate_has_no_decision_effect",
        "not_recorded_value_has_no_decision_effect",
        "decision_recording_candidate_not_created_has_no_patch_effect",
        "future_recording_candidate_requires_separate_governed_patch",
        "future_recording_candidate_may_only_prepare_review_schema",
        "future_recording_candidate_does_not_write_decision",
        "future_approval_value_requires_separate_human_decision_recording_patch",
        "future_candidate_patch_requires_separate_governed_patch_after_recorded_decision",
        "future_artifact_generation_requires_separate_governed_generation_patch",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_request_attempts_to_record_human_decision_now",
        "stop_if_request_attempts_to_write_decision_now",
        "stop_if_request_attempts_to_infer_approval_from_continue",
        "stop_if_request_attempts_to_create_candidate_patch_now",
        "stop_if_request_attempts_to_authorize_generator_now",
        "stop_if_request_attempts_to_install_dependencies_now",
        "stop_if_request_attempts_to_authorize_side_effects_now",
        "stop_if_request_attempts_to_generate_artifacts_now",
        "stop_if_request_attempts_to_scan_sources_now",
        "stop_if_request_attempts_to_enable_runtime_or_router_now",
    }
)

TRIGGER_TERMS_REQUIRING_FUTURE_PATCH = frozenset(
    {
        "approve",
        "record decision",
        "write decision",
        "human approved",
        "accepted",
        "create candidate patch",
        "candidate patch",
        "authorize",
        "generate",
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
        "recording candidate",
        "candidate shape",
        "evidence checklist",
        "review only",
        "show checklist",
    }
)
