# project-path: kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_boundary_design.py
"""Generator candidate human decision recording boundary design for routing scorer v3.

This module is intentionally standard-library-only and recording-boundary-schema-only.
It follows the generator candidate human decision record design and defines a
future boundary for how an explicit human decision recording step would be
admitted. The current recording state remains disabled/not-recorded and has no
approval effect.

It does not record a real human decision, does not infer approval from prior
schemas, does not approve or authorize a candidate patch, does not authorize a
generator, does not install dependencies, does not authorize side effects, does
not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors,
does not instantiate providers, does not run semantic scoring, does not modify
router authority, and does not change runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_human_decision_recording_boundary_design_v1"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION = (
    "3.31-generator-candidate-human-decision-recording-boundary-design"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_STATUS = (
    "generator_candidate_human_decision_recording_boundary_schema_only_no_decision_write_no_candidate_patch_no_generator_authorization"
)

REQUIRED_HUMAN_DECISION_RECORDING_BOUNDARY_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_recording_boundary_schema_only",
        "human_decision_recording_boundary_scope",
        "current_human_decision_recording_boundary_state",
        "current_human_decision_recording_boundary_effect",
        "current_recorded_decision_value",
        "required_prior_milestones",
        "required_future_recording_evidence",
        "allowed_future_recording_actions",
        "allowed_boundary_outputs",
        "prohibited_boundary_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "recording_boundary_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_SCOPE = "generator_candidate_human_decision_recording_boundary_schema_only"
ALLOWED_CURRENT_STATES = frozenset(
    {
        "decision_recording_boundary_not_open",
        "awaiting_explicit_human_decision_recording_patch",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
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
        "actual_human_decision_recording_boundary_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_FUTURE_RECORDING_EVIDENCE = frozenset(
    {
        "explicit_human_decision_text",
        "explicit_human_confirmation_to_record_decision",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
        "referenced_human_decision_record_freeze_id",
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

ALLOWED_FUTURE_RECORDING_ACTIONS = frozenset(
    {
        "record_approve_candidate_patch_design_only",
        "record_reject_candidate_patch_design",
        "record_defer_candidate_patch_design",
        "record_request_more_freeze_context",
        "record_request_more_architectural_review",
        "record_stop_after_preparation_closure",
    }
)

REQUIRED_ALLOWED_BOUNDARY_OUTPUTS = frozenset(
    {
        "human_decision_recording_boundary_schema",
        "future_recording_evidence_checklist",
        "allowed_future_recording_actions",
        "current_not_recorded_notice",
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

REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS = frozenset(
    {
        "recorded_human_decision",
        "decision_write",
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

FORBIDDEN_BOUNDARY_FIELDS = REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS.union(
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
        "route_decision",
    }
)


def _freeze_sorted(values: Sequence[str] | frozenset[str]) -> tuple[str, ...]:
    """Support freeze sorted behavior.
    
    Parameters
    ----------
    values : Sequence[str] | frozenset[str]
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return tuple(sorted(values))


def build_generator_candidate_human_decision_recording_boundary_contract() -> dict[str, Any]:
    """Return the inert decision-recording boundary schema."""

    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_STATUS,
        "declared_generator_candidate_human_decision_recording_boundary_schema_only": True,
        "human_decision_recording_boundary_scope": REQUIRED_SCOPE,
        "current_human_decision_recording_boundary_state": "decision_recording_boundary_not_open",
        "current_human_decision_recording_boundary_effect": "no_effect_schema_only_no_decision_write",
        "current_recorded_decision_value": "not_recorded",
        "required_prior_milestones": _freeze_sorted(REQUIRED_PRIOR_MILESTONES),
        "required_future_recording_evidence": _freeze_sorted(REQUIRED_FUTURE_RECORDING_EVIDENCE),
        "allowed_future_recording_actions": _freeze_sorted(ALLOWED_FUTURE_RECORDING_ACTIONS),
        "allowed_boundary_outputs": _freeze_sorted(REQUIRED_ALLOWED_BOUNDARY_OUTPUTS),
        "prohibited_boundary_outputs": _freeze_sorted(REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS),
        "disabled_flags": {name: False for name in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": {
            "real_human_decision_recorded_by_human_decision_recording_boundary": False,
            "human_decision_write_performed": False,
            "human_approval_inferred_from_preparation_chain": False,
            "candidate_patch_approval_recorded": False,
            "dependency_install_authorized": False,
            "side_effect_authorized": False,
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
        },
        "recording_boundary_effect_policy": {
            "recording_boundary_is_currently_closed": True,
            "current_decision_value_must_remain_not_recorded": True,
            "human_continue_text_is_not_approval": True,
            "preparation_chain_does_not_imply_approval": True,
            "future_recording_requires_separate_governed_patch": True,
            "future_candidate_patch_requires_separate_governed_patch": True,
            "future_generation_requires_separate_governed_patch": True,
        },
        "stop_conditions": (
            "stop_if_explicit_human_confirmation_is_missing",
            "stop_if_future_recording_evidence_is_incomplete",
            "stop_if_requested_action_would_record_decision_now",
            "stop_if_requested_action_would_create_candidate_patch",
            "stop_if_requested_action_would_authorize_generation",
            "stop_if_requested_action_would_enable_artifact_io",
            "stop_if_requested_action_would_scan_sources_or_materialize_raw_text",
            "stop_if_requested_action_would_enable_runtime_or_router_authority",
        ),
    }


