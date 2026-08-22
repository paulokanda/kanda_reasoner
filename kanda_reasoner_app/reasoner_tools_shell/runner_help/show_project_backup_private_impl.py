"""Qt controller for Show Project and complete Project backup buttons."""

from __future__ import annotations

from pathlib import Path
from threading import Event

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.show_project_backup_service import (
    BackupCancelled,
    _create_project_backup,
    create_show_project_backup,
    validate_backup_destination,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.show_project_backup_both_service import create_backup_both
from kanda_reasoner_app.reasoner_tools_shell.runner_help.pre_backup_cleanup_dialog import run_pre_backup_cleanup_dialog
from kanda_reasoner_app.templates.green_sonar_monitor import GreenSonarActivityMonitor
__all__ = [
    "ShowProjectBackupWorker",
    "choose_and_start_show_project_backup",
    "install_show_project_backup_button",
    "start_show_project_backup",
]

_BACKUP_LABELS = {"project": "Project", "both": "Both"}
_BUSY_CONTROL_NAMES = (
    "backup_show_project_button",
    "backup_project_button",
    "backup_both_button",
    "browse_project_button",
    "close_button",
    "create_first_and_second_prompt_files_button",
    "create_first_prompt_files_button",
    "run_button",
)


class ShowProjectBackupWorker(QObject):
    """Create one governed backup outside the Qt GUI thread."""

    progress = Signal(str)
    completed = Signal(object)
    cancelled = Signal(str)
    failed = Signal(str)
    finished = Signal()

    def __init__(
        self,
        project_root: Path,
        destination_dir: Path,
        backup_kind: str = "show_project",
    ) -> None:
        super().__init__()
        self._project_root = Path(project_root)
        self._destination_dir = Path(destination_dir)
        self._backup_kind = str(backup_kind)
        self._cancel_event = Event()

    def request_cancel(self) -> None:
        """Request cancellation without touching source folders."""
        self._cancel_event.set()

    def _cancel_requested(self) -> bool:
        return self._cancel_event.is_set()

    @Slot()
    def run(self) -> None:
        """Create, verify, and publish one atomic backup ZIP."""
        try:
            creator = {
                "project": _create_project_backup,
                "both": create_backup_both,
            }.get(self._backup_kind, create_show_project_backup)
            result = creator(
                self._project_root,
                self._destination_dir,
                progress=self.progress.emit,
                cancel_requested=self._cancel_requested,
            )
            self.completed.emit(result)
        except BackupCancelled as exc:
            self.cancelled.emit(str(exc))
        except Exception as exc:  # GUI boundary: never strand thread cleanup
            self.failed.emit(str(exc))
        finally:
            self.finished.emit()


class _ShowProjectBackupUiBridge(QObject):
    """Receive worker results in the GUI thread and settle the backup UI."""

    def __init__(self, window: object) -> None:
        super().__init__(window)
        self._window = window

    @Slot(str)
    def report_progress(self, message: str) -> None:
        _report_progress(self._window, message)

    @Slot(object)
    def report_success(self, payload: object) -> None:
        _report_success(self._window, payload)

    @Slot(str)
    def report_cancelled(self, message: str) -> None:
        _report_cancelled(self._window, message)

    @Slot(str)
    def report_failure(self, message: str) -> None:
        _report_failure(self._window, message)

    @Slot()
    def finish_thread(self) -> None:
        _finish_backup_thread(self._window)


def install_show_project_backup_button(window: object) -> None:
    """Connect both backup buttons and the shared cancel action."""
    show_button = getattr(window, "backup_show_project_button", None)
    project_button = getattr(window, "backup_project_button", None)
    both_button = getattr(window, "backup_both_button", None)
    cancel_button = getattr(window, "cancel_backup_button", None)
    if show_button is None:
        raise AttributeError("backup_show_project_button is missing from the window.")
    if project_button is None:
        raise AttributeError("backup_project_button is missing from the window.")
    if both_button is None:
        raise AttributeError("backup_both_button is missing from the window.")
    if cancel_button is None:
        raise AttributeError("cancel_backup_button is missing from the window.")
    show_button.clicked.connect(lambda: choose_and_start_show_project_backup(window))
    project_button.clicked.connect(lambda: _choose_and_start_project_backup(window))
    both_button.clicked.connect(lambda: _choose_and_start_both_backup(window))
    cancel_button.clicked.connect(lambda: _cancel_active_backup(window))


def choose_and_start_show_project_backup(window: object) -> None:
    """Ask for a destination folder and start one Show Project backup."""
    try:
        project_root = _selected_project_root(window)
        support_root = project_analysis_evidence_root(project_root)
        if not support_root.is_dir():
            raise FileNotFoundError(
                "Show Project folder does not exist yet: " + str(support_root)
            )
        destination = _choose_destination(
            window,
            "Select folder for Show Project backup",
            project_root,
        )
        if destination is None:
            _set_status(window, "Show Project backup cancelled before start.")
            return
        run_pre_backup_cleanup_dialog(window, project_root=project_root, support_root=support_root); start_show_project_backup(window, destination)
    except Exception as exc:
        _report_failure(
            window,
            "Could not start Show Project backup: " + str(exc),
            backup_kind="show_project",
        )


def _choose_and_start_project_backup(window: object) -> None:
    """Ask for a destination folder and start one complete Project backup."""
    try:
        project_root = _selected_project_root(window)
        destination = _choose_destination(
            window,
            "Select folder for complete Project backup",
            project_root,
        )
        if destination is None:
            _set_status(window, "Project backup cancelled before start.")
            return
        _start_project_backup(window, destination)
    except Exception as exc:
        _report_failure(
            window,
            "Could not start Project backup: " + str(exc),
            backup_kind="project",
        )


def _choose_and_start_both_backup(window: object) -> None:
    """Ask for a destination folder and start one combined backup."""
    try:
        project_root = _selected_project_root(window)
        support_root = project_analysis_evidence_root(project_root)
        if not support_root.is_dir():
            raise FileNotFoundError(
                "Show Project folder does not exist yet: " + str(support_root)
            )
        destination = _choose_destination(
            window,
            "Select folder for Project + Show Project backup",
            project_root,
        )
        if destination is None:
            _set_status(window, "Both backup cancelled before start.")
            return
        run_pre_backup_cleanup_dialog(window, project_root=project_root, support_root=support_root); _start_backup(window, destination, backup_kind="both")
    except Exception as exc:
        _report_failure(
            window,
            "Could not start combined backup: " + str(exc),
            backup_kind="both",
        )


def _choose_destination(
    window: object,
    title: str,
    project_root: Path,
) -> Path | None:
    destination = QFileDialog.getExistingDirectory(
        window,
        title,
        str(project_root.parent),
    )
    return Path(destination) if destination else None


def start_show_project_backup(window: object, destination_dir: str | Path) -> None:
    """Start one background backup for the selected Project Support root."""
    _start_backup(window, destination_dir, backup_kind="show_project")


def _start_project_backup(window: object, destination_dir: str | Path) -> None:
    """Start one background backup containing the complete selected Project."""
    _start_backup(window, destination_dir, backup_kind="project")


def _start_backup(
    window: object,
    destination_dir: str | Path,
    *,
    backup_kind: str,
) -> None:
    active_thread = getattr(window, "_active_backup_thread", None)
    if active_thread is None:
        active_thread = getattr(window, "_show_project_backup_thread", None)
    if active_thread is not None and active_thread.isRunning():
        _set_status(window, "A backup is already running. Use Cancel Backup first.")
        return

    project_root = _selected_project_root(window)
    destination = validate_backup_destination(project_root, destination_dir)
    thread = QThread(window)
    worker = ShowProjectBackupWorker(project_root, destination, backup_kind)
    bridge = _ShowProjectBackupUiBridge(window)
    worker.moveToThread(thread)
    window._active_backup_thread = thread
    window._active_backup_worker = worker
    window._active_backup_ui_bridge = bridge
    window._active_backup_kind = backup_kind
    window._show_project_backup_thread = thread
    window._show_project_backup_worker = worker
    window._show_project_backup_ui_bridge = bridge

    thread.started.connect(worker.run)
    worker.progress.connect(bridge.report_progress)
    worker.completed.connect(bridge.report_success)
    worker.cancelled.connect(bridge.report_cancelled)
    worker.failed.connect(bridge.report_failure)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(bridge.finish_thread)
    thread.finished.connect(thread.deleteLater)

    _set_backup_busy(window, True)
    _start_backup_sonar(window)
    _report_progress(window, "Preparing " + _backup_label(window) + " backup...")
    thread.start()


def _cancel_active_backup(window: object) -> None:
    thread = getattr(window, "_active_backup_thread", None)
    worker = getattr(window, "_active_backup_worker", None)
    if thread is None or worker is None or not thread.isRunning():
        _set_status(window, "No backup is currently running.")
        return
    worker.request_cancel()
    button = getattr(window, "cancel_backup_button", None)
    if button is not None:
        button.setText("Cancelling...")
        button.setEnabled(False)
    _report_progress(window, "Cancelling " + _backup_label(window) + " backup...")


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
    kind = str(getattr(window, "_active_backup_kind", "show_project"))
    show_button = getattr(window, "backup_show_project_button", None)
    project_button = getattr(window, "backup_project_button", None)
    both_button = getattr(window, "backup_both_button", None)
    cancel_button = getattr(window, "cancel_backup_button", None)
    if show_button is not None:
        show_button.setText("Backing Up..." if busy and kind == "show_project" else "Backup Show Project")
    if project_button is not None:
        project_button.setText("Backing Up..." if busy and kind == "project" else "Backup Project")
    if both_button is not None:
        both_button.setText("Backing Up..." if busy and kind == "both" else "Backup both")
    if cancel_button is not None:
        cancel_button.setText("Cancel Backup")
        cancel_button.setEnabled(busy)


def _backup_label(window: object) -> str:
    return _BACKUP_LABELS.get(str(getattr(window, "_active_backup_kind", "show_project")), "Show Project")


def _backup_sonar(window: object) -> GreenSonarActivityMonitor:
    monitor = getattr(window, "_show_project_backup_sonar_monitor", None)
    if monitor is None:
        monitor = GreenSonarActivityMonitor(
            window,
            title="Show Project Backup",
        )
        monitor.setObjectName("showProjectBackupSonarMonitor")
        window._show_project_backup_sonar_monitor = monitor
    return monitor


def _project_backup_sonar(window: object) -> GreenSonarActivityMonitor:
    monitor = getattr(window, "_project_backup_sonar_monitor", None)
    if monitor is None:
        monitor = GreenSonarActivityMonitor(window, title="Project Backup")
        monitor.setObjectName("projectBackupSonarMonitor")
        window._project_backup_sonar_monitor = monitor
    return monitor


def _both_backup_sonar(window: object) -> GreenSonarActivityMonitor:
    monitor = getattr(window, "_both_backup_sonar_monitor", None)
    if monitor is None:
        monitor = GreenSonarActivityMonitor(
            window, title="Project + Show Project Backup"
        )
        monitor.setObjectName("bothBackupSonarMonitor")
        window._both_backup_sonar_monitor = monitor
    return monitor


def _backup_sonar_for_kind(window: object, kind: str) -> GreenSonarActivityMonitor:
    if kind == "project":
        return _project_backup_sonar(window)
    if kind == "both":
        return _both_backup_sonar(window)
    return _backup_sonar(window)


def _current_backup_sonar(window: object) -> GreenSonarActivityMonitor:
    return _backup_sonar_for_kind(
        window, str(getattr(window, "_active_backup_kind", "show_project"))
    )


def _start_backup_sonar(window: object) -> None:
    label = _backup_label(window)
    _current_backup_sonar(window).start(
        "Preparing verified backup",
        (
            "Snapshotting the " + label + " folder",
            "ZIP creation and integrity validation run in a worker thread",
            "Cancel Backup removes only the unpublished partial ZIP",
        ),
    )


def _backup_sonar_details(window: object, message: str) -> tuple[str, str, str]:
    label = _backup_label(window)
    normalized = str(message or "").lower()
    if "cancelling" in normalized:
        return (
            "Cancellation requested for the active " + label + " backup",
            "The source folder remains read-only",
            "The unpublished partial ZIP is removed during worker settlement",
        )
    if "validating" in normalized:
        return (
            "Checking ZIP member integrity and expected file sizes",
            "The partial archive is published only after validation",
            "Source and destination boundaries remain fail-closed",
        )
    if "backing up" in normalized:
        return (
            "Writing the current " + label + " snapshot into the ZIP",
            "Already-compressed files are stored without recompression",
            "Source identity is checked before and after each file write",
        )
    return (
        "Preparing or settling the " + label + " backup operation",
        "Backup work remains outside the Qt GUI thread",
        "Detailed progress is also written to the log panel",
    )


def _report_progress(window: object, message: str) -> None:
    _set_status(window, message)
    _append_log(window, message)
    _current_backup_sonar(window).start(str(message), _backup_sonar_details(window, message))


def _report_success(window: object, payload: object) -> None:
    data = dict(payload) if isinstance(payload, dict) else {}
    archive_path = str(data.get("archive_path") or "")
    label = _BACKUP_LABELS.get(
        str(data.get("backup_kind") or "show_project"), "Show Project"
    )
    message = label + " backup created: " + archive_path
    _set_status(window, message)
    _append_log(window, message)
    details = (
        "Verified ZIP: " + archive_path,
        "Files: " + str(data.get("file_count") or 0),
        "Archive bytes: " + str(data.get("archive_bytes") or 0),
    )
    _current_backup_sonar(window).finish_success("Backup complete", details)


def _report_cancelled(window: object, message: str) -> None:
    label = _backup_label(window)
    status = label + " backup cancelled. Partial archive cleaned."
    _set_status(window, status)
    _append_log(window, status)
    details = (
        str(message),
        "Original source folders were not modified",
        "No partial backup archive remains published",
    )
    _current_backup_sonar(window).finish_error("Backup cancelled", details)


def _report_failure(
    window: object,
    message: str,
    *,
    backup_kind: str | None = None,
) -> None:
    kind = backup_kind or str(getattr(window, "_active_backup_kind", "show_project"))
    label = _BACKUP_LABELS.get(kind, "Show Project")
    error_message = "[ERROR] " + str(message)
    _set_status(window, error_message)
    _append_log(window, error_message)
    details = (
        str(message),
        "No incomplete archive is published as a successful backup",
        "Review the log before retrying",
    )
    _backup_sonar_for_kind(window, kind).finish_error("Backup needs review", details)
    QMessageBox.warning(window, label + " backup failed", str(message))


def _finish_backup_thread(window: object) -> None:
    _set_backup_busy(window, False)
    window._active_backup_thread = None
    window._active_backup_worker = None
    window._active_backup_ui_bridge = None
    window._active_backup_kind = None
    window._show_project_backup_thread = None
    window._show_project_backup_worker = None
    window._show_project_backup_ui_bridge = None


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
