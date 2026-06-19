"""Human decision intake design for routing scorer v3.

This module is intentionally standard-library-only and intake-schema-only. It
records no real human decision, authorizes no generator candidate, generates no
artifact, writes no artifact, reads no artifact, scans no sources, materializes
no raw text, generates no embeddings, materializes no vectors, instantiates no
providers, runs no semantic scoring, modifies no router authority, loads no
prompts, writes no freeze memory, and changes no runtime behavior. It defines a
static schema for how a future human decision could be represented only after a
separate governed process.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


HUMAN_DECISION_INTAKE_FEATURE_ID = (
    "routing_signal_scorer_v3_human_decision_intake_design_v1"
)
HUMAN_DECISION_INTAKE_SCHEMA_VERSION = "3.16-human-decision-intake-design"
HUMAN_DECISION_INTAKE_STATUS = (
    "decision_intake_schema_only_no_generator_authorization_no_runtime_behavior_change"
)

REQUIRED_INTAKE_FIELDS = frozenset(
    {
        "intake_id",
        "schema_version",
        "intake_status",
        "declared_human_decision_intake_only",
        "decision_scope",
        "decision_value",
        "required_prior_milestones",
        "allowed_future_decision_values",
        "required_decision_context_sections",
        "required_written_evidence_before_any_future_candidate",
        "allowed_intake_outputs",
        "prohibited_intake_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "decision_effect_policy",
        "escalation_rules",
    }
)

REQUIRED_DECISION_SCOPE = "human_decision_intake_schema_only"

ALLOWED_INTAKE_STATUSES = frozenset(
    {
        "schema_only",
        "awaiting_explicit_human_decision",
        "decision_recording_not_implemented",
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
        "human_architectural_review_record_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

ALLOWED_FUTURE_DECISION_VALUES = frozenset(
    {
        "not_recorded",
        "defer_generator_candidate_proposal",
        "reject_generator_candidate_proposal",
        "permit_separate_generator_candidate_proposal_review_only",
    }
)

REQUIRED_DECISION_CONTEXT_SECTIONS = frozenset(
    {
        "human_identity_or_role_confirmation_placeholder",
        "review_record_reference",
        "scope_decision_summary",
        "input_manifest_decision_summary",
        "privacy_and_redaction_decision_summary",
        "dependency_budget_decision_summary",
        "resource_budget_decision_summary",
        "authority_boundary_decision_summary",
        "runtime_boundary_decision_summary",
        "artifact_lifecycle_decision_summary",
        "validation_matrix_decision_summary",
        "freeze_plan_decision_summary",
        "stop_conditions_decision_summary",
        "final_decision_placeholder",
    }
)

REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE = frozenset(
    {
        "human_decision_intake_validation_ok",
        "human_architectural_review_record_validation_ok",
        "local_generator_candidate_review_gate_validation_ok",
        "dry_run_artifact_generation_plan_validation_ok",
        "disabled_generation_boundary_validation_ok",
        "v3_closure_shield_validation_ok",
        "explicit_human_decision_recorded_in_future_governed_patch",
        "human_decision_freeze_entry_written_before_candidate_patch",
        "privacy_review_written_evidence",
        "dependency_review_written_evidence",
        "resource_budget_written_evidence",
        "redaction_review_written_evidence",
        "authority_leakage_review_written_evidence",
    }
)

REQUIRED_ALLOWED_INTAKE_OUTPUTS = frozenset(
    {
        "human_decision_intake_schema",
        "human_decision_questionnaire",
        "allowed_future_decision_values_list",
        "required_evidence_list",
        "decision_effect_policy_summary",
        "stop_conditions_list",
        "review_evidence_only",
        "no_actual_decision_recorded",
        "no_generator_candidate_patch_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_INTAKE_OUTPUTS = frozenset(
    {
        "actual_human_decision",
        "generator_candidate_patch",
        "generator_candidate_authorization",
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

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "real_human_decision_recorded",
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
        "intake_is_schema_only",
        "intake_is_review_evidence_only",
        "intake_records_no_real_human_decision",
        "intake_must_not_authorize_generator_candidate_patch_by_itself",
        "intake_must_not_generate_artifacts",
        "intake_must_not_write_artifacts",
        "intake_must_not_read_artifacts",
        "intake_must_not_scan_sources",
        "intake_must_not_materialize_raw_text",
        "intake_must_not_generate_embeddings",
        "intake_must_not_materialize_vectors",
        "intake_must_not_choose_route",
        "intake_must_not_choose_required_prompts",
        "intake_must_not_decide_may_proceed",
        "intake_must_not_load_prompts",
        "intake_must_not_mutate_router",
        "intake_must_not_write_freeze_memory",
        "canon_remains_final_authority",
        "future_actual_decision_requires_separate_governed_patch",
        "future_generator_candidate_requires_separate_governed_patch_after_decision",
    }
)

REQUIRED_DECISION_EFFECT_POLICY = frozenset(
    {
        "default_decision_value_is_not_recorded",
        "schema_only_intake_has_no_decision_effect",
        "permit_separate_generator_candidate_proposal_review_only_is_not_generation_authorization",
        "permit_still_requires_separate_generator_candidate_patch",
        "reject_or_defer_blocks_generator_candidate_work",
        "any_generation_request_now_is_blocked",
        "any_request_to_use_intake_as_authority_is_blocked",
    }
)

REQUIRED_ESCALATION_RULES = frozenset(
    {
        "if_user_requests_generation_now_stop_at_decision_intake",
        "if_user_requests_embedding_now_stop_at_decision_intake",
        "if_user_requests_source_scan_now_stop_at_decision_intake",
        "if_user_requests_runtime_semantics_now_stop_at_decision_intake",
        "if_user_requests_router_authority_change_stop_at_decision_intake",
        "if_user_requests_auto_record_decision_stop_and_require_governed_patch",
        "if_review_entries_hidden_request_full_freeze_entries_before_touching_frozen_behavior",
        "if_any_raw_text_materialization_needed_stop_and_redesign",
        "if_any_dependency_beyond_stdlib_needed_stop_and_review",
    }
)

FORBIDDEN_INTAKE_FIELDS = frozenset(
    {
        "actual_human_decision",
        "approved_generator_candidate",
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
    if isinstance(value, str):
        return {value}
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return {str(item) for item in value}
    return set()


def _flag_is_false(flags: Mapping[str, Any], name: str) -> bool:
    return flags.get(name) is False


def build_human_decision_intake_contract() -> dict[str, Any]:
    """Return the static schema for human decision intake."""
    return {
        "intake_id": HUMAN_DECISION_INTAKE_FEATURE_ID,
        "schema_version": HUMAN_DECISION_INTAKE_SCHEMA_VERSION,
        "intake_status": "schema_only",
        "declared_human_decision_intake_only": True,
        "decision_scope": REQUIRED_DECISION_SCOPE,
        "decision_value": "not_recorded",
        "required_prior_milestones": sorted(REQUIRED_PRIOR_MILESTONES),
        "allowed_future_decision_values": sorted(ALLOWED_FUTURE_DECISION_VALUES),
        "required_decision_context_sections": sorted(REQUIRED_DECISION_CONTEXT_SECTIONS),
        "required_written_evidence_before_any_future_candidate": sorted(
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE
        ),
        "allowed_intake_outputs": sorted(REQUIRED_ALLOWED_INTAKE_OUTPUTS),
        "prohibited_intake_outputs": sorted(REQUIRED_PROHIBITED_INTAKE_OUTPUTS),
        "disabled_flags": {
            name: False for name in sorted(REQUIRED_DISABLED_FLAGS_FALSE)
        },
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "decision_effect_policy": sorted(REQUIRED_DECISION_EFFECT_POLICY),
        "escalation_rules": sorted(REQUIRED_ESCALATION_RULES),
    }


def validate_human_decision_intake_contract(
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate the decision-intake schema without recording a decision."""
    errors: list[str] = []

    if not isinstance(contract, Mapping):
        return {
            "ok": False,
            "errors": ["contract must be a mapping"],
            "real_human_decision_recorded": False,
            "generator_candidate_patch_authorized": False,
            "artifact_generation_authorized": False,
            "artifact_writing_authorized": False,
            "requires_future_governed_patch": True,
        }

    extra_forbidden = sorted(FORBIDDEN_INTAKE_FIELDS.intersection(contract.keys()))
    if extra_forbidden:
        errors.append("forbidden intake fields present: " + ", ".join(extra_forbidden))

    missing_fields = sorted(REQUIRED_INTAKE_FIELDS.difference(contract.keys()))
    if missing_fields:
        errors.append("missing required fields: " + ", ".join(missing_fields))

    if contract.get("intake_id") != HUMAN_DECISION_INTAKE_FEATURE_ID:
        errors.append("intake_id mismatch")
    if contract.get("schema_version") != HUMAN_DECISION_INTAKE_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if contract.get("intake_status") not in ALLOWED_INTAKE_STATUSES:
        errors.append("intake_status is not allowed")
    if contract.get("declared_human_decision_intake_only") is not True:
        errors.append("declared_human_decision_intake_only must be true")
    if contract.get("decision_scope") != REQUIRED_DECISION_SCOPE:
        errors.append("decision_scope mismatch")
    if contract.get("decision_value") != "not_recorded":
        errors.append("decision_value must remain not_recorded in this schema-only milestone")

    prior = _as_set(contract.get("required_prior_milestones"))
    if not REQUIRED_PRIOR_MILESTONES.issubset(prior):
        errors.append("required prior milestones incomplete")

    values = _as_set(contract.get("allowed_future_decision_values"))
    if not ALLOWED_FUTURE_DECISION_VALUES.issubset(values):
        errors.append("allowed future decision values incomplete")

    sections = _as_set(contract.get("required_decision_context_sections"))
    if not REQUIRED_DECISION_CONTEXT_SECTIONS.issubset(sections):
        errors.append("required decision context sections incomplete")

    evidence = _as_set(contract.get("required_written_evidence_before_any_future_candidate"))
    if not REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE.issubset(evidence):
        errors.append("required evidence before future candidate incomplete")

    allowed_outputs = _as_set(contract.get("allowed_intake_outputs"))
    if not REQUIRED_ALLOWED_INTAKE_OUTPUTS.issubset(allowed_outputs):
        errors.append("allowed intake outputs incomplete")

    prohibited_outputs = _as_set(contract.get("prohibited_intake_outputs"))
    if not REQUIRED_PROHIBITED_INTAKE_OUTPUTS.issubset(prohibited_outputs):
        errors.append("prohibited intake outputs incomplete")

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

    policy = _as_set(contract.get("decision_effect_policy"))
    if not REQUIRED_DECISION_EFFECT_POLICY.issubset(policy):
        errors.append("decision effect policy incomplete")

    escalation_rules = _as_set(contract.get("escalation_rules"))
    if not REQUIRED_ESCALATION_RULES.issubset(escalation_rules):
        errors.append("escalation rules incomplete")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "intake_id": contract.get("intake_id"),
        "schema_version": contract.get("schema_version"),
        "intake_status": contract.get("intake_status"),
        "decision_value": contract.get("decision_value"),
        "real_human_decision_recorded": False,
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


