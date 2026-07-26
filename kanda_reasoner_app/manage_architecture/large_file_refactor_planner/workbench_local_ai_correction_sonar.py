# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_local_ai_correction_sonar.py
"""Sonar activity adapter for Workbench Local AI correction lifecycle."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.templates.green_sonar_monitor import (
    GreenSonarActivityMonitor,
)

__all__ = [
    "finish_local_ai_correction_sonar_error",
    "finish_local_ai_correction_sonar_success",
    "start_local_ai_correction_sonar",
    "update_local_ai_correction_sonar",
]

_MONITOR_ATTR = "_workbench_local_ai_correction_sonar_monitor"

_PHASE_LABELS = {
    "STARTING_QTHREAD_WORKER": "Starting Qt worker",
    "ANALYZE_SOURCE": "Analyzing source structure",
    "BOUNDED_LOCAL_AI_STAGED_REVIEW": "Running bounded Local AI review",
    "RESPONSIBILITY_ANALYSIS": "Reviewing responsibility boundaries",
    "TARGETED_REPAIR_ATTEMPT_1": "Applying bounded repair attempt 1",
    "TARGETED_REPAIR_ATTEMPT_2": "Applying bounded repair attempt 2",
    "VALIDATE_CORRECTED_PLAN": "Validating corrected plan",
    "CANDIDATE_READY": "Preparing corrected candidate handoff",
}


def start_local_ai_correction_sonar(window: Any, stage: str) -> None:
    """Show animated sonar while one Local AI correction generation runs."""
    monitor = _monitor(window)
    if monitor is None:
        return
    monitor.start(
        "Local AI correction running",
        (
            "Stage: " + str(stage or "blocked Workbench stage"),
            "Bounded single-track correction is active",
            "GUI remains responsive; Cancel Local AI Wait is available",
        ),
    )


def update_local_ai_correction_sonar(window: Any, stage: str, phase: str) -> None:
    """Update sonar text while preserving the running animation."""
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is None:
        return
    phase_text = _PHASE_LABELS.get(str(phase), str(phase).replace("_", " ").title())
    monitor.start(
        "Local AI correction running",
        (
            phase_text,
            "Stage: " + str(stage or "blocked Workbench stage"),
            "No downstream gate opens until deterministic rerun evidence passes",
        ),
    )


def finish_local_ai_correction_sonar_success(window: Any, message: str) -> None:
    """Show successful Local AI correction settlement feedback."""
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is None:
        return
    monitor.finish_success(
        "Local AI correction candidate ready",
        (
            _single_line(message, "Candidate accepted for governed reload"),
            "Downstream evidence must be rerun deterministically",
            "No source mutation was performed by the correction worker",
        ),
    )


def finish_local_ai_correction_sonar_error(window: Any, message: str) -> None:
    """Show error, timeout, or cancellation settlement feedback."""
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is None:
        return
    monitor.finish_error(
        "Local AI correction stopped",
        (
            _single_line(message, "Correction did not complete cleanly"),
            "Current Workbench evidence remains fail-closed",
            "Heuristic and Web AI recovery routes remain available when allowed",
        ),
    )


def _monitor(window: Any) -> GreenSonarActivityMonitor | None:
    """Return the Workbench-local monitor without breaking non-widget fixtures."""
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is not None:
        return monitor
    try:
        monitor = GreenSonarActivityMonitor(
            window,
            title="Workbench Local AI Correction",
        )
    except (RuntimeError, TypeError):
        return None
    setattr(window, _MONITOR_ATTR, monitor)
    return monitor


def _single_line(message: str, fallback: str) -> str:
    """Return a compact first-line status for the floating monitor."""
    first_line = str(message or "").strip().splitlines()
    return first_line[0][:120] if first_line else fallback
