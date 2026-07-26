# project-path: kanda_reasoner_app/error_memory_gui/_receive_import.py
"""Receive/import dialog helpers for the Error Memory tab.

This private helper owns loading formatted AI lesson text from paste dialogs and
file imports into the public ErrorMemoryTab facade. Qt imports stay local so
helper import smoke remains headless-safe, and this module never imports the
origin facade upward.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.intake import ERROR_LESSON_JSON_BEGIN, ERROR_LESSON_JSON_END

__all__ = [
    "import_error_lesson_zip",
    "load_formatted_lesson_into_tab",
    "receive_formulary_from_ai",
]


def load_formatted_lesson_into_tab(tab: Any, formatted_text: str, lesson: dict[str, Any]) -> None:
    """Load one parsed lesson into intake/editor surfaces without saving it."""
    tab._selected_lesson_id = str(lesson.get('lesson_id', ''))
    tab._last_received_lesson = lesson
    tab._loaded_pending_intake_file = ''
    tab._loaded_pending_intake_lesson_id = ''
    tab.raw_error_edit.setPlainText(formatted_text)
    tab.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))


def receive_formulary_from_ai(tab: Any) -> None:
    """Open the paste dialog and load one formatted AI lesson into the editors."""
    from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QPlainTextEdit, QVBoxLayout
    from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window, show_error_copy_close_window

    receive_dialog = QDialog(tab)
    receive_dialog.setWindowTitle('Paste formatted Error Memory lesson from AI')
    receive_dialog.resize(860, 640)
    layout = QVBoxLayout(receive_dialog)
    help_label = QLabel(f'Paste the AI answer here. Required format is one JSON object between {ERROR_LESSON_JSON_BEGIN} and {ERROR_LESSON_JSON_END}, or one valid Error Memory lesson JSON object. Applying loads it into the AI-assisted intake window and Error Editor. It is not saved until Memorize Error. Short plain-text lesson notes are also accepted as draft lessons, but formatted JSON is preferred.')
    help_label.setWordWrap(True)
    layout.addWidget(help_label)
    response_edit = QPlainTextEdit()
    response_edit.setPlaceholderText('Paste AI formatted Error Memory JSON here. Required: KANDA_ERROR_LESSON_JSON_BEGIN / END block or one valid lesson JSON object.')
    layout.addWidget(response_edit, 1)
    button_row = QHBoxLayout()
    apply_button = QPushButton('Load into Error Editor')
    cancel_button = QPushButton('Cancel')
    button_row.addStretch(1)
    button_row.addWidget(apply_button)
    button_row.addWidget(cancel_button)
    layout.addLayout(button_row)

    def apply_ai_lesson() -> None:
        formatted_text = response_edit.toPlainText().strip()
        if not formatted_text:
            QMessageBox.warning(receive_dialog, 'Error Memory', 'Paste one formatted Error Memory lesson from AI first.')
            return
        try:
            lesson = tab._lesson_from_formatted_text(formatted_text)
        except Exception as exc:
            show_error_copy_close_window(receive_dialog, title='Could not load formatted AI lesson', message=f'The AI answer could not be parsed. Ask AI to return exactly one valid JSON object between {ERROR_LESSON_JSON_BEGIN} and {ERROR_LESSON_JSON_END}, with no markdown and no prose.\n\nError: {exc}')
            return
        load_formatted_lesson_into_tab(tab, formatted_text, lesson)
        show_auto_close_action_window(receive_dialog, title='Error Memory', message='Loaded formatted AI lesson into the intake window and Error Editor.', detail_text='Review or edit it, then click Memorize Error to save it into Lessons.', on_close=receive_dialog.close)

    apply_button.clicked.connect(apply_ai_lesson)
    cancel_button.clicked.connect(receive_dialog.close)
    receive_dialog.show()
    receive_dialog.raise_()
    receive_dialog.activateWindow()


def import_error_lesson_zip(tab: Any) -> None:
    """Import one AI-created formatted Error Lesson ZIP/JSON/TXT/MD into editors."""
    from PySide6.QtWidgets import QFileDialog, QMessageBox
    from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

    root = tab._current_project_root()
    drive_root = Path(root.anchor or str(root)).resolve(strict=False)
    daily_work = drive_root / (root.name + '_delete_after_daily_work')
    start_folder = daily_work if daily_work.exists() else drive_root
    selected, _filter = QFileDialog.getOpenFileName(tab, 'Select AI-created formatted Error Lesson ZIP/JSON', str(start_folder), 'Error Memory files (*.zip *.json *.txt *.md);;All files (*.*)')
    if not selected:
        return
    formatted_text = tab._formatted_import_text_for_window(selected)
    if not formatted_text:
        QMessageBox.warning(tab, 'Formatted lesson required', 'Import Error Lesson ZIP accepts only a KANDA_ERROR_LESSON_JSON block or one valid lesson JSON object created for Error Memory. The file was not loaded or memorized. Ask AI for a formatted Error Memory lesson ZIP.')
        return
    try:
        lesson = tab._lesson_from_formatted_text(formatted_text)
    except Exception as exc:
        show_error_copy_close_window(tab, title='Error Memory import failed', message=str(exc))
        return
    load_formatted_lesson_into_tab(tab, formatted_text, lesson)
    tab._show_action_done('Error Memory import', 'Loaded formatted Error Memory lesson into the AI-assisted intake and Error Editor.', 'It was not saved yet. Review or edit it, then click Memorize Error to save it into Lessons.')