def classify_human_decision_intake_request(request_text: str) -> dict[str, Any]:
    """Classify decision-intake requests while denying activation/generation."""
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
        "record decision now",
        "approve now",
        "authorize generator",
    )
    intake_terms = (
        "human decision",
        "decision intake",
        "decision schema",
        "decision questionnaire",
        "decision placeholder",
        "defer",
        "reject",
        "permit proposal",
    )
    denied = any(term in normalized for term in activation_terms)
    intake_like = any(term in normalized for term in intake_terms)

    if intake_like and not denied:
        return {
            "allowed_now": True,
            "permitted_output": "human_decision_intake_schema",
            "decision_value": "not_recorded",
            "review_evidence_only": True,
            "real_human_decision_recorded": False,
            "generator_candidate_patch_authorized": False,
            "artifact_generation_authorized": False,
            "artifact_writing_authorized": False,
            "artifact_reading_authorized": False,
            "embedding_generation_authorized": False,
            "vector_index_authorized": False,
            "provider_execution_authorized": False,
            "semantic_runtime_authorized": False,
            "authority_granted": False,
            "requires_future_governed_patch_for_decision_recording": True,
            "requires_future_governed_patch_for_generation": True,
        }

    return {
        "allowed_now": False,
        "permitted_output": "blocked_or_requires_governed_human_decision_process",
        "decision_value": "not_recorded",
        "review_evidence_only": True,
        "real_human_decision_recorded": False,
        "generator_candidate_patch_authorized": False,
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reading_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "authority_granted": False,
        "requires_future_governed_patch_for_decision_recording": True,
        "requires_future_governed_patch_for_generation": True,
    }
