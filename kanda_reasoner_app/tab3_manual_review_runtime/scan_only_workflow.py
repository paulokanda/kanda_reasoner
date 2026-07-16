# project-path: kanda_reasoner_app/tab3_manual_review_runtime/scan_only_workflow.py
"""Scan-only workflow helpers for the Tab 3 missing-docstring handler."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Literal

from kanda_reasoner_app.tab3_manual_review_runtime import scan_controls_runtime
from kanda_reasoner_app.tab3_manual_review_runtime import scan_report_lifecycle_runtime

__all__ = [
    "SCAN_MODE",
    "SCAN_DIFF_WRITE_MODES",
    "DEFAULT_SCAN_REPORT_NAME",
    "configure_scan_diff_write_controls",
    "configure_scan_only_controls",
    "ensure_scan_report_path",
    "prepare_scan_report_lifecycle",
    "refresh_selected_mode_controls",
    "run_scan_only_mode",
    "run_scan_selected_mode",
    "use_project_root_as_scan_scope",
]

SCAN_MODE = "scan"
SCAN_DIFF_WRITE_MODES = ("scan", "diff", "write")
DEFAULT_SCAN_REPORT_NAME = "missing_docstrings_report.jsonl"
ScanReportLifecycle = Literal["ready", "loaded", "cancelled"]


def configure_scan_diff_write_controls(window: object) -> None:
    """Expose the full scan/diff/write workflow controls."""
    scan_controls_runtime.configure_scan_diff_write_controls(window)


def refresh_selected_mode_controls(
    window: object,
    mode: str | None = None,
) -> None:
    """Refresh button text and write guard visibility for the selected mode."""
    scan_controls_runtime.refresh_selected_mode_controls(window, mode)


def configure_scan_only_controls(window: object) -> None:
    """Force legacy mode widgets to the scan-only workflow state."""
    scan_controls_runtime.configure_scan_only_controls(window)


def ensure_scan_report_path(
    owner: object,
    chooser: Callable[[object, Path], str | Path | None] | None = None,
) -> bool:
    """Ensure scan output has a report path before running."""
    return scan_report_lifecycle_runtime.ensure_scan_report_path(owner, chooser)


def prepare_scan_report_lifecycle(
    owner: object,
    reuse_prompt: Callable[[object, Path], bool] | None = None,
    previous_action_prompt: Callable[[object, Path], str] | None = None,
    folder_chooser: Callable[[object, Path], str | Path | None] | None = None,
    now_provider: Callable[[], datetime] | None = None,
) -> ScanReportLifecycle:
    """Prepare report lifecycle before launching a new scan."""
    return scan_report_lifecycle_runtime.prepare_scan_report_lifecycle(
        owner,
        reuse_prompt=reuse_prompt,
        previous_action_prompt=previous_action_prompt,
        folder_chooser=folder_chooser,
        now_provider=now_provider,
    )


def run_scan_selected_mode(
    owner: object,
    legacy_run_mode: Callable[[object, str], Any],
    chooser: Callable[[object, Path], str | Path | None] | None = None,
    reuse_prompt: Callable[[object, Path], bool] | None = None,
    previous_action_prompt: Callable[[object, Path], str] | None = None,
    folder_chooser: Callable[[object, Path], str | Path | None] | None = None,
) -> Any:
    """Run Tab 3 scan regardless of any legacy selected mode."""
    configure_scan_only_controls(owner)
    use_project_root_as_scan_scope(owner)
    if chooser is not None:
        if not ensure_scan_report_path(owner, chooser=chooser):
            return None
        return legacy_run_mode(owner, SCAN_MODE)

    lifecycle = prepare_scan_report_lifecycle(
        owner,
        reuse_prompt=reuse_prompt,
        previous_action_prompt=previous_action_prompt,
        folder_chooser=folder_chooser,
    )
    if lifecycle != "ready":
        return None
    return legacy_run_mode(owner, SCAN_MODE)


def run_scan_only_mode(
    owner: object,
    mode: str,
    legacy_run_mode: Callable[[object, str], Any],
    chooser: Callable[[object, Path], str | Path | None] | None = None,
    reuse_prompt: Callable[[object, Path], bool] | None = None,
    previous_action_prompt: Callable[[object, Path], str] | None = None,
    folder_chooser: Callable[[object, Path], str | Path | None] | None = None,
) -> Any:
    """Clamp legacy Tab 3 mode execution to scan only."""
    del mode
    configure_scan_only_controls(owner)
    use_project_root_as_scan_scope(owner)
    if chooser is not None:
        if not ensure_scan_report_path(owner, chooser=chooser):
            return None
        return legacy_run_mode(owner, SCAN_MODE)

    lifecycle = prepare_scan_report_lifecycle(
        owner,
        reuse_prompt=reuse_prompt,
        previous_action_prompt=previous_action_prompt,
        folder_chooser=folder_chooser,
    )
    if lifecycle != "ready":
        return None
    return legacy_run_mode(owner, SCAN_MODE)


def use_project_root_as_scan_scope(owner: object) -> None:
    """Configure scan to use the selected project root only."""
    scan_controls_runtime.use_project_root_as_scan_scope(owner)


_existing_report_path = scan_report_lifecycle_runtime.existing_report_path
_ask_reuse_previous_report = scan_report_lifecycle_runtime.ask_reuse_previous_report
_ask_previous_report_action = scan_report_lifecycle_runtime.ask_previous_report_action
_delete_report_file = scan_report_lifecycle_runtime.delete_report_file
_choose_report_destination_folder = scan_report_lifecycle_runtime.choose_report_destination_folder
_choose_scan_report_folder = scan_report_lifecycle_runtime.choose_scan_report_folder
_current_report_path_text = scan_report_lifecycle_runtime.current_report_path_text
_default_scan_report_path = scan_report_lifecycle_runtime.default_scan_report_path
_default_scan_report_folder = scan_report_lifecycle_runtime.default_scan_report_folder
_choose_scan_report_path = scan_report_lifecycle_runtime.choose_scan_report_path
_current_project_root = scan_controls_runtime.current_project_root
_path_is_inside = scan_report_lifecycle_runtime.path_is_inside
_normalize_report_path = scan_report_lifecycle_runtime.normalize_report_path
_set_current_report_path = scan_report_lifecycle_runtime.set_current_report_path
_load_current_report = scan_report_lifecycle_runtime.load_current_report
_combo_clear_and_add_scan = scan_controls_runtime.combo_clear_and_add_scan
_combo_clear_and_add_modes = scan_controls_runtime.combo_clear_and_add_modes
_current_mode_text = scan_controls_runtime.current_mode_text
_current_combo_text = scan_controls_runtime.current_combo_text
_safe_line_edit_text = scan_controls_runtime.safe_line_edit_text
_safe_widget_set_enabled = scan_controls_runtime.safe_widget_set_enabled
_safe_widget_set_checked = scan_controls_runtime.safe_widget_set_checked
_safe_widget_hide = scan_controls_runtime.safe_widget_hide
_safe_widget_show = scan_controls_runtime.safe_widget_show
_append_output = scan_controls_runtime.append_output
_show_warning = scan_controls_runtime.show_warning
