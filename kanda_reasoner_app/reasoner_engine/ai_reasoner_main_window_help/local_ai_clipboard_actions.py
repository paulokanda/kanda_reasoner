"""Wire text clipboard buttons for the canonical Local AI conversation."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.reasoner_engine.chat_clipboard_actions import (
    copy_editor_text,
    copy_text,
    paste_clipboard_into,
)

__all__ = ["connect_local_ai_clipboard_actions"]


def _notify(window: Any, message: str) -> None:
    """Show brief local-only clipboard feedback."""
    window.statusBar().showMessage(message, 2200)


def _selected_question(window: Any) -> str:
    """Return the question for the selected memory turn."""
    row = window.history_list.currentRow()
    turns = window.memory.turns()
    if 0 <= row < len(turns):
        return str(turns[row].question)
    return ""


def _refresh_primary_action(window: Any) -> None:
    """Recompute the canonical Ask gate after programmatic editor changes."""
    refresh = getattr(window, "_refresh_workflow_controls", None)
    if callable(refresh):
        refresh()


def _paste_question(window: Any) -> None:
    if paste_clipboard_into(window.question_edit):
        _refresh_primary_action(window)
        _notify(window, "Clipboard pasted into the Local AI question.")


def _copy_draft(window: Any) -> None:
    if copy_editor_text(window.question_edit):
        _notify(window, "Local AI question copied.")


def _copy_selected_question(window: Any) -> None:
    if copy_text(_selected_question(window)):
        _notify(window, "Selected Local AI question copied.")


def _copy_answer(window: Any) -> None:
    if copy_editor_text(window.answer_box):
        _notify(window, "Local AI answer copied.")


def _refresh_state(window: Any) -> None:
    window.copy_draft_button.setEnabled(bool(window.question_edit.text()))
    window.copy_history_question_button.setEnabled(bool(_selected_question(window)))
    window.copy_answer_button.setEnabled(bool(window.answer_box.toPlainText()))


def connect_local_ai_clipboard_actions(window: Any) -> None:
    """Connect Paste/Copy without changing Local AI runtime ownership."""
    window.paste_question_button.clicked.connect(
        lambda _checked=False: _paste_question(window)
    )
    window.copy_draft_button.clicked.connect(
        lambda _checked=False: _copy_draft(window)
    )
    window.copy_history_question_button.clicked.connect(
        lambda _checked=False: _copy_selected_question(window)
    )
    window.copy_answer_button.clicked.connect(
        lambda _checked=False: _copy_answer(window)
    )
    window.question_edit.textChanged.connect(lambda _text: _refresh_state(window))
    window.answer_box.textChanged.connect(lambda: _refresh_state(window))
    window.history_list.currentItemChanged.connect(
        lambda _current, _previous: _refresh_state(window)
    )
    _refresh_state(window)
