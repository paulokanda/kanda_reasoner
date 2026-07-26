# project-path: kanda_reasoner_app/manage_workflows/ai_review/_gui_row_adapter.py
"""Private widget adapter for Tab 2 AI review GUI rows."""

from __future__ import annotations

from typing import Any


class _QWidgetLikeRow:
    """Small QWidget wrapper imported lazily to keep tests easy."""

    def __new__(cls, row_layout: Any) -> Any:
        """Return a QWidget containing the supplied row layout."""
        from PySide6.QtWidgets import QWidget

        widget = QWidget()
        widget.setLayout(row_layout)
        return widget
