# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/_docstring_ai_header_runtime.py
"""Docstring Assistant active-engine badge and AI-control presentation."""

from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QGraphicsOpacityEffect,
    QGroupBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

__all__ = ["bind_embedded_docstring_widget", "install_docstring_header_surface"]

_STATUS_STYLES = {
    "Heuristic Activated": ("#8A5A00", "#FFF4D6", "#D7A72E"),
    "Local AI Activated": ("#0B7A32", "#E5F6EB", "#55A96F"),
    "Web AI Activated": ("#0057B8", "#E5F0FF", "#5D91D4"),
}


def install_docstring_header_surface(shell: object, outer_layout: QVBoxLayout) -> None:
    """Install the Docstring title row and animated active-engine badge."""
    template = shell.tab_header_template
    header_row = shell.header_row

    badge = QLabel("Heuristic Activated")
    badge.setObjectName("docstring_ai_activation_status_label")
    badge.setAlignment(Qt.AlignCenter)
    badge.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    badge.setToolTip(
        "Shows the active Docstring drafting engine. AI-disabled mode uses deterministic heuristics."
    )

    title_index = header_row.indexOf(template.title_label)
    if title_index < 0:
        title_index = 0
    header_row.setStretch(title_index, 0)
    header_row.insertWidget(title_index + 1, badge, 0, Qt.AlignVCenter)
    header_row.insertStretch(title_index + 2, 1)
    outer_layout.addLayout(header_row)

    effect = QGraphicsOpacityEffect(badge)
    badge.setGraphicsEffect(effect)
    animation = QPropertyAnimation(effect, b"opacity", shell)
    animation.setDuration(2400)
    animation.setStartValue(1.0)
    animation.setKeyValueAt(0.5, 0.22)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.InOutSine)
    animation.setLoopCount(-1)
    animation.start()

    shell._docstring_ai_status_label = badge
    shell._docstring_ai_status_effect = effect
    shell._docstring_ai_status_animation = animation
    _apply_status(shell, "Heuristic Activated")


def bind_embedded_docstring_widget(shell: object, widget: QWidget) -> None:
    """Keep the mode-only AI group in the left column and sync the badge."""
    group = _find_ai_group(widget)
    if group is not None:
        group.setObjectName("docstring_ai_assistant_left_group")
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        shell._docstring_ai_assistant_left_group = group

    for name in ("_heuristic_radio", "_local_ai_radio", "_web_ai_radio"):
        button = getattr(widget, name, None)
        signal = getattr(button, "toggled", None)
        connect = getattr(signal, "connect", None)
        if callable(connect):
            connect(lambda _checked, s=shell, w=widget: update_activation_status(s, w))

    update_activation_status(shell, widget)


def update_activation_status(shell: object, widget: object) -> None:
    """Synchronize the badge with heuristic, Local AI, or Web AI mode."""
    web = getattr(widget, "_web_ai_radio", None)
    local = getattr(widget, "_local_ai_radio", None)
    web_checked = getattr(web, "isChecked", None)
    local_checked = getattr(local, "isChecked", None)
    if callable(web_checked) and bool(web_checked()):
        _apply_status(shell, "Web AI Activated")
    elif callable(local_checked) and bool(local_checked()):
        _apply_status(shell, "Local AI Activated")
    else:
        _apply_status(shell, "Heuristic Activated")


def _find_ai_group(widget: QWidget) -> QGroupBox | None:
    """Return the existing task-owned AI Assistant group."""
    for group in widget.findChildren(QGroupBox):
        if str(group.title() or "").strip() == "AI Assistant":
            return group
    return None


def _apply_status(shell: object, text: str) -> None:
    """Apply one prominent status text and matching visual treatment."""
    label = getattr(shell, "_docstring_ai_status_label", None)
    if not isinstance(label, QLabel):
        return
    foreground, background, border = _STATUS_STYLES[text]
    label.setText(text)
    label.setStyleSheet(
        "QLabel {"
        f" color: {foreground}; background: {background}; border: 1px solid {border};"
        " border-radius: 6px; padding: 3px 9px; font-weight: 700;"
        "}"
    )
