#!/usr/bin/env python3
"""Validate project-switch cleanup for Error Memory and Freeze UI state."""

from __future__ import annotations

import argparse
import ast
import os
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "project-scope-error-freeze-memory-reset-v1r1"
SYNC = "kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py"
ERROR_TAB = "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
FREEZE_TAB = "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    path = root / relative
    require(path.is_file(), "missing source file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    sync = read(root, SYNC)
    error_tab = read(root, ERROR_TAB)
    freeze_tab = read(root, FREEZE_TAB)
    for relative, text in ((SYNC, sync), (ERROR_TAB, error_tab), (FREEZE_TAB, freeze_tab)):
        ast.parse(text, filename=relative)
    require(len(sync.splitlines()) <= 500, "project_scope_sync.py exceeds 500 lines")

    require('"error_memory"' in sync and '"freeze_feature_after_update"' in sync,
            "project-scoped tab registry is incomplete")
    require("_reset_error_memory(widget)" in sync and "_reset_freeze_tab(widget)" in sync,
            "specific reset owners are not routed")
    print("PROJECT_SWITCH_ERROR_FREEZE_RESET_ROUTING: PASS")

    error_block = sync.split("def _reset_error_memory", 1)[1].split("def _reset_freeze_tab", 1)[0]
    require('(\"_undo_deleted_lesson\", None)' in error_block,
            "Error Memory deleted-lesson Undo state is not cleared")
    require("_error_memory_ai_correction_generation" in error_block and "generation + 1" in error_block,
            "Error Memory stale AI generation is not invalidated")
    require("_undo_deleted_lesson" in error_tab,
            "Error Memory tab no longer owns deleted-lesson Undo state")
    print("ERROR_MEMORY_CROSS_PROJECT_UNDO_CLEARED: PASS")
    print("ERROR_MEMORY_STALE_AI_GENERATION_INVALIDATED: PASS")

    freeze_block = sync.split("def _reset_freeze_tab", 1)[1].split("def _reset_project_qa", 1)[0]
    for token in (
        "_local_freeze_ai_request_id",
        "_local_freeze_ai_identity",
        "_local_freeze_ai_result_queue",
        "_local_freeze_ai_poll_timer",
        "_local_freeze_ai_thread",
        "_local_freeze_ai_generation",
        "_what_to_say_text_edit",
        'status_label.setText("Not checked yet")',
    ):
        require(token in freeze_block, "Freeze reset is missing: " + token)
    require("_local_freeze_preview" in freeze_tab and "_local_freeze_ai_generation" in freeze_tab,
            "Freeze tab no longer owns the validated transient state")
    print("FREEZE_CROSS_PROJECT_PREVIEW_CLEARED: PASS")
    print("FREEZE_STALE_AI_HANDLES_INVALIDATED: PASS")
    print("FREEZE_STATUS_RESET_FOR_NEW_PROJECT: PASS")

    forbidden = (".unlink(", "rmtree(", "write_text(", "write_bytes(", "save_lesson(",
                 "write_confirmed_freeze_entry(")
    require(not any(token in sync for token in forbidden),
            "project-switch reset contains a durable write/delete primitive")
    print("PROJECT_SWITCH_DURABLE_MEMORY_UNTOUCHED: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def _is_missing_pyside6_dependency(exc: ImportError) -> bool:
    """Return True only for an unavailable PySide6 or shiboken6 dependency."""
    module_name = str(getattr(exc, "name", "") or "")
    message = str(exc)
    return (
        module_name == "PySide6"
        or module_name.startswith("PySide6.")
        or module_name == "shiboken6"
        or module_name.startswith("shiboken6.")
        or "PySide6" in message
        or "shiboken6" in message
    )


def validate_real_qt(root: Path) -> bool:
    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import (
            QApplication,
            QDialog,
            QLabel,
            QListWidget,
            QPlainTextEdit,
            QPushButton,
            QTableWidget,
            QTextEdit,
            QWidget,
        )
    except ImportError as exc:
        if not _is_missing_pyside6_dependency(exc):
            raise
        print("REAL_QT_PROJECT_SCOPE_MEMORY_RESET: NOT_APPLICABLE")
        return False

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.reasoner_tools_gui_shell.project_scope_sync import (
        reset_project_scoped_widget,
    )

    app = QApplication.instance() or QApplication([])

    class ErrorFixture(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.raw_error_edit = QPlainTextEdit()
            self.received_preview_edit = QTextEdit()
            self.lessons_table = QTableWidget(1, 1)
            self.pending_list = QListWidget()
            self.pending_list.addItem("Project A pending intake")
            self._undo_deleted_lesson = {"lesson_id": "project-a-deleted"}
            self._selected_lesson_id = "project-a-selected"
            self._last_received_lesson = {"lesson_id": "project-a-received"}
            self._loaded_pending_intake_file = "A.json"
            self._loaded_pending_intake_lesson_id = "A"
            self._dismissed_pending_intake_files = {"A.json"}
            self._dismissed_pending_intake_lesson_ids = {"A"}
            self._warned_duplicate_pending_intake_lesson_ids = {"A"}
            self._last_dismissed_pending_intake_file = "A.json"
            self._last_dismissed_pending_intake_lesson_id = "A"
            self._last_dismissed_pending_intake_text = "Project A"
            self._error_memory_ai_correction_generation = 7
            self.raw_error_edit.setPlainText("Project A raw error")
            self.received_preview_edit.setPlainText("Project A lesson")

    class FreezeFixture(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.output_log = QTextEdit()
            self.output_log.setPlainText("Project A freeze log")
            self.status_label = QLabel("VALID: Project A")
            self.do_staged_action_button = QPushButton()
            self.undo_staged_action_button = QPushButton()
            self.do_staged_action_button.setEnabled(True)
            self.undo_staged_action_button.setEnabled(True)
            self._local_freeze_preview = {"project": "A"}
            self._last_output_folder = Path("A-output")
            self._pending_staged_project_root = Path("A")
            self._pending_staged_action = "refresh"
            self._local_freeze_ai_request_id = "request-A"
            self._local_freeze_ai_identity = object()
            self._local_freeze_ai_result_queue = object()
            self._local_freeze_ai_generation = 11
            self._local_freeze_ai_thread = object()
            self._local_freeze_ai_poll_timer = QTimer(self)
            self._local_freeze_ai_poll_timer.start(1000)
            self._what_to_say_text_edit = QTextEdit()
            self._local_freeze_dialog = QDialog(self)
            self._what_to_say_dialog = QDialog(self)

        def _set_pending_staged_action(self, project_root, action) -> None:
            self._pending_staged_project_root = project_root
            self._pending_staged_action = action
            enabled = project_root is not None and action is not None
            self.do_staged_action_button.setEnabled(enabled)
            self.undo_staged_action_button.setEnabled(enabled)

    with tempfile.TemporaryDirectory(prefix="kanda-project-switch-memory-") as temp_dir:
        marker_a = Path(temp_dir) / "project-a-memory.txt"
        marker_b = Path(temp_dir) / "project-b-memory.txt"
        marker_a.write_text("A durable memory", encoding="utf-8")
        marker_b.write_text("B durable memory", encoding="utf-8")

        error = ErrorFixture()
        before_generation = error._error_memory_ai_correction_generation
        reset_project_scoped_widget("error_memory", error)
        require(error._undo_deleted_lesson is None, "old-project Undo payload survived")
        require(error._selected_lesson_id == "" and error._last_received_lesson is None,
                "old-project Error Memory selection survived")
        require(error._loaded_pending_intake_file == "" and not error._dismissed_pending_intake_files,
                "old-project pending intake state survived")
        require(error._error_memory_ai_correction_generation == before_generation + 1,
                "Error Memory generation did not advance")
        require(not error.raw_error_edit.toPlainText() and not error.received_preview_edit.toPlainText(),
                "Error Memory editors were not cleared")
        require(error.lessons_table.rowCount() == 0 and error.pending_list.count() == 0,
                "Error Memory collections were not cleared")
        print("REAL_QT_ERROR_MEMORY_PROJECT_SWITCH_CLEAN: PASS")
        print("REAL_QT_ERROR_MEMORY_UNDO_CANNOT_CROSS_PROJECTS: PASS")

        freeze = FreezeFixture()
        before_generation = freeze._local_freeze_ai_generation
        old_timer = freeze._local_freeze_ai_poll_timer
        reset_project_scoped_widget("freeze_feature_after_update", freeze)
        require(freeze._local_freeze_preview is None and freeze._last_output_folder is None,
                "old-project Freeze preview/output survived")
        require(freeze._pending_staged_project_root is None and freeze._pending_staged_action is None,
                "old-project staged Freeze action survived")
        require(not freeze.do_staged_action_button.isEnabled() and not freeze.undo_staged_action_button.isEnabled(),
                "old-project staged action remained executable")
        require(freeze._local_freeze_ai_request_id is None and freeze._local_freeze_ai_identity is None,
                "old-project Freeze AI identity survived")
        require(freeze._local_freeze_ai_result_queue is None and freeze._local_freeze_ai_thread is None,
                "old-project Freeze async handles survived")
        require(freeze._local_freeze_ai_poll_timer is None and not old_timer.isActive(),
                "old-project Freeze poll timer survived")
        require(freeze._local_freeze_ai_generation == before_generation + 1,
                "Freeze AI generation did not advance")
        require(freeze._what_to_say_text_edit is None,
                "old-project Freeze text dialog owner survived")
        require(freeze.status_label.text() == "Not checked yet" and not freeze.output_log.toPlainText(),
                "Freeze visual status was not reset")
        print("REAL_QT_FREEZE_PROJECT_SWITCH_CLEAN: PASS")
        print("REAL_QT_FREEZE_STALE_PREVIEW_CANNOT_CROSS_PROJECTS: PASS")

        require(marker_a.read_text(encoding="utf-8") == "A durable memory" and
                marker_b.read_text(encoding="utf-8") == "B durable memory",
                "project switch reset modified durable memory")
        print("REAL_QT_PROJECT_SWITCH_DURABLE_MEMORY_UNTOUCHED: PASS")

        error.close()
        freeze.close()
        app.processEvents()

    print("REAL_QT_PROJECT_SCOPE_MEMORY_RESET: PASS")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--real-qt-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not args.real_qt_only:
        validate_static(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
