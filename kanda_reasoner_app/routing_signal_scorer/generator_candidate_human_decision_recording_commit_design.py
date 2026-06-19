"""Generator candidate human decision recording commit design for routing scorer v3.

This module is intentionally standard-library-only and human-decision-recording-commit-schema-only.
It follows the generator candidate human decision recording candidate design and defines how a
future decision-recording commit could be described for review. The current commit
state remains not-committed and the current decision remains not_recorded.

It does not record or write a real human decision, does not create a recording commit,
does not infer approval from prior schemas or from "continue", does not approve or authorize a
candidate patch, does not authorize a generator, does not install dependencies, does not authorize
side effects, does not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors, does not instantiate
providers, does not run semantic scoring, does not modify router authority, and does not change
runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_human_decision_recording_commit_design_v1"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_SCHEMA_VERSION = (
    "3.34-generator-candidate-human-decision-recording-commit-design"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_STATUS = (
    "generator_candidate_human_decision_recording_commit_schema_only_no_decision_write_no_candidate_patch_no_generator_authorization"
)

REQUIRED_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_recording_commit_schema_only",
        "human_decision_recording_commit_scope",
        "current_human_decision_recording_commit_state",
        "current_human_decision_recording_commit_effect",
        "current_recorded_decision_value",
        "required_prior_milestones",
        "required_future_commit_evidence",
        "allowed_future_recording_commit_actions",
        "allowed_commit_outputs",
        "prohibited_commit_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "commit_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_SCOPE = "generator_candidate_human_decision_recording_commit_schema_only"
ALLOWED_CURRENT_STATES = frozenset(
    {
        "decision_recording_commit_not_committed",
        "awaiting_explicit_human_decision_recording_commit_patch",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "generator_candidate_human_decision_recording_implementation_frozen",
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

REQUIRED_FUTURE_COMMIT_EVIDENCE = frozenset(
    {
        "explicit_human_decision_text",
        "explicit_human_confirmation_to_prepare_recording_commit",
        "explicit_non_runtime_scope_acknowledged",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
        "referenced_human_decision_recording_implementation_freeze_id",
        "referenced_human_decision_recording_boundary_freeze_id",
        "referenced_human_decision_record_freeze_id",
        "referenced_human_decision_gate_freeze_id",
        "referenced_preparation_closure_freeze_id",
        "commit_design_only_scope_acknowledged",
        "decision_recording_commit_has_no_write_effect_acknowledged",
        "generator_non_authorization_acknowledged",
        "artifact_io_non_goals_acknowledged",
        "source_scanning_non_goals_acknowledged",
        "dependency_non_goals_acknowledged",
        "side_effect_non_goals_acknowledged",
        "runtime_router_non_goals_acknowledged",
        "rollback_or_stop_condition_acknowledged",
    }
)

ALLOWED_FUTURE_RECORDING_COMMIT_ACTIONS = frozenset(
    {
        "prepare_decision_recording_commit_design_for_review_only",
        "reject_decision_recording_commit_design",
        "defer_decision_recording_commit_design",
        "request_more_freeze_context",
        "request_more_architectural_review",
        "stop_before_decision_recording_commit",
    }
)

REQUIRED_ALLOWED_COMMIT_OUTPUTS = frozenset(
    {
        "human_decision_recording_commit_schema",
        "future_recording_commit_evidence_checklist",
        "allowed_future_recording_commit_actions",
        "current_not_recorded_notice",
        "current_commit_not_committed_notice",
        "decision_scope_requirements",
        "commit_stop_conditions",
        "no_real_human_decision_recorded",
        "no_decision_write_performed",
        "no_recording_commit_created",
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

REQUIRED_PROHIBITED_COMMIT_OUTPUTS = frozenset(
    {
        "recorded_human_decision",
        "decision_write",
        "decision_recording_commit_patch",
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
        "human_decision_recording_commit_enabled",
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

FORBIDDEN_FIELDS = REQUIRED_PROHIBITED_COMMIT_OUTPUTS.union(
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
        "recording_commit_does_not_record_real_human_decision",
        "recording_commit_does_not_write_human_decision",
        "recording_commit_does_not_create_recording_patch",
        "recording_commit_does_not_enable_write_function",
        "recording_commit_does_not_infer_human_approval",
        "recording_commit_does_not_approve_candidate_patch",
        "recording_commit_does_not_create_candidate_patch",
        "recording_commit_does_not_authorize_candidate_patch",
        "recording_commit_does_not_authorize_generator",
        "recording_commit_does_not_authorize_dependencies",
        "recording_commit_does_not_authorize_side_effects",
        "recording_commit_does_not_authorize_artifact_generation",
        "recording_commit_does_not_authorize_artifact_reading",
        "recording_commit_does_not_authorize_artifact_writing",
        "recording_commit_does_not_authorize_source_scanning",
        "recording_commit_does_not_authorize_raw_text_materialization",
        "recording_commit_does_not_authorize_embeddings",
        "recording_commit_does_not_authorize_vectors",
        "recording_commit_does_not_authorize_provider_execution",
        "recording_commit_does_not_authorize_runtime_semantic_scoring",
        "recording_commit_does_not_authorize_router_decisions",
        "recording_commit_does_not_write_freeze_memory",
        "recording_commit_does_not_auto_load_prompts",
    }
)

REQUIRED_COMMIT_EFFECT_POLICY = frozenset(
    {
        "schema_only_commit_has_no_decision_effect",
        "not_recorded_value_has_no_decision_effect",
        "decision_recording_commit_not_committed_has_no_write_effect",
        "future_recording_commit_requires_separate_governed_patch",
        "future_recording_commit_may_only_prepare_review_schema",
        "future_recording_commit_does_not_write_decision_in_this_milestone",
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
        "implement decision",
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
        "recording commit",
        "commit shape",
        "evidence checklist",
        "review only",
        "show checklist",
    }
)


def _sorted(values: Sequence[str] | set[str] | frozenset[str]) -> list[str]:
    return sorted(values)


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in _sorted(REQUIRED_DISABLED_FLAGS_FALSE)}


def build_generator_candidate_human_decision_recording_commit_contract() -> dict[str, Any]:
    """Return the inert decision-recording commit schema."""
    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_STATUS,
        "declared_generator_candidate_human_decision_recording_commit_schema_only": True,
        "human_decision_recording_commit_scope": REQUIRED_SCOPE,
        "current_human_decision_recording_commit_state": "decision_recording_commit_not_committed",
        "current_human_decision_recording_commit_effect": "no_effect_schema_only_not_committed_not_recorded",
        "current_recorded_decision_value": "not_recorded",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "required_future_commit_evidence": _sorted(REQUIRED_FUTURE_COMMIT_EVIDENCE),
        "allowed_future_recording_commit_actions": _sorted(ALLOWED_FUTURE_RECORDING_COMMIT_ACTIONS),
        "allowed_commit_outputs": _sorted(REQUIRED_ALLOWED_COMMIT_OUTPUTS),
        "prohibited_commit_outputs": _sorted(REQUIRED_PROHIBITED_COMMIT_OUTPUTS),
        "disabled_flags": _false_flags(),
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "commit_effect_policy": _sorted(REQUIRED_COMMIT_EFFECT_POLICY),
        "stop_conditions": _sorted(REQUIRED_STOP_CONDITIONS),
    }


def validate_generator_candidate_human_decision_recording_commit_contract(
    candidate: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the inert recording-commit schema and return denial facts."""
    errors: list[str] = []

    missing = REQUIRED_FIELDS.difference(candidate)
    if missing:
        errors.append("missing required human decision recording commit fields: " + ", ".join(sorted(missing)))

    forbidden = FORBIDDEN_FIELDS.intersection(candidate)
    if forbidden:
        errors.append("forbidden commit field present: " + ", ".join(sorted(forbidden)))

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_COMMIT_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_human_decision_recording_commit_schema_only") is not True:
        errors.append("schema-only declaration must be true")
    if candidate.get("human_decision_recording_commit_scope") != REQUIRED_SCOPE:
        errors.append("human_decision_recording_commit_scope mismatch")
    if candidate.get("current_human_decision_recording_commit_state") not in ALLOWED_CURRENT_STATES:
        errors.append("current human decision recording commit state is not allowed")
    if candidate.get("current_human_decision_recording_commit_state") != "decision_recording_commit_not_committed":
        errors.append("current human decision recording commit state must remain decision_recording_commit_not_committed")
    if candidate.get("current_human_decision_recording_commit_effect") != "no_effect_schema_only_not_committed_not_recorded":
        errors.append("current human decision recording commit effect must remain no_effect_schema_only_not_committed_not_recorded")
    if candidate.get("current_recorded_decision_value") != "not_recorded":
        errors.append("current recorded decision value must remain not_recorded")

    set_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_future_commit_evidence", REQUIRED_FUTURE_COMMIT_EVIDENCE),
        ("allowed_future_recording_commit_actions", ALLOWED_FUTURE_RECORDING_COMMIT_ACTIONS),
        ("allowed_commit_outputs", REQUIRED_ALLOWED_COMMIT_OUTPUTS),
        ("prohibited_commit_outputs", REQUIRED_PROHIBITED_COMMIT_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("commit_effect_policy", REQUIRED_COMMIT_EFFECT_POLICY),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for key, required in set_checks:
        values = candidate.get(key, [])
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            errors.append(f"{key} must be a sequence")
            continue
        if not required.issubset(set(values)):
            errors.append(f"{key} missing required values")

    flags = candidate.get("disabled_flags", {})
    if not isinstance(flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        flags = {}
    else:
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            if flag not in flags:
                errors.append(f"disabled flag missing: {flag}")
            elif flags[flag] is not False:
                errors.append(f"disabled flag must be false: {flag}")

    return {
        "ok": not errors,
        "errors": errors,
        "schema_id": candidate.get("schema_id"),
        "schema_version": candidate.get("schema_version"),
        "current_human_decision_recording_commit_state": candidate.get("current_human_decision_recording_commit_state"),
        "current_recorded_decision_value": candidate.get("current_recorded_decision_value"),
        "real_human_decision_recorded_by_human_decision_recording_commit": flags.get("real_human_decision_recording_enabled", True),
        "human_decision_write_performed": flags.get("human_decision_write_enabled", True),
        "human_decision_recording_commit_created": flags.get("human_decision_recording_commit_enabled", True),
        "human_decision_recording_write_function_enabled": flags.get("human_decision_recording_write_function_enabled", True),
        "human_approval_inferred_from_preparation_chain": flags.get("human_approval_inference_enabled", True),
        "candidate_patch_approval_recorded": flags.get("candidate_patch_approval_enabled", True),
        "dependency_install_authorized": flags.get("dependency_install_enabled", True),
        "side_effect_authorized": flags.get("side_effect_authorization_enabled", True),
        "generator_candidate_patch_created": flags.get("generator_candidate_patch_creation_enabled", True),
        "generator_candidate_patch_authorized": flags.get("generator_candidate_patch_authorization_enabled", True),
        "generator_commit_authorized": flags.get("generator_commit_enabled", True),
        "generator_implementation_authorized": flags.get("generator_commit_enabled", True),
        "artifact_generation_authorized": flags.get("artifact_generation_enabled", True),
        "artifact_writing_authorized": flags.get("artifact_writing_enabled", True),
        "artifact_reading_authorized": flags.get("artifact_reading_enabled", True),
        "source_scanning_authorized": flags.get("source_scanning_enabled", True),
        "raw_text_materialization_authorized": flags.get("raw_text_materialization_enabled", True),
        "embedding_generation_authorized": flags.get("embedding_generation_enabled", True),
        "vector_index_generation_authorized": flags.get("vector_index_writing_enabled", True),
        "provider_execution_authorized": flags.get("provider_execution_enabled", True),
        "semantic_runtime_authorized": flags.get("semantic_runtime_scoring_enabled", True),
        "router_authority_authorized": flags.get("router_authority_enabled", True),
        "requires_prior_generator_candidate_human_decision_recording_implementation": True,
        "requires_explicit_human_confirmation_to_prepare_recording_commit": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_human_decision_recording_commit_request(user_text: str) -> dict[str, Any]:
    """Classify requests without granting decision-recording or generation authority."""
    text = (user_text or "").lower()
    has_trigger = any(term in text for term in TRIGGER_TERMS_REQUIRING_FUTURE_PATCH)
    has_schema_talk = any(term in text for term in SCHEMA_TALK_TERMS)

    base = validate_generator_candidate_human_decision_recording_commit_contract(
        build_generator_candidate_human_decision_recording_commit_contract()
    )
    if has_trigger:
        return {
            **base,
            "allowed_now": False,
            "permitted_output": "none",
            "reason": "request would require a separate governed decision-recording, candidate-patch, or generation patch",
        }

    return {
        **base,
        "allowed_now": bool(has_schema_talk),
        "permitted_output": "human_decision_recording_commit_schema" if has_schema_talk else "none",
        "reason": "schema-only discussion is allowed; decision recording and generation remain disabled",
    }
