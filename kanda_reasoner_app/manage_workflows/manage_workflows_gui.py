# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_gui.py
"""Public entry point for the Workflow Review GUI.

This module is a normal readable facade. The older encoded backend payload
loader is deprecated for Workflow Review and is no longer used here.
"""

from __future__ import annotations


def _install_deleted_legacy_root_importlib_aliases():
    """Install in-process aliases for deleted legacy payload imports."""
    import importlib
    import sys

    legacy_root_name = "ask_ai" + "_project_reasoner"
    legacy_engine_name = legacy_root_name + ".project_reasoner_v10"

    canonical_root = importlib.import_module("kanda_reasoner_app")
    sys.modules.setdefault(legacy_root_name, canonical_root)

    try:
        canonical_engine = importlib.import_module("kanda_reasoner_app.reasoner_engine")
    except ModuleNotFoundError:
        return

    sys.modules.setdefault(legacy_engine_name, canonical_engine)
    setattr(canonical_root, "project_reasoner_v10", canonical_engine)


_install_deleted_legacy_root_importlib_aliases()


from .manage_workflows_gui_help.workflow_gui_constants import (
    _WORKFLOW_GUI_DEFAULT_MANAGER_NAME,
    _WORKFLOW_GUI_DEFAULT_PROJECT_ROOT,
)
from .manage_workflows_gui_help import (
    WorkflowManagerWindow,
    WorkflowRunWorker,
    get_recent_roots,
    get_recent_scripts,
    main,
    record_root,
    record_script,
)

DEFAULT_MANAGER_NAME = _WORKFLOW_GUI_DEFAULT_MANAGER_NAME
DEFAULT_PROJECT_ROOT = _WORKFLOW_GUI_DEFAULT_PROJECT_ROOT

__all__ = [
    "DEFAULT_MANAGER_NAME",
    "DEFAULT_PROJECT_ROOT",
    "WorkflowManagerWindow",
    "WorkflowRunWorker",
    "get_recent_roots",
    "get_recent_scripts",
    "main",
    "record_root",
    "record_script",
]


if __name__ == "__main__":
    raise SystemExit(main())
