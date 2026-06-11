"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'f')
collect_missing_docstring_insertions = globals()['collect_missing_docstring_insertions']
__all__ = ['collect_missing_docstring_insertions']
