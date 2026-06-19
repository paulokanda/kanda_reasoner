"""Generator candidate human decision record design for routing scorer v3.

This module is intentionally standard-library-only and human-decision-record-schema-only.
It follows the generator candidate human decision gate and defines how a future
explicit human decision record could be represented. The current record remains
``not_recorded`` and has no approval effect.

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


GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_human_decision_record_design_v1"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION = (
    "3.30-generator-candidate-human-decision-record-design"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS = (
    "generator_candidate_human_decision_record_schema_only_no_decision_recorded_no_candidate_patch_no_generator_authorization"
)

REQUIRED_HUMAN_DECISION_RECORD_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_record_schema_only",
        "human_decision_record_scope",
        "current_human_decision_record_state",
        "current_human_decision_record_effect",
        "current_recorded_decision_value",
        "required_prior_milestones",
        "required_future_recording_inputs",
        "allowed_future_recorded_decision_values",
        "allowed_record_outputs",
        "prohibited_record_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "record_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_HUMAN_DECISION_RECORD_SCOPE = "generator_candidate_human_decision_record_schema_only"
ALLOWED_CURRENT_HUMAN_DECISION_RECORD_STATES = frozenset(
    {
        "human_decision_record_not_recorded",
        "awaiting_explicit_human_decision_recording_patch",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
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

REQUIRED_FUTURE_RECORDING_INPUTS = frozenset(
    {
        "explicit_human_decision_text",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
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

ALLOWED_FUTURE_RECORDED_DECISION_VALUES = frozenset(
    {
        "not_recorded",
        "approve_candidate_patch_design_only",
        "reject_candidate_patch_design",
        "defer_candidate_patch_design",
        "request_more_freeze_context",
        "request_more_architectural_review",
        "stop_after_preparation_closure",
    }
)

REQUIRED_ALLOWED_RECORD_OUTPUTS = frozenset(
    {
        "human_decision_record_schema",
        "future_recording_input_checklist",
        "allowed_future_recorded_decision_values",
        "current_not_recorded_notice",
        "decision_scope_requirements",
        "candidate_patch_stop_conditions",
        "no_real_human_decision_recorded",
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

REQUIRED_PROHIBITED_RECORD_OUTPUTS = frozenset(
    {
        "recorded_human_decision",
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

FORBIDDEN_RECORD_FIELDS = REQUIRED_PROHIBITED_RECORD_OUTPUTS.union(
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
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "record_design_does_not_record_real_human_decision",
        "record_design_does_not_infer_human_approval",
        "record_design_does_not_approve_candidate_patch",
        "record_design_does_not_create_candidate_patch",
        "record_design_does_not_authorize_candidate_patch",
        "record_design_does_not_authorize_generator",
        "record_design_does_not_authorize_dependencies",
        "record_design_does_not_authorize_side_effects",
        "record_design_does_not_authorize_artifact_generation",
        "record_design_does_not_authorize_artifact_reading",
        "record_design_does_not_authorize_artifact_writing",
        "record_design_does_not_authorize_source_scanning",
        "record_design_does_not_authorize_raw_text_materialization",
        "record_design_does_not_authorize_embedding_generation",
        "record_design_does_not_authorize_vector_generation",
        "record_design_does_not_authorize_provider_execution",
        "record_design_does_not_authorize_runtime_semantic_enablement",
        "record_design_does_not_authorize_router_authority",
        "record_design_does_not_write_freeze_memory",
        "record_design_does_not_auto_load_prompts",
    }
)

REQUIRED_RECORD_EFFECT_POLICY = frozenset(
    {
        "schema_only_record_has_no_decision_effect",
        "not_recorded_value_has_no_decision_effect",
        "future_approve_candidate_patch_design_only_allows_only_separate_candidate_patch_design_review",
        "future_approve_candidate_patch_design_only_does_not_authorize_generation",
        "future_reject_value_blocks_candidate_patch_until_new_decision",
        "future_defer_value_blocks_candidate_patch_until_new_decision",
        "future_more_context_value_blocks_candidate_patch_until_context_is_loaded",
        "any_future_recorded_value_requires_separate_governed_recording_patch",
        "any_future_candidate_patch_requires_separate_governed_patch",
        "any_future_generation_requires_separate_governed_patch",
        "any_request_to_use_record_as_runtime_authority_is_blocked",
        "any_request_to_use_record_as_router_authority_is_blocked",
        "any_request_to_use_record_as_artifact_authority_is_blocked",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_explicit_human_decision_is_missing",
        "stop_if_decision_scope_is_ambiguous",
        "stop_if_full_freeze_context_is_required_but_not_loaded",
        "stop_if_decision_recording_is_requested_in_this_schema_patch",
        "stop_if_candidate_patch_creation_is_requested",
        "stop_if_generator_authorization_is_requested",
        "stop_if_dependency_install_is_requested",
        "stop_if_side_effect_authorization_is_requested",
        "stop_if_artifact_generation_is_requested",
        "stop_if_artifact_read_or_write_is_requested",
        "stop_if_source_scanning_is_requested",
        "stop_if_raw_text_materialization_is_requested",
        "stop_if_embedding_or_vector_generation_is_requested",
        "stop_if_provider_or_model_execution_is_requested",
        "stop_if_runtime_or_router_authority_is_requested",
        "stop_if_other_box_logic_would_be_modified",
    }
)

TRIGGER_TERMS_REQUIRING_FUTURE_PATCH = frozenset(
    {
        "approve",
        "approved",
        "record decision",
        "actual decision",
        "human decided",
        "permit",
        "authorize",
        "candidate patch now",
        "create candidate patch",
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
        "decision values",
        "evidence checklist",
        "review only",
        "show checklist",
    }
)


def _sorted(values: Sequence[str] | set[str] | frozenset[str]) -> list[str]:
    return sorted(values)


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in _sorted(REQUIRED_DISABLED_FLAGS_FALSE)}


def build_generator_candidate_human_decision_record_contract() -> dict[str, Any]:
    """Return the inert human decision record schema after the gate."""
    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS,
        "declared_generator_candidate_human_decision_record_schema_only": True,
        "human_decision_record_scope": REQUIRED_HUMAN_DECISION_RECORD_SCOPE,
        "current_human_decision_record_state": "human_decision_record_not_recorded",
        "current_human_decision_record_effect": "no_effect_schema_only_not_recorded",
        "current_recorded_decision_value": "not_recorded",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "required_future_recording_inputs": _sorted(REQUIRED_FUTURE_RECORDING_INPUTS),
        "allowed_future_recorded_decision_values": _sorted(ALLOWED_FUTURE_RECORDED_DECISION_VALUES),
        "allowed_record_outputs": _sorted(REQUIRED_ALLOWED_RECORD_OUTPUTS),
        "prohibited_record_outputs": _sorted(REQUIRED_PROHIBITED_RECORD_OUTPUTS),
        "disabled_flags": _false_flags(),
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "record_effect_policy": _sorted(REQUIRED_RECORD_EFFECT_POLICY),
        "stop_conditions": _sorted(REQUIRED_STOP_CONDITIONS),
    }


def validate_generator_candidate_human_decision_record_contract(
    record: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the inert record schema and return denial-oriented facts."""
    errors: list[str] = []

    missing = REQUIRED_HUMAN_DECISION_RECORD_FIELDS.difference(record)
    if missing:
        errors.append("missing required human decision record fields: " + ", ".join(sorted(missing)))

    forbidden = FORBIDDEN_RECORD_FIELDS.intersection(record)
    if forbidden:
        errors.append("forbidden record field present: " + ", ".join(sorted(forbidden)))

    if record.get("schema_id") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID:
        errors.append("schema_id mismatch")
    if record.get("schema_version") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if record.get("schema_status") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS:
        errors.append("schema_status mismatch")
    if record.get("declared_generator_candidate_human_decision_record_schema_only") is not True:
        errors.append("schema-only declaration must be true")
    if record.get("human_decision_record_scope") != REQUIRED_HUMAN_DECISION_RECORD_SCOPE:
        errors.append("human_decision_record_scope mismatch")
    if record.get("current_human_decision_record_state") not in ALLOWED_CURRENT_HUMAN_DECISION_RECORD_STATES:
        errors.append("current human decision record state is not allowed")
    if record.get("current_human_decision_record_state") != "human_decision_record_not_recorded":
        errors.append("current human decision record state must remain human_decision_record_not_recorded")
    if record.get("current_human_decision_record_effect") != "no_effect_schema_only_not_recorded":
        errors.append("current human decision record effect must remain no_effect_schema_only_not_recorded")
    if record.get("current_recorded_decision_value") != "not_recorded":
        errors.append("current recorded decision value must remain not_recorded")

    set_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_future_recording_inputs", REQUIRED_FUTURE_RECORDING_INPUTS),
        ("allowed_future_recorded_decision_values", ALLOWED_FUTURE_RECORDED_DECISION_VALUES),
        ("allowed_record_outputs", REQUIRED_ALLOWED_RECORD_OUTPUTS),
        ("prohibited_record_outputs", REQUIRED_PROHIBITED_RECORD_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("record_effect_policy", REQUIRED_RECORD_EFFECT_POLICY),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for key, required in set_checks:
        values = record.get(key, [])
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            errors.append(f"{key} must be a sequence")
            continue
        if not required.issubset(set(values)):
            errors.append(f"{key} missing required values")

    flags = record.get("disabled_flags", {})
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
        "schema_id": record.get("schema_id"),
        "schema_version": record.get("schema_version"),
        "current_human_decision_record_state": record.get("current_human_decision_record_state"),
        "current_recorded_decision_value": record.get("current_recorded_decision_value"),
        "real_human_decision_recorded_by_human_decision_record": flags.get("real_human_decision_recording_enabled", True),
        "human_approval_inferred_from_preparation_chain": flags.get("human_approval_inference_enabled", True),
        "candidate_patch_approval_recorded": flags.get("candidate_patch_approval_enabled", True),
        "dependency_install_authorized": flags.get("dependency_install_enabled", True),
        "side_effect_authorized": flags.get("side_effect_authorization_enabled", True),
        "generator_candidate_patch_created": flags.get("generator_candidate_patch_creation_enabled", True),
        "generator_candidate_patch_authorized": flags.get("generator_candidate_patch_authorization_enabled", True),
        "generator_implementation_authorized": flags.get("generator_implementation_enabled", True),
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
        "requires_prior_generator_candidate_human_decision_gate": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_human_decision_record_request(user_text: str) -> dict[str, Any]:
    """Classify a request against the schema-only human decision record boundary."""
    normalized = " ".join(str(user_text).lower().split())
    has_trigger = any(term in normalized for term in TRIGGER_TERMS_REQUIRING_FUTURE_PATCH)
    has_schema_talk = any(term in normalized for term in SCHEMA_TALK_TERMS)

    base = {
        "current_recorded_decision_value": "not_recorded",
        "real_human_decision_recorded_by_human_decision_record": False,
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
        "requires_prior_generator_candidate_human_decision_gate": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }

    if has_trigger:
        return {
            **base,
            "allowed_now": False,
            "permitted_output": "none",
            "reason": "request would record approval, create a candidate patch, or enable generation/runtime behavior",
        }

    return {
        **base,
        "allowed_now": bool(has_schema_talk),
        "permitted_output": "human_decision_record_schema" if has_schema_talk else "none",
        "reason": "schema-only discussion is allowed; decision recording and generation remain disabled",
    }
