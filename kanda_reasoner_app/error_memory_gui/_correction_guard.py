# project-path: kanda_reasoner_app/error_memory_gui/_correction_guard.py
"""Correction and repeat-guard action helpers for the Error Memory tab.

This private helper owns deterministic lesson correction button behavior and
repeat-guard advisory checks for the public tab facade. It does not import
``error_memory_tab`` and keeps PySide imports local so helper import smoke stays
headless-safe.
"""
from __future__ import annotations

import json
from typing import Any

from kanda_reasoner_app.error_memory.guard import analyze_error_against_lessons
from kanda_reasoner_app.error_memory.heuristic_normalizer import classify_and_normalize_error_lesson_text
from kanda_reasoner_app.error_memory.models import active_ready, active_ready_missing_reasons
from kanda_reasoner_app.error_memory_gui._correction_duplicate_guard import (
    consume_duplicate_correction_candidate,
)

__all__ = [
    "active_ready_missing_text",
    "apply_heuristic_correction_to_error_editor",
    "check_against_lessons",
    "heuristic_correction_result_for_editor",
    "operation_phase_for_guard",
    "refresh_heuristic_correction_button_state",
    "show_repeat_guard_report",
]


def _message_box():
    """Support message box behavior.
    """
    
    from PySide6.QtWidgets import QMessageBox

    return QMessageBox


def _show_error(parent: Any, *, title: str, message: str) -> None:
    """Support show error behavior.
    
    Parameters
    ----------
    parent : Any
        The parent value.
    title : str
        The title value.
    message : str
        The message text.
    """
    
    from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

    show_error_copy_close_window(parent, title=title, message=message)


def active_ready_missing_text(lesson: dict[str, Any], *, limit: int = 20) -> str:
    """Return a readable active-ready missing-field report."""
    reasons = active_ready_missing_reasons(dict(lesson or {}))
    if not reasons:
        return 'None. This lesson is active-ready.'
    shown = reasons[:limit]
    text = '\n- '.join(shown)
    if len(reasons) > limit:
        text += '\n- ... ' + str(len(reasons) - limit) + ' more item(s)'
    return text


def heuristic_correction_result_for_editor(tab: Any):
    """Classify the Error Editor payload for deterministic Level-1 cleanup."""
    return classify_and_normalize_error_lesson_text(
        tab.received_preview_edit.toPlainText(),
        project_slug=tab._current_project_root().name,
    )


def refresh_heuristic_correction_button_state(tab: Any) -> None:
    """Update the heuristic correction button label, color, and lock state."""
    result = tab._heuristic_correction_result_for_editor()
    if result.can_apply and result.level == 1 and isinstance(result.lesson, dict):
        tab.heuristic_correction_button.setText('Heuristic Correction')
        tab.heuristic_correction_button.setEnabled(True)
        tab.heuristic_correction_button.setStyleSheet('QPushButton { color: #187a2f; font-weight: 700; }')
        tab.heuristic_correction_button.setToolTip(result.reason + '\n\nThis payload is active-ready after deterministic normalization.')
        return
    reason = result.reason
    tab.heuristic_correction_button.setText('Need AI to Correct')
    tab.heuristic_correction_button.setEnabled(False)
    tab.heuristic_correction_button.setStyleSheet('QPushButton { color: #b00020; font-weight: 700; } QPushButton:disabled { color: #b00020; font-weight: 700; }')
    tab.heuristic_correction_button.setToolTip(reason)


