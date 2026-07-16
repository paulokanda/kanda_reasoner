"""Scan-only workflow helpers for the Tab 3 missing-docstring handler."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Literal

from kanda_reasoner_app.tab3_manual_review_runtime.scan_report_name_runtime import (
    REPORT_DATE_FORMAT,
    build_project_missing_docstrings_report_name,
)
from kanda_reasoner_app.tab3_manual_review_runtime.scan_target_options_runtime import (
    configure_scan_target_checkboxes,
)

__all__ = [
    "SCAN_MODE",
    "DEFAULT_SCAN_REPORT_NAME",
    "configure_scan_only_controls",
    "ensure_scan_report_path",
    "prepare_scan_report_lifecycle",
    "run_scan_only_mode",
    "run_scan_selected_mode",
    "use_project_root_as_scan_scope",
]

SCAN_MODE = "scan"
DEFAULT_SCAN_REPORT_NAME = "missing_docstrings_report.jsonl"
ScanReportLifecycle = Literal["ready", "loaded", "cancelled"]


def configure_scan_only_controls(window: object) -> None:
    """Force legacy mode widgets to the scan-only workflow state."""
    combo = getattr(window, "_mode_combo", None)
    _combo_clear_and_add_scan(combo)
    _safe_widget_set_enabled(combo, False)
    _safe_widget_hide(combo)

    confirm_write = getattr(window, "_confirm_write_checkbox", None)
    _safe_widget_set_checked(confirm_write, False)
    _safe_widget_hide(confirm_write)

    configure_scan_target_checkboxes(window)

    run_button = getattr(window, "_run_button", None)
    setter = getattr(run_button, "setText", None)
    if callable(setter):
        setter("Scan Files for Missing Docstrings")


def ensure_scan_report_path(
    owner: object,
    chooser: Callable[[object, Path], str | Path | None] | None = None,
) -> bool:
    """Ensure scan output has a report path before running.

    This function keeps the PA033/PA035 file-chooser contract for tests and
    compatibility when a chooser is supplied. Normal GUI scans use
    prepare_scan_report_lifecycle instead, which implements the report lifecycle
    prompts requested in PA036.
    """
    if chooser is None:
        return prepare_scan_report_lifecycle(owner) == "ready"

    if not hasattr(owner, "_report_path_edit"):
        return True
    project_root = _current_project_root(owner)
    existing_path = _current_report_path_text(owner)
    if existing_path:
        report_path = _normalize_report_path(Path(existing_path).expanduser())
        if not _path_is_inside(report_path, project_root):
            _set_current_report_path(owner, report_path)
            return True
        _append_output(
            owner,
            "[report] existing report path is inside the project; choose an outside report path.\n",
        )

    default_path = _default_scan_report_path(owner)
    while True:
        selected = chooser(owner, default_path)
        if selected is None or not str(selected).strip():
            _append_output(owner, "[report] scan cancelled because no report path was selected.\n")
            return False
        report_path = _normalize_report_path(Path(selected).expanduser())
        if not _path_is_inside(report_path, project_root):
            break
        _append_output(
            owner,
            "[report] report path must be outside the selected project root.\n",
        )
        return False

    _set_current_report_path(owner, report_path)
    _append_output(owner, "[report] report path selected: " + str(report_path) + "\n")
    return True


def prepare_scan_report_lifecycle(
    owner: object,
    reuse_prompt: Callable[[object, Path], bool] | None = None,
    previous_action_prompt: Callable[[object, Path], str] | None = None,
    folder_chooser: Callable[[object, Path], str | Path | None] | None = None,
    now_provider: Callable[[], datetime] | None = None,
) -> ScanReportLifecycle:
    """Prepare report lifecycle before launching a new scan.

    Existing report path behavior:
    - Ask whether to use the previous report.
    - If yes, load the previous report and do not scan.
    - If no, ask whether to delete or leave the previous report.

    New scan behavior:
    - Ask for a destination folder outside the selected project.
    - Generate a timestamped project-specific report filename.
    - Set the report path before starting the worker, because the worker needs
      a destination path when it writes the JSONL report.
    """
    if not hasattr(owner, "_report_path_edit"):
        return "ready"

    project_root = _current_project_root(owner)
    if project_root is None:
        _append_output(owner, "[report] scan cancelled because project root is empty.\n")
        return "cancelled"

    existing_path = _existing_report_path(owner)
    if existing_path is not None:
        should_reuse = _ask_reuse_previous_report(owner, existing_path, reuse_prompt)
        if should_reuse:
            _set_current_report_path(owner, existing_path)
            _load_current_report(owner)
            _append_output(owner, "[report] loaded previous report: " + str(existing_path) + "\n")
            return "loaded"

        action = _ask_previous_report_action(owner, existing_path, previous_action_prompt)
        if action == "delete":
            if not _delete_report_file(owner, existing_path):
                return "cancelled"
        else:
            _append_output(owner, "[report] previous report left unchanged: " + str(existing_path) + "\n")

    folder = _choose_report_destination_folder(owner, project_root, folder_chooser)
    if folder is None:
        _append_output(owner, "[report] scan cancelled because no report folder was selected.\n")
        return "cancelled"

    timestamp = (now_provider or datetime.now)().strftime(REPORT_DATE_FORMAT)
    report_name = build_project_missing_docstrings_report_name(project_root, timestamp)
    report_path = folder / report_name
    _set_current_report_path(owner, report_path)
    _append_output(owner, "[report] new scan report path: " + str(report_path) + "\n")
    return "ready"


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
    scope_combo = getattr(owner, "_scope_combo", None)
    target_edit = getattr(owner, "_target_path_edit", None)
    set_current = getattr(scope_combo, "setCurrentText", None)
    if callable(set_current):
        set_current("Full project")
    clear = getattr(target_edit, "clear", None)
    if callable(clear):
        clear()


def _existing_report_path(owner: object) -> Path | None:
    """Return an existing previous report path from the report field."""
    text = _current_report_path_text(owner)
    if not text:
        return None
    path = _normalize_report_path(Path(text).expanduser())
    if path.is_file():
        return path
    _append_output(owner, "[report] previous report not found: " + str(path) + "\n")
    return None


def _ask_reuse_previous_report(
    owner: object,
    report_path: Path,
    reuse_prompt: Callable[[object, Path], bool] | None,
) -> bool:
    """Ask whether to load the previous report instead of scanning."""
    if reuse_prompt is not None:
        return bool(reuse_prompt(owner, report_path))

    QMessageBox = _qt_widget("QMessageBox")
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


def _ask_previous_report_action(
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

    QMessageBox = _qt_widget("QMessageBox")
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


def _delete_report_file(owner: object, report_path: Path) -> bool:
    """Delete a previous report file if possible."""
    try:
        report_path.unlink()
    except FileNotFoundError:
        pass
    except OSError as exc:
        _append_output(owner, "[report] could not delete previous report: " + str(exc) + "\n")
        _show_warning(
            owner,
            "Could not delete report",
            "Could not delete previous report:\n" + str(report_path) + "\n\n" + str(exc),
        )
        return False
    _append_output(owner, "[report] deleted previous report: " + str(report_path) + "\n")
    return True


def _choose_report_destination_folder(
    owner: object,
    project_root: Path,
    folder_chooser: Callable[[object, Path], str | Path | None] | None,
) -> Path | None:
    """Ask for the folder where the new scan report should be written."""
    start_folder = _default_scan_report_folder(owner)
    chooser = folder_chooser if folder_chooser is not None else _choose_scan_report_folder
    while True:
        selected = chooser(owner, start_folder)
        if selected is None or not str(selected).strip():
            return None
        folder = Path(selected).expanduser()
        if not _path_is_inside(folder, project_root):
            return folder
        _append_output(owner, "[report] report folder must be outside the selected project root.\n")
        _show_warning(
            owner,
            "Report folder inside project",
            "Choose a report folder outside the selected project root.",
        )
        if folder_chooser is not None:
            return None


def _choose_scan_report_folder(owner: object, default_folder: Path) -> str | None:
    """Ask the user which folder should receive the scan report."""
    QFileDialog = _qt_widget("QFileDialog")
    selected = QFileDialog.getExistingDirectory(
        owner,
        "Select Missing Docstrings Report Folder",
        str(default_folder),
    )
    return str(selected or "").strip() or None


def _current_report_path_text(owner: object) -> str:
    """Return the visible report path text, if present."""
    edit = getattr(owner, "_report_path_edit", None)
    text_method = getattr(edit, "text", None)
    if not callable(text_method):
        return ""
    try:
        return str(text_method() or "").strip()
    except Exception:
        return ""


def _default_scan_report_path(owner: object) -> Path:
    """Return the legacy default path shown in compatibility save dialogs."""
    return _default_scan_report_folder(owner) / DEFAULT_SCAN_REPORT_NAME


def _default_scan_report_folder(owner: object) -> Path:
    """Return an outside-project folder for the scan report folder dialog."""
    project_root = _current_project_root(owner)
    if project_root is not None:
        parent = project_root.parent
        if parent.exists():
            return parent
    return Path.home()


def _choose_scan_report_path(owner: object, default_path: Path) -> str | None:
    """Ask the user where to save the scan report through the legacy path dialog."""
    QFileDialog = _qt_widget("QFileDialog")
    selected, _selected_filter = QFileDialog.getSaveFileName(
        owner,
        "Save Missing Docstrings Report",
        str(default_path),
        "JSON Lines (*.jsonl);;JSON (*.json);;All files (*)",
    )
    return str(selected or "").strip() or None


def _current_project_root(owner: object) -> Path | None:
    """Return the selected project root when it can be resolved."""
    root_text = _safe_line_edit_text(getattr(owner, "_root_path_edit", None))
    if not root_text:
        return None
    try:
        return Path(root_text).expanduser().resolve()
    except OSError:
        return Path(root_text).expanduser()


def _path_is_inside(path: Path, root: Path | None) -> bool:
    """Return whether path is inside root."""
    if root is None:
        return False
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def _normalize_report_path(path: Path) -> Path:
    """Return a report path with a JSONL suffix when no suffix is provided."""
    if path.suffix:
        return path
    return path.with_suffix(".jsonl")


def _set_current_report_path(owner: object, report_path: Path) -> None:
    """Set the visible report path through the report IO public contract."""
    module = __import__(
        "kanda_reasoner_app.tab3_manual_review_runtime.report_io_runtime",
        fromlist=["set_current_report_path"],
    )
    module.set_current_report_path(owner, report_path)


def _load_current_report(owner: object) -> None:
    """Load rows from the current report path when supported by the owner."""
    load_rows = getattr(owner, "_load_report_rows", None)
    if callable(load_rows):
        load_rows()


def _combo_clear_and_add_scan(combo: object) -> None:
    """Replace a combo box's contents with the single scan mode."""
    if combo is None:
        return
    clear = getattr(combo, "clear", None)
    if callable(clear):
        clear()
    add_item = getattr(combo, "addItem", None)
    if callable(add_item):
        add_item(SCAN_MODE)
    set_current = getattr(combo, "setCurrentText", None)
    if callable(set_current):
        set_current(SCAN_MODE)


