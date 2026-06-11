"""Source-preserving compatibility facade."""

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


from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'v')
DEFAULT_MANAGER_NAME = globals()['DEFAULT_MANAGER_NAME']; WorkflowManagerWindow = globals()['WorkflowManagerWindow']; WorkflowRunWorker = globals()['WorkflowRunWorker']; get_recent_roots = globals()['get_recent_roots']; get_recent_scripts = globals()['get_recent_scripts']; main = globals()['main']; record_root = globals()['record_root']; record_script = globals()['record_script']
__all__ = ['DEFAULT_MANAGER_NAME', 'WorkflowManagerWindow', 'WorkflowRunWorker', 'get_recent_roots', 'get_recent_scripts', 'main', 'record_root', 'record_script']
