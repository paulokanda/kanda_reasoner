# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_human_decision_recording_finalization_closure_shield_constants.py
"""Constants for generator candidate human decision recording finalization closure shields."""
from __future__ import annotations

__all__: list[str] = []

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_human_decision_recording_finalization_closure_shield_v1"
)

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_SCHEMA_VERSION = (
    "3.36-generator-candidate-human-decision-recording-finalization-closure-shield"
)

GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_STATUS = (
    "generator_candidate_human_decision_recording_finalization_closure_shield_schema_only_no_decision_write_no_candidate_patch_no_generator_authorization"
)

REQUIRED_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_recording_finalization_closure_shield_schema_only",
        "human_decision_recording_finalization_closure_shield_scope",
        "current_human_decision_recording_finalization_closure_shield_state",
        "current_human_decision_recording_finalization_closure_shield_effect",
        "current_recorded_decision_value",
        "required_prior_milestones",
        "required_future_closure_evidence",
        "allowed_future_closure_actions",
        "allowed_closure_outputs",
        "prohibited_closure_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "closure_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_SCOPE = "generator_candidate_human_decision_recording_finalization_closure_shield_schema_only"

ALLOWED_CURRENT_STATES = frozenset(
    {
        "decision_recording_finalization_closure_shield_closed",
        "awaiting_explicit_human_decision_recording_patch",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "generator_candidate_human_decision_recording_finalization_frozen",
        "generator_candidate_human_decision_recording_commit_frozen",
        "generator_candidate_human_decision_recording_implementation_frozen",
        "generator_candidate_human_decision_recording_candidate_frozen",
        "generator_candidate_human_decision_recording_boundary_frozen",
        "generator_candidate_human_decision_record_frozen",
        "generator_candidate_human_decision_gate_frozen",
        "generator_candidate_preparation_closure_shield_frozen",
        "generator_candidate_review_bundle_frozen",
        "generator_candidate_side_effect_boundary_frozen",
        "generator_candidate_dependency_boundary_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_FUTURE_CLOSURE_EVIDENCE = frozenset(
    {
        "explicit_human_decision_text",
        "explicit_human_confirmation_to_open_future_decision_recording_patch",
        "explicit_non_runtime_scope_acknowledged",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
        "referenced_human_decision_recording_finalization_freeze_id",
        "referenced_human_decision_recording_commit_freeze_id",
        "referenced_human_decision_recording_implementation_freeze_id",
        "referenced_human_decision_recording_boundary_freeze_id",
        "referenced_human_decision_record_freeze_id",
        "referenced_human_decision_gate_freeze_id",
        "referenced_preparation_closure_freeze_id",
        "closure_shield_has_no_write_effect_acknowledged",
        "generator_non_authorization_acknowledged",
        "artifact_io_non_goals_acknowledged",
        "source_scanning_non_goals_acknowledged",
        "dependency_non_goals_acknowledged",
        "side_effect_non_goals_acknowledged",
        "runtime_router_non_goals_acknowledged",
        "rollback_or_stop_condition_acknowledged",
    }
)

ALLOWED_FUTURE_CLOSURE_ACTIONS = frozenset(
    {
        "review_finalization_closure_shield_only",
        "reject_future_decision_recording_patch",
        "defer_future_decision_recording_patch",
        "request_more_freeze_context",
        "request_more_architectural_review",
        "stop_before_decision_recording_patch",
    }
)

REQUIRED_ALLOWED_CLOSURE_OUTPUTS = frozenset(
    {
        "human_decision_recording_finalization_closure_shield_schema",
        "future_recording_patch_evidence_checklist",
        "allowed_future_closure_actions",
        "current_not_recorded_notice",
        "current_closure_shield_closed_notice",
        "decision_scope_requirements",
        "closure_stop_conditions",
        "no_real_human_decision_recorded",
        "no_decision_write_performed",
        "no_decision_committed",
        "no_decision_finalized",
        "no_recording_patch_created",
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

REQUIRED_PROHIBITED_CLOSURE_OUTPUTS = frozenset(
    {
        "recorded_human_decision",
        "decision_write",
        "decision_commit",
        "decision_finalization",
        "decision_recording_patch",
        "decision_recording_write_function",
        "inferred_human_approval",
        "candidate_patch_approval",
        "candidate_patch_authorization",
        "generator_candidate_patch",
        "generator_commit",
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
        "human_decision_commit_enabled",
        "human_decision_finalization_enabled",
        "human_decision_recording_patch_enabled",
        "human_decision_recording_write_function_enabled",
        "human_approval_inference_enabled",
        "candidate_patch_approval_enabled",
        "generator_candidate_patch_creation_enabled",
        "generator_candidate_patch_authorization_enabled",
        "generator_commit_enabled",
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

FORBIDDEN_FIELDS = REQUIRED_PROHIBITED_CLOSURE_OUTPUTS.union(
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
        "closure_shield_does_not_record_real_human_decision",
        "closure_shield_does_not_write_human_decision",
        "closure_shield_does_not_commit_human_decision",
        "closure_shield_does_not_finalize_human_decision",
        "closure_shield_does_not_create_recording_patch",
        "closure_shield_does_not_enable_write_function",
        "closure_shield_does_not_infer_human_approval",
        "closure_shield_does_not_approve_candidate_patch",
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
        "closure_shield_does_not_authorize_embeddings",
        "closure_shield_does_not_authorize_vectors",
        "closure_shield_does_not_authorize_providers",
        "closure_shield_does_not_authorize_runtime_scoring",
        "closure_shield_does_not_authorize_router_authority",
        "closure_shield_does_not_write_freeze_memory",
        "closure_shield_does_not_auto_load_prompts",
    }
)

REQUIRED_CLOSURE_EFFECT_POLICY = frozenset(
    {
        "schema_has_no_runtime_effect",
        "schema_has_no_decision_write_effect",
        "schema_has_no_candidate_patch_effect",
        "schema_has_no_generation_effect",
        "schema_has_no_router_effect",
        "continue_is_not_approval",
        "freeze_validation_is_not_approval",
        "current_chain_closed_until_explicit_future_governed_patch",
        "future_decision_recording_requires_separate_governed_patch",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "requested_real_decision_recording",
        "requested_candidate_patch_authorization",
        "requested_generator_authorization",
        "requested_artifact_generation",
        "requested_artifact_io",
        "requested_source_scanning",
        "requested_embeddings_or_vectors",
        "requested_provider_execution",
        "requested_runtime_or_router_effect",
        "missing_full_freeze_context_for_frozen_behavior",
        "cross_box_modification_required",
    }
)

TRIGGER_TERMS_REQUIRING_FUTURE_PATCH = frozenset(
    {
        "approve",
        "record decision",
        "write decision",
        "finalize decision",
        "commit decision",
        "open decision patch",
        "create candidate patch",
        "authorize generator",
        "generate artifact",
        "write artifact",
        "read artifact",
        "scan source",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "router authority",
        "may proceed",
    }
)

SCHEMA_TALK_TERMS = frozenset(
    {
        "schema",
        "design",
        "shield",
        "closure",
        "finalization closure",
        "decision recording closure",
        "evidence checklist",
        "review only",
        "show checklist",
    }
)
