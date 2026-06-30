# project-path: kanda_reasoner_app/routing_signal_scorer/generator_candidate_side_effect_boundary_design.py
"""Generator candidate side-effect boundary design for routing scorer v3.

This module is intentionally standard-library-only and side-effect-boundary-design-only. It
models the side-effect boundary metadata that a future, separately governed generator
candidate patch would have to satisfy before any side-effect can be introduced. It does not create a generator candidate
patch, does not authorize a generator, does not record a human decision, does
not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors,
does not instantiate providers, does not run semantic scoring, does not modify
router authority, and does not change runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

__all__ = [
    'build_generator_candidate_side_effect_boundary_contract',
    'classify_generator_candidate_side_effect_boundary_request',
    'validate_generator_candidate_side_effect_boundary_contract',
]

from kanda_reasoner_app.routing_signal_scorer._generator_candidate_side_effect_boundary_constants import (
    GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_FEATURE_ID,
    GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_SCHEMA_VERSION,
    GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_STATUS,
    REQUIRED_SIDE_EFFECT_BOUNDARY_FIELDS,
    REQUIRED_SIDE_EFFECT_BOUNDARY_SCOPE,
    ALLOWED_CURRENT_SIDE_EFFECT_BOUNDARY_STATES,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_SIDE_EFFECT_BOUNDARY_SECTIONS,
    REQUIRED_CANDIDATE_PATCH_DECLARATIONS,
    REQUIRED_BOUNDARY_DECLARATIONS,
    REQUIRED_VALIDATION_DECLARATIONS,
    ALLOWED_FUTURE_SIDE_EFFECT_BOUNDARY_OUTCOMES,
    REQUIRED_ALLOWED_SIDE_EFFECT_BOUNDARY_OUTPUTS,
    REQUIRED_PROHIBITED_SIDE_EFFECT_BOUNDARY_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_SIDE_EFFECT_BOUNDARY_EFFECT_POLICY,
    REQUIRED_STOP_CONDITIONS,
    FORBIDDEN_SIDE_EFFECT_BOUNDARY_FIELDS,
)


def _sorted_tuple(values: frozenset[str]) -> tuple[str, ...]:
    """Support sorted tuple behavior.
    
    Parameters
    ----------
    values : frozenset[str]
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return tuple(sorted(values))


