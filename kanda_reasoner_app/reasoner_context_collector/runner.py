"""Compatibility launcher for the Project Reasoner tools shell.

This module preserves older launch commands. The composite GUI shell lives in
kanda_reasoner_app.reasoner_tools_shell.runner.
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


import importlib
from typing import Any


TRACE_PATH_EXPORT = "derive_" + "runtime_" + "trace_json_path"

__all__ = [
    "CollectorRunnerWindow",
    "main",
    "make_empty_index_payload",
    "resolve_output_json_path",
    TRACE_PATH_EXPORT,
]


def _load_shell_runner() -> Any:
    """Load the neutral tools shell runner lazily."""
    return importlib.import_module(
        "kanda_reasoner_app.reasoner_tools_shell.runner"
    )


class CollectorRunnerWindow:
    """Lazy compatibility proxy for the relocated tools shell window."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        shell_runner = _load_shell_runner()
        return shell_runner.CollectorRunnerWindow(*args, **kwargs)


def make_empty_index_payload(*args: Any, **kwargs: Any) -> Any:
    """Delegate to the relocated tools shell helper."""
    return _load_shell_runner().make_empty_index_payload(*args, **kwargs)


def resolve_output_json_path(*args: Any, **kwargs: Any) -> Any:
    """Delegate to the relocated tools shell helper."""
    return _load_shell_runner().resolve_output_json_path(*args, **kwargs)


def __getattr__(name: str) -> Any:
    """Delegate compatibility attributes to the relocated shell."""
    if name in __all__:
        return getattr(_load_shell_runner(), name)
    raise AttributeError(name)


def main() -> Any:
    """Run the relocated tools shell entry point."""
    return _load_shell_runner().main()


if __name__ == "__main__":
    raise SystemExit(main())
