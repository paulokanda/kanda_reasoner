# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_output_paths.py
"""Private mixin helpers extracted from reasoner_tools_gui_shell.main_window."""

from __future__ import annotations

from pathlib import Path
import shutil

from kanda_reasoner_app.project_analysis_evidence_paths import (
    primary_evidence_json_path,
    analysis_json_complete_dir,
    analysis_json_parts_dir,
    project_analysis_evidence_root,
    ensure_project_analysis_evidence_dirs,
    secondary_evidence_json_path,
    parts_index_file_path,
    parts_manifest_file_path,
)

from PySide6.QtWidgets import QMessageBox

__all__: list[str] = []


class _WindowOutputPathsMixin:
    """Private implementation mixin for ReasonerToolsWindow."""

    @staticmethod
    def _project_name(project_root: Path) -> str:
        """Support project name behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        str
            The string result.
        """
        
        return project_root.name.strip() or "project"

    @staticmethod
    def _docs_root(project_root: Path) -> Path:
        """Support docs root behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return project_analysis_evidence_root(project_root)

    def _json_complete_dir(self, project_root: Path) -> Path:
        """Support json complete dir behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return analysis_json_complete_dir(project_root)

    def _json_splitted_dir(self, project_root: Path) -> Path:
        """Support json splitted dir behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return analysis_json_parts_dir(project_root)

    def _collector_complete_file(self, project_root: Path) -> Path:
        """Support collector complete file behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return primary_evidence_json_path(project_root)

    def _collector_runtime_trace_file(self, project_root: Path) -> Path:
        """Support collector runtime trace file behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return secondary_evidence_json_path(project_root)

    def _split_manifest_file(self, project_root: Path) -> Path:
        """Support split manifest file behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return parts_manifest_file_path(project_root)

    def _split_index_file(self, project_root: Path) -> Path:
        """Support split index file behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return parts_index_file_path(project_root)

    def _daily_refactor_output_root(self, project_root: Path) -> Path:
        """Support daily refactor output root behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return self._docs_root(project_root)

    def _daily_refactor_bundle_file(self, project_root: Path) -> Path:
        """Support daily refactor bundle file behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        return (
            self._docs_root(project_root)
            / "daily_refactor"
            / f"{self._project_name(project_root)}_daily_rfctr_report_bundle.json"
        )

    @staticmethod
    def _directory_has_content(path: Path) -> bool:
        """Support directory has content behavior.
        
        Parameters
        ----------
        path : Path
            The file or folder path.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        if not path.exists() or not path.is_dir():
            return False
        try:
            return any(path.iterdir())
        except Exception:
            return False

    def _output_dirs_have_content(self, project_root: Path) -> bool:
        """Support output dirs have content behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return any(
            (
                self._directory_has_content(self._json_complete_dir(project_root)),
                self._directory_has_content(self._json_splitted_dir(project_root)),
            )
        )

    @staticmethod
    def _clear_directory_contents(path: Path) -> None:
        """Support clear directory contents behavior.
        
        Parameters
        ----------
        path : Path
            The file or folder path.
        """
        
        path.mkdir(parents=True, exist_ok=True)
        for child in path.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    def _confirm_delete_existing_outputs(self, project_root: Path) -> bool:
        """Support confirm delete existing outputs behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        complete_dir = self._json_complete_dir(project_root)
        splitted_dir = self._json_splitted_dir(project_root)
        answer = QMessageBox.question(
            self,
            "Delete existing files",
            f"Files in folders, delete?\n\n- {complete_dir}\n- {splitted_dir}\n\nSelecting Yes deletes the contents of both folders before new output is created.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def _reset_output_dirs(self, project_root: Path) -> None:
        """Support reset output dirs behavior.
        
        Parameters
        ----------
        project_root : Path
            The project root path.
        """
        
        ensure_project_analysis_evidence_dirs(project_root)
        self._clear_directory_contents(self._json_complete_dir(project_root))
        self._clear_directory_contents(self._json_splitted_dir(project_root))
