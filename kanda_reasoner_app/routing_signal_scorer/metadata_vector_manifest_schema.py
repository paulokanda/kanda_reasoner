# project-path: kanda_reasoner_app/routing_signal_scorer/metadata_vector_manifest_schema.py
"""Metadata Vector Manifest schema for future routing_signal_scorer v3 work.

This module is intentionally standard-library-only and does not implement
embeddings, vector search, model loading, corpus generation, prompt loading, or
routing authority. It validates a curated manifest shape that future semantic
providers may consume only after a separate governed generation phase.
"""

from __future__ import annotations


__all__ = [
    'build_empty_metadata_vector_manifest',
    'ManifestValidation',
    'metadata_manifest_item_eligibility_reasons',
    'render_metadata_vector_manifest_validation_text',
    'validate_metadata_vector_manifest',
    'validate_metadata_vector_manifest_item',
]
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

FEATURE_ID = "routing_signal_scorer_v3_metadata_vector_manifest_schema_v1"
SCHEMA_VERSION = "3.2-metadata-vector-manifest"
AUTHORITY = "advisory_schema_only"
DEFAULT_GENERATION_MODE = "schema_only_no_embeddings_no_vectors"
CURRENT_ALLOWED_USE = "advisory_routing_hint"
ACTIVE_LIFECYCLE_STATUS = "active"
VALID_LIFECYCLE_STATUSES = frozenset(
    {
        "proposed",
        "validated",
        "active",
        "deprecated",
        "superseded",
        "archived",
        "experimental",
    }
)

REQUIRED_MANIFEST_FIELDS = frozenset(
    {
        "schema_version",
        "manifest_id",
        "manifest_version",
        "generated_at",
        "generation_mode",
        "authority",
        "source_layer",
        "corpus_hash",
        "items",
    }
)

REQUIRED_ITEM_FIELDS = frozenset(
    {
        "id",
        "label",
        "route_family",
        "isolation_domain",
        "lifecycle_status",
        "source_path",
        "source_version",
        "source_structural_hash",
        "corpus_generation_run_id",
        "embedding_model_id",
        "embedding_model_version",
        "embedding_dimensions",
        "corpus_hash",
        "last_validated",
        "allowed_use",
        "forbidden_use",
        "semantic_summary",
        "canonical_terms",
        "keywords",
        "negative_examples",
        "min_score_threshold",
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
        "router_override",
        "required_prompt_files",
        "load_prompts_now",
        "freeze_write",
        "startup_mutation",
        "prompt_library_mutation",
    }
)

FORBIDDEN_RAW_CONTENT_FIELDS = frozenset(
    {
        "raw_prompt_text",
        "prompt_file_text",
        "freeze_entry_text",
        "freeze_memory_text",
        "user_query_text",
        "user_request_text",
        "conversation_text",
        "chat_history_text",
        "terminal_log_text",
        "raw_source_text",
        "raw_file_text",
    }
)

FORBIDDEN_VECTOR_FIELDS = frozenset(
    {
        "embedding",
        "embeddings",
        "vector",
        "vectors",
        "dense_vector",
        "sparse_vector",
        "vector_index_path",
        "faiss_index_path",
        "qdrant_collection",
        "chroma_collection",
    }
)

FORBIDDEN_RUNTIME_FIELDS = frozenset(
    {
        "provider_instance",
        "model_object",
        "model_cache_path",
        "external_api_key",
        "network_endpoint",
        "runtime_rebuild_enabled",
        "startup_rebuild_enabled",
        "auto_regenerate",
    }
)

FORBIDDEN_FIELDS = (
    FORBIDDEN_AUTHORITY_FIELDS
    | FORBIDDEN_RAW_CONTENT_FIELDS
    | FORBIDDEN_VECTOR_FIELDS
    | FORBIDDEN_RUNTIME_FIELDS
)

ALLOWED_GENERATION_MODES = frozenset(
    {
        "schema_only_no_embeddings_no_vectors",
        "offline_human_governed_manifest",
    }
)

ALLOWED_SOURCE_LAYERS = frozenset(
    {
        "generated_metadata_vector_manifest",
        "offline_human_governed_manifest",
    }
)


@dataclass(frozen=True)
class ManifestValidation:
    """Validation result for one Metadata Vector Manifest."""

    is_valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()


