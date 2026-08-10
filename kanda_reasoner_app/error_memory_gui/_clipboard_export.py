# project-path: kanda_reasoner_app/error_memory_gui/_clipboard_export.py
"""Clipboard and export action helpers for the Error Memory tab.

This private helper owns clipboard payload delivery, action notifications, and
complete Error Memory export orchestration for the public tab facade.  It does
not import ``error_memory_tab`` and keeps PySide imports local so helper import
smoke remains headless-safe.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.editor_clipboard import (
    extract_error_editor_text_for_ai,
)
from kanda_reasoner_app.error_memory.exporter import (
    build_complete_error_memory_ai_clipboard_json,
    write_complete_error_memory_ai_clipboard_export,
)
from kanda_reasoner_app.error_memory_gui._intake_blueprint import (
    read_error_memory_ai_formulary_canon,
    read_send_zip_errors_prompt,
)

__all__ = [
    "copy_ai_assisted_intake_error_draft_to_clipboard",
    "copy_complete_error_memory_json_to_clipboard",
    "copy_correct_error_delivery_canon_to_clipboard",
    "copy_send_zip_errors_prompt_to_clipboard",
    "copy_error_draft_to_clipboard",
    "copy_error_lesson_intake_blueprint_to_clipboard",
    "copy_path_to_clipboard",
    "export_for_ai",
    "show_action_done",
    "show_active_ready_failure_copy_window",
]


def copy_correct_error_delivery_canon_to_clipboard(tab: Any) -> None:
    """Copy the canonical Error Memory delivery prompt to the clipboard."""
    QApplication = _application()
    try:
        prompt_text = read_error_memory_ai_formulary_canon(
            tab._current_project_root(),
            module_file=__file__,
        )
        QApplication.clipboard().setText(
            prompt_text,
            mode=_clipboard_mode(),
        )
    except Exception as exc:
        _show_error(
            tab,
            title="Error Memory delivery canon copy failed",
            message=str(exc),
        )
        return
    tab._show_action_done(
        "Error Memory",
        "Correct Error Memory delivery canon copied to clipboard.",
        "Source: error_memory_ai_formulary_startup_canon.md",
    )


def copy_send_zip_errors_prompt_to_clipboard(tab: Any) -> None:
    """Copy the generalized self-contained Error Memory ZIP prompt."""
    QApplication = _application()
    try:
        prompt_text = read_send_zip_errors_prompt(
            tab._current_project_root(),
            module_file=__file__,
        )
        QApplication.clipboard().setText(prompt_text, mode=_clipboard_mode())
    except Exception as exc:
        _show_error(
            tab,
            title="Send Zip Errors prompt copy failed",
            message=str(exc),
        )
        return
    tab._show_action_done(
        "Error Memory",
        "Send Zip Errors prompt copied to clipboard.",
        "Source: self_contained_error_memory_lesson_intake_zip.md",
    )


def _application():
    """Support application behavior.
    """
    
    from PySide6.QtWidgets import QApplication

    return QApplication


def _clipboard_mode():
    """Support clipboard mode behavior.
    """
    
    from PySide6.QtGui import QClipboard

    return QClipboard.Mode.Clipboard


def _message_box():
    """Support message box behavior.
    """
    
    from PySide6.QtWidgets import QMessageBox

    return QMessageBox


def _timer():
    """Support timer behavior.
    """
    
    from PySide6.QtCore import QTimer

    return QTimer


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


def show_action_done(tab: Any, title: str, message: str, detail_text: str = '') -> None:
    """Show a silent auto-closing post-action notification."""
    from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window

    show_auto_close_action_window(tab, title=title, message=message, detail_text=detail_text)


def copy_complete_error_memory_json_to_clipboard(text: str) -> None:
    """Copy complete Error Memory JSON to the system clipboard.

    This helper deliberately never accepts paths. The export button uses it so
    second_prompt_files paths cannot overwrite the intended payload.
    """
    QApplication = _application()
    clipboard_mode = _clipboard_mode()
    payload = str(text or '')
    stripped = payload.strip()
    if not stripped.startswith('{'):
        raise ValueError('Complete Error Memory export did not produce JSON text.')
    if stripped.endswith('second_prompt_files') or '\n' not in payload:
        raise ValueError('Complete Error Memory export clipboard payload looks like a path, not JSON.')
    clipboard = QApplication.clipboard()
    clipboard.clear(mode=clipboard_mode)
    clipboard.setText(payload, mode=clipboard_mode)
    QApplication.processEvents()
    if clipboard.text(mode=clipboard_mode) != payload:
        clipboard.setText(payload, mode=clipboard_mode)
        QApplication.processEvents()


def copy_path_to_clipboard(tab: Any, path: Path, label: str) -> None:
    """Copy a resolved path and show the standard Error Memory action message."""
    QApplication = _application()
    QApplication.clipboard().setText(str(path))
    tab._show_action_done('Error Memory', label + ' path copied to clipboard.', str(path))


def copy_error_lesson_intake_blueprint_to_clipboard(tab: Any) -> None:
    """Copy active-ready Error Lesson Intake instructions and templates."""
    QApplication = _application()
    QMessageBox = _message_box()
    try:
        clipboard_text = tab._error_lesson_intake_blueprint_clipboard_text(context_text='')
        QApplication.clipboard().setText(clipboard_text, mode=_clipboard_mode())
    except Exception as exc:
        _show_error(tab, title='Error Lesson Intake blueprint copy failed', message=str(exc))
        return
    QMessageBox.information(tab, 'Error Lesson Intake blueprint copied', 'The active-ready Error Memory AI intake instructions and templates were copied. Paste them to AI when asking it to create text for the AI-assisted error lesson intake window.')


def show_active_ready_failure_copy_window(tab: Any, *, source_label: str, lesson: dict[str, Any]) -> None:
    """Show the active-ready failure popup with copyable AI correction context."""
    missing_text = tab._active_ready_missing_text(lesson)
    context_text = (
        'SOURCE WINDOW: ' + str(source_label or 'Error Memory') + '\n\n'
        'The lesson below is NOT active-ready and must be corrected without inventing evidence.\n\n'
        'Missing active-ready items:\n- ' + missing_text + '\n\n'
        'Current lesson JSON:\n' + tab._lesson_json_text_for_windows(lesson)
    )
    try:
        copy_text = tab._error_lesson_intake_blueprint_clipboard_text(context_text=context_text)
    except Exception:
        copy_text = context_text
    message = (
        'This lesson is not active-ready yet. Copy the correction request below and send it to AI, then paste the corrected marker-wrapped lesson back into the AI-assisted intake window.\n\n'
        'Missing active-ready items:\n- ' + missing_text
    )
    from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

    show_error_copy_close_window(
        tab,
        title='Lesson needs AI correction before Memorize Error',
        message=message,
        clipboard_text=copy_text,
    )


def _copy_error_text_only(tab: Any, text: str, *, empty_title: str) -> None:
    """Copy only the current meaningful error text to the system clipboard."""
    QMessageBox = _message_box()
    clipboard_text = extract_error_editor_text_for_ai(text)
    if not clipboard_text:
        QMessageBox.warning(
            tab,
            empty_title,
            'There is no error text to copy. Load, paste, import, or select one error first.',
        )
        return
    QApplication = _application()
    clipboard = QApplication.clipboard()
    mode = _clipboard_mode()
    clipboard.clear(mode=mode)
    clipboard.setText(clipboard_text, mode=mode)
    QApplication.processEvents()


def copy_ai_assisted_intake_error_draft_to_clipboard(tab: Any) -> None:
    """Copy only the AI-assisted intake error text to the clipboard."""
    _copy_error_text_only(
        tab,
        tab.raw_error_edit.toPlainText(),
        empty_title='AI-assisted intake is empty',
    )


def copy_error_draft_to_clipboard(tab: Any) -> None:
    """Copy only the current Error Editor error text to the clipboard."""
    _copy_error_text_only(
        tab,
        tab.received_preview_edit.toPlainText(),
        empty_title='Error Editor is empty',
    )


def export_for_ai(tab: Any) -> None:
    """Write and copy the complete Error Memory JSON payload for AI."""
    QTimer = _timer()
    root = tab._current_project_root()
    try:
        result = write_complete_error_memory_ai_clipboard_export(root, include_inactive=True)
        clipboard_text = str(result.get('complete_clipboard_json') or '')
        if not clipboard_text:
            clipboard_text = build_complete_error_memory_ai_clipboard_json(root, include_inactive=True)
        tab._copy_complete_error_memory_json_to_clipboard(clipboard_text)
    except Exception as exc:
        _show_error(tab, title='Error Memory export failed', message=str(exc))
        return
    complete_json_path = str(result.get('complete_json', ''))
    lesson_count = str(result.get('complete_json_lesson_count', '0'))
    tab.received_preview_edit.setPlainText(clipboard_text)
    cursor = tab.received_preview_edit.textCursor()
    cursor.movePosition(cursor.MoveOperation.Start)
    tab.received_preview_edit.setTextCursor(cursor)
    tab._show_action_done(
        'Error Memory complete JSON copied',
        'Complete Error Memory JSON was copied to the clipboard for manual AI transfer.',
        'Lessons copied: ' + lesson_count + '\n\nA backup JSON copy was written to:\n' + complete_json_path + '\n\nThe same JSON is also visible in Error Editor as a fallback copy source.',
    )
    tab._copy_complete_error_memory_json_to_clipboard(clipboard_text)
    QTimer.singleShot(250, lambda text=clipboard_text: tab._copy_complete_error_memory_json_to_clipboard(text))
    QTimer.singleShot(1000, lambda text=clipboard_text: tab._copy_complete_error_memory_json_to_clipboard(text))
