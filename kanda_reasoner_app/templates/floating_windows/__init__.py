"""Floating window helpers."""

from __future__ import annotations

from .auto_close_action_window import (
    AutoCloseActionFloatingWindow,
    show_auto_close_action_window,
)
from .error_copy_close_window import (
    ErrorCopyCloseFloatingWindow,
    show_error_copy_close_window,
)
from .float_window import HoverFloatingWindowController, attach_floating_window

__all__ = [
    "AutoCloseActionFloatingWindow",
    "ErrorCopyCloseFloatingWindow",
    "HoverFloatingWindowController",
    "attach_floating_window",
    "show_auto_close_action_window",
    "show_error_copy_close_window",
]
