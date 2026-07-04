# project-path: kanda_reasoner_app/routing_signal_scorer/human_architectural_review_record_design.py
"""Human architectural review record design for routing scorer v3.

This module is intentionally standard-library-only and review-record-only. It
creates no generator candidate, generates no artifact, writes no artifact, reads
no artifact, scans no sources, materializes no raw text, generates no embeddings,
materializes no vectors, instantiates no providers, runs no semantic scoring,
modifies no router authority, loads no prompts, writes no freeze memory, and
changes no runtime behavior. It defines a static schema for the human review
record that must exist before any future separately governed generator-candidate
proposal can even be discussed.
"""

from __future__ import annotations

__all__ = ['build_human_architectural_review_record_contract', 'classify_human_architectural_review_request', 'validate_human_architectural_review_record_contract']
from collections.abc import Mapping, Sequence
from typing import Any

HUMAN_ARCHITECTURAL_REVIEW_RECORD_FEATURE_ID = (
    "routing_signal_scorer_v3_human_architectural_review_record_design_v1"
)
HUMAN_ARCHITECTURAL_REVIEW_RECORD_SCHEMA_VERSION = (
    "3.15-human-architectural-review-record-design"
)
HUMAN_ARCHITECTURAL_REVIEW_RECORD_STATUS = (
    "review_record_schema_only_no_generator_no_artifact_write_no_runtime_behavior_change"
)

REQUIRED_REVIEW_RECORD_FIELDS = frozenset(
    {
        "record_id",
        "schema_version",
        "record_status",
        "declared_human_review_only",
        "review_scope",
        "required_prior_milestones",
        "required_review_questions",
        "allowed_record_outputs",
        "prohibited_record_outputs",
        "required_human_review_sections",
        "disabled_flags",
        "no_authority_assertions",
        "decision_policy",
        "escalation_rules",
    }
)

REQUIRED_REVIEW_SCOPE = "human_architectural_review_record_only"

