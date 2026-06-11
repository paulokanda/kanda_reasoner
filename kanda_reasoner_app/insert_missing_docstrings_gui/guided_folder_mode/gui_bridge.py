
"""GUI bridge primitives for Safe Mode.

This module intentionally avoids importing PySide. It provides a stable,
testable bridge that GUI code can call without coupling Safe Mode core logic
to widgets.
"""

from __future__ import annotations

from dataclasses import dataclass

from .apply_gate import build_folder_apply_gate
from .models import GuidedFolderSession
from .review_state import (
    FolderReviewState,
    accept_docstring,
    clear_decision,
    edit_docstring,
    reject_docstring,
    request_fallback,
    request_regeneration,
    skip_docstring,
)


SAFE_MODE_ACTION_ACCEPT = "accept"
SAFE_MODE_ACTION_EDIT = "edit"
SAFE_MODE_ACTION_REGENERATE = "regenerate"
SAFE_MODE_ACTION_FALLBACK = "fallback"
SAFE_MODE_ACTION_SKIP = "skip"
SAFE_MODE_ACTION_REJECT = "reject"
SAFE_MODE_ACTION_CLEAR = "clear"


@dataclass(frozen=True)
class SafeModeGuiSnapshot:
    """Represent a GUI-ready Safe Mode status snapshot."""

    current_index: int
    total_folders: int
    folder_relative_path: str
    python_file_count: int
    pending_count: int
    accepted_count: int
    skipped_count: int
    rejected_count: int
    can_apply_folder: bool
    can_continue_to_next_folder: bool
    status_message: str


@dataclass(frozen=True)
class SafeModeActionResult:
    """Represent the result of one GUI-triggered Safe Mode action."""

    success: bool
    state: FolderReviewState
    message: str = ""
    error: str = ""


@dataclass(frozen=True)
class SafeModeButtonState:
    """Represent GUI button enablement for one Safe Mode folder."""

    can_apply_folder: bool
    can_continue_to_next_folder: bool
    can_regenerate: bool
    can_fallback: bool
    can_edit: bool
    message: str = ""


def build_safe_mode_gui_snapshot(
    session: GuidedFolderSession,
    review_state: FolderReviewState | None = None,
) -> SafeModeGuiSnapshot:
    """Build a GUI-ready snapshot from session and optional review state."""
    current = session.current_folder()
    folder_relative_path = current.relative_path if current is not None else ""
    python_file_count = len(current.python_files) if current is not None else 0

    pending_count = 0
    accepted_count = 0
    skipped_count = 0
    rejected_count = 0
    can_apply = False

    if review_state is not None:
        pending_count = review_state.unresolved_count()
        accepted_count = len(review_state.accepted_docstrings())
        skipped_count = sum(
            1
            for decision in review_state.decisions.values()
            if decision.decision == "skipped"
        )
        rejected_count = sum(
            1
            for decision in review_state.decisions.values()
            if decision.decision == "rejected"
        )
        can_apply = build_folder_apply_gate(review_state).can_apply()

    can_continue = session.can_continue_to_next_folder()
    status_message = _build_status_message(
        folder_relative_path=folder_relative_path,
        pending_count=pending_count,
        can_apply=can_apply,
        can_continue=can_continue,
    )

    return SafeModeGuiSnapshot(
        current_index=session.current_index,
        total_folders=len(session.folder_queue),
        folder_relative_path=folder_relative_path,
        python_file_count=python_file_count,
        pending_count=pending_count,
        accepted_count=accepted_count,
        skipped_count=skipped_count,
        rejected_count=rejected_count,
        can_apply_folder=can_apply,
        can_continue_to_next_folder=can_continue,
        status_message=status_message,
    )


def perform_safe_mode_review_action(
    state: FolderReviewState,
    row_id: str,
    action: str,
    final_docstring: str = "",
    reason: str = "",
) -> SafeModeActionResult:
    """Apply one GUI review action to a Safe Mode review state."""
    try:
        if action == SAFE_MODE_ACTION_ACCEPT:
            updated = accept_docstring(
                state,
                row_id,
                final_docstring=final_docstring or None,
            )
            return SafeModeActionResult(True, updated, "Docstring accepted.")

        if action == SAFE_MODE_ACTION_EDIT:
            updated = edit_docstring(state, row_id, final_docstring)
            return SafeModeActionResult(True, updated, "Docstring edited.")

        if action == SAFE_MODE_ACTION_REGENERATE:
            updated = request_regeneration(state, row_id, reason or "GUI regeneration requested")
            return SafeModeActionResult(True, updated, "Regeneration requested.")

        if action == SAFE_MODE_ACTION_FALLBACK:
            updated = request_fallback(state, row_id, reason or "GUI fallback requested")
            return SafeModeActionResult(True, updated, "Fallback requested.")

        if action == SAFE_MODE_ACTION_SKIP:
            updated = skip_docstring(state, row_id, reason)
            return SafeModeActionResult(True, updated, "Docstring skipped.")

        if action == SAFE_MODE_ACTION_REJECT:
            updated = reject_docstring(state, row_id, reason or "Rejected in GUI review.")
            return SafeModeActionResult(True, updated, "Docstring rejected.")

        if action == SAFE_MODE_ACTION_CLEAR:
            updated = clear_decision(state, row_id)
            return SafeModeActionResult(True, updated, "Decision cleared.")

        return SafeModeActionResult(
            success=False,
            state=state,
            error=f"Unknown Safe Mode action: {action}",
        )

    except Exception as exc:
        return SafeModeActionResult(
            success=False,
            state=state,
            error=str(exc),
        )


def build_safe_mode_button_state(
    session: GuidedFolderSession,
    review_state: FolderReviewState | None = None,
) -> SafeModeButtonState:
    """Build GUI button enablement state for Safe Mode."""
    can_continue = session.can_continue_to_next_folder()
    if review_state is None:
        return SafeModeButtonState(
            can_apply_folder=False,
            can_continue_to_next_folder=can_continue,
            can_regenerate=False,
            can_fallback=False,
            can_edit=False,
            message="No Safe Mode review state is loaded.",
        )

    apply_gate = build_folder_apply_gate(review_state)
    pending = review_state.unresolved_count()
    has_rows = bool(review_state.rows)

    return SafeModeButtonState(
        can_apply_folder=apply_gate.can_apply(),
        can_continue_to_next_folder=can_continue,
        can_regenerate=has_rows,
        can_fallback=has_rows,
        can_edit=has_rows,
        message=_build_button_message(pending, apply_gate.can_apply()),
    )


def _build_status_message(
    folder_relative_path: str,
    pending_count: int,
    can_apply: bool,
    can_continue: bool,
) -> str:
    if not folder_relative_path:
        return "Safe Mode has no active folder."
    if pending_count:
        return f"Safe Mode folder '{folder_relative_path}' has {pending_count} pending row(s)."
    if can_apply:
        return f"Safe Mode folder '{folder_relative_path}' is ready to apply."
    if can_continue:
        return f"Safe Mode folder '{folder_relative_path}' is resolved."
    return f"Safe Mode folder '{folder_relative_path}' is waiting for review."


def _build_button_message(pending_count: int, can_apply: bool) -> str:
    if pending_count:
        return f"{pending_count} row(s) still need review."
    if can_apply:
        return "Folder can be applied."
    return "Folder has no approved patches to apply."
