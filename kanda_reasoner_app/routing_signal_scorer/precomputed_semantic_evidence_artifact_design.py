"""Precomputed semantic evidence artifact design contract.

This module is intentionally standard-library-only and design-only. It does
not generate artifacts, generate embeddings, store vector values, build
vector indexes, instantiate providers, load models, run evaluation, read raw
prompt-library files, read freeze entries, persist user requests, enable
semantic runtime behavior, modify the prompt router, or mutate project state.
It validates the disabled design contract for a future precomputed semantic
evidence artifact shape before any separate governed artifact generator can
be considered.
"""

from __future__ import annotations


__all__ = [
    'build_minimal_valid_precomputed_artifact_contract',
    'build_precomputed_artifact_design_status',
    'classify_precomputed_artifact_activation_request',
    'validate_precomputed_artifact_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


PRECOMPUTED_ARTIFACT_FEATURE_ID = "routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design_v1"
PRECOMPUTED_ARTIFACT_SCHEMA_VERSION = "3.8-precomputed-semantic-evidence-artifact-design"
PRECOMPUTED_ARTIFACT_STATUS = "design_contract_only_no_artifact_no_embedding_no_vector_no_runtime_behavior_change"

REQUIRED_PRECOMPUTED_ARTIFACT_FIELDS = frozenset(
    {
        "contract_id",
        "schema_version",
        "artifact_design_status",
        "declared_design_only",
        "source_manifest_requirements",
        "source_gold_set_requirements",
        "required_artifact_sections",
        "forbidden_artifact_sections",
        "required_validation_gates",
        "disabled_flags",
        "forbidden_actions",
        "permitted_outputs",
        "no_authority_assertions",
    }
)

ALLOWED_ARTIFACT_STATUSES = frozenset(
    {
        "design_only",
        "schema_ready",
        "schema_frozen",
        "rejected",
    }
)

REQUIRED_SOURCE_MANIFEST_REQUIREMENTS = frozenset(
    {
        "metadata_vector_manifest_must_be_frozen",
        "manifest_items_must_be_active_only",
        "manifest_items_must_exclude_raw_prompt_text",
        "manifest_items_must_exclude_user_queries",
        "manifest_items_must_exclude_freeze_entries",
        "manifest_items_must_exclude_vectors",
        "manifest_structural_hash_required",
        "manifest_schema_version_required",
    }
)

REQUIRED_SOURCE_GOLD_SET_REQUIREMENTS = frozenset(
    {
        "gold_set_schema_must_be_frozen",
        "gold_set_cases_synthetic_or_curated_only",
        "gold_set_category_coverage_required",
        "gold_set_metrics_declared_before_run",
        "gold_set_thresholds_declared_before_run",
        "gold_set_zero_authority_leakage_required",
        "gold_set_zero_privacy_leakage_required",
    }
)

REQUIRED_ARTIFACT_SECTIONS = frozenset(
    {
        "artifact_identity",
        "source_manifest_reference",
        "source_gold_set_reference",
        "schema_version",
        "generation_provenance_placeholder",
        "evidence_record_summaries",
        "validation_summary",
        "review_status",
        "no_authority_notice",
    }
)

REQUIRED_FORBIDDEN_ARTIFACT_SECTIONS = frozenset(
    {
        "raw_prompt_text",
        "raw_user_query_text",
        "private_project_text",
        "freeze_entry_text",
        "prompt_body_text",
        "terminal_log_text",
        "embedding_values",
        "vector_values",
        "vector_index_payload",
        "provider_config",
        "model_config",
        "credential_payload",
        "router_decision_payload",
    }
)

REQUIRED_VALIDATION_GATES = frozenset(
    {
        "schema_validation_required",
        "source_manifest_frozen_check_required",
        "source_gold_set_frozen_check_required",
        "no_raw_text_check_required",
        "no_vector_values_check_required",
        "no_authority_fields_check_required",
        "no_runtime_enablement_check_required",
        "review_evidence_only_check_required",
        "separate_governed_generation_patch_required",
        "freeze_required_before_runtime_visibility",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "artifact_generation_enabled",
        "precomputed_artifact_written",
        "embedding_generation_enabled",
        "embedding_values_allowed",
        "vector_values_allowed",
        "vector_index_generation_enabled",
        "provider_execution_enabled",
        "model_load_enabled",
        "external_api_enabled",
        "network_access_enabled",
        "evaluation_runner_enabled",
        "threshold_auto_tuning_enabled",
        "semantic_runtime_enabled",
        "startup_artifact_loading_enabled",
        "runtime_artifact_loading_enabled",
        "background_artifact_rebuild_enabled",
        "file_watcher_artifact_rebuild_enabled",
        "prompt_router_mutation_enabled",
        "write_freeze_memory_enabled",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "generate_precomputed_artifact",
        "write_precomputed_artifact",
        "generate_embeddings",
        "store_embedding_values",
        "store_vector_values",
        "create_vector_index",
        "instantiate_provider",
        "load_model",
        "call_external_api",
        "run_evaluation",
        "tune_thresholds",
        "read_raw_prompt_files",
        "read_freeze_entries",
        "persist_user_queries",
        "enable_semantic_runtime",
        "load_artifact_at_startup",
        "load_artifact_at_runtime",
        "rebuild_artifact_automatically",
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
        "artifact_design_status_report",
        "artifact_schema_checklist",
        "artifact_generation_preconditions_report",
        "artifact_denial_report",
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
        "artifact_outputs_are_evidence_only",
        "artifact_outputs_cannot_change_router_decision",
        "artifact_outputs_cannot_change_required_prompts",
        "artifact_outputs_cannot_change_may_proceed",
        "artifact_outputs_cannot_enable_semantic_runtime",
        "artifact_outputs_cannot_tune_thresholds",
        "artifact_outputs_cannot_write_freeze_memory",
    }
)

FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {
        "final_route",
        "required_prompts",
        "may_proceed_now",
        "route_override",
        "auto_load_prompts",
        "write_freeze_memory",
        "modify_startup",
        "modify_prompt_library",
        "modify_prompt_router",
        "enable_semantic_runtime",
        "threshold_override",
        "routing_decision",
        "provider_override",
        "corpus_override",
    }
)

