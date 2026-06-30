# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_help.py
"""Private mixin helpers extracted from reasoner_tools_gui_shell.main_window."""

from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTextEdit

from ..app_constants import _HELP_FILENAME, _PROJECT_ROOT

__all__: list[str] = []


class _WindowHelpMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    @staticmethod
    def _help_file_path() -> Path:
        """Support help file path behavior.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        try:
            return _PROJECT_ROOT / _HELP_FILENAME
        except Exception:
            return _PROJECT_ROOT / _HELP_FILENAME

    def _open_help_file(self) -> None:
        """Support open help file behavior.
        """
        
        help_path = self._help_file_path()
        if not help_path.exists():
            QMessageBox.warning(
                self,
                "Help file not found",
                f"Expected help file was not found:\n{help_path}",
            )
            return
        opened = QDesktopServices.openUrl(QUrl.fromLocalFile(str(help_path)))
        if opened:
            return
        try:
            content = help_path.read_text(encoding="utf-8")
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Help file could not be opened",
                f"Failed to open help file:\n{help_path}\n\nDetails: {exc}",
            )
            return
        dialog = QMainWindow(self)
        dialog.setWindowTitle("Reasoner Tools Help")
        dialog.resize(1100, 800)
        editor = QTextEdit(dialog)
        editor.setReadOnly(True)
        editor.setPlainText(content)
        dialog.setCentralWidget(editor)
        dialog.show()
        self._help_dialog = dialog
