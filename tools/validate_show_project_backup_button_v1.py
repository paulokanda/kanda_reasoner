"""Validate the Show Project backup button and archive contract."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
    show_project_backup_service as backup_service,
)

create_show_project_backup = backup_service.create_show_project_backup

FEATURE_ID = "show-project-backup-button-v1r2"


def _assert_static_contracts() -> None:
    ui_path = PROJECT_ROOT / (
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
        "window_methods_private_impl.py"
    )
    qt_helper_path = PROJECT_ROOT / (
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
        "show_project_backup_private_impl.py"
    )
    service_path = PROJECT_ROOT / (
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
        "show_project_backup_service.py"
    )
    runner_path = PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_shell/runner.py"
    manifest_path = PROJECT_ROOT / (
        "kanda_reasoner_app/reasoner_tools_shell/runner_help.json"
    )
    help_path = PROJECT_ROOT / (
        "kanda_reasoner_app/reasoner_tools_gui_help/project_structure_map.json"
    )

    ui_text = ui_path.read_text(encoding="utf-8-sig")
    qt_helper_text = qt_helper_path.read_text(encoding="utf-8-sig")
    service_text = service_path.read_text(encoding="utf-8-sig")
    runner_text = runner_path.read_text(encoding="utf-8-sig")
    manifest_text = manifest_path.read_text(encoding="utf-8-sig")
    help_text = help_path.read_text(encoding="utf-8-sig")

    browse_marker = 'self.browse_project_button = QPushButton("Browse...")'
    backup_marker = (
        'self.backup_show_project_button = QPushButton("Backup Show Project")'
    )
    assert browse_marker in ui_text
    assert backup_marker in ui_text
    assert ui_text.index(browse_marker) < ui_text.index(backup_marker)
    assert "install_show_project_backup_button(self)" in ui_text
    assert "self.backup_show_project_button," in ui_text
    assert '"backup_show_project_button"' in runner_text
    assert "QThread(window)" in qt_helper_text
    assert "worker.moveToThread(thread)" in qt_helper_text
    assert "create_show_project_backup" in service_text
    assert "project_analysis_evidence_root" in service_text
    assert "NamedTemporaryFile" in service_text
    assert "os.replace(partial_path, archive_path)" in service_text
    assert "archive.testzip()" in service_text
    assert "Symbolic links are not allowed" in service_text
    assert "is_junction" in service_text
    assert "show_project_backup_private_impl.py" in manifest_text
    assert "show_project_backup_service.py" in manifest_text
    assert "Backup Show Project" in help_text

    for path in (ui_path, qt_helper_path, service_path, runner_path):
        line_count = len(path.read_text(encoding="utf-8-sig").splitlines())
        assert line_count <= 500, str(path) + " exceeds 500 lines"

    print("BACKUP_BUTTON_AFTER_BROWSE: PASS")
    print("BACKUP_OWNER_SEPARATION: PASS")
    print("BACKUP_ATOMIC_ZIP_CONTRACT: PASS")
    print("TOUCHED_MODULE_SIZE_LIMIT: PASS")


def _prepare_fixture(base: Path) -> tuple[Path, Path, Path]:
    project_root = base / "eeg_kanda"
    project_root.mkdir()
    support_root = base / "eeg_kanda_show_project_to_AI"
    (support_root / "first_prompt_files").mkdir(parents=True)
    (support_root / "second_prompt_files" / "empty_folder").mkdir(parents=True)
    (support_root / "project_freeze_after_update").mkdir(parents=True)
    (support_root / "project_error_memory").mkdir(parents=True)
    (support_root / "first_prompt_files" / "tell_AI_read_before_all.md").write_text(
        "startup\n",
        encoding="utf-8",
    )
    (support_root / "second_prompt_files" / "handoff.json").write_text(
        '{"status": "ready"}\n',
        encoding="utf-8",
    )
    (support_root / "project_freeze_after_update" / "entry.md").write_text(
        "frozen\n",
        encoding="utf-8",
    )
    (support_root / "project_error_memory" / "lesson.json").write_text(
        '{"lesson": "active"}\n',
        encoding="utf-8",
    )
    for index in range(300):
        (support_root / "second_prompt_files" / f"item_{index:04d}.txt").write_text(
            "backup validation payload " + str(index) + "\n",
            encoding="utf-8",
        )
    destination = base / "backups"
    destination.mkdir()
    return project_root, support_root, destination


def _assert_archive_contract(
    project_root: Path,
    support_root: Path,
    destination: Path,
) -> None:
    fixed_time = datetime(2026, 7, 29, 1, 2, 3)
    result = create_show_project_backup(
        project_root,
        destination,
        timestamp=fixed_time,
    )
    archive_path = Path(str(result["archive_path"]))
    assert Path(str(result["source_root"])) == support_root
    assert archive_path.name == (
        "eeg_kanda_show_project_to_AI_backup_2026-07-29_010203.zip"
    )
    assert archive_path.is_file()
    assert not list(destination.glob("*.partial"))

    handoff_path = support_root / "second_prompt_files" / "handoff.json"
    lesson_path = support_root / "project_error_memory" / "lesson.json"
    expected_handoff = handoff_path.read_bytes()
    expected_lesson = lesson_path.read_bytes()

    with zipfile.ZipFile(archive_path, "r") as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
        prefix = support_root.name + "/"
        assert prefix in names
        assert prefix + "second_prompt_files/empty_folder/" in names
        assert (
            archive.read(prefix + "second_prompt_files/handoff.json")
            == expected_handoff
        )
        assert (
            archive.read(prefix + "project_error_memory/lesson.json")
            == expected_lesson
        )

    second_result = create_show_project_backup(
        project_root,
        destination,
        timestamp=fixed_time,
    )
    assert Path(str(second_result["archive_path"])).name.endswith("_02.zip")

    nested_destination = project_root / "backups"
    nested_destination.mkdir()
    try:
        create_show_project_backup(project_root, nested_destination)
    except ValueError as exc:
        assert "outside the selected Project source root" in str(exc)
    else:
        raise AssertionError("Project-source destination was not rejected.")

    support_destination = support_root / "backups"
    support_destination.mkdir()
    try:
        create_show_project_backup(project_root, support_destination)
    except ValueError as exc:
        assert "outside the Show Project folder" in str(exc)
    else:
        raise AssertionError("Show Project destination was not rejected.")

    print("BACKUP_FILENAME_IDENTITY: PASS")
    print("BACKUP_CONTENT_AND_EMPTY_DIRECTORY: PASS")
    print("PLATFORM_NEUTRAL_ARCHIVE_BYTE_IDENTITY: PASS")
    print("BACKUP_COLLISION_SAFE_NAMING: PASS")
    print("BACKUP_DESTINATION_BOUNDARY: PASS")


def _assert_source_change_fail_closed(
    project_root: Path,
    support_root: Path,
    base: Path,
) -> None:
    destination = base / "mutation_backup"
    destination.mkdir()
    late_file = support_root / "second_prompt_files" / "zzzz_mutated.txt"
    late_file.write_text("before\n", encoding="utf-8")
    changed = {"done": False}

    def mutate_after_progress(message: str) -> None:
        if changed["done"] or not message.startswith("Backing up Show Project files:"):
            return
        late_file.write_text("after\n", encoding="utf-8")
        changed["done"] = True

    try:
        create_show_project_backup(
            project_root,
            destination,
            timestamp=datetime(2026, 7, 29, 1, 2, 4),
            progress=mutate_after_progress,
        )
    except RuntimeError as exc:
        assert "content changed during backup" in str(exc)
    else:
        raise AssertionError("Source mutation did not fail closed.")
    assert changed["done"]
    assert not list(destination.glob("*.zip"))
    assert not list(destination.glob("*.partial"))
    late_file.unlink()
    print("BACKUP_SOURCE_CHANGE_FAIL_CLOSED: PASS")


def _assert_symlink_rejection(
    project_root: Path,
    support_root: Path,
    destination: Path,
) -> None:
    external = project_root.parent / "external_secret.txt"
    external.write_text("outside\n", encoding="utf-8")
    link = support_root / "external_link.txt"
    try:
        link.symlink_to(external)
    except (OSError, NotImplementedError):
        print("BACKUP_SYMLINK_ESCAPE_REJECTION: N/A")
        return
    try:
        create_show_project_backup(project_root, destination)
    except ValueError as exc:
        assert "Symbolic links are not allowed" in str(exc)
    else:
        raise AssertionError("Symbolic-link escape was not rejected.")
    finally:
        link.unlink(missing_ok=True)
    print("BACKUP_SYMLINK_ESCAPE_REJECTION: PASS")


def _assert_real_qt_background_route(
    project_root: Path,
    destination: Path,
    *,
    require_qt: bool,
) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from unittest.mock import patch

        from PySide6.QtCore import QEventLoop, QTimer
        from PySide6.QtWidgets import (
            QApplication,
            QLabel,
            QLineEdit,
            QPushButton,
            QWidget,
        )
        from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
            show_project_backup_private_impl as backup_impl,
        )
    except ModuleNotFoundError as exc:
        if require_qt:
            raise AssertionError("PySide6 is required for live Qt validation.") from exc
        print("REAL_QT_BACKUP_EVENT_LOOP_HEARTBEAT: BLOCKED - PySide6 unavailable")
        print("REAL_QT_BACKUP_BUTTON_STATE_RECOVERY: BLOCKED - PySide6 unavailable")
        return

    class TestWindow(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.project_root_edit = QLineEdit(str(project_root))
            self.backup_show_project_button = QPushButton("Backup Show Project")
            self.browse_project_button = QPushButton("Browse...")
            self.create_first_and_second_prompt_files_button = QPushButton(
                "Create Both"
            )
            self.create_first_prompt_files_button = QPushButton("Create First")
            self.run_button = QPushButton("Create Second")
            self.close_button = QPushButton("Close")
            self.first_prompt_status_label = QLabel("Idle")
            self.status_label = QLabel("Idle")
            self.messages: list[str] = []

        def _append_log(self, message: str) -> None:
            self.messages.append(message)

    app = QApplication.instance() or QApplication([])
    window = TestWindow()
    information_calls: list[str] = []
    warning_calls: list[str] = []
    heartbeat = {"count": 0, "timed_out": False}
    event_loop = QEventLoop()
    heartbeat_timer = QTimer()
    heartbeat_timer.setInterval(1)
    heartbeat_timer.timeout.connect(
        lambda: heartbeat.__setitem__("count", heartbeat["count"] + 1)
    )
    timeout_timer = QTimer()
    timeout_timer.setSingleShot(True)

    def timeout() -> None:
        heartbeat["timed_out"] = True
        event_loop.quit()

    timeout_timer.timeout.connect(timeout)

    with patch.object(
        backup_impl.QMessageBox,
        "information",
        side_effect=lambda _parent, _title, message: information_calls.append(message),
    ), patch.object(
        backup_impl.QMessageBox,
        "warning",
        side_effect=lambda _parent, _title, message: warning_calls.append(message),
    ):
        backup_impl.start_show_project_backup(window, destination)
        assert not window.backup_show_project_button.isEnabled()
        assert window.backup_show_project_button.text() == "Backing Up..."
        thread = window._show_project_backup_thread
        thread.finished.connect(event_loop.quit)
        heartbeat_timer.start()
        timeout_timer.start(30000)
        event_loop.exec()
        heartbeat_timer.stop()
        timeout_timer.stop()
        app.processEvents()

    assert not heartbeat["timed_out"]
    assert heartbeat["count"] > 0
    assert window.backup_show_project_button.isEnabled()
    assert window.backup_show_project_button.text() == "Backup Show Project"
    assert information_calls
    assert not warning_calls
    assert "Show Project backup created:" in window.first_prompt_status_label.text()
    assert window._show_project_backup_thread is None
    assert window._show_project_backup_worker is None

    print("REAL_QT_BACKUP_EVENT_LOOP_HEARTBEAT: PASS")
    print("REAL_QT_BACKUP_BUTTON_STATE_RECOVERY: PASS")
    print("REAL_QT_BACKUP_TERMINAL_SIGNAL: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-qt", action="store_true")
    args = parser.parse_args()

    _assert_static_contracts()
    with tempfile.TemporaryDirectory(prefix="kanda_show_project_backup_") as temp_dir:
        base = Path(temp_dir)
        project_root, support_root, destination = _prepare_fixture(base)
        canonical_support_root = project_analysis_evidence_root(project_root)
        assert support_root.parent == base
        if os.name == "nt":
            assert support_root != canonical_support_root
        with patch.object(
            backup_service,
            "project_analysis_evidence_root",
            return_value=support_root,
        ):
            _assert_archive_contract(project_root, support_root, destination)
            _assert_source_change_fail_closed(
                project_root, support_root, base
            )
            _assert_symlink_rejection(project_root, support_root, destination)
            _assert_real_qt_background_route(
                project_root,
                destination,
                require_qt=args.require_qt,
            )
        assert support_root.is_dir()
    print("BACKUP_VALIDATION_SUPPORT_ISOLATED: PASS")
    print("WINDOWS_DRIVE_ROOT_VALIDATION_FIXTURE_REGRESSION_BLOCKED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
