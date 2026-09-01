# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py
"""Project Q&A main window.

This is normal readable source. The older encoded backend payload
for this visible tab is deprecated and must not be restored as
the editable source of truth.
"""

from __future__ import annotations

import sys
import contextlib

from importlib import import_module as _qtcore_import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtCore import QProcess


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

from kanda_reasoner_app.templates.floating_windows import (
    install_error_popup_copy_close_filter,
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
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.window_controller_bridge import (
    _WindowControllerBridgeMixin,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge import LocalAIReasoner
from kanda_reasoner_app.reasoner_engine.v10_conversation_memory import ConversationMemory
from kanda_reasoner_app.reasoner_engine.index_loader import JsonProjectIndex
from kanda_reasoner_app.reasoner_engine.v10_model_registry import LocalModelRegistry
from kanda_reasoner_app.local_ai_configuration import application_local_ai_configuration
from kanda_reasoner_app.reasoner_engine.prompt_builder import PromptBuilder
from kanda_reasoner_app.reasoner_engine.reasoner_retriever import ProjectRetriever

__all__ = ["JsonProjectReasonerV10", "main"]

class JsonProjectReasonerV10(_WindowControllerBridgeMixin, QMainWindow):
    """Represent json project reasoner v10."""
    
    def __init__(self) -> None:
        """Support init behavior.
        """
        
        super().__init__()
        self.setWindowTitle("Local AI - KANDA Reasoner")
        self.resize(1880, 1080)

        self.project_index = JsonProjectIndex()
        self.retriever = ProjectRetriever(self.project_index)
        self.prompt_builder = PromptBuilder()
        self.ai = LocalAIReasoner()
        self.memory = ConversationMemory()
        self._local_ai_configuration = application_local_ai_configuration()
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
        self.model_combo.setEnabled(False)
        self.refresh_models_button = QPushButton("Open Config AI")
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
        self._project_root_controls_moved_to_host = False
        self._ai_runtime_controls_moved_to_host = False

        self.verbosity_combo = QComboBox()
        self.verbosity_combo.addItems(["Concise", "Detailed", "With Code"])
        self.debug_checkbox = QCheckBox("Debug Mode")

        self._build_ui()
        self._connect_signals()
        self.settings_manager.restore(self)
        self._wire_global_local_ai_configuration()
        self._sync_global_local_ai_controls()
        self._local_ai_configuration.refresh_models()
        self.runtime_controller.refresh_project_json_path_from_project_root(
            self,
            force=False,
            save=False,
        )
        self._refresh_profile_controls()
        self._refresh_static_context_controls()
        self._refresh_workflow_controls()
        self._settings_ready = True

    def _rebuild_retriever_for_active_profile(self) -> None:
        """Support rebuild retriever for active profile behavior.
        """
        
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

    def _on_ai_token_ready(self, token: str) -> None:
        """Support on ai token ready behavior.
        
        Parameters
        ----------
        token : str
            The token value.
        """
        
        current = self.answer_box.toPlainText()
        if current == "[Streaming...]\n\n":
            self.answer_box.setPlainText("")

        cursor = self.answer_box.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(token)
        self.answer_box.setTextCursor(cursor)
        self.answer_box.ensureCursorVisible()

    def _wire_global_local_ai_configuration(self) -> None:
        """Keep Project Q&A controls as read-only projections of Config Local AI."""
        self._local_ai_configuration.configuration_changed.connect(
            lambda _snapshot: self._sync_global_local_ai_controls()
        )
        self._local_ai_configuration.catalog_changed.connect(
            lambda _models: self._sync_global_local_ai_controls()
        )

    def _sync_global_local_ai_controls(self) -> None:
        """Keep the hidden compatibility projection aligned with Config Local AI."""
        snapshot = self._local_ai_configuration.snapshot()
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        for model in snapshot.available_models:
            self.model_combo.addItem(model)
        if snapshot.model_id and self.model_combo.findText(snapshot.model_id) < 0:
            self.model_combo.addItem(snapshot.model_id)
        self.model_combo.setCurrentText(snapshot.model_id)
        self.model_combo.blockSignals(False)
        self.model_combo.setToolTip(
            "Hidden compatibility projection; Config AI owns model selection."
        )

    def selected_local_ai_model(self) -> str:
        """Return the single application-scoped Local AI model selection."""
        return str(self._local_ai_configuration.snapshot().model_id or "").strip()

    def _build_ui(self) -> None:
        """Support build ui behavior.
        """
        
        build_main_window_ui(self)

    def _connect_signals(self) -> None:
        """Support connect signals behavior.
        """
        
        connect_main_window_signals(self)

    def move_project_root_controls_to_layout(
        self,
        destination_layout,
        insert_index: int | None = None,
    ) -> None:
        """Move Project Q&A project-root controls into a host layout."""
        if self._project_root_controls_moved_to_host:
            return

        widgets = [
            getattr(self, "project_root_label", None),
            self.project_root_edit,
            self.pick_project_root_button,
            self.run_analysis_button,
        ]
        self._move_widgets_to_host_layout(widgets, destination_layout, insert_index)
        self._project_root_controls_moved_to_host = True

    def move_ai_runtime_controls_to_layout(
        self,
        destination_layout,
        insert_index: int | None = None,
    ) -> None:
        """Move only the canonical Config AI shortcut into the host layout."""
        if self._ai_runtime_controls_moved_to_host:
            return

        widgets = [self.refresh_models_button]
        self._move_widgets_to_host_layout(widgets, destination_layout, insert_index)
        self._ai_runtime_controls_moved_to_host = True

    @staticmethod
    def _move_widgets_to_host_layout(
        widgets: list[object],
        destination_layout,
        insert_index: int | None = None,
    ) -> None:
        """Move live widgets into a host layout without duplicating state."""
        if insert_index is None:
            destination_layout.addSpacing(12)
            target_index = destination_layout.count()
        else:
            destination_layout.insertSpacing(insert_index, 12)
            target_index = insert_index + 1

        offset = 0
        for widget in widgets:
            if widget is None:
                continue
            parent = widget.parentWidget()
            parent_layout = parent.layout() if parent is not None else None
            if parent_layout is not None:
                with contextlib.suppress(Exception):
                    parent_layout.removeWidget(widget)
            widget.setParent(None)
            destination_layout.insertWidget(target_index + offset, widget, 0)
            offset += 1

    def show_help_dialog(self) -> None:
        """Show the help dialog.
        """
        
        dialog = HelpDialog(self)
        dialog.exec()

    def show_static_context_dialog(self) -> None:
        """Show the static context dialog.
        """
        
        self.static_context_controller.show_dialog(self)

    def clear_visuals_only(self) -> None:
        """Support clear visuals only behavior.
        """
        
        self.file_evidence_list.clear()
        self.symbol_evidence_list.clear()
        self.detail_box.clear()
        self.answer_box.setPlainText("[Streaming...]\n\n")
        self.prompt_preview.clear()
        self.log_box.clear()
        self.session_state.clear_visual_state()
        self._refresh_static_context_controls()
        self._refresh_workflow_controls()

    def _run_quick_question(self, question: str) -> None:
        """Support run quick question behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        """
        
        self.question_edit.setText(question)
        self.ask_local_ai()

    def ask_local_ai(self) -> None:
        """Support ask local ai behavior.
        """
        
        if self._analysis_running:
            QMessageBox.information(
                self,
                "Analysis running",
                "Please wait for the current analysis to finish.",
            )
            return

        question = self.question_edit.text().strip()
        selected_model = self._local_ai_configuration.selected_model_id().strip()
        if not selected_model:
            QMessageBox.warning(
                self,
                "Local AI not configured",
                "Open Config AI > Config Local AI and select a model first.",
            )
            self._local_ai_configuration.request_open_configuration()
            return

        try:
            self.runtime_controller.ensure_project_json_loaded_for_question(self)
        except Exception as exc:
            QMessageBox.warning(self, "JSON load failed", str(exc))
            return

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

def main() -> None:
    """Support main behavior.
    """
    
    app = QApplication(sys.argv)
    install_error_popup_copy_close_filter(app)
    window = JsonProjectReasonerV10()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