FORBIDDEN_RAW_TEXT_FIELDS = frozenset(
    {
        "request_text",
        "raw_user_query",
        "raw_user_query_text",
        "user_query_text",
        "chat_history",
        "private_project_text",
        "freeze_entry_text",
        "prompt_file_text",
        "prompt_body_text",
        "terminal_log_text",
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
        "index_path",
        "provider",
        "provider_name",
        "provider_instance",
        "provider_config",
        "external_api_key",
        "credential_path",
        "model_name",
        "model_path",
        "model_url",
        "download_url",
        "artifact_path",
        "runtime_artifact_path",
    }
)


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _as_strings(value: Any) -> set[str]:
    if not _is_sequence(value):
        return set()
    return {item for item in value if isinstance(item, str)}


def _append_missing(errors: list[str], label: str, missing: set[str]) -> None:
    if missing:
        errors.append(f"missing {label}: {', '.join(sorted(missing))}")


def _find_forbidden_fields(mapping: Mapping[str, Any], forbidden: set[str] | frozenset[str]) -> set[str]:
    found: set[str] = set()
    for key, value in mapping.items():
        if key in forbidden:
            found.add(key)
        if isinstance(value, Mapping):
            found.update(_find_forbidden_fields(value, forbidden))
        elif _is_sequence(value):
            for item in value:
                if isinstance(item, Mapping):
                    found.update(_find_forbidden_fields(item, forbidden))
    return found


def build_precomputed_artifact_design_status() -> dict[str, Any]:
    return {
        "feature_id": PRECOMPUTED_ARTIFACT_FEATURE_ID,
        "schema_version": PRECOMPUTED_ARTIFACT_SCHEMA_VERSION,
        "status": PRECOMPUTED_ARTIFACT_STATUS,
        "artifact_generation_enabled": False,
        "precomputed_artifact_written": False,
        "embedding_generation_enabled": False,
        "embedding_values_allowed": False,
        "vector_values_allowed": False,
        "vector_index_generation_enabled": False,
        "provider_execution_enabled": False,
        "model_load_enabled": False,
        "external_api_enabled": False,
        "network_access_enabled": False,
        "evaluation_runner_enabled": False,
        "threshold_auto_tuning_enabled": False,
        "semantic_runtime_enabled": False,
        "startup_artifact_loading_enabled": False,
        "runtime_artifact_loading_enabled": False,
        "advisory_only": True,
        "review_evidence_only": True,
        "lexical_fallback_primary": True,
        "requires_separate_governed_generation_patch": True,
    }


def build_minimal_valid_precomputed_artifact_contract() -> dict[str, Any]:
    return {
        "contract_id": PRECOMPUTED_ARTIFACT_FEATURE_ID,
        "schema_version": PRECOMPUTED_ARTIFACT_SCHEMA_VERSION,
        "artifact_design_status": "design_only",
        "declared_design_only": True,
        "source_manifest_requirements": sorted(REQUIRED_SOURCE_MANIFEST_REQUIREMENTS),
        "source_gold_set_requirements": sorted(REQUIRED_SOURCE_GOLD_SET_REQUIREMENTS),
        "required_artifact_sections": sorted(REQUIRED_ARTIFACT_SECTIONS),
        "forbidden_artifact_sections": sorted(REQUIRED_FORBIDDEN_ARTIFACT_SECTIONS),
        "required_validation_gates": sorted(REQUIRED_VALIDATION_GATES),
        "disabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "permitted_outputs": sorted(REQUIRED_PERMITTED_OUTPUTS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
    }


