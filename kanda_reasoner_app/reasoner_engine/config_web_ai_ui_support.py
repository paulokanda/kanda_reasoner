# project-path: kanda_reasoner_app/reasoner_engine/config_web_ai_ui_support.py
"""Shared visual helpers for remote Web AI configuration tabs."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QComboBox

__all__ = ["configure_opaque_combo"]


def configure_opaque_combo(combo: QComboBox) -> None:
    """Force a durable opaque popup while preserving the light control."""
    combo.setAutoFillBackground(True)
    combo_palette = combo.palette()
    combo_palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    combo_palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    combo_palette.setColor(QPalette.ColorRole.Text, QColor("#1f2933"))
    combo.setPalette(combo_palette)

    popup = combo.view()
    viewport = popup.viewport()
    popup.setStyleSheet(
        "QAbstractItemView {"
        "background-color: #1d2128;"
        "color: #f4f6f8;"
        "border: 1px solid #3d4552;"
        "outline: 0;"
        "selection-background-color: #2f4f48;"
        "selection-color: #ffffff;"
        "}"
    )
    viewport.setStyleSheet("background-color: #1d2128;")

    for surface in (popup, viewport):
        surface.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        surface.setAutoFillBackground(True)
        palette = surface.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#1d2128"))
        palette.setColor(QPalette.ColorRole.Window, QColor("#1d2128"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#f4f6f8"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#2f4f48"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        surface.setPalette(palette)
