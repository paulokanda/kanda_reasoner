"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'y')
DEFAULT_OUTPUT_JSON = globals()['DEFAULT_OUTPUT_JSON']; RuntimeCollectorWindow = globals()['RuntimeCollectorWindow']; main = globals()['main']
__all__ = ['DEFAULT_OUTPUT_JSON', 'RuntimeCollectorWindow', 'main']
