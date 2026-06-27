"""Project Q&A main window.

This is normal readable source. The older encoded backend payload
for this visible tab is deprecated and must not be restored as
the editable source of truth.
"""

from __future__ import annotations

import sys

from importlib import import_module as _qtcore_import_module


def _qt_core_attr(name: str):
    """Return a PySide6.QtCore attribute without a static QtCore import."""
    return getattr(_qtcore_import_module("PySide6.QtCore"), name)

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QCheckBox,
    QApplication,
    QButtonGroup,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QRadioButton,
)

from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.analysis_controller import (
    AnalysisController,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.runtime_controller import (
    RuntimeController,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.answer_presenter import (
    AnswerPresenter,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.profile_controller import (
    ProfileController,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.session_service import (
    SessionExecutionError,
    SessionService,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.settings_manager import (
    WindowSettingsManager,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.state_models import (
    AnalysisState,
    ProfileSelectionState,
    WindowSessionState,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.static_context_controller import (
    StaticContextController,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.ui_components import (
    CopyableListWidget,
    HelpDialog,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.ui_builder import (
    build_main_window_ui,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.signal_wiring import (
    connect_main_window_signals,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge import LocalAIReasoner
from kanda_reasoner_app.reasoner_engine.v10_conversation_memory import ConversationMemory
from kanda_reasoner_app.reasoner_engine.index_loader import JsonProjectIndex
from kanda_reasoner_app.reasoner_engine.v10_model_registry import LocalModelRegistry
from kanda_reasoner_app.reasoner_engine.v10_models import RetrievalBundle
from kanda_reasoner_app.reasoner_engine.prompt_builder import PromptBuilder
from kanda_reasoner_app.reasoner_engine.reasoner_retriever import ProjectRetriever

__all__ = ["JsonProjectReasonerV10", "main"]

class JsonProjectReasonerV10(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer V10 - Local AI Reasoner")
        self.resize(1880, 1080)

        self.project_index = JsonProjectIndex()
        self.retriever = ProjectRetriever(self.project_index)
        self.prompt_builder = PromptBuilder()
        self.ai = LocalAIReasoner()
        self.memory = ConversationMemory()
        self.model_registry = LocalModelRegistry()
        self.settings = _qt_core_attr("QSettings")("Kanda", "ProjectReasonerV10")

        self.settings_manager = WindowSettingsManager()
        self.profile_controller = ProfileController()
        self.static_context_controller = StaticContextController()
        self.analysis_controller = AnalysisController()
        self.runtime_controller = RuntimeController()
        self.session_service = SessionService()
        self.answer_presenter = AnswerPresenter()

        self._settings_ready = False
        self.session_state = WindowSessionState()
        self.profile_state = ProfileSelectionState()
        self.analysis_state = AnalysisState()
        self._analysis_process: QProcess | None = None
        self._static_context_dialog = None

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()
        self.cache_dir_edit = QLineEdit()
        self.governance_path_edit = QLineEdit()

        self.model_combo = QComboBox()
        self.refresh_models_button = QPushButton("Refresh Models")
        self.help_button = QPushButton("Help (?)")
        self.help_button.setFixedWidth(80)
        self.static_context_button = QPushButton("Static Context")

        self.load_button = QPushButton("Load JSON")
        self.ask_ai_button = QPushButton("Ask Local AI")
        self.clear_button = QPushButton("Clear")
        self.clear_memory_button = QPushButton("Clear Memory")
        self.pick_cache_dir_button = QPushButton("Set Cache Dir")
        self.pick_governance_button = QPushButton("Set Governance State")

        self.quick_startup_button = QPushButton("Explain startup chain")
        self.quick_topomap_button = QPushButton("Explain topomap chain")
        self.quick_timeline_button = QPushButton("Explain timeline chain")
        self.quick_responsibility_button = QPushButton("Responsibility map")
        self.quick_uncertainty_button = QPushButton("Uncertainty report")

        self.prefer_code_radio = QRadioButton("Prefer code")
        self.prefer_prose_radio = QRadioButton("Prefer prose")
        self.answer_style_group = QButtonGroup(self)
        self.answer_style_group.setExclusive(True)
        self.answer_style_group.addButton(self.prefer_code_radio)
        self.answer_style_group.addButton(self.prefer_prose_radio)
        self.prefer_code_radio.setChecked(True)

        self.file_evidence_list = CopyableListWidget()
        self.symbol_evidence_list = CopyableListWidget()
        self.history_list = CopyableListWidget()

        self.detail_box = QPlainTextEdit()
        self.detail_box.setReadOnly(True)
        self.answer_box = QPlainTextEdit()
        self.answer_box.setReadOnly(True)
        self.prompt_preview = QPlainTextEdit()
        self.prompt_preview.setReadOnly(True)
        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self.detected_profile_value_label = QLabel("Not loaded")
        self.active_profile_value_label = QLabel("Not loaded")
        self.profile_override_combo = QComboBox()
        self.reset_profile_override_button = QPushButton("Reset Profile")
        self.reset_profile_override_button.setEnabled(False)

        self.static_context_summary_value_label = QLabel("Not loaded")
        self.static_context_packaging_value_label = QLabel("Unknown")
        self.static_context_docs_value_label = QLabel("Unknown")

        self.project_root_edit = QLineEdit()
        self.pick_project_root_button = QPushButton("Select Project")
        self.run_analysis_button = QPushButton("Run Analysis")
        self.analysis_status_value_label = QLabel("Idle")
        self.analysis_output_json_value_label = QLabel("Not generated")
        self.analysis_auto_load_checkbox = QCheckBox("Auto-load JSON after analysis")
        self.analysis_auto_load_checkbox.setChecked(True)

        self.verbosity_combo = QComboBox()
        self.verbosity_combo.addItems(["Concise", "Detailed", "With Code"])
        self.debug_checkbox = QCheckBox("Debug Mode")

        self._build_ui()
        self._connect_signals()
        self.refresh_models()
        self.settings_manager.restore(self)
        self._refresh_profile_controls()
        self._refresh_static_context_controls()
        self._refresh_workflow_controls()
        self._settings_ready = True

    @property
    def _last_bundle(self) -> RetrievalBundle:
        return self.session_state.last_bundle

    @_last_bundle.setter
    def _last_bundle(self, value: RetrievalBundle) -> None:
        self.session_state.last_bundle = value

    @property
    def _last_prompt(self) -> str:
        return self.session_state.last_prompt

    @_last_prompt.setter
    def _last_prompt(self, value: str) -> None:
        self.session_state.last_prompt = value

    @property
    def _last_selected_model(self) -> str:
        return self.session_state.last_selected_model

    @_last_selected_model.setter
    def _last_selected_model(self, value: str) -> None:
        self.session_state.last_selected_model = value

    @property
    def _pending_question(self) -> str:
        return self.session_state.pending_question

    @_pending_question.setter
    def _pending_question(self, value: str) -> None:
        self.session_state.pending_question = value

    @property
    def _detected_project_profile_name(self) -> str:
        return self.profile_state.detected_profile_name

    @_detected_project_profile_name.setter
    def _detected_project_profile_name(self, value: str) -> None:
        self.profile_state.detected_profile_name = value

    @property
    def _active_project_profile_name(self) -> str:
        return self.profile_state.active_profile_name

    @_active_project_profile_name.setter
    def _active_project_profile_name(self, value: str) -> None:
        self.profile_state.active_profile_name = value

    @property
    def _manual_project_profile_name(self) -> str:
        return self.profile_state.manual_profile_name

    @_manual_project_profile_name.setter
    def _manual_project_profile_name(self, value: str) -> None:
        self.profile_state.manual_profile_name = value

    @property
    def _analysis_running(self) -> bool:
        return self.analysis_state.is_running

    @_analysis_running.setter
    def _analysis_running(self, value: bool) -> None:
        self.analysis_state.is_running = value

    @property
    def _last_generated_json_path(self) -> str:
        return self.analysis_state.last_generated_json_path

    @_last_generated_json_path.setter
    def _last_generated_json_path(self, value: str) -> None:
        self.analysis_state.last_generated_json_path = value

    def _save_last_config(self) -> None:
        self.settings_manager.save(self)

    def _append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def _refresh_profile_controls(self) -> None:
        self.profile_controller.refresh_controls(self)

    def _rebuild_retriever_for_active_profile(self) -> None:
        result = self.profile_controller.build_refresh_result(
            project_index=self.project_index,
            current_override_name=self.profile_override_combo.currentText(),
        )
        self.retriever = result.retriever
        self.profile_state = result.state
        self.detected_profile_value_label.setText(result.detected_label_text)
        self.active_profile_value_label.setText(result.active_label_text)
        self.profile_override_combo.setEnabled(result.override_enabled and not self._analysis_running)
        self.reset_profile_override_button.setEnabled(result.reset_enabled and not self._analysis_running)

    def _on_profile_override_changed(self) -> None:
        self.profile_controller.on_profile_override_changed(self)

    def _reset_profile_override(self) -> None:
        self.profile_controller.reset_profile_override(self)

    def _refresh_static_context_controls(self) -> None:
        self.static_context_controller.refresh_controls(self)

    def _refresh_workflow_controls(self) -> None:
        self.runtime_controller.refresh_workflow_controls(self)

    def _expected_generated_json_path(self, project_root: str) -> str:
        return self.analysis_controller.expected_generated_json_path(project_root)

    def pick_project_root(self) -> None:
        self.analysis_controller.pick_project_root(self)

    def _build_analysis_command(self, project_root: str) -> tuple[str, list[str]]:
        return self.analysis_controller.build_analysis_command(project_root)

    def run_analysis(self) -> None:
        self.analysis_controller.run_analysis(self)

    def _on_analysis_stdout_ready(self) -> None:
        self.analysis_controller.on_analysis_stdout_ready(self)

    def _on_analysis_stderr_ready(self) -> None:
        self.analysis_controller.on_analysis_stderr_ready(self)

    def _on_analysis_error_occurred(self, process_error: QProcess.ProcessError) -> None:
        self.analysis_controller.on_analysis_error_occurred(self, process_error)

    def _on_analysis_finished(self, exit_code: int, exit_status: object) -> None:
        self.analysis_controller.on_analysis_finished(self, exit_code, exit_status)

    def _on_ai_token_ready(self, token: str) -> None:
        current = self.answer_box.toPlainText()
        if current == "[Streaming...]\n\n":
            self.answer_box.setPlainText("")

        cursor = self.answer_box.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(token)
        self.answer_box.setTextCursor(cursor)
        self.answer_box.ensureCursorVisible()

    def _build_ui(self) -> None:
        build_main_window_ui(self)

    def _connect_signals(self) -> None:
        connect_main_window_signals(self)

    def show_help_dialog(self) -> None:
        dialog = HelpDialog(self)
        dialog.exec()

    def show_static_context_dialog(self) -> None:
        self.static_context_controller.show_dialog(self)

    def refresh_models(self) -> None:
        self.runtime_controller.refresh_models(self)

    def clear_visuals_only(self) -> None:
        self.file_evidence_list.clear()
        self.symbol_evidence_list.clear()
        self.detail_box.clear()
        self.answer_box.setPlainText("[Streaming...]\n\n")
        self.prompt_preview.clear()
        self.log_box.clear()
        self.session_state.clear_visual_state()
        self._refresh_static_context_controls()
        self._refresh_workflow_controls()

    def clear_memory(self) -> None:
        self.memory.clear()
        self.history_list.clear()
        self._append_log("Conversation memory cleared.")

    def _run_quick_question(self, question: str) -> None:
        self.question_edit.setText(question)
        self.ask_local_ai()

    def pick_cache_dir(self) -> None:
        self.runtime_controller.pick_cache_dir(self)

    def pick_governance_path(self) -> None:
        self.runtime_controller.pick_governance_path(self)

    def load_json(self) -> None:
        self.runtime_controller.load_json(self)

    def _load_json_from_path(self, file_path: str) -> None:
        self.runtime_controller.load_json_from_path(self, file_path)

    def ask_local_ai(self) -> None:
        if self._analysis_running:
            QMessageBox.information(
                self,
                "Analysis running",
                "Please wait for the current analysis to finish.",
            )
            return

        question = self.question_edit.text().strip()
        selected_model = self.model_combo.currentText().strip()

        try:
            result = self.session_service.execute(self, question, selected_model)
        except SessionExecutionError as exc:
            message = str(exc)
            if message == "No relevant evidence was retrieved.":
                QMessageBox.information(self, "No Evidence", message)
            elif message == "Please load a JSON file first.":
                QMessageBox.warning(self, "No JSON", message)
            elif message == "Please type a question.":
                QMessageBox.warning(self, "No Question", message)
            elif message == "Please select a model.":
                QMessageBox.warning(self, "No Model", message)
            else:
                QMessageBox.warning(self, "Session error", message)
            return

        for line in result.log_messages:
            self._append_log(line)

        self._last_bundle = result.bundle
        self._last_prompt = result.prompt
        self._last_selected_model = result.selected_model
        self._pending_question = result.question

        self.answer_presenter.populate_evidence_lists(self, result.bundle)
        self.prompt_preview.setPlainText(result.prompt)

        if result.route == "ranked":
            self.answer_box.setPlainText(result.answer_text)
            self.prompt_preview.clear()
            return

        self.answer_box.setPlainText(result.answer_text)
        self.ai.ask(result.prompt, result.selected_model)

    def _on_ai_answer_ready(self, text: str) -> None:
        self.answer_presenter.handle_ai_answer_ready(self, text)

    def _on_ai_error_ready(self, error_text: str) -> None:
        self.answer_presenter.handle_ai_error_ready(self, error_text)

    def closeEvent(self, event) -> None:
        self._save_last_config()
        super().closeEvent(event)

def main() -> None:
    app = QApplication(sys.argv)
    window = JsonProjectReasonerV10()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()






