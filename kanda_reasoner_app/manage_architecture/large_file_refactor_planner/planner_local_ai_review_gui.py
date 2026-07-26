# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_review_gui.py
"""Qt-safe background runner for the explicit comprehensive local-AI stage."""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable

from PySide6.QtCore import QTimer

from .docstring_formatting import format_docstring_proposals
from .models import PlannerState
from .planner_local_ai_comprehensive_formatting import (
    format_comprehensive_local_ai_review,
)
from .planner_local_ai_comprehensive_review import (
    ComprehensiveLocalAIReviewResult,
    review_and_refine_planning_with_local_ai,
)
from .planner_version_selector_gui import (
    refresh_planner_version_selector,
    render_selected_planner_version,
)
from .planner_version_state import (
    PLANNER_VERSION_LOCAL_AI,
    select_planner_version,
    store_local_ai_version,
)
from .planner_sonar_activity import (
    finish_planner_sonar_error,
    finish_planner_sonar_success,
    start_local_ai_review_sonar,
)
from .split_formatting import format_split_plan

__all__ = ["start_comprehensive_local_ai_review_for_window"]


def start_comprehensive_local_ai_review_for_window(
    window: object,
    report: object,
    plan: object,
    proposals: list[object],
    *,
    refresh_callback: Callable[[object], None],
) -> None:
    """Run split, ambiguity, and docstring review in one background worker."""

    if bool(getattr(window, "_large_file_refactor_ai_review_running", False)):
        return
    request_id = object()
    result_queue: queue.Queue[
        tuple[object, ComprehensiveLocalAIReviewResult]
    ] = queue.Queue(maxsize=1)
    window._large_file_refactor_ai_review_running = True
    window._large_file_refactor_ai_review_request_id = request_id
    window._large_file_refactor_ai_review_queue = result_queue
    start_local_ai_review_sonar(window)
    refresh_callback(window)

    def worker() -> None:
        result = review_and_refine_planning_with_local_ai(
            report,
            plan,
            proposals,
        )
        try:
            result_queue.put_nowait((request_id, result))
        except queue.Full:
            pass

    thread = threading.Thread(
        target=worker,
        name="kanda-large-file-comprehensive-local-ai-review",
        daemon=True,
    )
    window._large_file_refactor_ai_review_thread = thread
    timer = QTimer()
    timer.setInterval(200)
    window._large_file_refactor_ai_review_timer = timer

    def poll() -> None:
        try:
            returned_id, result = result_queue.get_nowait()
        except queue.Empty:
            return
        if returned_id is not getattr(
            window,
            "_large_file_refactor_ai_review_request_id",
            None,
        ):
            return
        timer.stop()
        window._large_file_refactor_ai_review_running = False
        _apply_result(window, result)
        if result.status == "blocked":
            finish_planner_sonar_error(window, result.status)
        else:
            finish_planner_sonar_success(window, result.status)
        refresh_callback(window)

    timer.timeout.connect(poll)
    thread.start()
    timer.start()


def _apply_result(
    window: object,
    result: ComprehensiveLocalAIReviewResult,
) -> None:
    """Apply one completed bounded review to Planner memory only."""

    store_local_ai_version(
        window,
        result.plan,
        list(result.docstring_proposals),
    )
    select_planner_version(window, PLANNER_VERSION_LOCAL_AI)
    refresh_planner_version_selector(window)
    window._large_file_refactor_plan_ai_review_result = result
    window._large_file_refactor_web_ai_proposal = None
    window._large_file_refactor_web_ai_proposal_applied = False
    render_selected_planner_version(window)
    window._large_file_refactor_plan_output.appendPlainText(
        "\n\n" + format_comprehensive_local_ai_review(result)
    )
    window._large_file_refactor_planner_state = (
        PlannerState.BLOCKED.value
        if result.plan.status == "blocked"
        else PlannerState.LLM_REVIEW_READY.value
    )
