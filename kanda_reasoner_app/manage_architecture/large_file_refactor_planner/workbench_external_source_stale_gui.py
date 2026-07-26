# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_external_source_stale_gui.py
"""Project stale external-source mutation state onto Workbench completion controls."""

from __future__ import annotations

from .workbench_external_source_stale_state import (
    EXTERNAL_SOURCE_STALE_MESSAGE,
    STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
    sync_external_source_stale_state_from_window,
)

__all__ = [
    "sync_completion_external_source_stale_state",
]


def sync_completion_external_source_stale_state(window: object) -> bool:
    """Refresh stale state, disable completion flow, and render recovery guidance."""
    state = sync_external_source_stale_state_from_window(window)
    if not state.stale:
        return False

    _disable_completion_controls(window)
    _render_completion_status(window, state)
    _render_transaction_summary(window)
    _render_refactor_gate(window, state)
    return True


def _disable_completion_controls(window: object) -> None:
    """Disable stale completion actions without changing project source."""
    attributes = (
        "_large_file_refactor_workbench_completion_prepare_button",
        "_large_file_refactor_workbench_transaction_prepare_button",
        "_large_file_refactor_workbench_semantic_review_check",
        "_large_file_refactor_workbench_warning_ack_check",
        "_large_file_refactor_workbench_transaction_confirm_check",
        "_large_file_refactor_workbench_refactor_large_module_button",
        "_large_file_refactor_workbench_transaction_rollback_button",
        "_large_file_refactor_workbench_ai_exchange_copy_button",
        "_large_file_refactor_workbench_ai_return_import_button",
    )
    for attribute in attributes:
        widget = getattr(window, attribute, None)
        if widget is not None:
            widget.setEnabled(False)


def _render_completion_status(window: object, state: object) -> None:
    """Show the explicit stale state and exact source-drift evidence."""
    output = getattr(
        window,
        "_large_file_refactor_workbench_completion_status_output",
        None,
    )
    if output is None:
        return

    lines = [
        STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
        "",
        EXTERNAL_SOURCE_STALE_MESSAGE,
    ]
    blockers = tuple(getattr(state, "blockers", ()) or ())
    if blockers:
        lines.extend(["", "Detected drift:"])
        lines.extend("- " + item for item in blockers)
    lines.extend(
        [
            "",
            "Safety action:",
            "The prepared Workbench transaction was invalidated without "
            "changing project source.",
            "The queued mutation request was cancelled when it was still "
            "safe to cancel.",
            "Rollback is unavailable because this Workbench transaction did "
            "not apply the external source changes.",
        ]
    )
    output.setPlainText("\n".join(lines))


def _render_transaction_summary(window: object) -> None:
    """Replace stale transaction summary text with read-only invalidation status."""
    output = getattr(
        window,
        "_large_file_refactor_workbench_transaction_summary_output",
        None,
    )
    if output is None:
        return
    output.setPlainText(
        "Transaction Summary\n"
        "===================\n"
        "status: "
        + STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        + "\n"
        "The previous prepared transaction is retained as read-only evidence.\n"
        "Create a fresh pipeline from the current project source."
    )


def _render_refactor_gate(window: object, state: object) -> None:
    """Render one explicit fail-closed gate for stale external source mutation."""
    output = getattr(
        window,
        "_large_file_refactor_workbench_refactor_gate_output",
        None,
    )
    if output is None:
        return

    lines = [
        "Refactor Large Module Gate",
        "==========================",
        "status: blocked",
        "enabled: false",
        "",
        "Blockers:",
        "- " + STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
    ]
    blockers = tuple(getattr(state, "blockers", ()) or ())
    lines.extend("- " + item for item in blockers)
    lines.extend(
        [
            "",
            EXTERNAL_SOURCE_STALE_MESSAGE,
            "",
            "No project source mutation was performed by this invalidation.",
        ]
    )
    output.setPlainText("\n".join(lines))
