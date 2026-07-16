"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_reasoner_main_window_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\main_window_help
# PURPOSE       : Reusable UI helpers extracted from ai_reasoner_main_window.py.
# EXPORTS       : shorten_path, CopyableListWidget, HelpDialog
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.project_reasoner_v10.help_index import HELP_INDEX

__all__ = ["shorten_path", "CopyableListWidget", "HelpDialog"]


def shorten_path(path: str, max_len: int = 90) -> str:
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


class CopyableListWidget(QListWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _selected_text(self) -> str:
        items = self.selectedItems()
        if not items:
            current = self.currentItem()
            if current is None:
                return ""
            return current.text()
        return "\n".join(item.text() for item in items)

    def _all_text(self) -> str:
        return "\n".join(self.item(i).text() for i in range(self.count()))

    def copy_selected(self) -> None:
        text = self._selected_text()
        if text:
            QApplication.clipboard().setText(text)

    def copy_all(self) -> None:
        text = self._all_text()
        if text:
            QApplication.clipboard().setText(text)

    def _show_context_menu(self, pos) -> None:
        menu = QMenu(self)

        copy_selected_action = QAction("Copy Selected", self)
        copy_selected_action.triggered.connect(self.copy_selected)
        menu.addAction(copy_selected_action)

        copy_all_action = QAction("Copy All", self)
        copy_all_action.triggered.connect(self.copy_all)
        menu.addAction(copy_all_action)

        menu.exec(self.mapToGlobal(pos))

    def keyPressEvent(self, event) -> None:
        if event.matches(QKeySequence.Copy):
            self.copy_selected()
            event.accept()
            return
        super().keyPressEvent(event)


class HelpDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(str(HELP_INDEX.get("window_title", "Help")))
        self.resize(1100, 800)

        self.section_list = CopyableListWidget()
        self.content_box = QPlainTextEdit()
        self.content_box.setReadOnly(True)

        layout = QHBoxLayout(self)

        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Sections"))
        left_panel.addWidget(self.section_list)

        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Help Content"))
        right_panel.addWidget(self.content_box)

        left_widget = QWidget()
        left_widget.setLayout(left_panel)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([260, 780])

        layout.addWidget(splitter)

        self._populate_sections()
        self.section_list.currentRowChanged.connect(self._show_section)

        if self.section_list.count() > 0:
            self.section_list.setCurrentRow(0)

    def _populate_sections(self) -> None:
        for section in HELP_INDEX.get("sections", []):
            title = str(section.get("title", "Untitled"))
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, section)
            self.section_list.addItem(item)

    def _show_section(self, row: int) -> None:
        item = self.section_list.item(row)
        if item is None:
            self.content_box.clear()
            return

        section = item.data(Qt.UserRole) or {}
        title = str(section.get("title", "Untitled"))
        items = section.get("items", [])

        lines: list[str] = [title, "=" * len(title), ""]
        for entry in items:
            label = str(entry.get("label", "Item"))
            lines.append(label)
            lines.append("-" * len(label))
            for key in (
                "purpose",
                "how_it_works",
                "best_use",
                "best_config",
                "what_it_is_for",
                "notes",
            ):
                value = str(entry.get(key, "")).strip()
                if value:
                    pretty_key = key.replace("_", " ").capitalize()
                    lines.append(pretty_key + ":")
                    lines.append(value)
                    lines.append("")

        self.content_box.setPlainText("\n".join(lines).strip())






