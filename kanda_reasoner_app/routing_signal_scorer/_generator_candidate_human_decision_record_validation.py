# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_human_decision_record_validation.py
"""Validation for generator candidate human decision record contracts."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_record_constants import (
    ALLOWED_CURRENT_HUMAN_DECISION_RECORD_STATES,
    ALLOWED_FUTURE_RECORDED_DECISION_VALUES,
    FORBIDDEN_RECORD_FIELDS,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS,
    REQUIRED_ALLOWED_RECORD_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_FUTURE_RECORDING_INPUTS,
    REQUIRED_HUMAN_DECISION_RECORD_FIELDS,
    REQUIRED_HUMAN_DECISION_RECORD_SCOPE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_RECORD_OUTPUTS,
    REQUIRED_RECORD_EFFECT_POLICY,
    REQUIRED_STOP_CONDITIONS,
)

__all__: list[str] = []


def validate_generator_candidate_human_decision_record_contract(
    record: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the inert record schema and return denial-oriented facts."""
    errors: list[str] = []

    missing = REQUIRED_HUMAN_DECISION_RECORD_FIELDS.difference(record)
    if missing:
        errors.append("missing required human decision record fields: " + ", ".join(sorted(missing)))

    forbidden = FORBIDDEN_RECORD_FIELDS.intersection(record)
    if forbidden:
        errors.append("forbidden record field present: " + ", ".join(sorted(forbidden)))

    if record.get("schema_id") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID:
        errors.append("schema_id mismatch")
    if record.get("schema_version") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if record.get("schema_status") != GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS:
        errors.append("schema_status mismatch")
    if record.get("declared_generator_candidate_human_decision_record_schema_only") is not True:
        errors.append("schema-only declaration must be true")
    if record.get("human_decision_record_scope") != REQUIRED_HUMAN_DECISION_RECORD_SCOPE:
        errors.append("human_decision_record_scope mismatch")
    if record.get("current_human_decision_record_state") not in ALLOWED_CURRENT_HUMAN_DECISION_RECORD_STATES:
        errors.append("current human decision record state is not allowed")
    if record.get("current_human_decision_record_state") != "human_decision_record_not_recorded":
        errors.append("current human decision record state must remain human_decision_record_not_recorded")
    if record.get("current_human_decision_record_effect") != "no_effect_schema_only_not_recorded":
        errors.append("current human decision record effect must remain no_effect_schema_only_not_recorded")
    if record.get("current_recorded_decision_value") != "not_recorded":
        errors.append("current recorded decision value must remain not_recorded")

    set_checks = [
        ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
        ("required_future_recording_inputs", REQUIRED_FUTURE_RECORDING_INPUTS),
        ("allowed_future_recorded_decision_values", ALLOWED_FUTURE_RECORDED_DECISION_VALUES),
        ("allowed_record_outputs", REQUIRED_ALLOWED_RECORD_OUTPUTS),
        ("prohibited_record_outputs", REQUIRED_PROHIBITED_RECORD_OUTPUTS),
        ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
        ("record_effect_policy", REQUIRED_RECORD_EFFECT_POLICY),
        ("stop_conditions", REQUIRED_STOP_CONDITIONS),
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
        "schema_id": record.get("schema_id"),
        "schema_version": record.get("schema_version"),
        "current_human_decision_record_state": record.get("current_human_decision_record_state"),
        "current_recorded_decision_value": record.get("current_recorded_decision_value"),
        "real_human_decision_recorded_by_human_decision_record": flags.get("real_human_decision_recording_enabled", True),
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
        "requires_prior_generator_candidate_human_decision_gate": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }
