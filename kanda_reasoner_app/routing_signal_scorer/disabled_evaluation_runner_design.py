# project-path: kanda_reasoner_app/routing_signal_scorer/disabled_evaluation_runner_design.py
"""Disabled evaluation runner design contract for future semantic evaluation.

This module is intentionally standard-library-only and design-only. It does not
run evaluation, invoke providers, generate embeddings, build vector indexes,
read prompt-library files, read freeze entries, persist user requests, tune
thresholds, enable semantic runtime behavior, or mutate project state. It
validates the disabled-by-default contract that a future evaluation runner must
satisfy before any separate governed implementation can be considered.
"""

from __future__ import annotations


__all__ = [
    'build_disabled_evaluation_runner_status',
    'build_minimal_valid_disabled_runner_contract',
    'classify_runner_activation_request',
    'validate_disabled_evaluation_runner_contract',
]
from collections.abc import Mapping, Sequence
from typing import Any


DISABLED_EVALUATION_RUNNER_FEATURE_ID = "routing_signal_scorer_v3_disabled_evaluation_runner_design_v1"
DISABLED_EVALUATION_RUNNER_SCHEMA_VERSION = "3.6-disabled-evaluation-runner-design"
DISABLED_EVALUATION_RUNNER_STATUS = "design_contract_only_runner_disabled_no_execution_no_ml_behavior_change"

REQUIRED_DISABLED_RUNNER_FIELDS = frozenset(
    {
        "contract_id",
        "schema_version",
        "runner_status",
        "declared_design_only",
        "enabled_flags",
        "preconditions_before_any_future_runner",
        "required_inputs_for_future_manual_runner",
        "forbidden_actions",
        "permitted_outputs",
        "review_gates",
        "no_authority_assertions",
    }
)

ALLOWED_RUNNER_STATUSES = frozenset(
    {
        "design_only",
        "disabled_contract_ready",
        "disabled_contract_frozen",
        "rejected",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "evaluation_execution_enabled",
        "semantic_runtime_enabled",
        "threshold_auto_tuning_enabled",
        "embedding_generation_enabled",
        "vector_index_generation_enabled",
        "corpus_generation_enabled",
        "external_api_enabled",
        "background_job_enabled",
        "startup_run_enabled",
        "runtime_run_enabled",
        "file_watcher_enabled",
        "write_freeze_memory_enabled",
        "prompt_router_mutation_enabled",
        "prompt_auto_loading_enabled",
        "may_proceed_generation_enabled",
    }
)

REQUIRED_FUTURE_PRECONDITIONS = frozenset(
    {
        "frozen_gold_set_required",
        "frozen_metadata_vector_manifest_required",
        "frozen_offline_corpus_governance_required",
        "human_review_required",
        "explicit_manual_invocation_required",
        "thresholds_declared_before_run",
        "metrics_declared_before_run",
        "lexical_fallback_primary",
        "semantic_evidence_advisory_only",
        "no_runtime_enablement_from_runner_results",
    }
)

REQUIRED_FUTURE_INPUTS = frozenset(
    {
        "frozen_gold_set_schema_validated_artifact",
        "frozen_metadata_vector_manifest_schema_validated_artifact",
        "predeclared_metric_threshold_contract",
        "human_approved_evaluation_plan",
        "dependency_review_if_any_future_optional_provider_exists",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "run_evaluation_now",
        "run_at_startup",
        "run_at_runtime",
        "run_in_background",
        "run_from_file_watcher",
        "rebuild_corpus",
        "generate_embeddings",
        "create_vector_index",
        "call_external_embedding_api",
        "persist_user_queries",
        "auto_adjust_thresholds_after_results",
        "enable_semantic_runtime",
        "promote_semantic_candidate",
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
        "review_evidence_only",
        "metrics_report_draft_only",
        "candidate_failure_report_only",
        "disagreement_report_only",
        "human_review_queue_only",
        "no_runtime_enablement",
        "no_threshold_changes",
        "no_prompt_loading",
        "no_may_proceed_signal",
        "no_final_route_signal",
    }
)

