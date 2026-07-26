# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_human_decision_record_schema.py
"""Inert contract builder for generator candidate human decision records."""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_record_constants import (
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS,
    REQUIRED_HUMAN_DECISION_RECORD_SCOPE,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_FUTURE_RECORDING_INPUTS,
    ALLOWED_FUTURE_RECORDED_DECISION_VALUES,
    REQUIRED_ALLOWED_RECORD_OUTPUTS,
    REQUIRED_PROHIBITED_RECORD_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_RECORD_EFFECT_POLICY,
    REQUIRED_STOP_CONDITIONS,
    TRIGGER_TERMS_REQUIRING_FUTURE_PATCH,
    SCHEMA_TALK_TERMS,
)

__all__: list[str] = []


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


def _false_flags() -> dict[str, bool]:
    """Support false flags behavior.
    
    Returns
    -------
    dict[str, bool]
        The mapped values.
    """
    
    return {flag: False for flag in _sorted(REQUIRED_DISABLED_FLAGS_FALSE)}


def build_generator_candidate_human_decision_record_contract() -> dict[str, Any]:
    """Return the inert human decision record schema after the gate."""
    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_STATUS,
        "declared_generator_candidate_human_decision_record_schema_only": True,
        "human_decision_record_scope": REQUIRED_HUMAN_DECISION_RECORD_SCOPE,
        "current_human_decision_record_state": "human_decision_record_not_recorded",
        "current_human_decision_record_effect": "no_effect_schema_only_not_recorded",
        "current_recorded_decision_value": "not_recorded",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "required_future_recording_inputs": _sorted(REQUIRED_FUTURE_RECORDING_INPUTS),
        "allowed_future_recorded_decision_values": _sorted(ALLOWED_FUTURE_RECORDED_DECISION_VALUES),
        "allowed_record_outputs": _sorted(REQUIRED_ALLOWED_RECORD_OUTPUTS),
        "prohibited_record_outputs": _sorted(REQUIRED_PROHIBITED_RECORD_OUTPUTS),
        "disabled_flags": _false_flags(),
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "record_effect_policy": _sorted(REQUIRED_RECORD_EFFECT_POLICY),
        "stop_conditions": _sorted(REQUIRED_STOP_CONDITIONS),
    }


def classify_generator_candidate_human_decision_record_request(user_text: str) -> dict[str, Any]:
    """Classify a request against the schema-only human decision record boundary."""
    normalized = " ".join(str(user_text).lower().split())
    has_trigger = any(term in normalized for term in TRIGGER_TERMS_REQUIRING_FUTURE_PATCH)
    has_schema_talk = any(term in normalized for term in SCHEMA_TALK_TERMS)

    base = {
        "current_recorded_decision_value": "not_recorded",
        "real_human_decision_recorded_by_human_decision_record": False,
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
        "requires_prior_generator_candidate_human_decision_gate": True,
        "requires_future_governed_decision_recording_patch": True,
        "requires_future_governed_candidate_patch": True,
        "requires_future_governed_generation_patch": True,
    }

    if has_trigger:
        return {
            **base,
            "allowed_now": False,
            "permitted_output": "none",
            "reason": "request would record approval, create a candidate patch, or enable generation/runtime behavior",
        }

    return {
        **base,
        "allowed_now": bool(has_schema_talk),
        "permitted_output": "human_decision_record_schema" if has_schema_talk else "none",
        "reason": "schema-only discussion is allowed; decision recording and generation remain disabled",
    }

