"""Offline corpus governance contract for future semantic evidence.

This module is intentionally standard-library-only and does not generate a
corpus, build embeddings, create vector indexes, read prompt-library files,
read freeze entries, or mutate any project memory. It provides deterministic
validation helpers for a future human-governed corpus-generation plan.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


OFFLINE_CORPUS_GOVERNANCE_FEATURE_ID = "routing_signal_scorer_v3_offline_corpus_governance_design_v1"
OFFLINE_CORPUS_GOVERNANCE_SCHEMA_VERSION = "3.3-offline-corpus-governance"
OFFLINE_CORPUS_GOVERNANCE_STATUS = "design_contract_only_no_generator_no_runtime_behavior_change"

REQUIRED_PLAN_FIELDS = frozenset(
    {
        "governance_id",
        "schema_version",
        "status",
        "trigger",
        "approved_by_human",
        "source_layers",
        "output_artifacts",
        "validation_gates",
        "forbidden_actions",
        "audit_trail",
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

ALLOWED_HUMAN_GOVERNED_TRIGGERS = frozenset(
    {
        "manual_human_governed_rebuild_request",
        "schema_version_change_human_reviewed",
        "source_hash_mismatch_human_reviewed",
        "lifecycle_status_change_human_reviewed",
        "model_version_change_human_reviewed",
        "evaluation_failure_human_reviewed",
    }
)

FORBIDDEN_AUTOMATIC_TRIGGERS = frozenset(
    {
        "startup",
        "runtime_request",
        "file_watcher",
        "background_thread",
        "scheduled_job",
        "automatic_prompt_library_change",
        "automatic_freeze_write",
        "semantic_score_disagreement",
    }
)

REQUIRED_SOURCE_LAYER_FIELDS = frozenset(
    {
        "layer_id",
        "source_type",
        "source_reference",
        "source_structural_hash_required",
        "human_review_required",
        "raw_text_allowed",
    }
)

ALLOWED_SOURCE_TYPES = frozenset(
    {
        "prompt_metadata_record",
        "routing_index_metadata_record",
        "box_manifest_metadata_record",
        "semantic_readiness_canon_metadata_record",
        "metadata_vector_manifest_item",
    }
)

FORBIDDEN_SOURCE_TYPES = frozenset(
    {
        "raw_prompt_text",
        "freeze_entry_text",
        "user_query_text",
        "chat_history",
        "terminal_log_text",
        "runtime_memory",
        "vector_values",
        "embedding_values",
        "external_network_content",
    }
)

REQUIRED_OUTPUT_ARTIFACT_FIELDS = frozenset(
    {
        "artifact_id",
        "artifact_type",
        "canonical_status",
        "contains_vectors",
        "contains_raw_text",
        "requires_freeze_before_runtime_use",
    }
)

ALLOWED_OUTPUT_ARTIFACT_TYPES = frozenset(
    {
        "metadata_vector_manifest_draft",
        "metadata_vector_manifest_candidate",
        "governance_diff_report",
        "validation_report",
    }
)

FORBIDDEN_OUTPUT_ARTIFACT_TYPES = frozenset(
    {
        "embedding_vector_file",
        "vector_index",
        "provider_cache",
        "runtime_cache",
        "freeze_memory_entry",
        "prompt_library_mutation",
        "startup_delivery_mutation",
    }
)

REQUIRED_VALIDATION_GATES = frozenset(
    {
        "metadata_vector_manifest_schema_validation",
        "active_only_eligibility_check",
        "no_authority_fields_check",
        "no_raw_prompt_text_check",
        "no_user_query_text_check",
        "no_freeze_entry_text_check",
        "no_vector_values_check",
        "source_structural_hash_check",
        "human_review_required",
        "diff_review_required",
        "freeze_required_before_runtime_use",
    }
)

REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
        "auto_generate_corpus_at_startup",
        "auto_generate_corpus_at_runtime",
        "auto_rebuild_vector_index",
        "read_raw_prompt_files_at_runtime",
        "read_freeze_entries_at_runtime_for_semantic_search",
        "persist_user_queries",
        "write_freeze_memory",
        "modify_prompt_library",
        "modify_startup_delivery",
        "install_ml_dependency",
        "call_external_embedding_api",
        "create_vector_index",
        "produce_final_route",
        "produce_required_prompts",
        "produce_may_proceed_now",
    }
)

REQUIRED_AUDIT_TRAIL_FIELDS = frozenset(
    {
        "generation_run_id_policy",
        "source_hashes_required",
        "diff_review_required",
        "human_reviewer_required",
        "freeze_before_runtime_use_required",
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


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _as_strings(value: Any) -> set[str]:
    if not _is_sequence(value):
        return set()
    return {item for item in value if isinstance(item, str)}


def _append_missing(errors: list[str], label: str, missing: set[str]) -> None:
    if missing:
        errors.append(f"{label} missing required values: {', '.join(sorted(missing))}")


def _contains_forbidden_key(mapping: Mapping[str, Any], forbidden_keys: set[str] | frozenset[str]) -> set[str]:
    return {key for key in mapping.keys() if key in forbidden_keys}


def validate_offline_corpus_governance_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a future offline corpus-governance plan without authorizing generation.

    The result is advisory evidence only. Even a valid plan does not authorize
    corpus generation, embedding generation, vector-index creation, or runtime use.
    """

    errors: list[str] = []

    if not isinstance(plan, Mapping):
        return {
            "ok": False,
            "feature_id": OFFLINE_CORPUS_GOVERNANCE_FEATURE_ID,
            "schema_version": OFFLINE_CORPUS_GOVERNANCE_SCHEMA_VERSION,
            "status": "invalid",
            "errors": ["plan must be a mapping"],
            "generation_authorized": False,
            "runtime_use_authorized": False,
            "advisory_only": True,
        }

    forbidden_top = _contains_forbidden_key(plan, FORBIDDEN_AUTHORITY_FIELDS)
    if forbidden_top:
        errors.append("plan contains forbidden authority fields: " + ", ".join(sorted(forbidden_top)))

    missing_fields = REQUIRED_PLAN_FIELDS - set(plan.keys())
    _append_missing(errors, "plan", missing_fields)

    schema_version = plan.get("schema_version")
    if schema_version != OFFLINE_CORPUS_GOVERNANCE_SCHEMA_VERSION:
        errors.append(f"schema_version must be {OFFLINE_CORPUS_GOVERNANCE_SCHEMA_VERSION}")

    status = plan.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append("status must be one of: " + ", ".join(sorted(ALLOWED_STATUSES)))

    trigger = plan.get("trigger")
    if trigger in FORBIDDEN_AUTOMATIC_TRIGGERS:
        errors.append(f"trigger is forbidden automatic trigger: {trigger}")
    if trigger not in ALLOWED_HUMAN_GOVERNED_TRIGGERS:
        errors.append("trigger must be a human-governed trigger")

    if plan.get("approved_by_human") is not True:
        errors.append("approved_by_human must be true for governance review readiness")

    source_layers = plan.get("source_layers")
    if not _is_sequence(source_layers) or not source_layers:
        errors.append("source_layers must be a non-empty list")
    else:
        for index, layer in enumerate(source_layers):
            if not isinstance(layer, Mapping):
                errors.append(f"source_layers[{index}] must be a mapping")
                continue
            forbidden_layer_keys = _contains_forbidden_key(layer, FORBIDDEN_AUTHORITY_FIELDS)
            if forbidden_layer_keys:
                errors.append(
                    f"source_layers[{index}] contains forbidden authority fields: "
                    + ", ".join(sorted(forbidden_layer_keys))
                )
            _append_missing(errors, f"source_layers[{index}]", REQUIRED_SOURCE_LAYER_FIELDS - set(layer.keys()))
            source_type = layer.get("source_type")
            if source_type in FORBIDDEN_SOURCE_TYPES:
                errors.append(f"source_layers[{index}] uses forbidden source_type: {source_type}")
            if source_type not in ALLOWED_SOURCE_TYPES:
                errors.append(f"source_layers[{index}] source_type is not allowed: {source_type}")
            if layer.get("source_structural_hash_required") is not True:
                errors.append(f"source_layers[{index}] must require source_structural_hash")
            if layer.get("human_review_required") is not True:
                errors.append(f"source_layers[{index}] must require human review")
            if layer.get("raw_text_allowed") is not False:
                errors.append(f"source_layers[{index}] must forbid raw text")

    output_artifacts = plan.get("output_artifacts")
    if not _is_sequence(output_artifacts) or not output_artifacts:
        errors.append("output_artifacts must be a non-empty list")
    else:
        for index, artifact in enumerate(output_artifacts):
            if not isinstance(artifact, Mapping):
                errors.append(f"output_artifacts[{index}] must be a mapping")
                continue
            forbidden_artifact_keys = _contains_forbidden_key(artifact, FORBIDDEN_AUTHORITY_FIELDS)
            if forbidden_artifact_keys:
                errors.append(
                    f"output_artifacts[{index}] contains forbidden authority fields: "
                    + ", ".join(sorted(forbidden_artifact_keys))
                )
            _append_missing(
                errors,
                f"output_artifacts[{index}]",
                REQUIRED_OUTPUT_ARTIFACT_FIELDS - set(artifact.keys()),
            )
            artifact_type = artifact.get("artifact_type")
            if artifact_type in FORBIDDEN_OUTPUT_ARTIFACT_TYPES:
                errors.append(f"output_artifacts[{index}] uses forbidden artifact_type: {artifact_type}")
            if artifact_type not in ALLOWED_OUTPUT_ARTIFACT_TYPES:
                errors.append(f"output_artifacts[{index}] artifact_type is not allowed: {artifact_type}")
            if artifact.get("canonical_status") != "candidate_generated_evidence_not_canonical_memory":
                errors.append(f"output_artifacts[{index}] must be generated evidence, not canonical memory")
            if artifact.get("contains_vectors") is not False:
                errors.append(f"output_artifacts[{index}] must not contain vectors")
            if artifact.get("contains_raw_text") is not False:
                errors.append(f"output_artifacts[{index}] must not contain raw text")
            if artifact.get("requires_freeze_before_runtime_use") is not True:
                errors.append(f"output_artifacts[{index}] must require freeze before runtime use")

    validation_gates = _as_strings(plan.get("validation_gates"))
    _append_missing(errors, "validation_gates", REQUIRED_VALIDATION_GATES - validation_gates)

    forbidden_actions = _as_strings(plan.get("forbidden_actions"))
    _append_missing(errors, "forbidden_actions", REQUIRED_FORBIDDEN_ACTIONS - forbidden_actions)

    audit_trail = plan.get("audit_trail")
    if not isinstance(audit_trail, Mapping):
        errors.append("audit_trail must be a mapping")
    else:
        _append_missing(errors, "audit_trail", REQUIRED_AUDIT_TRAIL_FIELDS - set(audit_trail.keys()))
        for field in REQUIRED_AUDIT_TRAIL_FIELDS:
            if audit_trail.get(field) is not True:
                errors.append(f"audit_trail.{field} must be true")

    ok = not errors
    return {
        "ok": ok,
        "feature_id": OFFLINE_CORPUS_GOVERNANCE_FEATURE_ID,
        "schema_version": OFFLINE_CORPUS_GOVERNANCE_SCHEMA_VERSION,
        "status": "valid_governance_plan" if ok else "invalid_governance_plan",
        "errors": tuple(errors),
        "generation_authorized": False,
        "runtime_use_authorized": False,
        "advisory_only": True,
        "reason": "Governance design validation only; corpus generation and runtime use require future governed freeze.",
    }


