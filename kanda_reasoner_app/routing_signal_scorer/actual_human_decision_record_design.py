# project-path: kanda_reasoner_app/routing_signal_scorer/actual_human_decision_record_design.py
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

__all__ = [
    'build_actual_human_decision_record_contract',
    'classify_actual_human_decision_record_request',
    'validate_actual_human_decision_record_contract',
]

from kanda_reasoner_app.routing_signal_scorer._actual_human_decision_record_constants import (
    ACTUAL_HUMAN_DECISION_RECORD_FEATURE_ID,
    ACTUAL_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
    REQUIRED_RECORD_FIELDS,
    REQUIRED_RECORD_SCOPE,
    ALLOWED_RECORD_STATUSES,
    ALLOWED_FUTURE_RECORDED_DECISION_VALUES,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_HUMAN_ATTESTATION_SECTIONS,
    REQUIRED_WRITTEN_EVIDENCE_BEFORE_RECORDING_REAL_DECISION,
    REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE,
    REQUIRED_ALLOWED_RECORD_OUTPUTS,
    REQUIRED_PROHIBITED_RECORD_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_RECORD_EFFECT_POLICY,
    REQUIRED_ESCALATION_RULES,
    FORBIDDEN_RECORD_FIELDS,
    TRIGGER_TERMS_REQUIRING_FUTURE_PATCH,
    SCHEMA_TALK_TERMS,
)


def _sorted(values: Sequence[str] | set[str] | frozenset[str]) -> list[str]:
    """Support sorted behavior.
    
    Parameters
    ----------
    values : Sequence[str] | set[str] | frozenset[str]
        The input values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
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
