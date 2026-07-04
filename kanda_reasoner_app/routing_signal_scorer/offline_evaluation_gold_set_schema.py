# project-path: kanda_reasoner_app/routing_signal_scorer/offline_evaluation_gold_set_schema.py
"""Offline evaluation gold-set schema contract for future semantic evidence.

This module is intentionally standard-library-only. It does not run an evaluation,
generate embeddings, build vector indexes, read prompt-library files, read freeze entries,
persist user requests, tune thresholds, or mutate project state. It validates
the future frozen gold-set artifact shape that must exist before semantic/embedding evidence can be evaluated.
"""

from __future__ import annotations

__all__ = ['build_disabled_gold_set_schema_status', 'build_minimal_valid_gold_set_case', 'build_minimal_valid_gold_set_template', 'classify_gold_set_case_category', 'validate_gold_set_case', 'validate_offline_evaluation_gold_set']
from collections.abc import Mapping, Sequence
from typing import Any

OFFLINE_EVALUATION_GOLD_SET_FEATURE_ID = "routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1"
OFFLINE_EVALUATION_GOLD_SET_SCHEMA_VERSION = "3.5-offline-evaluation-gold-set"
OFFLINE_EVALUATION_GOLD_SET_STATUS = "schema_contract_only_no_evaluation_runner_no_ml_behavior_change"

REQUIRED_GOLD_SET_FIELDS = frozenset(
    {
        "gold_set_id",
        "schema_version",
        "status",
        "declared_before_run",
        "case_records",
        "case_categories",
        "metrics_contract",
        "acceptance_thresholds",
        "privacy_policy",
        "review_gates",
        "forbidden_actions",
    }
)