def build_disabled_offline_corpus_governance_status() -> dict[str, Any]:
    """Return the safe default status for the offline corpus-governance phase."""

    return {
        "feature_id": OFFLINE_CORPUS_GOVERNANCE_FEATURE_ID,
        "schema_version": OFFLINE_CORPUS_GOVERNANCE_SCHEMA_VERSION,
        "status": OFFLINE_CORPUS_GOVERNANCE_STATUS,
        "corpus_generation_enabled": False,
        "runtime_manifest_use_enabled": False,
        "embedding_generation_enabled": False,
        "vector_index_generation_enabled": False,
        "external_api_enabled": False,
        "advisory_only": True,
        "reason": "Offline corpus governance is defined as a design/validation contract only in v1.",
    }


def classify_corpus_governance_trigger(trigger: str) -> dict[str, Any]:
    """Classify a corpus-governance trigger as human-governed or forbidden automatic."""

    if trigger in ALLOWED_HUMAN_GOVERNED_TRIGGERS:
        return {
            "trigger": trigger,
            "allowed_for_governance_review": True,
            "automatic_generation_allowed": False,
            "reason": "Trigger is allowed only for explicit human-governed review.",
        }
    if trigger in FORBIDDEN_AUTOMATIC_TRIGGERS:
        return {
            "trigger": trigger,
            "allowed_for_governance_review": False,
            "automatic_generation_allowed": False,
            "reason": "Automatic corpus generation trigger is forbidden.",
        }
    return {
        "trigger": trigger,
        "allowed_for_governance_review": False,
        "automatic_generation_allowed": False,
        "reason": "Unknown trigger is not allowed.",
    }


