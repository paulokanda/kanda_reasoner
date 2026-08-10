"""Shared clipboard operations for Local AI and Project Web AI chat surfaces."""

from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QApplication

__all__ = ["copy_editor_text", "copy_text", "paste_clipboard_into"]


def _clipboard():
    """Return the active Qt clipboard."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("A QApplication is required for clipboard actions.")
    return app.clipboard()


def _editor_text(editor: Any) -> str:
    """Return exact visible text from a supported Qt editor."""
    if hasattr(editor, "toPlainText"):
        return str(editor.toPlainText())
    if hasattr(editor, "text"):
        return str(editor.text())
    return ""


def copy_text(text: str) -> bool:
    """Copy non-empty text without persistence or logging."""
    value = str(text or "")
    if not value:
        return False
    _clipboard().setText(value)
    return True


def copy_editor_text(editor: Any) -> bool:
    """Copy the exact current editor text."""
    return copy_text(_editor_text(editor))


def paste_clipboard_into(editor: Any) -> bool:
    """Insert clipboard text at the current question-editor cursor."""
    value = _clipboard().text()
    if not value:
        return False
    if hasattr(editor, "insertPlainText"):
        editor.insertPlainText(value)
    elif hasattr(editor, "insert"):
        editor.insert(value)
    else:
        return False
    editor.setFocus()
    return True
