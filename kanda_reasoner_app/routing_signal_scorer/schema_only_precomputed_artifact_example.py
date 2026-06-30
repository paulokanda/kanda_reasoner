"""Schema-only precomputed artifact example design contract.

This module is intentionally standard-library-only and design-only. It does
not generate artifacts, write artifacts, read artifacts, load artifacts at
startup or runtime, materialize raw text, materialize embedding values,
materialize vector values, build vector indexes, instantiate providers, run
evaluation, tune thresholds, enable semantic runtime behavior, modify the
prompt router, or mutate project state. It validates a redacted static example
shape for future human review of precomputed semantic evidence artifacts.
"""

from __future__ import annotations


__all__ = [
    'build_disabled_schema_example_status',
    'build_minimal_schema_only_precomputed_artifact_example',
    'validate_schema_only_precomputed_artifact_example',
]
from collections.abc import Mapping, Sequence
from typing import Any


SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_FEATURE_ID = (
    "routing_signal_scorer_v3_schema_only_precomputed_artifact_example_v1"
)
SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_SCHEMA_VERSION = (
    "3.11-schema-only-precomputed-artifact-example"
)
SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_STATUS = (
    "design_fixture_only_no_artifact_generation_no_runtime_behavior_change"
)

REQUIRED_EXAMPLE_FIELDS = frozenset(
    {
        "artifact_example_id",
        "schema_version",
        "example_status",
        "declared_schema_only",
        "source_references",
        "artifact_identity",
        "candidate_records",
        "aggregate_summaries",
        "validation_gates",
        "disabled_flags",
        "forbidden_content_assertions",
        "no_authority_assertions",
        "permitted_uses",
    }
)

REQUIRED_SOURCE_REFERENCES = frozenset(
    {
        "metadata_vector_manifest_schema_ref",
        "offline_evaluation_gold_set_schema_ref",
        "precomputed_artifact_design_ref",
        "disabled_artifact_reader_boundary_ref",
        "advisory_artifact_ui_preview_design_ref",
    }
)

REQUIRED_CANDIDATE_FIELDS = frozenset(
    {
        "candidate_id",
        "source_manifest_item_id",
        "candidate_kind",
        "redacted_label",
        "synthetic_case_reference",
        "eligibility_status",
        "staleness_status",
        "authority_status",
        "privacy_status",
        "score_bucket_placeholder",
        "review_note",
    }
)

ALLOWED_CANDIDATE_KINDS = frozenset(
    {
        "active_prompt_metadata",
        "routing_group_metadata",
        "freeze_memory_metadata",
        "synthetic_negative_control",
        "synthetic_near_miss_control",
    }
)

REQUIRED_AGGREGATE_SUMMARIES = frozenset(
    {
        "candidate_count_by_kind",
        "eligible_candidate_count",
        "suppressed_stale_candidate_count",
        "suppressed_deprecated_candidate_count",
        "privacy_rejection_count",
        "authority_leakage_count",
        "schema_validation_status",
    }
)

REQUIRED_VALIDATION_GATES = frozenset(
    {
        "schema_version_matches",
        "source_manifest_reference_present",
        "gold_set_reference_present",
        "no_raw_text_fields_present",
        "no_embedding_values_present",
        "no_vector_values_present",
        "no_vector_index_present",
        "no_provider_config_present",
        "no_authority_fields_present",
        "review_evidence_only_output",
        "runtime_enablement_absent",
    }
)

REQUIRED_DISABLED_FLAGS_FALSE = frozenset(
    {
        "artifact_example_is_runtime_artifact",
        "artifact_generation_enabled",
        "artifact_writing_enabled",
        "artifact_reader_enabled",
        "artifact_loading_enabled",
        "startup_loading_enabled",
        "runtime_loading_enabled",
        "background_loading_enabled",
        "file_watcher_loading_enabled",
        "raw_text_materialization_enabled",
        "embedding_value_materialization_enabled",
        "vector_value_materialization_enabled",
        "vector_index_loading_enabled",
        "provider_execution_enabled",
        "evaluation_execution_enabled",
        "threshold_auto_tuning_enabled",
        "prompt_router_mutation_enabled",
        "write_freeze_memory_enabled",
    }
)

REQUIRED_FORBIDDEN_CONTENT_ASSERTIONS = frozenset(
    {
        "contains_no_raw_user_query_text",
        "contains_no_private_project_text",
        "contains_no_prompt_body_text",
        "contains_no_freeze_entry_text",
        "contains_no_terminal_log_text",
        "contains_no_embedding_values",
        "contains_no_vector_values",
        "contains_no_vector_index",
        "contains_no_provider_config",
        "contains_no_model_config",
        "contains_no_credentials",
        "contains_no_authority_fields",
    }
)

