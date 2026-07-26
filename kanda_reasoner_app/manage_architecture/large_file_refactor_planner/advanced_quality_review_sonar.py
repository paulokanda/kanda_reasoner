# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_review_sonar.py
"""Sonar feedback adapter for the Workbench Advanced Quality Review lifecycle."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.templates.green_sonar_monitor import (
    GreenSonarActivityMonitor,
)

__all__ = [
    "finish_aqr_sonar_blocked",
    "finish_aqr_sonar_success",
    "start_aqr_sonar",
    "update_aqr_sonar",
]

_MONITOR_ATTR = "_large_file_refactor_workbench_aqr_sonar_monitor"

_STAGE_LABELS = {
    "STARTING": "Starting Advanced Quality Review worker",
    "ENVIRONMENT_PREFLIGHT": "Checking pinned analyzer environment",
    "RUFF": "Running Ruff review",
    "API_REVIEW": "Reviewing public API contract",
    "IMPORT_GRAPH": "Reviewing import graph topology",
    "TYPE_REVIEW": "Running type-contract review",
    "DEAD_CODE": "Running dead-code advisory review",
    "DELTA": "Building baseline/Preview delta",
    "CROSS_CHECK": "Cross-checking analyzer evidence",
    "PERSISTENCE": "Persisting immutable AQR evidence",
    "CANCEL_REQUESTED": "Cancellation requested; settling worker",
}


def start_aqr_sonar(window: Any) -> None:
    """Start the Workbench AQR activity monitor."""
    if _main_workbench_owns_sonar(window):
        return
    monitor = _monitor(window)
    if monitor is None:
        return
    monitor.start(
        "Advanced Quality Review running",
        (
            "Pinned five-analyzer review is active",
            "Stages run sequentially with fail-closed evidence",
            "GUI remains responsive; Cancel remains available",
        ),
    )


def update_aqr_sonar(window: Any, stage: str, message: str) -> None:
    """Update the activity monitor from real AQR worker progress."""
    if _main_workbench_owns_sonar(window):
        return
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is None:
        return
    stage_text = _STAGE_LABELS.get(str(stage), str(stage).replace("_", " ").title())
    detail = _single_line(message, "AQR worker progress received")
    monitor.start(
        "Advanced Quality Review running",
        (
            stage_text,
            detail,
            "Preflight remains closed until terminal authorization evidence passes",
        ),
    )


def finish_aqr_sonar_success(window: Any, message: str) -> None:
    """Settle sonar on one authorizing AQR outcome."""
    if _main_workbench_owns_sonar(window):
        return
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is None:
        return
    monitor.finish_success(
        "Advanced Quality Review ready",
        (
            _single_line(message, "AQR completed with authorizing evidence"),
            "Canonical progression may now evaluate Preflight",
            "No source mutation was performed by AQR",
        ),
    )


def finish_aqr_sonar_blocked(window: Any, message: str) -> None:
    """Settle sonar on blocked, failed, cancelled, or indeterminate AQR."""
    if _main_workbench_owns_sonar(window):
        return
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is None:
        return
    monitor.finish_error(
        "Advanced Quality Review stopped",
        (
            _single_line(message, "AQR ended without authorizing evidence"),
            "Preflight remains closed",
            "Correction routes remain available for terminal blocker evidence",
        ),
    )


def _main_workbench_owns_sonar(window: Any) -> bool:
    """Return whether the automatic pipeline owns the shared feedback corner."""
    return bool(
        getattr(
            window,
            "_large_file_refactor_main_workbench_sonar_active",
            False,
        )
    )


def _monitor(window: Any) -> GreenSonarActivityMonitor | None:
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is not None:
        return monitor
    try:
        monitor = GreenSonarActivityMonitor(
            window,
            title="Workbench Advanced Quality Review",
        )
    except (RuntimeError, TypeError):
        return None
    setattr(window, _MONITOR_ATTR, monitor)
    return monitor


def _single_line(message: str, fallback: str) -> str:
    lines = str(message or "").strip().splitlines()
    return lines[0][:120] if lines else fallback
