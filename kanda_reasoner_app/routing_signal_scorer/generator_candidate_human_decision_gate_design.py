"""Generator candidate human decision gate design for routing scorer v3.

This module is intentionally standard-library-only and human-decision-gate-only.
It follows the generator-candidate preparation closure shield and makes explicit
that a real human decision is still required before any future generator
candidate patch can be proposed or implemented.

It does not record a real human decision, does not infer approval from prior
schemas, does not create or authorize a candidate patch, does not authorize a
generator, does not install dependencies, does not authorize side effects, does
not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors,
does not instantiate providers, does not run semantic scoring, does not modify
router authority, and does not change runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_FEATURE_ID = (
    "routing_signal_scorer_v3_generator_candidate_human_decision_gate_design_v1"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_SCHEMA_VERSION = (
    "3.29-generator-candidate-human-decision-gate-design"
)
GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_STATUS = (
    "generator_candidate_human_decision_gate_only_no_decision_recorded_no_candidate_patch_no_generator_authorization"
)

REQUIRED_HUMAN_DECISION_GATE_FIELDS = frozenset(
    {
        "schema_id",
        "schema_version",
        "schema_status",
        "declared_generator_candidate_human_decision_gate_only",
        "human_decision_gate_scope",
        "current_human_decision_gate_state",
        "current_human_decision_gate_effect",
        "required_prior_milestones",
        "required_human_decision_inputs",
        "allowed_future_decision_values",
        "allowed_gate_outputs",
        "prohibited_gate_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "decision_gate_effect_policy",
        "stop_conditions",
    }
)

REQUIRED_HUMAN_DECISION_GATE_SCOPE = "generator_candidate_human_decision_gate_only"
ALLOWED_CURRENT_HUMAN_DECISION_GATE_STATES = frozenset(
    {
        "human_decision_not_recorded",
        "awaiting_explicit_human_decision",
        "awaiting_full_freeze_context",
        "deferred",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
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

REQUIRED_HUMAN_DECISION_INPUTS = frozenset(
    {
        "explicit_human_decision_text",
        "decision_actor_or_source",
        "decision_timestamp_or_session_reference",
        "decision_scope",
        "referenced_preparation_closure_freeze_id",
        "referenced_review_bundle_freeze_id",
        "touched_paths_allowed_for_future_candidate_patch",
        "candidate_patch_non_goals_acknowledged",
        "artifact_io_non_goals_acknowledged",
        "source_scanning_non_goals_acknowledged",
        "runtime_router_non_goals_acknowledged",
        "rollback_or_stop_condition_acknowledged",
    }
)

ALLOWED_FUTURE_DECISION_VALUES = frozenset(
    {
        "approve_candidate_patch_design_only",
        "reject_candidate_patch_design",
        "defer_candidate_patch_design",
        "request_more_freeze_context",
        "request_more_architectural_review",
        "stop_after_preparation_closure",
    }
)

REQUIRED_ALLOWED_GATE_OUTPUTS = frozenset(
    {
        "human_decision_gate_schema",
        "human_decision_input_checklist",
        "missing_human_decision_notice",
        "future_decision_value_vocabulary",
        "decision_scope_requirements",
        "candidate_patch_stop_conditions",
        "no_real_human_decision_recorded",
        "no_approval_inferred_from_preparation_chain",
        "no_candidate_patch_created",
        "no_candidate_patch_authorized",
        "no_generator_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_GATE_OUTPUTS = frozenset(
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

FORBIDDEN_GATE_FIELDS = REQUIRED_PROHIBITED_GATE_OUTPUTS

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "gate_does_not_record_real_human_decision",
        "gate_does_not_infer_human_approval",
        "gate_does_not_create_candidate_patch",
        "gate_does_not_authorize_candidate_patch",
        "gate_does_not_authorize_generator",
        "gate_does_not_authorize_dependencies",
        "gate_does_not_authorize_side_effects",
        "gate_does_not_authorize_artifact_generation",
        "gate_does_not_authorize_artifact_reading",
        "gate_does_not_authorize_artifact_writing",
        "gate_does_not_authorize_source_scanning",
        "gate_does_not_authorize_raw_text_materialization",
        "gate_does_not_authorize_embedding_generation",
        "gate_does_not_authorize_vector_generation",
        "gate_does_not_authorize_provider_execution",
        "gate_does_not_authorize_runtime_semantic_enablement",
        "gate_does_not_authorize_router_authority",
        "gate_does_not_write_freeze_memory",
        "gate_does_not_auto_load_prompts",
    }
)

REQUIRED_STOP_CONDITIONS = frozenset(
    {
        "stop_if_explicit_human_decision_is_missing",
        "stop_if_decision_scope_is_ambiguous",
        "stop_if_full_freeze_context_is_required_but_not_loaded",
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


def _as_set(value: Any) -> set[Any]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, Sequence):
        return set(value)
    return set()


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)}


def build_generator_candidate_human_decision_gate_contract() -> dict[str, Any]:
    """Return the schema-only human decision gate after preparation closure."""
    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_STATUS,
        "declared_generator_candidate_human_decision_gate_only": True,
        "human_decision_gate_scope": REQUIRED_HUMAN_DECISION_GATE_SCOPE,
        "current_human_decision_gate_state": "human_decision_not_recorded",
        "current_human_decision_gate_effect": "no_effect_schema_only_human_decision_not_recorded",
        "required_prior_milestones": sorted(REQUIRED_PRIOR_MILESTONES),
        "required_human_decision_inputs": sorted(REQUIRED_HUMAN_DECISION_INPUTS),
        "allowed_future_decision_values": sorted(ALLOWED_FUTURE_DECISION_VALUES),
        "allowed_gate_outputs": sorted(REQUIRED_ALLOWED_GATE_OUTPUTS),
        "prohibited_gate_outputs": sorted(REQUIRED_PROHIBITED_GATE_OUTPUTS),
        "disabled_flags": _false_flags(),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "decision_gate_effect_policy": (
            "This human decision gate only states that a separate explicit human "
            "decision is required. It cannot record or infer approval, create or "
            "authorize a candidate patch, authorize generation, install dependencies, "
            "authorize side effects, perform artifact IO, scan sources, enable runtime "
            "behavior, grant router authority, auto-load prompts, or write freeze memory."
        ),
        "stop_conditions": sorted(REQUIRED_STOP_CONDITIONS),
    }


def validate_generator_candidate_human_decision_gate_contract(
    contract: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the schema-only human decision gate without enabling behavior."""
    errors: list[str] = []

    for field in sorted(REQUIRED_HUMAN_DECISION_GATE_FIELDS):
        if field not in contract:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_GATE_FIELDS):
        if field in contract:
            errors.append(f"forbidden gate field present: {field}")

    if contract.get("schema_id") != GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_FEATURE_ID:
        errors.append("schema_id mismatch")
    if contract.get("schema_version") != GENERATOR_CANDIDATE_HUMAN_DECISION_GATE_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if contract.get("human_decision_gate_scope") != REQUIRED_HUMAN_DECISION_GATE_SCOPE:
        errors.append("human_decision_gate_scope mismatch")
    if contract.get("current_human_decision_gate_state") not in ALLOWED_CURRENT_HUMAN_DECISION_GATE_STATES:
        errors.append("current_human_decision_gate_state is not allowed")
    if contract.get("declared_generator_candidate_human_decision_gate_only") is not True:
        errors.append("human decision gate must be declared schema-only")

    subset_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_human_decision_inputs", REQUIRED_HUMAN_DECISION_INPUTS),
        ("allowed_future_decision_values", ALLOWED_FUTURE_DECISION_VALUES),
        ("allowed_gate_outputs", REQUIRED_ALLOWED_GATE_OUTPUTS),
        ("prohibited_gate_outputs", REQUIRED_PROHIBITED_GATE_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for field, required in subset_checks:
        actual = _as_set(contract.get(field, []))
        missing = required - actual
        if missing:
            errors.append(f"{field} missing required values: {sorted(missing)}")

    disabled_flags = contract.get("disabled_flags", {})
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
    else:
        for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
            if flag not in disabled_flags:
                errors.append(f"missing disabled flag: {flag}")
            elif disabled_flags[flag] is not False:
                errors.append(f"disabled flag must be false: {flag}")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "schema_id": contract.get("schema_id"),
        "schema_version": contract.get("schema_version"),
        "current_human_decision_gate_state": contract.get("current_human_decision_gate_state"),
        "real_human_decision_recorded_by_human_decision_gate": False,
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
        "artifact_loading_authorized": False,
        "artifact_discovery_authorized": False,
        "source_scanning_authorized": False,
        "raw_text_materialization_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_generation_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "router_authority_authorized": False,
        "public_runtime_export_authorized": False,
        "freeze_memory_writing_authorized": False,
        "prompt_auto_loading_authorized": False,
        "requires_explicit_human_decision": True,
        "requires_prior_generator_candidate_preparation_closure_shield": True,
        "requires_future_governed_decision_record_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_human_decision_gate_request(request_text: str) -> dict[str, Any]:
    """Classify human-decision-gate requests without recording approval."""
    text = request_text.lower()
    forbidden_markers = (
        "approve",
        "approved",
        "authorization",
        "authorize",
        "record decision",
        "human says yes",
        "create candidate patch",
        "implement generator",
        "generate artifact",
        "write artifact",
        "read artifact",
        "scan source",
        "scan prompt",
        "materialize raw text",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "router authority",
        "may proceed",
        "install dependency",
        "side effect",
        "freeze write",
        "auto load",
    )
    allowed_markers = (
        "schema",
        "checklist",
        "gate",
        "human decision",
        "missing decision",
        "show",
        "review",
        "requirements",
    )
    blocked = any(marker in text for marker in forbidden_markers)
    allowed_schema_view = any(marker in text for marker in allowed_markers)
    allowed_now = allowed_schema_view and not blocked
    return {
        "allowed_now": allowed_now,
        "permitted_output": "generator_candidate_human_decision_gate_schema" if allowed_now else None,
        "current_human_decision_gate_state": "human_decision_not_recorded",
        "real_human_decision_recorded_by_human_decision_gate": False,
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
        "freeze_memory_writing_authorized": False,
        "prompt_auto_loading_authorized": False,
        "requires_explicit_human_decision": True,
        "requires_prior_generator_candidate_preparation_closure_shield": True,
        "requires_future_governed_decision_record_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
