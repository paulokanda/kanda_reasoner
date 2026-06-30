# project-path: kanda_reasoner_app/routing_signal_scorer/disabled_generation_boundary_design.py
"""Disabled generation boundary design contract for future semantic artifacts.

This module is intentionally standard-library-only and design-only. It does not
implement artifact generation, write artifacts, read artifacts, load artifacts,
generate embeddings, materialize vectors, build indexes, instantiate providers,
run evaluation, tune thresholds, enable semantic runtime behavior, modify the
prompt router, or mutate project state. It validates the disabled-by-default
boundary that any future semantic artifact generator must satisfy before a
separate governed implementation can be considered.
"""

from __future__ import annotations


__all__ = [
    'build_disabled_generation_boundary_contract',
    'classify_generation_activation_request',
    'validate_disabled_generation_boundary_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


DISABLED_GENERATION_BOUNDARY_FEATURE_ID = "routing_signal_scorer_v3_disabled_generation_boundary_design_v1"
DISABLED_GENERATION_BOUNDARY_SCHEMA_VERSION = "3.12-disabled-generation-boundary-design"
DISABLED_GENERATION_BOUNDARY_STATUS = "design_contract_only_generation_disabled_no_generator_no_ml_behavior_change"

REQUIRED_GENERATION_BOUNDARY_FIELDS = frozenset(
    {
        "contract_id",
        "schema_version",
        "generation_boundary_status",
        "declared_design_only",
        "default_generation_mode",
        "allowed_future_generation_modes",
        "required_future_generation_inputs",
        "required_future_generation_gates",
        "disabled_flags",
        "forbidden_actions",
        "permitted_outputs",
        "no_authority_assertions",
    }
)

ALLOWED_GENERATION_BOUNDARY_STATUSES = frozenset(
    {
        "design_only",
        "disabled_boundary_ready",
        "disabled_boundary_frozen",
        "rejected",
    }
)

REQUIRED_DEFAULT_GENERATION_MODE = "disabled_no_generation"

REQUIRED_ALLOWED_FUTURE_GENERATION_MODES = frozenset(
    {
        "disabled_no_generation",
        "manual_plan_only",
        "manual_dry_run_report_only",
        "human_reviewed_static_fixture_update",
        "separately_governed_local_generator_candidate",
    }
)

REQUIRED_FUTURE_GENERATION_INPUTS = frozenset(
    {
        "frozen_metadata_vector_manifest_schema",
        "frozen_offline_evaluation_gold_set_schema",
        "frozen_offline_corpus_governance_contract",
        "frozen_precomputed_artifact_schema_contract",
        "frozen_disabled_reader_boundary_contract",
        "human_approved_generation_plan",
        "dependency_review_if_generator_requires_new_dependency",
        "privacy_review_for_source_material",
        "resource_budget_review",
        "manual_invocation_record",
    }
)

REQUIRED_FUTURE_GENERATION_GATES = frozenset(
    {
        "separate_governed_patch_required",
        "tests_first_required",
        "human_confirmation_required",
        "local_first_required",
        "no_background_generation_required",
        "no_startup_generation_required",
        "no_runtime_generation_required",
        "no_file_watcher_generation_required",
        "redaction_gate_required",
        "no_raw_text_materialization_gate_required",
        "no_vector_value_materialization_gate_required",
        "authority_leakage_gate_required",
        "freeze_required_before_use",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_overwrite_enabled",
        "artifact_reader_enabled",
        "artifact_loading_enabled",
        "startup_generation_enabled",
        "runtime_generation_enabled",
        "background_generation_enabled",
        "file_watcher_generation_enabled",
        "prompt_library_scan_enabled",
        "freeze_entry_scan_enabled",
        "raw_text_materialization_enabled",
        "embedding_generation_enabled",
        "embedding_value_materialization_enabled",
        "vector_value_materialization_enabled",
        "vector_index_generation_enabled",
        "provider_execution_enabled",
        "network_access_enabled",
        "credential_loading_enabled",
        "evaluation_execution_enabled",
        "threshold_auto_tuning_enabled",
        "semantic_runtime_enabled",
        "prompt_router_mutation_enabled",
        "prompt_auto_loading_enabled",
        "may_proceed_generation_enabled",
        "write_freeze_memory_enabled",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "implement_generator_now",
        "generate_artifact_now",
        "write_artifact_now",
        "overwrite_artifact_now",
        "read_generated_artifact",
        "load_artifact_at_startup",
        "load_artifact_at_runtime",
        "run_generation_at_startup",
        "run_generation_at_runtime",
        "run_generation_in_background",
        "run_generation_from_file_watcher",
        "scan_prompt_library_for_generation",
        "scan_freeze_entries_for_generation",
        "materialize_raw_prompt_text",
        "materialize_raw_user_query_text",
        "materialize_freeze_entry_text",
        "generate_embeddings",
        "materialize_embedding_values",
        "materialize_vector_values",
        "create_vector_index",
        "instantiate_provider",
        "call_external_api",
        "load_credentials",
        "run_evaluation",
        "auto_adjust_thresholds_after_generation",
        "enable_semantic_runtime",
        "modify_prompt_router",
        "auto_load_prompts",
        "write_freeze_memory",
        "produce_final_route",
        "produce_required_prompts",
        "produce_may_proceed_now",
    }
)

REQUIRED_PERMITTED_OUTPUTS = frozenset(
    {
        "generation_boundary_status_report",
        "generation_denial_report",
        "future_generation_checklist",
        "dependency_review_checklist",
        "privacy_review_checklist",
        "resource_budget_checklist",
        "human_review_queue_only",
        "manual_plan_draft_only",
        "dry_run_report_only",
        "review_evidence_only",
        "no_artifact_written",
        "no_runtime_enablement",
        "no_prompt_loading",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "generation_boundary_is_design_only",
        "generation_results_would_be_evidence_only",
        "generator_must_not_choose_route",
        "generator_must_not_choose_required_prompts",
        "generator_must_not_decide_may_proceed",
        "generator_must_not_load_prompts",
        "generator_must_not_mutate_router",
        "generator_must_not_enable_semantic_runtime",
        "generator_must_not_write_freeze_memory",
        "canon_remains_final_authority",
    }
)

FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {
        "final_route",
        "required_prompts",
        "missing_context",
        "missing_behavior",
        "may_proceed_now",
        "route_override",
        "prompt_override",
        "authority_granted",
        "semantic_runtime_enabled",
        "router_mutation",
        "write_freeze_memory",
    }
)

