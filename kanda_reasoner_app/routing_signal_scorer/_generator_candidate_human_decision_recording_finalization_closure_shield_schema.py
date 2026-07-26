# project-path: kanda_reasoner_app/routing_signal_scorer/_generator_candidate_human_decision_recording_finalization_closure_shield_schema.py
"""Inert contract builder for generator candidate finalization closure shields."""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from kanda_reasoner_app.routing_signal_scorer._generator_candidate_human_decision_recording_finalization_closure_shield_constants import (
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_FEATURE_ID,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_SCHEMA_VERSION,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_STATUS,
    REQUIRED_SCOPE,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_FUTURE_CLOSURE_EVIDENCE,
    ALLOWED_FUTURE_CLOSURE_ACTIONS,
    REQUIRED_ALLOWED_CLOSURE_OUTPUTS,
    REQUIRED_PROHIBITED_CLOSURE_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_CLOSURE_EFFECT_POLICY,
    REQUIRED_STOP_CONDITIONS,
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


def build_generator_candidate_human_decision_recording_finalization_closure_shield_contract() -> dict[str, Any]:
    """Return the inert decision-recording finalization closure shield schema."""
    return {
        "schema_id": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_FEATURE_ID,
        "schema_version": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_SCHEMA_VERSION,
        "schema_status": GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_CLOSURE_SHIELD_STATUS,
        "declared_generator_candidate_human_decision_recording_finalization_closure_shield_schema_only": True,
        "human_decision_recording_finalization_closure_shield_scope": REQUIRED_SCOPE,
        "current_human_decision_recording_finalization_closure_shield_state": "decision_recording_finalization_closure_shield_closed",
        "current_human_decision_recording_finalization_closure_shield_effect": "no_effect_schema_only_closure_shield_closed_not_recorded",
        "current_recorded_decision_value": "not_recorded",
        "required_prior_milestones": _sorted(REQUIRED_PRIOR_MILESTONES),
        "required_future_closure_evidence": _sorted(REQUIRED_FUTURE_CLOSURE_EVIDENCE),
        "allowed_future_closure_actions": _sorted(ALLOWED_FUTURE_CLOSURE_ACTIONS),
        "allowed_closure_outputs": _sorted(REQUIRED_ALLOWED_CLOSURE_OUTPUTS),
        "prohibited_closure_outputs": _sorted(REQUIRED_PROHIBITED_CLOSURE_OUTPUTS),
        "disabled_flags": _false_flags(),
        "no_authority_assertions": _sorted(REQUIRED_NO_AUTHORITY_ASSERTIONS),
        "closure_effect_policy": _sorted(REQUIRED_CLOSURE_EFFECT_POLICY),
        "stop_conditions": _sorted(REQUIRED_STOP_CONDITIONS),
    }


