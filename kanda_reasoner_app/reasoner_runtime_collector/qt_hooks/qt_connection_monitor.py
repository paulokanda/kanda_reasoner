# project-path: kanda_reasoner_app/reasoner_runtime_collector/qt_hooks/qt_connection_monitor.py
"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'zm')
