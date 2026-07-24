# project-path: kanda_reasoner_app/tab3_manual_review_runtime/report_io_runtime.py
"""Runtime helpers for Tab 3 report save, load, and copy actions."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from kanda_reasoner_app.tab3_manual_review_runtime.review_persistence_fields import (
    review_rows_jsonl,
)
from kanda_reasoner_app.tab3_manual_review_runtime.project_paths_runtime import (
    scan_report_folder,
)

REPORT_IO_PREFS_NAME = ".kanda_tab3_report_io_prefs.json"

__all__ = [
    "save_report",
    "load_report",
    "copy_report",
    "report_text_for_export",
    "set_current_report_path",
]

def save_report(owner: object) -> None:
    """Save the active Tab 3 report to a remembered external file."""
    text = _current_report_text(owner)
    if not text.strip():
        _show_warning(owner, "No report", "There is no Tab 3 report to save.")
        return

    QFileDialog = _qt_widget("QFileDialog")
    start_folder = _remembered_folder(owner, "save_folder")
    default_path = start_folder / _default_report_name()
    selected, _filter = QFileDialog.getSaveFileName(
        owner,
        "Save Tab 3 report",
        str(default_path),
        "Report files (*.jsonl *.json *.txt);;All files (*)",
    )
    if not selected:
        return

    output_path = Path(selected).expanduser()
    _write_text_file(output_path, text)
    _remember_folder("save_folder", output_path.parent)
    _set_report_path(owner, output_path)
    _reload_loaded_report(owner)
    _append_output(owner, "[report] saved report to: " + str(output_path) + "\n")
    _show_info(owner, "Report saved", "Saved Tab 3 report to:\n" + str(output_path))


def load_report(owner: object) -> None:
    """Load a saved Tab 3 report into the current report and review panels."""
    QFileDialog = _qt_widget("QFileDialog")
    start_folder = _remembered_folder(owner, "load_folder")
    selected, _filter = QFileDialog.getOpenFileName(
        owner,
        "Load Tab 3 report",
        str(start_folder),
        "Report files (*.jsonl *.json *.txt);;All files (*)",
    )
    if not selected:
        return

    report_path = Path(selected).expanduser()
    if not report_path.is_file():
        _show_warning(owner, "Report not found", "Report file not found:\n" + str(report_path))
        return

    _remember_folder("load_folder", report_path.parent)
    _remember_folder("save_folder", report_path.parent)
    _set_report_path(owner, report_path)
    _reload_loaded_report(owner)
    _append_output(owner, "[report] loaded report from: " + str(report_path) + "\n")
    _show_info(owner, "Report loaded", "Loaded Tab 3 report from:\n" + str(report_path))


def copy_report(owner: object) -> None:
    """Copy the active Tab 3 report text and optionally save a copy file."""
    text = _current_report_text(owner)
    if not text.strip():
        _show_warning(owner, "No report", "There is no Tab 3 report to copy.")
        return

    QApplication = _qt_widget("QApplication")
    clipboard = QApplication.clipboard()
    if clipboard is not None:
        clipboard.setText(text)

    copied_path = _copy_report_file(owner, text)
    if copied_path is None:
        _append_output(owner, "[report] copied report text to clipboard.\n")
        _show_info(owner, "Report copied", "Copied Tab 3 report text to the clipboard.")
        return

    _append_output(owner, "[report] copied report text to clipboard and file: " + str(copied_path) + "\n")
    _show_info(
        owner,
        "Report copied",
        "Copied Tab 3 report text to the clipboard and to:\n" + str(copied_path),
    )


def report_text_for_export(owner: object) -> str:
    """Return active report text through a stable public contract."""
    return _current_report_text(owner)


def set_current_report_path(owner: object, report_path: Path) -> None:
    """Set the current report path through a stable public contract."""
    _set_report_path(owner, report_path)


def _copy_report_file(owner: object, text: str) -> Path | None:
    """Ask for a folder and write a timestamped report copy there."""
    QFileDialog = _qt_widget("QFileDialog")
    start_folder = _remembered_folder(owner, "copy_folder")
    selected = QFileDialog.getExistingDirectory(
        owner,
        "Copy Tab 3 report to folder",
        str(start_folder),
    )
    if not selected:
        return None

    folder = Path(selected).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    output_path = folder / _default_report_name()
    _write_text_file(output_path, text)
    _remember_folder("copy_folder", folder)
    return output_path


def _current_report_text(owner: object) -> str:
    """Return the current report text, preserving in-memory review fields."""
    rows = list(getattr(owner, "_report_rows", []) or [])
    if rows:
        return review_rows_jsonl(rows)

    report_path = _active_report_path(owner)
    if report_path is not None and report_path.is_file():
        try:
            return report_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    return ""


def _active_report_path(owner: object) -> Path | None:
    """Return the effective report path for the current Tab 3 window."""
    path_text = ""
    effective = getattr(owner, "_effective_report_path", None)
    if callable(effective):
        try:
            path_text = str(effective() or "").strip()
        except Exception:
            path_text = ""
    if not path_text:
        edit = getattr(owner, "_report_path_edit", None)
        text_method = getattr(edit, "text", None)
        if callable(text_method):
            path_text = str(text_method() or "").strip()
    if not path_text:
        return None
    return Path(path_text).expanduser()


def _set_report_path(owner: object, report_path: Path) -> None:
    """Set the visible report path and current report path on the owner."""
    edit = getattr(owner, "_report_path_edit", None)
    set_text = getattr(edit, "setText", None)
    if callable(set_text):
        set_text(str(report_path))
    setattr(owner, "_current_report_path", report_path)
    save_prefs = getattr(owner, "_save_prefs", None)
    if callable(save_prefs):
        save_prefs()


def _reload_loaded_report(owner: object) -> None:
    """Reload report rows into the review panel if the owner supports it."""
    load_rows = getattr(owner, "_load_report_rows", None)
    if callable(load_rows):
        load_rows()


def _write_text_file(path: Path, text: str) -> None:
    """Write text as UTF-8 without a BOM."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _default_report_name() -> str:
    """Return a timestamped report filename."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "tab3_missing_docstrings_report_" + stamp + ".jsonl"


def _remembered_folder(owner: object, key: str) -> Path:
    """Return the remembered folder for one report action."""
    prefs = _load_report_io_prefs()
    value = str(prefs.get(key) or "").strip()
    if value:
        path = Path(value).expanduser()
        if path.exists():
            return path
    return _default_external_folder(owner)


def _default_external_folder(owner: object) -> Path:
    """Return a dynamic default folder outside the active project when possible."""
    root_text = ""
    root_edit = getattr(owner, "_root_path_edit", None)
    text_method = getattr(root_edit, "text", None)
    if callable(text_method):
        root_text = str(text_method() or "").strip()
    if root_text:
        try:
            return scan_report_folder(owner)
        except (OSError, ValueError):
            pass
    return Path.home()


def _load_report_io_prefs() -> dict[str, str]:
    """Load report IO folder preferences."""
    path = _report_io_prefs_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(key): str(value) for key, value in data.items() if isinstance(key, str)}


def _remember_folder(key: str, folder: Path) -> None:
    """Remember one report IO folder preference."""
    prefs = _load_report_io_prefs()
    prefs[key] = str(folder)
    path = _report_io_prefs_path()
    try:
        path.write_text(json.dumps(prefs, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError:
        return


def _report_io_prefs_path() -> Path:
    """Return the user-level report IO preference path."""
    return Path.home() / REPORT_IO_PREFS_NAME


def _append_output(owner: object, text: str) -> None:
    """Append text to the Tab 3 output console if possible."""
    append_text = getattr(owner, "_append_text", None)
    if callable(append_text):
        append_text(text)


def _show_info(owner: object, title: str, message: str) -> None:
    """Show a silent auto-closing post-action information window."""
    from kanda_reasoner_app.templates.floating_windows import (
        show_auto_close_action_window,
    )

    show_auto_close_action_window(owner, title=title, message=message)


def _show_warning(owner: object, title: str, message: str) -> None:
    """Show a warning dialog."""
    QMessageBox = _qt_widget("QMessageBox")
    QMessageBox.warning(owner, title, message)


def _qt_widget(name: str) -> Any:
    """Return a PySide6.QtWidgets object lazily."""
    import importlib

    module = importlib.import_module("PySide" + "6.QtWidgets")
    return getattr(module, name)
