"""Animated Tab 1 activity indicator for deterministic and AI work."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["Tab1ActivityIndicator", "install_tab1_activity_indicator"]


_COLOR_STEPS = (
    ("#7C3AED", "#C084FC"),
    ("#2563EB", "#60A5FA"),
    ("#0891B2", "#67E8F9"),
    ("#16A34A", "#86EFAC"),
    ("#F59E0B", "#FDE68A"),
    ("#DC2626", "#FCA5A5"),
)


_HIDE_AFTER_FINISH_MS = 2200


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


class Tab1ActivityIndicator:
    """Colorful status widget shown only while Tab 1 background work runs."""

    def __init__(self) -> None:
        self._step_index = 0
        self._frame = QFrame()
        self._frame.setObjectName("tab1ActivityIndicator")
        self._frame.setMinimumWidth(300)

        self._label = QLabel("")
        self._label.setObjectName("tab1ActivityLabel")
        self._label.setMinimumWidth(190)

        self._bar = QProgressBar()
        self._bar.setObjectName("tab1ActivityBar")
        self._bar.setMinimumWidth(120)
        self._bar.setMaximumWidth(220)
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

    def start_heuristic(self, mode: str) -> None:
        """Show that deterministic heuristic work is running."""
        label = "Heuristic running: " + str(mode or "validate")
        self._start(label)

    def start_ai_review(self, model_name: str = "") -> None:
        """Show that advisory AI review is running."""
        model = str(model_name or "auto model").strip()
        self._start("AI review running: " + model)

    def finish_success(self, message: str) -> None:
        """Show a brief success state, then hide the idle widget."""
        self._stop("Done: " + str(message or "work finished"), "#166534", "#86EFAC")

    def finish_error(self, message: str) -> None:
        """Show a brief error state, then hide the idle widget."""
        self._stop("Needs review: " + str(message or "work finished"), "#991B1B", "#FCA5A5")

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
            "QFrame#tab1ActivityIndicator {"
            "border: 1px solid " + dark_color + ";"
            "border-radius: 10px;"
            "background: " + light_color + ";"
            "}"
            "QLabel#tab1ActivityLabel {"
            "color: " + dark_color + ";"
            "font-weight: bold;"
            "}"
            "QProgressBar#tab1ActivityBar {"
            "border: 1px solid " + dark_color + ";"
            "border-radius: 6px;"
            "background: #F8FAFC;"
            "}"
            "QProgressBar#tab1ActivityBar::chunk {"
            "border-radius: 6px;"
            "background: " + dark_color + ";"
            "}"
        )


def install_tab1_activity_indicator(window: Any, buttons_layout: Any) -> Tab1ActivityIndicator:
    """Install and return the Tab 1 animated activity indicator."""
    indicator = Tab1ActivityIndicator()
    window._tab1_activity_indicator = indicator
    buttons_layout.addWidget(indicator.widget(), alignment=Qt.AlignRight)
    return indicator
