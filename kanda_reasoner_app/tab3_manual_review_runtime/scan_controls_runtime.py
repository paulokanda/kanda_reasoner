# project-path: kanda_reasoner_app/tab3_manual_review_runtime/scan_controls_runtime.py
"""Widget and scan-scope helpers for the Tab 3 scan workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.tab3_manual_review_runtime.scan_target_options_runtime import (
    configure_scan_target_checkboxes,
)

__all__ = []

SCAN_MODE = "scan"
SCAN_DIFF_WRITE_MODES = ("scan", "diff", "write")


def configure_scan_diff_write_controls(window: object) -> None:
    """Expose the full scan/diff/write workflow controls."""
    combo = _mode_combo(window)
    combo_clear_and_add_modes(combo, SCAN_DIFF_WRITE_MODES)
    safe_widget_set_enabled(combo, True)
    safe_widget_show(combo)

    confirm_write = _confirm_write_checkbox(window)
    safe_widget_set_enabled(confirm_write, True)
    safe_widget_show(confirm_write)

    configure_scan_target_checkboxes(window)
    refresh_selected_mode_controls(window)


def refresh_selected_mode_controls(
    window: object,
    mode: str | None = None,
) -> None:
    """Refresh button text and write guard visibility for the selected mode."""
    normalized_mode = str(mode or current_mode_text(window) or SCAN_MODE).strip().lower()

    run_button = _run_button(window)
    setter = _optional_set_text(run_button)
    if callable(setter):
        setter(
            {
                "scan": "Scan Files for Missing Docstrings",
                "diff": "Preview Docstring Diff",
                "write": "Write Missing Docstrings",
            }.get(normalized_mode, "Run selected mode")
        )

    confirm_write = _confirm_write_checkbox(window)
    if normalized_mode == "write":
        safe_widget_show(confirm_write)
        safe_widget_set_enabled(confirm_write, True)
    else:
        safe_widget_set_enabled(confirm_write, False)


def configure_scan_only_controls(window: object) -> None:
    """Force legacy mode widgets to the scan-only workflow state."""
    combo = _mode_combo(window)
    combo_clear_and_add_scan(combo)
    safe_widget_set_enabled(combo, False)
    safe_widget_hide(combo)

    confirm_write = _confirm_write_checkbox(window)
    safe_widget_set_checked(confirm_write, False)
    safe_widget_hide(confirm_write)

    configure_scan_target_checkboxes(window)

    run_button = _run_button(window)
    setter = _optional_set_text(run_button)
    if callable(setter):
        setter("Scan Files for Missing Docstrings")


def use_project_root_as_scan_scope(owner: object) -> None:
    """Configure scan to use the selected project root only."""
    scope_combo = _scope_combo(owner)
    target_edit = _target_path_edit(owner)
    set_current = _optional_set_current_text(scope_combo)
    if callable(set_current):
        set_current("Full project")
    clear = _optional_clear(target_edit)
    if callable(clear):
        clear()


def combo_clear_and_add_scan(combo: object) -> None:
    """Replace a combo box's contents with the single scan mode."""
    combo_clear_and_add_modes(combo, (SCAN_MODE,))


def combo_clear_and_add_modes(combo: object, modes: tuple[str, ...]) -> None:
    """Replace a combo box's contents with the provided modes."""
    if combo is None:
        return
    current = current_combo_text(combo)
    clear = _optional_clear(combo)
    if callable(clear):
        clear()
    add_item = _optional_add_item(combo)
    if callable(add_item):
        for mode in modes:
            add_item(mode)
    set_current = _optional_set_current_text(combo)
    if callable(set_current):
        set_current(current if current in modes else modes[0])


def current_mode_text(owner: object) -> str:
    """Return the currently selected mode text when available."""
    return current_combo_text(_mode_combo(owner))


def current_combo_text(combo: object) -> str:
    """Return current combo text for Qt widgets and lightweight test doubles."""
    if combo is None:
        return ""
    current_text = _optional_current_text(combo)
    if callable(current_text):
        try:
            return str(current_text() or "").strip()
        except Exception:
            return ""
    value = _optional_current_text_value(combo)
    if str(value or "").strip():
        return str(value or "").strip()
    value = _optional_current_value(combo)
    if str(value or "").strip():
        return str(value or "").strip()
    return ""


