# project-path: kanda_reasoner_app/error_memory_gui/_clipboard_export.py
"""Clipboard and export action helpers for the Error Memory tab.

This private helper owns clipboard payload delivery, action notifications, and
complete Error Memory export orchestration for the public tab facade.  It does
not import ``error_memory_tab`` and keeps PySide imports local so helper import
smoke remains headless-safe.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
)
from kanda_reasoner_app.error_memory.editor_clipboard import (
    extract_error_editor_text_for_ai,
)
from kanda_reasoner_app.error_memory.exporter import (
    build_complete_error_memory_ai_clipboard_json,
    write_complete_error_memory_ai_clipboard_export,
)
from kanda_reasoner_app.error_memory.store import list_lessons
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
    "copy_last_saved_lesson_to_clipboard",
    "copy_path_to_clipboard",
    "export_for_ai",
    "show_action_done",
    "show_active_ready_failure_copy_window",
]


def copy_correct_error_delivery_canon_to_clipboard(tab: Any) -> None:
    """Copy the canonical Error Memory delivery prompt to the clipboard."""
    try:
        prompt_text = read_error_memory_ai_formulary_canon(
            tab._current_project_root(),
            module_file=__file__,
        )
        _copy_text_to_clipboard_verified(prompt_text)
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
    """Copy the runtime-safe Error Memory delivery prompt."""
    try:
        prompt_text = read_send_zip_errors_prompt(
            tab._current_project_root(),
            module_file=__file__,
        )
        _copy_text_to_clipboard_verified(prompt_text)
    except Exception as exc:
        _show_error(
            tab,
            title="Error Memory delivery prompt copy failed",
            message=str(exc),
        )
        return
    tab._show_action_done(
        "Error Memory",
        "Runtime-safe Error Memory delivery prompt copied to clipboard.",
        "Source/IDE: ZIP prompt; Portable/FROZEN: native marker intake.",
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


def _copy_text_to_clipboard_verified(text: str) -> None:
    """Copy through the live Qt application and verify exact round-trip."""
    QApplication = _application()
    application = QApplication.instance()
    if application is None:
        raise RuntimeError("A Qt application is required to access the clipboard.")
    payload = str(text or "")
    if not payload.strip():
        raise RuntimeError("Clipboard prompt payload is empty.")
    clipboard = application.clipboard()
    mode = _clipboard_mode()
    clipboard.clear(mode=mode)
    clipboard.setText(payload, mode=mode)
    application.processEvents()
    if clipboard.text(mode=mode) != payload:
        clipboard.setText(payload, mode=mode)
        application.processEvents()
    if clipboard.text(mode=mode) != payload:
        raise RuntimeError("Clipboard verification failed after retry.")


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


def _latest_saved_lesson(lessons: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the newest canonical lesson by saved lesson timestamps."""
    if not lessons:
        return None

    def saved_order(lesson: dict[str, Any]) -> tuple[str, str, str]:
        return (
            str(lesson.get("updated_at_utc") or ""),
            str(lesson.get("created_at_utc") or ""),
            str(lesson.get("lesson_id") or ""),
        )

    return dict(max(lessons, key=saved_order))


def copy_last_saved_lesson_to_clipboard(tab: Any) -> None:
    """Copy exactly one most recently saved canonical lesson to clipboard."""
    try:
        lessons = list_lessons(
            tab._current_project_root(),
            include_inactive=True,
        )
        lesson = _latest_saved_lesson(lessons)
    except Exception as exc:
        _show_error(tab, title="Get Last Lesson failed", message=str(exc))
        return
    if lesson is None:
        _message_box().information(
            tab,
            "Get Last Lesson",
            "There are no saved Error Memory lessons for the active Project.",
        )
        return
    payload = (
        ERROR_LESSON_JSON_BEGIN
        + "\n"
        + json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False)
        + "\n"
        + ERROR_LESSON_JSON_END
    )
    QApplication = _application()
    clipboard = QApplication.clipboard()
    mode = _clipboard_mode()
    clipboard.clear(mode=mode)
    clipboard.setText(payload, mode=mode)
    QApplication.processEvents()
    tab._show_action_done(
        "Error Memory",
        "Last saved lesson copied to clipboard.",
        "Lesson ID: " + str(lesson.get("lesson_id") or ""),
    )


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


