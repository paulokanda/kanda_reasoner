# project-path: kanda_reasoner_app/tab3_manual_review_runtime/scan_report_lifecycle_runtime.py
"""Report path and lifecycle helpers for the Tab 3 scan workflow."""

from __future__ import annotations

from datetime import datetime
from os import unlink
from pathlib import Path
from typing import Callable, Literal

from kanda_reasoner_app.tab3_manual_review_runtime.scan_controls_runtime import (
    append_output,
    current_project_root,
    safe_line_edit_text,
    show_warning,
)
from kanda_reasoner_app.tab3_manual_review_runtime.project_paths_runtime import (
    scan_report_folder,
)
from kanda_reasoner_app.tab3_manual_review_runtime.scan_report_name_runtime import (
    REPORT_DATE_FORMAT,
    build_project_missing_docstrings_report_name,
)

__all__ = []

DEFAULT_SCAN_REPORT_NAME = "missing_docstrings_report.jsonl"
ScanReportLifecycle = Literal["ready", "loaded", "cancelled"]


def ensure_scan_report_path(
    owner: object,
    chooser: Callable[[object, Path], str | Path | None] | None = None,
) -> bool:
    """Ensure scan output has a report path before running."""
    if chooser is None:
        return prepare_scan_report_lifecycle(owner) == "ready"

    if _report_path_edit(owner) is None:
        return True
    project_root = current_project_root(owner)
    existing_path = current_report_path_text(owner)
    if existing_path:
        report_path = normalize_report_path(Path(existing_path).expanduser())
        if not path_is_inside(report_path, project_root):
            set_current_report_path(owner, report_path)
            return True
        append_output(
            owner,
            "[report] existing report path is inside the project; choose an outside report path.\n",
        )

    default_path = default_scan_report_path(owner)
    while True:
        selected = chooser(owner, default_path)
        if selected is None or not str(selected).strip():
            append_output(owner, "[report] scan cancelled because no report path was selected.\n")
            return False
        report_path = normalize_report_path(Path(selected).expanduser())
        if not path_is_inside(report_path, project_root):
            break
        append_output(
            owner,
            "[report] report path must be outside the selected project root.\n",
        )
        return False

    set_current_report_path(owner, report_path)
    append_output(owner, "[report] report path selected: " + str(report_path) + "\n")
    return True


def prepare_scan_report_lifecycle(
    owner: object,
    reuse_prompt: Callable[[object, Path], bool] | None = None,
    previous_action_prompt: Callable[[object, Path], str] | None = None,
    folder_chooser: Callable[[object, Path], str | Path | None] | None = None,
    now_provider: Callable[[], datetime] | None = None,
) -> ScanReportLifecycle:
    """Prepare report lifecycle before launching a new scan."""
    if _report_path_edit(owner) is None:
        return "ready"

    project_root = current_project_root(owner)
    if project_root is None:
        append_output(owner, "[report] scan cancelled because project root is empty.\n")
        return "cancelled"

    existing_path = existing_report_path(owner)
    if existing_path is not None:
        should_reuse = ask_reuse_previous_report(owner, existing_path, reuse_prompt)
        if should_reuse:
            set_current_report_path(owner, existing_path)
            load_current_report(owner)
            append_output(owner, "[report] loaded previous report: " + str(existing_path) + "\n")
            return "loaded"

        action = ask_previous_report_action(owner, existing_path, previous_action_prompt)
        if action == "delete":
            if not delete_report_file(owner, existing_path):
                return "cancelled"
        else:
            append_output(owner, "[report] previous report left unchanged: " + str(existing_path) + "\n")

    folder = choose_report_destination_folder(owner, project_root, folder_chooser)
    if folder is None:
        append_output(owner, "[report] scan cancelled because no report folder was selected.\n")
        return "cancelled"

    timestamp = (now_provider or datetime.now)().strftime(REPORT_DATE_FORMAT)
    report_name = build_project_missing_docstrings_report_name(project_root, timestamp)
    report_path = folder / report_name
    set_current_report_path(owner, report_path)
    append_output(owner, "[report] new scan report path: " + str(report_path) + "\n")
    return "ready"


def existing_report_path(owner: object) -> Path | None:
    """Return an existing previous report path from the report field."""
    text = current_report_path_text(owner)
    if not text:
        return None
    path = normalize_report_path(Path(text).expanduser())
    if path.is_file():
        return path
    append_output(owner, "[report] previous report not found: " + str(path) + "\n")
    return None


def ask_reuse_previous_report(
    owner: object,
    report_path: Path,
    reuse_prompt: Callable[[object, Path], bool] | None,
) -> bool:
    """Ask whether to load the previous report instead of scanning."""
    if reuse_prompt is not None:
        return bool(reuse_prompt(owner, report_path))

    from PySide6.QtWidgets import QMessageBox

    message = (
        "Use previous version saved in folder?\n\n"
        + str(report_path)
        + "\n\nYes: load this report without scanning.\nNo: create a new scan report."
    )
    result = QMessageBox.question(
        owner,
        "Use previous report?",
        message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.Yes,
    )
    return result == QMessageBox.Yes


