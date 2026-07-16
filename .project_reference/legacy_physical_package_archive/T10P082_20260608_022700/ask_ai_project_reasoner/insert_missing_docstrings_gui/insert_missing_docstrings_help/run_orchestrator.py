"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'l')
run = globals()['run']
__all__ = ['run']
