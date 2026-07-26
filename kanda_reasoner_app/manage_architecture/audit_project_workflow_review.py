# project-path: kanda_reasoner_app/manage_architecture/audit_project_workflow_review.py
"""Embed the existing Workflow Review owner inside Audit Project."""
from __future__ import annotations

from importlib import import_module
from typing import Callable

__all__ = ["create_embedded_workflow_review"]


def create_embedded_workflow_review(
    *,
    parent: object,
    project_root_provider: Callable[[], str],
) -> object:
    """Create Workflow Review as an Audit Project child without duplicating it."""
    module = import_module(
        "kanda_reasoner_app.manage_workflows.manage_workflows_gui"
    )
    window_class = getattr(module, "WorkflowManagerWindow")
    page = window_class()
    page.setParent(parent)
    page.setObjectName("audit_project_workflow_review_page")
    page.setWindowTitle("Workflow Review")

    root_combo = getattr(page, "_root_combo", None)
    if root_combo is None:
        raise RuntimeError("Workflow Review root selector is unavailable.")

    def sync_project_root(value: str | None = None) -> None:
        selected = (
            str(value).strip()
            if value is not None
            else str(project_root_provider()).strip()
        )
        if not selected:
            return
        if root_combo.findText(selected) < 0:
            root_combo.insertItem(0, selected)
        root_combo.setCurrentText(selected)

    sync_project_root()
    page._audit_project_root_sync = sync_project_root

    for attribute in ("_root_path_label", "_root_combo", "_browse_root_btn"):
        control = getattr(page, attribute, None)
        if control is not None:
            control.setVisible(False)

    return page
