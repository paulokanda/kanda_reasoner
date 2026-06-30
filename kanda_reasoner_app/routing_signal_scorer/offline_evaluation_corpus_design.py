"""Offline evaluation corpus design contract for future semantic evidence.

This module is intentionally standard-library-only. It does not evaluate a
real model, generate embeddings, build vector indexes, read prompt-library
files, read freeze entries, persist user requests, or mutate project state.
It provides deterministic validation helpers for a future frozen evaluation
corpus that must exist before any real semantic/embedding provider is used.
"""

from __future__ import annotations


__all__ = [
    'build_disabled_offline_evaluation_corpus_status',
    'build_minimal_valid_evaluation_case',
    'build_minimal_valid_evaluation_corpus_template',
    'classify_evaluation_case_category',
    'validate_evaluation_case',
    'validate_offline_evaluation_corpus_plan',
]
from collections.abc import Mapping, Sequence
from typing import Any


OFFLINE_EVALUATION_CORPUS_FEATURE_ID = "routing_signal_scorer_v3_offline_evaluation_corpus_design_v1"
OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION = "3.4-offline-evaluation-corpus"
OFFLINE_EVALUATION_CORPUS_STATUS = "design_contract_only_no_runtime_evaluation_no_ml_behavior_change"

REQUIRED_EVALUATION_PLAN_FIELDS = frozenset(
    {
        "evaluation_id",
        "schema_version",
        "status",
        "declared_before_run",
        "case_categories",
        "metrics",
        "acceptance_thresholds",
        "evaluation_cases",
        "review_gates",
        "forbidden_actions",
        "privacy_policy",
    }
)

ALLOWED_STATUSES = frozenset(
    {
        "draft",
        "review_ready",
        "validated_design_only",
        "frozen_design",
        "rejected",
    }
)

REQUIRED_CASE_CATEGORIES = frozenset(
    {
        "positive_routing_cases",
        "near_miss_cases",
        "ambiguous_cases",
        "adversarial_instruction_cases",
        "stale_context_cases",
        "out_of_domain_cases",
        "freeze_shield_boundary_cases",
        "fast_path_false_positive_cases",
    }
)

REQUIRED_METRICS = frozenset(
    {
        "precision_at_1",
        "precision_at_3",
        "recall_at_1",
        "recall_at_3",
        "mrr",
        "ndcg_at_10",
        "false_positive_rate",
        "stale_candidate_suppression_rate",
        "deprecated_candidate_suppression_rate",
        "ambiguity_detection_rate",
        "authority_leakage_rate",
        "p95_latency_overhead_ms",
    }
)

REQUIRED_ACCEPTANCE_THRESHOLDS = frozenset(
    {
        "authority_leakage_rate_must_equal_zero",
        "deprecated_candidate_surface_count_must_equal_zero",
        "superseded_candidate_surface_count_must_equal_zero",
        "stale_candidate_surface_count_must_equal_zero",
        "external_api_call_count_must_equal_zero",
        "user_query_persistence_count_must_equal_zero",
        "fast_path_false_positive_rate_maximum",
        "ambiguity_detection_rate_minimum",
        "p95_latency_overhead_ms_maximum",
    }
)

REQUIRED_EVALUATION_CASE_FIELDS = frozenset(
    {
        "case_id",
        "category",
        "synthetic_request_summary",
        "expected_behavior",
        "expected_confidence_band",
        "forbidden_candidate_ids",
        "must_mark_ambiguity",
        "must_fallback_to_lexical",
        "no_authority_fields_expected",
        "contains_raw_user_text",
        "contains_private_project_text",
    }
)

REQUIRED_REVIEW_GATES = frozenset(
    {
        "human_review_required",
        "gold_set_freeze_required",
        "thresholds_declared_before_run",
        "semantic_vs_lexical_disagreement_review_required",
        "false_positive_review_required",
        "stale_candidate_review_required",
        "authority_leakage_review_required",
        "no_runtime_enablement_from_evaluation_alone",
    }
)

REQUIRED_PRIVACY_POLICY_VALUES = frozenset(
    {
        "synthetic_or_curated_cases_only",
        "no_raw_user_query_text",
        "no_private_chat_history",
        "no_freeze_entry_text",
        "no_prompt_file_body_text",
        "no_external_api_submission",
        "no_training_persistence",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "enable_semantic_runtime",
        "install_ml_dependency",
        "generate_embeddings",
        "create_vector_index",
        "call_external_embedding_api",
        "persist_user_queries",
        "auto_adjust_thresholds_after_results",
        "auto_promote_semantic_candidate",
        "produce_final_route",
        "produce_required_prompts",
        "produce_may_proceed_now",
        "modify_prompt_library",
        "write_freeze_memory",
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
        "self_update_corpus",
    }
)