REQUIRED_REVIEW_GATES = frozenset(
    {
        "manual_invocation_gate",
        "gold_set_freeze_gate",
        "manifest_freeze_gate",
        "privacy_gate",
        "authority_leakage_gate",
        "stale_candidate_gate",
        "threshold_change_separate_patch_gate",
        "runtime_enablement_separate_patch_gate",
        "dependency_adoption_separate_patch_gate",
        "freeze_required_before_any_runner_implementation",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "runner_results_are_evidence_only",
        "runner_results_cannot_change_router_decision",
        "runner_results_cannot_change_required_prompts",
        "runner_results_cannot_change_may_proceed",
        "runner_results_cannot_enable_semantic_runtime",
        "runner_results_cannot_adjust_thresholds",
        "runner_results_cannot_write_freeze_memory",
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
        "adjust_thresholds",
        "self_update_corpus",
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

FORBIDDEN_VECTOR_OR_PROVIDER_FIELDS = frozenset(
    {
        "embedding",
        "embeddings",
        "vector",
        "vectors",
        "vector_index",
        "index_path",
        "provider",
        "provider_name",
        "external_api_key",
        "model_name",
        "model_path",
    }
)


def _is_sequence(value: Any) -> bool:
    """Support is sequence behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _as_strings(value: Any) -> set[str]:
    """Support as strings behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    if not _is_sequence(value):
        return set()
    return {item for item in value if isinstance(item, str)}


def _append_missing(errors: list[str], label: str, missing: set[str]) -> None:
    """Support append missing behavior.
    
    Parameters
    ----------
    errors : list[str]
        The error values.
    label : str
        The label value.
    missing : set[str]
        The missing value.
    """
    
    if missing:
        errors.append(f"missing {label}: {', '.join(sorted(missing))}")


def _find_forbidden_fields(mapping: Mapping[str, Any], forbidden: set[str] | frozenset[str]) -> set[str]:
    """Support find forbidden fields behavior.
    
    Parameters
    ----------
    mapping : Mapping[str, Any]
        The mapping value.
    forbidden : set[str] | frozenset[str]
        The forbidden value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {key for key in mapping if key in forbidden}


def build_disabled_evaluation_runner_status() -> dict[str, Any]:
    """Return the disabled-by-default runner status for UI or tests."""

    return {
        "feature_id": DISABLED_EVALUATION_RUNNER_FEATURE_ID,
        "schema_version": DISABLED_EVALUATION_RUNNER_SCHEMA_VERSION,
        "runner_status": DISABLED_EVALUATION_RUNNER_STATUS,
        "evaluation_runner_enabled": False,
        "semantic_runtime_enabled": False,
        "threshold_auto_tuning_enabled": False,
        "embedding_generation_enabled": False,
        "vector_index_generation_enabled": False,
        "corpus_generation_enabled": False,
        "external_api_enabled": False,
        "startup_run_enabled": False,
        "runtime_run_enabled": False,
        "background_job_enabled": False,
        "file_watcher_enabled": False,
        "advisory_only": True,
        "lexical_fallback_primary": True,
    }


def build_minimal_valid_disabled_runner_contract() -> dict[str, Any]:
    """Build a schema-valid disabled runner contract without enabling execution."""

    return {
        "contract_id": DISABLED_EVALUATION_RUNNER_FEATURE_ID,
        "schema_version": DISABLED_EVALUATION_RUNNER_SCHEMA_VERSION,
        "runner_status": "disabled_contract_ready",
        "declared_design_only": True,
        "enabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "preconditions_before_any_future_runner": sorted(REQUIRED_FUTURE_PRECONDITIONS),
        "required_inputs_for_future_manual_runner": sorted(REQUIRED_FUTURE_INPUTS),
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "permitted_outputs": sorted(REQUIRED_PERMITTED_OUTPUTS),
        "review_gates": sorted(REQUIRED_REVIEW_GATES),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
    }


def classify_runner_activation_request(action: str) -> dict[str, Any]:
    """Classify a requested runner action without authorizing it."""

    normalized = (action or "").strip().lower().replace(" ", "_").replace("-", "_")
    forbidden = normalized in REQUIRED_FORBIDDEN_ACTIONS or any(
        token in normalized
        for token in (
            "run",
            "startup",
            "runtime",
            "background",
            "embedding",
            "vector",
            "provider",
            "threshold",
            "enable_semantic",
            "router",
            "freeze_memory",
            "may_proceed",
            "final_route",
        )
    )
    return {
        "action": action,
        "allowed_now": False,
        "known_forbidden_action": forbidden,
        "requires_future_governed_patch": True,
        "semantic_runtime_authorized": False,
        "evaluation_runner_authorized": False,
        "threshold_changes_authorized": False,
        "advisory_only": True,
    }


def validate_disabled_evaluation_runner_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the disabled evaluation runner contract shape.

    Validation output is evidence only. It never authorizes evaluation execution,
    semantic runtime, threshold changes, embeddings, vector indexes, provider
    calls, prompt-router changes, or freeze writes.
    """

    errors: list[str] = []

    if not isinstance(contract, Mapping):
        return {
            "ok": False,
            "errors": ["contract must be a mapping"],
            "evaluation_runner_authorized": False,
            "semantic_runtime_authorized": False,
            "threshold_changes_authorized": False,
            "advisory_only": True,
        }

    _append_missing(errors, "disabled runner fields", REQUIRED_DISABLED_RUNNER_FIELDS - set(contract))

    if contract.get("contract_id") != DISABLED_EVALUATION_RUNNER_FEATURE_ID:
        errors.append("contract_id must match disabled evaluation runner feature id")
    if contract.get("schema_version") != DISABLED_EVALUATION_RUNNER_SCHEMA_VERSION:
        errors.append("schema_version must match disabled evaluation runner schema version")
    if contract.get("runner_status") not in ALLOWED_RUNNER_STATUSES:
        errors.append("runner_status is not an allowed disabled runner status")
    if contract.get("declared_design_only") is not True:
        errors.append("declared_design_only must be true")

    authority_fields = _find_forbidden_fields(contract, FORBIDDEN_AUTHORITY_FIELDS)
    raw_text_fields = _find_forbidden_fields(contract, FORBIDDEN_RAW_TEXT_FIELDS)
    vector_provider_fields = _find_forbidden_fields(contract, FORBIDDEN_VECTOR_OR_PROVIDER_FIELDS)
    if authority_fields:
        errors.append(f"forbidden authority fields present: {', '.join(sorted(authority_fields))}")
    if raw_text_fields:
        errors.append(f"forbidden raw/private text fields present: {', '.join(sorted(raw_text_fields))}")
    if vector_provider_fields:
        errors.append(f"forbidden vector/provider fields present: {', '.join(sorted(vector_provider_fields))}")

    flags = contract.get("enabled_flags")
    if not isinstance(flags, Mapping):
        errors.append("enabled_flags must be a mapping")
    else:
        _append_missing(errors, "disabled flags", REQUIRED_DISABLED_FLAGS_FALSE - set(flags))
        enabled = sorted(flag for flag in REQUIRED_DISABLED_FLAGS_FALSE if flags.get(flag) is not False)
        if enabled:
            errors.append(f"all runner execution/runtime/provider flags must be false: {', '.join(enabled)}")
        nested_forbidden = set(flags) & (FORBIDDEN_AUTHORITY_FIELDS | FORBIDDEN_RAW_TEXT_FIELDS | FORBIDDEN_VECTOR_OR_PROVIDER_FIELDS)
        if nested_forbidden:
            errors.append(f"enabled_flags contains forbidden fields: {', '.join(sorted(nested_forbidden))}")

    preconditions = _as_strings(contract.get("preconditions_before_any_future_runner"))
    required_inputs = _as_strings(contract.get("required_inputs_for_future_manual_runner"))
    forbidden_actions = _as_strings(contract.get("forbidden_actions"))
    permitted_outputs = _as_strings(contract.get("permitted_outputs"))
    review_gates = _as_strings(contract.get("review_gates"))
    assertions = _as_strings(contract.get("no_authority_assertions"))

    _append_missing(errors, "future preconditions", REQUIRED_FUTURE_PRECONDITIONS - preconditions)
    _append_missing(errors, "future manual-runner inputs", REQUIRED_FUTURE_INPUTS - required_inputs)
    _append_missing(errors, "forbidden actions", REQUIRED_FORBIDDEN_ACTIONS - forbidden_actions)
    _append_missing(errors, "permitted outputs", REQUIRED_PERMITTED_OUTPUTS - permitted_outputs)
    _append_missing(errors, "review gates", REQUIRED_REVIEW_GATES - review_gates)
    _append_missing(errors, "no-authority assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS - assertions)

    return {
        "ok": not errors,
        "errors": errors,
        "evaluation_runner_authorized": False,
        "semantic_runtime_authorized": False,
        "threshold_changes_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "external_api_authorized": False,
        "freeze_memory_write_authorized": False,
        "prompt_router_mutation_authorized": False,
        "advisory_only": True,
    }