ALLOWED_RECORD_STATUSES = frozenset(
    {
        "schema_only",
        "awaiting_human_review",
        "human_review_recorded",
        "deferred",
        "rejected",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "v3_closure_shield_frozen",
        "disabled_generation_boundary_frozen",
        "dry_run_artifact_generation_plan_frozen",
        "local_generator_candidate_review_gate_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_REVIEW_QUESTIONS = frozenset(
    {
        "what_exact_future_generator_candidate_would_be_reviewed",
        "what_inputs_would_be_allowed_if_a_candidate_is_ever_proposed",
        "what_inputs_must_remain_forbidden",
        "what_raw_text_must_never_be_materialized",
        "what_artifact_outputs_would_remain_schema_only_or_review_only",
        "what_dependency_ceiling_would_apply",
        "what_resource_budget_would_apply",
        "what_privacy_redaction_policy_would_apply",
        "what_authority_leakage_tests_would_be_required",
        "what_freeze_and_validation_evidence_would_be_required",
        "what_human_stop_conditions_would_block_candidate_proposal",
    }
)

REQUIRED_ALLOWED_RECORD_OUTPUTS = frozenset(
    {
        "human_review_record_schema",
        "human_review_questionnaire",
        "human_review_decision_placeholder",
        "risk_register_template",
        "candidate_scope_placeholder",
        "dependency_budget_placeholder",
        "privacy_redaction_placeholder",
        "authority_leakage_review_placeholder",
        "future_patch_readiness_placeholder",
        "review_evidence_only",
        "no_artifact_generated",
        "no_artifact_written",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_RECORD_OUTPUTS = frozenset(
    {
        "generator_candidate_patch",
        "generated_artifact",
        "written_artifact",
        "loaded_artifact",
        "raw_prompt_text",
        "raw_user_query_text",
        "raw_freeze_entry_text",
        "raw_source_text",
        "embedding_values",
        "vector_values",
        "vector_index",
        "provider_config",
        "model_config",
        "runtime_semantic_score",
        "final_route",
        "required_prompts",
        "may_proceed_now",
        "prompt_auto_load_list",
        "freeze_memory_write",
    }
)

REQUIRED_HUMAN_REVIEW_SECTIONS = frozenset(
    {
        "scope_review",
        "input_manifest_review",
        "privacy_and_redaction_review",
        "dependency_review",
        "resource_budget_review",
        "authority_boundary_review",
        "runtime_boundary_review",
        "artifact_lifecycle_review",
        "validation_matrix_review",
        "freeze_plan_review",
        "stop_conditions_review",
        "final_human_decision_placeholder",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "generator_candidate_patch_authorized",
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_overwrite_enabled",
        "artifact_reader_enabled",
        "artifact_loading_enabled",
        "source_scanning_enabled",
        "prompt_library_scan_enabled",
        "freeze_entry_scan_enabled",
        "project_source_scan_enabled",
        "runtime_user_query_capture_enabled",
        "raw_text_materialization_enabled",
        "embedding_generation_enabled",
        "embedding_value_materialization_enabled",
        "vector_value_materialization_enabled",
        "vector_index_generation_enabled",
        "provider_execution_enabled",
        "network_access_enabled",
        "credential_loading_enabled",
        "startup_generation_enabled",
        "runtime_generation_enabled",
        "background_generation_enabled",
        "file_watcher_generation_enabled",
        "semantic_runtime_enabled",
        "prompt_router_mutation_enabled",
        "prompt_auto_loading_enabled",
        "may_proceed_generation_enabled",
        "write_freeze_memory_enabled",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "record_is_schema_only",
        "record_is_review_evidence_only",
        "record_must_not_authorize_generator_candidate_patch_by_itself",
        "record_must_not_generate_artifacts",
        "record_must_not_write_artifacts",
        "record_must_not_read_artifacts",
        "record_must_not_scan_sources",
        "record_must_not_materialize_raw_text",
        "record_must_not_generate_embeddings",
        "record_must_not_materialize_vectors",
        "record_must_not_choose_route",
        "record_must_not_choose_required_prompts",
        "record_must_not_decide_may_proceed",
        "record_must_not_load_prompts",
        "record_must_not_mutate_router",
        "record_must_not_write_freeze_memory",
        "canon_remains_final_authority",
        "future_generator_candidate_requires_separate_governed_patch",
    }
)

REQUIRED_DECISION_POLICY = frozenset(
    {
        "default_decision_is_not_recorded",
        "only_human_can_record_decision",
        "permit_proposal_is_not_generation_authorization",
        "permit_proposal_still_requires_separate_governed_patch",
        "reject_or_defer_blocks_generator_candidate_work",
        "any_generation_request_now_is_blocked",
    }
)

REQUIRED_ESCALATION_RULES = frozenset(
    {
        "if_user_requests_generation_now_stop_at_review_record",
        "if_user_requests_embedding_now_stop_at_review_record",
        "if_user_requests_source_scan_now_stop_at_review_record",
        "if_user_requests_runtime_semantics_now_stop_at_review_record",
        "if_user_requests_router_authority_change_stop_at_review_record",
        "if_review_entries_hidden_request_full_freeze_entries_before_touching_frozen_behavior",
        "if_any_raw_text_materialization_needed_stop_and_redesign",
        "if_any_dependency_beyond_stdlib_needed_stop_and_review",
    }
)

FORBIDDEN_REVIEW_RECORD_FIELDS = frozenset(
    {
        "artifact_path",
        "artifact_payload",
        "generated_artifact",
        "raw_user_query",
        "raw_user_queries",
        "prompt_body_text",
        "prompt_text",
        "freeze_entry_text",
        "source_document_text",
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
        "network_endpoint",
        "credential_path",
        "final_route",
        "required_prompts",
        "missing_context",
        "missing_behavior",
        "may_proceed_now",
        "route_override",
        "prompt_override",
        "authority_granted",
        "write_freeze_memory",
        "generator_candidate_patch",
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
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return {str(item) for item in value}
    return set()

def _flag_is_false(flags: Mapping[str, Any], name: str) -> bool:
    """Support flag is false behavior.
    
    Parameters
    ----------
    flags : Mapping[str, Any]
        The flags value.
    name : str
        The name value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return flags.get(name) is False

def build_human_architectural_review_record_contract() -> dict[str, Any]:
    """Return the static schema for a human architectural review record."""
    return {
        "record_id": HUMAN_ARCHITECTURAL_REVIEW_RECORD_FEATURE_ID,
        "schema_version": HUMAN_ARCHITECTURAL_REVIEW_RECORD_SCHEMA_VERSION,
        "record_status": "schema_only",
        "declared_human_review_only": True,
        "review_scope": REQUIRED_REVIEW_SCOPE,
        "required_prior_milestones": sorted(REQUIRED_PRIOR_MILESTONES),
        "required_review_questions": sorted(REQUIRED_REVIEW_QUESTIONS),
        "allowed_record_outputs": sorted(REQUIRED_ALLOWED_RECORD_OUTPUTS),
        "prohibited_record_outputs": sorted(REQUIRED_PROHIBITED_RECORD_OUTPUTS),
        "required_human_review_sections": sorted(REQUIRED_HUMAN_REVIEW_SECTIONS),
        "disabled_flags": {
            name: False for name in sorted(REQUIRED_DISABLED_FLAGS_FALSE)
        },
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "decision_policy": sorted(REQUIRED_DECISION_POLICY),
        "escalation_rules": sorted(REQUIRED_ESCALATION_RULES),
    }

def validate_human_architectural_review_record_contract(
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate the review-record schema without authorizing generation."""
    errors: list[str] = []

    if not isinstance(contract, Mapping):
        return {
            "ok": False,
            "errors": ["contract must be a mapping"],
            "generator_candidate_patch_authorized": False,
            "artifact_generation_authorized": False,
            "artifact_writing_authorized": False,
            "requires_future_governed_patch": True,
        }

    extra_forbidden = sorted(FORBIDDEN_REVIEW_RECORD_FIELDS.intersection(contract.keys()))
    if extra_forbidden:
        errors.append("forbidden review record fields present: " + ", ".join(extra_forbidden))

    missing_fields = sorted(REQUIRED_REVIEW_RECORD_FIELDS.difference(contract.keys()))
    if missing_fields:
        errors.append("missing required fields: " + ", ".join(missing_fields))

    if contract.get("record_id") != HUMAN_ARCHITECTURAL_REVIEW_RECORD_FEATURE_ID:
        errors.append("record_id mismatch")
    if contract.get("schema_version") != HUMAN_ARCHITECTURAL_REVIEW_RECORD_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if contract.get("record_status") not in ALLOWED_RECORD_STATUSES:
        errors.append("record_status is not allowed")
    if contract.get("declared_human_review_only") is not True:
        errors.append("declared_human_review_only must be true")
    if contract.get("review_scope") != REQUIRED_REVIEW_SCOPE:
        errors.append("review_scope mismatch")

    prior = _as_set(contract.get("required_prior_milestones"))
    if not REQUIRED_PRIOR_MILESTONES.issubset(prior):
        errors.append("required prior milestones incomplete")

    questions = _as_set(contract.get("required_review_questions"))
    if not REQUIRED_REVIEW_QUESTIONS.issubset(questions):
        errors.append("required review questions incomplete")

    allowed_outputs = _as_set(contract.get("allowed_record_outputs"))
    if not REQUIRED_ALLOWED_RECORD_OUTPUTS.issubset(allowed_outputs):
        errors.append("allowed record outputs incomplete")

    prohibited_outputs = _as_set(contract.get("prohibited_record_outputs"))
    if not REQUIRED_PROHIBITED_RECORD_OUTPUTS.issubset(prohibited_outputs):
        errors.append("prohibited record outputs incomplete")

    sections = _as_set(contract.get("required_human_review_sections"))
    if not REQUIRED_HUMAN_REVIEW_SECTIONS.issubset(sections):
        errors.append("required human review sections incomplete")

    flags = contract.get("disabled_flags")
    if not isinstance(flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        flags = {}

    false_missing = sorted(
        name for name in REQUIRED_DISABLED_FLAGS_FALSE if not _flag_is_false(flags, name)
    )
    if false_missing:
        errors.append("required disabled flags must be false: " + ", ".join(false_missing))

    no_authority = _as_set(contract.get("no_authority_assertions"))
    if not REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(no_authority):
        errors.append("no-authority assertions incomplete")

    decision_policy = _as_set(contract.get("decision_policy"))
    if not REQUIRED_DECISION_POLICY.issubset(decision_policy):
        errors.append("decision policy incomplete")

    escalation_rules = _as_set(contract.get("escalation_rules"))
    if not REQUIRED_ESCALATION_RULES.issubset(escalation_rules):
        errors.append("escalation rules incomplete")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "record_id": contract.get("record_id"),
        "schema_version": contract.get("schema_version"),
        "record_status": contract.get("record_status"),
        "generator_candidate_patch_authorized": False,
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
        "requires_future_governed_patch": True,
        "review_evidence_only": True,
    }

def classify_human_architectural_review_request(request_text: str) -> dict[str, Any]:
    """Classify human-review requests while denying activation/generation."""
    normalized = str(request_text or "").strip().lower()
    activation_terms = (
        "generate",
        "write artifact",
        "create artifact",
        "read artifact",
        "load artifact",
        "scan source",
        "scan prompt",
        "scan freeze",
        "raw text",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "startup",
        "background",
        "file watcher",
        "router authority",
        "may proceed",
        "auto-load",
        "bypass",
    )
    review_terms = (
        "human review",
        "architectural review",
        "record",
        "questionnaire",
        "risk register",
        "readiness",
        "review template",
    )
    denied = any(term in normalized for term in activation_terms)
    review_like = any(term in normalized for term in review_terms)

    if review_like and not denied:
        return {
            "allowed_now": True,
            "permitted_output": "human_review_record_schema",
            "review_evidence_only": True,
            "generator_candidate_patch_authorized": False,
            "artifact_generation_authorized": False,
            "artifact_writing_authorized": False,
            "artifact_reading_authorized": False,
            "embedding_generation_authorized": False,
            "vector_index_authorized": False,
            "provider_execution_authorized": False,
            "semantic_runtime_authorized": False,
            "authority_granted": False,
            "requires_future_governed_patch_for_generation": True,
        }

    return {
        "allowed_now": False,
        "permitted_output": "blocked_or_requires_human_review",
        "review_evidence_only": True,
        "generator_candidate_patch_authorized": False,
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reading_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "authority_granted": False,
        "requires_future_governed_patch_for_generation": True,
    }
