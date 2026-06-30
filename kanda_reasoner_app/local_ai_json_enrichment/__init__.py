# project-path: kanda_reasoner_app/local_ai_json_enrichment/__init__.py
"""Local-AI JSON enrichment box for Project Reasoner.

This package writes local-only enrichment into the local-AI working JSON.

It never writes to the canonical complete JSON generated for the selected
project root under project_analysis_evidence/json_complete.

The public API is exposed lazily so running
``python -m kanda_reasoner_app.local_ai_json_enrichment.enrichment_writer``
does not pre-import the module and trigger a runpy RuntimeWarning.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "DEFAULT_ENRICHMENT_KEY",
    "LocalAIJsonEnrichmentResult",
    "enrich_local_ai_json_with_live_sources",
    "load_local_ai_enrichment",
]

_EXPORTS = set(__all__)


def __getattr__(name: str) -> Any:
    """Return public objects from enrichment_writer without eager import."""
    if name in _EXPORTS:
        module = import_module(".enrichment_writer", __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    """Return the stable public API for introspection."""
    return sorted(set(globals()) | _EXPORTS)
