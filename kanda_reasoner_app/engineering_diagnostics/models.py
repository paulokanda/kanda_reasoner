# project-path: kanda_reasoner_app/engineering_diagnostics/models.py
"""Immutable public data contracts for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

__all__ = [
    "BASELINE_STATES",
    "DIAGNOSTIC_SCHEMA_VERSION",
    "DiagnosticBaselineRecord",
    "DiagnosticBoundaryError",
    "DiagnosticComparison",
    "DiagnosticConflictError",
    "DiagnosticFindingInput",
    "DiagnosticFindingRecord",
    "DiagnosticRunInput",
    "DiagnosticRunRecord",
    "DiagnosticStateError",
    "DiagnosticValidationError",
    "EngineeringDiagnosticsError",
]

DIAGNOSTIC_SCHEMA_VERSION = "1.0"
BASELINE_STATES = frozenset({"DRAFT", "ACTIVE", "SUPERSEDED", "RETIRED"})
_VALID_RUN_STATUSES = frozenset({"COMPLETED"})
_VALID_SEVERITIES = frozenset({"info", "warning", "error"})
_VALID_CONFIDENCE = frozenset({"low", "medium", "high"})


class EngineeringDiagnosticsError(RuntimeError):
    """Base error for the Engineering Diagnostics public contract."""


class DiagnosticValidationError(EngineeringDiagnosticsError, ValueError):
    """Raised when boundary data violates the public contract."""


class DiagnosticBoundaryError(EngineeringDiagnosticsError):
    """Raised when Project identity or ownership is stale or mismatched."""


class DiagnosticConflictError(EngineeringDiagnosticsError):
    """Raised when one immutable identity is reused with different content."""


class DiagnosticStateError(EngineeringDiagnosticsError):
    """Raised when a baseline or run transition is invalid."""


def _required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise DiagnosticValidationError(field_name + " is required.")
    return text


def _optional_text(value: object) -> str:
    return str(value or "").strip()


def _mapping_copy(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise DiagnosticValidationError("Mapping value is required.")
    return MappingProxyType(dict(value))


def _normalize_severity(value: object) -> str:
    text = str(value or "warning").strip().lower()
    if text not in _VALID_SEVERITIES:
        raise DiagnosticValidationError("Unsupported diagnostic severity: " + text)
    return text


def _normalize_confidence(value: object) -> str:
    text = str(value or "medium").strip().lower()
    if text not in _VALID_CONFIDENCE:
        raise DiagnosticValidationError("Unsupported diagnostic confidence: " + text)
    return text


@dataclass(frozen=True, slots=True)
class DiagnosticFindingInput:
    """One producer finding before deterministic identity is assigned."""

    code: str
    relative_path: str
    message: str
    severity: str = "warning"
    confidence: str = "medium"
    semantic_key: str = ""
    symbol_id: str = ""
    location_key: str = ""
    category: str = ""
    line: int | None = None
    evidence: Mapping[str, Any] = field(default_factory=dict)
    suggested_action: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _required_text(self.code, "code"))
        object.__setattr__(
            self,
            "relative_path",
            _required_text(self.relative_path, "relative_path"),
        )
        object.__setattr__(self, "message", _required_text(self.message, "message"))
        object.__setattr__(self, "severity", _normalize_severity(self.severity))
        object.__setattr__(
            self,
            "confidence",
            _normalize_confidence(self.confidence),
        )
        object.__setattr__(self, "semantic_key", _optional_text(self.semantic_key))
        object.__setattr__(self, "symbol_id", _optional_text(self.symbol_id))
        object.__setattr__(self, "location_key", _optional_text(self.location_key))
        object.__setattr__(self, "category", _optional_text(self.category))
        object.__setattr__(
            self,
            "suggested_action",
            _optional_text(self.suggested_action),
        )
        if self.line is not None and int(self.line) < 1:
            raise DiagnosticValidationError("line must be positive when supplied.")
        if self.line is not None:
            object.__setattr__(self, "line", int(self.line))
        object.__setattr__(self, "evidence", _mapping_copy(self.evidence))


@dataclass(frozen=True, slots=True)
class DiagnosticRunInput:
    """One completed producer run submitted to the persistence owner."""

    attempt_id: str
    project_id: str
    project_root_fingerprint: str
    producer_id: str
    producer_version: str
    source_fingerprint: str
    scope_fingerprint: str
    configuration_fingerprint: str
    operation_generation: int
    findings: tuple[DiagnosticFindingInput, ...] = ()
    completion_status: str = "COMPLETED"
    started_at_utc: str = ""
    completed_at_utc: str = ""
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in (
            "attempt_id",
            "project_id",
            "project_root_fingerprint",
            "producer_id",
            "producer_version",
            "source_fingerprint",
            "scope_fingerprint",
            "configuration_fingerprint",
        ):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        status = str(self.completion_status or "").strip().upper()
        if status not in _VALID_RUN_STATUSES:
            raise DiagnosticValidationError(
                "Only completed diagnostic runs are accepted in Wave 2O-A."
            )
        object.__setattr__(self, "completion_status", status)
        generation = int(self.operation_generation)
        if generation < 0:
            raise DiagnosticValidationError("operation_generation cannot be negative.")
        object.__setattr__(self, "operation_generation", generation)
        object.__setattr__(self, "findings", tuple(self.findings))
        if not all(isinstance(item, DiagnosticFindingInput) for item in self.findings):
            raise DiagnosticValidationError(
                "findings must contain DiagnosticFindingInput values."
            )
        object.__setattr__(
            self,
            "started_at_utc",
            _optional_text(self.started_at_utc),
        )
        object.__setattr__(
            self,
            "completed_at_utc",
            _optional_text(self.completed_at_utc),
        )
        object.__setattr__(self, "provenance", _mapping_copy(self.provenance))


@dataclass(frozen=True, slots=True)
class DiagnosticFindingRecord:
    """Persisted normalized finding associated with one completed run."""

    run_id: str
    issue_fingerprint: str
    evidence_digest: str
    code: str
    relative_path: str
    message: str
    severity: str
    confidence: str
    semantic_key: str
    symbol_id: str
    location_key: str
    category: str
    line: int | None
    evidence: Mapping[str, Any]
    suggested_action: str


@dataclass(frozen=True, slots=True)
class DiagnosticRunRecord:
    """Persisted identity and provenance for one completed run."""

    run_id: str
    attempt_id: str
    project_id: str
    project_root_fingerprint: str
    producer_id: str
    producer_version: str
    scan_identity: str
    source_fingerprint: str
    scope_fingerprint: str
    configuration_fingerprint: str
    operation_generation: int
    completion_status: str
    finding_count: int
    content_digest: str
    started_at_utc: str
    completed_at_utc: str
    provenance: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class DiagnosticBaselineRecord:
    """Immutable baseline metadata and lifecycle state."""

    baseline_id: str
    project_id: str
    producer_id: str
    scope_fingerprint: str
    source_run_id: str
    label: str
    state: str
    content_digest: str
    finding_count: int
    created_at_utc: str
    activated_at_utc: str
    superseded_at_utc: str
    generation: int


@dataclass(frozen=True, slots=True)
class DiagnosticComparison:
    """Read-only comparison between one run and its active baseline."""

    run_id: str
    baseline_id: str | None
    status: str
    new_issue_fingerprints: tuple[str, ...]
    persistent_issue_fingerprints: tuple[str, ...]
    resolved_issue_fingerprints: tuple[str, ...]
