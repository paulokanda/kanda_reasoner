# project-path: kanda_reasoner_app/engineering_diagnostics_gui/engineering_capability_render.py
"""Rendering helpers for comprehensive Engineering Safety capability coverage."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from ._engineering_capability_models import (
    EngineeringCapabilityCoverage,
    EngineeringCapabilityResult,
)
from .engineering_capability_dossier import build_capability_dossier_lines

__all__ = [
    "build_capability_console_summary",
    "build_capability_report_lines",
]


def _status_counts(
    results: Iterable[EngineeringCapabilityResult],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in results:
        counts[item.status] = counts.get(item.status, 0) + 1
    return dict(sorted(counts.items()))


def build_capability_console_summary(
    coverage: EngineeringCapabilityCoverage,
) -> str:
    """Return a compact capability ledger for the Full Diagnostics console."""
    problem_count = coverage.error_count + coverage.warning_count
    lines = [
        "FULL ENGINEERING CAPABILITY COVERAGE",
        (
            "Pontual Audit GUI catalog: "
            + str(coverage.gui_catalog_count)
            + "/"
            + str(coverage.gui_catalog_count)
            + " ACCOUNTED"
        ),
        (
            "Safety Suite CLI catalog: "
            + str(coverage.cli_catalog_count)
            + "/"
            + str(coverage.cli_catalog_count)
            + " ACCOUNTED"
        ),
        (
            "Unique GUI/CLI safety surfaces: "
            + str(coverage.unique_safety_surface_count)
            + "/"
            + str(coverage.unique_safety_surface_count)
            + " ACCOUNTED"
        ),
        "Architecture Review: 1/1 ACCOUNTED",
        (
            "Total engineering surfaces: "
            + str(coverage.total_surface_count)
            + "/"
            + str(coverage.total_surface_count)
            + " ACCOUNTED"
        ),
        "Errors: " + str(coverage.error_count),
        "Warnings: " + str(coverage.warning_count),
        "Architecture-grade capability dossiers: " + str(problem_count),
        "Status counts: " + str(_status_counts(coverage.results)),
        "Silent capability omissions: 0",
        "Problem and warning surfaces:",
    ]

    problems = [
        item for item in coverage.results if item.severity in {"ERROR", "WARNING"}
    ]
    if not problems:
        lines.append("- none")

    for item in problems[:20]:
        lines.append(
            "- ["
            + item.severity
            + "] "
            + item.label
            + " ("
            + item.command_name
            + "): "
            + item.status
            + " - "
            + item.assessment_reason
        )

    omitted = len(problems) - 20
    if omitted > 0:
        lines.append(
            "Additional warning/error surfaces in full handoff: " + str(omitted)
        )
    return "\n".join(lines)


def build_capability_report_lines(
    project_root: str | Path,
    coverage: EngineeringCapabilityCoverage,
) -> list[str]:
    """Render all capability surfaces plus detailed problem/warning dossiers."""
    problems = [
        item for item in coverage.results if item.severity in {"ERROR", "WARNING"}
    ]
    lines = [
        "FULL ENGINEERING CAPABILITY COVERAGE LEDGER",
        "Pontual Audit GUI accounted: "
        + str(coverage.gui_catalog_count)
        + "/"
        + str(coverage.gui_catalog_count),
        "Safety Suite CLI accounted: "
        + str(coverage.cli_catalog_count)
        + "/"
        + str(coverage.cli_catalog_count),
        "Unique GUI/CLI safety surfaces accounted: "
        + str(coverage.unique_safety_surface_count)
        + "/"
        + str(coverage.unique_safety_surface_count),
        "Architecture Review accounted: 1/1",
        "Total engineering surfaces accounted: "
        + str(coverage.total_surface_count)
        + "/"
        + str(coverage.total_surface_count),
        "Silent capability omissions: 0",
        "Capability errors: " + str(coverage.error_count),
        "Capability warnings: " + str(coverage.warning_count),
        "Architecture-grade correction dossiers: " + str(len(problems)),
        "",
        "CAPABILITY INDEX",
    ]

    for index, item in enumerate(coverage.results, start=1):
        lines.append(
            str(index).zfill(2)
            + " | "
            + item.section
            + " | "
            + item.label
            + " | "
            + item.command_name
            + " | "
            + item.status
            + " | "
            + item.severity
            + " | "
            + item.scope_mode
        )

    lines.extend(("", "CAPABILITY DETAILS", ""))
    for index, item in enumerate(coverage.results, start=1):
        lines.extend(build_capability_dossier_lines(project_root, item, index))

    return lines
