"""Source-preserving compatibility facade."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), 'r')
browse_report_path = globals()['browse_report_path']; browse_root = globals()['browse_root']; confirm_write = globals()['confirm_write']; save_output = globals()['save_output']; show_help = globals()['show_help']
__all__ = ['browse_report_path', 'browse_root', 'confirm_write', 'save_output', 'show_help']