def apply_heuristic_correction_to_error_editor(tab: Any) -> None:
    """Apply deterministic cleanup only when it creates an active-ready lesson."""
    QMessageBox = _message_box()
    result = tab._heuristic_correction_result_for_editor()
    if not result.can_apply or result.level != 1 or (not isinstance(result.lesson, dict)):
        QMessageBox.warning(tab, 'Need AI to Correct', 'This lesson cannot be corrected deterministically. AI correction or manual review is required.\n\n' + result.reason)
        tab._refresh_heuristic_correction_button_state()
        return
    lesson = dict(result.lesson)
    if consume_duplicate_correction_candidate(
        tab,
        lesson,
        action_label="Heuristic Correction",
    ):
        return
    if not active_ready(dict(lesson)):
        lesson['promotion_status'] = 'needs_ai_review'
        tab._last_received_lesson = lesson
        tab.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))
        tab.raw_error_edit.setPlainText(tab._formatted_lesson_block(lesson))
        tab._refresh_heuristic_correction_button_state()
        QMessageBox.warning(tab, 'Need AI to Correct', result.reason + '\n\nUse Mark Draft only if you want to keep this draft. Use AI correction or manually complete the missing fields before Mark Active or Memorize Error.')
        return
    lesson['promotion_status'] = 'active_ready'
    lesson['status'] = 'active'
    tab._selected_lesson_id = str(lesson.get('lesson_id', ''))
    tab._last_received_lesson = lesson
    tab.raw_error_edit.setPlainText(tab._formatted_lesson_block(lesson))
    tab.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))
    tab._refresh_heuristic_correction_button_state()
    tab._show_action_done('Heuristic Correction', 'Deterministic correction produced an active-ready lesson and set status to active.', 'Review it, then click Memorize Error to save it as active, or Mark Active after review.')


def operation_phase_for_guard(tab: Any, raw_text: str) -> str:
    """Return operation phase for the repeat guard from JSON or text clues."""
    try:
        payload = json.loads(tab.received_preview_edit.toPlainText().strip())
        if isinstance(payload, dict) and str(payload.get('operation_phase', '')).strip():
            return str(payload.get('operation_phase', '')).strip()
    except Exception:
        pass
    lowered = str(raw_text or '').lower()
    if 'install' in lowered or 'installer' in lowered or 'zip not found' in lowered:
        return 'install'
    if 'validation' in lowered or 'pytest' in lowered or 'py_compile' in lowered:
        return 'validation'
    if 'freeze' in lowered:
        return 'freeze_write'
    if 'startup' in lowered:
        return 'startup_sync'
    if 'prompt' in lowered:
        return 'prompt_sync'
    if 'traceback' in lowered or 'exception' in lowered or 'syntaxerror' in lowered:
        return 'runtime'
    return 'unknown'


def check_against_lessons(tab: Any) -> None:
    """Run the advisory repeat guard against current Error Memory text."""
    QMessageBox = _message_box()
    raw_text = tab.received_preview_edit.toPlainText().strip()
    if not raw_text:
        raw_text = tab.raw_error_edit.toPlainText().strip()
    if not raw_text:
        QMessageBox.information(tab, 'Repeat Error Guard', 'Load an error in Error Editor, paste formatted JSON, import an Error Lesson ZIP, or select a lesson first.')
        return
    try:
        report = analyze_error_against_lessons(
            tab._current_project_root(),
            raw_text,
            operation_phase=tab._operation_phase_for_guard(raw_text),
            include_drafts=True,
            include_deprecated=False,
        )
    except Exception as exc:
        _show_error(tab, title='Repeat Error Guard failed', message=str(exc))
        return
    tab._show_repeat_guard_report(report)


def show_repeat_guard_report(tab: Any, report: dict[str, Any]) -> None:
    """Show the repeat guard advisory JSON report."""
    from PySide6.QtWidgets import QDialog, QLabel, QPlainTextEdit, QPushButton, QVBoxLayout

    dialog = QDialog(tab)
    dialog.setWindowTitle('Repeat Error Guard - advisory report')
    layout = QVBoxLayout(dialog)
    label = QLabel('Advisory-only check. This does not hard-block implementation or freeze. Use it to avoid repeating known mistakes.')
    label.setWordWrap(True)
    layout.addWidget(label)
    editor = QPlainTextEdit()
    editor.setReadOnly(True)
    editor.setPlainText(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    layout.addWidget(editor, 1)
    close_button = QPushButton('Close')
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)
    dialog.resize(900, 650)
    dialog.exec()
