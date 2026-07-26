# project-path: kanda_reasoner_app/freeze_after_update_gui/_path_controls.py
"""Project-root and derived-path controls for the Freeze tab."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QMessageBox

from kanda_reasoner_app.freeze_after_update.paths import build_paths

__all__ = ["FreezePathControlsMixin"]


class FreezePathControlsMixin:
    """Project-root selection, derived paths, and folder-opening behavior."""

    def set_project_root(self, project_root: str | Path) -> None:
        """Accept project-root updates from host shells when available."""
        root = Path(project_root).expanduser().resolve(strict=False)
        root_text = str(root)
        if self.project_root_edit.text().strip() != root_text:
            self.project_root_edit.setText(root_text)
        self._refresh_derived_paths()

    def move_project_root_controls_to_layout(self, target_layout: QHBoxLayout, insert_index: int | None = None) -> None:
        """Move freeze Project Root controls into the host header template."""
        if self._project_root_controls_moved:
            return
        controls = [
            self.project_root_header_label,
            self.project_root_edit,
            self.search_project_button,
        ]
        if insert_index is None:
            target_layout.addSpacing(12)
            for control in controls:
                target_layout.addWidget(control, 0)
        else:
            current_index = insert_index
            target_layout.insertSpacing(current_index, 12)
            current_index += 1
            for control in controls:
                target_layout.insertWidget(current_index, control, 0)
                current_index += 1
        self._project_root_controls_moved = True

    def _project_root(self) -> Path | None:
        """Support project root behavior.
        
        Returns
        -------
        Path | None
            The resolved path.
        """
        
        text = self.project_root_edit.text().strip()
        if not text:
            return None
        return Path(text).expanduser()

    def _paths(self):
        """Support paths behavior.
        """
        
        project_root = self._project_root()
        if project_root is None:
            return None
        return build_paths(project_root)

    def _refresh_derived_paths(self) -> None:
        """Support refresh derived paths behavior.
        """
        
        paths = self._paths()
        if paths is None:
            self.box_folder_button.setToolTip("Select a project root before opening the box folder")
            self.external_ai_review_folder_button.setToolTip(
                "Select a project root before opening the external AI review folder"
            )
            return
        self.box_folder_button.setToolTip("Open box folder: " + str(paths.box_root))
        self.external_ai_review_folder_button.setToolTip("Open external AI review folder: " + str(paths.send_root))

    def _choose_project_folder(self) -> None:
        """Support choose project folder behavior.
        """
        
        folder = QFileDialog.getExistingDirectory(self, "Choose Project Folder")
        if folder:
            self.project_root_edit.setText(folder)

    def _require_project_root(self) -> Path | None:
        """Support require project root behavior.
        
        Returns
        -------
        Path | None
            The resolved path.
        """
        
        project_root = self._project_root()
        if project_root is None:
            QMessageBox.warning(self, "Project missing", "Select a project folder first.")
            return None
        return project_root

    def _open_path(self, path: Path | None, label: str) -> None:
        """Support open path behavior.
        
        Parameters
        ----------
        path : Path | None
            The file or folder path.
        label : str
            The label value.
        """
        
        if path is None:
            QMessageBox.warning(self, "Path missing", f"No {label} path is available yet.")
            return
        if not path.exists():
            QMessageBox.warning(self, "Path missing", f"The {label} path does not exist:\n{path}")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def _open_box_folder(self) -> None:
        """Support open box folder behavior.
        """
        
        paths = self._paths()
        self._open_path(paths.box_root if paths is not None else None, "box folder")

    def _send_root_path(self) -> Path | None:
        """Support send root path behavior.
        
        Returns
        -------
        Path | None
            The resolved path.
        """
        
        paths = self._paths()
        output_path = self._last_output_folder
        if output_path is None and paths is not None:
            output_path = paths.send_root
        return output_path

    def _what_to_say_path(self) -> Path | None:
        """Support what to say path behavior.
        
        Returns
        -------
        Path | None
            The resolved path.
        """
        
        paths = self._paths()
        if paths is None:
            return None
        return paths.what_to_say

    def _open_output_folder(self) -> None:
        """Support open output folder behavior.
        """
        
        self._open_path(self._send_root_path(), "External AI review folder")

    def _copy_output_folder_path(self) -> None:
        """Support copy output folder path behavior.
        """
        
        output_path = self._send_root_path()
        if output_path is None:
            QMessageBox.warning(self, "Path missing", "No external AI review folder path is available yet.")
            return
        QApplication.clipboard().setText(str(output_path))
        self.external_ai_review_folder_button.setToolTip("Open external AI review folder: " + str(output_path))
        self._append_log(f"Copied external AI review folder path: {output_path}")
