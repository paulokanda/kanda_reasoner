"""Local-AI JSON working copy box for Project Reasoner.

This package owns creation, refresh, status, and validation for the local-AI
working copy of the canonical complete JSON.

It does not create the canonical complete JSON. The canonical JSON is produced
by the official Project Reasoner app workflow, especially:
4. Fourth step: collect project structure.

The public API is exposed lazily so running
``python -m kanda_reasoner_app.local_ai_json_working_copy.copy_manager``
does not pre-import the module and trigger a runpy RuntimeWarning.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "DEFAULT_CANONICAL_RELATIVE_PATH",
    "DEFAULT_LOCAL_AI_RELATIVE_PATH",
    "DEFAULT_METADATA_RELATIVE_PATH",
    "LocalAIJsonCopyResult",
    "LocalAIJsonPaths",
    "build_default_paths",
    "ensure_local_ai_copy",
    "get_local_ai_copy_status",
    "refresh_local_ai_copy",
    "write_local_ai_copy_metadata",
]

_COPY_MANAGER_EXPORTS = set(__all__)


def __getattr__(name: str) -> Any:
    """Return public objects from copy_manager without eager submodule import."""
    if name in _COPY_MANAGER_EXPORTS:
        module = import_module(".copy_manager", __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    """Return the stable public API for introspection."""
    return sorted(set(globals()) | _COPY_MANAGER_EXPORTS)
