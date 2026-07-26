# project-path: tools/validate_workbench_heuristic_correction_async_gui_v1.py
"""Validate non-blocking Heuristic Correction execution in Workbench GUI."""
from __future__ import annotations

import ast
from pathlib import Path

__all__ = []

FEATURE_ID = "architecture-review-workbench-heuristic-correction-async-gui-v1"
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
GUI = PKG / "workbench_stage_correction_gui.py"
SERVICE = PKG / "workbench_stage_correction_service.py"


def run_validation() -> None:
    gui_text = GUI.read_text(encoding="utf-8")
    service_text = SERVICE.read_text(encoding="utf-8")
    gui_tree = ast.parse(gui_text)
    service_tree = ast.parse(service_text)

    _validate_heavy_build_off_gui_thread(gui_tree, gui_text)
    _validate_candidate_build_apply_split(service_tree, service_text)
    _validate_gui_thread_apply(gui_text)
    _validate_running_state_and_controls(gui_text)
    _validate_timeout_escape(gui_text)
    _validate_fail_closed_contract(gui_text, service_text)
    _validate_sizes()

    print("HEURISTIC_HEAVY_BUILD_OFF_GUI_THREAD: PASS")
    print("HEURISTIC_CANDIDATE_BUILD_APPLY_SPLIT: PASS")
    print("HEURISTIC_GUI_APPLY_POLLED_ON_QT_TIMER: PASS")
    print("HEURISTIC_RUNNING_STATE_DISABLING: PASS")
    print("HEURISTIC_TIMEOUT_ESCAPE_ROUTE: PASS")
    print("LOCAL_AI_AND_WEB_AI_REMAIN_RECOVERY_ROUTES: PASS")
    print("HEURISTIC_ASYNC_DOES_NOT_FORCE_PASS: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("WORKBENCH_HEURISTIC_CORRECTION_ASYNC_GUI: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError("missing function: " + name)


def _call_names_excluding_nested(function: ast.FunctionDef) -> set[str]:
    names: set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if node is function:
                self.generic_visit(node)
            # nested functions are intentionally not traversed

        def visit_Lambda(self, node: ast.Lambda) -> None:
            return

        def visit_Call(self, node: ast.Call) -> None:
            func = node.func
            if isinstance(func, ast.Name):
                names.add(func.id)
            elif isinstance(func, ast.Attribute):
                names.add(func.attr)
            self.generic_visit(node)

    Visitor().visit(function)
    return names


def _validate_heavy_build_off_gui_thread(tree: ast.AST, text: str) -> None:
    function = _function(tree, "_run_heuristic")
    direct_calls = _call_names_excluding_nested(function)
    for forbidden in (
        "analyze_python_file",
        "build_split_plan",
        "build_docstring_proposals",
        "build_heuristic_workbench_correction_candidate",
        "load_latest_snapshot_into_workbench",
    ):
        assert forbidden not in direct_calls, "GUI_THREAD_HEAVY_CALL:" + forbidden
    assert 'name="kanda-workbench-stage-heuristic-correction"' in text
    assert "daemon=True" in text
    assert "target=worker" in text
    assert "build_heuristic_workbench_correction_candidate(" in text


def _validate_candidate_build_apply_split(tree: ast.AST, text: str) -> None:
    build = _function(tree, "build_heuristic_workbench_correction_candidate")
    apply = _function(tree, "apply_heuristic_workbench_correction")
    build_calls = {n.func.id if isinstance(n.func, ast.Name) else n.func.attr
                   for n in ast.walk(build) if isinstance(n, ast.Call)
                   and isinstance(n.func, (ast.Name, ast.Attribute))}
    apply_calls = {n.func.id if isinstance(n.func, ast.Name) else n.func.attr
                   for n in ast.walk(apply) if isinstance(n, ast.Call)
                   and isinstance(n.func, (ast.Name, ast.Attribute))}
    assert "analyze_python_file" in build_calls
    assert "build_split_plan" in build_calls
    assert "build_docstring_proposals" in build_calls
    assert "store_heuristic_version" not in build_calls
    assert "load_latest_snapshot_into_workbench" not in build_calls
    assert "store_heuristic_version" in apply_calls
    assert "load_latest_snapshot_into_workbench" in apply_calls
    assert "window._large_file_refactor_last_analysis = candidate.report" in text


def _validate_gui_thread_apply(text: str) -> None:
    assert "timer.timeout.connect(poll)" in text
    assert "candidate = result_queue.get_nowait()" in text
    assert "result = apply_heuristic_workbench_correction(window, context, candidate)" in text
    assert "thread.start()" in text
    assert "timer.start()" in text


def _validate_running_state_and_controls(text: str) -> None:
    assert "_workbench_stage_heuristic_correction_running" in text
    assert "correction_running = bool(heuristic_running or local_running)" in text
    assert "needed and not correction_running" in text
    assert "The interface remains responsive" in text


def _validate_timeout_escape(text: str) -> None:
    assert "_HEURISTIC_TIMEOUT_SECONDS = 180.0" in text
    assert "time.monotonic() - started_at >= _HEURISTIC_TIMEOUT_SECONDS" in text
    assert "_workbench_stage_heuristic_timeout_stages" in text
    assert "use Local AI or Web AI correction" in text
    assert 'for key in ("local_ai", "web_copy", "web_receive")' in text


def _validate_fail_closed_contract(gui_text: str, service_text: str) -> None:
    assert "setEnabled(True)" not in gui_text
    assert "setEnabled(True)" not in service_text
    assert "deterministic rerun" in gui_text
    assert "Sequential downstream evidence was invalidated intentionally." in service_text
    assert "run_heuristic_workbench_correction" not in gui_text


def _validate_sizes() -> None:
    for path in (GUI, SERVICE):
        lines = len(path.read_text(encoding="utf-8").splitlines())
        assert lines <= 500, f"SIZE_POLICY:{path.name}:{lines}"


if __name__ == "__main__":
    run_validation()
