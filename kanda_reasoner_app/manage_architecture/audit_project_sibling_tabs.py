# project-path: kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py
"""Build Audit Project sibling tabs through their public Box contracts."""

from __future__ import annotations

from importlib import import_module

from .audit_project_workflow_review import create_embedded_workflow_review
from .full_audit_diagnostics_drillthrough import (
    install_full_audit_diagnostics_drillthrough,
)

__all__: list[str] = []

_ENGINEERING_SAFETY_LABEL = "Engineering Safety"
_ENGINEERING_DIAGNOSTICS_LABEL = "Engineering Diagnostics"
_WORKFLOW_REVIEW_LABEL = "Workflow Review"


def _build_audit_project_sibling_tabs(window: object) -> None:
    """Build Engineering Safety hierarchy and Workflow Review."""
    tab_widget = window._audit_project_subtab_widget
    root_provider = lambda: window._root_path_edit.text().strip()

    safety_module = import_module("reasoner_tools_gui_engineering_safety_panel")
    safety_factory = getattr(safety_module, "create_engineering_safety_panel")
    window._engineering_safety_page = safety_factory(
        project_root_provider=root_provider,
    )
    window._engineering_safety_page.setParent(tab_widget)
    tab_widget.addTab(window._engineering_safety_page, _ENGINEERING_SAFETY_LABEL)

    section_tabs = getattr(
        window._engineering_safety_page,
        "engineering_safety_section_tabs",
    )
    diagnostics_module = import_module(
        "kanda_reasoner_app.engineering_diagnostics_gui"
    )
    pontual_factory = getattr(
        diagnostics_module,
        "create_engineering_diagnostics_panel",
    )
    workspace_factory = getattr(
        diagnostics_module,
        "create_engineering_diagnostics_workspace",
    )
    workspace = workspace_factory(
        project_root_provider=root_provider,
        pontual_factory=pontual_factory,
    )
    workspace.setParent(section_tabs)
    section_tabs.addTab(workspace, _ENGINEERING_DIAGNOSTICS_LABEL)
    window._engineering_diagnostics_workspace = workspace
    window._full_engineering_diagnostics_page = (
        workspace.full_engineering_diagnostics_page
    )
    window._engineering_diagnostics_page = (
        workspace.pontual_engineering_diagnostics_page
    )
    window._root_path_edit.textChanged.connect(workspace.set_project_root)

    def select_diagnostics_tab() -> None:
        tab_widget.setCurrentWidget(window._engineering_safety_page)
        section_tabs.setCurrentWidget(workspace)
        workspace.select_pontual_engineering_diagnostics()

    window._full_audit_diagnostics_drillthrough = (
        install_full_audit_diagnostics_drillthrough(
            window._engineering_safety_page,
            window._engineering_diagnostics_page,
            project_root_provider=root_provider,
            select_diagnostics_tab=select_diagnostics_tab,
        )
    )

    window._workflow_review_page = create_embedded_workflow_review(
        parent=tab_widget,
        project_root_provider=root_provider,
    )
    window._root_path_edit.textChanged.connect(
        window._workflow_review_page._audit_project_root_sync
    )
    tab_widget.addTab(window._workflow_review_page, _WORKFLOW_REVIEW_LABEL)
