# project-path: kanda_reasoner_app/prompt_library_gui/group_window.py
"""Floating read-only windows for one Prompt Library group."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .group_catalog import PromptGroup, build_group_stack_text
from .library_catalog import PromptLibraryItem


class PromptGroupWindow(QWidget):
    """Read-only floating prompt browser filtered to one group."""

    def __init__(
        self,
        group: PromptGroup,
        items: list[PromptLibraryItem],
        library_root: Path,
    ) -> None:
        """Create a floating window for a prompt group.

        Args:
            group: Group descriptor shown by this window.
            items: Prompt items belonging to the group.
            library_root: Prompt library root for status display.
        """
        super().__init__()
        self.group = group
        self.items = items
        self.library_root = library_root
        self.setWindowTitle("Prompt Library - " + group.display_name)
        self.resize(1050, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        header = QLabel("Prompt Library - " + group.display_name)
        header.setStyleSheet("font-weight: bold; font-size: 15px;")
        layout.addWidget(header)

        description = QLabel(group.description)
        description.setWordWrap(True)
        layout.addWidget(description)

        action_row = QHBoxLayout()
        self.copy_selected_button = QPushButton("Copy Selected Prompt")
        self.copy_selected_button.clicked.connect(self.copy_selected_prompt)
        action_row.addWidget(self.copy_selected_button)

        self.copy_stack_button = QPushButton("Copy Full Group Stack")
        self.copy_stack_button.clicked.connect(self.copy_full_group_stack)
        action_row.addWidget(self.copy_stack_button)

        self.open_button = QPushButton("Open File Location")
        self.open_button.clicked.connect(self.open_selected_location)
        action_row.addWidget(self.open_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        action_row.addWidget(self.close_button)
        action_row.addStretch(1)
        layout.addLayout(action_row)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter, 1)

        self.prompt_list = QListWidget()
        self.prompt_list.currentItemChanged.connect(self._on_selection_changed)
        splitter.addWidget(self.prompt_list)

        detail_host = QWidget()
        detail_layout = QVBoxLayout(detail_host)
        detail_layout.setContentsMargins(8, 0, 0, 0)
        detail_layout.setSpacing(8)

        self.metadata_view = QTextEdit()
        self.metadata_view.setReadOnly(True)
        self.metadata_view.setMinimumHeight(170)
        detail_layout.addWidget(self.metadata_view, 0)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        detail_layout.addWidget(self.preview, 1)
        splitter.addWidget(detail_host)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self._populate_items()

    def _populate_items(self) -> None:
        """Load this group's items into the window list."""
        self.prompt_list.clear()
        for item in self.items:
            list_item = QListWidgetItem(item.title)
            list_item.setData(Qt.UserRole, item)
            self.prompt_list.addItem(list_item)

        if self.items:
            self.prompt_list.setCurrentRow(0)
            self.status_label.setText(
                "Loaded "
                + str(len(self.items))
                + " prompts for group: "
                + self.group.display_name
            )
        else:
            self.metadata_view.setPlainText("No matching prompts found for this group.")
            self.preview.setPlainText("")
            self.status_label.setText(
                "No prompt files matched group prompt_ids in " + str(self.library_root)
            )

    def selected_item(self) -> PromptLibraryItem | None:
        """Return the currently selected prompt item, if one is selected."""
        list_item = self.prompt_list.currentItem()
        if list_item is None:
            return None
        value = list_item.data(Qt.UserRole)
        if isinstance(value, PromptLibraryItem):
            return value
        return None

    def copy_selected_prompt(self) -> None:
        """Copy the selected prompt text to the system clipboard."""
        item = self.selected_item()
        if item is None:
            return
        QApplication.clipboard().setText(item.path.read_text(encoding="utf-8", errors="replace"))
        self.status_label.setText("Copied prompt text: " + item.relative_path)

    def copy_full_group_stack(self) -> None:
        """Copy all prompts in this group in group-defined order."""
        if not self.items:
            self.status_label.setText("No group prompts available to copy.")
            return
        QApplication.clipboard().setText(build_group_stack_text(self.group, self.items))
        self.status_label.setText("Copied full group stack: " + self.group.display_name)

    def open_selected_location(self) -> None:
        """Open the selected prompt file location in the OS file browser."""
        item = self.selected_item()
        if item is None:
            return
        folder = item.path.parent
        if not folder.exists():
            QMessageBox.warning(self, "Folder not found", str(folder))
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def _on_selection_changed(self, current: QListWidgetItem | None, _previous) -> None:
        """Update detail panes when the selected prompt changes."""
        if current is None:
            return
        item = current.data(Qt.UserRole)
        if not isinstance(item, PromptLibraryItem):
            return
        self.metadata_view.setPlainText(self._format_metadata(item))
        self.preview.setPlainText(item.path.read_text(encoding="utf-8", errors="replace"))

    def _format_metadata(self, item: PromptLibraryItem) -> str:
        """Return a plain-text metadata summary for a group prompt."""
        lines = [
            "Group: " + self.group.display_name,
            "Title: " + item.title,
            "Category: " + item.category,
            "Relative path: " + item.relative_path,
        ]
        if item.metadata_path is not None:
            lines.append("Metadata: " + item.metadata_path.name)
        else:
            lines.append("Metadata: none")

        for key in ("prompt_id", "version", "status", "load_type", "project_agnostic"):
            value = item.metadata.get(key)
            if value is not None:
                lines.append(str(key) + ": " + str(value))

        explainer = item.metadata.get("explainer")
        if isinstance(explainer, str) and explainer.strip():
            lines.extend(["", "Explainer:", explainer.strip()])

        how_it_works = item.metadata.get("how_it_works")
        if isinstance(how_it_works, str) and how_it_works.strip():
            lines.extend(["", "How it works:", how_it_works.strip()])

        return "\n".join(lines)
