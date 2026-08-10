# project-path: kanda_reasoner_app/engineering_diagnostics_gui/_engineering_capability_models.py
"""Immutable models for Full Diagnostics Engineering Safety coverage."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "EngineeringCapabilityCoverage",
    "EngineeringCapabilityResult",
]


@dataclass(frozen=True, slots=True)
class EngineeringCapabilityResult:
    """One explicit Engineering Safety capability assessment."""

    surface: str
    section: str
    label: str
    command_name: str
    scope_mode: str
    status: str
    severity: str
    assessment_reason: str
    execution: str
    status_code: int | None = None
    elapsed_seconds: float = 0.0
    finding_count: int | None = None
    evidence: str = ""
    correction_guidance: str = ""


@dataclass(frozen=True, slots=True)
class EngineeringCapabilityCoverage:
    """Complete coverage ledger for GUI, CLI, and Architecture surfaces."""

    results: tuple[EngineeringCapabilityResult, ...]
    gui_catalog_count: int
    cli_catalog_count: int
    unique_safety_surface_count: int
    architecture_surface_count: int

    @property
    def total_surface_count(self) -> int:
        return self.unique_safety_surface_count + self.architecture_surface_count

    @property
    def error_count(self) -> int:
        return sum(item.severity == "ERROR" for item in self.results)

    @property
    def warning_count(self) -> int:
        return sum(item.severity == "WARNING" for item in self.results)

    @property
    def clean_count(self) -> int:
        return sum(item.status == "CLEAN" for item in self.results)
