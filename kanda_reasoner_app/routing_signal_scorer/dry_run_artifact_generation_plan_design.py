"""Dry-run artifact generation plan design for routing scorer v3.

This module is intentionally standard-library-only and design-only. It does not
implement artifact generation, write artifacts, read artifacts, scan source
material, generate embeddings, materialize vectors, instantiate providers, run
semantic scoring, modify router authority, load prompts, write freeze memory, or
change runtime behavior. It only defines a static plan contract that can be used
as review evidence before any future separately governed generator candidate is
considered.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


DRY_RUN_ARTIFACT_GENERATION_PLAN_FEATURE_ID = (
    "routing_signal_scorer_v3_dry_run_artifact_generation_plan_design_v1"
)
DRY_RUN_ARTIFACT_GENERATION_PLAN_SCHEMA_VERSION = (
    "3.13-dry-run-artifact-generation-plan-design"
)
DRY_RUN_ARTIFACT_GENERATION_PLAN_STATUS = (
    "design_contract_only_dry_run_plan_no_generation_no_artifact_write"
)

REQUIRED_DRY_RUN_PLAN_FIELDS = frozenset(
    {
        "plan_id",
        "schema_version",
        "plan_status",
        "declared_design_only",
        "dry_run_mode",
        "source_material_policy",
        "permitted_plan_outputs",
        "required_review_gates_before_future_generation",
        "disabled_flags",
        "forbidden_actions",
        "no_authority_assertions",
        "planned_human_review_questions",
    }
)

REQUIRED_DRY_RUN_MODE = "static_plan_only_no_generation"

ALLOWED_PLAN_STATUSES = frozenset(
    {
        "design_only",
        "static_plan_ready",
        "review_evidence_only",
        "rejected",
    }
)

REQUIRED_SOURCE_MATERIAL_POLICY = frozenset(
    {
        "no_prompt_library_scan",
        "no_freeze_entry_scan",
        "no_project_source_scan",
        "no_runtime_user_query_capture",
        "no_raw_text_materialization",
        "redacted_metadata_only_if_future_patch_allows_input_listing",
        "human_approved_input_manifest_required_before_future_generation",
    }
)

REQUIRED_PERMITTED_PLAN_OUTPUTS = frozenset(
    {
        "dry_run_plan_summary",
        "future_generator_risk_register",
        "future_generator_input_manifest_template",
        "future_validation_matrix_draft",
        "future_privacy_review_checklist",
        "future_dependency_review_checklist",
        "future_resource_budget_checklist",
        "future_no_authority_checklist",
        "human_review_queue_only",
        "review_evidence_only",
        "no_artifact_written",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_REVIEW_GATES = frozenset(
    {
        "separate_governed_patch_required",
        "tests_first_required",
        "human_confirmation_required",
        "local_first_required",
        "privacy_review_required",
        "dependency_review_required",
        "resource_budget_review_required",
        "redaction_review_required",
        "no_raw_text_materialization_gate_required",
        "no_vector_value_materialization_gate_required",
        "authority_leakage_gate_required",
        "freeze_required_before_any_use",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
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

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "generate_artifact_from_plan",
        "write_artifact_from_plan",
        "overwrite_artifact_from_plan",
        "read_artifact_from_plan",
        "load_artifact_from_plan",
        "scan_prompt_library_for_plan",
        "scan_freeze_entries_for_plan",
        "scan_project_source_for_plan",
        "capture_runtime_user_query_for_plan",
        "materialize_raw_prompt_text",
        "materialize_raw_user_query_text",
        "materialize_freeze_entry_text",
        "generate_embeddings",
        "materialize_embedding_values",
        "materialize_vector_values",
        "create_vector_index",
        "instantiate_provider",
        "call_external_api",
        "load_credentials",
        "run_generation_at_startup",
        "run_generation_at_runtime",
        "run_generation_in_background",
        "run_generation_from_file_watcher",
        "enable_semantic_runtime",
        "modify_prompt_router",
        "auto_load_prompts",
        "write_freeze_memory",
        "produce_final_route",
        "produce_required_prompts",
        "produce_may_proceed_now",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "dry_run_plan_is_design_only",
        "dry_run_plan_is_review_evidence_only",
        "dry_run_plan_must_not_generate_artifacts",
        "dry_run_plan_must_not_choose_route",
        "dry_run_plan_must_not_choose_required_prompts",
        "dry_run_plan_must_not_decide_may_proceed",
        "dry_run_plan_must_not_load_prompts",
        "dry_run_plan_must_not_mutate_router",
        "dry_run_plan_must_not_enable_semantic_runtime",
        "dry_run_plan_must_not_write_freeze_memory",
        "canon_remains_final_authority",
    }
)

REQUIRED_REVIEW_QUESTIONS = frozenset(
    {
        "which_sources_would_future_generation_use",
        "how_will_raw_text_be_excluded_or_redacted",
        "how_will_embedding_and_vector_values_remain_absent_until_authorized",
        "how_will_artifact_writes_be_blocked_until_authorized",
        "how_will_provider_execution_remain_disabled",
        "how_will_artifacts_remain_evidence_only_not_authority",
        "how_will_router_authority_remain_canonical",
        "which_tests_block_startup_runtime_background_and_file_watcher_generation",
        "which_freeze_entries_must_be_loaded_before_future_generator_work",
        "which_human_confirmation_gate_is_required_before_future_generation",
    }
)

FORBIDDEN_PLAN_FIELDS = frozenset(
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
    }
)


def _as_set(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return {str(item) for item in value}
    return set()


def build_dry_run_artifact_generation_plan_contract() -> dict[str, Any]:
    """Return the static dry-run plan contract without generation authority."""

    return {
        "plan_id": DRY_RUN_ARTIFACT_GENERATION_PLAN_FEATURE_ID,
        "schema_version": DRY_RUN_ARTIFACT_GENERATION_PLAN_SCHEMA_VERSION,
        "plan_status": "design_only",
        "declared_design_only": True,
        "dry_run_mode": REQUIRED_DRY_RUN_MODE,
        "source_material_policy": sorted(REQUIRED_SOURCE_MATERIAL_POLICY),
        "permitted_plan_outputs": sorted(REQUIRED_PERMITTED_PLAN_OUTPUTS),
        "required_review_gates_before_future_generation": sorted(REQUIRED_REVIEW_GATES),
        "disabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "planned_human_review_questions": sorted(REQUIRED_REVIEW_QUESTIONS),
    }


def validate_dry_run_artifact_generation_plan_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a dry-run plan contract without executing generation."""

    errors: list[str] = []

    missing = sorted(REQUIRED_DRY_RUN_PLAN_FIELDS.difference(candidate.keys()))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    if candidate.get("plan_id") != DRY_RUN_ARTIFACT_GENERATION_PLAN_FEATURE_ID:
        errors.append("plan_id must remain " + DRY_RUN_ARTIFACT_GENERATION_PLAN_FEATURE_ID)

    if candidate.get("schema_version") != DRY_RUN_ARTIFACT_GENERATION_PLAN_SCHEMA_VERSION:
        errors.append("schema_version must remain " + DRY_RUN_ARTIFACT_GENERATION_PLAN_SCHEMA_VERSION)

    if candidate.get("plan_status") not in ALLOWED_PLAN_STATUSES:
        errors.append("plan_status is not allowed")

    if candidate.get("declared_design_only") is not True:
        errors.append("declared_design_only must be true")

    if candidate.get("dry_run_mode") != REQUIRED_DRY_RUN_MODE:
        errors.append("dry_run_mode must remain " + REQUIRED_DRY_RUN_MODE)

    if not REQUIRED_SOURCE_MATERIAL_POLICY.issubset(_as_set(candidate.get("source_material_policy"))):
        errors.append("missing source material policy requirements")

    if not REQUIRED_PERMITTED_PLAN_OUTPUTS.issubset(_as_set(candidate.get("permitted_plan_outputs"))):
        errors.append("missing permitted dry-run plan outputs")

    if not REQUIRED_REVIEW_GATES.issubset(_as_set(candidate.get("required_review_gates_before_future_generation"))):
        errors.append("missing required review gates before future generation")

    disabled_flags = candidate.get("disabled_flags")
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        disabled_flags = {}

    for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
        if flag not in disabled_flags:
            errors.append("missing disabled flag: " + flag)
        elif disabled_flags[flag] is not False:
            errors.append("disabled flag must be false: " + flag)

    if not REQUIRED_FORBIDDEN_ACTIONS.issubset(_as_set(candidate.get("forbidden_actions"))):
        errors.append("missing forbidden dry-run plan actions")

    if not REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(_as_set(candidate.get("no_authority_assertions"))):
        errors.append("missing dry-run no-authority assertions")

    if not REQUIRED_REVIEW_QUESTIONS.issubset(_as_set(candidate.get("planned_human_review_questions"))):
        errors.append("missing human review questions")

    forbidden_present = sorted(field for field in FORBIDDEN_PLAN_FIELDS if field in candidate)
    if forbidden_present:
        errors.append("forbidden plan fields present: " + ", ".join(forbidden_present))

    ok = not errors
    return {
        "ok": ok,
        "valid": ok,
        "errors": errors,
        "feature_id": DRY_RUN_ARTIFACT_GENERATION_PLAN_FEATURE_ID,
        "schema_version": DRY_RUN_ARTIFACT_GENERATION_PLAN_SCHEMA_VERSION,
        "plan_status": candidate.get("plan_status"),
        "dry_run_mode": candidate.get("dry_run_mode"),
        "design_only": candidate.get("declared_design_only") is True,
        "plan_report_only": True,
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reader_authorized": False,
        "artifact_loading_authorized": False,
        "source_scanning_authorized": False,
        "raw_text_materialization_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_generation_authorized": False,
        "provider_execution_authorized": False,
        "startup_generation_authorized": False,
        "runtime_generation_authorized": False,
        "background_generation_authorized": False,
        "semantic_runtime_authorized": False,
        "prompt_router_mutation_authorized": False,
        "prompt_auto_loading_authorized": False,
        "may_proceed_generation_authorized": False,
        "freeze_memory_write_authorized": False,
        "authority_granted": False,
        "review_evidence_only": True,
        "requires_future_governed_patch": True,
    }


