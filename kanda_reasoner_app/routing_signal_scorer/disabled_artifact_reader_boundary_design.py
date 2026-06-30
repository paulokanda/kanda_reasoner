"""Disabled precomputed artifact reader boundary design contract.

This module is intentionally standard-library-only and design-only. It does
not implement an artifact reader, load precomputed semantic evidence
artifacts at startup or runtime, materialize raw text, materialize vector
values, build vector indexes, instantiate providers, run evaluation, tune
thresholds, enable semantic runtime behavior, modify the prompt router, or
mutate project state. It validates the disabled boundary contract for a
future manually invoked artifact reader before any separate governed reader
implementation can be considered.
"""

from __future__ import annotations


__all__ = [
    'build_disabled_artifact_reader_boundary_contract',
    'classify_artifact_reader_activation_request',
    'validate_disabled_artifact_reader_boundary_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


DISABLED_ARTIFACT_READER_FEATURE_ID = "routing_signal_scorer_v3_disabled_artifact_reader_boundary_design_v1"
DISABLED_ARTIFACT_READER_SCHEMA_VERSION = "3.9-disabled-artifact-reader-boundary-design"
DISABLED_ARTIFACT_READER_STATUS = "design_contract_only_no_reader_no_loading_no_runtime_behavior_change"

REQUIRED_READER_CONTRACT_FIELDS = frozenset(
    {
        "contract_id",
        "schema_version",
        "reader_design_status",
        "declared_design_only",
        "artifact_source_requirements",
        "required_reader_gates",
        "disabled_flags",
        "forbidden_actions",
        "permitted_outputs",
        "no_authority_assertions",
    }
)

ALLOWED_READER_STATUSES = frozenset(
    {
        "design_only",
        "boundary_ready",
        "boundary_frozen",
        "rejected",
    }
)

REQUIRED_ARTIFACT_SOURCE_REQUIREMENTS = frozenset(
    {
        "precomputed_artifact_design_must_be_frozen",
        "artifact_must_be_schema_validated_before_reader_use",
        "artifact_must_reference_frozen_manifest",
        "artifact_must_reference_frozen_gold_set",
        "artifact_must_exclude_raw_text",
        "artifact_must_exclude_embedding_values",
        "artifact_must_exclude_vector_values",
        "artifact_must_exclude_provider_config",
        "artifact_must_exclude_runtime_enablement_flags",
        "artifact_structural_hash_required",
        "artifact_schema_version_required",
    }
)

REQUIRED_READER_GATES = frozenset(
    {
        "manual_invocation_required",
        "separate_governed_reader_patch_required",
        "artifact_schema_validation_required",
        "artifact_frozen_reference_check_required",
        "no_raw_text_materialization_check_required",
        "no_vector_materialization_check_required",
        "no_authority_fields_check_required",
        "no_runtime_enablement_check_required",
        "review_evidence_only_check_required",
        "freeze_required_before_reader_visibility",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "artifact_reader_implemented",
        "artifact_reader_enabled",
        "startup_artifact_loading_enabled",
        "runtime_artifact_loading_enabled",
        "background_artifact_loading_enabled",
        "file_watcher_artifact_loading_enabled",
        "artifact_auto_discovery_enabled",
        "artifact_auto_refresh_enabled",
        "raw_text_materialization_enabled",
        "embedding_value_materialization_enabled",
        "vector_value_materialization_enabled",
        "vector_index_loading_enabled",
        "provider_execution_enabled",
        "model_load_enabled",
        "external_api_enabled",
        "evaluation_execution_enabled",
        "threshold_auto_tuning_enabled",
        "semantic_runtime_enabled",
        "prompt_router_mutation_enabled",
        "write_freeze_memory_enabled",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "implement_artifact_reader",
        "enable_artifact_reader",
        "load_artifact_at_startup",
        "load_artifact_at_runtime",
        "auto_discover_artifacts",
        "auto_refresh_artifacts",
        "watch_artifact_files",
        "materialize_raw_text",
        "materialize_embedding_values",
        "materialize_vector_values",
        "load_vector_index",
        "instantiate_provider",
        "load_model",
        "call_external_api",
        "run_evaluation",
        "tune_thresholds",
        "persist_user_queries",
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
        "artifact_reader_boundary_status_report",
        "artifact_reader_preconditions_report",
        "artifact_reader_denial_report",
        "artifact_schema_validation_checklist",
        "human_review_queue_only",
        "review_evidence_only",
        "no_runtime_enablement",
        "no_prompt_loading",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "reader_output_is_advisory_only",
        "reader_output_is_review_evidence_only",
        "reader_must_not_choose_route",
        "reader_must_not_choose_required_prompts",
        "reader_must_not_decide_may_proceed",
        "reader_must_not_load_prompts",
        "reader_must_not_mutate_router",
        "reader_must_not_write_freeze_memory",
        "canon_remains_final_authority",
    }
)

FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {
        "route",
        "final_route",
        "route_decision",
        "required_prompts",
        "load_prompts",
        "may_proceed",
        "may_proceed_now",
        "decision",
        "authority",
        "override",
        "write_freeze_memory",
        "mutate_prompt_router",
        "semantic_runtime_enabled",
    }
)

FORBIDDEN_RAW_TEXT_FIELDS = frozenset(
    {
        "raw_text",
        "raw_prompt_text",
        "raw_user_query",
        "user_query_text",
        "private_project_text",
        "freeze_entry_text",
        "prompt_body_text",
        "terminal_log_text",
        "conversation_text",
    }
)