REQUIRED_NO_AUTHORITY_ASSERTIONS = frozenset(
    {
        "example_is_advisory_only",
        "example_is_review_evidence_only",
        "example_must_not_choose_route",
        "example_must_not_choose_required_prompts",
        "example_must_not_decide_may_proceed",
        "example_must_not_load_prompts",
        "example_must_not_mutate_router",
        "example_must_not_write_freeze_memory",
        "canon_remains_final_authority",
    }
)

REQUIRED_PERMITTED_USES = frozenset(
    {
        "schema_documentation_only",
        "static_validation_fixture_only",
        "human_review_training_only",
        "redacted_metadata_preview_training_only",
        "review_evidence_only",
        "no_runtime_enablement",
        "no_prompt_loading",
        "no_final_route_signal",
        "no_may_proceed_signal",
    }
)

FORBIDDEN_FIELD_NAMES = frozenset(
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
        "mutate_prompt_router",
    }
)


def _as_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return value


def _as_sequence(value: Any, name: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a sequence")
    return value


def _missing(required: frozenset[str], actual: Any) -> tuple[str, ...]:
    return tuple(sorted(required.difference(set(_as_sequence(actual, "sequence")))))


def _walk_field_names(value: Any) -> tuple[str, ...]:
    names: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            names.append(str(key))
            names.extend(_walk_field_names(nested))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for item in value:
            names.extend(_walk_field_names(item))
    return tuple(names)


def build_minimal_schema_only_precomputed_artifact_example() -> dict[str, Any]:
    """Return a redacted schema-only example fixture dictionary."""

    return {
        "artifact_example_id": SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_FEATURE_ID,
        "schema_version": SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_SCHEMA_VERSION,
        "example_status": "schema_only_static_fixture",
        "declared_schema_only": True,
        "source_references": {
            "metadata_vector_manifest_schema_ref": "routing_signal_scorer_v3_metadata_vector_manifest_schema_v1",
            "offline_evaluation_gold_set_schema_ref": "routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1",
            "precomputed_artifact_design_ref": "routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design_v1",
            "disabled_artifact_reader_boundary_ref": "routing_signal_scorer_v3_disabled_artifact_reader_boundary_design_v1",
            "advisory_artifact_ui_preview_design_ref": "routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design_v1",
        },
        "artifact_identity": {
            "artifact_kind": "redacted_schema_example_fixture",
            "structural_hash_placeholder": "sha256:redacted-static-fixture-placeholder",
            "source_schema_version": "3.8-precomputed-semantic-evidence-artifact-design",
            "review_evidence_only": True,
            "runtime_eligible": False,
        },
        "candidate_records": [
            {
                "candidate_id": "synthetic-active-prompt-metadata-001",
                "source_manifest_item_id": "synthetic-manifest-item-001",
                "candidate_kind": "active_prompt_metadata",
                "redacted_label": "Synthetic active prompt metadata label",
                "synthetic_case_reference": "positive_routing_cases.synthetic.001",
                "eligibility_status": "eligible_for_human_review_only",
                "staleness_status": "not_stale_in_fixture",
                "authority_status": "no_authority_fields_present",
                "privacy_status": "redacted_metadata_only",
                "score_bucket_placeholder": "high_bucket_without_numeric_vector",
                "review_note": "Synthetic metadata-only example; no private or raw text.",
            },
            {
                "candidate_id": "synthetic-near-miss-control-001",
                "source_manifest_item_id": "synthetic-manifest-item-002",
                "candidate_kind": "synthetic_near_miss_control",
                "redacted_label": "Synthetic near-miss metadata label",
                "synthetic_case_reference": "near_miss_cases.synthetic.001",
                "eligibility_status": "suppressed_for_human_review_training",
                "staleness_status": "not_stale_in_fixture",
                "authority_status": "no_authority_fields_present",
                "privacy_status": "redacted_metadata_only",
                "score_bucket_placeholder": "near_miss_bucket_without_numeric_vector",
                "review_note": "Synthetic control only; no routing or prompt-loading authority.",
            },
        ],
        "aggregate_summaries": {
            "candidate_count_by_kind": {
                "active_prompt_metadata": 1,
                "synthetic_near_miss_control": 1,
            },
            "eligible_candidate_count": 1,
            "suppressed_stale_candidate_count": 0,
            "suppressed_deprecated_candidate_count": 0,
            "privacy_rejection_count": 0,
            "authority_leakage_count": 0,
            "schema_validation_status": "example_fixture_passes_design_checks",
        },
        "validation_gates": sorted(REQUIRED_VALIDATION_GATES),
        "disabled_flags": {flag: False for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "forbidden_content_assertions": sorted(REQUIRED_FORBIDDEN_CONTENT_ASSERTIONS),
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "permitted_uses": sorted(REQUIRED_PERMITTED_USES),
    }


def validate_schema_only_precomputed_artifact_example(example: Mapping[str, Any]) -> tuple[str, ...]:
    """Validate a schema-only example fixture and return advisory notes."""

    record = _as_mapping(example, "example")
    missing_top = tuple(sorted(REQUIRED_EXAMPLE_FIELDS.difference(record)))
    if missing_top:
        raise ValueError(f"missing required example fields: {missing_top}")

    if record["artifact_example_id"] != SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_FEATURE_ID:
        raise ValueError("artifact_example_id mismatch")
    if record["schema_version"] != SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_SCHEMA_VERSION:
        raise ValueError("schema_version mismatch")
    if record["declared_schema_only"] is not True:
        raise ValueError("declared_schema_only must be true")
    if record["example_status"] not in {"schema_only_static_fixture", "rejected"}:
        raise ValueError("example_status must be schema_only_static_fixture or rejected")

    forbidden_present = sorted(FORBIDDEN_FIELD_NAMES.intersection(_walk_field_names(record)))
    if forbidden_present:
        raise ValueError(f"forbidden field names present: {tuple(forbidden_present)}")

    source_references = _as_mapping(record["source_references"], "source_references")
    missing_sources = tuple(sorted(REQUIRED_SOURCE_REFERENCES.difference(source_references)))
    if missing_sources:
        raise ValueError(f"missing source references: {missing_sources}")

    identity = _as_mapping(record["artifact_identity"], "artifact_identity")
    if identity.get("runtime_eligible") is not False:
        raise ValueError("artifact example must not be runtime eligible")
    if identity.get("review_evidence_only") is not True:
        raise ValueError("artifact example must be review-evidence-only")

    candidates = _as_sequence(record["candidate_records"], "candidate_records")
    if not candidates:
        raise ValueError("candidate_records must not be empty")
    for candidate in candidates:
        candidate_mapping = _as_mapping(candidate, "candidate")
        missing_candidate = tuple(sorted(REQUIRED_CANDIDATE_FIELDS.difference(candidate_mapping)))
        if missing_candidate:
            raise ValueError(f"candidate missing required fields: {missing_candidate}")
        if candidate_mapping["candidate_kind"] not in ALLOWED_CANDIDATE_KINDS:
            raise ValueError("candidate_kind is not allowed")
        if candidate_mapping["authority_status"] != "no_authority_fields_present":
            raise ValueError("candidate authority_status must preserve no-authority boundary")
        if candidate_mapping["privacy_status"] != "redacted_metadata_only":
            raise ValueError("candidate privacy_status must remain redacted metadata only")

    aggregate_summaries = _as_mapping(record["aggregate_summaries"], "aggregate_summaries")
    missing_aggregates = tuple(sorted(REQUIRED_AGGREGATE_SUMMARIES.difference(aggregate_summaries)))
    if missing_aggregates:
        raise ValueError(f"missing aggregate summaries: {missing_aggregates}")
    if aggregate_summaries["authority_leakage_count"] != 0:
        raise ValueError("authority_leakage_count must be zero")
    if aggregate_summaries["privacy_rejection_count"] != 0:
        raise ValueError("privacy_rejection_count must be zero in the static fixture")

    disabled_flags = _as_mapping(record["disabled_flags"], "disabled_flags")
    for flag in REQUIRED_DISABLED_FLAGS_FALSE:
        if disabled_flags.get(flag) is not False:
            raise ValueError(f"disabled flag must be false: {flag}")

    missing_gates = _missing(REQUIRED_VALIDATION_GATES, record["validation_gates"])
    if missing_gates:
        raise ValueError(f"missing validation gates: {missing_gates}")
    missing_forbidden_assertions = _missing(
        REQUIRED_FORBIDDEN_CONTENT_ASSERTIONS,
        record["forbidden_content_assertions"],
    )
    if missing_forbidden_assertions:
        raise ValueError(f"missing forbidden content assertions: {missing_forbidden_assertions}")
    missing_no_authority = _missing(REQUIRED_NO_AUTHORITY_ASSERTIONS, record["no_authority_assertions"])
    if missing_no_authority:
        raise ValueError(f"missing no-authority assertions: {missing_no_authority}")
    missing_permitted = _missing(REQUIRED_PERMITTED_USES, record["permitted_uses"])
    if missing_permitted:
        raise ValueError(f"missing permitted uses: {missing_permitted}")

    return (
        "schema-only static fixture accepted for human review training only",
        "no raw text, vector values, provider config, or authority fields detected",
        "no runtime, startup, artifact loading, threshold tuning, or router mutation enabled",
    )


def build_disabled_schema_example_status() -> dict[str, Any]:
    """Return disabled status for this design-only fixture phase."""

    return {
        "feature_id": SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_FEATURE_ID,
        "schema_version": SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_SCHEMA_VERSION,
        "status": SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_STATUS,
        "artifact_example_generation_enabled": False,
        "artifact_example_runtime_enabled": False,
        "artifact_reader_enabled": False,
        "artifact_loading_enabled": False,
        "semantic_runtime_enabled": False,
        "router_authority_enabled": False,
        "review_evidence_only": True,
    }
