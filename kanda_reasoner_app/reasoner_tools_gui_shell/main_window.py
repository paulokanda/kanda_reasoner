# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py
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
    """Represent reasoner tools window."""
    
    def __init__(self) -> None:
        """Support init behavior.
        """
        
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
            "Show Project to AI handoff generation, integrated refactor "
            "evidence, and AI reasoning."
        )
        subtitle.setAlignment(_qt_core_attr("Qt").AlignCenter)
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self.tabs.tabBar().tabMoved.connect(self._on_tab_moved)
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
            for spec in self._ordered_tool_specs(TOOLS):
                self._add_registered_tab(spec)
        finally:
            self.setUpdatesEnabled(True)

        self._refresh_tab_indexes_from_widgets()
        self.tabs.setCurrentIndex(0)
        _qt_core_attr("QTimer").singleShot(0, self._load_initial_tab)

    def _ordered_tool_specs(self, specs: Iterable[ToolSpec]) -> tuple[ToolSpec, ...]:
        """Return visible tool specs in the persisted user tab order.

        Saved tab order is advisory. Unknown or hidden tab IDs are ignored,
        and newly added visible tabs are appended in canonical registry order.
        """
        canonical_specs = tuple(
            spec for spec in specs if spec.visible_in_shell
        )
        saved_order = self._prefs.get("tab_order", [])
        if not isinstance(saved_order, list):
            return canonical_specs

        specs_by_id = {
            str(spec.tab_id): spec
            for spec in canonical_specs
            if spec.tab_id
        }
        selected_ids: set[str] = set()
        ordered_specs: list[ToolSpec] = []

        for raw_tab_id in saved_order:
            tab_id = str(raw_tab_id).strip()
            spec = specs_by_id.get(tab_id)
            if spec is None or tab_id in selected_ids:
                continue
            ordered_specs.append(spec)
            selected_ids.add(tab_id)

        for spec in canonical_specs:
            tab_id = str(spec.tab_id or "").strip()
            if tab_id and tab_id in selected_ids:
                continue
            ordered_specs.append(spec)

        return tuple(ordered_specs)

    def _register_tab_index(self, spec: ToolSpec, index: int) -> None:
        """Register one visible notebook index by stable tab ID."""
        if spec.tab_id:
            self.tabs.tabBar().setTabData(index, spec.tab_id)
            self._tab_index_by_tab_id[spec.tab_id] = index

    def _refresh_tab_indexes_from_widgets(self) -> None:
        """Refresh tab ID and lazy-page maps after user reordering."""
        tab_index_by_id: dict[str, int] = {}
        lazy_pages_by_tab_index: dict[int, LazyToolTab] = {}

        for index in range(self.tabs.count()):
            tab_id = str(self.tabs.tabBar().tabData(index) or "").strip()
            if tab_id:
                tab_index_by_id[tab_id] = index

            widget = self.tabs.widget(index)
            if isinstance(widget, LazyToolTab):
                lazy_pages_by_tab_index[index] = widget

        self._tab_index_by_tab_id = tab_index_by_id
        self._lazy_pages_by_tab_index = lazy_pages_by_tab_index
        self._tab_navigation_controller.refresh_tab_index_map(
            self._tab_index_by_tab_id
        )

    def _current_tab_order(self) -> list[str]:
        """Return the current visible tab order as stable tab IDs."""
        tab_order: list[str] = []
        for index in range(self.tabs.count()):
            tab_id = str(self.tabs.tabBar().tabData(index) or "").strip()
            if tab_id:
                tab_order.append(tab_id)
        return tab_order

    def _remember_tab_order(self) -> None:
        """Persist the current user-visible tab order."""
        self._prefs["tab_order"] = self._current_tab_order()
        self._save_prefs()

    def _on_tab_moved(self, _from_index: int, _to_index: int) -> None:
        """Persist tab reordering and keep tab navigation maps current."""
        self._refresh_tab_indexes_from_widgets()
        self._remember_tab_order()

    def _add_registered_tab(self, spec: ToolSpec) -> None:
        """Add one registered tab to the notebook."""
        if spec.tab_kind == "builtin_brain_navigator":
            self.brain_navigator_tab = create_brain_navigator_tab(
                open_tab_by_id=self._tab_navigation_controller.open_tab_by_id,
                can_open_tab_id=self._tab_navigation_controller.can_open_tab,
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
            if hasattr(self.ignore_rules_tab, "project_root_edit"):
                self._bind_project_root_field(self.ignore_rules_tab.project_root_edit)
                if self.current_project_root is not None:
                    self._set_project_root_field_text(
                        self.ignore_rules_tab.project_root_edit,
                        self.current_project_root,
                    )
            index = self.tabs.addTab(self.ignore_rules_tab, spec.step_title)
            self._register_tab_index(spec, index)
            return

        if spec.tab_kind == "builtin_prompt_library":
            self.prompt_library_tab = PromptLibraryTab()
            index = self.tabs.addTab(self.prompt_library_tab, spec.step_title)
            self._register_tab_index(spec, index)
            return

        raise ValueError(f"Unknown GUI tab kind: {spec.tab_kind}")
