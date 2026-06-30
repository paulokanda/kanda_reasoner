"""Provider boundary design contract for future semantic providers.

This module is intentionally standard-library-only and design-only. It does
not instantiate providers, load models, download models, generate embeddings,
build vector indexes, call external APIs, read prompt-library files, read
freeze entries, persist user requests, enable semantic runtime behavior, or
mutate project state. It validates the disabled provider-boundary contract
that any future provider adapter must satisfy before a separate governed
implementation can be considered.
"""

from __future__ import annotations


__all__ = [
    'build_minimal_valid_provider_boundary_contract',
    'build_provider_boundary_status',
    'classify_provider_activation_request',
    'validate_provider_boundary_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


PROVIDER_BOUNDARY_FEATURE_ID = "routing_signal_scorer_v3_provider_boundary_design_v1"
PROVIDER_BOUNDARY_SCHEMA_VERSION = "3.7-provider-boundary-design"
PROVIDER_BOUNDARY_STATUS = "design_contract_only_provider_disabled_no_model_no_embedding_no_ml_behavior_change"

REQUIRED_PROVIDER_BOUNDARY_FIELDS = frozenset(
    {
        "contract_id",
        "schema_version",
        "provider_boundary_status",
        "declared_design_only",
        "default_provider",
        "allowed_future_provider_classes",
        "forbidden_provider_classes_now",
        "required_future_adoption_gates",
        "disabled_flags",
        "forbidden_actions",
        "permitted_outputs",
        "no_authority_assertions",
    }
)

ALLOWED_BOUNDARY_STATUSES = frozenset(
    {
        "design_only",
        "disabled_boundary_ready",
        "disabled_boundary_frozen",
        "rejected",
    }
)

REQUIRED_DEFAULT_PROVIDER = "disabled_null_provider"

REQUIRED_ALLOWED_FUTURE_PROVIDER_CLASSES = frozenset(
    {
        "disabled_null_provider",
        "optional_local_embedding_provider_adapter",
        "optional_precomputed_embedding_artifact_reader",
        "optional_vector_index_adapter",
        "mock_semantic_evidence_adapter",
    }
)

REQUIRED_FORBIDDEN_PROVIDER_CLASSES_NOW = frozenset(
    {
        "external_api_provider",
        "network_provider",
        "credentialed_provider",
        "provider_auto_discovery",
        "runtime_provider_activation",
        "startup_provider_initialization",
        "background_provider_initialization",
        "self_learning_provider",
        "model_download_provider",
    }
)

REQUIRED_FUTURE_ADOPTION_GATES = frozenset(
    {
        "separate_governed_patch_required",
        "license_review_required",
        "dependency_review_required",
        "windows_pycharm_install_review_required",
        "local_first_review_required",
        "resource_budget_review_required",
        "privacy_review_required",
        "no_authority_regression_tests_required",
        "lexical_fallback_regression_tests_required",
        "disabled_by_default_configuration_required",
        "manual_activation_gate_required",
        "freeze_required_before_use",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "provider_execution_enabled",
        "local_embedding_provider_enabled",
        "external_api_provider_enabled",
        "network_access_enabled",
        "credential_loading_enabled",
        "model_download_enabled",
        "model_load_enabled",
        "embedding_generation_enabled",
        "vector_index_generation_enabled",
        "semantic_runtime_enabled",
        "automatic_provider_selection_enabled",
        "startup_provider_initialization_enabled",
        "runtime_provider_initialization_enabled",
        "background_provider_initialization_enabled",
        "file_watcher_provider_initialization_enabled",
        "prompt_router_mutation_enabled",
        "write_freeze_memory_enabled",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "instantiate_provider",
        "load_model",
        "download_model",
        "call_external_api",
        "load_credentials",
        "generate_embeddings",
        "read_raw_prompt_files",
        "read_freeze_entries",
        "persist_user_queries",
        "create_vector_index",
        "enable_semantic_runtime",
        "select_provider_automatically",
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
        "provider_boundary_status_report",
        "provider_denial_report",
        "dependency_review_checklist",
        "license_review_checklist",
        "resource_budget_checklist",
        "privacy_review_checklist",
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
        "provider_outputs_are_evidence_only",
        "provider_outputs_cannot_change_router_decision",
        "provider_outputs_cannot_change_required_prompts",
        "provider_outputs_cannot_change_may_proceed",
        "provider_outputs_cannot_enable_semantic_runtime",
        "provider_outputs_cannot_select_provider_automatically",
        "provider_outputs_cannot_write_freeze_memory",
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
        "select_provider",
        "provider_override",
        "self_update_provider",
    }
)

FORBIDDEN_RAW_TEXT_FIELDS = frozenset(
    {
        "request_text",
        "raw_user_query",
        "user_query_text",
        "chat_history",
        "private_project_text",
        "freeze_entry_text",
        "prompt_file_text",
        "prompt_body_text",
        "terminal_log_text",
    }
)

FORBIDDEN_VECTOR_OR_PROVIDER_RUNTIME_FIELDS = frozenset(
    {
        "embedding",
        "embeddings",
        "vector",
        "vectors",
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


def build_provider_boundary_status() -> dict[str, Any]:
    """Return the frozen disabled status for the provider boundary."""

    return {
        "feature_id": PROVIDER_BOUNDARY_FEATURE_ID,
        "schema_version": PROVIDER_BOUNDARY_SCHEMA_VERSION,
        "provider_boundary_status": PROVIDER_BOUNDARY_STATUS,
        "default_provider": REQUIRED_DEFAULT_PROVIDER,
        "provider_execution_enabled": False,
        "local_embedding_provider_enabled": False,
        "external_api_provider_enabled": False,
        "network_access_enabled": False,
        "credential_loading_enabled": False,
        "model_download_enabled": False,
        "model_load_enabled": False,
        "embedding_generation_enabled": False,
        "vector_index_generation_enabled": False,
        "semantic_runtime_enabled": False,
        "automatic_provider_selection_enabled": False,
        "startup_provider_initialization_enabled": False,
        "runtime_provider_initialization_enabled": False,
        "background_provider_initialization_enabled": False,
        "advisory_only": True,
        "lexical_fallback_primary": True,
        "requires_future_governed_patch": True,
    }


def build_minimal_valid_provider_boundary_contract() -> dict[str, Any]:
    """Return a minimal valid provider-boundary contract that authorizes nothing."""

    return {
        "contract_id": PROVIDER_BOUNDARY_FEATURE_ID,
        "schema_version": PROVIDER_BOUNDARY_SCHEMA_VERSION,
        "provider_boundary_status": "disabled_boundary_ready",
        "declared_design_only": True,
        "default_provider": REQUIRED_DEFAULT_PROVIDER,
        "allowed_future_provider_classes": sorted(REQUIRED_ALLOWED_FUTURE_PROVIDER_CLASSES),
        "forbidden_provider_classes_now": sorted(REQUIRED_FORBIDDEN_PROVIDER_CLASSES_NOW),
        "required_future_adoption_gates": sorted(REQUIRED_FUTURE_ADOPTION_GATES),
        "disabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "permitted_outputs": sorted(REQUIRED_PERMITTED_OUTPUTS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
    }


def validate_provider_boundary_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the disabled provider-boundary contract.

    A valid contract is review evidence only. It never authorizes provider
    execution, model loading, embedding generation, vector indexing, semantic
    runtime activation, prompt-router mutation, or freeze-memory writes.
    """

    errors: list[str] = []
    keys = set(contract)
    _append_missing(errors, "provider-boundary fields", REQUIRED_PROVIDER_BOUNDARY_FIELDS - keys)

    if contract.get("contract_id") != PROVIDER_BOUNDARY_FEATURE_ID:
        errors.append("contract_id must match provider boundary feature id")
    if contract.get("schema_version") != PROVIDER_BOUNDARY_SCHEMA_VERSION:
        errors.append("schema_version must match provider boundary schema version")
    if contract.get("provider_boundary_status") not in ALLOWED_BOUNDARY_STATUSES:
        errors.append("provider_boundary_status is not an allowed disabled design status")
    if contract.get("declared_design_only") is not True:
        errors.append("declared_design_only must be true")
    if contract.get("default_provider") != REQUIRED_DEFAULT_PROVIDER:
        errors.append("default_provider must remain disabled_null_provider")

    allowed = _as_strings(contract.get("allowed_future_provider_classes"))
    _append_missing(
        errors,
        "allowed future provider classes",
        REQUIRED_ALLOWED_FUTURE_PROVIDER_CLASSES - allowed,
    )
    forbidden_classes = _as_strings(contract.get("forbidden_provider_classes_now"))
    _append_missing(
        errors,
        "forbidden provider classes now",
        REQUIRED_FORBIDDEN_PROVIDER_CLASSES_NOW - forbidden_classes,
    )
    adoption_gates = _as_strings(contract.get("required_future_adoption_gates"))
    _append_missing(
        errors,
        "future provider adoption gates",
        REQUIRED_FUTURE_ADOPTION_GATES - adoption_gates,
    )

    flags = contract.get("disabled_flags")
    if not isinstance(flags, Mapping):
        errors.append("disabled_flags must be a mapping")
    else:
        missing_flags = REQUIRED_DISABLED_FLAGS_FALSE - set(flags)
        _append_missing(errors, "disabled provider flags", missing_flags)
        enabled = sorted(flag for flag in REQUIRED_DISABLED_FLAGS_FALSE if flags.get(flag) is not False)
        if enabled:
            errors.append(f"provider flags must be false: {', '.join(enabled)}")

    actions = _as_strings(contract.get("forbidden_actions"))
    _append_missing(errors, "forbidden provider actions", REQUIRED_FORBIDDEN_ACTIONS - actions)
    outputs = _as_strings(contract.get("permitted_outputs"))
    _append_missing(errors, "permitted provider-boundary outputs", REQUIRED_PERMITTED_OUTPUTS - outputs)
    no_authority = _as_strings(contract.get("no_authority_assertions"))
    _append_missing(errors, "no-authority assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS - no_authority)

    authority_fields = _find_forbidden_fields(contract, FORBIDDEN_AUTHORITY_FIELDS)
    if authority_fields:
        errors.append(f"forbidden authority fields: {', '.join(sorted(authority_fields))}")
    raw_text_fields = _find_forbidden_fields(contract, FORBIDDEN_RAW_TEXT_FIELDS)
    if raw_text_fields:
        errors.append(f"forbidden raw/private text fields: {', '.join(sorted(raw_text_fields))}")
    runtime_fields = _find_forbidden_fields(contract, FORBIDDEN_VECTOR_OR_PROVIDER_RUNTIME_FIELDS)
    if runtime_fields:
        errors.append(f"forbidden vector/provider runtime fields: {', '.join(sorted(runtime_fields))}")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "provider_execution_authorized": False,
        "local_embedding_provider_authorized": False,
        "external_api_provider_authorized": False,
        "network_access_authorized": False,
        "credential_loading_authorized": False,
        "model_download_authorized": False,
        "model_load_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "semantic_runtime_authorized": False,
        "prompt_router_mutation_authorized": False,
        "freeze_memory_write_authorized": False,
        "advisory_only": True,
        "lexical_fallback_primary": True,
        "requires_future_governed_patch": True,
    }


def classify_provider_activation_request(action: str) -> dict[str, Any]:
    """Classify a human or code request to activate a provider.

    This function is deliberately conservative: every activation-like request
    is denied now and routed to a future governed patch path.
    """

    normalized = " ".join(action.lower().replace("_", " ").split())
    activation_terms = {
        "enable",
        "activate",
        "run",
        "instantiate",
        "load",
        "download",
        "embed",
        "embedding",
        "vector",
        "provider",
        "api",
        "model",
        "semantic runtime",
    }
    requested_activation = any(term in normalized for term in activation_terms)
    return {
        "requested_activation": requested_activation,
        "allowed_now": False,
        "provider_execution_authorized": False,
        "model_load_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "semantic_runtime_authorized": False,
        "external_api_authorized": False,
        "requires_future_governed_patch": True,
        "advisory_only": True,
        "reason": "provider boundary is design-only and disabled by default",
    }
