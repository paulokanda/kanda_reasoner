# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_background_cancel.py
"""Cancel Planner background work without changing version preference state."""

from __future__ import annotations

from collections.abc import Callable

from .planner_sonar_activity import finish_planner_sonar_error

__all__ = ["cancel_planner_background_work"]


def cancel_planner_background_work(
    window: object,
    *,
    refresh_callback: Callable[[object], None] | None = None,
    user_visible: bool = False,
) -> bool:
    """Cancel active split-plan or Local AI polling and reject late results.

    Python worker threads may already be inside deterministic computation or a
    blocking local-model request. This controller stops GUI polling, invalidates
    request ownership, clears the running state, and guarantees that any late
    result cannot be applied to the current Planner card.
    """

    cancelled: list[str] = []
    if _cancel_operation(
        window,
        running_attr="_large_file_refactor_split_plan_running",
        request_attr="_large_file_refactor_split_plan_request_id",
        timer_attr="_large_file_refactor_split_plan_timer",
    ):
        cancelled.append("split-plan generation")
    if _cancel_operation(
        window,
        running_attr="_large_file_refactor_ai_review_running",
        request_attr="_large_file_refactor_ai_review_request_id",
        timer_attr="_large_file_refactor_ai_review_timer",
    ):
        cancelled.append("Local AI review")

    if not cancelled:
        return False

    if user_visible:
        message = "Canceled " + " and ".join(cancelled) + ". Late results will be ignored."
        finish_planner_sonar_error(window, message)
        _append_cancel_message(window, message)

    if refresh_callback is not None:
        refresh_callback(window)
    return True


def _cancel_operation(
    window: object,
    *,
    running_attr: str,
    request_attr: str,
    timer_attr: str,
) -> bool:
    """Stop one polling owner and invalidate its current request token."""

    running = bool(getattr(window, running_attr, False))
    request_id = getattr(window, request_attr, None)
    timer = getattr(window, timer_attr, None)
    if not running and request_id is None:
        return False
    if timer is not None and hasattr(timer, "stop"):
        timer.stop()
    setattr(window, request_attr, None)
    setattr(window, running_attr, False)
    return True


def _append_cancel_message(window: object, message: str) -> None:
    """Append bounded cancellation feedback without replacing an existing plan."""

    output = getattr(window, "_large_file_refactor_plan_output", None)
    if output is not None and hasattr(output, "appendPlainText"):
        output.appendPlainText("\n\nCANCELED: " + message)
    status_bar_method = getattr(window, "statusBar", None)
    if callable(status_bar_method):
        status_bar = status_bar_method()
        if status_bar is not None and hasattr(status_bar, "showMessage"):
            status_bar.showMessage(message)
