# project-path: kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_patch_design.py
"""Generator candidate human decision recording patch design for routing scorer v3.

This module is intentionally standard-library-only and decision-recording-patch-design-schema-only.
It follows the human decision recording finalization closure shield and defines the shape of a
future governed human-decision-recording patch without creating that patch and without recording,
writing, committing, finalizing, or inferring any real human decision.

It does not create or authorize a generator candidate patch; does not authorize a generator; does
not install dependencies; does not authorize side effects; does not generate, write, read, load, or
discover semantic artifacts; does not scan sources; does not materialize raw text; does not generate
embeddings or vectors; does not instantiate providers; does not run semantic scoring; does not
modify router authority; and does not change runtime behavior.
"""

from __future__ import annotations


__all__ = [
    'build_generator_candidate_human_decision_recording_patch_design_contract',
    'classify_generator_candidate_human_decision_recording_patch_design_request',
    'validate_generator_candidate_human_decision_recording_patch_design_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_FEATURE_ID = "routing_signal_scorer_v3_generator_candidate_human_decision_recording_patch_design_v1"
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_SCHEMA_VERSION = "3.37-generator-candidate-human-decision-recording-patch-design"
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_STATUS = (
    "generator_candidate_human_decision_recording_patch_design_schema_only_no_decision_write_no_candidate_patch_no_generator_authorization"
)

REQUIRED_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_recording_patch_design_schema_only",
        "human_decision_recording_patch_design_scope",
        "current_human_decision_recording_patch_design_state",
        "current_human_decision_recording_patch_design_effect",
        "current_recorded_decision_value",
        "required_prior_milestones",
        "required_future_patch_evidence",
        "allowed_future_patch_actions",
        "allowed_patch_design_outputs",
        "prohibited_patch_design_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "patch_design_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_SCOPE = "generator_candidate_human_decision_recording_patch_design_schema_only"
ALLOWED_CURRENT_STATES = frozenset(
    {
        "decision_recording_patch_design_not_created",
        "awaiting_explicit_human_decision_recording_patch",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "generator_candidate_human_decision_recording_finalization_closure_shield_frozen",
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
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_FUTURE_PATCH_EVIDENCE = frozenset(
    {
        "explicit_human_decision_text",
        "explicit_human_confirmation_to_create_future_decision_recording_patch",
        "explicit_non_runtime_scope_acknowledged",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
        "referenced_human_decision_recording_finalization_closure_shield_freeze_id",
        "referenced_human_decision_recording_finalization_freeze_id",
        "referenced_human_decision_recording_commit_freeze_id",
        "referenced_human_decision_recording_implementation_freeze_id",
        "referenced_human_decision_recording_boundary_freeze_id",
        "referenced_human_decision_record_freeze_id",
        "referenced_human_decision_gate_freeze_id",
        "referenced_preparation_closure_freeze_id",
        "patch_design_has_no_write_effect_acknowledged",
        "generator_non_authorization_acknowledged",
        "artifact_io_non_goals_acknowledged",
        "source_scanning_non_goals_acknowledged",
        "dependency_non_goals_acknowledged",
        "side_effect_non_goals_acknowledged",
        "runtime_router_non_goals_acknowledged",
        "rollback_or_stop_condition_acknowledged",
    }
)

ALLOWED_FUTURE_PATCH_ACTIONS = frozenset(
    {
        "review_decision_recording_patch_design_only",
        "reject_future_decision_recording_patch",
        "defer_future_decision_recording_patch",
        "request_more_freeze_context",
        "request_more_architectural_review",
        "stop_before_decision_recording_patch",
    }
)

REQUIRED_ALLOWED_PATCH_DESIGN_OUTPUTS = frozenset(
    {
        "human_decision_recording_patch_design_schema",
        "future_recording_patch_evidence_checklist",
        "future_recording_patch_required_fields",
        "allowed_future_patch_actions",
        "current_not_recorded_notice",
        "current_patch_design_not_created_notice",
        "decision_scope_requirements",
        "patch_stop_conditions",
        "no_real_human_decision_recorded",
        "no_decision_write_performed",
        "no_decision_committed",
        "no_decision_finalized",
        "no_decision_recording_patch_created",
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

REQUIRED_PROHIBITED_PATCH_DESIGN_OUTPUTS = frozenset(
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

FORBIDDEN_FIELDS = REQUIRED_PROHIBITED_PATCH_DESIGN_OUTPUTS.union(
    {
        "actual_human_decision",
        "approved_by_human",
        "approval_effect",
        "decision_runtime_effect",
        "decision_recording_patch_payload",
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
        "does_not_record_human_decision",
        "does_not_write_human_decision",
        "does_not_commit_human_decision",
        "does_not_finalize_human_decision",
        "does_not_create_decision_recording_patch",
        "does_not_infer_human_approval",
        "does_not_create_candidate_patch",
        "does_not_authorize_candidate_patch",
        "does_not_authorize_generator",
        "does_not_install_dependencies",
        "does_not_authorize_side_effects",
        "does_not_generate_artifacts",
        "does_not_write_artifacts",
        "does_not_read_artifacts",
        "does_not_scan_sources",
        "does_not_materialize_raw_text",
        "does_not_generate_embeddings",
        "does_not_generate_vectors",
        "does_not_execute_providers",
        "does_not_enable_runtime_scoring",
        "does_not_modify_router_authority",
    }
)

STOP_CONDITIONS = frozenset(
    {
        "request_attempts_to_record_decision_now",
        "request_attempts_to_create_decision_recording_patch_now",
        "request_attempts_to_infer_approval_from_continue",
        "request_attempts_to_create_generator_candidate_patch_now",
        "request_attempts_to_generate_artifacts_now",
        "request_attempts_to_scan_sources_now",
        "request_attempts_to_enable_embeddings_or_vectors_now",
        "request_attempts_to_modify_router_authority_now",
    }
)


def _as_set(value: object) -> set[str]:
    """Support as set behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    if isinstance(value, str) or not isinstance(value, Sequence):
        return set()
    return {str(item) for item in value}


def _disabled_flags_are_false(flags: object) -> tuple[bool, list[str]]:
    """Support disabled flags are false behavior.
    
    Parameters
    ----------
    flags : object
        The flags value.
    
    Returns
    -------
    tuple[bool, list[str]]
        The tuple of values.
    """
    
    if not isinstance(flags, Mapping):
        return False, ["disabled_flags must be a mapping"]
    errors: list[str] = []
    for key in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
        if flags.get(key) is not False:
            errors.append(f"disabled flag must be False: {key}")
    return not errors, errors


def build_generator_candidate_human_decision_recording_patch_design_contract() -> dict[str, Any]:
    """Build a generator candidate human decision recording patch design contract.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_STATUS,
        "declared_generator_candidate_human_decision_recording_patch_design_schema_only": True,
        "human_decision_recording_patch_design_scope": REQUIRED_SCOPE,
        "current_human_decision_recording_patch_design_state": "decision_recording_patch_design_not_created",
        "current_human_decision_recording_patch_design_effect": "no_effect_schema_only_decision_recording_patch_design_not_created",
        "current_recorded_decision_value": "not_recorded",
        "required_prior_milestones": sorted(REQUIRED_PRIOR_MILESTONES),
        "required_future_patch_evidence": sorted(REQUIRED_FUTURE_PATCH_EVIDENCE),
        "allowed_future_patch_actions": sorted(ALLOWED_FUTURE_PATCH_ACTIONS),
        "allowed_patch_design_outputs": sorted(REQUIRED_ALLOWED_PATCH_DESIGN_OUTPUTS),
        "prohibited_patch_design_outputs": sorted(REQUIRED_PROHIBITED_PATCH_DESIGN_OUTPUTS),
        "disabled_flags": {key: False for key in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "patch_design_effect_policy": "schema_only_no_decision_write_no_patch_creation_no_generator_authorization_no_runtime_effect",
        "stop_conditions": sorted(STOP_CONDITIONS),
    }


def validate_generator_candidate_human_decision_recording_patch_design_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the generator candidate human decision recording patch design contract.
    
    Parameters
    ----------
    candidate : Mapping[str, Any]
        The candidate value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    errors: list[str] = []
    if not isinstance(candidate, Mapping):
        return {"ok": False, "errors": ["candidate must be a mapping"]}

    missing = sorted(REQUIRED_FIELDS.difference(candidate.keys()))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    forbidden = sorted(FORBIDDEN_FIELDS.intersection(candidate.keys()))
    if forbidden:
        errors.append("forbidden fields present: " + ", ".join(forbidden))

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_PATCH_DESIGN_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("human_decision_recording_patch_design_scope") != REQUIRED_SCOPE:
        errors.append("scope mismatch")
    if candidate.get("current_human_decision_recording_patch_design_state") not in ALLOWED_CURRENT_STATES:
        errors.append("invalid current_human_decision_recording_patch_design_state")
    if candidate.get("current_recorded_decision_value") != "not_recorded":
        errors.append("current_recorded_decision_value must remain not_recorded")

    required_checks = (
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_future_patch_evidence", REQUIRED_FUTURE_PATCH_EVIDENCE),
        ("allowed_future_patch_actions", ALLOWED_FUTURE_PATCH_ACTIONS),
        ("allowed_patch_design_outputs", REQUIRED_ALLOWED_PATCH_DESIGN_OUTPUTS),
        ("prohibited_patch_design_outputs", REQUIRED_PROHIBITED_PATCH_DESIGN_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("stop_conditions", STOP_CONDITIONS),
    )
    for field, required in required_checks:
        actual = _as_set(candidate.get(field))
        missing_values = sorted(required.difference(actual))
        if missing_values:
            errors.append(f"{field} missing values: " + ", ".join(missing_values))

    flags_ok, flag_errors = _disabled_flags_are_false(candidate.get("disabled_flags"))
    if not flags_ok:
        errors.extend(flag_errors)

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "schema_id": candidate.get("schema_id"),
        "schema_version": candidate.get("schema_version"),
        "current_human_decision_recording_patch_design_state": candidate.get("current_human_decision_recording_patch_design_state"),
        "current_recorded_decision_value": candidate.get("current_recorded_decision_value"),
        "human_decision_recording_subchain_closed": ok,
        "real_human_decision_recorded_by_human_decision_recording_patch_design": False,
        "human_decision_write_performed": False,
        "human_decision_commit_performed": False,
        "human_decision_finalization_performed": False,
        "human_decision_recording_patch_design_created": False,
        "human_decision_recording_patch_created": False,
        "human_decision_recording_write_function_enabled": False,
        "human_approval_inferred_from_preparation_chain": False,
        "candidate_patch_approval_recorded": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_commit_authorized": False,
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
        "public_runtime_export_authorized": False,
        "requires_prior_generator_candidate_human_decision_recording_finalization_closure_shield": True,
        "requires_explicit_human_confirmation_to_create_future_decision_recording_patch": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_human_decision_recording_patch_design_request(action: str) -> dict[str, Any]:
    """Support classify generator candidate human decision recording patch design request behavior.
    
    Parameters
    ----------
    action : str
        The action value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    normalized = action.lower()
    denied_tokens = (
        "approve",
        "record decision",
        "write decision",
        "commit decision",
        "finalize decision",
        "create decision recording patch",
        "create candidate patch",
        "authorize generator",
        "generate artifact",
        "embedding",
        "vector",
        "provider",
        "runtime",
    )
    denied = any(token in normalized for token in denied_tokens)
    review_only = "schema" in normalized or "review" in normalized or "checklist" in normalized
    return {
        "allowed_now": bool(review_only and not denied),
        "permitted_output": "human_decision_recording_patch_design_schema" if review_only and not denied else None,
        "current_recorded_decision_value": "not_recorded",
        "real_human_decision_recorded_by_human_decision_recording_patch_design": False,
        "human_decision_write_performed": False,
        "human_decision_commit_performed": False,
        "human_decision_finalization_performed": False,
        "human_decision_recording_patch_design_created": False,
        "human_decision_recording_patch_created": False,
        "human_approval_inferred_from_preparation_chain": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_implementation_authorized": False,
        "artifact_generation_authorized": False,
        "source_scanning_authorized": False,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
