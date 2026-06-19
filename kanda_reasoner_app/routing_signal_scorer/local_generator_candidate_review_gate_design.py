"""Local generator candidate review gate design for routing scorer v3.

This module is intentionally standard-library-only and review-only. It does not
implement artifact generation, write artifacts, read artifacts, scan source
material, generate embeddings, materialize vectors, instantiate providers, run
semantic scoring, modify router authority, load prompts, write freeze memory, or
change runtime behavior. It only defines a static review-gate contract that must
be satisfied before any future separately governed local generator candidate can
be proposed.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_FEATURE_ID = (
    "routing_signal_scorer_v3_local_generator_candidate_review_gate_design_v1"
)
LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_SCHEMA_VERSION = (
    "3.14-local-generator-candidate-review-gate-design"
)
LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_STATUS = (
    "review_gate_only_no_generator_no_artifact_write_no_runtime_behavior_change"
)

REQUIRED_REVIEW_GATE_FIELDS = frozenset(
    {
        "gate_id",
        "schema_version",
        "gate_status",
        "declared_review_only",
        "candidate_scope",
        "required_prerequisites",
        "allowed_review_outputs",
        "required_human_decisions",
        "required_evidence_before_candidate_patch",
        "disabled_flags",
        "forbidden_actions",
        "no_authority_assertions",
        "permanent_blockers",
    }
)

REQUIRED_CANDIDATE_SCOPE = "local_generator_candidate_review_only"

ALLOWED_GATE_STATUSES = frozenset(
    {
        "review_only",
        "review_gate_ready",
        "blocked",
        "rejected",
    }
)

REQUIRED_PREREQUISITES = frozenset(
    {
        "v3_closure_shield_frozen",
        "disabled_generation_boundary_frozen",
        "dry_run_artifact_generation_plan_frozen",
        "freeze_hint_state_machine_regressions_passing",
        "runtime_lite_advisory_only_regressions_passing",
        "full_relevant_freeze_entries_loaded_if_compact_summary_hidden",
        "explicit_human_request_for_generator_candidate_review",
    }
)

REQUIRED_ALLOWED_REVIEW_OUTPUTS = frozenset(
    {
        "candidate_readiness_summary",
        "candidate_risk_register",
        "candidate_input_manifest_requirements",
        "candidate_privacy_review_requirements",
        "candidate_dependency_review_requirements",
        "candidate_resource_budget_requirements",
        "candidate_validation_matrix_requirements",
        "candidate_failure_blockers",
        "candidate_patch_boundary_recommendation",
        "human_review_queue_only",
        "review_evidence_only",
        "no_artifact_generated",
        "no_artifact_written",
        "no_runtime_enablement",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

REQUIRED_HUMAN_DECISIONS = frozenset(
    {
        "decide_whether_generator_candidate_is_allowed_to_be_proposed",
        "approve_exact_candidate_input_manifest_before_any_generation_patch",
        "approve_redaction_policy_before_any_generation_patch",
        "approve_dependency_policy_before_any_generation_patch",
        "approve_resource_budget_before_any_generation_patch",
        "approve_no_authority_boundary_before_any_generation_patch",
        "approve_freeze_plan_before_any_generation_patch",
    }
)

REQUIRED_EVIDENCE_BEFORE_CANDIDATE_PATCH = frozenset(
    {
        "local_generator_candidate_review_gate_validation_ok",
        "dry_run_artifact_generation_plan_validation_ok",
        "disabled_generation_boundary_validation_ok",
        "v3_closure_shield_validation_ok",
        "privacy_review_written_evidence",
        "dependency_review_written_evidence",
        "resource_budget_written_evidence",
        "redaction_review_written_evidence",
        "authority_leakage_review_written_evidence",
        "human_confirmation_of_candidate_scope",
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

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "create_generator_candidate_patch_from_review_gate",
        "generate_artifact_from_review_gate",
        "write_artifact_from_review_gate",
        "overwrite_artifact_from_review_gate",
        "read_artifact_from_review_gate",
        "load_artifact_from_review_gate",
        "scan_prompt_library_from_review_gate",
        "scan_freeze_entries_from_review_gate",
        "scan_project_source_from_review_gate",
        "capture_runtime_user_query_from_review_gate",
        "materialize_raw_prompt_text",
        "materialize_raw_user_query_text",
        "materialize_source_text",
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
        "review_gate_is_design_only",
        "review_gate_is_review_evidence_only",
        "review_gate_must_not_authorize_generator_candidate_patch_by_itself",
        "review_gate_must_not_generate_artifacts",
        "review_gate_must_not_choose_route",
        "review_gate_must_not_choose_required_prompts",
        "review_gate_must_not_decide_may_proceed",
        "review_gate_must_not_load_prompts",
        "review_gate_must_not_mutate_router",
        "review_gate_must_not_enable_semantic_runtime",
        "review_gate_must_not_write_freeze_memory",
        "canon_remains_final_authority",
        "future_generator_candidate_requires_separate_governed_patch",
    }
)

REQUIRED_PERMANENT_BLOCKERS = frozenset(
    {
        "missing_explicit_human_request",
        "missing_privacy_review",
        "missing_dependency_review",
        "missing_resource_budget_review",
        "missing_redaction_review",
        "missing_authority_leakage_review",
        "missing_input_manifest_review",
        "request_to_generate_now",
        "request_to_write_artifacts_now",
        "request_to_scan_sources_now",
        "request_to_materialize_raw_text_now",
        "request_to_generate_embeddings_now",
        "request_to_enable_provider_now",
        "request_to_enable_runtime_semantics_now",
        "request_to_modify_router_authority_now",
        "request_to_bypass_future_governed_patch",
    }
)

FORBIDDEN_GATE_FIELDS = frozenset(
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
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return {str(item) for item in value}
    return set()


def _flag_is_false(flags: Mapping[str, Any], name: str) -> bool:
    return flags.get(name) is False


def build_local_generator_candidate_review_gate_contract() -> dict[str, Any]:
    """Return the static review-gate contract for a future generator candidate."""
    return {
        "gate_id": LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_FEATURE_ID,
        "schema_version": LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_SCHEMA_VERSION,
        "gate_status": "review_only",
        "declared_review_only": True,
        "candidate_scope": REQUIRED_CANDIDATE_SCOPE,
        "required_prerequisites": sorted(REQUIRED_PREREQUISITES),
        "allowed_review_outputs": sorted(REQUIRED_ALLOWED_REVIEW_OUTPUTS),
        "required_human_decisions": sorted(REQUIRED_HUMAN_DECISIONS),
        "required_evidence_before_candidate_patch": sorted(
            REQUIRED_EVIDENCE_BEFORE_CANDIDATE_PATCH
        ),
        "disabled_flags": {
            name: False for name in sorted(REQUIRED_DISABLED_FLAGS_FALSE)
        },
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "permanent_blockers": sorted(REQUIRED_PERMANENT_BLOCKERS),
    }


def validate_local_generator_candidate_review_gate_contract(
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate the review gate without authorizing generator behavior."""
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

    extra_forbidden = sorted(FORBIDDEN_GATE_FIELDS.intersection(contract.keys()))
    if extra_forbidden:
        errors.append("forbidden gate fields present: " + ", ".join(extra_forbidden))

    missing_fields = sorted(REQUIRED_REVIEW_GATE_FIELDS.difference(contract.keys()))
    if missing_fields:
        errors.append("missing required fields: " + ", ".join(missing_fields))

    if contract.get("gate_id") != LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_FEATURE_ID:
        errors.append("gate_id mismatch")
    if contract.get("schema_version") != LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if contract.get("gate_status") not in ALLOWED_GATE_STATUSES:
        errors.append("gate_status is not allowed")
    if contract.get("declared_review_only") is not True:
        errors.append("declared_review_only must be true")
    if contract.get("candidate_scope") != REQUIRED_CANDIDATE_SCOPE:
        errors.append("candidate_scope mismatch")

    prerequisites = _as_set(contract.get("required_prerequisites"))
    if not REQUIRED_PREREQUISITES.issubset(prerequisites):
        errors.append("required prerequisites incomplete")

    outputs = _as_set(contract.get("allowed_review_outputs"))
    if not REQUIRED_ALLOWED_REVIEW_OUTPUTS.issubset(outputs):
        errors.append("allowed review outputs incomplete")

    decisions = _as_set(contract.get("required_human_decisions"))
    if not REQUIRED_HUMAN_DECISIONS.issubset(decisions):
        errors.append("required human decisions incomplete")

    evidence = _as_set(contract.get("required_evidence_before_candidate_patch"))
    if not REQUIRED_EVIDENCE_BEFORE_CANDIDATE_PATCH.issubset(evidence):
        errors.append("required evidence before candidate patch incomplete")

    flags = contract.get("disabled_flags")
    if not isinstance(flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        flags = {}

    false_missing = sorted(
        name for name in REQUIRED_DISABLED_FLAGS_FALSE if not _flag_is_false(flags, name)
    )
    if false_missing:
        errors.append("required disabled flags must be false: " + ", ".join(false_missing))

    forbidden = _as_set(contract.get("forbidden_actions"))
    if not REQUIRED_FORBIDDEN_ACTIONS.issubset(forbidden):
        errors.append("forbidden actions incomplete")

    no_authority = _as_set(contract.get("no_authority_assertions"))
    if not REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(no_authority):
        errors.append("no-authority assertions incomplete")

    blockers = _as_set(contract.get("permanent_blockers"))
    if not REQUIRED_PERMANENT_BLOCKERS.issubset(blockers):
        errors.append("permanent blockers incomplete")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "gate_id": contract.get("gate_id"),
        "schema_version": contract.get("schema_version"),
        "gate_status": contract.get("gate_status"),
        "generator_candidate_patch_authorized": False,
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
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


def classify_local_generator_candidate_review_request(request_text: str) -> dict[str, Any]:
    """Classify review requests while denying activation/generation requests."""
    normalized = str(request_text or "").strip().lower()
    activation_terms = (
        "generate",
        "write artifact",
        "create artifact",
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
        "review",
        "gate",
        "candidate",
        "risk",
        "readiness",
        "checklist",
        "plan",
        "boundary",
    )
    denied = any(term in normalized for term in activation_terms)
    review_like = any(term in normalized for term in review_terms)

    if review_like and not denied:
        return {
            "allowed_now": True,
            "permitted_output": "candidate_readiness_summary",
            "review_evidence_only": True,
            "generator_candidate_patch_authorized": False,
            "artifact_generation_authorized": False,
            "artifact_writing_authorized": False,
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
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "authority_granted": False,
        "requires_future_governed_patch_for_generation": True,
    }