def build_empty_metadata_vector_manifest(
    *,
    manifest_id: str = "routing-signal-scorer-v3-metadata-vector-manifest-empty",
    manifest_version: str = "0.0.0-schema-only",
    generated_at: str = "1970-01-01T00:00:00Z",
) -> dict[str, object]:
    """Return a valid empty schema-only Metadata Vector Manifest.

    The returned manifest contains no embeddings, no vectors, no raw prompt
    text, no user queries, no freeze entries, and no runtime provider settings.
    """

    return {
        "schema_version": SCHEMA_VERSION,
        "manifest_id": str(manifest_id),
        "manifest_version": str(manifest_version),
        "generated_at": str(generated_at),
        "generation_mode": DEFAULT_GENERATION_MODE,
        "authority": AUTHORITY,
        "source_layer": "generated_metadata_vector_manifest",
        "corpus_hash": "sha256:empty-schema-only",
        "items": [],
        "contains_embeddings": False,
        "contains_vectors": False,
        "contains_raw_prompt_text": False,
        "contains_user_queries": False,
        "contains_freeze_entries": False,
        "runtime_rebuild_allowed": False,
        "startup_rebuild_allowed": False,
        "external_api_allowed": False,
        "advisory_only_reason": "metadata manifest schema is evidence preparation only and never routing authority",
    }


def validate_metadata_vector_manifest(manifest: Mapping[str, Any]) -> ManifestValidation:
    """Validate a Metadata Vector Manifest without side effects."""

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(manifest, Mapping):
        return ManifestValidation(False, ("manifest is not a mapping",), ())

    _reject_forbidden_fields(manifest, errors, context="manifest")

    missing = sorted(REQUIRED_MANIFEST_FIELDS - set(manifest.keys()))
    if missing:
        errors.append("manifest missing required fields: " + ", ".join(missing))

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("manifest schema_version mismatch")
    if manifest.get("authority") != AUTHORITY:
        errors.append("manifest authority must be advisory_schema_only")
    if manifest.get("generation_mode") not in ALLOWED_GENERATION_MODES:
        errors.append("manifest generation_mode is not allowed")
    if manifest.get("source_layer") not in ALLOWED_SOURCE_LAYERS:
        errors.append("manifest source_layer is not allowed")

    for boolean_field, expected in {
        "contains_embeddings": False,
        "contains_vectors": False,
        "contains_raw_prompt_text": False,
        "contains_user_queries": False,
        "contains_freeze_entries": False,
        "runtime_rebuild_allowed": False,
        "startup_rebuild_allowed": False,
        "external_api_allowed": False,
    }.items():
        if manifest.get(boolean_field, expected) is not expected:
            errors.append(f"{boolean_field} must be {expected}")

    corpus_hash = manifest.get("corpus_hash")
    if corpus_hash is not None and not _is_sha256_like(str(corpus_hash)):
        errors.append("manifest corpus_hash must be sha256-prefixed")

    items = manifest.get("items", [])
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes, bytearray)):
        errors.append("manifest items must be a list")
        items = []

    seen_ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            errors.append(f"item {index} is not a mapping")
            continue
        validation = validate_metadata_vector_manifest_item(item)
        errors.extend(f"item {index}: {error}" for error in validation.errors)
        warnings.extend(f"item {index}: {warning}" for warning in validation.warnings)
        item_id = str(item.get("id", ""))
        if item_id:
            if item_id in seen_ids:
                errors.append(f"item {index}: duplicate id {item_id}")
            seen_ids.add(item_id)

    return ManifestValidation(not errors, tuple(errors), tuple(warnings))