def validate_precomputed_artifact_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    fields = set(contract)
    _append_missing(errors, "precomputed artifact fields", REQUIRED_PRECOMPUTED_ARTIFACT_FIELDS - fields)

    if contract.get("contract_id") != PRECOMPUTED_ARTIFACT_FEATURE_ID:
        errors.append("contract_id must match precomputed semantic evidence artifact feature id")
    if contract.get("schema_version") != PRECOMPUTED_ARTIFACT_SCHEMA_VERSION:
        errors.append("schema_version must match precomputed semantic evidence artifact schema version")
    if contract.get("artifact_design_status") not in ALLOWED_ARTIFACT_STATUSES:
        errors.append("artifact_design_status is not an allowed design status")
    if contract.get("declared_design_only") is not True:
        errors.append("declared_design_only must be true")

    _append_missing(
        errors,
        "source manifest requirements",
        REQUIRED_SOURCE_MANIFEST_REQUIREMENTS - _as_strings(contract.get("source_manifest_requirements")),
    )
    _append_missing(
        errors,
        "source gold-set requirements",
        REQUIRED_SOURCE_GOLD_SET_REQUIREMENTS - _as_strings(contract.get("source_gold_set_requirements")),
    )
    _append_missing(
        errors,
        "required artifact sections",
        REQUIRED_ARTIFACT_SECTIONS - _as_strings(contract.get("required_artifact_sections")),
    )
    _append_missing(
        errors,
        "forbidden artifact sections",
        REQUIRED_FORBIDDEN_ARTIFACT_SECTIONS - _as_strings(contract.get("forbidden_artifact_sections")),
    )
    _append_missing(
        errors,
        "artifact validation gates",
        REQUIRED_VALIDATION_GATES - _as_strings(contract.get("required_validation_gates")),
    )
    _append_missing(
        errors,
        "forbidden precomputed artifact actions",
        REQUIRED_FORBIDDEN_ACTIONS - _as_strings(contract.get("forbidden_actions")),
    )
    _append_missing(
        errors,
        "permitted precomputed artifact outputs",
        REQUIRED_PERMITTED_OUTPUTS - _as_strings(contract.get("permitted_outputs")),
    )
    _append_missing(
        errors,
        "no-authority assertions",
        REQUIRED_NO_AUTHORITY_ASSERTIONS - _as_strings(contract.get("no_authority_assertions")),
    )

    disabled_flags = contract.get("disabled_flags")
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
    else:
        missing_disabled_flags = REQUIRED_DISABLED_FLAGS_FALSE - set(disabled_flags)
        _append_missing(errors, "disabled precomputed artifact flags", missing_disabled_flags)
        enabled = sorted(flag for flag in REQUIRED_DISABLED_FLAGS_FALSE if disabled_flags.get(flag) is not False)
        if enabled:
            errors.append(f"precomputed artifact flags must be false: {', '.join(enabled)}")

    authority_fields = _find_forbidden_fields(contract, FORBIDDEN_AUTHORITY_FIELDS)
    raw_text_fields = _find_forbidden_fields(contract, FORBIDDEN_RAW_TEXT_FIELDS)
    vector_runtime_fields = _find_forbidden_fields(contract, FORBIDDEN_VECTOR_PROVIDER_RUNTIME_FIELDS)
    if authority_fields:
        errors.append(f"forbidden authority fields: {', '.join(sorted(authority_fields))}")
    if raw_text_fields:
        errors.append(f"forbidden raw/private text fields: {', '.join(sorted(raw_text_fields))}")
    if vector_runtime_fields:
        errors.append(f"forbidden vector/provider/runtime fields: {', '.join(sorted(vector_runtime_fields))}")

    return {
        "ok": not errors,
        "errors": errors,
        "artifact_generation_authorized": False,
        "embedding_generation_authorized": False,
        "vector_values_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "evaluation_execution_authorized": False,
        "threshold_tuning_authorized": False,
        "semantic_runtime_authorized": False,
        "prompt_router_mutation_authorized": False,
        "freeze_memory_write_authorized": False,
        "advisory_only": True,
        "review_evidence_only": True,
        "requires_future_governed_patch": True,
    }


def classify_precomputed_artifact_activation_request(request: str) -> dict[str, Any]:
    normalized = request.lower()
    matched = any(
        token in normalized
        for token in (
            "generate artifact",
            "write artifact",
            "precompute",
            "generate embeddings",
            "store vectors",
            "create vector index",
            "load provider",
            "run evaluation",
            "enable semantic runtime",
            "load artifact at startup",
        )
    )
    return {
        "request_recognized": matched,
        "allowed_now": False,
        "artifact_generation_authorized": False,
        "embedding_generation_authorized": False,
        "vector_values_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "evaluation_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "requires_future_governed_patch": True,
        "advisory_only": True,
        "reason": "precomputed semantic evidence artifacts remain design-only and require a separate governed generation patch",
    }
