# project-path: kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py
"""Copy-and-close error floating window helper.

This module provides the error-message variant imported by
``kanda_reasoner_app.templates.floating_windows``. It delegates UI mechanics
to the generic copy message template so callers get one safe action:
Copy and Close.
"""

from __future__ import annotations

from typing import Any

from .clipboard_message_window import CopyMessageFloatingWindow, show_copy_message_window

__all__ = [
    "ErrorCopyCloseFloatingWindow",
    "show_error_copy_close_window",
]


ErrorCopyCloseFloatingWindow = CopyMessageFloatingWindow


def show_error_copy_close_window(
    parent: Any | None,
    *,
    title: str,
    message: str,
    detail_text: str = "",
    clipboard_text: str | None = None,
    button_text: str = "Copy and Close",
    modal: bool = True,
) -> ErrorCopyCloseFloatingWindow:
    """Show an error window with one Copy and Close action.

    The copied text defaults to the visible message and detail text. Callers
    may provide a richer ``clipboard_text`` when the user should copy a full
    correction request instead of only the visible summary.
    """
    return show_copy_message_window(
        parent,
        title=title,
        message=message,
        detail_text=detail_text,
        clipboard_text=clipboard_text,
        button_text=button_text,
        modal=modal,
    )
