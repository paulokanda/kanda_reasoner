# project-path: kanda_reasoner_app/routing_signal_scorer/_actual_human_decision_record_constants.py
"""Constants for actual human decision record contracts."""
from __future__ import annotations

__all__: list[str] = []

ACTUAL_HUMAN_DECISION_RECORD_FEATURE_ID = (
    "routing_signal_scorer_v3_actual_human_decision_record_design_v1"
)

ACTUAL_HUMAN_DECISION_RECORD_SCHEMA_VERSION = (
    "3.17-actual-human-decision-record-design"
)

ACTUAL_HUMAN_DECISION_RECORD_STATUS = (
    "actual_decision_record_schema_only_no_decision_write_no_generator_authorization"
)

REQUIRED_RECORD_FIELDS = frozenset(
    {
        "record_id",
        "schema_version",
        "record_status",
        "declared_actual_human_decision_record_schema_only",
        "decision_record_scope",
        "decision_value",
        "decision_record_effect",
        "required_prior_milestones",
        "allowed_future_recorded_decision_values",
        "required_human_attestation_sections",
        "required_written_evidence_before_recording_real_decision",
        "required_written_evidence_before_any_future_candidate",
        "allowed_record_outputs",
        "prohibited_record_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "record_effect_policy",
        "escalation_rules",
    }
)

REQUIRED_RECORD_SCOPE = "actual_human_decision_record_schema_only"

ALLOWED_RECORD_STATUSES = frozenset(
    {
        "schema_only",
        "awaiting_explicit_human_decision_recording_patch",
        "decision_recording_not_implemented",
        "deferred",
        "rejected",
    }
)