ALLOWED_GOLD_SET_STATUSES = frozenset(
    {
        "draft",
        "review_ready",
        "validated_schema_only",
        "frozen_gold_set",
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

REQUIRED_GOLD_SET_CASE_FIELDS = frozenset(
    {
        "case_id",
        "category",
        "case_is_synthetic",
        "synthetic_request_template",
        "expected_behavior",
        "expected_candidate_ids",
        "forbidden_candidate_ids",
        "expected_confidence_band",
        "must_mark_ambiguity",
        "must_fallback_to_lexical",
        "source_context_status",
        "no_authority_fields_expected",
        "contains_raw_user_text",
        "contains_private_project_text",
        "contains_prompt_body_text",
        "contains_freeze_entry_text",
    }
)

REQUIRED_METRICS_CONTRACT = frozenset(
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
        "superseded_candidate_suppression_rate",
        "ambiguity_detection_rate",
        "authority_leakage_rate",
        "privacy_leakage_rate",
        "p95_latency_overhead_ms",
    }
)

REQUIRED_ACCEPTANCE_THRESHOLDS = frozenset(
    {
        "authority_leakage_rate_must_equal_zero",
        "privacy_leakage_rate_must_equal_zero",
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

REQUIRED_PRIVACY_POLICY_VALUES = frozenset(
    {
        "synthetic_or_curated_cases_only",
        "no_raw_user_query_text",
        "no_private_chat_history",
        "no_private_project_text",
        "no_freeze_entry_text",
        "no_prompt_file_body_text",
        "no_external_api_submission",
        "no_training_persistence",
    }
)

REQUIRED_REVIEW_GATES = frozenset(
    {
        "human_review_required",
        "gold_set_freeze_required",
        "thresholds_declared_before_run",
        "case_category_coverage_review_required",
        "semantic_vs_lexical_disagreement_review_required",
        "false_positive_review_required",
        "stale_candidate_review_required",
        "authority_leakage_review_required",
        "privacy_leakage_review_required",
        "no_runtime_enablement_from_gold_set_alone",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "run_evaluation",
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
        "private_project_text",
        "freeze_entry_text",
        "prompt_file_text",
        "prompt_body_text",
        "terminal_log_text",
    }
)

ALLOWED_SOURCE_CONTEXT_STATUSES = frozenset(
    {
        "active",
        "deprecated",
        "superseded",
        "stale",
        "out_of_domain",
        "not_applicable",
    }
)

AMBIGUOUS_CATEGORIES = frozenset({"ambiguous_cases"})
STALE_SUPPRESSION_CATEGORIES = frozenset({"stale_context_cases"})

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

def _append_missing(errors: list[str], label: str, missing: set[str] | frozenset[str]) -> None:
    """Support append missing behavior.
    
    Parameters
    ----------
    errors : list[str]
        The error values.
    label : str
        The label value.
    missing : set[str] | frozenset[str]
        The missing value.
    """
    
    if missing:
        errors.append(f"{label} missing required values: {', '.join(sorted(missing))}")

def _contains_forbidden_key(mapping: Mapping[str, Any], forbidden_keys: set[str] | frozenset[str]) -> set[str]:
    """Support contains forbidden key behavior.
    
    Parameters
    ----------
    mapping : Mapping[str, Any]
        The mapping value.
    forbidden_keys : set[str] | frozenset[str]
        The forbidden keys value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {key for key in mapping.keys() if key in forbidden_keys}

def classify_gold_set_case_category(category: str) -> dict[str, Any]:
    """Classify whether a gold-set case category is known and advisory-only."""

    return {
        "category": category,
        "known_category": category in REQUIRED_CASE_CATEGORIES,
        "semantic_runtime_authorized": False,
        "evaluation_runner_authorized": False,
        "advisory_only": True,
    }

def validate_gold_set_case(case: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one future gold-set case without storing raw user text."""

    errors: list[str] = []
    if not isinstance(case, Mapping):
        return {
            "ok": False,
            "errors": ["gold-set case must be a mapping"],
            "semantic_runtime_authorized": False,
            "evaluation_runner_authorized": False,
            "advisory_only": True,
        }

    missing = REQUIRED_GOLD_SET_CASE_FIELDS - set(case.keys())
    _append_missing(errors, "gold-set case", missing)

    forbidden_authority = _contains_forbidden_key(case, FORBIDDEN_AUTHORITY_FIELDS)
    if forbidden_authority:
        errors.append("gold-set case contains forbidden authority fields: " + ", ".join(sorted(forbidden_authority)))

    forbidden_raw = _contains_forbidden_key(case, FORBIDDEN_RAW_TEXT_FIELDS)
    if forbidden_raw:
        errors.append("gold-set case contains forbidden raw/private text fields: " + ", ".join(sorted(forbidden_raw)))

    category = case.get("category")
    if category is not None and category not in REQUIRED_CASE_CATEGORIES:
        errors.append(f"unknown gold-set case category: {category}")

    if case.get("case_is_synthetic") is not True:
        errors.append("gold-set case must be synthetic or curated, with case_is_synthetic true for this schema phase")

    if not isinstance(case.get("synthetic_request_template"), str) or not case.get("synthetic_request_template"):
        errors.append("gold-set case must include a non-empty synthetic_request_template")

    if case.get("contains_raw_user_text") is not False:
        errors.append("gold-set case must not contain raw user text")

    if case.get("contains_private_project_text") is not False:
        errors.append("gold-set case must not contain private project text")

    if case.get("contains_prompt_body_text") is not False:
        errors.append("gold-set case must not contain prompt body text")

    if case.get("contains_freeze_entry_text") is not False:
        errors.append("gold-set case must not contain freeze entry text")

    if case.get("no_authority_fields_expected") is not True:
        errors.append("gold-set case must expect no authority fields")

    source_status = case.get("source_context_status")
    if source_status is not None and source_status not in ALLOWED_SOURCE_CONTEXT_STATUSES:
        errors.append(f"unknown source_context_status: {source_status}")

    if category in AMBIGUOUS_CATEGORIES and case.get("must_mark_ambiguity") is not True:
        errors.append("ambiguous gold-set cases must require ambiguity marking")

    if category in STALE_SUPPRESSION_CATEGORIES and source_status not in {"deprecated", "superseded", "stale"}:
        errors.append("stale_context_cases must use deprecated, superseded, or stale source_context_status")

    if source_status in {"deprecated", "superseded", "stale"}:
        forbidden_ids = case.get("forbidden_candidate_ids")
        if not _as_strings(forbidden_ids):
            errors.append("deprecated, superseded, or stale cases must declare forbidden_candidate_ids")

    return {
        "ok": not errors,
        "errors": errors,
        "semantic_runtime_authorized": False,
        "evaluation_runner_authorized": False,
        "threshold_changes_authorized": False,
        "advisory_only": True,
    }

def validate_offline_evaluation_gold_set(gold_set: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the future offline evaluation gold-set artifact shape."""

    errors: list[str] = []
    if not isinstance(gold_set, Mapping):
        return {
            "ok": False,
            "errors": ["gold set must be a mapping"],
            "semantic_runtime_authorized": False,
            "evaluation_runner_authorized": False,
            "advisory_only": True,
        }

    missing = REQUIRED_GOLD_SET_FIELDS - set(gold_set.keys())
    _append_missing(errors, "gold set", missing)

    forbidden_authority = _contains_forbidden_key(gold_set, FORBIDDEN_AUTHORITY_FIELDS)
    if forbidden_authority:
        errors.append("gold set contains forbidden authority fields: " + ", ".join(sorted(forbidden_authority)))

    forbidden_raw = _contains_forbidden_key(gold_set, FORBIDDEN_RAW_TEXT_FIELDS)
    if forbidden_raw:
        errors.append("gold set contains forbidden raw/private text fields: " + ", ".join(sorted(forbidden_raw)))

    if gold_set.get("schema_version") != OFFLINE_EVALUATION_GOLD_SET_SCHEMA_VERSION:
        errors.append("gold set schema_version mismatch")

    status = gold_set.get("status")
    if status is not None and status not in ALLOWED_GOLD_SET_STATUSES:
        errors.append(f"unknown gold set status: {status}")

    if gold_set.get("declared_before_run") is not True:
        errors.append("gold set must be declared before any evaluation run")

    categories = _as_strings(gold_set.get("case_categories"))
    _append_missing(errors, "case_categories", REQUIRED_CASE_CATEGORIES - categories)

    metrics = _as_strings(gold_set.get("metrics_contract"))
    _append_missing(errors, "metrics_contract", REQUIRED_METRICS_CONTRACT - metrics)

    thresholds = _as_strings(gold_set.get("acceptance_thresholds"))
    _append_missing(errors, "acceptance_thresholds", REQUIRED_ACCEPTANCE_THRESHOLDS - thresholds)

    privacy = _as_strings(gold_set.get("privacy_policy"))
    _append_missing(errors, "privacy_policy", REQUIRED_PRIVACY_POLICY_VALUES - privacy)

    gates = _as_strings(gold_set.get("review_gates"))
    _append_missing(errors, "review_gates", REQUIRED_REVIEW_GATES - gates)

    forbidden_actions = _as_strings(gold_set.get("forbidden_actions"))
    _append_missing(errors, "forbidden_actions", REQUIRED_FORBIDDEN_ACTIONS - forbidden_actions)

    records = gold_set.get("case_records")
    if not _is_sequence(records):
        errors.append("case_records must be a sequence")
        records = []

    record_categories: set[str] = set()
    for index, record in enumerate(records):
        result = validate_gold_set_case(record) if isinstance(record, Mapping) else {
            "ok": False,
            "errors": ["case record must be a mapping"],
        }
        if not result["ok"]:
            errors.append(f"case_records[{index}] invalid: " + "; ".join(result["errors"]))
        if isinstance(record, Mapping) and isinstance(record.get("category"), str):
            record_categories.add(record["category"])

    _append_missing(errors, "case_records category coverage", REQUIRED_CASE_CATEGORIES - record_categories)

    return {
        "ok": not errors,
        "errors": errors,
        "semantic_runtime_authorized": False,
        "evaluation_runner_authorized": False,
        "threshold_changes_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "advisory_only": True,
    }

def build_minimal_valid_gold_set_case(category: str = "positive_routing_cases") -> dict[str, Any]:
    """Build a synthetic, schema-valid case for tests and design examples only."""

    source_status = "active"
    forbidden_candidate_ids: list[str] = []
    if category == "stale_context_cases":
        source_status = "deprecated"
        forbidden_candidate_ids = ["deprecated_candidate_id"]
    elif category == "out_of_domain_cases":
        source_status = "out_of_domain"
    elif category == "ambiguous_cases":
        source_status = "active"

    return {
        "case_id": f"synthetic_{category}_001",
        "category": category,
        "case_is_synthetic": True,
        "synthetic_request_template": f"Synthetic request template for {category}.",
        "expected_behavior": "advisory_evidence_only_no_authority",
        "expected_candidate_ids": [] if category in {"out_of_domain_cases", "ambiguous_cases"} else ["active_candidate_id"],
        "forbidden_candidate_ids": forbidden_candidate_ids,
        "expected_confidence_band": "NO_MATCH" if category == "out_of_domain_cases" else "STRONG_ADVISORY",
        "must_mark_ambiguity": category == "ambiguous_cases",
        "must_fallback_to_lexical": category == "out_of_domain_cases",
        "source_context_status": source_status,
        "no_authority_fields_expected": True,
        "contains_raw_user_text": False,
        "contains_private_project_text": False,
        "contains_prompt_body_text": False,
        "contains_freeze_entry_text": False,
    }

def build_minimal_valid_gold_set_template() -> dict[str, Any]:
    """Build a minimal future gold-set artifact template without enabling evaluation."""

    return {
        "gold_set_id": "routing_signal_scorer_v3_synthetic_gold_set_template_v1",
        "schema_version": OFFLINE_EVALUATION_GOLD_SET_SCHEMA_VERSION,
        "status": "validated_schema_only",
        "declared_before_run": True,
        "case_categories": sorted(REQUIRED_CASE_CATEGORIES),
        "metrics_contract": sorted(REQUIRED_METRICS_CONTRACT),
        "acceptance_thresholds": sorted(REQUIRED_ACCEPTANCE_THRESHOLDS),
        "privacy_policy": sorted(REQUIRED_PRIVACY_POLICY_VALUES),
        "review_gates": sorted(REQUIRED_REVIEW_GATES),
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "case_records": [build_minimal_valid_gold_set_case(category) for category in sorted(REQUIRED_CASE_CATEGORIES)],
    }

def build_disabled_gold_set_schema_status() -> dict[str, Any]:
    """Return a status payload showing this feature does not execute evaluation."""

    return {
        "feature_id": OFFLINE_EVALUATION_GOLD_SET_FEATURE_ID,
        "schema_version": OFFLINE_EVALUATION_GOLD_SET_SCHEMA_VERSION,
        "status": OFFLINE_EVALUATION_GOLD_SET_STATUS,
        "evaluation_runner_enabled": False,
        "semantic_runtime_enabled": False,
        "threshold_auto_tuning_enabled": False,
        "embedding_generation_enabled": False,
        "vector_index_generation_enabled": False,
        "raw_user_query_storage_enabled": False,
        "external_api_enabled": False,
        "advisory_only": True,
    }
