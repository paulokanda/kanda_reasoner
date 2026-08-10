# project-path: kanda_reasoner_app/engineering_diagnostics/grouping_models.py
"""Immutable grouping contracts for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

__all__ = [
    "DIAGNOSTIC_GROUPING_SCHEMA_VERSION",
    "GROUP_CONFIDENCE_LEVELS",
    "GROUP_DECISION_ACTIONS",
    "GROUP_KINDS",
    "GROUP_REVIEW_STATES",
    "DiagnosticGroupDecisionRecord",
    "DiagnosticGroupRecord",
    "DiagnosticManualGroupingState",
]

DIAGNOSTIC_GROUPING_SCHEMA_VERSION = "1.0"
GROUP_CONFIDENCE_LEVELS = frozenset({"high", "medium"})
GROUP_KINDS = frozenset({"DETERMINISTIC", "MANUAL"})
GROUP_REVIEW_STATES = frozenset({"UNREVIEWED", "REVIEWED"})
GROUP_DECISION_ACTIONS = frozenset(
    {
        "CREATE_GROUP",
        "ASSIGN_ISSUE",
        "UNGROUP_ISSUE",
        "MARK_REVIEWED",
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


def _confidence(value: object) -> str:
    text = _required_text(value, "group confidence").lower()
    if text not in GROUP_CONFIDENCE_LEVELS:
        raise ValueError("Unsupported group confidence: " + text)
    return text


def _tuple_text(values: object) -> tuple[str, ...]:
    if values is None:
        return ()
    result: list[str] = []
    for value in tuple(values):
        text = _optional_text(value)
        if text and text not in result:
            result.append(text)
    return tuple(result)


def _mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise ValueError("evidence must be a mapping.")
    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class DiagnosticGroupRecord:
    """One deterministic or human-created diagnostic group."""

    group_id: str
    project_id: str
    producer_id: str
    scope_fingerprint: str
    kind: str
    recipe_id: str
    label: str
    confidence: str
    member_issue_fingerprints: tuple[str, ...] = ()
    evidence: Mapping[str, Any] = field(default_factory=dict)
    review_state: str = "UNREVIEWED"
    created_at_utc: str = ""
    reviewed_at_utc: str = ""
    author: str = ""
    generation: int = 0

    def __post_init__(self) -> None:
        for field_name in (
            "group_id",
            "project_id",
            "producer_id",
            "scope_fingerprint",
            "recipe_id",
            "label",
        ):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        object.__setattr__(self, "kind", _choice(self.kind, GROUP_KINDS, "group kind"))
        object.__setattr__(self, "confidence", _confidence(self.confidence))
        object.__setattr__(
            self,
            "review_state",
            _choice(self.review_state, GROUP_REVIEW_STATES, "group review state"),
        )
        members = tuple(sorted(_tuple_text(self.member_issue_fingerprints)))
        object.__setattr__(self, "member_issue_fingerprints", members)
        object.__setattr__(self, "evidence", _mapping(self.evidence))
        object.__setattr__(self, "created_at_utc", _optional_text(self.created_at_utc))
        object.__setattr__(self, "reviewed_at_utc", _optional_text(self.reviewed_at_utc))
        object.__setattr__(self, "author", _optional_text(self.author))
        generation = int(self.generation)
        if generation < 0:
            raise ValueError("group generation cannot be negative.")
        object.__setattr__(self, "generation", generation)
        if self.kind == "DETERMINISTIC" and self.author:
            raise ValueError("Deterministic groups cannot declare a human author.")
        if self.kind == "MANUAL" and not self.author:
            raise ValueError("Manual groups require an author.")


@dataclass(frozen=True, slots=True)
class DiagnosticGroupDecisionRecord:
    """Append-only history record for one manual grouping decision."""

    decision_id: str
    group_id: str
    project_id: str
    producer_id: str
    scope_fingerprint: str
    action: str
    issue_fingerprint: str
    previous_group_id: str
    reason: str
    author: str
    created_at_utc: str
    resulting_generation: int

    def __post_init__(self) -> None:
        for field_name in (
            "decision_id",
            "group_id",
            "project_id",
            "producer_id",
            "scope_fingerprint",
            "reason",
            "author",
            "created_at_utc",
        ):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        object.__setattr__(
            self,
            "action",
            _choice(self.action, GROUP_DECISION_ACTIONS, "group decision action"),
        )
        object.__setattr__(
            self,
            "issue_fingerprint",
            _optional_text(self.issue_fingerprint),
        )
        object.__setattr__(
            self,
            "previous_group_id",
            _optional_text(self.previous_group_id),
        )
        generation = int(self.resulting_generation)
        if generation < 1:
            raise ValueError("resulting_generation must be positive.")
        object.__setattr__(self, "resulting_generation", generation)
        if self.action in {"ASSIGN_ISSUE", "UNGROUP_ISSUE"} and not self.issue_fingerprint:
            raise ValueError(self.action + " requires issue_fingerprint.")


@dataclass(frozen=True, slots=True)
class DiagnosticManualGroupingState:
    """Current manual groups plus append-only decision history for one scope."""

    project_id: str
    producer_id: str
    scope_fingerprint: str
    generation: int
    groups: tuple[DiagnosticGroupRecord, ...] = ()
    decisions: tuple[DiagnosticGroupDecisionRecord, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("project_id", "producer_id", "scope_fingerprint"):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        generation = int(self.generation)
        if generation < 0:
            raise ValueError("manual grouping generation cannot be negative.")
        object.__setattr__(self, "generation", generation)
        object.__setattr__(self, "groups", tuple(self.groups))
        object.__setattr__(self, "decisions", tuple(self.decisions))
