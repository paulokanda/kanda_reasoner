"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'v')
DEFAULT_MANAGER_NAME = globals()['DEFAULT_MANAGER_NAME']; WorkflowManagerWindow = globals()['WorkflowManagerWindow']; WorkflowRunWorker = globals()['WorkflowRunWorker']; get_recent_roots = globals()['get_recent_roots']; get_recent_scripts = globals()['get_recent_scripts']; main = globals()['main']; record_root = globals()['record_root']; record_script = globals()['record_script']
__all__ = ['DEFAULT_MANAGER_NAME', 'WorkflowManagerWindow', 'WorkflowRunWorker', 'get_recent_roots', 'get_recent_scripts', 'main', 'record_root', 'record_script']