FORBIDDEN_RAW_TEXT_FIELDS = frozenset(
    {
        "request_text",
        "raw_user_query",
        "user_query_text",
        "chat_history",
        "freeze_entry_text",
        "prompt_file_text",
        "terminal_log_text",
    }
)


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _as_strings(value: Any) -> set[str]:
    if not _is_sequence(value):
        return set()
    return {item for item in value if isinstance(item, str)}


def _append_missing(errors: list[str], label: str, missing: set[str] | frozenset[str]) -> None:
    if missing:
        errors.append(f"{label} missing required values: {', '.join(sorted(missing))}")


def _contains_forbidden_key(mapping: Mapping[str, Any], forbidden_keys: set[str] | frozenset[str]) -> set[str]:
    return {key for key in mapping.keys() if key in forbidden_keys}


def classify_evaluation_case_category(category: str) -> dict[str, Any]:
    """Classify whether a category is part of the frozen evaluation design."""

    return {
        "category": category,
        "known_category": category in REQUIRED_CASE_CATEGORIES,
        "semantic_runtime_authorized": False,
        "advisory_only": True,
    }


def validate_evaluation_case(case: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one future evaluation case without storing raw user text."""

    errors: list[str] = []
    if not isinstance(case, Mapping):
        return {
            "ok": False,
            "errors": ["evaluation case must be a mapping"],
            "semantic_runtime_authorized": False,
            "advisory_only": True,
        }

    missing = REQUIRED_EVALUATION_CASE_FIELDS - set(case.keys())
    _append_missing(errors, "evaluation case", missing)

    forbidden_authority = _contains_forbidden_key(case, FORBIDDEN_AUTHORITY_FIELDS)
    if forbidden_authority:
        errors.append("evaluation case contains forbidden authority fields: " + ", ".join(sorted(forbidden_authority)))

    forbidden_raw = _contains_forbidden_key(case, FORBIDDEN_RAW_TEXT_FIELDS)
    if forbidden_raw:
        errors.append("evaluation case contains forbidden raw text fields: " + ", ".join(sorted(forbidden_raw)))

    category = case.get("category")
    if category is not None and category not in REQUIRED_CASE_CATEGORIES:
        errors.append(f"unknown evaluation case category: {category}")

    if case.get("contains_raw_user_text") is not False:
        errors.append("evaluation case must not contain raw user text")

    if case.get("contains_private_project_text") is not False:
        errors.append("evaluation case must not contain private project text")

    if case.get("no_authority_fields_expected") is not True:
        errors.append("evaluation case must expect no authority fields")

    if not isinstance(case.get("synthetic_request_summary"), str) or not case.get("synthetic_request_summary"):
        errors.append("synthetic_request_summary must be a non-empty string")

    return {
        "ok": not errors,
        "feature_id": OFFLINE_EVALUATION_CORPUS_FEATURE_ID,
        "schema_version": OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION,
        "errors": errors,
        "semantic_runtime_authorized": False,
        "advisory_only": True,
    }


def validate_offline_evaluation_corpus_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a future offline evaluation corpus plan.

    A valid plan is still only design evidence. It never authorizes semantic
    runtime enablement, embedding generation, threshold auto-tuning, or vector
    index generation.
    """

    errors: list[str] = []

    if not isinstance(plan, Mapping):
        return {
            "ok": False,
            "feature_id": OFFLINE_EVALUATION_CORPUS_FEATURE_ID,
            "schema_version": OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION,
            "status": "invalid",
            "errors": ["plan must be a mapping"],
            "semantic_runtime_authorized": False,
            "threshold_changes_authorized": False,
            "advisory_only": True,
        }

    forbidden_top = _contains_forbidden_key(plan, FORBIDDEN_AUTHORITY_FIELDS | FORBIDDEN_RAW_TEXT_FIELDS)
    if forbidden_top:
        errors.append("plan contains forbidden fields: " + ", ".join(sorted(forbidden_top)))

    missing_fields = REQUIRED_EVALUATION_PLAN_FIELDS - set(plan.keys())
    _append_missing(errors, "evaluation plan", missing_fields)

    if plan.get("schema_version") != OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION:
        errors.append(f"schema_version must be {OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION}")

    if plan.get("status") not in ALLOWED_STATUSES:
        errors.append("status must be one of: " + ", ".join(sorted(ALLOWED_STATUSES)))

    if plan.get("declared_before_run") is not True:
        errors.append("thresholds and metrics must be declared before any evaluation run")

    categories = _as_strings(plan.get("case_categories"))
    _append_missing(errors, "case_categories", REQUIRED_CASE_CATEGORIES - categories)

    metrics = _as_strings(plan.get("metrics"))
    _append_missing(errors, "metrics", REQUIRED_METRICS - metrics)

    thresholds = plan.get("acceptance_thresholds")
    if not isinstance(thresholds, Mapping):
        errors.append("acceptance_thresholds must be a mapping")
    else:
        missing_thresholds = REQUIRED_ACCEPTANCE_THRESHOLDS - set(thresholds.keys())
        _append_missing(errors, "acceptance_thresholds", missing_thresholds)
        if thresholds.get("authority_leakage_rate_must_equal_zero") is not True:
            errors.append("authority leakage threshold must require zero leakage")
        if thresholds.get("external_api_call_count_must_equal_zero") is not True:
            errors.append("external API call threshold must require zero calls")
        if thresholds.get("user_query_persistence_count_must_equal_zero") is not True:
            errors.append("user query persistence threshold must require zero persistence")

    cases = plan.get("evaluation_cases")
    if not _is_sequence(cases) or not cases:
        errors.append("evaluation_cases must be a non-empty sequence")
    else:
        seen_categories: set[str] = set()
        for index, case in enumerate(cases):
            case_result = validate_evaluation_case(case)
            if not case_result["ok"]:
                errors.append(f"evaluation_cases[{index}] invalid: " + "; ".join(case_result["errors"]))
            elif isinstance(case, Mapping):
                seen_categories.add(str(case.get("category")))
        missing_case_categories = REQUIRED_CASE_CATEGORIES - seen_categories
        _append_missing(errors, "evaluation_cases categories", missing_case_categories)

    review_gates = _as_strings(plan.get("review_gates"))
    _append_missing(errors, "review_gates", REQUIRED_REVIEW_GATES - review_gates)

    forbidden_actions = _as_strings(plan.get("forbidden_actions"))
    _append_missing(errors, "forbidden_actions", REQUIRED_FORBIDDEN_ACTIONS - forbidden_actions)

    privacy_policy = _as_strings(plan.get("privacy_policy"))
    _append_missing(errors, "privacy_policy", REQUIRED_PRIVACY_POLICY_VALUES - privacy_policy)

    return {
        "ok": not errors,
        "feature_id": OFFLINE_EVALUATION_CORPUS_FEATURE_ID,
        "schema_version": OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION,
        "status": "valid_design_only" if not errors else "invalid",
        "errors": errors,
        "semantic_runtime_authorized": False,
        "threshold_changes_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "advisory_only": True,
        "reason": "offline evaluation corpus design is evidence for future governed review only",
    }


def build_minimal_valid_evaluation_case(category: str) -> dict[str, Any]:
    return {
        "case_id": f"eval-{category}",
        "category": category,
        "synthetic_request_summary": f"Synthetic curated request summary for {category}.",
        "expected_behavior": "produce advisory evidence only and preserve canon authority",
        "expected_confidence_band": "DESIGN_ONLY_EXPECTATION",
        "forbidden_candidate_ids": [],
        "must_mark_ambiguity": category == "ambiguous_cases",
        "must_fallback_to_lexical": category in {"out_of_domain_cases", "stale_context_cases"},
        "no_authority_fields_expected": True,
        "contains_raw_user_text": False,
        "contains_private_project_text": False,
    }


def build_minimal_valid_evaluation_corpus_template() -> dict[str, Any]:
    return {
        "evaluation_id": "routing-signal-scorer-v3-offline-evaluation-corpus-template",
        "schema_version": OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION,
        "status": "review_ready",
        "declared_before_run": True,
        "case_categories": sorted(REQUIRED_CASE_CATEGORIES),
        "metrics": sorted(REQUIRED_METRICS),
        "acceptance_thresholds": {
            "authority_leakage_rate_must_equal_zero": True,
            "deprecated_candidate_surface_count_must_equal_zero": True,
            "superseded_candidate_surface_count_must_equal_zero": True,
            "stale_candidate_surface_count_must_equal_zero": True,
            "external_api_call_count_must_equal_zero": True,
            "user_query_persistence_count_must_equal_zero": True,
            "fast_path_false_positive_rate_maximum": 0.0,
            "ambiguity_detection_rate_minimum": 1.0,
            "p95_latency_overhead_ms_maximum": 100,
        },
        "evaluation_cases": [
            build_minimal_valid_evaluation_case(category)
            for category in sorted(REQUIRED_CASE_CATEGORIES)
        ],
        "review_gates": sorted(REQUIRED_REVIEW_GATES),
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "privacy_policy": sorted(REQUIRED_PRIVACY_POLICY_VALUES),
    }


def build_disabled_offline_evaluation_corpus_status() -> dict[str, Any]:
    return {
        "feature_id": OFFLINE_EVALUATION_CORPUS_FEATURE_ID,
        "schema_version": OFFLINE_EVALUATION_CORPUS_SCHEMA_VERSION,
        "status": OFFLINE_EVALUATION_CORPUS_STATUS,
        "evaluation_runtime_enabled": False,
        "semantic_runtime_enabled": False,
        "threshold_auto_tuning_enabled": False,
        "embedding_generation_enabled": False,
        "vector_index_generation_enabled": False,
        "external_api_enabled": False,
        "raw_user_query_storage_enabled": False,
        "advisory_only": True,
    }
