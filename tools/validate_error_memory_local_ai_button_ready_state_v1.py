# project-path: tools/validate_error_memory_local_ai_button_ready_state_v1.py
"""Validate immediate standby restoration for Error Memory Correct with AI."""

from __future__ import annotations

import argparse
import ast
import os
import py_compile
import threading
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

FEATURE_ID = "error-memory-local-ai-button-ready-state-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ACTION_PATH = "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def function_source(text: str, name: str) -> str:
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return ast.get_source_segment(text, node) or ""
    raise AssertionError("Function not found: " + name)


def method_source(text: str, class_name: str, method_name: str) -> str:
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == method_name:
                    return ast.get_source_segment(text, child) or ""
    raise AssertionError(f"Method not found: {class_name}.{method_name}")


def validate_static_contract() -> None:
    action_path = PROJECT_ROOT / ACTION_PATH
    require(action_path.is_file(), "AI correction action is missing")
    py_compile.compile(str(action_path), doraise=True)
    py_compile.compile(str(Path(__file__)), doraise=True)

    text = read(ACTION_PATH)
    helper = function_source(text, "_restore_terminal_button_state")
    require("terminal_ui_ready" in helper, "Terminal UI restoration is not idempotent")
    require("_set_running_state(tab, False)" in helper, "Standby state is not restored")
    require("thread.quit()" in helper, "Terminal result does not expedite thread shutdown")

    on_result = method_source(text, "_AICorrectionReceiver", "on_result")
    on_failure = method_source(text, "_AICorrectionReceiver", "on_failure")
    require(
        on_result.index("_restore_terminal_button_state(tab, job)")
        < on_result.index("apply_corrected_lesson_to_work_windows"),
        "Success result restores the button only after preview application",
    )
    require(
        on_result.index("_restore_terminal_button_state(tab, job)")
        < on_result.index("_show_success"),
        "Success result restores the button only after its notification",
    )
    require(
        on_failure.index("_restore_terminal_button_state(tab, job)")
        < on_failure.index("_show_copyable_error"),
        "Failure result restores the button only after its notification",
    )

    thread_finished = method_source(text, "_AICorrectionReceiver", "on_thread_finished")
    require("_ACTIVE_JOBS.pop" in thread_finished, "Thread-finish cleanup was removed")
    require("_set_running_state(tab, False)" in thread_finished, "Cleanup is not idempotent")
    print("CORRECT_WITH_AI_TERMINAL_BUTTON_STATE_OWNER: PASS")
    print("CORRECT_WITH_AI_SUCCESS_STANDBY_BEFORE_NOTICE: PASS")
    print("CORRECT_WITH_AI_FAILURE_STANDBY_BEFORE_NOTICE: PASS")
    print("CORRECT_WITH_AI_THREAD_FINISH_CLEANUP_PRESERVED: PASS")


def _wait_for(app: Any, predicate: Callable[[], bool], timeout: float = 2.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.005)
    app.processEvents()
    return bool(predicate())


