"""Reusable delayed floating window helpers for Qt widgets."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "HoverFloatingWindowController",
    "attach_floating_window",
]


def _qt_core_attr(name: str) -> Any:
    """Return a PySide6.QtCore attribute."""
    return getattr(import_module("PySide6.QtCore"), name)


def _qt_gui_attr(name: str) -> Any:
    """Return a PySide6.QtGui attribute."""
    return getattr(import_module("PySide6.QtGui"), name)


def _qt_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWidgets attribute."""
    return getattr(import_module("PySide6.QtWidgets"), name)


_QObject = _qt_core_attr("QObject")
_QEvent = _qt_core_attr("QEvent")
_QPoint = _qt_core_attr("QPoint")
_QTimer = _qt_core_attr("QTimer")
_Qt = _qt_core_attr("Qt")
_QCursor = _qt_gui_attr("QCursor")
_QFrame = _qt_widgets_attr("QFrame")
_QLabel = _qt_widgets_attr("QLabel")
_QVBoxLayout = _qt_widgets_attr("QVBoxLayout")


def _event_type(name: str) -> Any:
    """Return a Qt event type across PySide6 enum variants."""
    enum_group = getattr(_QEvent, "Type", None)
    if enum_group is not None:
        return getattr(enum_group, name)
    return getattr(_QEvent, name)


class HoverFloatingWindowController(_QObject):
    """Show a small floating message after hovering over a widget."""

    def __init__(
        self,
        target_widget: Any,
        *,
        trigger_word: str,
        message: str,
        delay_ms: int = 4000,
    ) -> None:
        super().__init__(target_widget)
        self._target_widget = target_widget
        self._trigger_word = trigger_word
        self._message = message
        self._delay_ms = delay_ms
        self._popup = None

        self._enter_event = _event_type("Enter")
        self._leave_event = _event_type("Leave")
        self._mouse_move_event = _event_type("MouseMove")

        self._timer = _QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._show_popup)

        self._target_widget.setMouseTracking(True)
        self._target_widget.installEventFilter(self)

    def eventFilter(self, watched: Any, event: Any) -> bool:
        """Track hover state and show the popup only after a pause."""
        if watched is not self._target_widget:
            return False

        event_type = event.type()
        if event_type == self._enter_event:
            self._restart_timer()
        elif event_type == self._mouse_move_event:
            if self._popup is not None and self._popup.isVisible():
                self._popup.hide()
            self._restart_timer()
        elif event_type == self._leave_event:
            self._timer.stop()
            self.hide()

        return False

    def _restart_timer(self) -> None:
        """Restart the delayed display timer."""
        self._timer.stop()
        self._timer.start(self._delay_ms)

    def _build_popup(self) -> Any:
        """Build the floating popup widget."""
        popup = _QFrame()
        popup.setWindowFlags(_Qt.ToolTip | _Qt.FramelessWindowHint)
        popup.setFrameShape(_QFrame.StyledPanel)
        popup.setStyleSheet(
            "QFrame {"
            " background-color: #fffff0;"
            " border: 1px solid #6fa8dc;"
            " border-radius: 6px;"
            "}"
            "QLabel {"
            " color: #111111;"
            " padding: 8px 10px;"
            "}"
        )

        layout = _QVBoxLayout(popup)
        layout.setContentsMargins(0, 0, 0, 0)

        label = _QLabel(self._message)
        label.setWordWrap(True)
        label.setMinimumWidth(360)
        label.setMaximumWidth(620)
        label.setTextInteractionFlags(_Qt.TextSelectableByMouse)

        layout.addWidget(label)
        return popup

    def _show_popup(self) -> None:
        """Show the floating popup near the cursor."""
        if not self._target_widget.isVisible():
            return

        if self._popup is None:
            self._popup = self._build_popup()

        cursor_pos = _QCursor.pos()
        self._popup.move(cursor_pos + _QPoint(16, 18))
        self._popup.show()
        self._popup.raise_()

    def hide(self) -> None:
        """Hide the popup when it is visible."""
        if self._popup is not None:
            self._popup.hide()


def attach_floating_window(
    target_widget: Any,
    *,
    trigger_word: str,
    message: str,
    delay_ms: int = 4000,
) -> HoverFloatingWindowController:
    """Attach a delayed floating message to a widget."""
    return HoverFloatingWindowController(
        target_widget,
        trigger_word=trigger_word,
        message=message,
        delay_ms=delay_ms,
    )
