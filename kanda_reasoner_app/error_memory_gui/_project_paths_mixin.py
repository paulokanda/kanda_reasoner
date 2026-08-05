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
from kanda_reasoner_app.portable_smoke_runtime_report import (
    record_portable_smoke_event,
)
from kanda_reasoner_app.error_memory.backend import ErrorMemoryBackendError
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

    def _current_project_root(self) -> Path | None:
        """Return the selected Project root, or ``None`` when unselected."""
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
        root = self._project_root
        if isinstance(root, Path) and root.exists() and root.is_dir():
            return root
        return None

    def _require_project_root(self) -> Path:
        """Return the selected Project root or raise one actionable error."""
        root = self._current_project_root()
        if root is None:
            raise RuntimeError(
                "No Project selected. Select a Project in the Show Project to AI "
                "tab, then retry this Error Memory action."
            )
        return root

    def _search_project_root(self) -> None:
        """Support search project root behavior.
        """
        
        start = self._project_root if isinstance(self._project_root, Path) else Path.home()
        selected = QFileDialog.getExistingDirectory(self, 'Select project root', str(start))
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

    def _set_project_controls_enabled(self, enabled: bool) -> None:
        """Enable Project-owned actions only when Project authority exists."""
        for name in (
            'open_memory_button',
            'open_second_prompt_button',
            'copy_memory_path_button',
            'copy_second_prompt_path_button',
            'copy_correct_error_delivery_button',
            'send_zip_errors_button',
            'receive_formulary_button',
            'copy_ai_assisted_intake_error_draft_button',
            'delete_draft_button',
            'memorize_error_button',
            'import_zip_button',
            'check_against_lessons_button',
            'save_preview_button',
            'copy_error_draft_button',
            'undo_button',
            'delete_button',
            'export_errors_button',
            'import_errors_button',
            'export_button',
            'mark_draft_button',
            'mark_active_button',
            'deprecate_button',
            'supersede_button',
            'correct_with_ai_button',
        ):
            control = getattr(self, name, None)
            if control is not None:
                control.setEnabled(enabled)

    def _set_project_status(self, message: str, *, error: bool = False) -> None:
        """Show one concise Project-state message inside the tab."""
        label = getattr(self, 'project_selection_status_label', None)
        if label is None:
            return
        label.setText(message)
        label.setStyleSheet(
            "color: #B00020; font-weight: bold; padding: 4px 0;"
            if error
            else "color: #9A6700; font-weight: bold; padding: 4px 0;"
        )
        label.show()

    def _show_no_project_state(self, message: str) -> None:
        """Render a stable empty state instead of raising a lazy-tab traceback."""
        self._project_root = None
        field = getattr(self, 'project_root_value_label', None)
        if field is not None and field.text().strip():
            self._syncing_project_root_field = True
            try:
                field.clear()
            finally:
                self._syncing_project_root_field = False
        self._set_project_status(message, error=False)
        table = getattr(self, 'lessons_table', None)
        if table is not None:
            table.clearContents()
            table.setRowCount(0)
        self._set_project_controls_enabled(False)
        refresh = getattr(self, '_refresh_heuristic_correction_button_state', None)
        if callable(refresh):
            refresh()
        record_portable_smoke_event(
            status="PASS",
            kind="error_memory_state",
            source="no_project",
            message=message,
        )

    def _show_project_error_state(self, exc: Exception) -> None:
        """Keep the tab usable and show an actionable load failure message."""
        self._set_project_controls_enabled(False)
        self._set_project_status(
            "Error Memory could not load the selected Project. Reselect the Project "
            "in Show Project to AI and retry. Details: "
            + type(exc).__name__
            + ": "
            + str(exc),
            error=True,
        )
        record_portable_smoke_event(
            status="FAIL",
            kind="error_memory_state",
            source="selected_project",
            message=type(exc).__name__ + ": " + str(exc),
        )

    def _refresh_paths(self) -> None:
        """Refresh Project Error Memory or show an actionable empty/error state."""
        root = self._current_project_root()
        if root is None or not root.exists() or not root.is_dir():
            self._show_no_project_state(
                "No Project selected. Select a Project in the Show Project to AI "
                "tab. Project Error Memory will load automatically after selection."
            )
            return
        try:
            bootstrap_error_memory_store(root)
            self.project_root_value_label.setText(str(root))
            self._reload_table()
            self._load_pending_ai_assisted_error_lesson_intake()
        except ErrorMemoryBackendError as exc:
            text = str(exc)
            if 'ACTIVE_PROJECT_SELECTION_REQUIRED' in text:
                self._show_no_project_state(
                    "No active registered Project is selected. Select the Project in "
                    "the Show Project to AI tab, then retry Error Memory."
                )
                return
            self._show_project_error_state(exc)
            return
        except Exception as exc:
            self._show_project_error_state(exc)
            return
        label = getattr(self, 'project_selection_status_label', None)
        if label is not None:
            label.hide()
        self._set_project_controls_enabled(True)
        refresh = getattr(self, '_refresh_heuristic_correction_button_state', None)
        if callable(refresh):
            refresh()
        record_portable_smoke_event(
            status="PASS",
            kind="error_memory_state",
            source="selected_project",
            message=str(root),
        )

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

