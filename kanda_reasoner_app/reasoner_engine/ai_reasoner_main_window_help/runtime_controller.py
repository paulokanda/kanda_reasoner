# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py
"""Runtime controls and JSON loading for the Project Reasoner main window.

This helper belongs to the V10 GUI / Runtime Controller box. It may call the
Local-AI JSON Working Copy Box through its public API, but it must not implement
copy logic itself.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from PySide6.QtWidgets import QFileDialog, QMessageBox
from kanda_reasoner_app.local_ai_json_contract import ensure_local_ai_copy, refresh_local_ai_copy
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.project_json_path_resolver import (
    current_project_root_from_window,
    is_deprecated_project_json_path,
    resolve_project_json_path,
    should_replace_project_json_path,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.ui_components import shorten_path
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.json_track import classify_loaded_json_track
from kanda_reasoner_app.templates.floating_windows import (
    show_auto_close_action_window,
    show_error_copy_close_window,
)
__all__ = ['RuntimeController']

class RuntimeController:
    """Coordinate runtime setup and JSON-loading actions for the main window."""

    def _selected_project_root(self, window: Any) -> Path:
        """Return the selected project root for Project Q&A artifacts."""
        project_root = current_project_root_from_window(window)
        if project_root is None:
            raise ValueError('Select a project root before using local-AI JSON copy actions.')
        return project_root

    def _set_project_json_path(self, window: Any, file_path: str, *, reason: str) -> None:
        """Set the Project JSON/Profile path and matching track label."""
        path_text = str(file_path).strip()
        window.json_path_edit.setText(path_text)
        if hasattr(window, 'analysis_output_json_value_label'):
            window.analysis_output_json_value_label.setText(shorten_path(path_text))
        if hasattr(window, 'json_track_value_label'):
            window.json_track_value_label.setText(classify_loaded_json_track(path_text))
        window._append_log(reason + ': ' + path_text)

    def refresh_project_json_path_from_project_root(self, window: Any, *, force: bool = False, save: bool = True) -> bool:
        """Fill the JSON field from the selected project's show-project folder."""
        project_root = current_project_root_from_window(window)
        if project_root is None:
            return False
        resolution = resolve_project_json_path(project_root)
        current_path = window.json_path_edit.text().strip()
        if not should_replace_project_json_path(current_path, resolution, force=force):
            if hasattr(window, 'json_track_value_label'):
                window.json_track_value_label.setText(classify_loaded_json_track(current_path))
            return False
        self._set_project_json_path(
            window,
            str(resolution.selected_json),
            reason='Project JSON path resolved for selected project',
        )
        window._append_log('Project JSON source kind: ' + resolution.selected_kind)
        if save:
            window._save_last_config()
        return True

    def _show_local_ai_json_copy_result(self, window: Any, *, title: str, action_label: str, result: Any) -> None:
        """Show and log the result of a local-AI JSON copy operation."""
        lines = [action_label, '', 'message: ' + str(getattr(result, 'message', '')), 'canonical_json: ' + str(getattr(result, 'canonical_json', '')), 'local_ai_json: ' + str(getattr(result, 'local_ai_json', '')), 'metadata_json: ' + str(getattr(result, 'metadata_json', '')), 'hashes_match: ' + str(getattr(result, 'hashes_match', '')), 'local_is_stale: ' + str(getattr(result, 'local_is_stale', '')), 'bytes_copied: ' + str(getattr(result, 'bytes_copied', ''))]
        text = '\n'.join(lines)
        window._append_log(action_label)
        window._append_log('Local-AI JSON: ' + str(getattr(result, 'message', '')))
        show_auto_close_action_window(window, title=title, message=action_label, detail_text=text)

    def ensure_local_ai_json_copy(self, window: Any) -> None:
        """Create the local-AI JSON copy if missing."""
        try:
            project_root = self._selected_project_root(window)
            result = ensure_local_ai_copy(project_root)
        except Exception as exc:
            window._append_log('Local-AI JSON ensure failed: ' + str(exc))
            show_error_copy_close_window(window, title='Local-AI JSON error', message='Failed to create or inspect local-AI JSON copy:\n' + str(exc))
            return
        self._set_project_json_path(
            window,
            str(getattr(result, 'local_ai_json', '')),
            reason='Local-AI JSON path selected',
        )
        self._show_local_ai_json_copy_result(window, title='Local-AI JSON copy', action_label='Local-AI JSON ensure completed.', result=result)
        window._save_last_config()

    def refresh_local_ai_json_copy(self, window: Any) -> None:
        """Refresh the local-AI JSON copy from the canonical complete JSON."""
        try:
            project_root = self._selected_project_root(window)
            resolution = resolve_project_json_path(project_root)
        except Exception as exc:
            window._append_log('Local-AI JSON refresh failed: ' + str(exc))
            show_error_copy_close_window(window, title='Local-AI JSON error', message='Failed to resolve selected project JSON paths:\n' + str(exc))
            return
        question = (
            'Refresh '
            + resolution.local_ai_json.name
            + ' from '
            + resolution.canonical_json.name
            + '?\n\nThis overwrites only the local-AI working copy. The canonical complete JSON is not modified.'
        )
        answer = QMessageBox.question(window, 'Refresh local-AI JSON', question, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            window._append_log('Local-AI JSON refresh cancelled.')
            return
        try:
            result = refresh_local_ai_copy(project_root)
        except Exception as exc:
            window._append_log('Local-AI JSON refresh failed: ' + str(exc))
            show_error_copy_close_window(window, title='Local-AI JSON error', message='Failed to refresh local-AI JSON copy:\n' + str(exc))
            return
        self._set_project_json_path(
            window,
            str(getattr(result, 'local_ai_json', '')),
            reason='Local-AI JSON path selected',
        )
        self._show_local_ai_json_copy_result(window, title='Local-AI JSON refreshed', action_label='Local-AI JSON refresh completed.', result=result)
        window._save_last_config()

    def refresh_models(self, window: Any) -> None:
        """Project the global Local AI catalog into the read-only combo."""
        from kanda_reasoner_app.local_ai_configuration import (
            application_local_ai_configuration,
        )

        controller = application_local_ai_configuration()
        snapshot = controller.snapshot()
        window.model_combo.blockSignals(True)
        try:
            window.model_combo.clear()
            if snapshot.model_id:
                window.model_combo.addItem(snapshot.model_id)
                for model_name in snapshot.available_models:
                    if model_name != snapshot.model_id:
                        window.model_combo.addItem(model_name)
                window.model_combo.setCurrentIndex(0)
            else:
                window.model_combo.addItem("Global Local AI model not selected")
        finally:
            window.model_combo.blockSignals(False)
        window.model_combo.setEnabled(False)
        window._append_log("Local AI configuration: " + controller.summary())

    def pick_cache_dir(self, window: Any) -> None:
        """Support pick cache dir behavior.
        
        Parameters
        ----------
        window : Any
            The window value.
        """
        
        path = QFileDialog.getExistingDirectory(window, 'Select cache directory')
        if not path:
            return
        window.cache_dir_edit.setText(path)
        try:
            window.ai.set_cache_dir(path)
            window._append_log('Cache dir set: ' + path)
            window._save_last_config()
        except Exception as exc:
            QMessageBox.warning(window, 'Cache dir error', str(exc))

    def pick_governance_path(self, window: Any) -> None:
        """Support pick governance path behavior.
        
        Parameters
        ----------
        window : Any
            The window value.
        """
        
        path, _selected_filter = QFileDialog.getOpenFileName(window, 'Select governance_state.json', os.getcwd(), 'JSON Files (*.json)')
        if not path:
            return
        window.governance_path_edit.setText(path)
        try:
            window.ai.set_governance_state_path(path)
            window._append_log('Governance state set: ' + path)
            window._save_last_config()
        except Exception as exc:
            QMessageBox.warning(window, 'Governance path error', str(exc))

    def load_json(self, window: Any) -> None:
        """Load the json.
        
        Parameters
        ----------
        window : Any
            The window value.
        """
        
        current_path = window.json_path_edit.text().strip()
        start_dir = os.path.dirname(current_path) if current_path and (not is_deprecated_project_json_path(current_path)) else os.getcwd()
        if not current_path or is_deprecated_project_json_path(current_path):
            project_root = current_project_root_from_window(window)
            if project_root is not None:
                start_dir = str(resolve_project_json_path(project_root).selected_json.parent)
        file_path, _selected_filter = QFileDialog.getOpenFileName(window, 'Select project JSON/profile', start_dir, 'JSON Files (*.json)')
        if not file_path:
            return
        try:
            self.load_json_from_path(window, file_path)
            show_auto_close_action_window(window, title='Loaded', message='JSON loaded successfully.')
        except Exception as exc:
            show_error_copy_close_window(window, title='Error', message='Failed to load JSON:\n' + str(exc))

    def load_json_from_path(self, window: Any, file_path: str) -> None:
        """Load the json from path.
        
        Parameters
        ----------
        window : Any
            The window value.
        file_path : str
            The file path.
        """
        
        window.project_index.load_json(file_path)
        window.json_path_edit.setText(file_path)
        if window.project_index.project_root:
            window.project_root_edit.setText(window.project_index.project_root)
        summary = (window.project_index.index_data or {}).get('project_summary', {})
        window.analysis_status_value_label.setText('Loaded')
        window.analysis_output_json_value_label.setText(shorten_path(file_path))
        json_track = classify_loaded_json_track(file_path)
        if hasattr(window, 'json_track_value_label'):
            window.json_track_value_label.setText(json_track)
        window._append_log('Loaded JSON: ' + file_path)
        window._append_log('JSON track: ' + json_track)
        window._append_log('Project root: ' + window.project_index.project_root)
        window._append_log('Python files: ' + str(summary.get('python_file_count', 'unknown')))
        window._append_log('Entry files: ' + str(summary.get('entry_file_count', 'unknown')))
        window._refresh_profile_controls()
        window._refresh_static_context_controls()
        self.refresh_workflow_controls(window)
        window._append_log('Detected profile: ' + window.detected_profile_value_label.text())
        window._append_log('Active profile: ' + window.active_profile_value_label.text())
        window._append_log('Static context: ' + window.static_context_summary_value_label.text())
        window._save_last_config()

    def _json_path_is_loadable(self, window: Any) -> bool:
        """Return True when the JSON field points at a loadable project file."""
        path_text = window.json_path_edit.text().strip()
        if not path_text or is_deprecated_project_json_path(path_text):
            return False
        return Path(path_text).expanduser().is_file()

    def _load_project_json_candidate_for_question(
        self,
        window: Any,
        candidate_path: Path,
        *,
        reason: str,
    ) -> bool:
        """Load one resolved Project Q&A JSON candidate before asking."""
        if not candidate_path.is_file():
            return False
        self._set_project_json_path(window, str(candidate_path), reason=reason)
        self.load_json_from_path(window, str(candidate_path))
        return bool(window.project_index.index_data)

    def ensure_project_json_loaded_for_question(self, window: Any) -> bool:
        """Resolve and load the selected project's JSON before asking."""
        if bool(window.project_index.index_data):
            return True

        if self._json_path_is_loadable(window):
            self.load_json_from_path(window, window.json_path_edit.text().strip())
            return bool(window.project_index.index_data)

        project_root = current_project_root_from_window(window)
        if project_root is None:
            raise ValueError(
                "Select a project root or load a Project Q&A JSON file before asking."
            )

        resolution = resolve_project_json_path(project_root)
        if self._load_project_json_candidate_for_question(
            window,
            resolution.local_ai_json,
            reason="Project Q&A local-AI JSON auto-selected before asking",
        ):
            return True

        if resolution.canonical_json.is_file():
            result = ensure_local_ai_copy(project_root)
            local_ai_json = Path(str(getattr(result, "local_ai_json", resolution.local_ai_json)))
            if self._load_project_json_candidate_for_question(
                window,
                local_ai_json,
                reason="Project Q&A local-AI JSON auto-created before asking",
            ):
                return True

        if not project_root.is_dir():
            raise FileNotFoundError(
                "Selected Project root does not exist or is not a directory: "
                + str(project_root)
            )

        window.project_index.initialize_live_project(str(project_root))
        window._append_log(
            "Local AI source mode: bounded read-only live Project source. "
            "Complete Project Q&A JSON was not available."
        )
        return True

    def refresh_workflow_controls(self, window: Any) -> None:
        """Support refresh workflow controls behavior.
        
        Parameters
        ----------
        window : Any
            The window value.
        """
        
        has_project_root = bool(window.project_root_edit.text().strip())
        has_loaded_json = bool(window.project_index.index_data)
        has_question = bool(window.question_edit.text().strip())
        is_running = bool(window._analysis_running)
        window.pick_project_root_button.setEnabled(not is_running)
        window.run_analysis_button.setEnabled(has_project_root and (not is_running))
        window.load_button.setEnabled(not is_running)
        # The Ask button is a user command gate, not the data-integrity gate.
        # JSON/model validation remains inside ask_local_ai and SessionService.
        window.ask_ai_button.setEnabled(has_question and (not is_running))
        window.static_context_button.setEnabled(has_loaded_json and (not is_running))
        window.profile_override_combo.setEnabled(has_loaded_json and (not is_running))
        window.reset_profile_override_button.setEnabled(bool(window._manual_project_profile_name) and (not is_running))
        if hasattr(window, 'ensure_local_ai_json_button'):
            window.ensure_local_ai_json_button.setEnabled(not is_running)
        if hasattr(window, 'refresh_local_ai_json_button'):
            window.refresh_local_ai_json_button.setEnabled(not is_running)
