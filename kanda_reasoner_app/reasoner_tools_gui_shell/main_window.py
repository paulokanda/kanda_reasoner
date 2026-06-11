"""Main KANDA Reasoner tools window implementation."""

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

from importlib import import_module as _qtcore_import_module


def _qt_core_attr(name: str):
    """Return a PySide6.QtCore attribute without a static QtCore import."""
    return getattr(_qtcore_import_module("PySide6.QtCore"), name)

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
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QInputDialog,
    QGroupBox,
    QFileDialog,
)

from .app_constants import (
    APP_DISPLAY_NAME,
    APP_ICON_PATH,
    APP_TITLE_DETAIL,
    _COLLECTOR_SUBTABS_TO_REMOVE,
    _HELP_FILENAME,
    _PREFS_FILENAME,
)
from .gui_support import (
    _find_button_by_text,
    _prune_named_subtabs,
    _replace_exact_label_text,
    _safe_disconnect,
)
from .ignore_rules_tab import IgnoreRulesTab
from .lazy_tabs import LazyToolTab
from .brain_navigator.contract import create_brain_navigator_tab
from .tab_navigation_controller import create_tab_navigation_controller
from kanda_reasoner_app.prompt_library_gui.prompt_library_tab import PromptLibraryTab
from .tool_specs import TOOLS, ToolSpec
from kanda_reasoner_app.project_root_resolver import resolve_active_project_root

__all__ = [
    "ReasonerToolsWindow",
]
from .main_window_help.window_help import _WindowHelpMixin
from .main_window_help.window_output_paths import _WindowOutputPathsMixin
from .main_window_help.window_project_root import _WindowProjectRootMixin
from .main_window_help.window_state import _WindowStateMixin
from .main_window_help.window_tool_patches import _WindowToolPatchesMixin
from .main_window_help.window_geometry import resize_window_for_primary_screen

class ReasonerToolsWindow(_WindowStateMixin, _WindowProjectRootMixin, _WindowOutputPathsMixin, _WindowToolPatchesMixin, _WindowHelpMixin, QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_DISPLAY_NAME)
        if APP_ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PATH)))
        resize_window_for_primary_screen(self)

        self._prefs = self._load_prefs()
        saved_project_root = self._normalize_project_root(
            self._prefs.get("last_project_root", "")
        )
        self.current_project_root: Path | None = resolve_active_project_root(
            persisted_root=saved_project_root
        )
        self._collector_widget: QWidget | None = None
        self._splitter_widget: QWidget | None = None
        self._daily_refactor_widget: QWidget | None = None
        self._help_dialog: QMainWindow | None = None
        self._is_propagating_project_root = False
        self._project_root_field_names = (
            "project_root_edit",
            "_project_root_edit",
            "root_path_edit",
            "_root_path_edit",
            "root_edit",
            "_root_edit",
            "root_combo",
            "_root_combo",
            "project_root_combo",
            "_project_root_combo",
            "domain_edit",
            "_domain_edit",
            "project_dir_edit",
            "_project_dir_edit",
        )

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(12)

        title_row_widget = QWidget()
        title_row = QHBoxLayout(title_row_widget)
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(4)
        title_row.setAlignment(_qt_core_attr("Qt").AlignCenter)

        title = QLabel(APP_DISPLAY_NAME)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(16)
        title.setFont(title_font)
        title.setAlignment(_qt_core_attr("Qt").AlignRight | _qt_core_attr("Qt").AlignVCenter)
        title_row.addWidget(title, 0)

        title_detail = QLabel(" - " + APP_TITLE_DETAIL)
        title_detail_font = QFont()
        title_detail_font.setPointSize(11)
        title_detail.setFont(title_detail_font)
        title_detail.setStyleSheet("color: #555555; font-weight: 600;")
        title_detail.setAlignment(_qt_core_attr("Qt").AlignLeft | _qt_core_attr("Qt").AlignVCenter)
        title_row.addWidget(title_detail, 0)

        root.addWidget(title_row_widget)

        subtitle = QLabel(
            "Unified workflow shell for architecture, workflows, docstrings, "
            "project structure collection, JSON splitting, daily refactor reporting, "
            "and AI reasoning."
        )
        subtitle.setAlignment(_qt_core_attr("Qt").AlignCenter)
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(False)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        root.addWidget(self.tabs, 1)

        self._pages: list[LazyToolTab] = []
        self._lazy_pages_by_tab_index: dict[int, LazyToolTab] = {}
        self._tab_index_by_tab_id: dict[str, int] = {}
        self._tab_navigation_controller = create_tab_navigation_controller(
            set_current_index=self.tabs.setCurrentIndex,
            get_current_index=self.tabs.currentIndex,
        )
        self.setUpdatesEnabled(False)
        try:
            for spec in TOOLS:
                self._add_registered_tab(spec)
        finally:
            self.setUpdatesEnabled(True)

        self._tab_navigation_controller.refresh_tab_index_map(
            self._tab_index_by_tab_id
        )
        self.tabs.setCurrentIndex(0)
        _qt_core_attr("QTimer").singleShot(0, self._load_initial_tab)

    def _register_tab_index(self, spec: ToolSpec, index: int) -> None:
        """Register one visible notebook index by stable tab ID."""
        if spec.tab_id:
            self._tab_index_by_tab_id[spec.tab_id] = index

    def _add_registered_tab(self, spec: ToolSpec) -> None:
        """Add one registered tab to the notebook."""
        if spec.tab_kind == "builtin_brain_navigator":
            self.brain_navigator_tab = create_brain_navigator_tab(
                open_tab_by_id=self._tab_navigation_controller.open_tab_by_id
            )
            index = self.tabs.addTab(self.brain_navigator_tab, spec.step_title)
            self._register_tab_index(spec, index)
            return

        if spec.tab_kind == "lazy_tool":
            page = LazyToolTab(spec, self._on_tool_loaded)
            self._pages.append(page)
            index = self.tabs.addTab(page, spec.step_title)
            self._lazy_pages_by_tab_index[index] = page
            self._register_tab_index(spec, index)
            return

        if spec.tab_kind == "builtin_ignore_rules":
            self.ignore_rules_tab = IgnoreRulesTab(self._prefs_path())
            self.ignore_rules_tab.set_project_root(self.current_project_root)
            index = self.tabs.addTab(self.ignore_rules_tab, spec.step_title)
            self._register_tab_index(spec, index)
            return

        if spec.tab_kind == "builtin_prompt_library":
            self.prompt_library_tab = PromptLibraryTab()
            index = self.tabs.addTab(self.prompt_library_tab, spec.step_title)
            self._register_tab_index(spec, index)
            return

        raise ValueError(f"Unknown GUI tab kind: {spec.tab_kind}")
