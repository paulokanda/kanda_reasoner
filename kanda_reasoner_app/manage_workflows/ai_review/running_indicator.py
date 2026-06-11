"""Animated Tab 2 activity indicator for deterministic and AI work."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["Tab2ActivityIndicator", "install_tab2_activity_indicator"]

_COLOR_STEPS = (
    ("#9333EA", "#E9D5FF"),
    ("#2563EB", "#BFDBFE"),
    ("#0891B2", "#A5F3FC"),
    ("#16A34A", "#BBF7D0"),
    ("#EA580C", "#FED7AA"),
)

_HIDE_AFTER_FINISH_MS = 1800


def _qt_core_attr(name: str) -> Any:
    """Return a PySide6.QtCore attribute at GUI import time."""
    return getattr(import_module("PySide6.QtCore"), name)


def _qt_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWidgets attribute at GUI import time."""
    return getattr(import_module("PySide6.QtWidgets"), name)


QFrame = _qt_widgets_attr("QFrame")
QHBoxLayout = _qt_widgets_attr("QHBoxLayout")
QLabel = _qt_widgets_attr("QLabel")
QProgressBar = _qt_widgets_attr("QProgressBar")
QTimer = _qt_core_attr("QTimer")
Qt = _qt_core_attr("Qt")


class Tab2ActivityIndicator:
    """Colorful status widget shown only while Tab 2 background work runs."""

    def __init__(self) -> None:
        self._step_index = 0
        self._frame = QFrame()
        self._frame.setObjectName("tab2ActivityIndicator")
        self._frame.setMinimumWidth(320)

        self._label = QLabel("")
        self._label.setObjectName("tab2ActivityLabel")
        self._label.setMinimumWidth(205)

        self._bar = QProgressBar()
        self._bar.setObjectName("tab2ActivityBar")
        self._bar.setMinimumWidth(120)
        self._bar.setMaximumWidth(230)
        self._bar.setTextVisible(False)
        self._bar.setRange(0, 1)
        self._bar.setValue(0)

        layout = QHBoxLayout(self._frame)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        layout.addWidget(self._label)
        layout.addWidget(self._bar)

        self._timer = QTimer()
        self._timer.setInterval(220)
        self._timer.timeout.connect(self._advance_animation)
        self._apply_idle_style()
        self.set_idle()

    def widget(self) -> Any:
        """Return the Qt widget that should be inserted in the layout."""
        return self._frame

    def start_deterministic(self, mode: str) -> None:
        """Show that deterministic Tab 2 work is running."""
        self._start("Deterministic running: " + str(mode or "validate"))

    def start_ai_review(self, label: str) -> None:
        """Show that advisory AI review is running."""
        self._start("AI review running: " + str(label or "local model"))

    def finish_success(self, message: str) -> None:
        """Show a brief success state, then hide the idle widget."""
        self._stop("Done: " + str(message or "work finished"), "#166534", "#BBF7D0")

    def finish_error(self, message: str) -> None:
        """Show a brief error state, then hide the idle widget."""
        self._stop("Needs review: " + str(message or "work finished"), "#991B1B", "#FECACA")

    def set_idle(self) -> None:
        """Return the widget to a hidden idle state."""
        if self._timer.isActive():
            self._timer.stop()
        self._label.setText("")
        self._bar.setRange(0, 1)
        self._bar.setValue(0)
        self._bar.setVisible(False)
        self._frame.setVisible(False)
        self._apply_idle_style()

    def _start(self, label: str) -> None:
        """Start the activity animation with a label."""
        self._frame.setVisible(True)
        self._bar.setVisible(True)
        self._label.setText(label)
        self._bar.setRange(0, 0)
        self._advance_animation()
        if not self._timer.isActive():
            self._timer.start()

    def _stop(self, label: str, dark_color: str, light_color: str) -> None:
        """Stop animation and apply a final state style briefly."""
        if self._timer.isActive():
            self._timer.stop()
        self._frame.setVisible(True)
        self._bar.setVisible(True)
        self._label.setText(label)
        self._bar.setRange(0, 1)
        self._bar.setValue(1)
        self._apply_style(dark_color, light_color)
        self._hide_after_finish()

    def _hide_after_finish(self) -> None:
        """Hide the activity widget after users can see the final state."""
        single_shot = getattr(QTimer, "singleShot", None)
        if callable(single_shot):
            single_shot(_HIDE_AFTER_FINISH_MS, self.set_idle)
            return
        self.set_idle()

    def _advance_animation(self) -> None:
        """Advance the color pulse for the activity bar."""
        dark, light = _COLOR_STEPS[self._step_index % len(_COLOR_STEPS)]
        self._step_index += 1
        self._apply_style(dark, light)

    def _apply_idle_style(self) -> None:
        """Apply the quiet idle style used before hiding the widget."""
        self._apply_style("#334155", "#CBD5E1")

    def _apply_style(self, dark_color: str, light_color: str) -> None:
        """Apply a colorful but compact stylesheet."""
        self._frame.setStyleSheet(
            "QFrame#tab2ActivityIndicator {"
            "border: 1px solid " + dark_color + ";"
            "border-radius: 10px;"
            "background: " + light_color + ";"
            "}"
            "QLabel#tab2ActivityLabel {"
            "color: " + dark_color + ";"
            "font-weight: bold;"
            "}"
            "QProgressBar#tab2ActivityBar {"
            "border: 1px solid " + dark_color + ";"
            "border-radius: 6px;"
            "background: #F8FAFC;"
            "}"
            "QProgressBar#tab2ActivityBar::chunk {"
            "border-radius: 6px;"
            "background: " + dark_color + ";"
            "}"
        )


def install_tab2_activity_indicator(window: Any, layout: Any) -> Tab2ActivityIndicator:
    """Install and return the Tab 2 animated activity indicator."""
    indicator = Tab2ActivityIndicator()
    window._tab2_activity_indicator = indicator
    layout.addWidget(indicator.widget(), alignment=Qt.AlignRight)
    return indicator