def validate_generator_candidate_human_decision_recording_boundary_contract(
    candidate: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the schema and return explicit non-authority flags."""

    missing = sorted(REQUIRED_HUMAN_DECISION_RECORDING_BOUNDARY_FIELDS.difference(candidate))
    forbidden_present = sorted(FORBIDDEN_BOUNDARY_FIELDS.intersection(candidate))
    disabled_flags = candidate.get("disabled_flags", {})
    no_authority = candidate.get("no_authority_assertions", {})
    policy = candidate.get("recording_boundary_effect_policy", {})

    disabled_missing = []
    disabled_not_false = []
    if not isinstance(disabled_flags, Mapping):
        disabled_missing = sorted(REQUIRED_DISABLED_FLAGS_FALSE)
    else:
        disabled_missing = sorted(REQUIRED_DISABLED_FLAGS_FALSE.difference(disabled_flags))
        disabled_not_false = sorted(
            key for key in REQUIRED_DISABLED_FLAGS_FALSE if disabled_flags.get(key) is not False
        )

    no_authority_not_false = []
    if not isinstance(no_authority, Mapping):
        no_authority_not_false = ["no_authority_assertions_not_mapping"]
    else:
        no_authority_not_false = sorted(key for key, value in no_authority.items() if value is not False)

    prior_milestones = set(candidate.get("required_prior_milestones", ()))
    future_evidence = set(candidate.get("required_future_recording_evidence", ()))
    allowed_actions = set(candidate.get("allowed_future_recording_actions", ()))
    allowed_outputs = set(candidate.get("allowed_boundary_outputs", ()))
    prohibited_outputs = set(candidate.get("prohibited_boundary_outputs", ()))

    ok = (
        not missing
        and not forbidden_present
        and candidate.get("schema_id") == GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID
        and candidate.get("schema_version") == GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION
        and candidate.get("declared_generator_candidate_human_decision_recording_boundary_schema_only") is True
        and candidate.get("human_decision_recording_boundary_scope") == REQUIRED_SCOPE
        and candidate.get("current_human_decision_recording_boundary_state") in ALLOWED_CURRENT_STATES
        and candidate.get("current_recorded_decision_value") == "not_recorded"
        and REQUIRED_PRIOR_MILESTONES.issubset(prior_milestones)
        and REQUIRED_FUTURE_RECORDING_EVIDENCE.issubset(future_evidence)
        and ALLOWED_FUTURE_RECORDING_ACTIONS.issubset(allowed_actions)
        and REQUIRED_ALLOWED_BOUNDARY_OUTPUTS.issubset(allowed_outputs)
        and REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS.issubset(prohibited_outputs)
        and not disabled_missing
        and not disabled_not_false
        and not no_authority_not_false
        and isinstance(policy, Mapping)
        and policy.get("recording_boundary_is_currently_closed") is True
        and policy.get("current_decision_value_must_remain_not_recorded") is True
        and policy.get("human_continue_text_is_not_approval") is True
        and policy.get("preparation_chain_does_not_imply_approval") is True
        and policy.get("future_recording_requires_separate_governed_patch") is True
        and policy.get("future_candidate_patch_requires_separate_governed_patch") is True
        and policy.get("future_generation_requires_separate_governed_patch") is True
    )

    return {
        "ok": ok,
        "schema_id": candidate.get("schema_id"),
        "schema_version": candidate.get("schema_version"),
        "missing_required_fields": tuple(missing),
        "forbidden_fields_present": tuple(forbidden_present),
        "disabled_flags_missing": tuple(disabled_missing),
        "disabled_flags_not_false": tuple(disabled_not_false),
        "no_authority_flags_not_false": tuple(no_authority_not_false),
        "current_human_decision_recording_boundary_state": candidate.get(
            "current_human_decision_recording_boundary_state"
        ),
        "current_recorded_decision_value": candidate.get("current_recorded_decision_value"),
        "real_human_decision_recorded_by_human_decision_recording_boundary": False,
        "human_decision_write_performed": False,
        "human_approval_inferred_from_preparation_chain": False,
        "candidate_patch_approval_recorded": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
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
        "requires_prior_generator_candidate_human_decision_record": True,
        "requires_explicit_human_confirmation_to_record_decision": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_human_decision_recording_boundary_request(action: str) -> dict[str, Any]:
    """Classify any requested action as not allowed by this boundary."""

    lowered = action.lower()
    requested_recording = any(
        token in lowered
        for token in (
            "record",
            "approve",
            "approved",
            "human decision",
            "candidate patch",
            "generate",
            "artifact",
            "embedding",
            "vector",
            "runtime",
            "router",
        )
    )
    return {
        "requested_action": action,
        "recording_or_generation_language_detected": requested_recording,
        "allowed_now": False,
        "current_human_decision_recording_boundary_state": "decision_recording_boundary_not_open",
        "current_recorded_decision_value": "not_recorded",
        "real_human_decision_recorded_by_human_decision_recording_boundary": False,
        "human_decision_write_performed": False,
        "human_approval_inferred_from_preparation_chain": False,
        "candidate_patch_approval_recorded": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
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
        "requires_prior_generator_candidate_human_decision_record": True,
        "requires_explicit_human_confirmation_to_record_decision": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


__all__ = [
    "GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID",
    "GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION",
    "build_generator_candidate_human_decision_recording_boundary_contract",
    "validate_generator_candidate_human_decision_recording_boundary_contract",
    "classify_generator_candidate_human_decision_recording_boundary_request",
]
