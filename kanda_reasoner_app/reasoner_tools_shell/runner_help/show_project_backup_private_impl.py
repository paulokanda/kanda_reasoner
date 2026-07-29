"""Qt controller for the Show Project Support backup button."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.show_project_backup_service import (
    create_show_project_backup,
    validate_backup_destination,
)

__all__ = [
    "ShowProjectBackupWorker",
    "choose_and_start_show_project_backup",
    "install_show_project_backup_button",
    "start_show_project_backup",
]

_BUSY_CONTROL_NAMES = (
    "backup_show_project_button",
    "browse_project_button",
    "close_button",
    "create_first_and_second_prompt_files_button",
    "create_first_prompt_files_button",
    "run_button",
)


class ShowProjectBackupWorker(QObject):
    """Create one Show Project backup outside the Qt GUI thread."""

    progress = Signal(str)
    completed = Signal(object)
    failed = Signal(str)
    finished = Signal()

    def __init__(self, project_root: Path, destination_dir: Path) -> None:
        super().__init__()
        self._project_root = Path(project_root)
        self._destination_dir = Path(destination_dir)

    @Slot()
    def run(self) -> None:
        """Create, verify, and publish one atomic backup ZIP."""
        try:
            result = create_show_project_backup(
                self._project_root,
                self._destination_dir,
                progress=self.progress.emit,
            )
            self.completed.emit(result)
        except Exception as exc:  # GUI boundary: never strand thread cleanup
            self.failed.emit(str(exc))
        finally:
            self.finished.emit()


def install_show_project_backup_button(window: object) -> None:
    """Connect the Show Project backup button to its governed action."""
    button = getattr(window, "backup_show_project_button", None)
    if button is None:
        raise AttributeError("backup_show_project_button is missing from the window.")
    button.clicked.connect(lambda: choose_and_start_show_project_backup(window))


def choose_and_start_show_project_backup(window: object) -> None:
    """Ask for a destination folder and start one background backup."""
    try:
        project_root = _selected_project_root(window)
        support_root = project_analysis_evidence_root(project_root)
        if not support_root.is_dir():
            raise FileNotFoundError(
                "Show Project folder does not exist yet: " + str(support_root)
            )
        destination = QFileDialog.getExistingDirectory(
            window,
            "Select folder for Show Project backup",
            str(project_root.parent),
        )
        if not destination:
            _set_status(window, "Show Project backup cancelled.")
            return
        start_show_project_backup(window, Path(destination))
    except Exception as exc:
        _report_failure(window, "Could not start Show Project backup: " + str(exc))


def start_show_project_backup(window: object, destination_dir: str | Path) -> None:
    """Start one background backup for the selected Project Support root."""
    active_thread = getattr(window, "_show_project_backup_thread", None)
    if active_thread is not None and active_thread.isRunning():
        _set_status(window, "Show Project backup is already running.")
        return

    project_root = _selected_project_root(window)
    destination = validate_backup_destination(project_root, destination_dir)
    thread = QThread(window)
    worker = ShowProjectBackupWorker(project_root, destination)
    worker.moveToThread(thread)
    window._show_project_backup_thread = thread
    window._show_project_backup_worker = worker

    thread.started.connect(worker.run)
    worker.progress.connect(lambda message: _report_progress(window, message))
    worker.completed.connect(lambda payload: _report_success(window, payload))
    worker.failed.connect(lambda message: _report_failure(window, message))
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(lambda: _finish_backup_thread(window))
    thread.finished.connect(thread.deleteLater)

    _set_backup_busy(window, True)
    _report_progress(window, "Preparing Show Project backup...")
    thread.start()


def _selected_project_root(window: object) -> Path:
    raw_root = str(getattr(window, "project_root_edit").text()).strip()
    if not raw_root:
        raise ValueError("Project root field is empty.")
    project_root = Path(raw_root).expanduser().resolve(strict=False)
    if not project_root.is_dir():
        raise FileNotFoundError(
            "Selected project root is not a directory: " + str(project_root)
        )
    return project_root


def _set_backup_busy(window: object, busy: bool) -> None:
    for name in _BUSY_CONTROL_NAMES:
        control = getattr(window, name, None)
        setter = getattr(control, "setEnabled", None)
        if callable(setter):
            setter(not busy)
    button = getattr(window, "backup_show_project_button", None)
    if button is not None:
        button.setText("Backing Up..." if busy else "Backup Show Project")


def _report_progress(window: object, message: str) -> None:
    _set_status(window, message)
    _append_log(window, message)


def _report_success(window: object, payload: object) -> None:
    data = dict(payload) if isinstance(payload, dict) else {}
    archive_path = str(data.get("archive_path") or "")
    message = "Show Project backup created: " + archive_path
    _set_status(window, message)
    _append_log(window, message)
    QMessageBox.information(
        window,
        "Show Project backup complete",
        message
        + "\n\nFiles: "
        + str(data.get("file_count") or 0)
        + "\nArchive bytes: "
        + str(data.get("archive_bytes") or 0),
    )


def _report_failure(window: object, message: str) -> None:
    error_message = "[ERROR] " + str(message)
    _set_status(window, error_message)
    _append_log(window, error_message)
    QMessageBox.warning(window, "Show Project backup failed", str(message))


def _finish_backup_thread(window: object) -> None:
    _set_backup_busy(window, False)
    window._show_project_backup_thread = None
    window._show_project_backup_worker = None


def _set_status(window: object, message: str) -> None:
    for name in ("first_prompt_status_label", "status_label"):
        status = getattr(window, name, None)
        if status is not None:
            try:
                status.setText(message)
            except Exception:
                pass


def _append_log(window: object, message: str) -> None:
    try:
        getattr(window, "_append_log")(message)
    except Exception:
        pass
