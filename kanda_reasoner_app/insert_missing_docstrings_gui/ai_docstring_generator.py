"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'm')
AIDocstringGenerator = globals()['AIDocstringGenerator']; GenerationResult = globals()['GenerationResult']; GenerationStats = globals()['GenerationStats']
__all__ = ['AIDocstringGenerator', 'GenerationResult', 'GenerationStats']
