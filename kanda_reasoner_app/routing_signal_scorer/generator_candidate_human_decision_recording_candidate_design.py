"""Generator candidate human decision recording candidate design for routing scorer v3.

This module is intentionally standard-library-only and human-decision-recording-candidate-schema-only.
It follows the generator candidate human decision recording boundary and defines how a
future decision-recording candidate could be described for review. The current candidate
state remains not-created and the current decision remains not_recorded.

It does not record or write a real human decision, does not infer approval from prior
schemas or from "continue", does not approve or authorize a candidate patch, does not
authorize a generator, does not install dependencies, does not authorize side effects,
does not generate, write, read, load, or discover semantic artifacts, does not scan
sources, does not materialize raw text, does not generate embeddings or vectors, does
not instantiate providers, does not run semantic scoring, does not modify router
authority, and does not change runtime behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

__all__ = [
    'build_generator_candidate_human_decision_recording_candidate_contract',
    'classify_generator_candidate_human_decision_recording_candidate_request',
    'validate_generator_candidate_human_decision_recording_candidate_contract',
]

from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_recording_candidate_constants import (
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_FEATURE_ID,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_SCHEMA_VERSION,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_STATUS,
    REQUIRED_FIELDS,
    REQUIRED_SCOPE,
    ALLOWED_CURRENT_STATES,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_FUTURE_CANDIDATE_EVIDENCE,
    ALLOWED_FUTURE_RECORDING_CANDIDATE_ACTIONS,
    REQUIRED_ALLOWED_CANDIDATE_OUTPUTS,
    REQUIRED_PROHIBITED_CANDIDATE_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    FORBIDDEN_FIELDS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_CANDIDATE_EFFECT_POLICY,
    REQUIRED_STOP_CONDITIONS,
    TRIGGER_TERMS_REQUIRING_FUTURE_PATCH,
    SCHEMA_TALK_TERMS,
)


def _sorted(values: Sequence[str] | set[str] | frozenset[str]) -> list[str]:
    return sorted(values)


def _false_flags() -> dict[str, bool]:
    return {flag: False for flag in _sorted(REQUIRED_DISABLED_FLAGS_FALSE)}


def build_generator_candidate_human_decision_recording_candidate_contract() -> dict[str, Any]:
    """Return the inert decision-recording candidate schema."""
    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_STATUS,
        "declared_generator_candidate_human_decision_recording_candidate_schema_only": True,
        "human_decision_recording_candidate_scope": REQUIRED_SCOPE,
        "current_human_decision_recording_candidate_state": "decision_recording_candidate_not_created",
        "current_human_decision_recording_candidate_effect": "no_effect_schema_only_not_created_not_recorded",
        "current_recorded_decision_value": "not_recorded",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "required_future_candidate_evidence": _sorted(REQUIRED_FUTURE_CANDIDATE_EVIDENCE),
        "allowed_future_recording_candidate_actions": _sorted(ALLOWED_FUTURE_RECORDING_CANDIDATE_ACTIONS),
        "allowed_candidate_outputs": _sorted(REQUIRED_ALLOWED_CANDIDATE_OUTPUTS),
        "prohibited_candidate_outputs": _sorted(REQUIRED_PROHIBITED_CANDIDATE_OUTPUTS),
        "disabled_flags": _false_flags(),
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "candidate_effect_policy": _sorted(REQUIRED_CANDIDATE_EFFECT_POLICY),
        "stop_conditions": _sorted(REQUIRED_STOP_CONDITIONS),
    }


def validate_generator_candidate_human_decision_recording_candidate_contract(
    candidate: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the inert recording-candidate schema and return denial facts."""
    errors: list[str] = []

    missing = REQUIRED_FIELDS.difference(candidate)
    if missing:
        errors.append("missing required human decision recording candidate fields: " + ", ".join(sorted(missing)))

    forbidden = FORBIDDEN_FIELDS.intersection(candidate)
    if forbidden:
        errors.append("forbidden candidate field present: " + ", ".join(sorted(forbidden)))

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_CANDIDATE_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_human_decision_recording_candidate_schema_only") is not True:
        errors.append("schema-only declaration must be true")
    if candidate.get("human_decision_recording_candidate_scope") != REQUIRED_SCOPE:
        errors.append("human_decision_recording_candidate_scope mismatch")
    if candidate.get("current_human_decision_recording_candidate_state") not in ALLOWED_CURRENT_STATES:
        errors.append("current human decision recording candidate state is not allowed")
    if candidate.get("current_human_decision_recording_candidate_state") != "decision_recording_candidate_not_created":
        errors.append("current human decision recording candidate state must remain decision_recording_candidate_not_created")
    if candidate.get("current_human_decision_recording_candidate_effect") != "no_effect_schema_only_not_created_not_recorded":
        errors.append("current human decision recording candidate effect must remain no_effect_schema_only_not_created_not_recorded")
    if candidate.get("current_recorded_decision_value") != "not_recorded":
        errors.append("current recorded decision value must remain not_recorded")

    set_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_future_candidate_evidence", REQUIRED_FUTURE_CANDIDATE_EVIDENCE),
        ("allowed_future_recording_candidate_actions", ALLOWED_FUTURE_RECORDING_CANDIDATE_ACTIONS),
        ("allowed_candidate_outputs", REQUIRED_ALLOWED_CANDIDATE_OUTPUTS),
        ("prohibited_candidate_outputs", REQUIRED_PROHIBITED_CANDIDATE_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("candidate_effect_policy", REQUIRED_CANDIDATE_EFFECT_POLICY),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
    ]
    for key, required in set_checks:
        values = candidate.get(key, [])
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            errors.append(f"{key} must be a sequence")
            continue
        if not required.issubset(set(values)):
            errors.append(f"{key} missing required values")

    flags = candidate.get("disabled_flags", {})
    if not isinstance(flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        flags = {}
    else:
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            if flag not in flags:
                errors.append(f"disabled flag missing: {flag}")
            elif flags[flag] is not False:
                errors.append(f"disabled flag must be false: {flag}")

    return {
        "ok": not errors,
        "errors": errors,
        "schema_id": candidate.get("schema_id"),
        "schema_version": candidate.get("schema_version"),
        "current_human_decision_recording_candidate_state": candidate.get("current_human_decision_recording_candidate_state"),
        "current_recorded_decision_value": candidate.get("current_recorded_decision_value"),
        "real_human_decision_recorded_by_human_decision_recording_candidate": flags.get("real_human_decision_recording_enabled", True),
        "human_decision_write_performed": flags.get("human_decision_write_enabled", True),
        "human_decision_recording_candidate_created": flags.get("human_decision_recording_candidate_creation_enabled", True),
        "human_approval_inferred_from_preparation_chain": flags.get("human_approval_inference_enabled", True),
        "candidate_patch_approval_recorded": flags.get("candidate_patch_approval_enabled", True),
        "dependency_install_authorized": flags.get("dependency_install_enabled", True),
        "side_effect_authorized": flags.get("side_effect_authorization_enabled", True),
        "generator_candidate_patch_created": flags.get("generator_candidate_patch_creation_enabled", True),
        "generator_candidate_patch_authorized": flags.get("generator_candidate_patch_authorization_enabled", True),
        "generator_implementation_authorized": flags.get("generator_implementation_enabled", True),
        "artifact_generation_authorized": flags.get("artifact_generation_enabled", True),
        "artifact_writing_authorized": flags.get("artifact_writing_enabled", True),
        "artifact_reading_authorized": flags.get("artifact_reading_enabled", True),
        "source_scanning_authorized": flags.get("source_scanning_enabled", True),
        "raw_text_materialization_authorized": flags.get("raw_text_materialization_enabled", True),
        "embedding_generation_authorized": flags.get("embedding_generation_enabled", True),
        "vector_index_generation_authorized": flags.get("vector_index_writing_enabled", True),
        "provider_execution_authorized": flags.get("provider_execution_enabled", True),
        "semantic_runtime_authorized": flags.get("semantic_runtime_scoring_enabled", True),
        "router_authority_authorized": flags.get("router_authority_enabled", True),
        "requires_prior_generator_candidate_human_decision_recording_boundary": True,
        "requires_explicit_human_confirmation_to_prepare_recording_candidate": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }


def classify_generator_candidate_human_decision_recording_candidate_request(user_text: str) -> dict[str, Any]:
    """Classify a request against the schema-only decision-recording candidate boundary."""
    normalized = " ".join(str(user_text).lower().split())
    has_trigger = any(term in normalized for term in TRIGGER_TERMS_REQUIRING_FUTURE_PATCH)
    has_schema_talk = any(term in normalized for term in SCHEMA_TALK_TERMS)

    base = {
        "current_recorded_decision_value": "not_recorded",
        "real_human_decision_recorded_by_human_decision_recording_candidate": False,
        "human_decision_write_performed": False,
        "human_decision_recording_candidate_created": False,
        "human_approval_inferred_from_preparation_chain": False,
        "candidate_patch_approval_recorded": False,
        "dependency_install_authorized": False,
        "side_effect_authorized": False,
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
        "requires_prior_generator_candidate_human_decision_recording_boundary": True,
        "requires_explicit_human_confirmation_to_prepare_recording_candidate": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }

    if has_trigger:
        return {
            **base,
            "allowed_now": False,
            "permitted_output": "none",
            "reason": "request would record or write a decision, create a candidate patch, or enable generation/runtime behavior",
        }

    return {
        **base,
        "allowed_now": bool(has_schema_talk),
        "permitted_output": "human_decision_recording_candidate_schema" if has_schema_talk else "none",
        "reason": "schema-only discussion is allowed; decision recording and generation remain disabled",
    }
