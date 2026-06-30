# project-path: kanda_reasoner_app/templates/floating_windows/__init__.py
"""Floating window helpers."""

from __future__ import annotations

from .auto_close_action_window import (
    AutoCloseActionFloatingWindow,
    show_auto_close_action_window,
)
from .clipboard_message_window import (
    CopyMessageFloatingWindow,
    show_copy_message_window,
)
from .error_copy_close_window import (
    ErrorCopyCloseFloatingWindow,
    show_error_copy_close_window,
)
from .float_window import HoverFloatingWindowController, attach_floating_window

__all__ = [
    "AutoCloseActionFloatingWindow",
    "CopyMessageFloatingWindow",
    "ErrorCopyCloseFloatingWindow",
    "HoverFloatingWindowController",
    "attach_floating_window",
    "show_auto_close_action_window",
    "show_copy_message_window",
    "show_error_copy_close_window",
]
