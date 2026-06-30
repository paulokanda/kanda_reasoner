# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab_help/list_actions.py
"""List editing actions for the ignore-rules tab."""

from __future__ import annotations

__all__ = [
    "IgnoreRulesListActionsMixin",
]

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QInputDialog, QListWidget, QMessageBox


class IgnoreRulesListActionsMixin:
    """Provide folder, file, and extension list actions."""

    def _browse_folder(self) -> str | None:
        """Browse for a folder and return the selected folder name."""
        last_path = self._get_last_browse_path()
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select folder to ignore",
            last_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if not folder_path:
            return None
        self._set_last_browse_path(folder_path)
        return Path(folder_path).name

    def _browse_file(self) -> str | None:
        """Browse for a file and return the selected file name."""
        last_path = self._get_last_browse_path()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file to ignore",
            last_path,
            "Python files (*.py);;All files (*.*)",
        )
        if not file_path:
            return None
        self._set_last_browse_path(str(Path(file_path).parent))
        return Path(file_path).name

    def _add_item(self, list_widget: QListWidget, title: str, category: str) -> None:
        """Add one text item to a list and save rules."""
        text, ok = QInputDialog.getText(self, f"Add {title}", f"Enter {title}:")
        if ok and text.strip():
            item_text = text.strip()
            if list_widget.findItems(item_text, Qt.MatchExactly):
                QMessageBox.warning(
                    self,
                    "Duplicate",
                    f"'{item_text}' already exists.",
                )
                return
            list_widget.addItem(item_text)
            self._save_rules()

    def _edit_item(self, list_widget: QListWidget, title: str, category: str) -> None:
        """Edit the selected list item and save rules."""
        current = list_widget.currentItem()
        if not current:
            QMessageBox.warning(self, "No selection", "Select an item to edit.")
            return
        old = current.text()
        new, ok = QInputDialog.getText(self, f"Edit {title}", f"Edit {title}:", text=old)
        if ok and new.strip():
            new_text = new.strip()
            if new_text != old and list_widget.findItems(new_text, Qt.MatchExactly):
                QMessageBox.warning(
                    self,
                    "Duplicate",
                    f"'{new_text}' already exists.",
                )
                return
            current.setText(new_text)
            self._save_rules()

    def _remove_item(self, list_widget: QListWidget, category: str) -> None:
        """Remove the selected list item and save rules."""
        current = list_widget.currentItem()
        if current:
            row = list_widget.row(current)
            list_widget.takeItem(row)
            self._save_rules()

    def _clear_list(self, list_widget: QListWidget, category: str) -> None:
        """Clear all items from a list after confirmation."""
        if list_widget.count() == 0:
            return
        reply = QMessageBox.question(
            self,
            "Clear list",
            "Remove all items from this list?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            list_widget.clear()
            self._save_rules()

    def _add_folder(self):
        """Add a folder ignore rule selected through a browse dialog."""
        folder_name = self._browse_folder()
        if folder_name:
            if self.folder_list.findItems(folder_name, Qt.MatchExactly):
                QMessageBox.warning(
                    self,
                    "Duplicate",
                    f"'{folder_name}' already exists.",
                )
                return
            self.folder_list.addItem(folder_name)
            self._save_rules()

    def _edit_folder(self):
        """Edit the selected folder rule."""
        self._edit_item(self.folder_list, "folder name", "folders")

    def _remove_folder(self):
        """Remove the selected folder rule."""
        self._remove_item(self.folder_list, "folders")

    def _add_file(self):
        """Add a file ignore rule selected through a browse dialog."""
        file_name = self._browse_file()
        if file_name:
            if self.file_list.findItems(file_name, Qt.MatchExactly):
                QMessageBox.warning(
                    self,
                    "Duplicate",
                    f"'{file_name}' already exists.",
                )
                return
            self.file_list.addItem(file_name)
            self._save_rules()

    def _edit_file(self):
        """Edit the selected file rule."""
        self._edit_item(self.file_list, "file name/pattern", "files")

    def _remove_file(self):
        """Remove the selected file rule."""
        self._remove_item(self.file_list, "files")

    def _add_extension(self):
        """Add an extension ignore rule."""
        self._add_item(self.ext_list, "extension (e.g., .pyc)", "extensions")

    def _edit_extension(self):
        """Edit the selected extension rule."""
        self._edit_item(self.ext_list, "extension", "extensions")

    def _remove_extension(self):
        """Remove the selected extension rule."""
        self._remove_item(self.ext_list, "extensions")

    def _populate_list(self, list_widget: QListWidget, items: list[str]) -> None:
        """Replace list contents with the provided items."""
        list_widget.clear()
        for item in items:
            list_widget.addItem(item)
