# project-path: kanda_reasoner_app/routing_signal_scorer/human_decision_intake_design.py
"""Human decision intake design for routing scorer v3.

This module is intentionally standard-library-only and intake-schema-only. It
records no real human decision, authorizes no generator candidate, generates no
artifact, writes no artifact, reads no artifact, scans no sources, materializes
no raw text, generates no embeddings, materializes no vectors, instantiates no
providers, runs no semantic scoring, modifies no router authority, loads no
prompts, writes no freeze memory, and changes no runtime behavior. It defines a
static schema for how a future human decision could be represented only after a
separate governed process.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

__all__ = [
    'build_human_decision_intake_contract',
    'classify_human_decision_intake_request',
    'validate_human_decision_intake_contract',
]

from kanda_reasoner_app.routing_signal_scorer._human_decision_intake_constants import (
    HUMAN_DECISION_INTAKE_FEATURE_ID,
    HUMAN_DECISION_INTAKE_SCHEMA_VERSION,
    HUMAN_DECISION_INTAKE_STATUS,
    REQUIRED_INTAKE_FIELDS,
    REQUIRED_DECISION_SCOPE,
    ALLOWED_INTAKE_STATUSES,
    REQUIRED_PRIOR_MILESTONES,
    ALLOWED_FUTURE_DECISION_VALUES,
    REQUIRED_DECISION_CONTEXT_SECTIONS,
    REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE,
    REQUIRED_ALLOWED_INTAKE_OUTPUTS,
    REQUIRED_PROHIBITED_INTAKE_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_DECISION_EFFECT_POLICY,
    REQUIRED_ESCALATION_RULES,
    FORBIDDEN_INTAKE_FIELDS,
)


def _as_set(value: Any) -> set[str]:
    """Support as set behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    if isinstance(value, str):
        return {value}
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return {str(item) for item in value}
    return set()


def _flag_is_false(flags: Mapping[str, Any], name: str) -> bool:
    """Support flag is false behavior.
    
    Parameters
    ----------
    flags : Mapping[str, Any]
        The flags value.
    name : str
        The name value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return flags.get(name) is False


def build_human_decision_intake_contract() -> dict[str, Any]:
    """Return the static schema for human decision intake."""
    return {
        "intake_id": HUMAN_DECISION_INTAKE_FEATURE_ID,
        "schema_version": HUMAN_DECISION_INTAKE_SCHEMA_VERSION,
        "intake_status": "schema_only",
        "declared_human_decision_intake_only": True,
        "decision_scope": REQUIRED_DECISION_SCOPE,
        "decision_value": "not_recorded",
        "required_prior_milestones": sorted(REQUIRED_PRIOR_MILESTONES),
        "allowed_future_decision_values": sorted(ALLOWED_FUTURE_DECISION_VALUES),
        "required_decision_context_sections": sorted(REQUIRED_DECISION_CONTEXT_SECTIONS),
        "required_written_evidence_before_any_future_candidate": sorted(
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE
        ),
        "allowed_intake_outputs": sorted(REQUIRED_ALLOWED_INTAKE_OUTPUTS),
        "prohibited_intake_outputs": sorted(REQUIRED_PROHIBITED_INTAKE_OUTPUTS),
        "disabled_flags": {
            name: False for name in sorted(REQUIRED_DISABLED_FLAGS_FALSE)
        },
        "no_authority_assertions": sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "decision_effect_policy": sorted(REQUIRED_DECISION_EFFECT_POLICY),
        "escalation_rules": sorted(REQUIRED_ESCALATION_RULES),
    }


def validate_human_decision_intake_contract(
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate the decision-intake schema without recording a decision."""
    errors: list[str] = []

    if not isinstance(contract, Mapping):
        return {
            "ok": False,
            "errors": ["contract must be a mapping"],
            "real_human_decision_recorded": False,
            "generator_candidate_patch_authorized": False,
            "artifact_generation_authorized": False,
            "artifact_writing_authorized": False,
            "requires_future_governed_patch": True,
        }

    extra_forbidden = sorted(FORBIDDEN_INTAKE_FIELDS.intersection(contract.keys()))
    if extra_forbidden:
        errors.append("forbidden intake fields present: " + ", ".join(extra_forbidden))

    missing_fields = sorted(REQUIRED_INTAKE_FIELDS.difference(contract.keys()))
    if missing_fields:
        errors.append("missing required fields: " + ", ".join(missing_fields))

    if contract.get("intake_id") != HUMAN_DECISION_INTAKE_FEATURE_ID:
        errors.append("intake_id mismatch")
    if contract.get("schema_version") != HUMAN_DECISION_INTAKE_SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if contract.get("intake_status") not in ALLOWED_INTAKE_STATUSES:
        errors.append("intake_status is not allowed")
    if contract.get("declared_human_decision_intake_only") is not True:
        errors.append("declared_human_decision_intake_only must be true")
    if contract.get("decision_scope") != REQUIRED_DECISION_SCOPE:
        errors.append("decision_scope mismatch")
    if contract.get("decision_value") != "not_recorded":
        errors.append("decision_value must remain not_recorded in this schema-only milestone")

    prior = _as_set(contract.get("required_prior_milestones"))
    if not REQUIRED_PRIOR_MILESTONES.issubset(prior):
        errors.append("required prior milestones incomplete")

    values = _as_set(contract.get("allowed_future_decision_values"))
    if not ALLOWED_FUTURE_DECISION_VALUES.issubset(values):
        errors.append("allowed future decision values incomplete")

    sections = _as_set(contract.get("required_decision_context_sections"))
    if not REQUIRED_DECISION_CONTEXT_SECTIONS.issubset(sections):
        errors.append("required decision context sections incomplete")

    evidence = _as_set(contract.get("required_written_evidence_before_any_future_candidate"))
    if not REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE.issubset(evidence):
        errors.append("required evidence before future candidate incomplete")

    allowed_outputs = _as_set(contract.get("allowed_intake_outputs"))
    if not REQUIRED_ALLOWED_INTAKE_OUTPUTS.issubset(allowed_outputs):
        errors.append("allowed intake outputs incomplete")

    prohibited_outputs = _as_set(contract.get("prohibited_intake_outputs"))
    if not REQUIRED_PROHIBITED_INTAKE_OUTPUTS.issubset(prohibited_outputs):
        errors.append("prohibited intake outputs incomplete")

    flags = contract.get("disabled_flags")
    if not isinstance(flags, Mapping):
        errors.append("disabled_flags must be a mapping")
        flags = {}

    false_missing = sorted(
        name for name in REQUIRED_DISABLED_FLAGS_FALSE if not _flag_is_false(flags, name)
    )
    if false_missing:
        errors.append("required disabled flags must be false: " + ", ".join(false_missing))

    no_authority = _as_set(contract.get("no_authority_assertions"))
    if not REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(no_authority):
        errors.append("no-authority assertions incomplete")

    policy = _as_set(contract.get("decision_effect_policy"))
    if not REQUIRED_DECISION_EFFECT_POLICY.issubset(policy):
        errors.append("decision effect policy incomplete")

    escalation_rules = _as_set(contract.get("escalation_rules"))
    if not REQUIRED_ESCALATION_RULES.issubset(escalation_rules):
        errors.append("escalation rules incomplete")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "intake_id": contract.get("intake_id"),
        "schema_version": contract.get("schema_version"),
        "intake_status": contract.get("intake_status"),
        "decision_value": contract.get("decision_value"),
        "real_human_decision_recorded": False,
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
        "requires_future_governed_patch": True,
        "review_evidence_only": True,
    }


