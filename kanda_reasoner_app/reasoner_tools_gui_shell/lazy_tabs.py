# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py
"""Lazy loading tab host for embedded Reasoner tools."""

from __future__ import annotations

import contextlib
import importlib
import json
import shutil
import sys
import traceback
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QInputDialog,
    QGroupBox,
    QFileDialog,
)

from .error_panels import ToolLoadErrorPanel
from .gui_support import (
    _architecture_worker_script_path,
    _first_existing_attr,
    _first_imported_module,
    _format_help_catalog_text,
    _help_catalog_path,
    _prepare_embedded_widget,
)
from .tab_header_template import TabHeaderTemplate
from .tool_specs import ToolSpec

__all__ = [
    "LazyToolTab",
]


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

from kanda_reasoner_app.templates.floating_windows.float_window import attach_floating_window

class LazyToolTab(QWidget):
    """Represent lazy tool tab."""
    
    def __init__(self, spec: ToolSpec, on_loaded) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        spec : ToolSpec
            The spec value.
        on_loaded : object
            The on loaded value.
        """
        
        super().__init__()
        self.spec = spec
        self._loaded = False
        self._embedded_widget: QWidget | None = None
        self._on_loaded = on_loaded
        self._help_dialog: QMainWindow | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(10)

        help_handler = self._open_help_catalog if spec.help_catalog else None
        if spec.source_hint == _FREEZE_AFTER_UPDATE_GUI_SOURCE:
            help_handler = self._open_freeze_feature_help
        self.tab_header_template = TabHeaderTemplate(
            spec.step_title,
            help_handler=help_handler,
        )
        self.header_row = self.tab_header_template.layout
        self._header_controls_insert_index = self.header_row.indexOf(
            self.tab_header_template.project_root_host
        )

        self.python_executable_label: QLabel | None = None
        self.help_button: QPushButton | None = self.tab_header_template.help_button
        if spec.source_hint in {
            _DOCSTRINGS_GUI_SOURCE,
            _CONTEXT_COLLECTOR_GUI_SOURCE,
            _ERROR_MEMORY_GUI_SOURCE,
            _ENGINEERING_SAFETY_GUI_SOURCE,
            _FREEZE_AFTER_UPDATE_GUI_SOURCE,
            _DAILY_REFACTOR_GUI_SOURCE,
        }:
            refresh_handler = self._refresh_header_ai_models
            review_handler = None
            if spec.source_hint == _DOCSTRINGS_GUI_SOURCE:
                refresh_handler = self._refresh_docstring_header_ai_models
            elif spec.source_hint == _CONTEXT_COLLECTOR_GUI_SOURCE:
                review_handler = self._show_project_ai_review_first_check
            elif spec.source_hint == _FREEZE_AFTER_UPDATE_GUI_SOURCE:
                review_handler = self._freeze_feature_ai_review_first_check
            elif spec.source_hint == _ERROR_MEMORY_GUI_SOURCE:
                review_handler = None
            elif spec.source_hint == _ENGINEERING_SAFETY_GUI_SOURCE:
                review_handler = self._engineering_safety_ai_review_first_check
            self.tab_header_template.install_ai_group_blueprint(
                refresh_handler=refresh_handler,
                review_handler=review_handler,
            )

        outer.addLayout(self.header_row)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        outer.addWidget(line)

        status_source_row = QHBoxLayout()
        self.status_source_row = status_source_row
        self._show_status_source_row = spec.source_hint not in _HEADER_TEMPLATE_ONLY_SOURCES

        self.status_label = QLabel("Tool not loaded yet. It will load when this tab is opened.")
        self.status_label.setWordWrap(False)

        self.source_label: QLabel | None = QLabel(f"Source: {spec.source_hint}")
        self.source_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.source_label.setWordWrap(False)
        self.source_label.setStyleSheet(
            "border: 1px solid black; padding: 2px 6px;"
        )

        self._source_hover_window = None
        if self._show_status_source_row:
            status_source_row.addWidget(self.status_label, 0)
            status_source_row.addSpacing(24)
            status_source_row.addWidget(self.source_label, 0)

            source_hover_message = {
                _WORKFLOWS_GUI_SOURCE: (
                    "Workflow Review:\n"
                    f"Source: {_CANONICAL_PACKAGE_NAME}/manage_workflows/"
                    "manage_workflows_gui.py"
                ),
            }.get(spec.source_hint)
            if source_hover_message:
                self._source_hover_window = attach_floating_window(
                    self.source_label,
                    trigger_word="Source",
                    message=source_hover_message,
                    delay_ms=4000,
                )

        self._status_source_insert_index = status_source_row.count()
        if self._show_status_source_row:
            status_source_row.addStretch(1)
            outer.addLayout(status_source_row)
        else:
            self.status_label.hide()
            self.source_label.hide()


        self.load_button = QPushButton("Load this tool now")
        self.load_button.clicked.connect(self.load_tool)
        outer.addWidget(self.load_button)

        self.content_host = QWidget()
        self.content_layout = QVBoxLayout(self.content_host)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        outer.addWidget(self.content_host, 1)

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

    def _refresh_header_ai_models(self) -> None:
        """Refresh the template AI model dropdown from the local model registry."""
        combo = self.tab_header_template.ai_model_combo
        if combo is None:
            return

        previous = combo.currentText()
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Auto (first available Ollama model)")
        try:
            from kanda_reasoner_app.reasoner_engine.v10_model_registry import LocalModelRegistry

            models = LocalModelRegistry().list_models()
        except Exception:
            models = []
        for model_name in models:
            combo.addItem(model_name)
        index = combo.findText(previous)
        if index >= 0:
            combo.setCurrentIndex(index)
        combo.blockSignals(False)

    def _refresh_docstring_header_ai_models(self) -> None:
        """Refresh Docstring Assistant header models through Tab 3 settings."""
        widget = self._embedded_widget
        if widget is None:
            self._refresh_header_ai_models()
            return

        refresh = getattr(widget, "refresh_models", None)
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
        body_combo = getattr(widget, "_model_combo", None)
        if header_combo is None or body_combo is None:
            return

        self._copy_tab3_model_combo_to_header(widget)
        self._connect_signal(
            header_combo,
            "currentTextChanged",
            lambda text: self._apply_header_ai_model_to_tab3(widget, str(text or "")),
        )
        self._connect_signal(
            body_combo,
            "currentTextChanged",
            lambda _text: self._copy_tab3_model_combo_to_header(widget),
        )

    def _copy_tab3_model_combo_to_header(self, widget: QWidget) -> None:
        """Copy Tab 3 model combo items and current selection to the header."""
        header_combo = self.tab_header_template.ai_model_combo
        body_combo = getattr(widget, "_model_combo", None)
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

        body_combo = getattr(widget, "_model_combo", None)
        if body_combo is None:
            return

        items = self._combo_items(body_combo)
        add_item = getattr(body_combo, "addItem", None)
        if selected not in items and callable(add_item):
            add_item(selected)
        set_current = getattr(body_combo, "setCurrentText", None)
        if callable(set_current):
            set_current(selected)

    @staticmethod
    def _combo_current_text(combo: object) -> str:
        """Return the current combo text when available."""
        current_text = getattr(combo, "currentText", None)
        if callable(current_text):
            return str(current_text() or "").strip()
        return ""

    @staticmethod
    def _combo_items(combo: object) -> list[str]:
        """Return all visible combo-box items."""
        count_method = getattr(combo, "count", None)
        item_text = getattr(combo, "itemText", None)
        if not callable(count_method) or not callable(item_text):
            return []
        try:
            count = int(count_method())
        except (TypeError, ValueError):
            return []
        items: list[str] = []
        for index in range(max(0, count)):
            value = str(item_text(index) or "").strip()
            if value:
                items.append(value)
        return items

    @staticmethod
    def _replace_combo_items(combo: object, items: list[str], selected: str) -> None:
        """Replace combo items while preserving one selected text."""
        block_signals = getattr(combo, "blockSignals", None)
        clear = getattr(combo, "clear", None)
        add_item = getattr(combo, "addItem", None)
        find_text = getattr(combo, "findText", None)
        set_current_index = getattr(combo, "setCurrentIndex", None)
        if callable(block_signals):
            block_signals(True)
        try:
            if callable(clear):
                clear()
            if callable(add_item):
                for item in items:
                    add_item(item)
            if selected and callable(find_text) and callable(set_current_index):
                index = int(find_text(selected))
                if index >= 0:
                    set_current_index(index)
        finally:
            if callable(block_signals):
                block_signals(False)

    @staticmethod
    def _connect_signal(widget: object, signal_name: str, slot: object) -> None:
        """Connect one signal when both the signal and connect method exist."""
        signal = getattr(widget, signal_name, None)
        connect = getattr(signal, "connect", None)
        if callable(connect):
            connect(slot)

    def _show_project_ai_review_first_check(self) -> None:
        """Report the Show Project header AI review action state."""
        message = "AI Review First Check is not implemented for Show Project to AI yet."
        widget = self._embedded_widget
        if widget is not None:
            status_label = getattr(widget, "first_prompt_status_label", None)
            if status_label is not None:
                with contextlib.suppress(Exception):
                    status_label.setText(message)
            append_log = getattr(widget, "_append_log", None)
            if callable(append_log):
                with contextlib.suppress(Exception):
                    append_log(message)
        QMessageBox.information(self, "AI Review First Check", message)

    def _open_freeze_feature_help(self) -> None:
        """Open the embedded Freeze Feature After Update help window."""
        if not self.ensure_loaded():
            return
        widget = self._embedded_widget
        opener = getattr(widget, "_show_help_window", None)
        if callable(opener):
            opener()

    def _freeze_feature_ai_review_first_check(self) -> None:
        """Open the Freeze tab's local freeze entry workflow from the AI header."""
        if not self.ensure_loaded():
            return
        widget = self._embedded_widget
        opener = getattr(widget, "_open_local_freeze_entry_dialog", None)
        if callable(opener):
            opener()

    def _engineering_safety_ai_review_first_check(self) -> None:
        """Run the Engineering Safety first-check action from the AI header."""
        if not self.ensure_loaded():
            return
        widget = self._embedded_widget
        runner = getattr(widget, "run_ai_review_first_check", None)
        if callable(runner):
            runner()
            return
        QMessageBox.information(
            self,
            "AI Review First Check",
            "AI Review First Check is not available for Engineering Safety.",
        )


    def _move_tab1_project_root_controls_to_header_row(self, widget) -> None:
        """Move Tab 1 Project Root controls beside the Architecture Review header."""
        if self.spec.source_hint != _ARCHITECTURE_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_tab1_ai_review_controls_to_header_row(self, widget) -> None:
        """Move Tab 1 AI review controls beside the Architecture Review header."""
        if self.spec.source_hint != _ARCHITECTURE_GUI_SOURCE:
            return

        mover = getattr(widget, "move_ai_review_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.ai_group_layout)

    def _move_tab2_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Tab 2 Project Root controls into the header template."""
        if self.spec.source_hint != _WORKFLOWS_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_tab2_ai_review_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Tab 2 AI review controls into the header template."""
        if self.spec.source_hint != _WORKFLOWS_GUI_SOURCE:
            return

        mover = getattr(widget, "move_ai_review_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.ai_group_layout)


    def _move_tab3_project_root_controls_to_header_row(self, widget) -> None:
        """Move Tab 3 Project Root controls into the header template."""
        if self.spec.source_hint != _DOCSTRINGS_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_tab3_safe_mode_radio_to_header_row(self, widget) -> None:
        """Move Tab 3 Tab 1 audit source control into the header template."""
        if self.spec.source_hint != _DOCSTRINGS_GUI_SOURCE:
            return

        mover = getattr(widget, "move_safe_mode_radio_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)


    def _move_show_project_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Show Project to AI Project Root controls beside the tab header."""
        if self.spec.source_hint != _CONTEXT_COLLECTOR_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_error_memory_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Error Memory Project Root controls into the header template."""
        if self.spec.source_hint != _ERROR_MEMORY_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_engineering_safety_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Engineering Safety Project Root controls into the header template."""
        if self.spec.source_hint != _ENGINEERING_SAFETY_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_freeze_after_update_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Freeze Feature After Update Project Root controls into the header."""
        if self.spec.source_hint != _FREEZE_AFTER_UPDATE_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_refactor_report_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Refactor Report project-root controls into the header template."""
        if self.spec.source_hint != _DAILY_REFACTOR_GUI_SOURCE:
            return

        edit = getattr(widget, "domain_edit", None)
        if edit is None:
            return

        label = getattr(widget, "_header_project_root_label", None)
        if label is None:
            label = QLabel("Project Root:")
            label.setStyleSheet("color: #0B3D91; font-weight: bold; padding-left: 4px;")
            widget._header_project_root_label = label

        browse_button = self._find_refactor_report_project_root_button(widget)
        if browse_button is not None:
            browse_button.setText("browse project folder")
        controls = [label, edit]
        if browse_button is not None:
            controls.append(browse_button)

        target_index = self.tab_header_template.project_root_layout.count()
        self.tab_header_template.project_root_layout.insertSpacing(target_index, 12)
        offset = 1
        for control in controls:
            self._move_widget_to_layout(
                control,
                self.tab_header_template.project_root_layout,
                target_index + offset,
            )
            offset += 1

        self._hide_refactor_report_mode_a_group(widget)

    def _move_project_qa_project_root_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Project Q&A project-root controls into the header template."""
        if self.spec.source_hint != _PROJECT_QA_GUI_SOURCE:
            return

        mover = getattr(widget, "move_project_root_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.project_root_layout)

    def _move_project_qa_ai_controls_to_header_row(self, widget: QWidget) -> None:
        """Move Project Q&A local-AI controls into the header template."""
        if self.spec.source_hint != _PROJECT_QA_GUI_SOURCE:
            return

        mover = getattr(widget, "move_ai_runtime_controls_to_layout", None)
        if not callable(mover):
            return

        mover(self.tab_header_template.ai_group_layout)

    @staticmethod
    def _find_refactor_report_project_root_button(widget: QWidget) -> QPushButton | None:
        """Return the Refactor Report project-folder browse button."""
        find_children = getattr(widget, "findChildren", None)
        if not callable(find_children):
            return None
        for button in find_children(QPushButton):
            text = str(button.text() or "")
            if "Select Project Folder" in text:
                return button
        return None

    @staticmethod
    def _hide_refactor_report_mode_a_group(widget: QWidget) -> None:
        """Hide the old Refactor Report Mode A project-files body group."""
        find_children = getattr(widget, "findChildren", None)
        if not callable(find_children):
            return
        for group in find_children(QGroupBox):
            title = str(group.title() or "")
            if title.startswith("Mode A: from project files"):
                group.hide()
        domain_label = getattr(widget, "domain_label", None)
        if domain_label is not None:
            hide = getattr(domain_label, "hide", None)
            if callable(hide):
                hide()

    @staticmethod
    def _move_widget_to_layout(widget: QWidget, destination_layout: object, index: int) -> None:
        """Detach one widget from its current layout and insert it elsewhere."""
        parent = widget.parentWidget()
        parent_layout = parent.layout() if parent is not None else None
        if parent_layout is not None:
            with contextlib.suppress(Exception):
                parent_layout.removeWidget(widget)
        widget.setParent(None)
        insert_widget = getattr(destination_layout, "insertWidget", None)
        add_widget = getattr(destination_layout, "addWidget", None)
        if callable(insert_widget):
            insert_widget(index, widget, 0)
        elif callable(add_widget):
            add_widget(widget, 0)

    def load_tool(self) -> bool:
        """Load the tool.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        if self._loaded:
            return True

        self.status_label.setText("Loading tool...")
        self.status_label.setStyleSheet("")
        QApplication.processEvents()

        try:
            module = _first_imported_module(self.spec.module_candidates)
            widget_class = _first_existing_attr(module, self.spec.class_candidates)
            widget = widget_class()
            widget = _prepare_embedded_widget(widget)
            self._move_tab2_project_root_controls_to_header_row(widget)
            self._move_tab2_ai_review_controls_to_header_row(widget)
            self._move_tab1_project_root_controls_to_header_row(widget)
            self._move_tab1_ai_review_controls_to_header_row(widget)
            self._move_tab3_project_root_controls_to_header_row(widget)
            self._move_tab3_safe_mode_radio_to_header_row(widget)
            self._bind_tab3_header_ai_model_controls(widget)
            self._move_show_project_project_root_controls_to_header_row(widget)
            self._move_error_memory_project_root_controls_to_header_row(widget)
            self._move_engineering_safety_project_root_controls_to_header_row(widget)
            self._move_freeze_after_update_project_root_controls_to_header_row(widget)
            self._move_refactor_report_project_root_controls_to_header_row(widget)
            self._move_project_qa_project_root_controls_to_header_row(widget)
            self._move_project_qa_ai_controls_to_header_row(widget)
            self.content_layout.addWidget(widget)
            self._embedded_widget = widget

            self.status_label.setText("LOADED")
            self.status_label.setStyleSheet("color: #008000; font-weight: bold;")
            self.load_button.hide()

            self._loaded = True
            self._on_loaded(self.spec, widget)

            pending_loader = getattr(widget, "load_pending_ai_assisted_error_lesson_intake_now", None)
            if callable(pending_loader):
                try:
                    pending_loader()
                except Exception:
                    pass
                QTimer.singleShot(0, pending_loader)
                QTimer.singleShot(250, pending_loader)

            return True

        except (ImportError, AttributeError, RuntimeError, TypeError):
            error_panel = ToolLoadErrorPanel(
                title=self.spec.step_title,
                source_hint=self.spec.source_hint,
                error_text=traceback.format_exc(),
            )

            self.content_layout.addWidget(error_panel)
            self.status_label.setText("FAILED TO LOAD")
            self.status_label.setStyleSheet("color: #B00020; font-weight: bold;")
            self.load_button.setText("Retry loading")
            self._loaded = True
            return False

    def ensure_loaded(self) -> bool:
        """Support ensure loaded behavior.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        if not self._loaded:
            return self.load_tool()
        return True
