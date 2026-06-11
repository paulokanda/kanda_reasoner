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

def _install_deleted_legacy_context_collector_aliases():
    """Install aliases for deleted legacy context collector imports."""
    import importlib
    import sys

    legacy_root_name = "ask_ai" + "_project_reasoner"
    legacy_engine_name = legacy_root_name + ".project_reasoner_v10"
    legacy_collector_name = legacy_root_name + ".project_reasoner_v10_data_collector"
    old_canonical_collector_name = "kanda_reasoner_app.project_reasoner_v10_data_collector"

    canonical_root = importlib.import_module("kanda_reasoner_app")
    sys.modules.setdefault(legacy_root_name, canonical_root)

    try:
        canonical_engine = importlib.import_module("kanda_reasoner_app.reasoner_engine")
    except ModuleNotFoundError:
        canonical_engine = None

    if canonical_engine is not None:
        sys.modules.setdefault(legacy_engine_name, canonical_engine)
        setattr(canonical_root, "project_reasoner_v10", canonical_engine)

    canonical_collector = importlib.import_module(
        "kanda_reasoner_app.reasoner_context_collector"
    )
    sys.modules.setdefault(legacy_collector_name, canonical_collector)
    sys.modules.setdefault(old_canonical_collector_name, canonical_collector)
    setattr(canonical_root, "project_reasoner_v10_data_collector", canonical_collector)


_install_deleted_legacy_context_collector_aliases()

def _install_deleted_legacy_runtime_collector_aliases():
    """Install aliases for deleted legacy runtime collector imports."""
    import importlib
    import sys

    legacy_root_name = "ask_ai" + "_project_reasoner"
    legacy_engine_name = legacy_root_name + ".project_reasoner_v10"
    legacy_runtime_collector_name = legacy_root_name + ".project_reasoner_v10_runtime_collector"
    old_canonical_runtime_collector_name = (
        "kanda_reasoner_app.project_reasoner_v10_runtime_collector"
    )

    canonical_root = importlib.import_module("kanda_reasoner_app")
    sys.modules.setdefault(legacy_root_name, canonical_root)

    try:
        canonical_engine = importlib.import_module("kanda_reasoner_app.reasoner_engine")
    except ModuleNotFoundError:
        canonical_engine = None

    if canonical_engine is not None:
        sys.modules.setdefault(legacy_engine_name, canonical_engine)
        setattr(canonical_root, "project_reasoner_v10", canonical_engine)

    canonical_runtime_collector = importlib.import_module(
        "kanda_reasoner_app.reasoner_runtime_collector"
    )
    sys.modules.setdefault(legacy_runtime_collector_name, canonical_runtime_collector)
    sys.modules.setdefault(
        old_canonical_runtime_collector_name,
        canonical_runtime_collector,
    )
    setattr(
        canonical_root,
        "project_reasoner_v10_runtime_collector",
        canonical_runtime_collector,
    )


_install_deleted_legacy_runtime_collector_aliases()

load_payload(__name__, globals(), 'zp')
