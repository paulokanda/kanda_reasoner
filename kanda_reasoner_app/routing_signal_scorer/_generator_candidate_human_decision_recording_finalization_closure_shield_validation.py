# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_human_decision_recording_finalization_closure_shield_validation.py
"""Validation for generator candidate finalization closure shield contracts."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_recording_finalization_closure_shield_constants import (
    ALLOWED_CURRENT_STATES,
    ALLOWED_FUTURE_CLOSURE_ACTIONS,
    FORBIDDEN_FIELDS,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_FEATURE_ID,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_SCHEMA_VERSION,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_STATUS,
    REQUIRED_ALLOWED_CLOSURE_OUTPUTS,
    REQUIRED_CLOSURE_EFFECT_POLICY,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_FIELDS,
    REQUIRED_FUTURE_CLOSURE_EVIDENCE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_CLOSURE_OUTPUTS,
    REQUIRED_SCOPE,
    REQUIRED_STOP_CONDITIONS,
    SCHEMA_TALK_TERMS,
    TRIGGER_TERMS_REQUIRING_FUTURE_PATCH,
)
from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_recording_finalization_closure_shield_schema import (
    build_generator_candidate_human_decision_recording_finalization_closure_shield_contract,
)

__all__: list[str] = []


def validate_generator_candidate_human_decision_recording_finalization_closure_shield_contract(
    candidate: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the inert finalization-closure-shield schema and return denial facts."""
    errors: list[str] = []

    missing = REQUIRED_FIELDS.difference(candidate)
    if missing:
        errors.append("missing required human decision recording finalization closure shield fields: " + ", ".join(sorted(missing)))

    forbidden = FORBIDDEN_FIELDS.intersection(candidate)
    if forbidden:
        errors.append("forbidden closure shield field present: " + ", ".join(sorted(forbidden)))

    if candidate.get("schema_id") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_FEATURE_ID:
        errors.append("schema_id mismatch")
    if candidate.get("schema_version") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if candidate.get("schema_status") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_STATUS:
        errors.append("schema_status mismatch")
    if candidate.get("declared_generator_candidate_human_decision_recording_finalization_closure_shield_schema_only") is not True:
        errors.append("schema-only declaration must be true")
    if candidate.get("human_decision_recording_finalization_closure_shield_scope") != REQUIRED_SCOPE:
        errors.append("human_decision_recording_finalization_closure_shield_scope mismatch")
    if candidate.get("current_human_decision_recording_finalization_closure_shield_state") not in ALLOWED_CURRENT_STATES:
        errors.append("current human decision recording finalization closure shield state is not allowed")
    if candidate.get("current_human_decision_recording_finalization_closure_shield_state") != "decision_recording_finalization_closure_shield_closed":
        errors.append("current human decision recording finalization closure shield state must remain closed")
    if candidate.get("current_human_decision_recording_finalization_closure_shield_effect") != "no_effect_schema_only_closure_shield_closed_not_recorded":
        errors.append("current human decision recording finalization closure shield effect must remain inert")
    if candidate.get("current_recorded_decision_value") != "not_recorded":
        errors.append("current recorded decision value must remain not_recorded")

    set_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_future_closure_evidence", REQUIRED_FUTURE_CLOSURE_EVIDENCE),
        ("allowed_future_closure_actions", ALLOWED_FUTURE_CLOSURE_ACTIONS),
        ("allowed_closure_outputs", REQUIRED_ALLOWED_CLOSURE_OUTPUTS),
        ("prohibited_closure_outputs", REQUIRED_PROHIBITED_CLOSURE_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("closure_effect_policy", REQUIRED_CLOSURE_EFFECT_POLICY),
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
        "current_human_decision_recording_finalization_closure_shield_state": candidate.get("current_human_decision_recording_finalization_closure_shield_state"),
        "current_recorded_decision_value": candidate.get("current_recorded_decision_value"),
        "real_human_decision_recorded_by_human_decision_recording_finalization_closure_shield": flags.get("real_human_decision_recording_enabled", True),
        "human_decision_write_performed": flags.get("human_decision_write_enabled", True),
        "human_decision_commit_performed": flags.get("human_decision_commit_enabled", True),
        "human_decision_finalization_performed": flags.get("human_decision_finalization_enabled", True),
        "human_decision_recording_patch_created": flags.get("human_decision_recording_patch_enabled", True),
        "human_decision_recording_write_function_enabled": flags.get("human_decision_recording_write_function_enabled", True),
        "human_approval_inferred_from_preparation_chain": flags.get("human_approval_inference_enabled", True),
        "candidate_patch_approval_recorded": flags.get("candidate_patch_approval_enabled", True),
        "dependency_install_authorized": flags.get("dependency_install_enabled", True),
        "side_effect_authorized": flags.get("side_effect_authorization_enabled", True),
        "generator_candidate_patch_created": flags.get("generator_candidate_patch_creation_enabled", True),
        "generator_candidate_patch_authorized": flags.get("generator_candidate_patch_authorization_enabled", True),
        "generator_commit_authorized": flags.get("generator_commit_enabled", True),
        "generator_implementation_authorized": flags.get("generator_commit_enabled", True),
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
        "requires_prior_generator_candidate_human_decision_recording_finalization": True,
        "requires_explicit_human_confirmation_to_open_future_decision_recording_patch": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
        "human_decision_recording_subchain_closed": not errors,
    }


def classify_generator_candidate_human_decision_recording_finalization_closure_shield_request(user_text: str) -> dict[str, Any]:
    """Classify requests without granting decision-recording or generation authority."""
    text = (user_text or "").lower()
    has_trigger = any(term in text for term in TRIGGER_TERMS_REQUIRING_FUTURE_PATCH)
    has_schema_talk = any(term in text for term in SCHEMA_TALK_TERMS)

    base = validate_generator_candidate_human_decision_recording_finalization_closure_shield_contract(
        build_generator_candidate_human_decision_recording_finalization_closure_shield_contract()
    )
    if has_trigger:
        return {
            **base,
            "allowed_now": False,
            "permitted_output": "none",
            "reason": "request would require a separate governed decision-recording, candidate-patch, or generation patch",
        }

    return {
        **base,
        "allowed_now": bool(has_schema_talk),
        "permitted_output": "human_decision_recording_finalization_closure_shield_schema" if has_schema_talk else "none",
        "reason": "schema-only closure-shield discussion is allowed; decision recording and generation remain disabled",
    }