def safe_line_edit_text(widget: object) -> str:
    """Return text from a line-edit-like widget, or an empty string."""
    text_method = _optional_text(widget)
    if not callable(text_method):
        return ""
    try:
        return str(text_method() or "").strip()
    except Exception:
        return ""


def safe_widget_set_enabled(widget: object, enabled: bool) -> None:
    """Set widget enabled state when supported."""
    setter = _optional_set_enabled(widget)
    if callable(setter):
        setter(bool(enabled))


def safe_widget_set_checked(widget: object, checked: bool) -> None:
    """Set widget checked state when supported."""
    setter = _optional_set_checked(widget)
    if callable(setter):
        setter(bool(checked))


def safe_widget_hide(widget: object) -> None:
    """Hide a widget when supported."""
    hide = _optional_hide(widget)
    if callable(hide):
        hide()


def safe_widget_show(widget: object) -> None:
    """Show a widget when supported."""
    show = _optional_show(widget)
    if callable(show):
        show()


def append_output(owner: object, text: str) -> None:
    """Append a message to the Tab 3 output if possible."""
    append_text = _optional_append_text(owner)
    if callable(append_text):
        append_text(text)


def show_warning(owner: object, title: str, message: str) -> None:
    """Show a warning dialog when Qt is available."""
    try:
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.warning(owner, title, message)
    except Exception:
        append_output(owner, "[warning] " + title + ": " + message + "\n")


def current_project_root(owner: object) -> Path | None:
    """Return the selected project root when it can be resolved."""
    root_text = safe_line_edit_text(_root_path_edit(owner))
    if not root_text:
        return None
    try:
        return Path(root_text).expanduser().resolve()
    except OSError:
        return Path(root_text).expanduser()


def _mode_combo(owner: object) -> object:
    try:
        return owner._mode_combo
    except AttributeError:
        return None


def _confirm_write_checkbox(owner: object) -> object:
    try:
        return owner._confirm_write_checkbox
    except AttributeError:
        return None


def _run_button(owner: object) -> object:
    try:
        return owner._run_button
    except AttributeError:
        return None


def _scope_combo(owner: object) -> object:
    try:
        return owner._scope_combo
    except AttributeError:
        return None


def _target_path_edit(owner: object) -> object:
    try:
        return owner._target_path_edit
    except AttributeError:
        return None


def _root_path_edit(owner: object) -> object:
    try:
        return owner._root_path_edit
    except AttributeError:
        return None


def _optional_set_text(widget: object) -> Any:
    try:
        return widget.setText
    except AttributeError:
        return None


def _optional_set_current_text(widget: object) -> Any:
    try:
        return widget.setCurrentText
    except AttributeError:
        return None


def _optional_clear(widget: object) -> Any:
    try:
        return widget.clear
    except AttributeError:
        return None


def _optional_add_item(widget: object) -> Any:
    try:
        return widget.addItem
    except AttributeError:
        return None


def _optional_current_text(widget: object) -> Any:
    try:
        return widget.currentText
    except AttributeError:
        return None


def _optional_current_text_value(widget: object) -> Any:
    try:
        return widget.current_text
    except AttributeError:
        return ""


def _optional_current_value(widget: object) -> Any:
    try:
        return widget.current
    except AttributeError:
        return ""


def _optional_text(widget: object) -> Any:
    try:
        return widget.text
    except AttributeError:
        return None


def _optional_set_enabled(widget: object) -> Any:
    try:
        return widget.setEnabled
    except AttributeError:
        return None


def _optional_set_checked(widget: object) -> Any:
    try:
        return widget.setChecked
    except AttributeError:
        return None


def _optional_hide(widget: object) -> Any:
    try:
        return widget.hide
    except AttributeError:
        return None


def _optional_show(widget: object) -> Any:
    try:
        return widget.show
    except AttributeError:
        return None


def _optional_append_text(owner: object) -> Any:
    try:
        return owner._append_text
    except AttributeError:
        return None