FORBIDDEN_VECTOR_PROVIDER_RUNTIME_FIELDS = frozenset(
    {
        "embedding",
        "embeddings",
        "embedding_values",
        "vector",
        "vectors",
        "vector_values",
        "vector_index",
        "vector_index_payload",
        "provider",
        "provider_config",
        "model",
        "model_config",
        "credential",
        "credentials",
        "api_key",
        "network_endpoint",
        "runtime_loader",
        "startup_loader",
    }
)


def _as_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return value


def _as_sequence(value: Any, name: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a sequence")
    return value


def _missing(required: frozenset[str], actual: Any) -> tuple[str, ...]:
    return tuple(sorted(required.difference(set(_as_sequence(actual, "sequence")))))


def build_disabled_artifact_reader_boundary_contract() -> dict[str, Any]:
    """Return the disabled artifact reader boundary design contract."""

    return {
        "contract_id": DISABLED_ARTIFACT_READER_FEATURE_ID,
        "schema_version": DISABLED_ARTIFACT_READER_SCHEMA_VERSION,
        "reader_design_status": "design_only",
        "declared_design_only": True,
        "artifact_source_requirements": sorted(REQUIRED_ARTIFACT_SOURCE_REQUIREMENTS),
        "required_reader_gates": sorted(REQUIRED_READER_GATES),
        "disabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "permitted_outputs": sorted(REQUIRED_PERMITTED_OUTPUTS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
    }


def validate_disabled_artifact_reader_boundary_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the disabled reader boundary without enabling any behavior."""

    candidate = _as_mapping(contract, "contract")
    missing_fields = sorted(REQUIRED_READER_CONTRACT_FIELDS.difference(candidate))
    errors: list[str] = []
    if missing_fields:
        errors.append("missing required fields: " + ", ".join(missing_fields))

    if candidate.get("contract_id") != DISABLED_ARTIFACT_READER_FEATURE_ID:
        errors.append("contract_id mismatch")
    if candidate.get("schema_version") != DISABLED_ARTIFACT_READER_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("reader_design_status") not in ALLOWED_READER_STATUSES:
        errors.append("unsupported reader design status")
    if candidate.get("declared_design_only") is not True:
        errors.append("declared_design_only must be true")

    if "artifact_source_requirements" in candidate:
        missing = _missing(REQUIRED_ARTIFACT_SOURCE_REQUIREMENTS, candidate["artifact_source_requirements"])
        if missing:
            errors.append("missing artifact source requirements: " + ", ".join(missing))
    if "required_reader_gates" in candidate:
        missing = _missing(REQUIRED_READER_GATES, candidate["required_reader_gates"])
        if missing:
            errors.append("missing reader gates: " + ", ".join(missing))
    if "forbidden_actions" in candidate:
        missing = _missing(REQUIRED_FORBIDDEN_ACTIONS, candidate["forbidden_actions"])
        if missing:
            errors.append("missing forbidden actions: " + ", ".join(missing))
    if "permitted_outputs" in candidate:
        missing = _missing(REQUIRED_PERMITTED_OUTPUTS, candidate["permitted_outputs"])
        if missing:
            errors.append("missing permitted outputs: " + ", ".join(missing))
    if "no_authority_assertions" in candidate:
        missing = _missing(REQUIRED_NO_AUTHORITY_ASSERTIONS, candidate["no_authority_assertions"])
        if missing:
            errors.append("missing no-authority assertions: " + ", ".join(missing))

    flags = _as_mapping(candidate.get("disabled_flags", {}), "disabled_flags")
    for flag in REQUIRED_DISABLED_FLAGS_FALSE:
        if flags.get(flag) is not False:
            errors.append(f"disabled flag must be false: {flag}")

    forbidden_field_names = (
        FORBIDDEN_AUTHORITY_FIELDS
        | FORBIDDEN_RAW_TEXT_FIELDS
        | FORBIDDEN_VECTOR_PROVIDER_RUNTIME_FIELDS
    )
    leaked = sorted(forbidden_field_names.intersection(candidate.keys()))
    if leaked:
        errors.append("forbidden field present: " + ", ".join(leaked))

    return {
        "valid": not errors,
        "errors": errors,
        "advisory_only": True,
        "review_evidence_only": True,
        "artifact_reader_enabled": False,
        "startup_loading_enabled": False,
        "runtime_loading_enabled": False,
        "semantic_runtime_enabled": False,
        "authority_granted": False,
        "requires_future_governed_patch": True,
    }


def classify_artifact_reader_activation_request(action: str) -> dict[str, Any]:
    """Deny activation-like reader requests in this design-only phase."""

    normalized = action.lower().strip()
    activation_terms = (
        "enable",
        "load",
        "read artifact",
        "reader",
        "runtime",
        "startup",
        "semantic runtime",
        "vector",
        "embedding",
        "provider",
        "route",
        "threshold",
    )
    is_activation_like = any(term in normalized for term in activation_terms)
    return {
        "action": action,
        "activation_like": is_activation_like,
        "allowed_now": False,
        "artifact_reader_authorized": False,
        "artifact_loading_authorized": False,
        "raw_text_materialization_authorized": False,
        "vector_materialization_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "authority_granted": False,
        "requires_future_governed_patch": True,
        "advisory_only": True,
        "reason": "artifact reader is a disabled boundary design only",
    }
