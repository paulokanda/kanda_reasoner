# project-path: kanda_reasoner_app/routing_signal_scorer/advisory_precomputed_artifact_ui_preview_design.py
"""Advisory precomputed artifact UI preview design contract.

This module is intentionally standard-library-only and design-only. It does
not implement a UI widget, read artifacts, load artifacts at startup or
runtime, materialize raw text, materialize vector values, build vector
indexes, instantiate providers, run evaluation, tune thresholds, enable
semantic runtime behavior, modify the prompt router, or mutate project
state. It validates the advisory display boundary for a future precomputed
semantic evidence artifact preview.
"""

from __future__ import annotations


__all__ = [
    'build_advisory_artifact_ui_preview_contract',
    'classify_artifact_ui_preview_activation_request',
    'validate_advisory_artifact_ui_preview_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


ADVISORY_ARTIFACT_UI_PREVIEW_FEATURE_ID = "routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design_v1"
ADVISORY_ARTIFACT_UI_PREVIEW_SCHEMA_VERSION = "3.10-advisory-precomputed-artifact-ui-preview-design"
ADVISORY_ARTIFACT_UI_PREVIEW_STATUS = "design_contract_only_no_ui_no_artifact_loading_no_runtime_behavior_change"

REQUIRED_PREVIEW_CONTRACT_FIELDS = frozenset(
    {
        "contract_id",
        "schema_version",
        "preview_design_status",
        "declared_design_only",
        "source_requirements",
        "display_sections",
        "display_gates",
        "disabled_flags",
        "forbidden_actions",
        "permitted_outputs",
        "no_authority_assertions",
    }
)

ALLOWED_PREVIEW_STATUSES = frozenset(
    {
        "design_only",
        "preview_boundary_ready",
        "preview_boundary_frozen",
        "rejected",
    }
)

REQUIRED_SOURCE_REQUIREMENTS = frozenset(
    {
        "disabled_artifact_reader_boundary_must_be_frozen",
        "precomputed_artifact_design_must_be_frozen",
        "artifact_must_be_schema_validated_before_preview",
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

REQUIRED_DISPLAY_SECTIONS = frozenset(
    {
        "artifact_identity_summary",
        "source_manifest_reference_summary",
        "source_gold_set_reference_summary",
        "schema_validation_status_summary",
        "eligibility_counts_summary",
        "ambiguity_policy_summary",
        "stale_deprecated_suppression_summary",
        "no_authority_banner",
        "review_evidence_only_banner",
        "disabled_runtime_banner",
    }
)

REQUIRED_DISPLAY_GATES = frozenset(
    {
        "manual_preview_invocation_required",
        "separate_governed_ui_patch_required",
        "artifact_reader_boundary_frozen_required",
        "artifact_schema_validation_required",
        "no_raw_text_materialization_check_required",
        "no_vector_materialization_check_required",
        "no_authority_fields_check_required",
        "no_runtime_enablement_check_required",
        "review_evidence_only_check_required",
        "display_redaction_check_required",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "ui_preview_implemented",
        "ui_preview_enabled",
        "artifact_reader_enabled",
        "artifact_loading_enabled",
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
        "implement_ui_preview",
        "enable_ui_preview",
        "read_artifact_for_display",
        "load_artifact_at_startup",
        "load_artifact_at_runtime",
        "auto_discover_artifacts",
        "auto_refresh_artifacts",
        "watch_artifact_files",
        "display_raw_text",
        "display_user_query_text",
        "display_prompt_body_text",
        "display_freeze_entry_text",
        "display_embedding_values",
        "display_vector_values",
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
        "artifact_preview_boundary_status_report",
        "artifact_preview_preconditions_report",
        "artifact_preview_denial_report",
        "artifact_display_checklist",
        "redacted_metadata_summary_only",
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
        "preview_output_is_advisory_only",
        "preview_output_is_review_evidence_only",
        "preview_must_not_choose_route",
        "preview_must_not_choose_required_prompts",
        "preview_must_not_decide_may_proceed",
        "preview_must_not_load_prompts",
        "preview_must_not_mutate_router",
        "preview_must_not_write_freeze_memory",
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
        "display_text_payload",
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
        "artifact_reader",
    }
)


def _as_mapping(value: Any, name: str) -> Mapping[str, Any]:
    """Support as mapping behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    name : str
        The name value.
    
    Returns
    -------
    Mapping[str, Any]
        The mapped values.
    """
    
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return value


def _as_sequence(value: Any, name: str) -> Sequence[Any]:
    """Support as sequence behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    name : str
        The name value.
    
    Returns
    -------
    Sequence[Any]
        The sequence of values.
    """
    
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a sequence")
    return value


def _missing(required: frozenset[str], actual: Any) -> tuple[str, ...]:
    """Support missing behavior.
    
    Parameters
    ----------
    required : frozenset[str]
        The required value.
    actual : Any
        The actual value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return tuple(sorted(required.difference(set(_as_sequence(actual, "sequence")))))


def build_advisory_artifact_ui_preview_contract() -> dict[str, Any]:
    """Return the advisory artifact UI preview design contract."""

    return {
        "contract_id": ADVISORY_ARTIFACT_UI_PREVIEW_FEATURE_ID,
        "schema_version": ADVISORY_ARTIFACT_UI_PREVIEW_SCHEMA_VERSION,
        "preview_design_status": "design_only",
        "declared_design_only": True,
        "source_requirements": sorted(REQUIRED_SOURCE_REQUIREMENTS),
        "display_sections": sorted(REQUIRED_DISPLAY_SECTIONS),
        "display_gates": sorted(REQUIRED_DISPLAY_GATES),
        "disabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "permitted_outputs": sorted(REQUIRED_PERMITTED_OUTPUTS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
    }


def validate_advisory_artifact_ui_preview_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the advisory UI preview boundary without enabling display behavior."""

    candidate = _as_mapping(contract, "contract")
    missing_fields = sorted(REQUIRED_PREVIEW_CONTRACT_FIELDS.difference(candidate))
    errors: list[str] = []
    if missing_fields:
        errors.append("missing required fields: " + ", ".join(missing_fields))

    if candidate.get("contract_id") != ADVISORY_ARTIFACT_UI_PREVIEW_FEATURE_ID:
        errors.append("contract_id mismatch")
    if candidate.get("schema_version") != ADVISORY_ARTIFACT_UI_PREVIEW_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("preview_design_status") not in ALLOWED_PREVIEW_STATUSES:
        errors.append("unsupported preview design status")
    if candidate.get("declared_design_only") is not True:
        errors.append("declared_design_only must be true")

    for key, required, label in [
        ("source_requirements", REQUIRED_SOURCE_REQUIREMENTS, "source requirements"),
        ("display_sections", REQUIRED_DISPLAY_SECTIONS, "display sections"),
        ("display_gates", REQUIRED_DISPLAY_GATES, "display gates"),
        ("forbidden_actions", REQUIRED_FORBIDDEN_ACTIONS, "forbidden actions"),
        ("permitted_outputs", REQUIRED_PERMITTED_OUTPUTS, "permitted outputs"),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS, "no-authority assertions"),
    ]:
        if key in candidate:
            missing = _missing(required, candidate[key])
            if missing:
                errors.append(f"missing {label}: " + ", ".join(missing))

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
        "ui_preview_enabled": False,
        "artifact_reader_enabled": False,
        "artifact_loading_enabled": False,
        "raw_text_materialization_enabled": False,
        "vector_materialization_enabled": False,
        "semantic_runtime_enabled": False,
        "authority_granted": False,
        "requires_future_governed_patch": True,
    }


def classify_artifact_ui_preview_activation_request(action: str) -> dict[str, Any]:
    """Deny activation-like UI preview requests in this design-only phase."""

    normalized = action.lower().strip()
    activation_terms = (
        "enable",
        "display",
        "ui",
        "preview",
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
        "ui_preview_authorized": False,
        "artifact_reader_authorized": False,
        "artifact_loading_authorized": False,
        "raw_text_materialization_authorized": False,
        "vector_materialization_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "authority_granted": False,
        "requires_future_governed_patch": True,
        "advisory_only": True,
        "reason": "artifact UI preview is an advisory design boundary only",
    }
