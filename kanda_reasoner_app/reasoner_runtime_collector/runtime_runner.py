"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

def _install_runtime_runner_deleted_legacy_aliases():
    """Install aliases required by legacy payload code before payload loading."""
    import importlib
    import sys

    canonical_root = importlib.import_module("kanda_reasoner_app")
    canonical_runtime_collector = importlib.import_module(
        "kanda_reasoner_app.reasoner_runtime_collector"
    )
    canonical_runner = sys.modules.get(__name__)

    legacy_root_name = "ask_ai" + "_project_reasoner"
    legacy_collector_name = legacy_root_name + ".project_reasoner_v10_runtime_collector"
    legacy_runner_name = legacy_collector_name + ".runtime_runner"
    old_canonical_collector_name = (
        "kanda_reasoner_app.project_reasoner_v10_runtime_collector"
    )
    old_canonical_runner_name = old_canonical_collector_name + ".runtime_runner"

    sys.modules.setdefault(legacy_root_name, canonical_root)
    sys.modules.setdefault(legacy_collector_name, canonical_runtime_collector)
    sys.modules.setdefault(old_canonical_collector_name, canonical_runtime_collector)

    setattr(
        canonical_root,
        "project_reasoner_v10_runtime_collector",
        canonical_runtime_collector,
    )

    if canonical_runner is not None:
        sys.modules.setdefault(legacy_runner_name, canonical_runner)
        sys.modules.setdefault(old_canonical_runner_name, canonical_runner)


_install_runtime_runner_deleted_legacy_aliases()

load_payload(__name__, globals(), 'y')
DEFAULT_OUTPUT_JSON = globals()['DEFAULT_OUTPUT_JSON']; RuntimeCollectorWindow = globals()['RuntimeCollectorWindow']; main = globals()['main']
__all__ = ['DEFAULT_OUTPUT_JSON', 'RuntimeCollectorWindow', 'main']
