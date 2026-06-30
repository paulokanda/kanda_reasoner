# project-path: kanda_reasoner_app/live_source_verification/__init__.py
"""Live source verification box for Project Reasoner.

This package verifies current files under a selected PROJECT_ROOT.

It reads live source files as final implementation truth, but it does not
modify source files, canonical JSON, local-AI JSON, retriever logic, prompt
logic, AI bridge logic, GUI logic, or collector output.

The public API is exposed lazily so running
``python -m kanda_reasoner_app.live_source_verification.verifier`` does not
pre-import the verifier module and trigger a runpy RuntimeWarning.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "DEFAULT_CONTEXT_LINES",
    "DEFAULT_MAX_TEXT_FILE_SIZE_BYTES",
    "LiveSourcePathResult",
    "LiveSourceSnippetResult",
    "batch_verify_sources",
    "extract_live_source_snippet",
    "read_live_source_text",
    "verify_live_source_path",
]

_VERIFIER_EXPORTS = set(__all__)


def __getattr__(name: str) -> Any:
    """Return public objects from verifier without eager submodule import."""
    if name in _VERIFIER_EXPORTS:
        module = import_module(".verifier", __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    """Return the stable public API for introspection."""
    return sorted(set(globals()) | _VERIFIER_EXPORTS)