def validate_metadata_vector_manifest_item(item: Mapping[str, Any]) -> ManifestValidation:
    """Validate one manifest item."""

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(item, Mapping):
        return ManifestValidation(False, ("item is not a mapping",), ())

    _reject_forbidden_fields(item, errors, context="item")

    missing = sorted(REQUIRED_ITEM_FIELDS - set(item.keys()))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    lifecycle = str(item.get("lifecycle_status", ""))
    if lifecycle not in VALID_LIFECYCLE_STATUSES:
        errors.append("lifecycle_status is not allowed")
    elif lifecycle != ACTIVE_LIFECYCLE_STATUS:
        warnings.append("non-active lifecycle_status must not be surfaced by runtime semantic evidence")

    allowed_use = item.get("allowed_use", [])
    if not _is_string_list(allowed_use):
        errors.append("allowed_use must be a list of strings")
    elif CURRENT_ALLOWED_USE not in allowed_use:
        warnings.append("allowed_use does not include advisory_routing_hint")

    forbidden_use = item.get("forbidden_use", [])
    if not _is_string_list(forbidden_use):
        errors.append("forbidden_use must be a list of strings")
    else:
        missing_forbidden = {
            "final_route_decision",
            "required_prompt_decision",
            "may_proceed_now_decision",
            "prompt_auto_loading",
            "freeze_write",
        } - set(forbidden_use)
        if missing_forbidden:
            warnings.append("forbidden_use should explicitly include: " + ", ".join(sorted(missing_forbidden)))

    for hash_field in ("source_structural_hash", "corpus_hash"):
        value = item.get(hash_field)
        if value is not None and not _is_sha256_like(str(value)):
            errors.append(f"{hash_field} must be sha256-prefixed")

    for list_field in ("canonical_terms", "keywords", "negative_examples"):
        if list_field in item and not _is_string_list(item[list_field]):
            errors.append(f"{list_field} must be a list of strings")

    semantic_summary = item.get("semantic_summary")
    if semantic_summary is not None and not isinstance(semantic_summary, str):
        errors.append("semantic_summary must be a string")
    if isinstance(semantic_summary, str) and len(semantic_summary.strip()) < 12:
        warnings.append("semantic_summary is very short")

    try:
        threshold = float(item.get("min_score_threshold", 0.0))
    except (TypeError, ValueError):
        errors.append("min_score_threshold must be numeric")
    else:
        if threshold < 0.0 or threshold > 1.0:
            errors.append("min_score_threshold must be between 0.0 and 1.0")

    try:
        dimensions = int(item.get("embedding_dimensions", 0))
    except (TypeError, ValueError):
        errors.append("embedding_dimensions must be an integer")
    else:
        if dimensions < 0:
            errors.append("embedding_dimensions must not be negative")

    embedding_model_id = str(item.get("embedding_model_id", ""))
    if embedding_model_id.startswith("external_api"):
        errors.append("external API embedding model ids are forbidden in v3 manifest schema")

    return ManifestValidation(not errors, tuple(errors), tuple(warnings))


def metadata_manifest_item_eligibility_reasons(item: Mapping[str, Any]) -> tuple[bool, tuple[str, ...]]:
    """Return whether a manifest item is eligible for future semantic evidence."""

    reasons: list[str] = []
    validation = validate_metadata_vector_manifest_item(item)
    if not validation.is_valid:
        reasons.extend(validation.errors)
    if item.get("lifecycle_status") != ACTIVE_LIFECYCLE_STATUS:
        reasons.append("lifecycle_status is not active")
    if CURRENT_ALLOWED_USE not in item.get("allowed_use", []):
        reasons.append("allowed_use does not include advisory_routing_hint")
    forbidden_use = set(item.get("forbidden_use", [])) if _is_string_list(item.get("forbidden_use", [])) else set()
    if "final_route_decision" not in forbidden_use:
        reasons.append("forbidden_use does not explicitly forbid final_route_decision")
    if str(item.get("source_structural_hash", "")).strip() in {"", "sha256:"}:
        reasons.append("source_structural_hash is empty")
    if str(item.get("corpus_hash", "")).strip() in {"", "sha256:"}:
        reasons.append("corpus_hash is empty")
    return (not reasons, tuple(reasons))


def render_metadata_vector_manifest_validation_text(result: ManifestValidation) -> str:
    """Render compact validation status for logs/UI without authority language."""

    status = "VALID" if result.is_valid else "INVALID"
    lines = [
        f"metadata_vector_manifest_schema={SCHEMA_VERSION}",
        f"status={status}",
        "authority=advisory_schema_only",
        "manifest evidence is not routing authority",
    ]
    if result.errors:
        lines.append("errors:")
        lines.extend(f"- {error}" for error in result.errors)
    if result.warnings:
        lines.append("warnings:")
        lines.extend(f"- {warning}" for warning in result.warnings)
    return "\n".join(lines)


def _reject_forbidden_fields(mapping: Mapping[str, Any], errors: list[str], *, context: str) -> None:
    """Support reject forbidden fields behavior.
    
    Parameters
    ----------
    mapping : Mapping[str, Any]
        The mapping value.
    errors : list[str]
        The error values.
    context : str
        The context value.
    """
    
    found = FORBIDDEN_FIELDS & set(mapping.keys())
    if found:
        errors.append(f"{context} contains forbidden fields: " + ", ".join(sorted(found)))


def _is_string_list(value: object) -> bool:
    """Support is string list behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _is_sha256_like(value: str) -> bool:
    """Support is sha256 like behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return value.startswith("sha256:") and len(value) > len("sha256:")