def ask_previous_report_action(
    owner: object,
    report_path: Path,
    previous_action_prompt: Callable[[object, Path], str] | None,
) -> str:
    """Ask whether to delete or leave the previous report before a new scan."""
    if previous_action_prompt is not None:
        action = str(previous_action_prompt(owner, report_path) or "leave").strip().lower()
        if action == "delete":
            return "delete"
        return "leave"

    from PySide6.QtWidgets import QMessageBox

    box = QMessageBox(owner)
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle("Previous report")
    box.setText("Delete previous report or leave it?")
    box.setInformativeText(str(report_path))
    delete_button = box.addButton("Delete", QMessageBox.DestructiveRole)
    leave_button = box.addButton("Leave", QMessageBox.AcceptRole)
    box.setDefaultButton(leave_button)
    box.exec()
    if box.clickedButton() is delete_button:
        return "delete"
    return "leave"


def delete_report_file(owner: object, report_path: Path) -> bool:
    """Delete a previous report file if possible."""
    try:
        unlink(report_path)
    except FileNotFoundError:
        pass
    except OSError as exc:
        append_output(owner, "[report] could not delete previous report: " + str(exc) + "\n")
        show_warning(
            owner,
            "Could not delete report",
            "Could not delete previous report:\n" + str(report_path) + "\n\n" + str(exc),
        )
        return False
    append_output(owner, "[report] deleted previous report: " + str(report_path) + "\n")
    return True


def choose_report_destination_folder(
    owner: object,
    project_root: Path,
    folder_chooser: Callable[[object, Path], str | Path | None] | None,
) -> Path | None:
    """Ask for the folder where the new scan report should be written."""
    start_folder = default_scan_report_folder(owner)
    chooser = folder_chooser if folder_chooser is not None else choose_scan_report_folder
    while True:
        selected = chooser(owner, start_folder)
        if selected is None or not str(selected).strip():
            return None
        folder = Path(selected).expanduser()
        if not path_is_inside(folder, project_root):
            return folder
        append_output(owner, "[report] report folder must be outside the selected project root.\n")
        show_warning(
            owner,
            "Report folder inside project",
            "Choose a report folder outside the selected project root.",
        )
        if folder_chooser is not None:
            return None


def choose_scan_report_folder(owner: object, default_folder: Path) -> str | None:
    """Ask the user which folder should receive the scan report."""
    from PySide6.QtWidgets import QFileDialog

    selected = QFileDialog.getExistingDirectory(
        owner,
        "Select Missing Docstrings Report Folder",
        str(default_folder),
    )
    return str(selected or "").strip() or None


def current_report_path_text(owner: object) -> str:
    """Return the visible report path text, if present."""
    return safe_line_edit_text(_report_path_edit(owner))


def default_scan_report_path(owner: object) -> Path:
    """Return the legacy default path shown in compatibility save dialogs."""
    return default_scan_report_folder(owner) / DEFAULT_SCAN_REPORT_NAME


def default_scan_report_folder(owner: object) -> Path:
    """Return the canonical external Docstring Assistant report folder."""
    try:
        return scan_report_folder(owner)
    except (OSError, ValueError):
        return Path.home()


def choose_scan_report_path(owner: object, default_path: Path) -> str | None:
    """Ask the user where to save the scan report through the legacy path dialog."""
    from PySide6.QtWidgets import QFileDialog

    selected, _selected_filter = QFileDialog.getSaveFileName(
        owner,
        "Save Missing Docstrings Report",
        str(default_path),
        "JSON Lines (*.jsonl);;JSON (*.json);;All files (*)",
    )
    return str(selected or "").strip() or None


def path_is_inside(path: Path, root: Path | None) -> bool:
    """Return whether path is inside root."""
    if root is None:
        return False
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def normalize_report_path(path: Path) -> Path:
    """Return a report path with a JSONL suffix when no suffix is provided."""
    if path.suffix:
        return path
    return path.with_suffix(".jsonl")


def set_current_report_path(owner: object, report_path: Path) -> None:
    """Set the visible report path through the report IO public contract."""
    from kanda_reasoner_app.tab3_manual_review_runtime import report_io_runtime

    report_io_runtime.set_current_report_path(owner, report_path)


def load_current_report(owner: object) -> None:
    """Load rows from the current report path when supported by the owner."""
    load_rows = _optional_load_report_rows(owner)
    if callable(load_rows):
        load_rows()


def _report_path_edit(owner: object) -> object:
    try:
        return owner._report_path_edit
    except AttributeError:
        return None


def _optional_load_report_rows(owner: object) -> object:
    try:
        return owner._load_report_rows
    except AttributeError:
        return None
