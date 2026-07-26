# project-path: kanda_reasoner_app/error_memory_gui/_project_paths_mixin.py
"""Project-root and folder/path controls mixin for the Error Memory tab."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog

from kanda_reasoner_app.error_memory.paths import (
    resolve_project_error_memory_root,
    resolve_second_prompt_files_root,
)
from kanda_reasoner_app.error_memory.store import bootstrap_error_memory_store
from kanda_reasoner_app.error_memory_gui._clipboard_export import copy_path_to_clipboard
from kanda_reasoner_app.error_memory_gui._pending_sources import pending_intake_dirs_for_root_hint
from kanda_reasoner_app.error_memory_gui._project_roots import (
    source_root_from_directory_hint,
    source_root_peer_from_generated_output,
)
from kanda_reasoner_app.error_memory_gui._intake_actions_mixin import (
    PENDING_AI_ASSISTED_INTAKE_DIR_NAME,
)
from kanda_reasoner_app.error_memory_gui._table_view import pending_path_for_row

__all__ = ['ErrorMemoryProjectPathsMixin']


ERROR_MEMORY_PENDING_PATH_ROLE = Qt.UserRole + 2


class ErrorMemoryProjectPathsMixin:
    """Project-root, path refresh, folder opening, and row-path wrappers."""

    def set_project_root(self, project_root: str | Path) -> None:
        """Accept project-root updates from host shells when available."""
        root = self._existing_directory_from_text(str(project_root))
        if root is None:
            return
        self._project_root = root
        root_text = str(root)
        if self.project_root_value_label.text().strip() != root_text:
            self._syncing_project_root_field = True
            try:
                self.project_root_value_label.setText(root_text)
            finally:
                self._syncing_project_root_field = False
        self._refresh_paths()
        QTimer.singleShot(0, self.load_pending_ai_assisted_error_lesson_intake_now)

    def _source_root_peer_from_generated_output(path: Path) -> Path | None:
        """Return the existing source-root peer for a generated output path."""
        return source_root_peer_from_generated_output(path)

    def _source_root_from_directory_hint(cls, path: Path) -> Path | None:
        """Resolve output-folder hints back to a real source project root."""
        return source_root_from_directory_hint(
            path,
            pending_dir_name=PENDING_AI_ASSISTED_INTAKE_DIR_NAME,
        )

    def _on_project_root_field_changed(self, text: str) -> None:
        """Keep the Error Memory internal root in sync with the shell row field."""
        if self._syncing_project_root_field:
            return
        root = self._existing_directory_from_text(text)
        if root is None:
            return
        if root == self._project_root:
            self.load_pending_ai_assisted_error_lesson_intake_now()
            return
        self._project_root = root
        self._refresh_paths()

    def _current_project_root(self) -> Path:
        """Support current project root behavior.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        field = getattr(self, 'project_root_value_label', None)
        if field is not None:
            try:
                text = field.text().strip()
            except Exception:
                text = ''
            root = self._existing_directory_from_text(text)
            if root is not None:
                if root != self._project_root:
                    self._project_root = root
                return root
        return self._project_root

    def _search_project_root(self) -> None:
        """Support search project root behavior.
        """
        
        selected = QFileDialog.getExistingDirectory(self, 'Select project root', str(self._project_root))
        if not selected:
            return
        self.set_project_root(selected)

    def _copy_path_to_clipboard(self, path: Path, label: str) -> None:
        """Support copy path to clipboard behavior.
        
        Parameters
        ----------
        path : Path
            The file or folder path.
        label : str
            The label value.
        """
        
        copy_path_to_clipboard(self, path, label)

    def _refresh_paths(self) -> None:
        """Support refresh paths behavior.
        """
        
        root = self._current_project_root()
        if not root.exists() or not root.is_dir():
            return
        bootstrap_error_memory_store(root)
        self.project_root_value_label.setText(str(root))
        self._reload_table()
        self._load_pending_ai_assisted_error_lesson_intake()

    def _pending_intake_dirs_for_root_hint(self, root_hint: str | Path) -> list[Path]:
        """Return possible pending-intake folders for one root hint."""
        return pending_intake_dirs_for_root_hint(
            root_hint,
            pending_dir_name=PENDING_AI_ASSISTED_INTAKE_DIR_NAME,
        )

    def _pending_path_for_row(self, row: int) -> str:
        """Support pending path for row behavior.
        
        Parameters
        ----------
        row : int
            The row data.
        
        Returns
        -------
        str
            The string result.
        """
        
        return pending_path_for_row(
            self.lessons_table,
            row,
            pending_path_role=ERROR_MEMORY_PENDING_PATH_ROLE,
        )

    def _open_folder(self, path: Path) -> None:
        """Support open folder behavior.
        
        Parameters
        ----------
        path : Path
            The file or folder path.
        """
        
        path.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

