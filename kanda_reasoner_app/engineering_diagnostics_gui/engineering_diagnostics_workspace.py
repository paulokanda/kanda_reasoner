# project-path: kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py
"""Two-level Engineering Diagnostics workspace for Engineering Safety."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from .controller import EngineeringDiagnosticsController
from .engineering_diagnostics_tab import create_engineering_diagnostics_panel
from .full_engineering_diagnostics_tab import (
    create_full_engineering_diagnostics_panel,
)

__all__ = ["create_engineering_diagnostics_workspace"]


def _tool_root() -> Path:
    return Path(__file__).resolve().parents[2]


def create_engineering_diagnostics_workspace(
    project_root_provider: Callable[[], object] | None = None,
    *,
    controller: EngineeringDiagnosticsController | None = None,
    pontual_factory: Callable[..., object] | None = None,
    defer_initial_refresh: bool = False,
):
    """Create Full and Pontual Diagnostics over one shared public controller."""
    from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

    workspace = QWidget()
    workspace.setObjectName("engineering_diagnostics_workspace")
    layout = QVBoxLayout(workspace)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)

    tabs = QTabWidget(workspace)
    tabs.setObjectName("engineering_diagnostics_mode_tabs")
    active_controller = controller or EngineeringDiagnosticsController(
        tool_root=_tool_root()
    )
    full_page = create_full_engineering_diagnostics_panel(
        project_root_provider=project_root_provider,
        controller=active_controller,
    )
    pontual_builder = pontual_factory or create_engineering_diagnostics_panel
    pontual_page = pontual_builder(
        project_root_provider=project_root_provider,
        controller=active_controller,
        defer_initial_refresh=defer_initial_refresh,
    )
    full_index = tabs.addTab(full_page, "Full Engineering Diagnostics")
    tabs.addTab(pontual_page, "Pontual Engineering Diagnostics")
    tabs.setTabVisible(full_index, False)
    tabs.setCurrentWidget(pontual_page)
    layout.addWidget(tabs, 1)

    def set_project_root(value: object = None) -> None:
        full_page.set_project_root(value)
        pontual_page.set_project_root(value)

    def select_pontual() -> None:
        tabs.setCurrentWidget(pontual_page)

    def project_scope_switch_block_reason() -> str:
        for page in (full_page, pontual_page):
            blocker = getattr(page, "project_scope_switch_block_reason", None)
            if callable(blocker):
                reason = str(blocker() or "").strip()
                if reason:
                    return reason
        return ""

    def request_project_scope_settlement() -> None:
        for page in (full_page, pontual_page):
            requester = getattr(page, "request_project_scope_settlement", None)
            if callable(requester):
                requester()

    def shutdown_ready() -> bool:
        for page in (full_page, pontual_page):
            ready = getattr(page, "shutdown_ready", None)
            if callable(ready) and not bool(ready()):
                return False
        return True

    def begin_shutdown() -> bool:
        ready = True
        for page in (full_page, pontual_page):
            begin = getattr(page, "begin_shutdown", None)
            if callable(begin):
                ready = bool(begin()) and ready
        return ready and shutdown_ready()

    workspace.set_project_root = set_project_root
    workspace.select_pontual_engineering_diagnostics = select_pontual
    workspace.project_scope_switch_block_reason = project_scope_switch_block_reason
    workspace.request_project_scope_settlement = request_project_scope_settlement
    workspace.begin_shutdown = begin_shutdown
    workspace.shutdown_ready = shutdown_ready
    workspace.engineering_diagnostics_mode_tabs = tabs
    workspace.full_engineering_diagnostics_page = full_page
    workspace.pontual_engineering_diagnostics_page = pontual_page
    workspace.engineering_diagnostics_controller = active_controller
    return workspace
