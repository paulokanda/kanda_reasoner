"""Actual human decision record design for routing scorer v3.

This module is intentionally standard-library-only and decision-record-schema-only.
It records no real human decision, authorizes no generator candidate, generates no
artifact, writes no artifact, reads no artifact, scans no sources, materializes no
raw text, generates no embeddings, materializes no vectors, instantiates no
providers, runs no semantic scoring, modifies no router authority, loads no
prompts, writes no freeze memory, and changes no runtime behavior. It defines a
static schema for how a future actual human decision record could be represented
only after a separate governed process.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


ACTUAL_HUMAN_DECISION_RECORD_FEATURE_ID = (
    "routing_signal_scorer_v3_actual_human_decision_record_design_v1"
)
ACTUAL_HUMAN_DECISION_RECORD_SCHEMA_VERSION = (
    "3.17-actual-human-decision-record-design"
)
ACTUAL_HUMAN_DECISION_RECORD_STATUS = (
    "actual_decision_record_schema_only_no_decision_write_no_generator_authorization"
)

REQUIRED_RECORD_FIELDS = frozenset(
    {
        "record_id",
        "schema_version",
        "record_status",
        "declared_actual_human_decision_record_schema_only",
        "decision_record_scope",
        "decision_value",
        "decision_record_effect",
        "required_prior_milestones",
        "allowed_future_recorded_decision_values",
        "required_human_attestation_sections",
        "required_written_evidence_before_recording_real_decision",
        "required_written_evidence_before_any_future_candidate",
        "allowed_record_outputs",
        "prohibited_record_outputs",
        "disabled_flags",
        "no_authority_assertions",
        "record_effect_policy",
        "escalation_rules",
    }
)

REQUIRED_RECORD_SCOPE = "actual_human_decision_record_schema_only"

ALLOWED_RECORD_STATUSES = frozenset(
    {
        "schema_only",
        "awaiting_explicit_human_decision_recording_patch",
        "decision_recording_not_implemented",
        "deferred",
        "rejected",
    }
)

ALLOWED_FUTURE_RECORDED_DECISION_VALUES = frozenset(
    {
        "not_recorded",
        "defer_generator_candidate_proposal",
        "reject_generator_candidate_proposal",
        "permit_separate_generator_candidate_proposal_review_only",
    }
)

REQUIRED_PRIOR_MILESTONES = frozenset(
    {
        "v3_closure_shield_frozen",
        "disabled_generation_boundary_frozen",
        "dry_run_artifact_generation_plan_frozen",
        "local_generator_candidate_review_gate_frozen",
        "human_architectural_review_record_frozen",
        "human_decision_intake_frozen",
        "runtime_lite_advisory_only_regressions_passing",
        "freeze_hint_state_machine_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
    }
)

REQUIRED_HUMAN_ATTESTATION_SECTIONS = frozenset(
    {
        "human_actor_role_attestation_placeholder",
        "explicit_decision_phrase_placeholder",
        "review_record_reference",
        "decision_intake_reference",
        "scope_decision_attestation",
        "privacy_redaction_attestation",
        "dependency_budget_attestation",
        "resource_budget_attestation",
        "authority_boundary_attestation",
        "runtime_boundary_attestation",
        "artifact_lifecycle_attestation",
        "validation_matrix_attestation",
        "freeze_plan_attestation",
        "stop_conditions_attestation",
        "final_recorded_decision_placeholder",
    }
)

REQUIRED_WRITTEN_EVIDENCE_BEFORE_RECORDING_REAL_DECISION = frozenset(
    {
        "actual_human_decision_record_design_validation_ok",
        "human_decision_intake_validation_ok",
        "human_architectural_review_record_validation_ok",
        "local_generator_candidate_review_gate_validation_ok",
        "dry_run_artifact_generation_plan_validation_ok",
        "disabled_generation_boundary_validation_ok",
        "v3_closure_shield_validation_ok",
        "explicit_human_decision_recording_patch_requested",
        "human_decision_scope_review_written_evidence",
        "human_decision_privacy_review_written_evidence",
        "human_decision_dependency_review_written_evidence",
        "human_decision_resource_review_written_evidence",
        "human_decision_authority_review_written_evidence",
    }
)

REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE = frozenset(
    {
        "actual_human_decision_record_validation_ok",
        "real_human_decision_recorded_in_separate_frozen_patch",
        "recorded_decision_value_is_not_recorded_or_reject_or_defer_or_permit_review_only",
        "generator_candidate_still_requires_separate_governed_patch",
        "generator_candidate_review_gate_validation_ok",
        "dry_run_plan_validation_ok",
        "disabled_generation_boundary_validation_ok",
        "v3_closure_shield_validation_ok",
        "privacy_review_written_evidence",
        "dependency_review_written_evidence",
        "resource_budget_written_evidence",
        "redaction_review_written_evidence",
        "authority_leakage_review_written_evidence",
    }
)

REQUIRED_ALLOWED_RECORD_OUTPUTS = frozenset(
    {
        "actual_human_decision_record_schema",
        "human_attestation_questionnaire",
        "allowed_future_recorded_decision_values_list",
        "required_evidence_list",
        "record_effect_policy_summary",
        "stop_conditions_list",
        "review_evidence_only",
        "no_real_decision_recorded_by_this_schema",
        "no_generator_candidate_patch_authorized",
        "no_artifact_generated",
        "no_artifact_written",
        "no_artifact_read",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_PROHIBITED_RECORD_OUTPUTS = frozenset(
    {
        "real_human_decision_recorded",
        "generator_candidate_patch",
        "generator_candidate_authorization",
        "generated_artifact",
        "written_artifact",
        "loaded_artifact",
        "read_artifact",
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
        "missing_context_decision",
        "missing_behavior_decision",
        "may_proceed_now",
        "prompt_auto_load_list",
        "freeze_memory_write",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "real_human_decision_recorded",
        "decision_write_enabled",
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
        "record_design_records_no_real_human_decision",
        "record_design_must_not_authorize_generator_candidate_patch_by_itself",
        "record_design_must_not_generate_artifacts",
        "record_design_must_not_write_artifacts",
        "record_design_must_not_read_artifacts",
        "record_design_must_not_scan_sources",
        "record_design_must_not_materialize_raw_text",
        "record_design_must_not_generate_embeddings",
        "record_design_must_not_materialize_vectors",
        "record_design_must_not_choose_route",
        "record_design_must_not_choose_required_prompts",
        "record_design_must_not_decide_may_proceed",
        "record_design_must_not_load_prompts",
        "record_design_must_not_mutate_router",
        "record_design_must_not_write_freeze_memory",
        "canon_remains_final_authority",
        "future_real_decision_recording_requires_separate_governed_patch",
        "future_generator_candidate_requires_separate_governed_patch_after_recorded_decision",
    }
)

REQUIRED_RECORD_EFFECT_POLICY = frozenset(
    {
        "schema_only_record_has_no_decision_effect",
        "not_recorded_value_has_no_decision_effect",
        "future_defer_value_blocks_generator_candidate_until_new_decision",
        "future_reject_value_blocks_generator_candidate_until_new_decision",
        "future_permit_review_only_value_allows_only_separate_generator_candidate_proposal_review",
        "even_future_permit_review_only_value_does_not_authorize_generation",
        "any_request_to_use_record_as_runtime_authority_is_blocked",
        "any_request_to_use_record_as_router_authority_is_blocked",
        "any_request_to_use_record_as_artifact_authority_is_blocked",
    }
)

REQUIRED_ESCALATION_RULES = frozenset(
    {
        "if_human_says_go_next_without_explicit_decision_record_stop",
        "if_request_mentions_generate_or_embeddings_stop",
        "if_request_mentions_provider_or_model_loading_stop",
        "if_request_mentions_artifact_write_or_reader_stop",
        "if_request_mentions_runtime_enablement_stop",
        "if_request_mentions_router_authority_stop",
        "if_full_freeze_context_is_compact_request_specific_freeze_entries_first",
        "if_actual_decision_recording_is_needed_create_separate_governed_patch",
        "if_generator_candidate_is_needed_create_later_separate_governed_patch_after_recording",
    }
)

FORBIDDEN_RECORD_FIELDS = frozenset(
    {
        "actual_human_decision",
        "recorded_human_decision",
        "human_approval",
        "approved_by_human",
        "generator_candidate_patch_authorized",
        "generate_artifact_now",
        "artifact_payload",
        "artifact_path",
        "artifact_content",
        "source_text",
        "raw_prompt_text",
        "raw_user_query_text",
        "raw_freeze_entry_text",
        "embedding_values",
        "vector_values",
        "vector_index",
        "provider_config",
        "model_config",
        "runtime_semantic_score",
        "final_route",
        "may_proceed_now",
    }
)

TRIGGER_TERMS_REQUIRING_FUTURE_PATCH = frozenset(
    {
        "approve",
        "approved",
        "record decision",
        "actual decision",
        "permit",
        "authorize",
        "generator candidate",
        "generate",
        "generation",
        "artifact",
        "embedding",
        "vector",
        "provider",
        "runtime",
        "startup",
        "background",
        "router",
        "may proceed",
    }
)

SCHEMA_TALK_TERMS = frozenset(
    {
        "schema",
        "design",
        "record shape",
        "questionnaire",
        "decision values",
        "evidence list",
        "review only",
    }
)


def _sorted(values: Sequence[str] | set[str] | frozenset[str]) -> list[str]:
    return sorted(values)


def build_actual_human_decision_record_contract() -> dict[str, Any]:
    """Return an inert, schema-only actual human decision record contract."""

    return {
        "record_id": ACTUAL_HUMAN_DECISION_RECORD_FEATURE_ID,
        "schema_version": ACTUAL_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
        "record_status": "schema_only",
        "declared_actual_human_decision_record_schema_only": True,
        "decision_record_scope": REQUIRED_RECORD_SCOPE,
        "decision_value": "not_recorded",
        "decision_record_effect": "no_effect_schema_only_not_recorded",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "allowed_future_recorded_decision_values": _sorted(
            ALLOWED_FUTURE_RECORDED_DECISION_VALUES
        ),
        "required_human_attestation_sections": _sorted(
            REQUIRED_HUMAN_ATTESTATION_SECTIONS
        ),
        "required_written_evidence_before_recording_real_decision": _sorted(
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_RECORDING_REAL_DECISION
        ),
        "required_written_evidence_before_any_future_candidate": _sorted(
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE
        ),
        "allowed_record_outputs": _sorted(REQUIRED_ALLOWED_RECORD_OUTPUTS),
        "prohibited_record_outputs": _sorted(REQUIRED_PROHIBITED_RECORD_OUTPUTS),
        "disabled_flags": {flag: False for flag in _sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "record_effect_policy": _sorted(REQUIRED_RECORD_EFFECT_POLICY),
        "escalation_rules": _sorted(REQUIRED_ESCALATION_RULES),
    }


def validate_actual_human_decision_record_contract(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate the inert record schema and return denial-oriented facts."""

    errors: list[str] = []

    missing = REQUIRED_RECORD_FIELDS.difference(record)
    if missing:
        errors.append("missing required record fields: " + ", ".join(sorted(missing)))

    forbidden = FORBIDDEN_RECORD_FIELDS.intersection(record)
    if forbidden:
        errors.append("forbidden record fields present: " + ", ".join(sorted(forbidden)))

    if record.get("record_id") != ACTUAL_HUMAN_DECISION_RECORD_FEATURE_ID:
        errors.append("record_id mismatch")
    if record.get("schema_version") != ACTUAL_HUMAN_DECISION_RECORD_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if record.get("record_status") not in ALLOWED_RECORD_STATUSES:
        errors.append("record_status is not allowed")
    if record.get("record_status") != "schema_only":
        errors.append("record_status must remain schema_only")
    if record.get("declared_actual_human_decision_record_schema_only") is not True:
        errors.append("schema-only declaration must be true")
    if record.get("decision_record_scope") != REQUIRED_RECORD_SCOPE:
        errors.append("decision_record_scope mismatch")
    if record.get("decision_value") != "not_recorded":
        errors.append("decision_value must remain not_recorded")
    if record.get("decision_record_effect") != "no_effect_schema_only_not_recorded":
        errors.append("decision_record_effect must remain no_effect_schema_only_not_recorded")

    set_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("allowed_future_recorded_decision_values", ALLOWED_FUTURE_RECORDED_DECISION_VALUES),
        ("required_human_attestation_sections", REQUIRED_HUMAN_ATTESTATION_SECTIONS),
        (
            "required_written_evidence_before_recording_real_decision",
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_RECORDING_REAL_DECISION,
        ),
        (
            "required_written_evidence_before_any_future_candidate",
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE,
        ),
        ("allowed_record_outputs", REQUIRED_ALLOWED_RECORD_OUTPUTS),
        ("prohibited_record_outputs", REQUIRED_PROHIBITED_RECORD_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("record_effect_policy", REQUIRED_RECORD_EFFECT_POLICY),
        ("escalation_rules", REQUIRED_ESCALATION_RULES),
    ]
    for key, required in set_checks:
        values = record.get(key, [])
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            errors.append(f"{key} must be a sequence")
            continue
        if not required.issubset(set(values)):
            errors.append(f"{key} missing required values")

    flags = record.get("disabled_flags", {})
    if not isinstance(flags, Mapping):
        errors.append("disabled_flags must be a mapping")
    else:
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            if flag not in flags:
                errors.append(f"disabled flag missing: {flag}")
            elif flags[flag] is not False:
                errors.append(f"disabled flag must remain false: {flag}")

    ok = not errors
    flags_mapping = flags if isinstance(flags, Mapping) else {}
    return {
        "ok": ok,
        "errors": errors,
        "decision_value": record.get("decision_value"),
        "real_human_decision_recorded": flags_mapping.get(
            "real_human_decision_recorded", True
        ),
        "decision_write_authorized": flags_mapping.get("decision_write_enabled", True),
        "generator_candidate_patch_authorized": flags_mapping.get(
            "generator_candidate_patch_authorized", True
        ),
        "artifact_generation_authorized": flags_mapping.get(
            "artifact_generation_enabled", True
        ),
        "artifact_writing_authorized": flags_mapping.get("artifact_writing_enabled", True),
        "artifact_reading_authorized": flags_mapping.get("artifact_reader_enabled", True),
        "source_scanning_authorized": flags_mapping.get("source_scanning_enabled", True),
        "raw_text_materialization_authorized": flags_mapping.get(
            "raw_text_materialization_enabled", True
        ),
        "embedding_generation_authorized": flags_mapping.get(
            "embedding_generation_enabled", True
        ),
        "vector_index_generation_authorized": flags_mapping.get(
            "vector_index_generation_enabled", True
        ),
        "provider_execution_authorized": flags_mapping.get("provider_execution_enabled", True),
        "semantic_runtime_authorized": flags_mapping.get("semantic_runtime_enabled", True),
        "router_authority_authorized": flags_mapping.get(
            "prompt_router_mutation_enabled", True
        ),
        "requires_future_governed_patch": True,
    }


def classify_actual_human_decision_record_request(user_text: str) -> dict[str, Any]:
    """Classify a request against the schema-only decision-record boundary."""

    normalized = " ".join(str(user_text).lower().split())
    has_trigger = any(term in normalized for term in TRIGGER_TERMS_REQUIRING_FUTURE_PATCH)
    has_schema_talk = any(term in normalized for term in SCHEMA_TALK_TERMS)

    if has_trigger:
        return {
            "allowed_now": False,
            "permitted_output": "none",
            "decision_value": "not_recorded",
            "real_human_decision_recorded": False,
            "decision_write_authorized": False,
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
            "requires_future_governed_patch_for_decision_recording": True,
            "requires_future_governed_patch_for_generation": True,
            "reason": "request would record a decision, authorize generation, or enable runtime behavior",
        }

    return {
        "allowed_now": bool(has_schema_talk),
        "permitted_output": "actual_human_decision_record_schema" if has_schema_talk else "none",
        "decision_value": "not_recorded",
        "real_human_decision_recorded": False,
        "decision_write_authorized": False,
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
        "requires_future_governed_patch_for_decision_recording": True,
        "requires_future_governed_patch_for_generation": True,
        "reason": "schema-only discussion is allowed; decision recording and generation remain disabled",
    }