def classify_human_decision_intake_request(request_text: str) -> dict[str, Any]:
    """Classify decision-intake requests while denying activation/generation."""
    normalized = str(request_text or "").strip().lower()
    activation_terms = (
        "generate",
        "write artifact",
        "create artifact",
        "read artifact",
        "load artifact",
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
        "record decision now",
        "approve now",
        "authorize generator",
    )
    intake_terms = (
        "human decision",
        "decision intake",
        "decision schema",
        "decision questionnaire",
        "decision placeholder",
        "defer",
        "reject",
        "permit proposal",
    )
    denied = any(term in normalized for term in activation_terms)
    intake_like = any(term in normalized for term in intake_terms)

    if intake_like and not denied:
        return {
            "allowed_now": True,
            "permitted_output": "human_decision_intake_schema",
            "decision_value": "not_recorded",
            "review_evidence_only": True,
            "real_human_decision_recorded": False,
            "generator_candidate_patch_authorized": False,
            "artifact_generation_authorized": False,
            "artifact_writing_authorized": False,
            "artifact_reading_authorized": False,
            "embedding_generation_authorized": False,
            "vector_index_authorized": False,
            "provider_execution_authorized": False,
            "semantic_runtime_authorized": False,
            "authority_granted": False,
            "requires_future_governed_patch_for_decision_recording": True,
            "requires_future_governed_patch_for_generation": True,
        }

    return {
        "allowed_now": False,
        "permitted_output": "blocked_or_requires_governed_human_decision_process",
        "decision_value": "not_recorded",
        "review_evidence_only": True,
        "real_human_decision_recorded": False,
        "generator_candidate_patch_authorized": False,
        "artifact_generation_authorized": False,
        "artifact_writing_authorized": False,
        "artifact_reading_authorized": False,
        "embedding_generation_authorized": False,
        "vector_index_authorized": False,
        "provider_execution_authorized": False,
        "semantic_runtime_authorized": False,
        "authority_granted": False,
        "requires_future_governed_patch_for_decision_recording": True,
        "requires_future_governed_patch_for_generation": True,
    }