def validate_real_qt_runtime() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication, QPlainTextEdit, QPushButton, QWidget

    from kanda_reasoner_app.error_memory_gui import _ai_correction_action as action
    from kanda_reasoner_app.error_memory_gui import _ai_correction_worker as worker_module

    app = QApplication.instance() or QApplication([])

    class Tab(QWidget):
        def __init__(self, intake: str, editor: str) -> None:
            super().__init__()
            self.raw_error_edit = QPlainTextEdit(self)
            self.raw_error_edit.setPlainText(intake)
            self.received_preview_edit = QPlainTextEdit(self)
            self.received_preview_edit.setPlainText(editor)
            self.correct_with_ai_button = QPushButton("Correct with AI", self)
            self._project_root = PROJECT_ROOT
            self._error_memory_ai_correction_generation = 0
            self.applied_lesson_id = ""

    original_service = worker_module.correct_error_memory_lesson_with_local_ai
    original_apply = action.apply_corrected_lesson_to_work_windows
    original_success = action._show_success
    original_error = action._show_copyable_error
    tabs: list[QWidget] = []

    try:
        success_observed: dict[str, Any] = {}
        success_event = threading.Event()
        success_tab = Tab("intake", "editor")
        tabs.append(success_tab)

        def successful_service(**_kwargs: Any) -> Any:
            time.sleep(0.04)
            return SimpleNamespace(
                ok=True,
                lesson_block=SimpleNamespace(lesson_id="lesson-ready-button-success-v1"),
                message="Correction completed.",
                raw_response="",
            )

        def apply_preview(tab: Any, block: Any) -> None:
            tab.applied_lesson_id = str(getattr(block, "lesson_id", ""))

        def capture_success(tab: Any, _title: str, _message: str) -> None:
            success_observed.update(
                text=tab.correct_with_ai_button.text(),
                enabled=tab.correct_with_ai_button.isEnabled(),
                job_active=action._job_for(tab) is not None,
            )
            success_event.set()

        worker_module.correct_error_memory_lesson_with_local_ai = successful_service
        action.apply_corrected_lesson_to_work_windows = apply_preview
        action._show_success = capture_success
        action.run_error_memory_ai_correction_from_tab(success_tab)

        require(
            _wait_for(app, success_event.is_set),
            "Success notification was not reached",
        )
        require(
            success_observed.get("text") == "Correct with AI",
            "Button label was still busy when the completed correction was shown",
        )
        require(
            success_observed.get("enabled") is True,
            "Button was not returned to standby when the completed correction was shown",
        )
        require(
            success_observed.get("job_active") is True,
            "Test did not observe the terminal state before thread-finish cleanup",
        )
        require(
            success_tab.applied_lesson_id == "lesson-ready-button-success-v1",
            "Successful preview was not applied",
        )
        require(
            _wait_for(app, lambda: action._job_for(success_tab) is None),
            "Successful job did not finish cleanup",
        )

        failure_observed: dict[str, Any] = {}
        failure_event = threading.Event()
        failure_tab = Tab("failure intake", "failure editor")
        tabs.append(failure_tab)

        def failed_service(**_kwargs: Any) -> Any:
            time.sleep(0.04)
            raise RuntimeError("audited terminal failure")

        def capture_error(parent: Any, **kwargs: Any) -> None:
            if "audited terminal failure" not in str(kwargs.get("message", "")):
                return
            failure_observed.update(
                text=parent.correct_with_ai_button.text(),
                enabled=parent.correct_with_ai_button.isEnabled(),
                job_active=action._job_for(parent) is not None,
            )
            failure_event.set()

        worker_module.correct_error_memory_lesson_with_local_ai = failed_service
        action._show_copyable_error = capture_error
        action.run_error_memory_ai_correction_from_tab(failure_tab)

        require(
            _wait_for(app, failure_event.is_set),
            "Failure notification was not reached",
        )
        require(
            failure_observed.get("text") == "Correct with AI",
            "Button label was still busy when failure completion was shown",
        )
        require(
            failure_observed.get("enabled") is True,
            "Button was not returned to standby when failure completion was shown",
        )
        require(
            failure_observed.get("job_active") is True,
            "Failure test did not observe state before thread cleanup",
        )
        require(
            _wait_for(app, lambda: action._job_for(failure_tab) is None),
            "Failed job did not finish cleanup",
        )
    finally:
        worker_module.correct_error_memory_lesson_with_local_ai = original_service
        action.apply_corrected_lesson_to_work_windows = original_apply
        action._show_success = original_success
        action._show_copyable_error = original_error
        deadline = time.monotonic() + 2.0
        while action._ACTIVE_JOBS and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.005)
        require(not action._ACTIVE_JOBS, "Background job registry was not cleaned up")
        for tab in tabs:
            tab.close()
            tab.deleteLater()
        app.processEvents()

    print("REAL_QT_CORRECT_WITH_AI_BUTTON_READY_BEFORE_SUCCESS_NOTICE: PASS")
    print("REAL_QT_CORRECT_WITH_AI_BUTTON_READY_BEFORE_FAILURE_NOTICE: PASS")
    print("REAL_QT_CORRECT_WITH_AI_TERMINAL_JOB_CLEANUP: PASS")


def main() -> int:
    global PROJECT_ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(PROJECT_ROOT))
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    PROJECT_ROOT = Path(args.root).resolve()
    validate_static_contract()
    if args.static_only:
        print("REAL_QT_CORRECT_WITH_AI_BUTTON_READY_RUNTIME: NOT_CLAIMED")
    else:
        validate_real_qt_runtime()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
