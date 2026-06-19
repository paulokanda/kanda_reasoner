"""Generator candidate review bundle design for routing scorer v3.

This module is intentionally standard-library-only and review-bundle-design-only.
It bundles the previously frozen generator-candidate preparation boundaries into
one schema that a future, separately governed candidate patch would have to
reference. It does not create a generator candidate patch, does not authorize a
generator, does not record a human decision, does not generate, write, read,
load, or discover semantic artifacts, does not scan sources, does not
materialize raw text, does not generate embeddings or vectors, does not
instantiate providers, does not run semantic scoring, does not modify router
authority, and does not change runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_REVIEW_BUNDLE_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_review_bundle_design_v1"
)
GENERATOR_CANDIDATE_REVIEW_BUNDLE_SCHEMA_VERSION = (
    "3.27-generator-candidate-review-bundle-design"
)
GENERATOR_CANDIDATE_REVIEW_BUNDLE_STATUS = (
    "generator_candidate_review_bundle_only_no_candidate_patch_no_generator_authorization"
)

REQUIRED_REVIEW_BUNDLE_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_review_bundle_only",
        "review_bundle_scope",
        "current_review_bundle_state",
        "current_review_bundle_effect",
        "required_prior_milestones",
        "required_review_bundle_sections",
        "required_bundle_inputs",
        "required_candidate_patch_declarations",
        "required_boundary_declarations",
        "required_validation_declarations",
        "allowed_future_review_bundle_outcomes",
        "allowed_review_bundle_outputs",
        "prohibited_review_bundle_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "review_bundle_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_REVIEW_BUNDLE_SCOPE = "generator_candidate_review_bundle_only"
ALLOWED_CURRENT_REVIEW_BUNDLE_STATES = frozenset(
    {
        "not_review_bundle_defined",
        "review_bundle_schema_only",
        "awaiting_separate_human_review",
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
        "generator_candidate_proposal_review_frozen",
        "generator_candidate_patch_preflight_frozen",
        "generator_candidate_patch_envelope_frozen",
        "generator_candidate_patch_skeleton_frozen",
        "generator_candidate_patch_file_set_frozen",
        "generator_candidate_dependency_boundary_frozen",
        "generator_candidate_side_effect_boundary_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_REVIEW_BUNDLE_SECTIONS = frozenset(
    {
        "candidate_patch_identity",
        "candidate_patch_scope",
        "candidate_patch_non_goals",
        "candidate_patch_file_set_summary",
        "candidate_patch_dependency_boundary_summary",
        "candidate_patch_side_effect_boundary_summary",
        "candidate_patch_preflight_summary",
        "candidate_patch_envelope_summary",
        "candidate_patch_skeleton_summary",
        "candidate_patch_human_decision_summary",
        "candidate_patch_validation_summary",
        "candidate_patch_public_contract_boundary",
        "candidate_patch_router_authority_boundary",
        "candidate_patch_runtime_boundary",
        "candidate_patch_artifact_lifecycle_boundary",
        "candidate_patch_source_boundary",
        "candidate_patch_raw_text_boundary",
        "candidate_patch_kbsc_shielding_plan",
        "candidate_patch_freeze_plan",
        "candidate_patch_stop_conditions",
    }
)

REQUIRED_BUNDLE_INPUTS = frozenset(
    {
        "frozen_proposal_schema_reference",
        "frozen_proposal_review_reference",
        "frozen_preflight_reference",
        "frozen_envelope_reference",
        "frozen_skeleton_reference",
        "frozen_file_set_reference",
        "frozen_dependency_boundary_reference",
        "frozen_side_effect_boundary_reference",
        "recorded_human_decision_reference_required_for_future_patch",
        "kbsc_shielding_evidence_required_for_future_patch",
        "validation_evidence_required_for_future_patch",
        "freeze_hint_required_for_future_patch",
    }
)

REQUIRED_CANDIDATE_PATCH_DECLARATIONS = frozenset(
    {
        "candidate_patch_is_separate_future_patch",
        "candidate_patch_is_not_created_by_this_review_bundle",
        "candidate_patch_is_not_authorized_by_this_review_bundle",
        "candidate_patch_requires_recorded_human_decision_reference",
        "candidate_patch_requires_preflight_reference",
        "candidate_patch_requires_envelope_reference",
        "candidate_patch_requires_skeleton_reference",
        "candidate_patch_requires_file_set_reference",
        "candidate_patch_requires_dependency_boundary_reference",
        "candidate_patch_requires_side_effect_boundary_reference",
        "candidate_patch_requires_explicit_touched_paths",
        "candidate_patch_requires_no_public_runtime_export_by_default",
        "candidate_patch_requires_no_router_authority_by_default",
        "candidate_patch_requires_kbsc_before_merge",
    }
)

REQUIRED_BOUNDARY_DECLARATIONS = frozenset(
    {
        "review_bundle_does_not_create_candidate_patch",
        "review_bundle_does_not_authorize_candidate_patch",
        "review_bundle_does_not_authorize_generator",
        "review_bundle_does_not_authorize_dependencies",
        "review_bundle_does_not_authorize_side_effects",
        "review_bundle_does_not_authorize_artifact_generation",
        "review_bundle_does_not_authorize_artifact_reading",
        "review_bundle_does_not_authorize_artifact_writing",
        "review_bundle_does_not_authorize_source_scanning",
        "review_bundle_does_not_authorize_raw_text_materialization",
        "review_bundle_does_not_authorize_embedding_generation",
        "review_bundle_does_not_authorize_vector_generation",
        "review_bundle_does_not_authorize_provider_execution",
        "review_bundle_does_not_authorize_runtime_semantic_enablement",
        "review_bundle_does_not_authorize_router_authority",
        "review_bundle_does_not_write_freeze_memory",
        "review_bundle_does_not_auto_load_prompts",
    }
)

REQUIRED_VALIDATION_DECLARATIONS = frozenset(
    {
        "candidate_patch_must_have_static_validation",
        "candidate_patch_must_have_contract_tests",
        "candidate_patch_must_have_regression_tests",
        "candidate_patch_must_have_no_public_export_test",
        "candidate_patch_must_have_no_forbidden_runtime_paths_test",
        "candidate_patch_must_have_ascii_test",
        "candidate_patch_must_have_freeze_hint",
        "candidate_patch_must_have_install_validation_commands",
        "candidate_patch_must_have_rollback_boundary",
        "candidate_patch_must_have_kbsc_shield_test",
    }
)

ALLOWED_FUTURE_REVIEW_BUNDLE_OUTCOMES = frozenset(
    {
        "reject_generator_candidate_patch_readiness",
        "defer_generator_candidate_patch_readiness",
        "request_more_preflight_evidence",
        "request_more_human_decision_evidence",
        "request_more_boundary_evidence",
        "permit_separate_governed_generator_candidate_patch_design_only",
    }
)

REQUIRED_ALLOWED_REVIEW_BUNDLE_OUTPUTS = frozenset(
    {
        "generator_candidate_review_bundle_schema",
        "candidate_patch_readiness_checklist",
        "candidate_patch_required_inputs",
        "candidate_patch_required_boundaries",
        "candidate_patch_required_validation_summary",
        "candidate_patch_stop_conditions",
        "future_review_bundle_outcome_vocabulary",
        "review_bundle_effect_policy_summary",
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

REQUIRED_PROHIBITED_REVIEW_BUNDLE_OUTPUTS = frozenset(
    {
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generator_implementation",
        "artifact_generation_plan_authorization",
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
        "generator_candidate_patch_creation_enabled",
        "generator_candidate_patch_authorization_enabled",
        "generator_implementation_enabled",
        "dependency_install_enabled",
        "side_effect_authorization_enabled",
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_reading_enabled",
        "source_scanning_enabled",
        "raw_text_materialization_enabled",
        "embedding_generation_enabled",
        "vector_index_generation_enabled",
        "provider_execution_enabled",
        "semantic_runtime_enabled",
        "router_authority_enabled",
        "startup_generation_enabled",
        "background_generation_enabled",
        "public_runtime_export_enabled",
        "freeze_memory_write_enabled",
        "prompt_auto_loading_enabled",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "review_bundle_cannot_record_real_human_decision",
        "review_bundle_cannot_create_candidate_patch",
        "review_bundle_cannot_authorize_candidate_patch",
        "review_bundle_cannot_authorize_generator_implementation",
        "review_bundle_cannot_authorize_dependency_install",
        "review_bundle_cannot_authorize_side_effects",
        "review_bundle_cannot_authorize_artifact_generation",
        "review_bundle_cannot_authorize_artifact_io",
        "review_bundle_cannot_authorize_source_scanning",
        "review_bundle_cannot_authorize_raw_text_materialization",
        "review_bundle_cannot_authorize_runtime_semantic_scoring",
        "review_bundle_cannot_authorize_router_changes",
        "review_bundle_cannot_write_project_freeze_memory",
        "review_bundle_cannot_decide_may_proceed_now",
    }
)

REQUIRED_REVIEW_BUNDLE_EFFECT_POLICY = frozenset(
    {
        "schema_only_current_effect_is_no_effect",
        "review_bundle_output_is_review_readiness_metadata_only",
        "review_bundle_output_has_no_runtime_effect",
        "review_bundle_output_has_no_router_effect",
        "review_bundle_output_has_no_freeze_memory_effect",
        "review_bundle_output_has_no_candidate_patch_authority",
        "review_bundle_output_has_no_generation_authority",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_real_human_decision_would_be_recorded",
        "stop_if_candidate_patch_would_be_created",
        "stop_if_candidate_patch_would_be_authorized",
        "stop_if_generator_would_be_implemented",
        "stop_if_dependency_would_be_installed",
        "stop_if_side_effect_would_be_authorized",
        "stop_if_artifact_would_be_generated_written_or_read",
        "stop_if_source_would_be_scanned",
        "stop_if_raw_text_would_be_materialized",
        "stop_if_embedding_or_vector_would_be_generated",
        "stop_if_provider_or_model_would_be_loaded",
        "stop_if_runtime_or_startup_behavior_would_change",
        "stop_if_router_authority_would_change",
        "stop_if_public_runtime_contract_would_change",
        "stop_if_other_box_logic_would_be_modified",
    }
)

FORBIDDEN_REVIEW_BUNDLE_FIELDS = frozenset(
    {
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generator_implementation",
        "artifact_payload",
        "artifact_output_path",
        "artifact_input_path",
        "source_text",
        "raw_prompt_text",
        "raw_freeze_text",
        "embedding_values",
        "vector_values",
        "provider_name",
        "model_name",
        "runtime_route_signal",
        "may_proceed_now",
    }
)


def _sorted_tuple(values: frozenset[str]) -> tuple[str, ...]:
    return tuple(sorted(values))


def build_generator_candidate_review_bundle_contract() -> dict[str, Any]:
    """Return the frozen design contract for generator candidate review bundle."""

    return {
        "schema_id": GENERATOR_CANDIDATE_REVIEW_BUNDLE_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_REVIEW_BUNDLE_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_REVIEW_BUNDLE_STATUS,
        "declared_generator_candidate_review_bundle_only": True,
        "review_bundle_scope": REQUIRED_REVIEW_BUNDLE_SCOPE,
        "current_review_bundle_state": "not_review_bundle_defined",
        "current_review_bundle_effect": "no_effect_schema_only_not_review_bundle_defined",
        "required_prior_milestones": _sorted_tuple(REQUIRED_PRIOR_MILESTONES),
        "required_review_bundle_sections": _sorted_tuple(REQUIRED_REVIEW_BUNDLE_SECTIONS),
        "required_bundle_inputs": _sorted_tuple(REQUIRED_BUNDLE_INPUTS),
        "required_candidate_patch_declarations": _sorted_tuple(REQUIRED_CANDIDATE_PATCH_DECLARATIONS),
        "required_boundary_declarations": _sorted_tuple(REQUIRED_BOUNDARY_DECLARATIONS),
        "required_validation_declarations": _sorted_tuple(REQUIRED_VALIDATION_DECLARATIONS),
        "allowed_future_review_bundle_outcomes": _sorted_tuple(ALLOWED_FUTURE_REVIEW_BUNDLE_OUTCOMES),
        "allowed_review_bundle_outputs": _sorted_tuple(REQUIRED_ALLOWED_REVIEW_BUNDLE_OUTPUTS),
        "prohibited_review_bundle_outputs": _sorted_tuple(REQUIRED_PROHIBITED_REVIEW_BUNDLE_OUTPUTS),
        "disabled_flags": {key: False for key in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted_tuple(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "review_bundle_effect_policy": _sorted_tuple(REQUIRED_REVIEW_BUNDLE_EFFECT_POLICY),
        "stop_conditions": _sorted_tuple(REQUIRED_STOP_CONDITIONS),
    }


def _as_set(value: object) -> set[str]:
    if isinstance(value, str) or not isinstance(value, Sequence):
        return set()
    return {item for item in value if isinstance(item, str)}


def validate_generator_candidate_review_bundle_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a candidate review-bundle design contract without side effects."""

    errors: list[str] = []
    for field in sorted(REQUIRED_REVIEW_BUNDLE_FIELDS):
        if field not in candidate:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_REVIEW_BUNDLE_FIELDS):
        if field in candidate:
            errors.append(f"forbidden review_bundle field present: {field}")

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_REVIEW_BUNDLE_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_REVIEW_BUNDLE_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_REVIEW_BUNDLE_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_review_bundle_only") is not True:
        errors.append("contract must declare review-bundle-only mode")
    if candidate.get("review_bundle_scope") != REQUIRED_REVIEW_BUNDLE_SCOPE:
        errors.append("review_bundle_scope mismatch")
    if candidate.get("current_review_bundle_state") not in ALLOWED_CURRENT_REVIEW_BUNDLE_STATES:
        errors.append("current_review_bundle_state is not allowed")
    if candidate.get("current_review_bundle_effect") != "no_effect_schema_only_not_review_bundle_defined":
        errors.append("current_review_bundle_effect must remain schema-only/no-effect")

    required_sets = {
        "required_prior_milestones": REQUIRED_PRIOR_MILESTONES,
        "required_review_bundle_sections": REQUIRED_REVIEW_BUNDLE_SECTIONS,
        "required_bundle_inputs": REQUIRED_BUNDLE_INPUTS,
        "required_candidate_patch_declarations": REQUIRED_CANDIDATE_PATCH_DECLARATIONS,
        "required_boundary_declarations": REQUIRED_BOUNDARY_DECLARATIONS,
        "required_validation_declarations": REQUIRED_VALIDATION_DECLARATIONS,
        "allowed_future_review_bundle_outcomes": ALLOWED_FUTURE_REVIEW_BUNDLE_OUTCOMES,
        "allowed_review_bundle_outputs": REQUIRED_ALLOWED_REVIEW_BUNDLE_OUTPUTS,
        "prohibited_review_bundle_outputs": REQUIRED_PROHIBITED_REVIEW_BUNDLE_OUTPUTS,
        "no_authority_assertions": REQUIRED_NO_AUTHORITY_ASSERTIONS,
        "review_bundle_effect_policy": REQUIRED_REVIEW_BUNDLE_EFFECT_POLICY,
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
        "current_review_bundle_state": candidate.get("current_review_bundle_state"),
        "real_human_decision_recorded_by_review_bundle": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_implementation_authorized": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
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
        "requires_prior_generator_candidate_patch_preflight": True,
        "requires_prior_generator_candidate_patch_envelope": True,
        "requires_prior_generator_candidate_patch_skeleton": True,
        "requires_prior_generator_candidate_patch_file_set": True,
        "requires_prior_generator_candidate_dependency_boundary": True,
        "requires_prior_generator_candidate_side_effect_boundary": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_review_bundle_request(action: str) -> dict[str, Any]:
    """Classify whether an action is allowed by this design-only review bundle."""

    lowered = action.lower()
    unsafe_terms = (
        "create candidate patch",
        "candidate patch now",
        "authorize generator",
        "implement generator",
        "install dependency",
        "add dependency",
        "authorize side effect",
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
        "review bundle",
        "review_bundle",
        "sections",
        "declarations",
    )
    allowed_now = any(term in lowered for term in safe_terms) and not any(
        term in lowered for term in unsafe_terms
    )
    return {
        "allowed_now": allowed_now,
        "permitted_output": "generator_candidate_review_bundle_schema" if allowed_now else None,
        "current_review_bundle_state": "not_review_bundle_defined",
        "real_human_decision_recorded_by_review_bundle": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_implementation_authorized": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
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
        "requires_prior_generator_candidate_patch_preflight": True,
        "requires_prior_generator_candidate_patch_envelope": True,
        "requires_prior_generator_candidate_patch_skeleton": True,
        "requires_prior_generator_candidate_patch_file_set": True,
        "requires_prior_generator_candidate_dependency_boundary": True,
        "requires_prior_generator_candidate_side_effect_boundary": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
