# project-path: tools/validate_local_freeze_entry_responsive_open_v1.py
"""Validate responsive Local Freeze Entry bootstrap with real Qt."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
import tempfile
import time

FEATURE_ID = "local-freeze-entry-responsive-open-v1r1"
TARGETS = (
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_bootstrap_worker.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py",
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "tools/validate_local_freeze_entry_responsive_open_v1.py",
)


def _read(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise AssertionError("Missing expected file: " + relative)
    return path.read_text(encoding="utf-8")


def _validate_static(root: Path) -> None:
    for relative in TARGETS:
        source = _read(root, relative)
        ast.parse(source, filename=relative)
        if len(source.splitlines()) > 500:
            raise AssertionError(relative + " exceeds 500 physical lines")
        source.encode("ascii")

    worker = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_bootstrap_worker.py",
    )
    runtime = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py",
    )
    tab = _read(
        root,
        "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    )
    required_worker = (
        "class _LocalFreezeBootstrapWorker(QObject)",
        "worker.moveToThread(thread)",
        "thread.finished.connect(relay.settle",
        "QThread.currentThread().isInterruptionRequested()",
        "build_freeze_form_inputs_from_latest_hint(",
        "preview_freeze_entry(project_root, inputs)",
        "validate_freeze_entry_preview(project_root, preview)",
    )
    for token in required_worker:
        if token not in worker:
            raise AssertionError("Missing QThread bootstrap contract: " + token)
    if "ai_runtime.fill_selected()" in runtime:
        raise AssertionError("Local Freeze dialog still runs synchronous initial fill")
    show_index = runtime.find("        dialog.show()")
    start_index = runtime.find("        job.start()")
    if show_index < 0 or start_index < 0 or show_index >= start_index:
        raise AssertionError("Local Freeze dialog must show before bootstrap starts")
    for token in (
        "Stale Local Freeze bootstrap result discarded",
        "Local Freeze intake and initial Preview completed off the GUI thread.",
        "LOCAL FREEZE CONFIRMATION BINDING BLOCKED",
        "Active Project authority is unavailable",
        "current_job.request_cancel()",
        "self._local_freeze_bootstrap_retired_jobs.append(current_job)",
    ):
        if token not in runtime:
            raise AssertionError("Missing responsive settlement contract: " + token)
    for token in (
        "self._local_freeze_bootstrap_generation = 0",
        "self._local_freeze_bootstrap_job: Any = None",
        "self._local_freeze_bootstrap_retired_jobs: list[Any] = []",
    ):
        if token not in tab:
            raise AssertionError("Missing Local Freeze job registry: " + token)
    print("LOCAL_FREEZE_BOOTSTRAP_QTHREAD: PASS")
    print("LOCAL_FREEZE_DIALOG_SHOWS_BEFORE_BOOTSTRAP: PASS")
    print("LOCAL_FREEZE_STALE_RESULT_QUARANTINE: PASS")
    print("LOCAL_FREEZE_AUTHORITY_ERROR_UI_GUARD: PASS")


def _run_event_loop(milliseconds: int) -> None:
    from PySide6.QtCore import QEventLoop, QTimer

    loop = QEventLoop()
    QTimer.singleShot(milliseconds, loop.quit)
    loop.exec()


def _button(dialog: object, text: str):
    from PySide6.QtWidgets import QPushButton

    for button in dialog.findChildren(QPushButton):
        if button.text() == text:
            return button
    raise AssertionError("Missing dialog button: " + text)


def _line_edit(dialog: object, placeholder: str):
    from PySide6.QtWidgets import QLineEdit

    for editor in dialog.findChildren(QLineEdit):
        if editor.placeholderText() == placeholder:
            return editor
    raise AssertionError("Missing line edit: " + placeholder)


def _validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from PySide6.QtCore import QThread, QTimer
    from PySide6.QtWidgets import QApplication

    from kanda_reasoner_app.freeze_after_update_gui import (
        _local_freeze_bootstrap_worker as worker_module,
    )
    from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
        FreezeAfterUpdateTab,
    )
    from kanda_reasoner_app import project_operation_authority as authority_module
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )

    app = QApplication.instance() or QApplication([])
    original_build = worker_module.build_freeze_form_inputs_from_latest_hint
    original_preview = worker_module.preview_freeze_entry
    original_validate = worker_module.validate_freeze_entry_preview

    inputs = {
        "feature_title": "Responsive Local Freeze Entry v1r1",
        "primary_box": "freeze_after_update_gui",
        "box_type": "Module Box",
        "validated_files": (
            "kanda_reasoner_app/freeze_after_update_gui/"
            "_local_freeze_dialog_runtime.py"
        ),
        "generated_files": "",
        "protected_paths": "project_freeze_after_update/frozen_features_memory/",
        "do_not_regress_rules": "Preview remains read-only.",
        "validation_evidence_summary": (
            "VALIDATION OK: local-freeze-entry-responsive-open-v1r1\n"
            "STATUS: IN_SYNC"
        ),
        "known_warnings": "",
        "planned_next_step": "Human review.",
        "notes": "Real Qt responsiveness fixture.",
    }

    def delayed_build(*_args: object, **_kwargs: object) -> dict[str, str]:
        time.sleep(0.80)
        return dict(inputs)

    def fake_preview(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {
            "ok": True,
            "is_writable": True,
            "markdown": "# Responsive preview\n",
            "errors": [],
            "warnings": [],
        }

    def fake_validate(*_args: object, **_kwargs: object) -> dict[str, object]:
        return {"ok": True, "errors": [], "warnings": []}

    worker_module.build_freeze_form_inputs_from_latest_hint = delayed_build
    worker_module.preview_freeze_entry = fake_preview
    worker_module.validate_freeze_entry_preview = fake_validate

    tab = FreezeAfterUpdateTab()
    original_registry_type = authority_module.ProjectSelectionRegistry
    try:
        with tempfile.TemporaryDirectory(prefix="kanda_local_freeze_qt_") as temp:
            temp_root = Path(temp)
            project_root = temp_root / "responsive_project"
            project_root.mkdir()
            registry_path = temp_root / "tool_support" / "projects.json"
            registry_type = ProjectSelectionRegistry
            authority_module.ProjectSelectionRegistry = lambda **_kwargs: registry_type(
                tool_source_root=root,
                registry_path=registry_path,
            )
            selection = registry_type(
                tool_source_root=root,
                registry_path=registry_path,
            )
            selection.register_explicit_root(project_root)
            print("LOCAL_FREEZE_VALIDATOR_ACTIVE_PROJECT_REGISTERED: PASS")
            tab.set_project_root(project_root)
            click_started = time.monotonic()
            tab.new_local_freeze_entry_button.click()
            click_elapsed = time.monotonic() - click_started
            dialog = tab._local_freeze_dialog
            if dialog is None or not dialog.isVisible():
                raise AssertionError("Local Freeze dialog was not visible immediately")
            if click_elapsed >= 0.50:
                raise AssertionError(
                    "Local Freeze click blocked for " + str(round(click_elapsed, 3))
                )
            print("LOCAL_FREEZE_DIALOG_VISIBLE_BEFORE_INTAKE_COMPLETES: PASS")

            feature_edit = _line_edit(
                dialog,
                "Example: Local Freeze Writer Contract v1.1",
            )
            apply_threads: list[object] = []
            feature_edit.textChanged.connect(
                lambda _text: apply_threads.append(QThread.currentThread())
            )
            heartbeat = {"count": 0}
            timer = QTimer()
            timer.setInterval(20)
            timer.timeout.connect(
                lambda: heartbeat.__setitem__("count", heartbeat["count"] + 1)
            )
            timer.start()
            _run_event_loop(280)
            timer.stop()
            if heartbeat["count"] < 5:
                raise AssertionError("Qt event-loop heartbeat stalled during bootstrap")
            if feature_edit.text():
                raise AssertionError("Delayed intake completed before heartbeat window")
            print("LOCAL_FREEZE_GUI_HEARTBEAT: PASS")

            deadline = time.monotonic() + 4.0
            while not feature_edit.text() and time.monotonic() < deadline:
                app.processEvents()
                time.sleep(0.01)
            if feature_edit.text() != inputs["feature_title"]:
                raise AssertionError("Bootstrap result was not applied")
            if not apply_threads or any(thread is not app.thread() for thread in apply_threads):
                raise AssertionError("Bootstrap result was not applied on the GUI thread")
            if not _button(dialog, "Confirm and Write Freeze Entry").isEnabled():
                raise AssertionError("Validated Preview did not preserve human confirmation")
            print("LOCAL_FREEZE_BOOTSTRAP_APPLY_ON_GUI_THREAD: PASS")
            print("LOCAL_FREEZE_PREVIEW_CONFIRMATION_PRESERVED: PASS")

            existing = dialog
            tab.new_local_freeze_entry_button.click()
            if tab._local_freeze_dialog is not existing:
                raise AssertionError("Second click created a duplicate formulary window")
            print("LOCAL_FREEZE_SINGLE_WINDOW_GUARD: PASS")
            dialog.close()
            _run_event_loop(80)

            selection.clear_current_selection()
            tab.set_project_root(project_root)
            tab.new_local_freeze_entry_button.click()
            authority_dialog = tab._local_freeze_dialog
            if authority_dialog is None or not authority_dialog.isVisible():
                raise AssertionError(
                    "Local Freeze authority-error dialog was not visible"
                )
            authority_feature_edit = _line_edit(
                authority_dialog,
                "Example: Local Freeze Writer Contract v1.1",
            )
            deadline = time.monotonic() + 4.0
            while not authority_feature_edit.text() and time.monotonic() < deadline:
                app.processEvents()
                time.sleep(0.01)
            confirm_button = _button(
                authority_dialog,
                "Confirm and Write Freeze Entry",
            )
            if confirm_button.isEnabled():
                raise AssertionError(
                    "Missing Active Project authority did not disable confirmation"
                )
            if "Active Project authority is unavailable" not in (
                confirm_button.toolTip()
            ):
                raise AssertionError(
                    "Missing Active Project authority was not explained"
                )
            print("LOCAL_FREEZE_MISSING_AUTHORITY_FAILS_CLOSED: PASS")
            authority_dialog.close()
            _run_event_loop(80)
    finally:
        authority_module.ProjectSelectionRegistry = original_registry_type
        worker_module.build_freeze_form_inputs_from_latest_hint = original_build
        worker_module.preview_freeze_entry = original_preview
        worker_module.validate_freeze_entry_preview = original_validate
        tab.close()
        app.processEvents()

    print("LOCAL_FREEZE_RESPONSIVE_REAL_QT_V1R1: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    _validate_static(root)
    _validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
