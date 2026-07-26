# project-path: kanda_reasoner_app/templates/floating_windows/auto_close_action_window.py
"""Template for silent auto-closing action floating windows.

Use this helper for short post-action messages that should not require an
extra click. The window closes by itself after a short delay and can run one
optional close command exactly once when it closes.

This is not a confirmation gate. Use a normal confirmation dialog when a
human must explicitly approve a governed write or destructive action.

Sound policy:
This template is intentionally silent. It avoids native alert dialogs, system
beeps, and message-box information sounds.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any, Callable

CloseCommand = Callable[[], None]
CloseErrorHandler = Callable[[Exception], None]

__all__ = [
    "AutoCloseActionFloatingWindow",
    "show_auto_close_action_window",
]


def _qt_core_attr(name: str) -> Any:
    """Return a PySide6.QtCore attribute."""
    return getattr(import_module("PySide6.QtCore"), name)


def _qt_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWidgets attribute."""
    return getattr(import_module("PySide6.QtWidgets"), name)


_QTimer = _qt_core_attr("QTimer")
_Qt = _qt_core_attr("Qt")
_QDialog = _qt_widgets_attr("QDialog")
_QHBoxLayout = _qt_widgets_attr("QHBoxLayout")
_QLabel = _qt_widgets_attr("QLabel")
_QPushButton = _qt_widgets_attr("QPushButton")
_QSpacerItem = _qt_widgets_attr("QSpacerItem")
_QSizePolicy = _qt_widgets_attr("QSizePolicy")
_QVBoxLayout = _qt_widgets_attr("QVBoxLayout")


def _qt_enum_value(group_name: str, name: str) -> Any:
    """Return a Qt enum value across PySide6 enum variants."""
    enum_group = getattr(_Qt, group_name, None)
    if enum_group is not None:
        return getattr(enum_group, name)
    return getattr(_Qt, name)


class AutoCloseActionFloatingWindow(_QDialog):
    """Small silent floating message window that closes automatically.

    The optional close command is run exactly once, whether the user presses
    the button, the timeout closes the window, or application code closes it.
    """

    def __init__(
        self,
        parent: Any | None = None,
        *,
        title: str,
        message: str,
        detail_text: str = "",
        timeout_ms: int = 3000,
        button_text: str = "OK",
        on_close: CloseCommand | None = None,
        on_close_error: CloseErrorHandler | None = None,
    ) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        parent : Any | None, optional
            The optional parent value.
        title : str
            The title value.
        message : str
            The message text.
        detail_text : str, optional
            The optional detail text value.
        timeout_ms : int, optional
            The optional timeout ms value.
        button_text : str, optional
            The optional button text value.
        on_close : CloseCommand | None, optional
            The optional on close value.
        on_close_error : CloseErrorHandler | None, optional
            The optional on close error value.
        """
        
        super().__init__(parent)
        self._timeout_ms = max(0, int(timeout_ms))
        self._on_close = on_close
        self._on_close_error = on_close_error
        self._close_command_ran = False
        self._finishing_silently = False

        self.setWindowTitle(title)
        self.setWindowFlag(_qt_enum_value("WindowType", "Tool"), True)
        self.setWindowFlag(_qt_enum_value("WindowType", "WindowContextHelpButtonHint"), False)
        self.setAttribute(_qt_enum_value("WidgetAttribute", "WA_DeleteOnClose"), True)
        self.setModal(False)
        self.setMinimumWidth(420)

        self._timer = _QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.close_silently)

        self._build_ui(message=message, detail_text=detail_text, button_text=button_text)

    def _build_ui(self, *, message: str, detail_text: str, button_text: str) -> None:
        """Build the small message body and action row."""
        layout = _QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(10)

        message_label = _QLabel(message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(_qt_enum_value("TextInteractionFlag", "TextSelectableByMouse"))
        layout.addWidget(message_label)

        if detail_text:
            detail_label = _QLabel(detail_text)
            detail_label.setWordWrap(True)
            detail_label.setTextInteractionFlags(_qt_enum_value("TextInteractionFlag", "TextSelectableByMouse"))
            detail_label.setStyleSheet("color: #555555;")
            layout.addWidget(detail_label)

        button_row = _QHBoxLayout()
        button_row.addItem(_QSpacerItem(10, 10, _QSizePolicy.Expanding, _QSizePolicy.Minimum))
        ok_button = _QPushButton(button_text)
        ok_button.setAutoDefault(False)
        ok_button.setDefault(False)
        ok_button.clicked.connect(self.close_silently)
        button_row.addWidget(ok_button)
        layout.addLayout(button_row)

    def showEvent(self, event: Any) -> None:
        """Start the auto-close timer when the window appears."""
        super().showEvent(event)
        if self._timeout_ms:
            self._timer.start(self._timeout_ms)

    def accept(self) -> None:
        """Close silently instead of using a message-box style accept path."""
        self.close_silently(result=1)

    def reject(self) -> None:
        """Close silently instead of using a message-box style reject path."""
        self.close_silently(result=0)

    def done(self, result: int) -> None:
        """Close silently when external code calls QDialog.done."""
        self.close_silently(result=result)

    def closeEvent(self, event: Any) -> None:
        """Run the optional close command for window-manager closes."""
        self._timer.stop()
        super().closeEvent(event)
        self._run_close_command_once()

    def close_silently(self, result: int = 0) -> None:
        """Close without any native alert sound or system beep."""
        if self._finishing_silently:
            return
        self._finishing_silently = True
        self._timer.stop()
        super().done(result)
        self._run_close_command_once()

    def _run_close_command_once(self) -> None:
        """Run the configured close command no more than once."""
        if self._close_command_ran:
            return
        self._close_command_ran = True
        if self._on_close is None:
            return
        try:
            self._on_close()
        except Exception as exc:
            if self._on_close_error is not None:
                self._on_close_error(exc)
                return
            print("Auto-close floating window close command failed: " + str(exc))


def show_auto_close_action_window(
    parent: Any | None,
    *,
    title: str,
    message: str,
    detail_text: str = "",
    timeout_ms: int = 3000,
    button_text: str = "OK",
    on_close: CloseCommand | None = None,
    on_close_error: CloseErrorHandler | None = None,
) -> AutoCloseActionFloatingWindow:
    """Create, show, and return a silent auto-closing action window.

    Keep a reference to the returned dialog if caller code needs to prevent
    early garbage collection in unusual ownership patterns. Normal Qt parent
    ownership is enough when a parent is provided.
    """
    dialog = AutoCloseActionFloatingWindow(
        parent,
        title=title,
        message=message,
        detail_text=detail_text,
        timeout_ms=timeout_ms,
        button_text=button_text,
        on_close=on_close,
        on_close_error=on_close_error,
    )
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()
    return dialog
