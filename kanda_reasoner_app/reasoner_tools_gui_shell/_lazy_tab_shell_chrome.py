# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_shell_chrome.py
"""Header, help, and AI-model behavior for the lazy tool tab host."""

from __future__ import annotations

import contextlib

from PySide6.QtCore import QMetaObject
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTextEdit, QWidget

from .gui_support import _format_help_catalog_text, _help_catalog_path

_CANONICAL_PACKAGE_NAME = "kanda_reasoner_app"
_ARCHITECTURE_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/manage_architecture/manage_architecture_gui.py"
_WORKFLOWS_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/manage_workflows/manage_workflows_gui.py"
_DOCSTRINGS_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py"
_CONTEXT_COLLECTOR_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/reasoner_context_collector/runner.py"
_ERROR_MEMORY_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/error_memory_gui/error_memory_tab.py"
_ENGINEERING_SAFETY_GUI_SOURCE = "reasoner_tools_gui_engineering_safety_panel.py"
_FREEZE_AFTER_UPDATE_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/freeze_after_update_gui/freeze_after_update_tab.py"
_DAILY_REFACTOR_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/daily_rfctr_report/daily_refactor_report.py"
_PROJECT_QA_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/reasoner_engine/ai_reasoner_main_window.py"
_CONFIG_AI_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/reasoner_engine/config_ai_tab.py"
_WEB_AI_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/reasoner_engine/project_web_ai_tab.py"
_PROJECT_STRUCTURE_3D_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/project_structure_visualizer/project_structure_3d_tab.py"
_ACTIVE_PROJECT_BUTTON_ONLY_SOURCES = {
    _CONFIG_AI_GUI_SOURCE,
    _PROJECT_STRUCTURE_3D_GUI_SOURCE,
    _WEB_AI_GUI_SOURCE,
}
_HEADER_TEMPLATE_ONLY_SOURCES = {
    _ARCHITECTURE_GUI_SOURCE,
    _WORKFLOWS_GUI_SOURCE,
    _DOCSTRINGS_GUI_SOURCE,
    _CONTEXT_COLLECTOR_GUI_SOURCE,
    _ERROR_MEMORY_GUI_SOURCE,
    _ENGINEERING_SAFETY_GUI_SOURCE,
    _FREEZE_AFTER_UPDATE_GUI_SOURCE,
    _DAILY_REFACTOR_GUI_SOURCE,
    _PROJECT_QA_GUI_SOURCE,
}


