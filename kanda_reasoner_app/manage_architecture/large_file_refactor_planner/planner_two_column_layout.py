"""Two-column layout helper for the Large File Refactor Planner GUI."""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QWidget

__all__ = ["build_planner_two_column_splitter"]


def build_planner_two_column_splitter(
    left_sections: Sequence[Any],
    right_sections: Sequence[Any],
) -> QSplitter:
    """Return a resizable two-column splitter containing Planner sections."""
    splitter = QSplitter(Qt.Horizontal)
    splitter.setChildrenCollapsible(False)

    left_widget = QWidget()
    left_layout = QVBoxLayout(left_widget)
    left_layout.setContentsMargins(0, 0, 0, 0)
    left_layout.setSpacing(8)
    for index, section in enumerate(left_sections):
        stretch = 2 if index == 0 else 1
        left_layout.addWidget(section, stretch)

    right_widget = QWidget()
    right_layout = QVBoxLayout(right_widget)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(8)
    for index, section in enumerate(right_sections):
        stretch = 2 if index == 0 else 0
        right_layout.addWidget(section, stretch)

    splitter.addWidget(left_widget)
    splitter.addWidget(right_widget)
    splitter.setStretchFactor(0, 1)
    splitter.setStretchFactor(1, 1)
    splitter.setSizes([720, 720])
    return splitter
