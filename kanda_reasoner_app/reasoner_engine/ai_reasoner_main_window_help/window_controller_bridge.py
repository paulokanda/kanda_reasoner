# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/window_controller_bridge.py
"""Controller bridge mixin for the Project Q&A main window."""

from __future__ import annotations

__all__ = []


class _WindowControllerBridgeMixin:
    """Expose state accessors and thin controller delegates for the main window."""

    @property
    def _last_bundle(self):
        """Support last bundle behavior."""
        return self.session_state.last_bundle

    @_last_bundle.setter
    def _last_bundle(self, value) -> None:
        """Support last bundle behavior."""
        self.session_state.last_bundle = value

    @property
    def _last_prompt(self) -> str:
        """Support last prompt behavior."""
        return self.session_state.last_prompt

    @_last_prompt.setter
    def _last_prompt(self, value: str) -> None:
        """Support last prompt behavior."""
        self.session_state.last_prompt = value

    @property
    def _last_selected_model(self) -> str:
        """Support last selected model behavior."""
        return self.session_state.last_selected_model

    @_last_selected_model.setter
    def _last_selected_model(self, value: str) -> None:
        """Support last selected model behavior."""
        self.session_state.last_selected_model = value

    @property
    def _pending_question(self) -> str:
        """Support pending question behavior."""
        return self.session_state.pending_question

    @_pending_question.setter
    def _pending_question(self, value: str) -> None:
        """Support pending question behavior."""
        self.session_state.pending_question = value

    @property
    def _detected_project_profile_name(self) -> str:
        """Support detected project profile name behavior."""
        return self.profile_state.detected_profile_name

    @_detected_project_profile_name.setter
    def _detected_project_profile_name(self, value: str) -> None:
        """Support detected project profile name behavior."""
        self.profile_state.detected_profile_name = value

    @property
    def _active_project_profile_name(self) -> str:
        """Support active project profile name behavior."""
        return self.profile_state.active_profile_name

    @_active_project_profile_name.setter
    def _active_project_profile_name(self, value: str) -> None:
        """Support active project profile name behavior."""
        self.profile_state.active_profile_name = value

    @property
    def _manual_project_profile_name(self) -> str:
        """Support manual project profile name behavior."""
        return self.profile_state.manual_profile_name

    @_manual_project_profile_name.setter
    def _manual_project_profile_name(self, value: str) -> None:
        """Support manual project profile name behavior."""
        self.profile_state.manual_profile_name = value

    @property
    def _analysis_running(self) -> bool:
        """Support analysis running behavior."""
        return self.analysis_state.is_running

    @_analysis_running.setter
    def _analysis_running(self, value: bool) -> None:
        """Support analysis running behavior."""
        self.analysis_state.is_running = value

    @property
    def _last_generated_json_path(self) -> str:
        """Support last generated json path behavior."""
        return self.analysis_state.last_generated_json_path

    @_last_generated_json_path.setter
    def _last_generated_json_path(self, value: str) -> None:
        """Support last generated json path behavior."""
        self.analysis_state.last_generated_json_path = value

    def _save_last_config(self) -> None:
        """Support save last config behavior."""
        self.settings_manager.save(self)

    def _append_log(self, text: str) -> None:
        """Support append log behavior."""
        self.log_box.appendPlainText(text)

    def _refresh_profile_controls(self) -> None:
        """Support refresh profile controls behavior."""
        self.profile_controller.refresh_controls(self)

    def _on_profile_override_changed(self) -> None:
        """Support on profile override changed behavior."""
        self.profile_controller.on_profile_override_changed(self)

    def _reset_profile_override(self) -> None:
        """Support reset profile override behavior."""
        self.profile_controller.reset_profile_override(self)

    def _refresh_static_context_controls(self) -> None:
        """Support refresh static context controls behavior."""
        self.static_context_controller.refresh_controls(self)

    def _refresh_workflow_controls(self) -> None:
        """Support refresh workflow controls behavior."""
        self.runtime_controller.refresh_workflow_controls(self)

    def _expected_generated_json_path(self, project_root: str) -> str:
        """Support expected generated json path behavior."""
        return self.analysis_controller.expected_generated_json_path(project_root)

    def pick_project_root(self) -> None:
        """Support pick project root behavior."""
        self.analysis_controller.pick_project_root(self)

    def _build_analysis_command(self, project_root: str) -> tuple[str, list[str]]:
        """Support build analysis command behavior."""
        return self.analysis_controller.build_analysis_command(project_root)

    def run_analysis(self) -> None:
        """Run the analysis."""
        self.analysis_controller.run_analysis(self)

    def _on_analysis_stdout_ready(self) -> None:
        """Support on analysis stdout ready behavior."""
        self.analysis_controller.on_analysis_stdout_ready(self)

    def _on_analysis_stderr_ready(self) -> None:
        """Support on analysis stderr ready behavior."""
        self.analysis_controller.on_analysis_stderr_ready(self)

    def _on_analysis_error_occurred(self, process_error: object) -> None:
        """Support on analysis error occurred behavior."""
        self.analysis_controller.on_analysis_error_occurred(self, process_error)

    def _on_analysis_finished(self, exit_code: int, exit_status: object) -> None:
        """Support on analysis finished behavior."""
        self.analysis_controller.on_analysis_finished(self, exit_code, exit_status)

    def refresh_models(self) -> None:
        """Support refresh models behavior."""
        self.runtime_controller.refresh_models(self)

    def clear_memory(self) -> None:
        """Support clear memory behavior."""
        self.memory.clear()
        self.history_list.clear()
        self._append_log("Conversation memory cleared.")

    def pick_cache_dir(self) -> None:
        """Support pick cache dir behavior."""
        self.runtime_controller.pick_cache_dir(self)

    def pick_governance_path(self) -> None:
        """Support pick governance path behavior."""
        self.runtime_controller.pick_governance_path(self)

    def load_json(self) -> None:
        """Load the json."""
        self.runtime_controller.load_json(self)

    def _load_json_from_path(self, file_path: str) -> None:
        """Support load json from path behavior."""
        self.runtime_controller.load_json_from_path(self, file_path)

    def _on_ai_answer_ready(self, text: str) -> None:
        """Support on ai answer ready behavior."""
        self.answer_presenter.handle_ai_answer_ready(self, text)

    def _on_ai_error_ready(self, error_text: str) -> None:
        """Support on ai error ready behavior."""
        self.answer_presenter.handle_ai_error_ready(self, error_text)

    def closeEvent(self, event) -> None:
        """Support close event behavior."""
        self._save_last_config()
        super().closeEvent(event)
