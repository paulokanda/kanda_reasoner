"""Generator candidate proposal review design for routing scorer v3.

This module is intentionally standard-library-only and review-design-only. It
reviews only the shape of a future generator-candidate proposal. It does not
create a generator candidate patch, does not authorize a generator, does not
record a human decision, does not generate, write, read, load, or discover
semantic artifacts, does not scan sources, does not materialize raw text, does
not generate embeddings or vectors, does not instantiate providers, does not
run semantic scoring, does not modify router authority, and does not change
runtime behavior.
"""

from __future__ import annotations


__all__ = [
    'build_generator_candidate_proposal_review_contract',
    'classify_generator_candidate_proposal_review_request',
    'validate_generator_candidate_proposal_review_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_PROPOSAL_REVIEW_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_proposal_review_design_v1"
)
GENERATOR_CANDIDATE_PROPOSAL_REVIEW_SCHEMA_VERSION = (
    "3.20-generator-candidate-proposal-review-design"
)
GENERATOR_CANDIDATE_PROPOSAL_REVIEW_STATUS = (
    "generator_candidate_proposal_review_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_REVIEW_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_proposal_review_only",
        "review_scope",
        "current_review_state",
        "current_review_effect",
        "required_prior_milestones",
        "required_proposal_inputs",
        "required_review_questions",
        "required_rejection_reasons",
        "allowed_future_review_outcomes",
        "allowed_review_outputs",
        "prohibited_review_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "review_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_REVIEW_SCOPE = "generator_candidate_proposal_review_only"

ALLOWED_CURRENT_REVIEW_STATES = frozenset(
    {
        "not_reviewed",
        "review_schema_only",
        "awaiting_separate_candidate_proposal",
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
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_PROPOSAL_INPUTS = frozenset(
    {
        "separate_generator_candidate_proposal_patch",
        "separate_recorded_human_decision_reference",
        "proposal_identity",
        "human_decision_traceability",
        "scope_statement",
        "non_goal_statement",
        "privacy_boundary_review",
        "authority_boundary_review",
        "source_selection_policy",
        "raw_text_handling_policy",
        "artifact_lifecycle_policy",
        "dependency_budget_policy",
        "resource_budget_policy",
        "validation_plan",
        "rollback_plan",
        "kbsc_shielding_plan",
        "stop_conditions",
    }
)

REQUIRED_REVIEW_QUESTIONS = frozenset(
    {
        "does_proposal_reference_a_separate_recorded_human_decision",
        "does_proposal_preserve_design_only_until_separate_generation_patch",
        "does_proposal_refuse_runtime_semantic_enablement",
        "does_proposal_refuse_router_authority_changes",
        "does_proposal_refuse_prompt_auto_loading",
        "does_proposal_refuse_freeze_memory_writes_from_output",
        "does_proposal_define_source_selection_without_scanning_now",
        "does_proposal_define_raw_text_handling_without_materializing_now",
        "does_proposal_define_artifact_lifecycle_without_writing_now",
        "does_proposal_define_dependency_budget_without_adding_dependencies_now",
        "does_proposal_define_resource_budget_without_running_generation_now",
        "does_proposal_define_validation_and_rollback",
        "does_proposal_include_kbsc_shielding_plan",
        "does_proposal_include_stop_conditions",
    }
)

REQUIRED_REJECTION_REASONS = frozenset(
    {
        "missing_recorded_human_decision",
        "tries_to_create_generator_patch_now",
        "tries_to_authorize_generator_now",
        "tries_to_generate_artifact_now",
        "tries_to_write_artifact_now",
        "tries_to_read_or_load_artifact_now",
        "tries_to_scan_sources_now",
        "tries_to_materialize_raw_text_now",
        "tries_to_generate_embeddings_now",
        "tries_to_materialize_vectors_now",
        "tries_to_add_provider_or_model_now",
        "tries_to_add_network_or_credentials_now",
        "tries_to_enable_runtime_semantics_now",
        "tries_to_change_router_authority_now",
        "tries_to_auto_load_prompts_now",
        "tries_to_write_freeze_memory_from_output_now",
    }
)

ALLOWED_FUTURE_REVIEW_OUTCOMES = frozenset(
    {
        "reject_candidate_proposal",
        "defer_candidate_proposal",
        "request_more_human_review_evidence",
        "permit_separate_governed_generator_candidate_patch_review_only",
    }
)

REQUIRED_ALLOWED_REVIEW_OUTPUTS = frozenset(
    {
        "proposal_review_schema",
        "proposal_input_checklist",
        "proposal_review_questions",
        "proposal_rejection_reasons",
        "future_review_outcome_vocabulary",
        "review_effect_policy_summary",
        "stop_conditions_list",
        "review_evidence_only",
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

REQUIRED_PROHIBITED_REVIEW_OUTPUTS = frozenset(
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
        "real_human_decision_recorded_by_review",
        "generator_candidate_patch_created",
        "generator_candidate_patch_authorized",
        "generator_implementation_authorized",
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
        "review_is_evidence_only",
        "review_does_not_create_candidate_patch",
        "review_does_not_authorize_generator_candidate",
        "review_does_not_authorize_generator_implementation",
        "review_requires_separate_recorded_human_decision",
        "review_requires_separate_governed_candidate_patch_for_any_candidate_work",
        "review_must_not_generate_artifacts",
        "review_must_not_write_artifacts",
        "review_must_not_read_artifacts",
        "review_must_not_scan_sources",
        "review_must_not_materialize_raw_text",
        "review_must_not_generate_embeddings",
        "review_must_not_materialize_vectors",
        "review_must_not_choose_route",
        "review_must_not_decide_required_prompts",
        "review_must_not_decide_missing_context",
        "review_must_not_decide_missing_behavior",
        "review_must_not_decide_may_proceed_now",
        "future_generator_candidate_patch_requires_separate_governed_patch",
        "future_artifact_generation_requires_later_separate_governed_patch",
    }
)

REQUIRED_REVIEW_EFFECT_POLICY = frozenset(
    {
        "review_schema_has_no_runtime_effect",
        "not_reviewed_state_has_no_generator_candidate_effect",
        "review_schema_cannot_satisfy_recorded_human_decision_prerequisite",
        "future_permit_review_only_outcome_does_not_authorize_generation",
        "future_permit_review_only_outcome_still_requires_separate_governed_patch",
        "review_output_is_not_router_authority",
        "review_output_is_not_may_proceed_authority",
        "review_output_is_not_prompt_loading_authority",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_recorded_human_decision_missing",
        "stop_if_candidate_patch_is_created_in_review_step",
        "stop_if_generator_authorization_is_claimed",
        "stop_if_artifact_generation_is_requested",
        "stop_if_artifact_io_is_requested",
        "stop_if_source_scanning_is_requested",
        "stop_if_raw_text_materialization_is_requested",
        "stop_if_embeddings_or_vectors_are_requested",
        "stop_if_provider_or_model_execution_is_requested",
        "stop_if_runtime_semantic_enablement_is_requested",
        "stop_if_router_authority_change_is_requested",
        "stop_if_prompt_auto_loading_is_requested",
        "stop_if_freeze_memory_write_from_output_is_requested",
    }
)

FORBIDDEN_REVIEW_FIELDS = frozenset(
    {
        "approved_generator_candidate_patch",
        "generator_candidate_patch",
        "generator_authorization",
        "artifact_generator",
        "generated_artifact",
        "artifact_writer",
        "artifact_reader",
        "source_scan_result",
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
        "router_override",
        "may_proceed_now",
    }
)


def _as_set(value: object) -> set[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return set()
    return {str(item) for item in value}


def _missing(required: set[str] | frozenset[str], actual: object) -> list[str]:
    return sorted(set(required) - _as_set(actual))


def _disabled_flags() -> dict[str, bool]:
    return {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)}


def build_generator_candidate_proposal_review_contract() -> dict[str, Any]:
    """Return the inert review schema for a future proposal review."""

    return {
        "schema_id": GENERATOR_CANDIDATE_PROPOSAL_REVIEW_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_PROPOSAL_REVIEW_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_PROPOSAL_REVIEW_STATUS,
        "declared_generator_candidate_proposal_review_only": True,
        "review_scope": REQUIRED_REVIEW_SCOPE,
        "current_review_state": "not_reviewed",
        "current_review_effect": "no_effect_schema_only_not_reviewed",
        "required_prior_milestones": sorted(REQUIRED_PRIOR_MILESTONES),
        "required_proposal_inputs": sorted(REQUIRED_PROPOSAL_INPUTS),
        "required_review_questions": sorted(REQUIRED_REVIEW_QUESTIONS),
        "required_rejection_reasons": sorted(REQUIRED_REJECTION_REASONS),
        "allowed_future_review_outcomes": sorted(ALLOWED_FUTURE_REVIEW_OUTCOMES),
        "allowed_review_outputs": sorted(REQUIRED_ALLOWED_REVIEW_OUTPUTS),
        "prohibited_review_outputs": sorted(REQUIRED_PROHIBITED_REVIEW_OUTPUTS),
        "disabled_flags": _disabled_flags(),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "review_effect_policy": sorted(REQUIRED_REVIEW_EFFECT_POLICY),
        "stop_conditions": sorted(REQUIRED_STOP_CONDITIONS),
    }


def validate_generator_candidate_proposal_review_contract(
    contract: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate that a proposal review schema remains inert."""

    errors: list[str] = []

    for field in sorted(REQUIRED_REVIEW_FIELDS):
        if field not in contract:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_REVIEW_FIELDS):
        if field in contract:
            errors.append(f"forbidden field present: {field}")

    if contract.get("schema_id") != GENERATOR_CANDIDATE_PROPOSAL_REVIEW_FEATURE_ID:
        errors.append("schema_id mismatch")
    if contract.get("schema_version") != GENERATOR_CANDIDATE_PROPOSAL_REVIEW_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if contract.get("schema_status") != GENERATOR_CANDIDATE_PROPOSAL_REVIEW_STATUS:
        errors.append("schema_status mismatch")
    if contract.get("declared_generator_candidate_proposal_review_only") is not True:
        errors.append("must declare generator candidate proposal review only")
    if contract.get("review_scope") != REQUIRED_REVIEW_SCOPE:
        errors.append("review_scope mismatch")
    if contract.get("current_review_state") not in ALLOWED_CURRENT_REVIEW_STATES:
        errors.append("invalid current_review_state")
    if contract.get("current_review_effect") != "no_effect_schema_only_not_reviewed":
        errors.append("current_review_effect must remain no effect")

    required_sets = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_proposal_inputs", REQUIRED_PROPOSAL_INPUTS),
        ("required_review_questions", REQUIRED_REVIEW_QUESTIONS),
        ("required_rejection_reasons", REQUIRED_REJECTION_REASONS),
        ("allowed_future_review_outcomes", ALLOWED_FUTURE_REVIEW_OUTCOMES),
        ("allowed_review_outputs", REQUIRED_ALLOWED_REVIEW_OUTPUTS),
        ("prohibited_review_outputs", REQUIRED_PROHIBITED_REVIEW_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("review_effect_policy", REQUIRED_REVIEW_EFFECT_POLICY),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for field, required in required_sets:
        missing = _missing(required, contract.get(field))
        if missing:
            errors.append(f"{field} missing: {', '.join(missing)}")

    disabled_flags = contract.get("disabled_flags")
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        disabled_flags = {}
    for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
        if flag not in disabled_flags:
            errors.append(f"disabled_flags missing: {flag}")
        elif disabled_flags[flag] is not False:
            errors.append(f"disabled flag must be false: {flag}")

    return {
        "ok": not errors,
        "errors": errors,
        "current_review_state": contract.get("current_review_state"),
        "real_human_decision_recorded_by_review": False,
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
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_proposal_review_request(request_text: str) -> dict[str, Any]:
    """Classify whether a request stays inside the inert review boundary."""

    text = request_text.lower()
    blocked_markers = {
        "approve",
        "authorize",
        "create patch",
        "candidate patch",
        "generate",
        "artifact",
        "write",
        "read",
        "load",
        "scan",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "router",
        "may proceed",
    }
    review_markers = {"review", "checklist", "schema", "questions", "rejection"}
    blocked = any(marker in text for marker in blocked_markers)
    review_only = any(marker in text for marker in review_markers)

    return {
        "allowed_now": review_only and not blocked,
        "permitted_output": (
            "generator_candidate_proposal_review_schema" if review_only and not blocked else None
        ),
        "current_review_state": "not_reviewed",
        "real_human_decision_recorded_by_review": False,
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
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