def classify_dry_run_artifact_generation_plan_request(action: str) -> dict[str, Any]:
    """Classify a planning request without allowing generation or writes."""

    normalized = " ".join(str(action or "").strip().lower().split())
    plan_markers = (
        "plan",
        "dry run",
        "dry-run",
        "checklist",
        "review",
        "risk register",
        "input manifest",
    )
    activation_markers = (
        "generate artifact",
        "write artifact",
        "create artifact",
        "read artifact",
        "load artifact",
        "embedding",
        "vector",
        "provider",
        "startup",
        "runtime",
        "background",
        "file watcher",
        "enable semantic",
        "auto load",
        "may proceed",
        "write freeze",
    )
    matched_plan_markers = [marker for marker in plan_markers if marker in normalized]
    matched_activation_markers = [marker for marker in activation_markers if marker in normalized]

    return {
        "allowed_now": bool(matched_plan_markers) and not matched_activation_markers,
        "action": str(action or ""),
        "matched_plan_markers": matched_plan_markers,
        "matched_activation_markers": matched_activation_markers,
        "permitted_output": "dry_run_plan_summary" if matched_plan_markers else "generation_denial_report",
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reader_authorized": False,
        "source_scanning_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "startup_generation_authorized": False,
        "runtime_generation_authorized": False,
        "background_generation_authorized": False,
        "semantic_runtime_authorized": False,
        "prompt_router_mutation_authorized": False,
        "freeze_memory_write_authorized": False,
        "authority_granted": False,
        "review_evidence_only": True,
        "requires_future_governed_patch_for_generation": True,
        "reason": "dry-run planning may produce review evidence only and cannot generate artifacts",
    }
