# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui_layout.py
"""Compact layout helpers for the Large File Refactor Workbench GUI."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QLabel,
    QPlainTextEdit,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

__all__ = [
    "build_scrollable_workbench_content",
    "compact_workbench_text_outputs",
]

_OUTPUT_MAX_HEIGHT = 96
_OUTPUT_MIN_HEIGHT = 54


def build_scrollable_workbench_content() -> tuple[QScrollArea, QWidget, QVBoxLayout]:
    """Return a scroll area plus its owned content widget and layout.

    The caller must add the returned QScrollArea itself to the page layout.
    The scroll container ignores its content width hint so long Workbench text
    cannot force the host GUI to grow horizontally when Architecture Review is
    opened. Vertical scrolling remains available for the full workflow.
    """
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setMinimumHeight(0)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
    scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    content = QWidget(scroll)
    content.setMinimumWidth(0)
    content.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum)
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(8)
    scroll.setWidget(content)
    return scroll, content, content_layout


def compact_workbench_text_outputs(root: QWidget) -> None:
    """Keep Workbench output and label hints from resizing the host GUI."""
    for output in root.findChildren(QPlainTextEdit):
        output.setMinimumHeight(_OUTPUT_MIN_HEIGHT)
        output.setMaximumHeight(_OUTPUT_MAX_HEIGHT)
        output.setMinimumWidth(0)
        output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    for label in root.findChildren(QLabel):
        label.setWordWrap(True)
        label.setMinimumWidth(0)
        label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
