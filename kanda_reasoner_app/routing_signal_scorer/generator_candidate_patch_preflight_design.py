"""Generator candidate patch preflight design for routing scorer v3.

This module is intentionally standard-library-only and preflight-design-only. It
models the checklist that a future, separately governed generator-candidate
patch would have to satisfy before it could be proposed for review. It does not
create a generator candidate patch, does not authorize a generator, does not
record a human decision, does not generate, write, read, load, or discover
semantic artifacts, does not scan sources, does not materialize raw text, does
not generate embeddings or vectors, does not instantiate providers, does not
run semantic scoring, does not modify router authority, and does not change
runtime behavior.
"""

from __future__ import annotations


__all__ = [
    'build_generator_candidate_patch_preflight_contract',
    'classify_generator_candidate_patch_preflight_request',
    'validate_generator_candidate_patch_preflight_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_PATCH_PREFLIGHT_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_patch_preflight_design_v1"
)
GENERATOR_CANDIDATE_PATCH_PREFLIGHT_SCHEMA_VERSION = (
    "3.21-generator-candidate-patch-preflight-design"
)
GENERATOR_CANDIDATE_PATCH_PREFLIGHT_STATUS = (
    "generator_candidate_patch_preflight_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_PREFLIGHT_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_patch_preflight_only",
        "preflight_scope",
        "current_preflight_state",
        "current_preflight_effect",
        "required_prior_milestones",
        "required_candidate_patch_inputs",
        "required_preflight_checks",
        "required_rejection_reasons",
        "allowed_future_preflight_outcomes",
        "allowed_preflight_outputs",
        "prohibited_preflight_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "preflight_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_PREFLIGHT_SCOPE = "generator_candidate_patch_preflight_only"
ALLOWED_CURRENT_PREFLIGHT_STATES = frozenset(
    {
        "not_preflighted",
        "preflight_schema_only",
        "awaiting_separate_recorded_human_decision",
        "awaiting_separate_proposal_review",
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
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_CANDIDATE_PATCH_INPUTS = frozenset(
    {
        "separate_recorded_human_decision_reference",
        "separate_generator_candidate_proposal_review_reference",
        "candidate_patch_identity",
        "candidate_patch_non_goals",
        "candidate_patch_touched_paths",
        "candidate_patch_dependency_budget",
        "candidate_patch_privacy_boundary",
        "candidate_patch_source_boundary",
        "candidate_patch_raw_text_boundary",
        "candidate_patch_artifact_lifecycle_boundary",
        "candidate_patch_runtime_boundary",
        "candidate_patch_router_authority_boundary",
        "candidate_patch_validation_plan",
        "candidate_patch_rollback_plan",
        "candidate_patch_kbsc_shielding_plan",
        "candidate_patch_stop_conditions",
    }
)

REQUIRED_PREFLIGHT_CHECKS = frozenset(
    {
        "confirms_candidate_patch_is_separate_future_patch",
        "confirms_recorded_human_decision_reference_exists",
        "confirms_proposal_review_reference_exists",
        "confirms_no_runtime_semantic_enablement_in_candidate",
        "confirms_no_router_authority_change_in_candidate",
        "confirms_no_prompt_auto_loading_in_candidate",
        "confirms_no_freeze_memory_write_from_output_in_candidate",
        "confirms_no_source_scanning_at_preflight_time",
        "confirms_no_raw_text_materialization_at_preflight_time",
        "confirms_no_artifact_write_at_preflight_time",
        "confirms_no_embedding_generation_at_preflight_time",
        "confirms_no_provider_execution_at_preflight_time",
        "confirms_validation_plan_exists",
        "confirms_rollback_plan_exists",
        "confirms_kbsc_shielding_plan_exists",
        "confirms_stop_conditions_exist",
    }
)

REQUIRED_REJECTION_REASONS = frozenset(
    {
        "missing_recorded_human_decision",
        "missing_generator_candidate_proposal_review",
        "tries_to_create_candidate_patch_now",
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

ALLOWED_FUTURE_PREFLIGHT_OUTCOMES = frozenset(
    {
        "reject_candidate_patch_preflight",
        "defer_candidate_patch_preflight",
        "request_more_human_decision_evidence",
        "request_more_proposal_review_evidence",
        "permit_separate_governed_generator_candidate_patch_design_only",
    }
)

REQUIRED_ALLOWED_PREFLIGHT_OUTPUTS = frozenset(
    {
        "candidate_patch_preflight_schema",
        "candidate_patch_input_checklist",
        "candidate_patch_preflight_checks",
        "candidate_patch_rejection_reasons",
        "future_preflight_outcome_vocabulary",
        "preflight_effect_policy_summary",
        "stop_conditions_list",
        "preflight_evidence_only",
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

REQUIRED_PROHIBITED_PREFLIGHT_OUTPUTS = frozenset(
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
        "real_human_decision_recorded_by_preflight",
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
        "preflight_does_not_decide_routes",
        "preflight_does_not_decide_required_prompts",
        "preflight_does_not_decide_missing_context",
        "preflight_does_not_decide_missing_behavior",
        "preflight_does_not_decide_may_proceed_now",
        "preflight_does_not_load_prompts",
        "preflight_does_not_write_freeze_memory",
        "preflight_does_not_authorize_generation",
        "preflight_does_not_create_candidate_patch",
    }
)

REQUIRED_PREFLIGHT_EFFECT_POLICY = frozenset(
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

FORBIDDEN_PREFLIGHT_FIELDS = frozenset(
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


def _sorted_tuple(values: frozenset[str]) -> tuple[str, ...]:
    return tuple(sorted(values))


def build_generator_candidate_patch_preflight_contract() -> dict[str, Any]:
    """Return the frozen design contract for generator candidate patch preflight."""

    return {
        "schema_id": GENERATOR_CANDIDATE_PATCH_PREFLIGHT_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_PATCH_PREFLIGHT_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_PATCH_PREFLIGHT_STATUS,
        "declared_generator_candidate_patch_preflight_only": True,
        "preflight_scope": REQUIRED_PREFLIGHT_SCOPE,
        "current_preflight_state": "not_preflighted",
        "current_preflight_effect": "no_effect_schema_only_not_preflighted",
        "required_prior_milestones": _sorted_tuple(REQUIRED_PRIOR_MILESTONES),
        "required_candidate_patch_inputs": _sorted_tuple(REQUIRED_CANDIDATE_PATCH_INPUTS),
        "required_preflight_checks": _sorted_tuple(REQUIRED_PREFLIGHT_CHECKS),
        "required_rejection_reasons": _sorted_tuple(REQUIRED_REJECTION_REASONS),
        "allowed_future_preflight_outcomes": _sorted_tuple(ALLOWED_FUTURE_PREFLIGHT_OUTCOMES),
        "allowed_preflight_outputs": _sorted_tuple(REQUIRED_ALLOWED_PREFLIGHT_OUTPUTS),
        "prohibited_preflight_outputs": _sorted_tuple(REQUIRED_PROHIBITED_PREFLIGHT_OUTPUTS),
        "disabled_flags": {key: False for key in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted_tuple(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "preflight_effect_policy": _sorted_tuple(REQUIRED_PREFLIGHT_EFFECT_POLICY),
        "stop_conditions": _sorted_tuple(REQUIRED_STOP_CONDITIONS),
    }


def _as_set(value: object) -> set[str]:
    if isinstance(value, str) or not isinstance(value, Sequence):
        return set()
    return {item for item in value if isinstance(item, str)}


def validate_generator_candidate_patch_preflight_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a candidate preflight design contract without side effects."""

    errors: list[str] = []
    for field in sorted(REQUIRED_PREFLIGHT_FIELDS):
        if field not in candidate:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_PREFLIGHT_FIELDS):
        if field in candidate:
            errors.append(f"forbidden preflight field present: {field}")

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_PATCH_PREFLIGHT_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_PATCH_PREFLIGHT_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_PATCH_PREFLIGHT_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_patch_preflight_only") is not True:
        errors.append("contract must declare preflight-only mode")
    if candidate.get("preflight_scope") != REQUIRED_PREFLIGHT_SCOPE:
        errors.append("preflight_scope mismatch")
    if candidate.get("current_preflight_state") not in ALLOWED_CURRENT_PREFLIGHT_STATES:
        errors.append("current_preflight_state is not allowed")
    if candidate.get("current_preflight_effect") != "no_effect_schema_only_not_preflighted":
        errors.append("current_preflight_effect must remain schema-only/no-effect")

    required_sets = {
        "required_prior_milestones": REQUIRED_PRIOR_MILESTONES,
        "required_candidate_patch_inputs": REQUIRED_CANDIDATE_PATCH_INPUTS,
        "required_preflight_checks": REQUIRED_PREFLIGHT_CHECKS,
        "required_rejection_reasons": REQUIRED_REJECTION_REASONS,
        "allowed_future_preflight_outcomes": ALLOWED_FUTURE_PREFLIGHT_OUTCOMES,
        "allowed_preflight_outputs": REQUIRED_ALLOWED_PREFLIGHT_OUTPUTS,
        "prohibited_preflight_outputs": REQUIRED_PROHIBITED_PREFLIGHT_OUTPUTS,
        "no_authority_assertions": REQUIRED_NO_AUTHORITY_ASSERTIONS,
        "preflight_effect_policy": REQUIRED_PREFLIGHT_EFFECT_POLICY,
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
        "current_preflight_state": candidate.get("current_preflight_state"),
        "real_human_decision_recorded_by_preflight": False,
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
        "requires_prior_generator_candidate_proposal_review": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_patch_preflight_request(action: str) -> dict[str, Any]:
    """Classify whether an action is allowed by this design-only preflight."""

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
        "preflight",
        "questions",
        "rejection reasons",
    )
    allowed_now = any(term in lowered for term in safe_terms) and not any(
        term in lowered for term in unsafe_terms
    )
    return {
        "allowed_now": allowed_now,
        "permitted_output": "generator_candidate_patch_preflight_schema" if allowed_now else None,
        "current_preflight_state": "not_preflighted",
        "real_human_decision_recorded_by_preflight": False,
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
        "requires_prior_generator_candidate_proposal_review": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
