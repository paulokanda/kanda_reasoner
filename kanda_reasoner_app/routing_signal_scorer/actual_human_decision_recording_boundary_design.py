"""Actual human decision recording boundary design for routing scorer v3.

This module is intentionally standard-library-only and boundary-design-only. It
records no real human decision, writes no decision record, authorizes no
generator candidate, generates no artifact, writes no artifact, reads no
artifact, scans no sources, materializes no raw text, generates no embeddings,
materializes no vectors, instantiates no providers, runs no semantic scoring,
modifies no router authority, loads no prompts, writes no freeze memory, and
changes no runtime behavior. It defines the future boundary that must be passed
before any separate actual decision-recording implementation can even be
proposed.
"""

from __future__ import annotations


__all__ = [
    'build_actual_human_decision_recording_boundary_contract',
    'classify_actual_human_decision_recording_boundary_request',
    'validate_actual_human_decision_recording_boundary_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID = (
    "routing_signal_scorer_v3_actual_human_decision_recording_boundary_design_v1"
)
ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION = (
    "3.18-actual-human-decision-recording-boundary-design"
)
ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_STATUS = (
    "decision_recording_boundary_schema_only_no_decision_write_no_generator_authorization"
)

REQUIRED_BOUNDARY_FIELDS = frozenset(
    {
        "boundary_id",
        "schema_version",
        "boundary_status",
        "declared_actual_human_decision_recording_boundary_only",
        "recording_boundary_scope",
        "current_recording_state",
        "current_recording_effect",
        "required_prior_milestones",
        "allowed_future_decision_values",
        "required_pre_recording_evidence",
        "required_recording_patch_constraints",
        "allowed_boundary_outputs",
        "prohibited_boundary_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "recording_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_RECORDING_BOUNDARY_SCOPE = "actual_human_decision_recording_boundary_schema_only"

ALLOWED_CURRENT_RECORDING_STATES = frozenset(
    {
        "not_recorded",
        "recording_not_implemented",
        "awaiting_separate_governed_recording_patch",
        "deferred",
    }
)

ALLOWED_FUTURE_DECISION_VALUES = frozenset(
    {
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
        "actual_human_decision_record_design_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_PRE_RECORDING_EVIDENCE = frozenset(
    {
        "actual_human_decision_recording_boundary_validation_ok",
        "actual_human_decision_record_design_validation_ok",
        "human_decision_intake_validation_ok",
        "human_architectural_review_record_validation_ok",
        "local_generator_candidate_review_gate_validation_ok",
        "dry_run_artifact_generation_plan_validation_ok",
        "disabled_generation_boundary_validation_ok",
        "v3_closure_shield_validation_ok",
        "explicit_human_request_to_record_actual_decision",
        "human_actor_role_attestation_present",
        "explicit_decision_value_selected_from_allowed_vocabulary",
        "written_scope_review_present",
        "written_privacy_review_present",
        "written_dependency_budget_review_present",
        "written_resource_budget_review_present",
        "written_authority_boundary_review_present",
        "written_artifact_lifecycle_review_present",
        "written_validation_plan_present",
        "written_stop_conditions_present",
    }
)

REQUIRED_RECORDING_PATCH_CONSTRAINTS = frozenset(
    {
        "separate_governed_patch_required",
        "separate_validation_required",
        "separate_freeze_required",
        "records_only_explicit_human_decision_value",
        "must_not_generate_artifacts",
        "must_not_write_semantic_artifacts",
        "must_not_read_semantic_artifacts",
        "must_not_scan_sources",
        "must_not_materialize_raw_text",
        "must_not_generate_embeddings",
        "must_not_materialize_vectors",
        "must_not_execute_provider",
        "must_not_enable_semantic_runtime",
        "must_not_change_router_authority",
        "must_not_auto_load_prompts",
        "must_not_write_freeze_memory_from_decision_output",
    }
)

REQUIRED_ALLOWED_BOUNDARY_OUTPUTS = frozenset(
    {
        "actual_human_decision_recording_boundary_schema",
        "pre_recording_evidence_checklist",
        "allowed_future_decision_values_list",
        "recording_patch_constraints_list",
        "recording_effect_policy_summary",
        "stop_conditions_list",
        "review_evidence_only",
        "no_real_decision_recorded_by_this_boundary",
        "no_decision_write_authorized_by_this_boundary",
        "no_generator_candidate_patch_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS = frozenset(
    {
        "real_human_decision_recorded",
        "decision_record_written",
        "decision_record_storage_path",
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
        "decision_recording_enabled",
        "decision_write_enabled",
        "decision_record_storage_enabled",
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
        "boundary_is_schema_only",
        "boundary_is_review_evidence_only",
        "boundary_records_no_real_human_decision",
        "boundary_writes_no_decision_record",
        "boundary_must_not_authorize_generator_candidate_patch_by_itself",
        "boundary_must_not_generate_artifacts",
        "boundary_must_not_write_artifacts",
        "boundary_must_not_read_artifacts",
        "boundary_must_not_scan_sources",
        "boundary_must_not_materialize_raw_text",
        "boundary_must_not_generate_embeddings",
        "boundary_must_not_materialize_vectors",
        "boundary_must_not_choose_route",
        "boundary_must_not_decide_required_prompts",
        "boundary_must_not_decide_missing_context",
        "boundary_must_not_decide_missing_behavior",
        "boundary_must_not_decide_may_proceed_now",
        "future_real_decision_recording_requires_separate_governed_patch",
        "future_generator_candidate_requires_separate_governed_patch_after_recorded_decision",
    }
)

REQUIRED_RECORDING_EFFECT_POLICY = frozenset(
    {
        "schema_only_boundary_has_no_decision_effect",
        "not_recorded_state_has_no_generator_candidate_effect",
        "future_recorded_defer_value_blocks_generator_candidate_until_new_decision",
        "future_recorded_reject_value_blocks_generator_candidate_until_new_decision",
        "future_recorded_permit_review_only_value_does_not_authorize_generation",
        "future_recorded_permit_review_only_value_only_allows_separate_candidate_proposal_review",
        "future_generator_candidate_still_requires_separate_governed_patch",
        "future_artifact_generation_still_requires_separate_governed_patch",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "missing_explicit_human_request_to_record_actual_decision",
        "missing_allowed_decision_value",
        "missing_human_actor_role_attestation",
        "missing_scope_review_evidence",
        "missing_privacy_review_evidence",
        "missing_dependency_budget_review_evidence",
        "missing_resource_budget_review_evidence",
        "missing_authority_boundary_review_evidence",
        "request_attempts_to_generate_artifacts",
        "request_attempts_to_write_semantic_artifacts",
        "request_attempts_to_read_semantic_artifacts",
        "request_attempts_to_scan_sources",
        "request_attempts_to_materialize_raw_text",
        "request_attempts_to_create_embeddings_or_vectors",
        "request_attempts_to_enable_runtime_semantics",
        "request_attempts_to_change_router_authority",
    }
)

FORBIDDEN_BOUNDARY_FIELDS = frozenset(
    {
        "actual_human_decision",
        "recorded_decision",
        "decision_record_written",
        "decision_record_storage_path",
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generated_artifact",
        "written_artifact_path",
        "loaded_artifact_path",
        "raw_text",
        "embedding_values",
        "vector_values",
        "vector_index",
        "provider_config",
        "runtime_semantic_score",
        "final_route",
        "may_proceed_now",
    }
)


def _sorted(values: Sequence[str] | frozenset[str]) -> list[str]:
    return sorted(values)


def build_actual_human_decision_recording_boundary_contract() -> dict[str, Any]:
    """Return the static review-only recording-boundary contract."""
    return {
        "boundary_id": ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID,
        "schema_version": ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION,
        "boundary_status": ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_STATUS,
        "declared_actual_human_decision_recording_boundary_only": True,
        "recording_boundary_scope": REQUIRED_RECORDING_BOUNDARY_SCOPE,
        "current_recording_state": "not_recorded",
        "current_recording_effect": "no_effect_schema_only_not_recorded",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "allowed_future_decision_values": _sorted(ALLOWED_FUTURE_DECISION_VALUES),
        "required_pre_recording_evidence": _sorted(REQUIRED_PRE_RECORDING_EVIDENCE),
        "required_recording_patch_constraints": _sorted(REQUIRED_RECORDING_PATCH_CONSTRAINTS),
        "allowed_boundary_outputs": _sorted(REQUIRED_ALLOWED_BOUNDARY_OUTPUTS),
        "prohibited_boundary_outputs": _sorted(REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS),
        "disabled_flags": {flag: False for flag in _sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "recording_effect_policy": _sorted(REQUIRED_RECORDING_EFFECT_POLICY),
        "stop_conditions": _sorted(REQUIRED_STOP_CONDITIONS),
    }


def validate_actual_human_decision_recording_boundary_contract(
    boundary: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate that the boundary remains schema-only and non-authoritative."""
    errors: list[str] = []

    missing_fields = REQUIRED_BOUNDARY_FIELDS.difference(boundary.keys())
    if missing_fields:
        errors.append("missing required boundary fields: " + ", ".join(sorted(missing_fields)))

    forbidden_fields = FORBIDDEN_BOUNDARY_FIELDS.intersection(boundary.keys())
    if forbidden_fields:
        errors.append("forbidden boundary fields present: " + ", ".join(sorted(forbidden_fields)))

    if boundary.get("boundary_id") != ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID:
        errors.append("boundary_id mismatch")
    if boundary.get("schema_version") != ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if boundary.get("recording_boundary_scope") != REQUIRED_RECORDING_BOUNDARY_SCOPE:
        errors.append("recording_boundary_scope mismatch")
    if boundary.get("declared_actual_human_decision_recording_boundary_only") is not True:
        errors.append("boundary must declare schema-only recording boundary")
    if boundary.get("current_recording_state") != "not_recorded":
        errors.append("current_recording_state must remain not_recorded")
    if boundary.get("current_recording_effect") != "no_effect_schema_only_not_recorded":
        errors.append("current_recording_effect must remain no_effect_schema_only_not_recorded")

    status = boundary.get("current_recording_state")
    if status not in ALLOWED_CURRENT_RECORDING_STATES:
        errors.append("current_recording_state is not in allowed current states")

    checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("allowed_future_decision_values", ALLOWED_FUTURE_DECISION_VALUES),
        ("required_pre_recording_evidence", REQUIRED_PRE_RECORDING_EVIDENCE),
        ("required_recording_patch_constraints", REQUIRED_RECORDING_PATCH_CONSTRAINTS),
        ("allowed_boundary_outputs", REQUIRED_ALLOWED_BOUNDARY_OUTPUTS),
        ("prohibited_boundary_outputs", REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("recording_effect_policy", REQUIRED_RECORDING_EFFECT_POLICY),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for field, required in checks:
        values = boundary.get(field, [])
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            errors.append(field + " must be a sequence")
            continue
        missing = required.difference(set(values))
        if missing:
            errors.append(field + " missing: " + ", ".join(sorted(missing)))

    disabled_flags = boundary.get("disabled_flags", {})
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        disabled_flags = {}
    for flag in REQUIRED_DISABLED_FLAGS_FALSE:
        if disabled_flags.get(flag) is not False:
            errors.append("disabled flag must be false: " + flag)

    return {
        "ok": not errors,
        "errors": errors,
        "current_recording_state": boundary.get("current_recording_state"),
        "real_human_decision_recorded": False,
        "decision_recording_authorized": False,
        "decision_write_authorized": False,
        "generator_candidate_patch_authorized": False,
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
        "requires_future_governed_patch": True,
    }


def classify_actual_human_decision_recording_boundary_request(request_text: str) -> dict[str, Any]:
    """Classify whether a request is limited to viewing the boundary schema."""
    lowered = request_text.lower()
    dangerous_terms = {
        "approve",
        "record decision",
        "write decision",
        "store decision",
        "generate",
        "artifact",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "enable",
        "router",
        "may proceed",
    }
    dangerous = any(term in lowered for term in dangerous_terms)
    schema_terms = {
        "schema",
        "boundary",
        "checklist",
        "design",
        "review",
    }
    schema_only = any(term in lowered for term in schema_terms) and not dangerous

    return {
        "allowed_now": schema_only,
        "permitted_output": (
            "actual_human_decision_recording_boundary_schema" if schema_only else "none"
        ),
        "current_recording_state": "not_recorded",
        "real_human_decision_recorded": False,
        "decision_recording_authorized": False,
        "decision_write_authorized": False,
        "generator_candidate_patch_authorized": False,
        "artifact_generation_authorized": False,
        "semantic_runtime_authorized": False,
        "router_authority_authorized": False,
        "requires_future_governed_patch_for_decision_recording": not schema_only,
        "requires_future_governed_patch_for_generation": True,
    }
