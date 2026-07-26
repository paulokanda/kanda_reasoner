# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_settings_panel_presentation.py
"""Planner-local compact presentation rules for the one-row Settings group."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QSizePolicy

__all__ = ["apply_settings_panel_presentation"]


def apply_settings_panel_presentation(
    settings_box: QGroupBox,
    settings_row: QHBoxLayout,
) -> None:
    """Keep the single-row Settings group at its natural vertical height."""

    settings_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    settings_row.setContentsMargins(8, 4, 8, 4)
    settings_row.setSpacing(6)
    settings_row.setAlignment(Qt.AlignVCenter)