FORBIDDEN_RAW_TEXT_FIELDS = frozenset(
    {
        "raw_user_query",
        "raw_user_queries",
        "prompt_body_text",
        "prompt_text",
        "freeze_entry_text",
        "terminal_log_text",
        "private_project_text",
        "source_document_text",
    }
)

FORBIDDEN_GENERATION_RUNTIME_FIELDS = frozenset(
    {
        "artifact_path",
        "artifact_payload",
        "generated_artifact",
        "embedding",
        "embeddings",
        "embedding_values",
        "vector",
        "vectors",
        "vector_values",
        "vector_index",
        "provider_name",
        "provider_config",
        "model_name",
        "model_path",
        "external_api_key",
        "credential_path",
        "network_endpoint",
    }
)


def _as_set(value: Any) -> set[str]:
    """Support as set behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    if isinstance(value, str):
        return {value}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return {str(item) for item in value}
    return set()


def build_disabled_generation_boundary_contract() -> dict[str, Any]:
    """Return the design-only disabled generation boundary contract."""

    return {
        "contract_id": DISABLED_GENERATION_BOUNDARY_FEATURE_ID,
        "schema_version": DISABLED_GENERATION_BOUNDARY_SCHEMA_VERSION,
        "generation_boundary_status": "design_only",
        "declared_design_only": True,
        "default_generation_mode": REQUIRED_DEFAULT_GENERATION_MODE,
        "allowed_future_generation_modes": sorted(REQUIRED_ALLOWED_FUTURE_GENERATION_MODES),
        "required_future_generation_inputs": sorted(REQUIRED_FUTURE_GENERATION_INPUTS),
        "required_future_generation_gates": sorted(REQUIRED_FUTURE_GENERATION_GATES),
        "disabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "permitted_outputs": sorted(REQUIRED_PERMITTED_OUTPUTS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
    }


def validate_disabled_generation_boundary_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a disabled generation boundary contract without enabling it."""

    errors: list[str] = []

    missing_fields = sorted(REQUIRED_GENERATION_BOUNDARY_FIELDS.difference(candidate.keys()))
    if missing_fields:
        errors.append("missing required fields: " + ", ".join(missing_fields))

    if candidate.get("contract_id") != DISABLED_GENERATION_BOUNDARY_FEATURE_ID:
        errors.append("contract_id must remain " + DISABLED_GENERATION_BOUNDARY_FEATURE_ID)

    if candidate.get("schema_version") != DISABLED_GENERATION_BOUNDARY_SCHEMA_VERSION:
        errors.append("schema_version must remain " + DISABLED_GENERATION_BOUNDARY_SCHEMA_VERSION)

    if candidate.get("generation_boundary_status") not in ALLOWED_GENERATION_BOUNDARY_STATUSES:
        errors.append("generation_boundary_status is not allowed")

    if candidate.get("declared_design_only") is not True:
        errors.append("declared_design_only must be true")

    if candidate.get("default_generation_mode") != REQUIRED_DEFAULT_GENERATION_MODE:
        errors.append("default_generation_mode must remain disabled_no_generation")

    allowed_modes = _as_set(candidate.get("allowed_future_generation_modes"))
    if not REQUIRED_ALLOWED_FUTURE_GENERATION_MODES.issubset(allowed_modes):
        errors.append("missing required future generation modes")

    future_inputs = _as_set(candidate.get("required_future_generation_inputs"))
    if not REQUIRED_FUTURE_GENERATION_INPUTS.issubset(future_inputs):
        errors.append("missing required future generation inputs")

    future_gates = _as_set(candidate.get("required_future_generation_gates"))
    if not REQUIRED_FUTURE_GENERATION_GATES.issubset(future_gates):
        errors.append("missing required future generation gates")

    disabled_flags = candidate.get("disabled_flags")
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        disabled_flags = {}

    for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
        if flag not in disabled_flags:
            errors.append("missing disabled flag: " + flag)
        elif disabled_flags[flag] is not False:
            errors.append("disabled flag must be false: " + flag)

    forbidden_actions = _as_set(candidate.get("forbidden_actions"))
    if not REQUIRED_FORBIDDEN_ACTIONS.issubset(forbidden_actions):
        errors.append("missing forbidden generation actions")

    permitted_outputs = _as_set(candidate.get("permitted_outputs"))
    if not REQUIRED_PERMITTED_OUTPUTS.issubset(permitted_outputs):
        errors.append("missing permitted generation-boundary outputs")

    no_authority = _as_set(candidate.get("no_authority_assertions"))
    if not REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(no_authority):
        errors.append("missing no-authority generation assertions")

    for field_group_name, fields in [
        ("forbidden authority fields", FORBIDDEN_AUTHORITY_FIELDS),
        ("forbidden raw/private text fields", FORBIDDEN_RAW_TEXT_FIELDS),
        ("forbidden generation/runtime fields", FORBIDDEN_GENERATION_RUNTIME_FIELDS),
    ]:
        present = sorted(field for field in fields if field in candidate)
        if present:
            errors.append(field_group_name + " present: " + ", ".join(present))

    ok = not errors
    return {
        "ok": ok,
        "valid": ok,
        "errors": errors,
        "feature_id": DISABLED_GENERATION_BOUNDARY_FEATURE_ID,
        "schema_version": DISABLED_GENERATION_BOUNDARY_SCHEMA_VERSION,
        "generation_boundary_status": candidate.get("generation_boundary_status"),
        "design_only": candidate.get("declared_design_only") is True,
        "default_generation_mode": candidate.get("default_generation_mode"),
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reader_authorized": False,
        "startup_generation_authorized": False,
        "runtime_generation_authorized": False,
        "background_generation_authorized": False,
        "raw_text_materialization_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_generation_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "prompt_router_mutation_authorized": False,
        "prompt_auto_loading_authorized": False,
        "may_proceed_generation_authorized": False,
        "freeze_memory_write_authorized": False,
        "authority_granted": False,
        "review_evidence_only": True,
        "requires_future_governed_patch": True,
    }


def classify_generation_activation_request(action: str) -> dict[str, Any]:
    """Classify any request to turn on generation as denied for now."""

    normalized = " ".join(str(action or "").strip().lower().split())
    trigger_words = (
        "generate",
        "write artifact",
        "build artifact",
        "create artifact",
        "embedding",
        "vector",
        "provider",
        "startup",
        "runtime",
        "background",
        "file watcher",
        "enable semantic",
        "auto load",
        "may proceed",
    )
    matched_triggers = [word for word in trigger_words if word in normalized]

    return {
        "allowed_now": False,
        "action": str(action or ""),
        "matched_triggers": matched_triggers,
        "generation_boundary_status": "disabled",
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reader_authorized": False,
        "startup_generation_authorized": False,
        "runtime_generation_authorized": False,
        "background_generation_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "prompt_router_mutation_authorized": False,
        "freeze_memory_write_authorized": False,
        "requires_future_governed_patch": True,
        "reason": "generation boundary is disabled by design and requires a separate governed patch",
        "permitted_output": "generation_denial_report",
        "advisory_only": True,
    }