class LazyTabShellChromeMixin:
    """Own header model synchronization, help actions, and AI review actions."""

    def _open_help_catalog(self) -> None:
        """Support open help catalog behavior.
        """
        
        if not self.spec.help_catalog:
            return

        try:
            from .help_docs.renderer import open_help_document_for_legacy_catalog

            rich_dialog = open_help_document_for_legacy_catalog(
                self,
                self.spec.help_catalog,
                window_title=f"Help - {self.spec.step_title}",
            )
        except Exception:
            rich_dialog = None
        if rich_dialog is not None:
            self._help_dialog = rich_dialog
            return

        path = _help_catalog_path(self.spec.help_catalog)
        if not path.exists():
            QMessageBox.warning(
                self,
                "Help catalog not found",
                f"Expected help catalog was not found:\n{path}",
            )
            return

        dialog = QMainWindow(self)
        dialog.setWindowTitle(f"Help - {self.spec.step_title}")
        dialog.resize(1000, 750)

        editor = QTextEdit(dialog)
        editor.setReadOnly(True)
        editor.setPlainText(_format_help_catalog_text(path))
        dialog.setCentralWidget(editor)
        dialog.show()

        self._help_dialog = dialog

    def _local_ai_configuration(self):
        from kanda_reasoner_app.local_ai_configuration import (
            application_local_ai_configuration,
        )

        return application_local_ai_configuration()

    def _open_global_local_ai_configuration(self) -> None:
        """Open the single editable Config AI Local surface."""
        self._local_ai_configuration().request_open_configuration()

    def _configure_global_local_ai_header(self) -> None:
        """Make legacy header model controls read-only global projections."""
        combo = self.tab_header_template.ai_model_combo
        button = self.tab_header_template.refresh_ai_models_button
        if combo is not None:
            combo.setEnabled(False)
            combo.setToolTip("Globally controlled by Config AI > Config Local AI.")
        if button is not None:
            button.setText("Open Config AI")
            button.setToolTip("Open the global Local AI configuration.")
        controller = self._local_ai_configuration()
        controller.configuration_changed.connect(
            lambda _snapshot: self._sync_global_local_ai_header()
        )
        controller.catalog_changed.connect(
            lambda _models: self._sync_global_local_ai_header()
        )
        self._sync_global_local_ai_header()

    def _sync_global_local_ai_header(self) -> None:
        combo = self.tab_header_template.ai_model_combo
        if combo is None:
            return
        snapshot = self._local_ai_configuration().snapshot()
        items = list(snapshot.available_models)
        if snapshot.model_id and snapshot.model_id not in items:
            items.insert(0, snapshot.model_id)
        self._replace_combo_items(combo, items, snapshot.model_id)

    def _refresh_header_ai_models(self) -> None:
        """Refresh the template AI model dropdown from the local model registry."""
        combo = self.tab_header_template.ai_model_combo
        if combo is None:
            return

        controller = self._local_ai_configuration()
        self._sync_global_local_ai_header()
        controller.refresh_models()

    def _refresh_docstring_header_ai_models(self) -> None:
        """Refresh Docstring Assistant header models through Tab 3 settings."""
        widget = self._embedded_widget
        if widget is None:
            self._refresh_header_ai_models()
            return

        try:
            refresh = widget.refresh_models
        except AttributeError:
            refresh = None
        if callable(refresh):
            try:
                refresh()
            except Exception:
                self._refresh_header_ai_models()
                return

        self._copy_tab3_model_combo_to_header(widget)

    def _bind_tab3_header_ai_model_controls(self, widget: QWidget) -> None:
        """Bind the Docstring Assistant header AI model group to Tab 3 controls."""
        if self.spec.source_hint != _DOCSTRINGS_GUI_SOURCE:
            return

        header_combo = self.tab_header_template.ai_model_combo
        try:
            body_combo = widget._model_combo
        except AttributeError:
            body_combo = None
        if header_combo is None or body_combo is None:
            return

        self._copy_tab3_model_combo_to_header(widget)
        header_combo.setObjectName("lazy_tab_header_ai_model_combo")
        body_combo.setObjectName("lazy_tab_body_ai_model_combo")
        QMetaObject.connectSlotsByName(self)


    def _copy_tab3_model_combo_to_header(self, widget: QWidget) -> None:
        """Copy Tab 3 model combo items and current selection to the header."""
        header_combo = self.tab_header_template.ai_model_combo
        try:
            body_combo = widget._model_combo
        except AttributeError:
            body_combo = None
        if header_combo is None or body_combo is None:
            return

        selected = self._combo_current_text(body_combo)
        items = [
            "Auto (first available Ollama model)",
            *[
                item
                for item in self._combo_items(body_combo)
                if item and item != "Auto (first available Ollama model)"
            ],
        ]
        if selected and selected not in items:
            items.append(selected)
        self._replace_combo_items(header_combo, items, selected or items[0])

    def _apply_header_ai_model_to_tab3(self, widget: QWidget, text: str) -> None:
        """Apply a header model selection to the Docstring Assistant model combo."""
        selected = str(text or "").strip()
        if not selected or selected == "Auto (first available Ollama model)":
            return

        try:
            body_combo = widget._model_combo
        except AttributeError:
            body_combo = None
        if body_combo is None:
            return

        items = self._combo_items(body_combo)
        if selected not in items:
            try:
                body_combo.addItem(selected)
            except AttributeError:
                pass
        try:
            body_combo.setCurrentText(selected)
        except AttributeError:
            pass

    @staticmethod
    def _combo_current_text(combo: object) -> str:
        """Return the current combo text when available."""
        try:
            return str(combo.currentText() or "").strip()
        except AttributeError:
            return ""

    @staticmethod
    def _combo_items(combo: object) -> list[str]:
        """Return all visible combo-box items."""
        try:
            count = int(combo.count())
        except (AttributeError, TypeError, ValueError):
            return []
        items: list[str] = []
        for index in range(max(0, count)):
            try:
                value = str(combo.itemText(index) or "").strip()
            except AttributeError:
                return []
            if value:
                items.append(value)
        return items

    @staticmethod
    def _replace_combo_items(combo: object, items: list[str], selected: str) -> None:
        """Replace combo items while preserving one selected text."""
        try:
            combo.blockSignals(True)
        except AttributeError:
            return
        try:
            try:
                combo.clear()
            except AttributeError:
                return
            for item in items:
                try:
                    combo.addItem(item)
                except AttributeError:
                    return
            if selected:
                try:
                    index = int(combo.findText(selected))
                except (AttributeError, TypeError, ValueError):
                    index = -1
                if index >= 0:
                    try:
                        combo.setCurrentIndex(index)
                    except AttributeError:
                        pass
        finally:
            combo.blockSignals(False)

    @staticmethod
    def _connect_signal(widget: object, signal_name: str, slot: object) -> None:
        """Retain the legacy private helper shape; active wiring uses Qt auto-connect."""
        del widget, slot
        if signal_name != "currentTextChanged":
            return

    def _show_project_ai_review_first_check(self) -> None:
        """Report the Show Project header AI review action state."""
        message = "AI Review First Check is not implemented for Show Project to AI yet."
        widget = self._embedded_widget
        if widget is not None:
            try:
                status_label = widget.first_prompt_status_label
            except AttributeError:
                status_label = None
            if status_label is not None:
                with contextlib.suppress(Exception):
                    status_label.setText(message)
            try:
                append_log = widget._append_log
            except AttributeError:
                append_log = None
            if callable(append_log):
                with contextlib.suppress(Exception):
                    append_log(message)
        QMessageBox.information(self, "AI Review First Check", message)

    def _open_freeze_feature_help(self) -> None:
        """Open the embedded Freeze Feature After Update help window."""
        if not self.ensure_loaded():
            return
        widget = self._embedded_widget
        try:
            opener = widget._show_help_window
        except AttributeError:
            opener = None
        if callable(opener):
            opener()

    def _freeze_feature_ai_review_first_check(self) -> None:
        """Open the Freeze tab's local freeze entry workflow from the AI header."""
        if not self.ensure_loaded():
            return
        widget = self._embedded_widget
        try:
            opener = widget._open_local_freeze_entry_dialog
        except AttributeError:
            opener = None
        if callable(opener):
            opener()

    def _engineering_safety_ai_review_first_check(self) -> None:
        """Run the Engineering Safety first-check action from the AI header."""
        if not self.ensure_loaded():
            return
        widget = self._embedded_widget
        try:
            runner = widget.run_ai_review_first_check
        except AttributeError:
            runner = None
        if callable(runner):
            runner()
            return
        QMessageBox.information(
            self,
            "AI Review First Check",
            "AI Review First Check is not available for Engineering Safety.",
        )

