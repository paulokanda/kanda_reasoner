# project-path: kanda_reasoner_app/engineering_diagnostics_gui/navigation_models.py
"""Immutable public navigation contracts for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

from kanda_reasoner_app.engineering_diagnostics import (
    ARCHITECTURE_PRODUCER_ID,
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    SHADOW_PRODUCER_ID,
)

__all__ = [
    "EngineeringDiagnosticsNavigationRequest",
    "EngineeringDiagnosticsNavigationSummary",
]

_ALLOWED_PRODUCERS = frozenset(
    {
        BOM_PRODUCER_ID,
        RUFF_PRODUCER_ID,
        ARCHITECTURE_PRODUCER_ID,
        SHADOW_PRODUCER_ID,
    }
)
_ALLOWED_BASELINE_STATES = frozenset({"all", "new", "persistent", "current"})
_ALLOWED_SEVERITIES = frozenset({"all", "error", "warning", "info"})


def _required_choice(value: object, allowed: frozenset[str], field_name: str) -> str:
    text = str(value or "").strip().lower()
    if text not in allowed:
        raise ValueError("Unsupported " + field_name + ": " + text)
    return text


@dataclass(frozen=True, slots=True)
class EngineeringDiagnosticsNavigationRequest:
    """One explicit read-only request to show an existing diagnostic run."""

    producer_id: str
    compatible_run_id: str = ""
    baseline_state: str = "all"
    rule_family: str = ""
    severity: str = "all"
    origin: str = "full_audit"

    def __post_init__(self) -> None:
        producer = str(self.producer_id or "").strip()
        if producer not in _ALLOWED_PRODUCERS:
            raise ValueError("Unsupported producer_id: " + producer)
        object.__setattr__(self, "producer_id", producer)
        object.__setattr__(
            self,
            "compatible_run_id",
            str(self.compatible_run_id or "").strip(),
        )
        object.__setattr__(
            self,
            "baseline_state",
            _required_choice(
                self.baseline_state,
                _ALLOWED_BASELINE_STATES,
                "baseline_state",
            ),
        )
        object.__setattr__(
            self,
            "severity",
            _required_choice(self.severity, _ALLOWED_SEVERITIES, "severity"),
        )
        object.__setattr__(self, "rule_family", str(self.rule_family or "").strip())
        origin = str(self.origin or "").strip()
        if not origin:
            raise ValueError("origin is required.")
        object.__setattr__(self, "origin", origin)


@dataclass(frozen=True, slots=True)
class EngineeringDiagnosticsNavigationSummary:
    """Read-only counts for the newest source-compatible diagnostic run."""

    producer_id: str
    compatible_run_id: str
    raw_finding_count: int
    canonical_issue_count: int
    diagnostic_group_count: int
    new_high_priority_count: int
    comparison_status: str
    source_fingerprint: str

    @property
    def available(self) -> bool:
        """Return whether a source-compatible run can be opened."""
        return bool(self.compatible_run_id)
