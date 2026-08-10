# project-path: kanda_reasoner_app/engineering_diagnostics/lifecycle_models.py
"""Immutable lifecycle-governance contracts for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

__all__ = [
    "DIAGNOSTIC_LIFECYCLE_SCHEMA_VERSION",
    "LIFECYCLE_ACTIONS",
    "LIFECYCLE_STATES",
    "LIFECYCLE_TARGET_KINDS",
    "DiagnosticLifecycleDecisionRecord",
    "DiagnosticLifecycleHead",
    "DiagnosticLifecycleState",
    "DiagnosticLifecycleTarget",
]

DIAGNOSTIC_LIFECYCLE_SCHEMA_VERSION = "1.0"
LIFECYCLE_TARGET_KINDS = frozenset({"ISSUE", "GROUP"})
LIFECYCLE_STATES = frozenset(
    {
        "OPEN",
        "INVESTIGATING",
        "CONFIRMED",
        "FIX_PLANNED",
        "PATCH_PREPARED",
        "VALIDATING",
        "RESOLUTION_CANDIDATE",
        "RESOLVED",
        "ACCEPTED_RISK",
        "FALSE_POSITIVE",
        "SUPPRESSED",
        "DEFERRED",
        "REOPENED",
    }
)
LIFECYCLE_ACTIONS = frozenset(
    {
        "START_INVESTIGATION",
        "CONFIRM",
        "PLAN_FIX",
        "MARK_PATCH_PREPARED",
        "START_VALIDATION",
        "MARK_RESOLUTION_CANDIDATE",
        "MARK_RESOLVED",
        "ACCEPT_RISK",
        "MARK_FALSE_POSITIVE",
        "SUPPRESS",
        "DEFER",
        "REOPEN",
    }
)


def _required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(field_name + " is required.")
    return text


def _optional_text(value: object) -> str:
    return str(value or "").strip()


def _choice(value: object, allowed: frozenset[str], field_name: str) -> str:
    text = _required_text(value, field_name).upper()
    if text not in allowed:
        raise ValueError("Unsupported " + field_name + ": " + text)
    return text


def _unique_text(values: Iterable[object]) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        text = _optional_text(value)
        if text and text not in result:
            result.append(text)
    return tuple(sorted(result))


@dataclass(frozen=True, slots=True)
class DiagnosticLifecycleTarget:
    """One current issue or diagnostic group eligible for human governance."""

    target_kind: str
    target_id: str
    label: str
    member_issue_fingerprints: tuple[str, ...]

    def __post_init__(self) -> None:
        kind = _choice(self.target_kind, LIFECYCLE_TARGET_KINDS, "target kind")
        target_id = _required_text(self.target_id, "target_id")
        label = _required_text(self.label, "target label")
        members = _unique_text(self.member_issue_fingerprints)
        if not members:
            raise ValueError("Lifecycle target requires current issue members.")
        if kind == "ISSUE" and members != (target_id,):
            raise ValueError("Issue lifecycle target must contain only its target_id.")
        object.__setattr__(self, "target_kind", kind)
        object.__setattr__(self, "target_id", target_id)
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "member_issue_fingerprints", members)


@dataclass(frozen=True, slots=True)
class DiagnosticLifecycleHead:
    """Current lifecycle state for one stable issue or group identity."""

    project_id: str
    producer_id: str
    scope_fingerprint: str
    target_kind: str
    target_id: str
    target_label: str
    current_state: str
    generation: int
    last_decision_id: str = ""
    updated_at_utc: str = ""
    last_run_id: str = ""
    member_digest: str = ""

    def __post_init__(self) -> None:
        for field_name in (
            "project_id",
            "producer_id",
            "scope_fingerprint",
            "target_id",
            "target_label",
        ):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        object.__setattr__(
            self,
            "target_kind",
            _choice(self.target_kind, LIFECYCLE_TARGET_KINDS, "target kind"),
        )
        object.__setattr__(
            self,
            "current_state",
            _choice(self.current_state, LIFECYCLE_STATES, "lifecycle state"),
        )
        generation = int(self.generation)
        if generation < 0:
            raise ValueError("lifecycle generation cannot be negative.")
        object.__setattr__(self, "generation", generation)
        for field_name in (
            "last_decision_id",
            "updated_at_utc",
            "last_run_id",
            "member_digest",
        ):
            object.__setattr__(
                self,
                field_name,
                _optional_text(getattr(self, field_name)),
            )


@dataclass(frozen=True, slots=True)
class DiagnosticLifecycleDecisionRecord:
    """Append-only human lifecycle decision."""

    decision_id: str
    project_id: str
    producer_id: str
    scope_fingerprint: str
    run_id: str
    target_kind: str
    target_id: str
    target_label: str
    member_issue_fingerprints: tuple[str, ...]
    action: str
    previous_state: str
    resulting_state: str
    reason_code: str
    rationale: str
    author: str
    decided_at_utc: str
    expires_at_utc: str
    revisit_condition: str
    related_ticket: str
    related_wave: str
    explicit_confirmation: bool
    resulting_generation: int

    def __post_init__(self) -> None:
        for field_name in (
            "decision_id",
            "project_id",
            "producer_id",
            "scope_fingerprint",
            "run_id",
            "target_id",
            "target_label",
            "reason_code",
            "rationale",
            "author",
            "decided_at_utc",
        ):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        object.__setattr__(
            self,
            "target_kind",
            _choice(self.target_kind, LIFECYCLE_TARGET_KINDS, "target kind"),
        )
        object.__setattr__(
            self,
            "action",
            _choice(self.action, LIFECYCLE_ACTIONS, "lifecycle action"),
        )
        object.__setattr__(
            self,
            "previous_state",
            _choice(self.previous_state, LIFECYCLE_STATES, "previous state"),
        )
        object.__setattr__(
            self,
            "resulting_state",
            _choice(self.resulting_state, LIFECYCLE_STATES, "resulting state"),
        )
        members = _unique_text(self.member_issue_fingerprints)
        if not members:
            raise ValueError("Lifecycle decision requires current issue members.")
        object.__setattr__(self, "member_issue_fingerprints", members)
        for field_name in (
            "expires_at_utc",
            "revisit_condition",
            "related_ticket",
            "related_wave",
        ):
            object.__setattr__(
                self,
                field_name,
                _optional_text(getattr(self, field_name)),
            )
        if not self.expires_at_utc and not self.revisit_condition:
            raise ValueError("Lifecycle decision requires expiration or revisit condition.")
        generation = int(self.resulting_generation)
        if generation < 1:
            raise ValueError("resulting_generation must be positive.")
        object.__setattr__(self, "resulting_generation", generation)
        object.__setattr__(
            self,
            "explicit_confirmation",
            bool(self.explicit_confirmation),
        )


@dataclass(frozen=True, slots=True)
class DiagnosticLifecycleState:
    """Current lifecycle heads plus searchable append-only history."""

    project_id: str
    producer_id: str
    scope_fingerprint: str
    heads: tuple[DiagnosticLifecycleHead, ...] = ()
    decisions: tuple[DiagnosticLifecycleDecisionRecord, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("project_id", "producer_id", "scope_fingerprint"):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        object.__setattr__(self, "heads", tuple(self.heads))
        object.__setattr__(self, "decisions", tuple(self.decisions))