def _complete_error_correction_prompt(text: str, *, source_label: str) -> str:
    """Return one self-contained AI correction request with the complete payload.

    This is a clipboard-only delivery helper.  It deliberately does not parse,
    shorten, normalize, save, activate, memorize, delete, or consume Error
    Memory data.  The current window text is preserved verbatim inside the
    correction request so AI receives all available lesson evidence.
    """
    payload = str(text or "")
    if not payload.strip():
        return ""

    return (
        "KANDA ERROR MEMORY - CORRECT COMPLETE ERROR / LESSON\n\n"
        "Task:\n"
        "Review and correct the COMPLETE Error Memory error/lesson supplied below. "
        "Use the entire supplied payload as evidence; do not reduce it to raw_error_text only.\n\n"
        "Critical rules:\n"
        "- Preserve valid existing evidence, lesson identity, technical details, and validation evidence when supported.\n"
        "- Correct incomplete, inconsistent, inaccurate, or non-active-ready fields only when justified by the supplied evidence.\n"
        "- Do not invent failures, root causes, hashes, commands, files, validation results, or facts that are not supported.\n"
        "- Keep Error Memory semantics separate from Machine-Card/MCard semantics.\n"
        "- This request is for human-reviewed correction only. Do not save, memorize, activate, retire, delete, supersede, or consume Error Memory data.\n"
        "- Return exactly ONE complete Error Memory lesson for human review.\n"
        "- The first visible characters of the returned lesson must be KANDA_ERROR_LESSON_JSON_BEGIN.\n"
        "- The last visible characters of the returned lesson must be KANDA_ERROR_LESSON_JSON_END.\n"
        "- Between the markers return one valid JSON object only: no Markdown fence, no comments, no trailing commas.\n"
        "- Active output must retain the complete active-ready metadata required by the Error Memory intake canon. "
        "If evidence is insufficient for active-ready status, return status draft and state what remains unsupported in notes.\n"
        "- Keep raw_error_text and raw_error_snapshot_scrubbed evidence-grounded and export-safe.\n"
        "- Use forward slashes in commands/paths inside JSON where required by the Error Memory intake canon.\n\n"
        "SOURCE WINDOW: " + str(source_label or "Error Memory") + "\n\n"
        "COMPLETE CURRENT ERROR / LESSON TO CORRECT - BEGIN\n"
        + payload
        + ("\n" if not payload.endswith("\n") else "")
        + "COMPLETE CURRENT ERROR / LESSON TO CORRECT - END\n"
    )


def _copy_error_text_only(tab: Any, text: str, *, empty_title: str) -> None:
    """Copy the complete current Error Memory payload plus AI correction request.

    The historical helper name is retained for compatibility with existing GUI
    wiring.  Its corrected contract is complete-payload delivery, not text
    extraction.  Clipboard copy is the only side effect.
    """
    QMessageBox = _message_box()
    payload = str(text or "")
    if not payload.strip():
        QMessageBox.warning(
            tab,
            empty_title,
            'There is no error text to copy. Load, paste, import, or select one error first.',
        )
        return

    source_label = (
        "AI Assisted Error Lesson Intake"
        if getattr(tab, "raw_error_edit", None) is not None
        and text == tab.raw_error_edit.toPlainText()
        else "Error Editor"
    )
    clipboard_text = _complete_error_correction_prompt(
        payload,
        source_label=source_label,
    )

    QApplication = _application()
    clipboard = QApplication.clipboard()
    mode = _clipboard_mode()
    clipboard.clear(mode=mode)
    clipboard.setText(clipboard_text, mode=mode)
    QApplication.processEvents()
    if clipboard.text(mode=mode) != clipboard_text:
        clipboard.setText(clipboard_text, mode=mode)
        QApplication.processEvents()
    if clipboard.text(mode=mode) != clipboard_text:
        raise RuntimeError("Clipboard verification failed after retry.")

    if hasattr(tab, "_show_action_done"):
        tab._show_action_done(
            "Error Memory",
            "Complete error/lesson plus AI correction request copied.",
            "Clipboard only. No Error Memory data was saved, changed, or consumed.",
        )



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
