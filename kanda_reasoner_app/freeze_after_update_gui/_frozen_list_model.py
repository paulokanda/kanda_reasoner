# project-path: kanda_reasoner_app/freeze_after_update_gui/_frozen_list_model.py
"""Virtualized table model for the List Frozen floating window."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor

__all__ = ["FrozenEntryTableModel"]

_ACTIVE_COLOR = QColor("#008000")
_DEPRECATED_COLOR = QColor("#B00020")
_HEADERS = ("#", "Status", "Date", "Feature", "Freeze ID", "Primary Box")


class FrozenEntryTableModel(QAbstractTableModel):
    """Expose frozen-entry summaries without creating thousands of widgets."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._entries: list[dict[str, Any]] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        """Return the number of frozen entries."""
        return 0 if parent.isValid() else len(self._entries)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        """Return the fixed display-column count."""
        return 0 if parent.isValid() else len(_HEADERS)

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """Return horizontal column labels and vertical row numbers."""
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal and 0 <= section < len(_HEADERS):
            return _HEADERS[section]
        if orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        return None

    def data(  # noqa: N802
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """Return display, color, path, and tooltip data for one cell."""
        if not index.isValid() or not 0 <= index.row() < len(self._entries):
            return None
        entry = self._entries[index.row()]
        active = bool(entry.get("active"))
        if role == Qt.ItemDataRole.ForegroundRole:
            return _ACTIVE_COLOR if active else _DEPRECATED_COLOR
        if role == Qt.ItemDataRole.UserRole:
            return str(entry.get("path") or "")
        if role == Qt.ItemDataRole.ToolTipRole and entry.get("error"):
            return str(entry.get("error"))
        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() in {0, 1, 2}:
            return Qt.AlignmentFlag.AlignCenter
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        values = (
            str(index.row() + 1),
            "Active" if active else "Deprecated",
            str(entry.get("date") or ""),
            str(entry.get("feature_title") or ""),
            str(entry.get("freeze_id") or ""),
            str(entry.get("box") or ""),
        )
        return values[index.column()]

    def replace_entries(self, entries: list[dict[str, Any]]) -> None:
        """Atomically replace the visible newest-first entry snapshot."""
        self.beginResetModel()
        self._entries = list(entries)
        self.endResetModel()

    def entry_at(self, row: int) -> dict[str, Any] | None:
        """Return one entry snapshot by row."""
        if 0 <= row < len(self._entries):
            return self._entries[row]
        return None

    def entries(self) -> list[dict[str, Any]]:
        """Return a shallow copy of the current entry snapshot."""
        return list(self._entries)
