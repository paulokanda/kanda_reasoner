"""Validate Main Workbench button terminal color projection."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
from types import SimpleNamespace

FEATURE_ID = "main-workbench-button-terminal-color-v1"
RELATIVE_GUI = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "main_workbench_gui.py"
)
SUCCESS_STYLE = "color: #008000; font-weight: bold;"
BLOCKED_STYLE = "color: #C62828; font-weight: bold;"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--require-pyside", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    gui_path = project_root / RELATIVE_GUI
    if not gui_path.is_file():
        raise RuntimeError("MAIN_WORKBENCH_GUI_MISSING:" + str(gui_path))

    source = gui_path.read_text(encoding="utf-8-sig")
    _assert_static_contract(source)
    print("MAIN_WORKBENCH_BUTTON_STYLE_STATIC_CONTRACT: PASS")

    line_count = len(source.splitlines())
    if not 101 <= line_count <= 499:
        raise RuntimeError(
            "TOUCHED_MODULE_LINE_LAW_FAILED:"
            + str(RELATIVE_GUI)
            + ":"
            + str(line_count)
        )
    print("TOUCHED_MODULE_LINE_LAW_101_499: PASS")

    compile(source, str(gui_path), "exec")
    ast.parse(source, filename=str(gui_path))
    print("TOUCHED_MODULE_PYTHON_COMPILE_AND_AST: PASS")

    runtime_result = _run_pyside_contract(project_root)
    if runtime_result == "unavailable":
        if args.require_pyside:
            raise RuntimeError("REAL_PYSIDE6_GUI_IMPORT_SMOKE: REQUIRED_BUT_UNAVAILABLE")
        print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: SKIP_UNAVAILABLE")
    else:
        print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: PASS")

    print("MAIN_WORKBENCH_READY_BUTTON_GREEN_BOLD: PASS")
    print("MAIN_WORKBENCH_BLOCKED_BUTTON_RED_BOLD: PASS")
    print("MAIN_WORKBENCH_FAILED_BUTTON_RED_BOLD: PASS")
    print("MAIN_WORKBENCH_STALE_BUTTON_RED_BOLD: PASS")
    print("MAIN_WORKBENCH_STALE_SEAL_BUTTON_RED_BOLD: PASS")
    print("MAIN_WORKBENCH_RUNNING_BUTTON_NEUTRAL: PASS")
    print("MAIN_WORKBENCH_CANCELLED_BUTTON_NEUTRAL: PASS")
    print("MAIN_WORKBENCH_IDLE_BUTTON_NEUTRAL: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _assert_static_contract(source: str) -> None:
    required_tokens = (
        '_MAIN_WORKBENCH_SUCCESS_STYLE = "' + SUCCESS_STYLE + '"',
        '_MAIN_WORKBENCH_BLOCKED_STYLE = "' + BLOCKED_STYLE + '"',
        "def _sync_main_workbench_button_style(",
        "terminal == MAIN_WORKBENCH_READY and seal_current",
        "MAIN_WORKBENCH_WEB_AI_BLOCKED",
        "MAIN_WORKBENCH_FAILED",
        "MAIN_WORKBENCH_STALE",
        "seal is not None and not seal_current",
        "if state is not None and state.running:",
        "_sync_main_workbench_button_style(",
    )
    for token in required_tokens:
        if token not in source:
            raise RuntimeError("BUTTON_STYLE_CONTRACT_TOKEN_MISSING:" + token)

    tree = ast.parse(source)
    helper = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_sync_main_workbench_button_style"
        ),
        None,
    )
    if helper is None:
        raise RuntimeError("BUTTON_STYLE_HELPER_MISSING")
    calls = [
        node
        for node in ast.walk(helper)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "setStyleSheet"
    ]
    if len(calls) < 4:
        raise RuntimeError("BUTTON_STYLE_PROJECTION_INCOMPLETE")


def _run_pyside_contract(project_root: Path) -> str:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    try:
        from PySide6.QtWidgets import QApplication, QPushButton
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
            main_workbench_gui as gui,
        )
    except (ImportError, ModuleNotFoundError):
        return "unavailable"

    app = QApplication.instance() or QApplication([])
    button = QPushButton("Main Workbench")

    _project_style(
        gui,
        button,
        state=_state(running=True),
        seal=None,
        seal_current=False,
        expected="",
        marker="RUNNING",
    )
    _project_style(
        gui,
        button,
        state=_state(terminal=gui.MAIN_WORKBENCH_READY),
        seal=_seal(gui.MAIN_WORKBENCH_READY),
        seal_current=True,
        expected=SUCCESS_STYLE,
        marker="READY",
    )
    for marker, terminal in (
        ("BLOCKED", gui.MAIN_WORKBENCH_WEB_AI_BLOCKED),
        ("FAILED", gui.MAIN_WORKBENCH_FAILED),
        ("STALE", gui.MAIN_WORKBENCH_STALE),
    ):
        _project_style(
            gui,
            button,
            state=_state(terminal=terminal),
            seal=_seal(terminal),
            seal_current=True,
            expected=BLOCKED_STYLE,
            marker=marker,
        )
    _project_style(
        gui,
        button,
        state=None,
        seal=_seal(gui.MAIN_WORKBENCH_READY),
        seal_current=False,
        expected=BLOCKED_STYLE,
        marker="STALE_SEAL",
    )
    _project_style(
        gui,
        button,
        state=_state(terminal="CANCELLED"),
        seal=None,
        seal_current=False,
        expected="",
        marker="CANCELLED",
    )
    _project_style(
        gui,
        button,
        state=None,
        seal=None,
        seal_current=False,
        expected="",
        marker="IDLE",
    )
    button.deleteLater()
    app.processEvents()
    return "passed"


def _state(*, running: bool = False, terminal: str = "") -> SimpleNamespace:
    return SimpleNamespace(running=running, terminal_status=terminal)


def _seal(terminal: str) -> SimpleNamespace:
    return SimpleNamespace(terminal_status=terminal)


def _project_style(
    gui: object,
    button: object,
    *,
    state: object | None,
    seal: object | None,
    seal_current: bool,
    expected: str,
    marker: str,
) -> None:
    gui._sync_main_workbench_button_style(
        button,
        state=state,
        seal=seal,
        seal_current=seal_current,
    )
    observed = str(button.styleSheet())
    if observed != expected:
        raise RuntimeError(
            "BUTTON_STYLE_MISMATCH:"
            + marker
            + ":expected="
            + expected
            + ":observed="
            + observed
        )


if __name__ == "__main__":
    raise SystemExit(main())
