# project-path: kanda_reasoner_app/engineering_diagnostics/lifecycle.py
"""Deterministic lifecycle transition rules for human diagnostic governance."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from .lifecycle_models import LIFECYCLE_ACTIONS, LIFECYCLE_STATES
from .models import DiagnosticStateError

__all__ = [
    "LIFECYCLE_ACTION_RESULT",
    "allowed_lifecycle_actions",
    "validate_lifecycle_transition",
]

LIFECYCLE_ACTION_RESULT: Mapping[str, str] = MappingProxyType(
    {
        "START_INVESTIGATION": "INVESTIGATING",
        "CONFIRM": "CONFIRMED",
        "PLAN_FIX": "FIX_PLANNED",
        "MARK_PATCH_PREPARED": "PATCH_PREPARED",
        "START_VALIDATION": "VALIDATING",
        "MARK_RESOLUTION_CANDIDATE": "RESOLUTION_CANDIDATE",
        "MARK_RESOLVED": "RESOLVED",
        "ACCEPT_RISK": "ACCEPTED_RISK",
        "MARK_FALSE_POSITIVE": "FALSE_POSITIVE",
        "SUPPRESS": "SUPPRESSED",
        "DEFER": "DEFERRED",
        "REOPEN": "REOPENED",
    }
)

_ALLOWED = {
    "OPEN": {
        "START_INVESTIGATION",
        "CONFIRM",
        "ACCEPT_RISK",
        "MARK_FALSE_POSITIVE",
        "SUPPRESS",
        "DEFER",
    },
    "INVESTIGATING": {
        "CONFIRM",
        "PLAN_FIX",
        "ACCEPT_RISK",
        "MARK_FALSE_POSITIVE",
        "SUPPRESS",
        "DEFER",
    },
    "CONFIRMED": {
        "PLAN_FIX",
        "ACCEPT_RISK",
        "SUPPRESS",
        "DEFER",
    },
    "FIX_PLANNED": {
        "MARK_PATCH_PREPARED",
        "ACCEPT_RISK",
        "DEFER",
    },
    "PATCH_PREPARED": {"START_VALIDATION", "DEFER"},
    "VALIDATING": {
        "MARK_RESOLUTION_CANDIDATE",
        "CONFIRM",
        "PLAN_FIX",
    },
    "RESOLUTION_CANDIDATE": {"MARK_RESOLVED", "REOPEN"},
    "RESOLVED": {"REOPEN"},
    "ACCEPTED_RISK": {"REOPEN"},
    "FALSE_POSITIVE": {"REOPEN"},
    "SUPPRESSED": {"REOPEN"},
    "DEFERRED": {"REOPEN"},
    "REOPENED": {
        "START_INVESTIGATION",
        "CONFIRM",
        "PLAN_FIX",
        "ACCEPT_RISK",
        "MARK_FALSE_POSITIVE",
        "SUPPRESS",
        "DEFER",
    },
}


def allowed_lifecycle_actions(current_state: str) -> tuple[str, ...]:
    """Return deterministic available actions for one current state."""
    state = str(current_state or "").strip().upper()
    if state not in LIFECYCLE_STATES:
        raise DiagnosticStateError("LIFECYCLE_STATE_UNSUPPORTED:" + state)
    return tuple(sorted(_ALLOWED[state]))


def validate_lifecycle_transition(current_state: str, action: str) -> str:
    """Validate one state transition and return its deterministic result."""
    state = str(current_state or "").strip().upper()
    normalized_action = str(action or "").strip().upper()
    if state not in LIFECYCLE_STATES:
        raise DiagnosticStateError("LIFECYCLE_STATE_UNSUPPORTED:" + state)
    if normalized_action not in LIFECYCLE_ACTIONS:
        raise DiagnosticStateError(
            "LIFECYCLE_ACTION_UNSUPPORTED:" + normalized_action
        )
    if normalized_action not in _ALLOWED[state]:
        raise DiagnosticStateError(
            "LIFECYCLE_TRANSITION_NOT_ALLOWED:"
            + state
            + "->"
            + normalized_action
        )
    return LIFECYCLE_ACTION_RESULT[normalized_action]