ALLOWED_FUTURE_RECORDED_DECISION_VALUES = frozenset(
    {
        "not_recorded",
        "defer_generator_candidate_proposal",
        "reject_generator_candidate_proposal",
        "permit_separate_generator_candidate_proposal_review_only",
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
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_HUMAN_ATTESTATION_SECTIONS = frozenset(
    {
        "human_actor_role_attestation_placeholder",
        "explicit_decision_phrase_placeholder",
        "review_record_reference",
        "decision_intake_reference",
        "scope_decision_attestation",
        "privacy_redaction_attestation",
        "dependency_budget_attestation",
        "resource_budget_attestation",
        "authority_boundary_attestation",
        "runtime_boundary_attestation",
        "artifact_lifecycle_attestation",
        "validation_matrix_attestation",
        "freeze_plan_attestation",
        "stop_conditions_attestation",
        "final_recorded_decision_placeholder",
    }
)

REQUIRED_WRITTEN_EVIDENCE_BEFORE_RECORDING_REAL_DECISION = frozenset(
    {
        "actual_human_decision_record_design_validation_ok",
        "human_decision_intake_validation_ok",
        "human_architectural_review_record_validation_ok",
        "local_generator_candidate_review_gate_validation_ok",
        "dry_run_artifact_generation_plan_validation_ok",
        "disabled_generation_boundary_validation_ok",
        "v3_closure_shield_validation_ok",
        "explicit_human_decision_recording_patch_requested",
        "human_decision_scope_review_written_evidence",
        "human_decision_privacy_review_written_evidence",
        "human_decision_dependency_review_written_evidence",
        "human_decision_resource_review_written_evidence",
        "human_decision_authority_review_written_evidence",
    }
)

REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE = frozenset(
    {
        "actual_human_decision_record_validation_ok",
        "real_human_decision_recorded_in_separate_frozen_patch",
        "recorded_decision_value_is_not_recorded_or_reject_or_defer_or_permit_review_only",
        "generator_candidate_still_requires_separate_governed_patch",
        "generator_candidate_review_gate_validation_ok",
        "dry_run_plan_validation_ok",
        "disabled_generation_boundary_validation_ok",
        "v3_closure_shield_validation_ok",
        "privacy_review_written_evidence",
        "dependency_review_written_evidence",
        "resource_budget_written_evidence",
        "redaction_review_written_evidence",
        "authority_leakage_review_written_evidence",
    }
)

REQUIRED_ALLOWED_RECORD_OUTPUTS = frozenset(
    {
        "actual_human_decision_record_schema",
        "human_attestation_questionnaire",
        "allowed_future_recorded_decision_values_list",
        "required_evidence_list",
        "record_effect_policy_summary",
        "stop_conditions_list",
        "review_evidence_only",
        "no_real_decision_recorded_by_this_schema",
        "no_generator_candidate_patch_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_RECORD_OUTPUTS = frozenset(
    {
        "real_human_decision_recorded",
        "generator_candidate_patch",
        "generator_candidate_authorization",
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
        "real_human_decision_recorded",
        "decision_write_enabled",
        "generator_candidate_patch_authorized",
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_overwrite_enabled",
        "artifact_reader_enabled",
        "artifact_loading_enabled",
        "source_scanning_enabled",
        "prompt_library_scan_enabled",
        "freeze_entry_scan_enabled",
        "project_source_scan_enabled",
        "runtime_user_query_capture_enabled",
        "raw_text_materialization_enabled",
        "embedding_generation_enabled",
        "embedding_value_materialization_enabled",
        "vector_value_materialization_enabled",
        "vector_index_generation_enabled",
        "provider_execution_enabled",
        "network_access_enabled",
        "credential_loading_enabled",
        "startup_generation_enabled",
        "runtime_generation_enabled",
        "background_generation_enabled",
        "file_watcher_generation_enabled",
        "semantic_runtime_enabled",
        "prompt_router_mutation_enabled",
        "prompt_auto_loading_enabled",
        "may_proceed_generation_enabled",
        "write_freeze_memory_enabled",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "record_is_schema_only",
        "record_is_review_evidence_only",
        "record_design_records_no_real_human_decision",
        "record_design_must_not_authorize_generator_candidate_patch_by_itself",
        "record_design_must_not_generate_artifacts",
        "record_design_must_not_write_artifacts",
        "record_design_must_not_read_artifacts",
        "record_design_must_not_scan_sources",
        "record_design_must_not_materialize_raw_text",
        "record_design_must_not_generate_embeddings",
        "record_design_must_not_materialize_vectors",
        "record_design_must_not_choose_route",
        "record_design_must_not_choose_required_prompts",
        "record_design_must_not_decide_may_proceed",
        "record_design_must_not_load_prompts",
        "record_design_must_not_mutate_router",
        "record_design_must_not_write_freeze_memory",
        "canon_remains_final_authority",
        "future_real_decision_recording_requires_separate_governed_patch",
        "future_generator_candidate_requires_separate_governed_patch_after_recorded_decision",
    }
)

REQUIRED_RECORD_EFFECT_POLICY = frozenset(
    {
        "schema_only_record_has_no_decision_effect",
        "not_recorded_value_has_no_decision_effect",
        "future_defer_value_blocks_generator_candidate_until_new_decision",
        "future_reject_value_blocks_generator_candidate_until_new_decision",
        "future_permit_review_only_value_allows_only_separate_generator_candidate_proposal_review",
        "even_future_permit_review_only_value_does_not_authorize_generation",
        "any_request_to_use_record_as_runtime_authority_is_blocked",
        "any_request_to_use_record_as_router_authority_is_blocked",
        "any_request_to_use_record_as_artifact_authority_is_blocked",
    }
)

REQUIRED_ESCALATION_RULES = frozenset(
    {
        "if_human_says_go_next_without_explicit_decision_record_stop",
        "if_request_mentions_generate_or_embeddings_stop",
        "if_request_mentions_provider_or_model_loading_stop",
        "if_request_mentions_artifact_write_or_reader_stop",
        "if_request_mentions_runtime_enablement_stop",
        "if_request_mentions_router_authority_stop",
        "if_full_freeze_context_is_compact_request_specific_freeze_entries_first",
        "if_actual_decision_recording_is_needed_create_separate_governed_patch",
        "if_generator_candidate_is_needed_create_later_separate_governed_patch_after_recording",
    }
)

FORBIDDEN_RECORD_FIELDS = frozenset(
    {
        "actual_human_decision",
        "recorded_human_decision",
        "human_approval",
        "approved_by_human",
        "generator_candidate_patch_authorized",
        "generate_artifact_now",
        "artifact_payload",
        "artifact_path",
        "artifact_content",
        "source_text",
        "raw_prompt_text",
        "raw_user_query_text",
        "raw_freeze_entry_text",
        "embedding_values",
        "vector_values",
        "vector_index",
        "provider_config",
        "model_config",
        "runtime_semantic_score",
        "final_route",
        "may_proceed_now",
    }
)

TRIGGER_TERMS_REQUIRING_FUTURE_PATCH = frozenset(
    {
        "approve",
        "approved",
        "record decision",
        "actual decision",
        "permit",
        "authorize",
        "generator candidate",
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
        "questionnaire",
        "decision values",
        "evidence list",
        "review only",
    }
)
