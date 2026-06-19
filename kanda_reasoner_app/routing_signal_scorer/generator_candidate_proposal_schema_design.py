"""Generator candidate proposal schema design for routing scorer v3.

This module is intentionally standard-library-only and schema-design-only. It
creates no generator candidate patch, records no approval, writes no proposal,
generates no artifact, writes no artifact, reads no artifact, scans no sources,
materializes no raw text, generates no embeddings, materializes no vectors,
instantiates no providers, runs no semantic scoring, modifies no router
authority, loads no prompts, writes no freeze memory, and changes no runtime
behavior. It only defines the future review schema that a separately governed
generator-candidate proposal would need to satisfy after a separate recorded
human decision permits proposal review.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_proposal_schema_design_v1"
)
GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_VERSION = (
    "3.19-generator-candidate-proposal-schema-design"
)
GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_STATUS = (
    "generator_candidate_proposal_schema_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_PROPOSAL_SCHEMA_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_proposal_schema_only",
        "proposal_scope",
        "current_proposal_state",
        "current_proposal_effect",
        "required_prior_milestones",
        "required_recorded_decision_prerequisites",
        "allowed_future_proposal_values",
        "required_candidate_proposal_sections",
        "required_candidate_patch_constraints",
        "allowed_schema_outputs",
        "prohibited_schema_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "proposal_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_PROPOSAL_SCOPE = "generator_candidate_proposal_schema_only"

ALLOWED_CURRENT_PROPOSAL_STATES = frozenset(
    {
        "not_proposed",
        "proposal_schema_only",
        "awaiting_separate_recorded_human_decision",
        "awaiting_separate_governed_candidate_patch",
        "deferred",
    }
)

ALLOWED_FUTURE_PROPOSAL_VALUES = frozenset(
    {
        "defer_generator_candidate_proposal",
        "reject_generator_candidate_proposal",
        "submit_review_only_generator_candidate_proposal",
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
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_RECORDED_DECISION_PREREQUISITES = frozenset(
    {
        "separate_actual_decision_recording_patch_frozen",
        "recorded_decision_value_equals_permit_separate_generator_candidate_proposal_review_only",
        "recorded_decision_has_human_actor_role_attestation",
        "recorded_decision_has_scope_review",
        "recorded_decision_has_privacy_review",
        "recorded_decision_has_dependency_budget_review",
        "recorded_decision_has_resource_budget_review",
        "recorded_decision_has_authority_boundary_review",
        "recorded_decision_has_artifact_lifecycle_review",
        "recorded_decision_has_validation_plan",
        "recorded_decision_has_stop_conditions",
    }
)

REQUIRED_CANDIDATE_PROPOSAL_SECTIONS = frozenset(
    {
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

REQUIRED_CANDIDATE_PATCH_CONSTRAINTS = frozenset(
    {
        "separate_governed_patch_required",
        "separate_validation_required",
        "separate_freeze_required",
        "candidate_patch_must_be_review_only_until_validated",
        "candidate_patch_must_not_enable_runtime_semantics",
        "candidate_patch_must_not_change_router_authority",
        "candidate_patch_must_not_auto_load_prompts",
        "candidate_patch_must_not_write_freeze_memory_from_candidate_output",
        "candidate_patch_must_not_materialize_raw_text_without_separate_policy",
        "candidate_patch_must_not_write_semantic_artifacts_without_separate_writer_boundary",
        "candidate_patch_must_not_read_semantic_artifacts_without_separate_reader_boundary",
        "candidate_patch_must_not_generate_embeddings_without_separate_provider_boundary",
        "candidate_patch_must_not_generate_vectors_without_separate_vector_boundary",
        "candidate_patch_must_not_use_network_or_credentials",
        "candidate_patch_must_not_add_unapproved_dependencies",
    }
)

REQUIRED_ALLOWED_SCHEMA_OUTPUTS = frozenset(
    {
        "generator_candidate_proposal_schema",
        "candidate_proposal_section_checklist",
        "recorded_decision_prerequisite_checklist",
        "candidate_patch_constraints_list",
        "proposal_effect_policy_summary",
        "stop_conditions_list",
        "review_evidence_only",
        "no_generator_candidate_patch_created",
        "no_generator_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_SCHEMA_OUTPUTS = frozenset(
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
        "real_human_decision_recorded_by_schema",
        "generator_candidate_patch_created",
        "generator_candidate_patch_authorized",
        "generator_implementation_enabled",
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
        "schema_is_review_evidence_only",
        "schema_does_not_create_candidate_patch",
        "schema_does_not_authorize_generator_candidate",
        "schema_requires_separate_recorded_human_decision_before_candidate_proposal",
        "schema_requires_separate_governed_candidate_patch",
        "schema_must_not_generate_artifacts",
        "schema_must_not_write_artifacts",
        "schema_must_not_read_artifacts",
        "schema_must_not_scan_sources",
        "schema_must_not_materialize_raw_text",
        "schema_must_not_generate_embeddings",
        "schema_must_not_materialize_vectors",
        "schema_must_not_choose_route",
        "schema_must_not_decide_required_prompts",
        "schema_must_not_decide_missing_context",
        "schema_must_not_decide_missing_behavior",
        "schema_must_not_decide_may_proceed_now",
        "future_generator_candidate_proposal_requires_separate_governed_patch",
        "future_artifact_generation_requires_later_separate_governed_patch",
    }
)

REQUIRED_PROPOSAL_EFFECT_POLICY = frozenset(
    {
        "schema_only_proposal_has_no_runtime_effect",
        "not_proposed_state_has_no_generator_candidate_effect",
        "proposal_schema_cannot_satisfy_recorded_human_decision_prerequisite",
        "future_submit_review_only_value_does_not_authorize_generation",
        "future_generator_candidate_patch_is_review_only_until_separately_validated",
        "future_generator_candidate_patch_must_remain_non_authoritative",
        "future_artifact_generation_still_requires_separate_governed_patch",
        "future_semantic_runtime_enablement_still_requires_separate_governed_patch",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "missing_separate_recorded_human_decision",
        "recorded_decision_value_not_permit_review_only_candidate_proposal",
        "missing_human_actor_role_attestation",
        "missing_scope_review_evidence",
        "missing_privacy_review_evidence",
        "missing_dependency_budget_review_evidence",
        "missing_resource_budget_review_evidence",
        "missing_authority_boundary_review_evidence",
        "request_attempts_to_create_generator_candidate_patch_now",
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

FORBIDDEN_PROPOSAL_SCHEMA_FIELDS = frozenset(
    {
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generator_implementation",
        "artifact_generator",
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


def build_generator_candidate_proposal_schema_contract() -> dict[str, Any]:
    """Return the static review-only generator-candidate proposal schema."""
    return {
        "schema_id": GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_STATUS,
        "declared_generator_candidate_proposal_schema_only": True,
        "proposal_scope": REQUIRED_PROPOSAL_SCOPE,
        "current_proposal_state": "not_proposed",
        "current_proposal_effect": "no_effect_schema_only_not_proposed",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "required_recorded_decision_prerequisites": _sorted(REQUIRED_RECORDED_DECISION_PREREQUISITES),
        "allowed_future_proposal_values": _sorted(ALLOWED_FUTURE_PROPOSAL_VALUES),
        "required_candidate_proposal_sections": _sorted(REQUIRED_CANDIDATE_PROPOSAL_SECTIONS),
        "required_candidate_patch_constraints": _sorted(REQUIRED_CANDIDATE_PATCH_CONSTRAINTS),
        "allowed_schema_outputs": _sorted(REQUIRED_ALLOWED_SCHEMA_OUTPUTS),
        "prohibited_schema_outputs": _sorted(REQUIRED_PROHIBITED_SCHEMA_OUTPUTS),
        "disabled_flags": {flag: False for flag in _sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "proposal_effect_policy": _sorted(REQUIRED_PROPOSAL_EFFECT_POLICY),
        "stop_conditions": _sorted(REQUIRED_STOP_CONDITIONS),
    }


def validate_generator_candidate_proposal_schema_contract(
    schema: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate that the proposal schema remains non-authoritative."""
    errors: list[str] = []

    missing_fields = REQUIRED_PROPOSAL_SCHEMA_FIELDS.difference(schema.keys())
    if missing_fields:
        errors.append("missing required proposal schema fields: " + ", ".join(sorted(missing_fields)))

    forbidden_fields = FORBIDDEN_PROPOSAL_SCHEMA_FIELDS.intersection(schema.keys())
    if forbidden_fields:
        errors.append("forbidden proposal schema fields present: " + ", ".join(sorted(forbidden_fields)))

    if schema.get("schema_id") != GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_FEATURE_ID:
        errors.append("schema_id mismatch")
    if schema.get("schema_version") != GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if schema.get("proposal_scope") != REQUIRED_PROPOSAL_SCOPE:
        errors.append("proposal_scope mismatch")
    if schema.get("declared_generator_candidate_proposal_schema_only") is not True:
        errors.append("schema must declare proposal schema only")
    if schema.get("current_proposal_state") != "not_proposed":
        errors.append("current_proposal_state must remain not_proposed")
    if schema.get("current_proposal_effect") != "no_effect_schema_only_not_proposed":
        errors.append("current_proposal_effect must remain no_effect_schema_only_not_proposed")

    status = schema.get("current_proposal_state")
    if status not in ALLOWED_CURRENT_PROPOSAL_STATES:
        errors.append("current_proposal_state is not in allowed current states")

    checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_recorded_decision_prerequisites", REQUIRED_RECORDED_DECISION_PREREQUISITES),
        ("allowed_future_proposal_values", ALLOWED_FUTURE_PROPOSAL_VALUES),
        ("required_candidate_proposal_sections", REQUIRED_CANDIDATE_PROPOSAL_SECTIONS),
        ("required_candidate_patch_constraints", REQUIRED_CANDIDATE_PATCH_CONSTRAINTS),
        ("allowed_schema_outputs", REQUIRED_ALLOWED_SCHEMA_OUTPUTS),
        ("prohibited_schema_outputs", REQUIRED_PROHIBITED_SCHEMA_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("proposal_effect_policy", REQUIRED_PROPOSAL_EFFECT_POLICY),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for field, required in checks:
        values = schema.get(field, [])
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            errors.append(field + " must be a sequence")
            continue
        missing = required.difference(set(values))
        if missing:
            errors.append(field + " missing: " + ", ".join(sorted(missing)))

    disabled_flags = schema.get("disabled_flags", {})
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        disabled_flags = {}
    for flag in REQUIRED_DISABLED_FLAGS_FALSE:
        if disabled_flags.get(flag) is not False:
            errors.append("disabled flag must be false: " + flag)

    return {
        "ok": not errors,
        "errors": errors,
        "current_proposal_state": schema.get("current_proposal_state"),
        "real_human_decision_recorded_by_schema": False,
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


def classify_generator_candidate_proposal_schema_request(request_text: str) -> dict[str, Any]:
    """Classify whether a request is limited to viewing the proposal schema."""
    lowered = request_text.lower()
    dangerous_terms = {
        "approve",
        "record decision",
        "write decision",
        "candidate patch",
        "implement",
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
        "proposal",
        "checklist",
        "design",
        "review",
    }
    schema_only = any(term in lowered for term in schema_terms) and not dangerous

    return {
        "allowed_now": schema_only,
        "permitted_output": (
            "generator_candidate_proposal_schema" if schema_only else "none"
        ),
        "current_proposal_state": "not_proposed",
        "real_human_decision_recorded_by_schema": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "artifact_generation_authorized": False,
        "semantic_runtime_authorized": False,
        "router_authority_authorized": False,
        "requires_prior_recorded_human_decision": True,
        "requires_future_governed_candidate_patch": not schema_only,
        "requires_future_governed_generation_patch": True,
    }
