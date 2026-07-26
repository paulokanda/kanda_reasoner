"""Validate Qt-native bounded Heuristic correction with a real event-loop heartbeat."""
from __future__ import annotations

import argparse
import ast
import os
import time
from pathlib import Path

__all__ = []

FEATURE_ID = "architecture-review-workbench-heuristic-correction-qthread-bounded-runtime-v2"
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
GUI = PKG / "workbench_stage_correction_gui.py"
SERVICE = PKG / "workbench_stage_correction_service.py"
WORKER = PKG / "workbench_heuristic_correction_qt_worker.py"
CONTROLLER = PKG / "workbench_heuristic_correction_qt_controller.py"
SEARCH = PKG / "workbench_heuristic_feedback_search.py"
TOUCHED = (GUI, SERVICE, WORKER, CONTROLLER, SEARCH, Path(__file__).resolve())


def run_validation(*, static_only: bool = False) -> None:
    texts = {path.name: path.read_text(encoding="utf-8") for path in TOUCHED}
    _validate_qthread_signal_contract(texts)
    _validate_bounded_correction_path(texts)
    _validate_cancel_timeout_late_result_contract(texts)
    _validate_fail_closed_contract(texts)
    _validate_sizes()
    print("HEURISTIC_QTHREAD_SIGNAL_WORKER: PASS")
    print("HEURISTIC_CORRECTION_GIT_REQUERY_BOUNDED_OUT: PASS")
    print("HEURISTIC_CANCEL_TIMEOUT_LATE_RESULT_DISCARD: PASS")
    print("HEURISTIC_NO_SYNTHETIC_PASS_OR_FORCE_ENABLE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    if static_only:
        print("REAL_QT_WIDGET_HEARTBEAT: SKIPPED_STATIC_ONLY")
    else:
        _validate_real_widget_heartbeat()
        print("REAL_QT_WIDGET_HEARTBEAT: PASS")
    print("WORKBENCH_HEURISTIC_QTHREAD_BOUNDED_RUNTIME: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _validate_qthread_signal_contract(texts: dict[str, str]) -> None:
    worker = texts[WORKER.name]
    controller = texts[CONTROLLER.name]
    gui = texts[GUI.name]
    assert "class WorkbenchHeuristicCorrectionWorker(QObject)" in worker
    assert "result_ready = Signal(object)" in worker
    assert "finished = Signal()" in worker
    assert "worker.moveToThread(thread)" in controller
    assert "thread.started.connect(worker.run)" in controller
    assert "worker.result_ready.connect(receiver.on_result)" in controller
    assert "worker.finished.connect(thread.quit)" in controller
    assert "start_heuristic_correction(" in gui
    heuristic = _function(ast.parse(gui), "_run_heuristic")
    names = _call_names(heuristic)
    assert "Thread" not in names
    assert "build_heuristic_workbench_correction_candidate" not in names
    assert "QTimer" not in names


def _validate_bounded_correction_path(texts: dict[str, str]) -> None:
    service = texts[SERVICE.name]
    search = texts[SEARCH.name]

    service_tree = ast.parse(service)
    service_function = _function(service_tree, "build_heuristic_workbench_correction_candidate")
    service_calls = {_call_name(node) for node in ast.walk(service_function) if isinstance(node, ast.Call)}
    assert "search_feedback_aware_heuristic_correction" in service_calls

    search_tree = ast.parse(search)
    search_function = _function(search_tree, "search_feedback_aware_heuristic_correction")
    calls = [node for node in ast.walk(search_function) if isinstance(node, ast.Call)]
    build_calls = [node for node in calls if _call_name(node) == "build_split_plan"]
    assert build_calls, "BUILD_SPLIT_PLAN_CALL_MISSING"
    keywords = {item.arg: item.value for item in build_calls[0].keywords}
    assert "source_path" in keywords
    assert isinstance(keywords["source_path"], ast.Constant)
    assert keywords["source_path"].value is None
    assert "preferred_strategy" in keywords
    assert "context.blockers" in search
    assert "ast_static_only_no_git_requery" in service
    assert "progress_callback" in service


def _validate_cancel_timeout_late_result_contract(texts: dict[str, str]) -> None:
    controller = texts[CONTROLLER.name]
    gui = texts[GUI.name]
    assert "_HEURISTIC_TIMEOUT_MS = 30_000" in controller
    assert 'job["accept_result"] = False' in controller
    assert "thread.requestInterruption()" in controller
    assert "result_delivered" in controller
    assert "thread_finished" in controller
    assert "_cleanup_if_terminal" in controller
    assert "Cancel Heuristic Wait" in gui
    assert "cancel_heuristic_correction(" in gui
    assert 'for key in ("local_ai", "web_copy", "web_receive")' in gui


def _validate_fail_closed_contract(texts: dict[str, str]) -> None:
    joined = "\n".join(texts[name] for name in (GUI.name, SERVICE.name, WORKER.name, CONTROLLER.name))
    assert "setEnabled(True)" not in joined
    assert "No PASS was synthesized" in joined
    assert "No downstream gate will open" in joined
    assert "deterministic rerun" in joined


def _validate_sizes() -> None:
    for path in TOUCHED:
        count = len(path.read_text(encoding="utf-8").splitlines())
        assert count <= 500, f"SIZE_POLICY:{path.name}:{count}"


def _validate_real_widget_heartbeat() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from types import SimpleNamespace

    from PySide6.QtCore import QEventLoop, QTimer
    from PySide6.QtWidgets import QApplication, QLineEdit, QWidget

    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.docstring_planner import (
        build_docstring_proposals,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_bounded_refinement import (
        attach_docstring_proposals_to_plan,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import PlannerSettings
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
        PLANNER_VERSION_HEURISTIC,
        initialize_planner_version_state,
        select_planner_version,
        store_heuristic_version,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui import (
        build_large_file_refactor_workbench_page,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_snapshot_bridge import (
        load_latest_snapshot_into_workbench,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_gui import (
        sync_workbench_stage_correction_controls,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_service import (
        HeuristicWorkbenchCorrectionCandidate,
    )
    import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_heuristic_correction_qt_worker as worker_module

    app = QApplication.instance() or QApplication([])
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    assert target.is_file(), "CONTROLLED_RUNTIME_TARGET_MISSING"

    class TestWindow(QWidget):
        pass

    window = TestWindow()
    window._root_path_edit = QLineEdit(str(ROOT), window)
    page = build_large_file_refactor_workbench_page(window)
    page.setParent(window)
    initialize_planner_version_state(window)

    report = analyze_python_file(target)
    plan = build_split_plan(report, PlannerSettings(), source_path=None)
    proposals = build_docstring_proposals(report, plan)
    plan = attach_docstring_proposals_to_plan(plan, proposals)
    window._large_file_refactor_last_analysis = report
    window._large_file_refactor_planner_candidates = [SimpleNamespace(path=str(target))]
    store_heuristic_version(window, plan, proposals)
    select_planner_version(window, PLANNER_VERSION_HEURISTIC)
    intake, message = load_latest_snapshot_into_workbench(window, str(ROOT))
    assert intake is not None and intake.ready_for_real_preview, message
    assert intake.planner_candidate_verified, "RUNTIME_FIXTURE_TARGET_NOT_IN_WARNING_QUEUE"
    window._large_file_refactor_workbench_intake = intake

    window._large_file_refactor_workbench_real_preview = SimpleNamespace(
        status="blocked",
        blockers=("RUNTIME_HEARTBEAT_TEST_BLOCKER",),
        warnings=(),
        target_file=str(target),
    )
    window._large_file_refactor_workbench_real_preview_output.setPlainText(
        "BLOCKED\nRUNTIME_HEARTBEAT_TEST_BLOCKER"
    )
    sync_workbench_stage_correction_controls(
        window,
        lambda current: current._root_path_edit.text(),
    )
    button = window._large_file_refactor_workbench_correction_controls["REAL_PREVIEW"]["heuristic"]
    assert button.isEnabled(), "REAL_HEURISTIC_BUTTON_NOT_ENABLED"

    original_builder = worker_module.build_heuristic_workbench_correction_candidate

    def slow_builder(*, plan, context, progress_callback=None):
        if progress_callback is not None:
            progress_callback("RUNTIME_SLEEP_PHASE")
        time.sleep(0.8)
        return HeuristicWorkbenchCorrectionCandidate(
            ok=False,
            message="Synthetic runtime heartbeat candidate finished.",
        )

    worker_module.build_heuristic_workbench_correction_candidate = slow_builder
    beats = {"count": 0}
    heartbeat = QTimer()
    heartbeat.setInterval(25)
    heartbeat.timeout.connect(lambda: beats.__setitem__("count", beats["count"] + 1))
    heartbeat.start()
    try:
        started = time.monotonic()
        button.click()
        click_elapsed = time.monotonic() - started
        assert click_elapsed < 0.35, f"HEURISTIC_CLICK_BLOCKED_GUI:{click_elapsed:.3f}"

        loop = QEventLoop()
        QTimer.singleShot(1400, loop.quit)
        loop.exec()
        assert beats["count"] >= 15, f"GUI_HEARTBEAT_STARVED:{beats['count']}"
        assert not bool(getattr(window, "_workbench_stage_heuristic_correction_running", False))
    finally:
        heartbeat.stop()
        worker_module.build_heuristic_workbench_correction_candidate = original_builder
        window.close()
        page.close()
        app.processEvents()


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError("MISSING_FUNCTION:" + name)


def _call_names(function: ast.FunctionDef) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(function):
        if isinstance(node, ast.Call):
            names.add(_call_name(node))
    return names


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    run_validation(static_only=args.static_only)
