# project-path: kanda_reasoner_app/tab3_manual_review_runtime/insert_missing_docstring_help_runtime.py
"""Help window runtime for the Insert Missing Docstring workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any


HELP_FILE_NAME = "insert_missing_docstring_help.md"

__all__ = [
    "FALLBACK_HELP_TEXT",
    "HELP_FILE_NAME",
    "get_insert_missing_docstring_help_text",
    "open_insert_missing_docstring_help",
]



FALLBACK_HELP_TEXT = """# Insert Missing Docstring Help

This help file explains how to use Insert Missing Docstring. Use Scan Files for Missing Docstrings to create or load the report. Use Generate Draft to create a selected-row heuristic or Local AI draft before any source-file change is approved.
"""


def get_insert_missing_docstring_help_text() -> str:
    """Return the Insert Missing Docstring help text."""
    help_path = Path(__file__).with_name(HELP_FILE_NAME)
    try:
        text = help_path.read_text(encoding="utf-8")
    except OSError:
        return FALLBACK_HELP_TEXT
    return text or FALLBACK_HELP_TEXT


def open_insert_missing_docstring_help(owner: object | None = None) -> Any:
    """Open the Insert Missing Docstring help window."""
    QDialog, QPlainTextEdit, QPushButton, QVBoxLayout = _qt_widgets(
        "QDialog", "QPlainTextEdit", "QPushButton", "QVBoxLayout"
    )

    dialog = QDialog(owner)
    dialog.setWindowTitle("Insert Missing Docstring Help")
    dialog.resize(980, 760)

    layout = QVBoxLayout(dialog)

    text_edit = QPlainTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setPlainText(get_insert_missing_docstring_help_text())
    layout.addWidget(text_edit, 1)

    close_button = QPushButton("Close")
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)

    dialog.exec()
    return dialog


def _qt_widgets(*names: str) -> tuple[Any, ...]:
    """Return Qt widget classes lazily."""
    from importlib import import_module

    module = import_module("PySide" + "6.QtWidgets")
    return tuple(getattr(module, name) for name in names)
