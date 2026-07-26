# project-path: tools/validate_error_memory_correct_with_ai_stability_v1.py
"""Validate the audited Error Memory Correct with AI stability correction."""

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

FEATURE_ID = "error-memory-correct-with-ai-stability-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

TOUCHED = (
    "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_worker.py",
    "tools/validate_error_memory_correct_with_ai_stability_v1.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def class_node(tree: ast.AST, name: str) -> ast.ClassDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise AssertionError("Class not found: " + name)


def validate_compile_and_size() -> None:
    for relative_path in TOUCHED:
        path = PROJECT_ROOT / relative_path
        require(path.is_file(), "Missing touched file: " + relative_path)
        py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(line_count <= 500, relative_path + " exceeds 500 physical lines")
    print("TOUCHED_PYTHON_COMPILE: PASS")
    print("TOUCHED_MODULES_UNDER_500_LINES: PASS")


def validate_show_event_descriptor() -> None:
    text = read("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
    tree = ast.parse(text)
    cls = class_node(tree, "ErrorMemoryTab")
    show_event = next(
        node
        for node in cls.body
        if isinstance(node, ast.FunctionDef) and node.name == "showEvent"
    )
    require(not show_event.decorator_list, "ErrorMemoryTab.showEvent still has decorators")
    source = ast.get_source_segment(text, show_event) or ""
    require("super().showEvent(event)" in source, "showEvent no longer delegates to QWidget")
    require(
        "_error_memory_ai_correction_generation = 0" in text,
        "AI correction generation state is not initialized",
    )
    print("ERROR_MEMORY_SHOW_EVENT_CALLABLE: PASS")
    print("ERROR_MEMORY_TAB_LIFECYCLE_PRESERVED: PASS")


def validate_background_worker_contract() -> None:
    action_text = read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    worker_text = read("kanda_reasoner_app/error_memory_gui/_ai_correction_worker.py")
    worker_tree = ast.parse(worker_text)

    required_action = (
        "QThread()",
        "worker.moveToThread(thread)",
        "thread.started.connect(worker.run)",
        "worker.finished.connect(thread.quit)",
        "worker.finished.connect(worker.deleteLater)",
        "thread.finished.connect(receiver.on_thread_finished)",
        "thread.finished.connect(thread.deleteLater)",
        "Error Memory AI correction apply failed",
        "Error Memory AI correction failed to start",
    )
    for marker in required_action:
        require(marker in action_text, "Background-thread contract missing: " + marker)
    require(
        "correct_error_memory_lesson_with_local_ai" not in action_text,
        "GUI action still calls the synchronous AI service directly",
    )
    require(
        "correct_error_memory_lesson_with_local_ai" in worker_text,
        "Background worker does not own the synchronous service call",
    )

    worker_cls = class_node(worker_tree, "ErrorMemoryAICorrectionWorker")
    run_method = next(
        node
        for node in worker_cls.body
        if isinstance(node, ast.FunctionDef) and node.name == "run"
    )
    run_source = ast.get_source_segment(worker_text, run_method) or ""
    require("except Exception as exc" in run_source, "Worker lacks an exception boundary")
    require(
        "finally:" in run_source and "self.finished.emit()" in run_source,
        "Worker does not always emit finished",
    )
    print("CORRECT_WITH_AI_BACKGROUND_QTHREAD: PASS")
    print("CORRECT_WITH_AI_WORKER_EXCEPTION_BOUNDARY: PASS")
    print("CORRECT_WITH_AI_GUI_APPLY_EXCEPTION_BOUNDARY: PASS")
    print("CORRECT_WITH_AI_THREAD_START_ROLLBACK: PASS")
    print("CORRECT_WITH_AI_THREAD_CLEANUP: PASS")


def validate_preview_only_contract() -> None:
    action_text = read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    forbidden = (
        "save_corrected_selected_draft",
        "selected_saved_draft_lesson_id",
        "consume_duplicate_correction_candidate",
        "save_lesson(",
        "delete_lesson(",
        "set_selected_lesson_status",
    )
    for marker in forbidden:
        require(marker not in action_text, "Correct with AI still owns mutation: " + marker)
    required = (
        "apply_corrected_lesson_to_work_windows",
        "The corrected lesson was loaded as a preview only.",
        "did not save, delete, activate, supersede, or memorize any lesson",
    )
    for marker in required:
        require(marker in action_text, "Preview-only contract missing: " + marker)
    print("CORRECT_WITH_AI_PREVIEW_ONLY: PASS")
    print("CORRECT_WITH_AI_NO_AUTOMATIC_SAVE: PASS")
    print("CORRECT_WITH_AI_NO_DESTRUCTIVE_DUPLICATE_CLEANUP: PASS")
    print("CORRECT_WITH_AI_NO_AUTOMATIC_MEMORIZE: PASS")


def validate_stale_and_single_flight_contract() -> None:
    text = read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    required = (
        "_same_source_text",
        "The stale AI result was discarded.",
        "generation",
        "A local AI correction is already running",
    )
    for marker in required:
        require(marker in text, "Stale-result or single-flight guard missing: " + marker)
    print("CORRECT_WITH_AI_STALE_RESULT_GUARD: PASS")
    print("CORRECT_WITH_AI_SINGLE_FLIGHT: PASS")


def validate_button_contract() -> None:
    tab_text = read("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
    action_text = read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    require(
        "self.correct_with_ai_button = QPushButton('Correct with AI')" in tab_text,
        "Correct with AI button is missing",
    )
    require(
        "self.correct_with_ai_button.clicked.connect(self._correct_with_ai_from_error_memory_tab)"
        in tab_text,
        "Correct with AI button is not connected",
    )
    require(
        "background worker and load the result as preview only" in tab_text,
        "Correct with AI tooltip does not disclose preview-only behavior",
    )
    require(
        "run_error_memory_ai_correction_from_tab" in action_text,
        "Tab correction entry point is missing",
    )
    require(
        "run_error_memory_ai_correction_from_header" in action_text,
        "Header correction entry point is missing",
    )
    print("CORRECT_WITH_AI_BUTTON_WIRING: PASS")
    print("CORRECT_WITH_AI_TOOLTIP_CONTRACT: PASS")


def validate_audited_original_risk() -> None:
    local_ai_text = read("kanda_reasoner_app/reasoner_engine/v10_qwen_ai_models.py")
    action_text = read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    require("TIMEOUT = 600" in local_ai_text, "Audited synchronous request timeout changed")
    require(
        "QApplication.setOverrideCursor" not in action_text,
        "GUI-thread wait-cursor blocking pattern remains",
    )
    print("AUDITED_OLLAMA_TIMEOUT_600_SECONDS: PASS")
    print("GUI_THREAD_BLOCKING_CALL_REMOVED: PASS")


def _wait_for(
    app: Any,
    predicate: Callable[[], bool],
    *,
    timeout_seconds: float = 4.0,
) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.005)
    app.processEvents()
    return bool(predicate())


def validate_real_qt_worker_runtime() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    from PySide6.QtWidgets import QApplication, QPlainTextEdit, QPushButton, QWidget

    from kanda_reasoner_app.error_memory_gui import _ai_correction_action as action
    from kanda_reasoner_app.error_memory_gui import _ai_correction_worker as worker_module

    app = QApplication.instance() or QApplication([])
    main_thread_id = threading.get_ident()

    original_service = worker_module.correct_error_memory_lesson_with_local_ai
    original_warning = action._show_standard_warning
    original_error = action._show_copyable_error
    original_success = action._show_success
    original_apply = action.apply_corrected_lesson_to_work_windows

    notices: list[tuple[str, str, str]] = []
    service_thread_ids: list[int] = []

    class FakeTab(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.raw_error_edit = QPlainTextEdit(self)
            self.received_preview_edit = QPlainTextEdit(self)
            self.correct_with_ai_button = QPushButton("Correct with AI", self)
            self._project_root = PROJECT_ROOT
            self._error_memory_ai_correction_generation = 0
            self._last_received_lesson = None
            self._selected_lesson_id = ""

    def warning(_parent: Any, title: str, message: str) -> None:
        notices.append(("warning", title, message))

    def error(
        _parent: Any,
        *,
        title: str,
        message: str,
        detail_text: str = "",
    ) -> None:
        notices.append(("error", title, message + "\n" + detail_text))

    def success(_tab: Any, title: str, message: str) -> None:
        notices.append(("success", title, message))

    def make_result(lesson_id: str) -> Any:
        lesson = {
            "lesson_id": lesson_id,
            "status": "draft",
            "symptom": "audited runtime probe",
        }
        block = SimpleNamespace(
            lesson=lesson,
            formatted_text=(
                "KANDA_ERROR_LESSON_JSON_BEGIN\n"
                + '{"lesson_id":"' + lesson_id + '","status":"draft"}'
                + "\nKANDA_ERROR_LESSON_JSON_END"
            ),
        )
        return SimpleNamespace(
            ok=True,
            lesson_block=block,
            message="Audited fake correction completed.",
            raw_response="",
        )

    def make_tab(raw: str, editor: str) -> FakeTab:
        tab = FakeTab()
        tab.raw_error_edit.setPlainText(raw)
        tab.received_preview_edit.setPlainText(editor)
        return tab

    action._show_standard_warning = warning
    action._show_copyable_error = error
    action._show_success = success

    tabs: list[FakeTab] = []
    try:
        success_tab = make_tab("success intake", "success editor")
        tabs.append(success_tab)

        service_started = threading.Event()
        service_release = threading.Event()

        def gated_success(**_kwargs: Any) -> Any:
            service_thread_ids.append(threading.get_ident())
            service_started.set()
            if not service_release.wait(timeout=2.0):
                raise RuntimeError("audited service release timeout")
            return make_result("lesson-audited-success-v1")

        worker_module.correct_error_memory_lesson_with_local_ai = gated_success
        started = time.monotonic()
        action.run_error_memory_ai_correction_from_tab(success_tab)
        returned_after = time.monotonic() - started

        require(returned_after < 0.5, "Correct with AI still blocks the GUI caller")
        require(
            not success_tab.correct_with_ai_button.isEnabled(),
            "Correct with AI button was not disabled while running",
        )
        require(service_started.wait(timeout=1.0), "Background service did not start")
        service_release.set()
        require(
            _wait_for(app, lambda: action._job_for(success_tab) is None),
            "Successful background job did not finish",
        )
        require(
            success_tab.correct_with_ai_button.isEnabled(),
            "Correct with AI button was not restored after success",
        )
        require(
            success_tab._selected_lesson_id == "lesson-audited-success-v1",
            "Successful result was not applied to the preview",
        )
        require(
            any(
                kind == "success" and "preview only" in message
                for kind, _title, message in notices
            ),
            "Preview-only success notice was not emitted",
        )
        require(
            service_thread_ids and service_thread_ids[-1] != main_thread_id,
            "Local AI service still ran on the GUI thread",
        )

        notices.clear()
        stale_tab = make_tab("stale intake", "stale editor")
        tabs.append(stale_tab)

        def stale_success(**_kwargs: Any) -> Any:
            time.sleep(0.12)
            return make_result("lesson-audited-stale-v1")

        worker_module.correct_error_memory_lesson_with_local_ai = stale_success
        action.run_error_memory_ai_correction_from_tab(stale_tab)
        stale_tab.raw_error_edit.setPlainText("user changed intake")
        require(
            _wait_for(app, lambda: action._job_for(stale_tab) is None),
            "Stale-result background job did not finish",
        )
        require(
            stale_tab._selected_lesson_id == "",
            "Stale AI result was incorrectly applied",
        )
        require(
            any(
                kind == "warning" and "stale AI result was discarded" in message
                for kind, _title, message in notices
            ),
            "Stale-result warning was not emitted",
        )

        notices.clear()
        failure_tab = make_tab("failure intake", "failure editor")
        tabs.append(failure_tab)

        def worker_failure(**_kwargs: Any) -> Any:
            time.sleep(0.03)
            raise RuntimeError("audited worker exception probe")

        worker_module.correct_error_memory_lesson_with_local_ai = worker_failure
        action.run_error_memory_ai_correction_from_tab(failure_tab)
        require(
            _wait_for(app, lambda: action._job_for(failure_tab) is None),
            "Failed background job did not clean up",
        )
        require(
            failure_tab.correct_with_ai_button.isEnabled(),
            "Button was not restored after worker failure",
        )
        require(
            any(
                kind == "error" and "audited worker exception probe" in message
                for kind, _title, message in notices
            ),
            "Worker exception was not surfaced through the error boundary",
        )

        notices.clear()
        apply_failure_tab = make_tab("apply failure intake", "apply failure editor")
        tabs.append(apply_failure_tab)

        def apply_success(**_kwargs: Any) -> Any:
            time.sleep(0.05)
            return make_result("lesson-audited-apply-failure-v1")

        worker_module.correct_error_memory_lesson_with_local_ai = apply_success

        def fail_apply(_tab: Any, _block: Any) -> None:
            raise RuntimeError("audited preview apply exception")

        action.apply_corrected_lesson_to_work_windows = fail_apply
        action.run_error_memory_ai_correction_from_tab(apply_failure_tab)
        require(
            _wait_for(app, lambda: action._job_for(apply_failure_tab) is None),
            "Apply-failure background job did not clean up",
        )
        require(
            apply_failure_tab.correct_with_ai_button.isEnabled(),
            "Button was not restored after preview apply failure",
        )
        require(
            any(
                kind == "error" and "audited preview apply exception" in message
                for kind, _title, message in notices
            ),
            "Preview apply exception was not contained",
        )
    finally:
        worker_module.correct_error_memory_lesson_with_local_ai = original_service
        action._show_standard_warning = original_warning
        action._show_copyable_error = original_error
        action._show_success = original_success
        action.apply_corrected_lesson_to_work_windows = original_apply

        deadline = time.monotonic() + 2.0
        while action._ACTIVE_JOBS and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.005)
        require(not action._ACTIVE_JOBS, "Background job registry was not cleaned up")

        for tab in tabs:
            tab.close()
            tab.deleteLater()
        app.processEvents()

    print("REAL_QT_CORRECT_WITH_AI_NON_BLOCKING: PASS")
    print("REAL_QT_CORRECT_WITH_AI_PREVIEW_APPLY: PASS")
    print("REAL_QT_CORRECT_WITH_AI_STALE_RESULT_REJECTED: PASS")
    print("REAL_QT_CORRECT_WITH_AI_WORKER_FAILURE_RECOVERED: PASS")
    print("REAL_QT_CORRECT_WITH_AI_APPLY_FAILURE_RECOVERED: PASS")
    print("REAL_QT_CORRECT_WITH_AI_BUTTON_RESTORED: PASS")
    print("REAL_QT_CORRECT_WITH_AI_JOB_CLEANUP: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--static-only",
        action="store_true",
        help="Run source and audit gates without the real PySide6 thread probe.",
    )
    arguments = parser.parse_args()

    validate_compile_and_size()
    validate_show_event_descriptor()
    validate_background_worker_contract()
    validate_preview_only_contract()
    validate_stale_and_single_flight_contract()
    validate_button_contract()
    validate_audited_original_risk()
    if arguments.static_only:
        print("REAL_QT_CORRECT_WITH_AI_RUNTIME: NOT_CLAIMED")
    else:
        validate_real_qt_worker_runtime()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
