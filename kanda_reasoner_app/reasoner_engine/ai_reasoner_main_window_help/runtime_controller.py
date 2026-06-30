"""Runtime controls and JSON loading for the Project Reasoner main window.

This helper belongs to the V10 GUI / Runtime Controller box. It may call the
Local-AI JSON Working Copy Box through its public API, but it must not implement
copy logic itself.
"""
from __future__ import annotations
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
import os
from pathlib import Path
from typing import Any
from PySide6.QtWidgets import QFileDialog, QMessageBox
from kanda_reasoner_app.local_ai_json_contract import ensure_local_ai_copy, refresh_local_ai_copy
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.ui_components import shorten_path
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.json_track import classify_loaded_json_track
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window
__all__ = ['RuntimeController']

class RuntimeController:
    """Coordinate runtime setup and JSON-loading actions for the main window."""

    def _tool_project_root(self) -> Path:
        """Return the developer_tools root that owns Reasoner assets."""
        return Path(__file__).resolve().parents[3]

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
            result = ensure_local_ai_copy(self._tool_project_root())
        except Exception as exc:
            window._append_log('Local-AI JSON ensure failed: ' + str(exc))
            show_error_copy_close_window(window, title='Local-AI JSON error', message='Failed to create or inspect local-AI JSON copy:\n' + str(exc))
            return
        self._show_local_ai_json_copy_result(window, title='Local-AI JSON copy', action_label='Local-AI JSON ensure completed.', result=result)

    def refresh_local_ai_json_copy(self, window: Any) -> None:
        """Refresh the local-AI JSON copy from the canonical complete JSON."""
        answer = QMessageBox.question(window, 'Refresh local-AI JSON', 'Refresh developer_tools__complete_local_AI.json from developer_tools__complete.json?\n\nThis overwrites only the local-AI working copy. The canonical complete JSON is not modified.', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            window._append_log('Local-AI JSON refresh cancelled.')
            return
        try:
            result = refresh_local_ai_copy(self._tool_project_root())
        except Exception as exc:
            window._append_log('Local-AI JSON refresh failed: ' + str(exc))
            show_error_copy_close_window(window, title='Local-AI JSON error', message='Failed to refresh local-AI JSON copy:\n' + str(exc))
            return
        self._show_local_ai_json_copy_result(window, title='Local-AI JSON refreshed', action_label='Local-AI JSON refresh completed.', result=result)

    def refresh_models(self, window: Any) -> None:
        """Refresh the model dropdown from the live Ollama registry."""
        previous_selection = window.model_combo.currentText().strip()
        saved_selection = ''
        settings = getattr(window, 'settings', None)
        if settings is not None:
            saved_selection = str(settings.value('selected_model', '', type=str)).strip()
        models = window.model_registry.list_models()
        using_fallback = False
        if not models:
            models = ['qwen2.5-coder:7b', 'qwen2.5-coder:32b']
            using_fallback = True
        window.model_combo.clear()
        for model_name in models:
            window.model_combo.addItem(model_name)
        preferred_candidates = (previous_selection, saved_selection, 'qwen3-coder:30b', 'qwen2.5-coder:7b')
        for preferred in preferred_candidates:
            if not preferred:
                continue
            index = window.model_combo.findText(preferred)
            if index >= 0:
                window.model_combo.setCurrentIndex(index)
                break
        if using_fallback:
            window._append_log('Could not verify models from Ollama. Added fallback model names.')
        else:
            window._append_log('Ollama model refresh found ' + str(len(models)) + ' model(s): ' + ', '.join(models))
        window._save_last_config()

    def pick_cache_dir(self, window: Any) -> None:
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
        current_path = window.json_path_edit.text().strip()
        start_dir = os.path.dirname(current_path) if current_path else os.getcwd()
        file_path, _selected_filter = QFileDialog.getOpenFileName(window, 'Select project_structure_index.json', start_dir, 'JSON Files (*.json)')
        if not file_path:
            return
        try:
            self.load_json_from_path(window, file_path)
            show_auto_close_action_window(window, title='Loaded', message='JSON loaded successfully.')
        except Exception as exc:
            show_error_copy_close_window(window, title='Error', message='Failed to load JSON:\n' + str(exc))

    def load_json_from_path(self, window: Any, file_path: str) -> None:
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

    def refresh_workflow_controls(self, window: Any) -> None:
        has_project_root = bool(window.project_root_edit.text().strip())
        has_json = bool(window.project_index.index_data)
        is_running = bool(window._analysis_running)
        window.pick_project_root_button.setEnabled(not is_running)
        window.run_analysis_button.setEnabled(has_project_root and (not is_running))
        window.load_button.setEnabled(not is_running)
        window.ask_ai_button.setEnabled(has_json and (not is_running))
        window.static_context_button.setEnabled(has_json and (not is_running))
        window.profile_override_combo.setEnabled(has_json and (not is_running))
        window.reset_profile_override_button.setEnabled(bool(window._manual_project_profile_name) and (not is_running))
        if hasattr(window, 'ensure_local_ai_json_button'):
            window.ensure_local_ai_json_button.setEnabled(not is_running)
        if hasattr(window, 'refresh_local_ai_json_button'):
            window.refresh_local_ai_json_button.setEnabled(not is_running)
