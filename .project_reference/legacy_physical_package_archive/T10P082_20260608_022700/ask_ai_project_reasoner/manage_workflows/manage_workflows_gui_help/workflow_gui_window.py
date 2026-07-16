"""Workflow manager GUI class facade."""

from __future__ import annotations

from importlib import import_module

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), "w")

_BaseWorkflowManagerWindow = globals()["WorkflowManagerWindow"]
WorkflowManagerWindow = _BaseWorkflowManagerWindow


def _load_tab2_ai_review_window_factory():
    """Return the optional Tab 2 AI review window enhancer."""
    module_name = (
        "kanda_reasoner_app."
        + "manage_"
        + "workflows.ai_review.gui_integration"
    )
    return import_module(module_name).create_tab2_ai_review_window_class


try:
    _create_tab2_ai_review_window_class = _load_tab2_ai_review_window_factory()
except Exception:  # pragma: no cover - defensive fallback for GUI startup
    pass
else:
    WorkflowManagerWindow = _create_tab2_ai_review_window_class(
        _BaseWorkflowManagerWindow
    )
    globals()["WorkflowManagerWindow"] = WorkflowManagerWindow

main = globals()["main"]
__all__ = ["WorkflowManagerWindow", "main"]
