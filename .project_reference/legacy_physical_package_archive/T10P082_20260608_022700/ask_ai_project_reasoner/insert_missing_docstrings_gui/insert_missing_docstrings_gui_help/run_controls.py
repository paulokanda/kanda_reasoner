"""Compatibility facade for Tab 3 scan-only run controls."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload
from kanda_reasoner_app.tab3_manual_review_runtime.scan_only_workflow import (
    run_scan_only_mode,
    run_scan_selected_mode,
)

load_payload(__name__, globals(), 's')

_legacy_run_selected_mode = globals()["run_selected_mode"]
_legacy_run_mode = globals()["run_mode"]


def run_selected_mode(self) -> None:
    """Run the scan-only Tab 3 workflow."""
    run_scan_selected_mode(self, _legacy_run_mode)


def run_mode(self, mode: str) -> None:
    """Run Tab 3 in scan mode regardless of legacy mode input."""
    run_scan_only_mode(self, mode, _legacy_run_mode)


append_text = globals()['append_text']
cleanup_worker = globals()['cleanup_worker']
effective_report_path = globals()['effective_report_path']
handle_worker_error = globals()['handle_worker_error']
handle_worker_progress = globals()['handle_worker_progress']
handle_worker_success = globals()['handle_worker_success']
stop_running_selected_mode = globals()['stop_running_selected_mode']

__all__ = [
    'append_text',
    'cleanup_worker',
    'effective_report_path',
    'handle_worker_error',
    'handle_worker_progress',
    'handle_worker_success',
    'run_mode',
    'run_selected_mode',
    'stop_running_selected_mode',
]
