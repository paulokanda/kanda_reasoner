# project-path: tools/validate_engineering_diagnostics_history_qthread_freeze_repair_v2.py
"""Focused structural validator for Engineering Diagnostics history QThread repair."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import py_compile

FEATURE_ID = (
    "kanda-reasoner-engineering-diagnostics-history-qthread-freeze-repair-v2"
)

TOUCHED = (
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/history_async.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/history_qt_worker.py",
    "tools/validate_engineering_diagnostics_history_qthread_freeze_repair_v2.py",
    "tools/validate_engineering_diagnostics_history_qthread_real_qt_v2.py",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise RuntimeError("FUNCTION_NOT_FOUND:" + name)


def _call_names(function: ast.FunctionDef) -> set[str]:
    result: set[str] = set()
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        current = node.func
        if isinstance(current, ast.Name):
            result.add(current.id)
        if isinstance(current, ast.Attribute):
            result.add(current.attr)
    return result


def validate(project_root: Path) -> None:
    """Validate the exact repair shape without executing the real Qt fixture."""
    paths = {relative: project_root / relative for relative in TOUCHED}
    for relative, path in paths.items():
        _require(path.is_file(), "TOUCHED_FILE_MISSING:" + relative)
        raw = path.read_bytes()
        raw.decode("ascii")
        _require(
            len(raw.decode("utf-8").splitlines()) <= 500,
            "MODULE_SIZE_LIMIT:" + relative,
        )
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)

    tab_text = paths[TOUCHED[0]].read_text(encoding="utf-8")
    runtime_text = paths[TOUCHED[1]].read_text(encoding="utf-8")
    worker_text = paths[TOUCHED[2]].read_text(encoding="utf-8")

    _require(
        "active_controller.load_run_view(" not in tab_text,
        "GUI_THREAD_DIRECT_RUN_VIEW_LOAD_REMAINS",
    )
    _require(
        "bind_async_history(" in tab_text,
        "ASYNC_HISTORY_BINDING_MISSING",
    )
    _require(
        "history_actions.cancel()" in tab_text,
        "PROJECT_SWITCH_HISTORY_CANCEL_MISSING",
    )
    _require(
        "history_actions.close()" in tab_text,
        "PANEL_DESTROY_HISTORY_CLOSE_MISSING",
    )

    _require(
        "class _EngineeringDiagnosticsHistoryRuntime(QObject)" in runtime_text,
        "QT_RUNTIME_OBJECT_MISSING",
    )
    _require("thread = QThread()" in runtime_text, "QTHREAD_OWNER_MISSING")
    _require(
        "worker.moveToThread(thread)" in runtime_text,
        "WORKER_MOVE_TO_THREAD_MISSING",
    )
    _require(
        "thread.started.connect(worker.run)" in runtime_text,
        "QTHREAD_START_SIGNAL_MISSING",
    )
    _require(
        "worker.result_ready.connect(self._on_result)" in runtime_text,
        "GUI_RECEIVER_SIGNAL_MISSING",
    )
    _require(
        "worker.finished.connect(thread.quit)" in runtime_text,
        "QTHREAD_QUIT_MISSING",
    )
    _require(
        "thread.finished.connect(self._on_thread_finished)" in runtime_text,
        "GUI_THREAD_FINISH_RECEIVER_MISSING",
    )
    _require(
        "worker.finished.connect(worker.deleteLater)" in runtime_text,
        "WORKER_DELETE_LATER_MISSING",
    )
    _require(
        "_HISTORY_TIMEOUT_MS = 30_000" in runtime_text,
        "BOUNDED_HISTORY_TIMEOUT_MISSING",
    )
    _require(
        "thread.requestInterruption()" in runtime_text,
        "INTERRUPTION_REQUEST_MISSING",
    )
    _require(
        "outcome.generation != self._generation" in runtime_text,
        "STALE_GENERATION_REJECTION_MISSING",
    )
    _require(
        "outcome.project_root != request.project_root" in runtime_text,
        "STALE_PROJECT_REJECTION_MISSING",
    )
    _require(
        "outcome.run_id != request.run_id" in runtime_text,
        "STALE_RUN_REJECTION_MISSING",
    )
    _require(
        "ThreadPoolExecutor" not in runtime_text,
        "DEPRECATED_HISTORY_THREAD_POOL_PATTERN_PRESENT",
    )

    worker_tree = ast.parse(worker_text)
    run_function = _function(worker_tree, "run")
    calls = _call_names(run_function)
    _require("load_run_view" in calls, "WORKER_RUN_VIEW_CALL_MISSING")
    _require(
        "class EngineeringDiagnosticsHistoryWorker(QObject)" in worker_text,
        "QT_WORKER_OBJECT_MISSING",
    )
    _require("result_ready = Signal(object)" in worker_text, "WORKER_SIGNAL_MISSING")
    _require(
        "QThread.currentThread()" in worker_text,
        "WORKER_THREAD_IDENTITY_CHECK_MISSING",
    )

    print("ENGINEERING_DIAGNOSTICS_DIRECT_HISTORY_GUI_BLOCK: REMOVED")
    print("ENGINEERING_DIAGNOSTICS_QTHREAD_SIGNAL_WORKER: PASS")
    print("ENGINEERING_DIAGNOSTICS_SERIAL_HISTORY_LANE: PASS")
    print("ENGINEERING_DIAGNOSTICS_STALE_GENERATION_REJECTION: PASS")
    print("ENGINEERING_DIAGNOSTICS_STALE_PROJECT_REJECTION: PASS")
    print("ENGINEERING_DIAGNOSTICS_STALE_RUN_REJECTION: PASS")
    print("ENGINEERING_DIAGNOSTICS_HISTORY_TIMEOUT_BOUND: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("ASCII_SOURCE_CONTRACT: PASS")
    print("PYTHON_COMPILE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    validate(project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
