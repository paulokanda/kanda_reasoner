# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_sonar.py
"""Sonar feedback adapter for Main Workbench and Web AI package lifecycle."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.templates.green_sonar_monitor import (
    GreenSonarActivityMonitor,
)

from .main_workbench_pipeline_models import (
    MAIN_WORKBENCH_CANCELLED,
    MAIN_WORKBENCH_FAILED,
    MAIN_WORKBENCH_READY,
    MAIN_WORKBENCH_STALE,
    MAIN_WORKBENCH_WEB_AI_BLOCKED,
    MainWorkbenchControllerState,
)

__all__ = [
    "finish_main_workbench_package_sonar",
    "main_workbench_sonar_is_active",
    "start_main_workbench_package_sonar",
    "sync_main_workbench_sonar",
    "update_main_workbench_package_sonar",
]

_MONITOR_ATTR = "_large_file_refactor_main_workbench_sonar_monitor"
_ACTIVE_ATTR = "_large_file_refactor_main_workbench_sonar_active"

_STAGE_LABELS = {
    "PLAN_INTAKE": "Loading and validating the Planner handoff",
    "DEPENDENCY_READINESS": "Checking helper and facade dependencies",
    "REAL_PREVIEW": "Generating the real source Preview",
    "STRUCTURAL_VALIDATION": "Validating the generated module family",
    "ADVANCED_QUALITY_REVIEW": "Running the guarded quality review",
    "TERMINAL": "Settling Main Workbench evidence",
}

_PACKAGE_LABELS = {
    "RUNNING": "Collecting bounded Project context",
    "CANCEL_REQUESTED": "Package cancellation requested",
    "CANCELLED": "Package result cancelled",
    "STALE": "Package evidence became stale",
    "FAILED": "Package construction failed",
    "READY": "Verified Web AI package is ready",
}


def main_workbench_sonar_is_active(window: Any) -> bool:
    """Return whether Main Workbench currently owns floating sonar feedback."""
    return bool(getattr(window, _ACTIVE_ATTR, False))


def sync_main_workbench_sonar(
    window: Any,
    state: MainWorkbenchControllerState,
) -> None:
    """Project one pipeline state onto the shared Main Workbench sonar."""
    monitor = _monitor(window)
    if monitor is None:
        return
    if state.running:
        _set_active(window, True)
        stage_text = _STAGE_LABELS.get(
            str(state.stage),
            str(state.stage).replace("_", " ").title(),
        )
        cancellation = (
            "Cancellation requested; late worker output will be ignored"
            if state.cancel_requested
            else "Generation " + str(state.generation) + " remains authoritative"
        )
        monitor.start(
            "Main Workbench running",
            (
                stage_text,
                _single_line(state.message, "Automatic pipeline is progressing"),
                cancellation,
            ),
        )
        return
    _set_active(window, False)
    terminal = str(state.terminal_status or "")
    if terminal == MAIN_WORKBENCH_READY:
        monitor.finish_success(
            "Main Workbench ready for Web AI",
            (
                "All local deterministic assurance stages completed",
                "Canonical Active Project source was not modified",
                "Send Complete Project to Web AI is now available",
            ),
        )
    elif terminal == MAIN_WORKBENCH_WEB_AI_BLOCKED:
        monitor.finish_success(
            "Main Workbench evidence packageable",
            (
                "Unresolved blockers require external semantic review",
                "The complete Preview and blocker evidence are preserved",
                "Canonical Active Project source was not modified",
            ),
        )
    elif terminal in {
        MAIN_WORKBENCH_FAILED,
        MAIN_WORKBENCH_STALE,
        MAIN_WORKBENCH_CANCELLED,
    }:
        monitor.finish_error(
            "Main Workbench stopped",
            (
                _single_line(state.message, "Pipeline ended without package readiness"),
                _blocker_summary(state.blockers),
                "Use the detailed Workbench or rerun from a fresh card state",
            ),
        )


def start_main_workbench_package_sonar(window: Any) -> None:
    """Start sonar while the complete Web AI package is assembled."""
    monitor = _monitor(window)
    if monitor is None:
        return
    _set_active(window, True)
    monitor.start(
        "Building complete Web AI package",
        (
            _PACKAGE_LABELS["RUNNING"],
            "Manifest, hashes, candidates, and governance context are being verified",
            "Canonical Active Project source remains read-only",
        ),
    )


def update_main_workbench_package_sonar(window: Any, status: str) -> None:
    """Update running package feedback without creating another monitor."""
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is None:
        return
    _set_active(window, True)
    monitor.start(
        "Building complete Web AI package",
        (
            _PACKAGE_LABELS.get(str(status), str(status).replace("_", " ").title()),
            "Only the current sealed card generation may be published",
            "Incomplete staging artifacts are not exchange authority",
        ),
    )


def finish_main_workbench_package_sonar(
    window: Any,
    status: str,
    message: str,
) -> None:
    """Settle package sonar on ready, failed, cancelled, or stale outcome."""
    monitor = getattr(window, _MONITOR_ATTR, None)
    _set_active(window, False)
    if monitor is None:
        return
    detail = _single_line(message, _PACKAGE_LABELS.get(status, "Package settled"))
    if status == "READY":
        monitor.finish_success(
            "Complete Web AI package ready",
            (
                detail,
                "The verified ZIP and self-contained prompt are available",
                "Repeated identical evidence will reuse the same exchange",
            ),
        )
        return
    monitor.finish_error(
        "Web AI package stopped",
        (
            detail,
            "No incomplete package was promoted as exchange authority",
            "Rerun Main Workbench when source or evidence is stale",
        ),
    )


def _monitor(window: Any) -> GreenSonarActivityMonitor | None:
    monitor = getattr(window, _MONITOR_ATTR, None)
    if monitor is not None:
        return monitor
    try:
        monitor = GreenSonarActivityMonitor(window, title="Main Workbench")
    except (RuntimeError, TypeError):
        return None
    setattr(window, _MONITOR_ATTR, monitor)
    return monitor


def _set_active(window: Any, active: bool) -> None:
    setattr(window, _ACTIVE_ATTR, bool(active))


def _single_line(message: str, fallback: str) -> str:
    lines = str(message or "").strip().splitlines()
    return lines[0][:120] if lines else fallback


def _blocker_summary(blockers: tuple[str, ...]) -> str:
    if not blockers:
        return "No additional blocker details were recorded"
    return "First blocker: " + str(blockers[0])[:104]
