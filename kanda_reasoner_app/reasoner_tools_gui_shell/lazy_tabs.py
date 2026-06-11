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
from PySide6.QtGui import QDesktopServices, QFont, QIcon
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
    QSizePolicy,
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
    _docstring_worker_script_path,
    _first_existing_attr,
    _first_imported_module,
    _format_help_catalog_text,
    _help_catalog_path,
    _prepare_embedded_widget,
)
from .tool_specs import ToolSpec

__all__ = [
    "LazyToolTab",
]


_CANONICAL_PACKAGE_NAME = "kanda_reasoner_app"
_ARCHITECTURE_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/manage_architecture/manage_architecture_gui.py"
_WORKFLOWS_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/manage_workflows/manage_workflows_gui.py"
_DOCSTRINGS_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py"

from kanda_reasoner_app.templates.floating_windows.float_window import attach_floating_window

class LazyToolTab(QWidget):
    def __init__(self, spec: ToolSpec, on_loaded) -> None:
        super().__init__()
        self.spec = spec
        self._loaded = False
        self._embedded_widget: QWidget | None = None
        self._on_loaded = on_loaded
        self._help_dialog: QMainWindow | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(10)

        header_row = QHBoxLayout()

        banner = QLabel(spec.step_title)
        banner_font = QFont()
        banner_font.setBold(True)
        banner_font.setPointSize(12)
        banner.setFont(banner_font)
        banner.setWordWrap(True)
        header_row.addWidget(banner, 1)

        self.python_executable_label: QLabel | None = None
        if spec.source_hint in (
            _ARCHITECTURE_GUI_SOURCE,
            _WORKFLOWS_GUI_SOURCE,
        ):
            self.python_executable_label = QLabel(
                f"Python executable: {sys.executable}"
            )
            self.python_executable_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.python_executable_label.setWordWrap(False)
            header_row.addWidget(self.python_executable_label, 0)
            header_row.addSpacing(24)

        self.help_button: QPushButton | None = None
        if spec.help_catalog:
            self.help_button = QPushButton("Help")
            self.help_button.setStyleSheet("color: #003366; font-weight: bold;")
            self.help_button.clicked.connect(self._open_help_catalog)
            header_row.addWidget(self.help_button, 0, Qt.AlignRight)

        outer.addLayout(header_row)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        outer.addWidget(line)

        status_source_row = QHBoxLayout()
        self.status_source_row = status_source_row

        self.status_label = QLabel("Tool not loaded yet. It will load when this tab is opened.")
        self.status_label.setWordWrap(False)
        status_source_row.addWidget(self.status_label, 0)

        status_source_row.addSpacing(24)

        self.source_label = QLabel(f"Source: {spec.source_hint}")
        self.source_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.source_label.setWordWrap(False)
        self.source_label.setStyleSheet(
            "border: 1px solid black; padding: 2px 6px;"
        )
        status_source_row.addWidget(self.source_label, 0)

        source_hover_message = {
            _ARCHITECTURE_GUI_SOURCE: (
                "Tab 1:\n"
                f"Source: {_CANONICAL_PACKAGE_NAME}/manage_architecture/"
                "manage_architecture_gui.py"),
            _WORKFLOWS_GUI_SOURCE: (
                "Tab 2:\n"
                f"Source: {_CANONICAL_PACKAGE_NAME}/manage_workflows/"
                "manage_workflows_gui.py\n"
                "Worker script: manage_workflows.py"
            ),
        }.get(spec.source_hint)
        self._source_hover_window = None
        if source_hover_message:
            self._source_hover_window = attach_floating_window(
                self.source_label,
                trigger_word="Source",
                message=source_hover_message,
                delay_ms=4000,
            )

        worker_script_text: str | None = None
        if spec.source_hint == _DOCSTRINGS_GUI_SOURCE:
            worker_script_text = f"Worker Script: {_docstring_worker_script_path()}"

        if worker_script_text:
            status_source_row.addSpacing(24)

            self.worker_script_label = QLabel(worker_script_text)
            self.worker_script_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.worker_script_label.setWordWrap(False)
            self.worker_script_label.setStyleSheet(
                "border: 1px solid #0B3D91; color: #0B3D91; "
                "font-weight: bold; padding: 2px 6px;"
            )
            status_source_row.addWidget(self.worker_script_label, 0)

        self._status_source_insert_index = status_source_row.count()
        status_source_row.addStretch(1)

        outer.addLayout(status_source_row)


        self.load_button = QPushButton("Load this tool now")
        self.load_button.clicked.connect(self.load_tool)
        outer.addWidget(self.load_button)

        self.content_host = QWidget()
        self.content_layout = QVBoxLayout(self.content_host)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        outer.addWidget(self.content_host, 1)

    def _open_help_catalog(self) -> None:
        if not self.spec.help_catalog:
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


    def _move_tab1_worker_script_selector_to_status_row(self, widget) -> None:
        """Move Tab 1 worker-script controls beside LOADED / Source."""
        if self.spec.source_hint != _ARCHITECTURE_GUI_SOURCE:
            return

        mover = getattr(widget, "move_script_selector_to_layout", None)
        if not callable(mover):
            return

        insert_index = getattr(self, "_status_source_insert_index", None)
        mover(self.status_source_row, insert_index)

    def _move_tab2_worker_script_selector_to_status_row(self, widget: QWidget) -> None:
        """Move Tab 2 worker-script controls beside LOADED / Source."""
        if self.spec.source_hint != _WORKFLOWS_GUI_SOURCE:
            return

        mover = getattr(widget, "move_script_selector_to_layout", None)
        if not callable(mover):
            return

        mover(self.status_source_row, self._status_source_insert_index)


    def _move_tab3_safe_mode_radio_to_status_row(self, widget) -> None:
        """Move Tab 3 Safe Mode control beside LOADED / Source."""
        if self.spec.source_hint != _DOCSTRINGS_GUI_SOURCE:
            return

        mover = getattr(widget, "move_safe_mode_radio_to_layout", None)
        if not callable(mover):
            return

        insert_index = getattr(self, "_status_source_insert_index", None)
        mover(self.status_source_row, insert_index)

    def load_tool(self) -> bool:
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
            self._move_tab2_worker_script_selector_to_status_row(widget)
            self._move_tab1_worker_script_selector_to_status_row(widget)
            self._move_tab3_safe_mode_radio_to_status_row(widget)
            self.content_layout.addWidget(widget)
            self._embedded_widget = widget

            self.status_label.setText("LOADED")
            self.status_label.setStyleSheet("color: #008000; font-weight: bold;")
            self.load_button.hide()

            self._loaded = True
            self._on_loaded(self.spec, widget)
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
        if not self._loaded:
            return self.load_tool()
        return True