def build_minimal_valid_governance_plan_template() -> dict[str, Any]:
    """Build a deterministic example plan template for tests and future human review."""

    return {
        "governance_id": "offline-corpus-governance-template-v1",
        "schema_version": OFFLINE_CORPUS_GOVERNANCE_SCHEMA_VERSION,
        "status": "review_ready",
        "trigger": "manual_human_governed_rebuild_request",
        "approved_by_human": True,
        "source_layers": [
            {
                "layer_id": "prompt-metadata-records",
                "source_type": "prompt_metadata_record",
                "source_reference": "future curated metadata records only",
                "source_structural_hash_required": True,
                "human_review_required": True,
                "raw_text_allowed": False,
            }
        ],
        "output_artifacts": [
            {
                "artifact_id": "metadata-vector-manifest-candidate",
                "artifact_type": "metadata_vector_manifest_candidate",
                "canonical_status": "candidate_generated_evidence_not_canonical_memory",
                "contains_vectors": False,
                "contains_raw_text": False,
                "requires_freeze_before_runtime_use": True,
            }
        ],
        "validation_gates": sorted(REQUIRED_VALIDATION_GATES),
        "forbidden_actions": sorted(REQUIRED_FORBIDDEN_ACTIONS),
        "audit_trail": {
            "generation_run_id_policy": True,
            "source_hashes_required": True,
            "diff_review_required": True,
            "human_reviewer_required": True,
            "freeze_before_runtime_use_required": True,
        },
    }
