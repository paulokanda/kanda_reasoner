# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_sonar_activity.py
"""Planner-local adapter for the reusable green sonar activity monitor."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.templates.green_sonar_monitor import (
    GreenSonarActivityMonitor,
)

__all__ = [
    "finish_planner_sonar_error",
    "finish_planner_sonar_success",
    "start_local_ai_review_sonar",
    "start_split_plan_sonar",
]


def _planner_monitor(window: Any) -> GreenSonarActivityMonitor:
    """Return the box-local Planner sonar monitor."""

    monitor = getattr(window, "_large_file_refactor_planner_sonar_monitor", None)
    if monitor is None:
        monitor = GreenSonarActivityMonitor(
            window,
            title="Large File Refactor Planner",
        )
        window._large_file_refactor_planner_sonar_monitor = monitor
    return monitor


def start_split_plan_sonar(window: Any, target_label: str) -> None:
    """Show deterministic split-plan generation activity."""

    _planner_monitor(window).start(
        "Generating split plan",
        (
            "Grouping symbols by responsibility and dependency evidence",
            "Target: " + str(target_label or "selected module"),
            "Planner remains pre-implementation and does not write source",
        ),
    )


def start_local_ai_review_sonar(window: Any) -> None:
    """Show explicit comprehensive local-AI planning review activity."""

    _planner_monitor(window).start(
        "Reviewing and refining planning with local AI",
        (
            "Reviewing split grouping and ambiguous symbol ownership",
            "Reviewing low-confidence docstring proposals",
            "All accepted refinements remain bounded and revalidated",
        ),
    )


def finish_planner_sonar_success(window: Any, result_status: str) -> None:
    """Show successful completion feedback and schedule monitor hiding."""

    monitor = getattr(window, "_large_file_refactor_planner_sonar_monitor", None)
    if monitor is None:
        return
    monitor.finish_success(
        "Planning work complete",
        (
            "Result: " + str(result_status or "completed"),
            "Review the Proposed split plan panel",
            "Continue to Workbench only when the plan is valid",
        ),
    )


def finish_planner_sonar_error(window: Any, message: str) -> None:
    """Show attention feedback and schedule monitor hiding."""

    monitor = getattr(window, "_large_file_refactor_planner_sonar_monitor", None)
    if monitor is None:
        return
    monitor.finish_error(
        "Planning work needs review",
        (
            str(message or "Planner work did not complete cleanly"),
            "Review blockers and warnings in the Planner",
            "No source write is performed by this monitor",
        ),
    )