def _safe_line_edit_text(widget: object) -> str:
    """Return text from a line-edit-like widget, or an empty string."""
    text_method = getattr(widget, "text", None)
    if not callable(text_method):
        return ""
    try:
        return str(text_method() or "").strip()
    except Exception:
        return ""


def _safe_widget_set_enabled(widget: object, enabled: bool) -> None:
    """Set widget enabled state when supported."""
    setter = getattr(widget, "setEnabled", None)
    if callable(setter):
        setter(bool(enabled))


def _safe_widget_set_checked(widget: object, checked: bool) -> None:
    """Set widget checked state when supported."""
    setter = getattr(widget, "setChecked", None)
    if callable(setter):
        setter(bool(checked))


def _safe_widget_hide(widget: object) -> None:
    """Hide a widget when supported."""
    hide = getattr(widget, "hide", None)
    if callable(hide):
        hide()


def _append_output(owner: object, text: str) -> None:
    """Append a message to the Tab 3 output if possible."""
    append_text = getattr(owner, "_append_text", None)
    if callable(append_text):
        append_text(text)


def _show_warning(owner: object, title: str, message: str) -> None:
    """Show a warning dialog when Qt is available."""
    try:
        QMessageBox = _qt_widget("QMessageBox")
        QMessageBox.warning(owner, title, message)
    except Exception:
        _append_output(owner, "[warning] " + title + ": " + message + "\n")


def _qt_widget(name: str) -> Any:
    """Return a PySide6.QtWidgets object lazily."""
    module = __import__("PySide" + "6.QtWidgets", fromlist=[name])
    return getattr(module, name)
