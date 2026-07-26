# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_split_plan_gui.py
"""Qt-safe background runner for deterministic split-plan generation."""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QTimer

from .models import PlannerState
from .planner_version_selector_gui import refresh_planner_version_selector
from .planner_version_state import store_heuristic_version
from .planner_sonar_activity import (
    finish_planner_sonar_error,
    finish_planner_sonar_success,
    start_split_plan_sonar,
)
from .split_formatting import format_split_plan
from .split_planner import build_split_plan

__all__ = ["start_split_plan_generation_for_window"]


def start_split_plan_generation_for_window(
    window: object,
    report: Any,
    settings: Any,
    *,
    refresh_callback: Callable[[object], None],
    completion_callback: Callable[[object, Any], None] | None = None,
) -> None:
    """Build the deterministic split plan off the GUI thread only."""

    if bool(getattr(window, "_large_file_refactor_split_plan_running", False)):
        return

    request_id = object()
    result_queue: queue.Queue[tuple[object, Any, str]] = queue.Queue(maxsize=1)
    window._large_file_refactor_split_plan_running = True
    window._large_file_refactor_split_plan_request_id = request_id
    window._large_file_refactor_split_plan_queue = result_queue

    target_label = str(getattr(report, "target_file", "") or "selected module")
    source_path = str(
        getattr(window, "_large_file_refactor_planner_selected_path", "") or ""
    )
    start_split_plan_sonar(window, target_label)
    refresh_callback(window)

    def worker() -> None:
        try:
            plan = build_split_plan(report, settings, source_path=source_path or None)
            result_queue.put_nowait((request_id, plan, ""))
        except Exception as exc:
            result_queue.put_nowait((request_id, None, str(exc)))

    thread = threading.Thread(
        target=worker,
        name="kanda-large-file-split-plan-generation",
        daemon=True,
    )
    timer = QTimer()
    timer.setInterval(120)
    window._large_file_refactor_split_plan_thread = thread
    window._large_file_refactor_split_plan_timer = timer

    def poll() -> None:
        try:
            returned_id, plan, error_text = result_queue.get_nowait()
        except queue.Empty:
            return

        if returned_id is not getattr(
            window,
            "_large_file_refactor_split_plan_request_id",
            None,
        ):
            return

        timer.stop()
        window._large_file_refactor_split_plan_running = False

        if error_text:
            window._large_file_refactor_planner_state = PlannerState.BLOCKED.value
            window._large_file_refactor_plan_output.setPlainText(
                "Split-plan generation failed: " + error_text
            )
            finish_planner_sonar_error(window, error_text)
            refresh_callback(window)
            return

        store_heuristic_version(window, plan, [])
        refresh_planner_version_selector(window)
        window._large_file_refactor_plan_output.setPlainText(format_split_plan(plan))
        window._large_file_refactor_planner_state = (
            PlannerState.BLOCKED.value
            if getattr(plan, "status", "") == "blocked"
            else PlannerState.PLAN_READY.value
        )
        window._large_file_refactor_plan_ai_review_result = None
        window._large_file_refactor_web_ai_proposal = None
        window._large_file_refactor_web_ai_proposal_applied = False
        finish_planner_sonar_success(
            window,
            "deterministic split plan ready",
        )
        refresh_callback(window)
        if completion_callback is not None:
            completion_callback(window, plan)

    timer.timeout.connect(poll)
    thread.start()
    timer.start()