def build_generator_candidate_side_effect_boundary_contract() -> dict[str, Any]:
    """Return the frozen design contract for generator candidate side-effect boundary."""

    return {
        "schema_id": GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_STATUS,
        "declared_generator_candidate_side_effect_boundary_only": True,
        "side_effect_boundary_scope": REQUIRED_SIDE_EFFECT_BOUNDARY_SCOPE,
        "current_side_effect_boundary_state": "not_side_effect_boundary_defined",
        "current_side_effect_boundary_effect": "no_effect_schema_only_not_side_effect_boundary_defined",
        "required_prior_milestones": _sorted_tuple(REQUIRED_PRIOR_MILESTONES),
        "required_side_effect_boundary_sections": _sorted_tuple(REQUIRED_SIDE_EFFECT_BOUNDARY_SECTIONS),
        "required_candidate_patch_declarations": _sorted_tuple(REQUIRED_CANDIDATE_PATCH_DECLARATIONS),
        "required_boundary_declarations": _sorted_tuple(REQUIRED_BOUNDARY_DECLARATIONS),
        "required_validation_declarations": _sorted_tuple(REQUIRED_VALIDATION_DECLARATIONS),
        "allowed_future_side_effect_boundary_outcomes": _sorted_tuple(ALLOWED_FUTURE_SIDE_EFFECT_BOUNDARY_OUTCOMES),
        "allowed_side_effect_boundary_outputs": _sorted_tuple(REQUIRED_ALLOWED_SIDE_EFFECT_BOUNDARY_OUTPUTS),
        "prohibited_side_effect_boundary_outputs": _sorted_tuple(REQUIRED_PROHIBITED_SIDE_EFFECT_BOUNDARY_OUTPUTS),
        "disabled_flags": {key: False for key in sorted(REQUIRED_DISABLED_FLAGS_FALSE)},
        "no_authority_assertions": _sorted_tuple(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "side_effect_boundary_effect_policy": _sorted_tuple(REQUIRED_SIDE_EFFECT_BOUNDARY_EFFECT_POLICY),
        "stop_conditions": _sorted_tuple(REQUIRED_STOP_CONDITIONS),
    }


def _as_set(value: object) -> set[str]:
    """Support as set behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    if isinstance(value, str) or not isinstance(value, Sequence):
        return set()
    return {item for item in value if isinstance(item, str)}


def validate_generator_candidate_side_effect_boundary_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a candidate side_effect_boundary design contract without side effects."""

    errors: list[str] = []
    for field in sorted(REQUIRED_SIDE_EFFECT_BOUNDARY_FIELDS):
        if field not in candidate:
            errors.append(f"missing required field: {field}")

    for field in sorted(FORBIDDEN_SIDE_EFFECT_BOUNDARY_FIELDS):
        if field in candidate:
            errors.append(f"forbidden side_effect_boundary field present: {field}")

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_SIDE_EFFECT_BOUNDARY_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_side_effect_boundary_only") is not True:
        errors.append("contract must declare side_effect_boundary-only mode")
    if candidate.get("side_effect_boundary_scope") != REQUIRED_SIDE_EFFECT_BOUNDARY_SCOPE:
        errors.append("side_effect_boundary_scope mismatch")
    if candidate.get("current_side_effect_boundary_state") not in ALLOWED_CURRENT_SIDE_EFFECT_BOUNDARY_STATES:
        errors.append("current_side_effect_boundary_state is not allowed")
    if candidate.get("current_side_effect_boundary_effect") != "no_effect_schema_only_not_side_effect_boundary_defined":
        errors.append("current_side_effect_boundary_effect must remain schema-only/no-effect")

    required_sets = {
        "required_prior_milestones": REQUIRED_PRIOR_MILESTONES,
        "required_side_effect_boundary_sections": REQUIRED_SIDE_EFFECT_BOUNDARY_SECTIONS,
        "required_candidate_patch_declarations": REQUIRED_CANDIDATE_PATCH_DECLARATIONS,
        "required_boundary_declarations": REQUIRED_BOUNDARY_DECLARATIONS,
        "required_validation_declarations": REQUIRED_VALIDATION_DECLARATIONS,
        "allowed_future_side_effect_boundary_outcomes": ALLOWED_FUTURE_SIDE_EFFECT_BOUNDARY_OUTCOMES,
        "allowed_side_effect_boundary_outputs": REQUIRED_ALLOWED_SIDE_EFFECT_BOUNDARY_OUTPUTS,
        "prohibited_side_effect_boundary_outputs": REQUIRED_PROHIBITED_SIDE_EFFECT_BOUNDARY_OUTPUTS,
        "no_authority_assertions": REQUIRED_NO_AUTHORITY_ASSERTIONS,
        "side_effect_boundary_effect_policy": REQUIRED_SIDE_EFFECT_BOUNDARY_EFFECT_POLICY,
        "stop_conditions": REQUIRED_STOP_CONDITIONS,
    }
    for field, required in required_sets.items():
        actual = _as_set(candidate.get(field))
        missing = sorted(required.difference(actual))
        if missing:
            errors.append(f"{field} missing required values: {missing}")

    disabled_flags = candidate.get("disabled_flags")
    if not isinstance(disabled_flags, Mapping):
        errors.append("disabled_flags must be a mapping")
    else:
        for flag in sorted(REQUIRED_DISABLED_FLAGS_FALSE):
            if disabled_flags.get(flag) is not False:
                errors.append(f"disabled flag must be false: {flag}")

    ok = not errors
    return {
        "ok": ok,
        "errors": tuple(errors),
        "schema_id": candidate.get("schema_id"),
        "schema_version": candidate.get("schema_version"),
        "current_side_effect_boundary_state": candidate.get("current_side_effect_boundary_state"),
        "real_human_decision_recorded_by_side_effect_boundary": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_implementation_authorized": False,
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
        "requires_prior_recorded_human_decision": True,
        "requires_prior_generator_candidate_patch_preflight": True,
        "requires_prior_generator_candidate_patch_envelope": True,
        "requires_prior_generator_candidate_patch_skeleton": True,
        "requires_prior_generator_candidate_patch_file_set": True,
        "requires_prior_generator_candidate_dependency_boundary": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_side_effect_boundary_request(action: str) -> dict[str, Any]:
    """Classify whether an action is allowed by this design-only side_effect_boundary."""

    lowered = action.lower()
    unsafe_terms = (
        "create candidate patch",
        "candidate patch now",
        "authorize generator",
        "implement generator",
        "generate artifact",
        "write artifact",
        "read artifact",
        "load artifact",
        "scan source",
        "scan prompt",
        "raw text",
        "embedding",
        "vector",
        "provider",
        "model",
        "network",
        "credential",
        "runtime semantic",
        "router authority",
        "may proceed",
        "auto-load",
        "freeze memory write",
    )
    safe_terms = (
        "show",
        "view",
        "schema",
        "checklist",
        "side_effect_boundary",
        "sections",
        "declarations",
    )
    allowed_now = any(term in lowered for term in safe_terms) and not any(
        term in lowered for term in unsafe_terms
    )
    return {
        "allowed_now": allowed_now,
        "permitted_output": "generator_candidate_side_effect_boundary_schema" if allowed_now else None,
        "current_side_effect_boundary_state": "not_side_effect_boundary_defined",
        "real_human_decision_recorded_by_side_effect_boundary": False,
        "generator_candidate_patch_created": False,
        "generator_candidate_patch_authorized": False,
        "generator_implementation_authorized": False,
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
        "requires_prior_recorded_human_decision": True,
        "requires_prior_generator_candidate_patch_preflight": True,
        "requires_prior_generator_candidate_patch_envelope": True,
        "requires_prior_generator_candidate_patch_skeleton": True,
        "requires_prior_generator_candidate_patch_file_set": True,
        "requires_prior_generator_candidate_dependency_boundary": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
