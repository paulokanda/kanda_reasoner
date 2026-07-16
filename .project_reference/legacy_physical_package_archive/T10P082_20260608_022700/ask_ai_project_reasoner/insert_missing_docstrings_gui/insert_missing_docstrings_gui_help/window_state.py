"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 't')
# legacy-test anchors: QRadioButton; _tab1_audit_docstring_radio; get missing docstring from Tab1 audit.; setChecked(True); setStyleSheet; font.setBold(True); color: red; font-weight: bold;
current_prefs_payload = globals()['current_prefs_payload']; initialize_window = globals()['initialize_window']
__all__ = ['current_prefs_payload', 'initialize_window']
