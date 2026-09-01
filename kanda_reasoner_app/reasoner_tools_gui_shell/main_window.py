# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py
"""Main KANDA Reasoner tools window implementation."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from importlib import import_module as _qtcore_import_module


def _qt_core_attr(name: str):
    """Return a PySide6.QtCore attribute without a static QtCore import."""
    return getattr(_qtcore_import_module("PySide6.QtCore"), name)

from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from .app_constants import (
    APP_DISPLAY_NAME,
    APP_ICON_PATH,
    APP_TITLE_DETAIL,
)
from .ignore_rules_tab import IgnoreRulesTab
from .lazy_tabs import LazyToolTab
from .brain_navigator.contract import create_brain_navigator_tab
from .tab_navigation_controller import create_tab_navigation_controller
from kanda_reasoner_app.prompt_library_gui.prompt_library_tab import PromptLibraryTab
from kanda_reasoner_app.reasoner_tools_gui_shell.kanda_memo_prompts.contract import (
    create_kanda_memo_prompts_tab,
)
from .tool_specs import TOOLS, ToolSpec
from kanda_reasoner_app.project_root_resolver import resolve_observed_project_root
from kanda_reasoner_app.project_selection_registry import (
    ProjectSelectionRegistry,
    ProjectSelectionRegistryError,
)
from kanda_reasoner_app.external_ai_configuration import (
    ExternalAIConfigurationController,
    install_application_external_ai_configuration,
)
from kanda_reasoner_app.local_ai_configuration import (
    LocalAIConfigurationController,
    install_application_local_ai_configuration,
)
from kanda_reasoner_app.web_ai_configuration import (
    WebAIConfigurationController,
    install_application_web_ai_configuration,
)
from kanda_reasoner_app.portable_smoke_runtime_report import (
    PORTABLE_SMOKE_REPORT_PATH_ENV,
    PORTABLE_SMOKE_REPORT_ROOT_ENV,
    PORTABLE_SMOKE_REPORT_TOKEN_ENV,
    record_portable_smoke_event,
)

__all__ = [
    "ReasonerToolsWindow",
]

_PORTABLE_SMOKE_REQUIRED_TAB_IDS = (
    "project_structure_map",
    "project_qa",
    "error_memory",
)
_PORTABLE_FINAL_ACCEPTANCE_REQUIRED_TAB_IDS = (
    "architecture_review",
    "project_structure_3d",
    "config_web_ai",
)
from .main_window_help.window_help import _WindowHelpMixin
from .main_window_help.window_output_paths import _WindowOutputPathsMixin
from .main_window_help.window_project_root import _WindowProjectRootMixin
from .main_window_help.window_state import _WindowStateMixin
from .main_window_help.window_tool_patches import _WindowToolPatchesMixin
from .main_window_help.window_geometry import (
    resize_window_for_primary_screen,
    restore_window_size_from_prefs,
    widen_window_to_screen_width_floor,
)

class ReasonerToolsWindow(
    _WindowStateMixin,
    _WindowProjectRootMixin,
    _WindowOutputPathsMixin,
    _WindowToolPatchesMixin,
    _WindowHelpMixin,
    QMainWindow,
):
    """Represent reasoner tools window."""
    
    def __init__(self) -> None:
        """Support init behavior.
        """
        
        super().__init__()
        self.setWindowTitle(APP_DISPLAY_NAME)
        if APP_ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PATH)))
        self.setProperty("kandaGeometryGuardExempt", True)
        self.setProperty("kandaMainWindowFixedSize", True)
        self._prefs = self._load_prefs()
        if not restore_window_size_from_prefs(self, self._prefs):
            resize_window_for_primary_screen(self)
        widen_window_to_screen_width_floor(self)
        self.setFixedSize(self.size())

        self._project_switch_ticket = 0
        self._project_selection_registry = ProjectSelectionRegistry()
        try:
            observation = self._project_selection_registry.load_current_observation(
                selection_ticket=self._project_switch_ticket
            )
            boundary = self._project_selection_registry.resolve_current_boundary()
        except ProjectSelectionRegistryError:
            observation = None
            boundary = None

        if observation is None:
            legacy_root = resolve_observed_project_root(
                persisted_root=self._normalize_project_root(
                    self._prefs.get("last_project_root", "")
                )
            )
            if legacy_root is not None:
                boundary = (
                    self._project_selection_registry
                    .register_legacy_external_root(legacy_root)
                )
                observation = (
                    self._project_selection_registry.load_current_observation(
                        selection_ticket=self._project_switch_ticket
                    )
                )

        self.current_project_observation = observation
        self.current_project_boundary = boundary
        self.current_project_root: Path | None = (
            observation.project_root if observation is not None else None
        )
        self._web_ai_configuration = WebAIConfigurationController(self)
        install_application_web_ai_configuration(self._web_ai_configuration)
        self._external_ai_configuration = ExternalAIConfigurationController(self)
        install_application_external_ai_configuration(
            self._external_ai_configuration
        )
        self._local_ai_configuration = LocalAIConfigurationController(self)
        install_application_local_ai_configuration(self._local_ai_configuration)
        self._collector_widget: QWidget | None = None
        self._daily_refactor_widget: QWidget | None = None
        self._loaded_tools_by_tab_id: dict[str, QWidget] = {}
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
        title.setAlignment(
            _qt_core_attr("Qt").AlignRight
            | _qt_core_attr("Qt").AlignVCenter
        )
        title_row.addWidget(title, 0)

        title_detail = QLabel(" - " + APP_TITLE_DETAIL)
        title_detail_font = QFont()
        title_detail_font.setPointSize(11)
        title_detail.setFont(title_detail_font)
        title_detail.setStyleSheet("color: #555555; font-weight: 600;")
        title_detail.setAlignment(
            _qt_core_attr("Qt").AlignLeft
            | _qt_core_attr("Qt").AlignVCenter
        )
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

        self.select_project_button = QPushButton("Select Active Project", central)
        self.select_project_button.clicked.connect(self._select_active_project)
        self.select_project_button.hide()
        self.eject_project_button = QPushButton("Eject Active Project", central)
        self.eject_project_button.clicked.connect(self._eject_active_project)
        self.eject_project_button.hide()
        self._refresh_active_project_controls()

        self.tabs = QTabWidget()
        self.tabs.setMinimumSize(0, 0)
        self.tabs.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.tabBar().setUsesScrollButtons(True)
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
        self._web_ai_configuration.open_configuration_requested.connect(
            lambda: self._tab_navigation_controller.open_tab_by_id("config_web_ai")
        )
        self._local_ai_configuration.open_configuration_requested.connect(
            lambda: self._tab_navigation_controller.open_tab_by_id("config_web_ai")
        )
        self.setUpdatesEnabled(False)
        try:
            for spec in self._ordered_tool_specs(TOOLS):
                self._add_registered_tab(spec)
        finally:
            self.setUpdatesEnabled(True)

        self._refresh_tab_indexes_from_widgets()
        self.tabs.setCurrentIndex(0)
        timer = _qt_core_attr("QTimer")
        timer.singleShot(0, self._load_initial_tab)
        if self._portable_smoke_runtime_reporting_enabled():
            timer.singleShot(1, self._preload_portable_smoke_tabs)

    @staticmethod
    def _portable_smoke_runtime_reporting_enabled() -> bool:
        """Return whether token-bound Portable runtime smoke reporting is active."""
        required = (
            PORTABLE_SMOKE_REPORT_PATH_ENV,
            PORTABLE_SMOKE_REPORT_ROOT_ENV,
            PORTABLE_SMOKE_REPORT_TOKEN_ENV,
        )
        return all(str(os.environ.get(name, "") or "").strip() for name in required)

    def _preload_portable_smoke_tabs(self) -> None:
        """Activate required lazy tabs automatically during Portable smoke only."""
        for tab_id in (
            _PORTABLE_SMOKE_REQUIRED_TAB_IDS
            + _PORTABLE_FINAL_ACCEPTANCE_REQUIRED_TAB_IDS
        ):
            result = self._tab_navigation_controller.open_tab_by_id(tab_id)
            if result.success:
                continue
            record_portable_smoke_event(
                status="FAIL",
                kind="smoke_tab_preload",
                source=tab_id,
                message=result.reason,
            )

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
            page = LazyToolTab(
                spec,
                self._on_tool_loaded,
                select_project_handler=self._select_active_project,
                eject_project_handler=self._eject_active_project,
                active_project_provider=lambda: self.current_project_root,
            )
            self._pages.append(page)
            index = self.tabs.addTab(page, spec.step_title)
            self._lazy_pages_by_tab_index[index] = page
            self._register_tab_index(spec, index)
            return

        if spec.tab_kind == "builtin_ignore_rules":
            self.ignore_rules_tab = IgnoreRulesTab(
                self._prefs_path(),
                select_project_handler=self._select_active_project,
                eject_project_handler=self._eject_active_project,
            )
            self.ignore_rules_tab.set_project_root(self.current_project_root)
            self._apply_project_widget_enabled_state(
                "exclusion_rules",
                self.ignore_rules_tab,
            )
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

        if spec.tab_kind == "builtin_kanda_memo_prompts":
            self.kanda_memo_prompts_tab = create_kanda_memo_prompts_tab(
                project_root=self.current_project_root,
            )
            self._loaded_tools_by_tab_id[spec.tab_id] = (
                self.kanda_memo_prompts_tab
            )
            self._apply_project_widget_enabled_state(
                spec.tab_id, self.kanda_memo_prompts_tab
            )
            index = self.tabs.addTab(
                self.kanda_memo_prompts_tab,
                spec.step_title,
            )
            self._register_tab_index(spec, index)
            return

        raise ValueError(f"Unknown GUI tab kind: {spec.tab_kind}")
