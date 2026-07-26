"""Validate Planner-local child tabs and box-boundary preservation."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys

__all__ = [
    "main",
]

FEATURE_ID = "large-file-refactor-planner-child-tabs-v1"
MAX_PHYSICAL_LINES = 500
GUI_SHELL_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py"
)
LAYOUT_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "planner_inner_tabs_layout.py"
)
TEMPLATE_RELATIVE = Path("kanda_reasoner_app/templates/inner_tabs_template.py")


def _require(condition: bool, message: str) -> None:
    """Raise an assertion when one focused contract check fails."""
    if not condition:
        raise AssertionError(message)


def _read_source(path: Path) -> str:
    """Read, compile, and parse one Python source file."""
    _require(path.is_file(), "Required source file is missing: " + str(path))
    source = path.read_text(encoding="utf-8", errors="strict")
    compile(source, str(path), "exec")
    ast.parse(source, filename=str(path))
    _require(
        len(source.splitlines()) <= MAX_PHYSICAL_LINES,
        path.name + " exceeds 500 physical lines.",
    )
    return source


def _validate_static_contract(project_root: Path) -> None:
    """Validate child-tab composition and anti-contamination boundaries."""
    gui_source = _read_source(project_root / GUI_SHELL_RELATIVE)
    layout_source = _read_source(project_root / LAYOUT_RELATIVE)
    template_source = _read_source(project_root / TEMPLATE_RELATIVE)

    gui_required = (
        "from .planner_inner_tabs_layout import build_planner_inner_tabs",
        "inner_tabs = build_planner_inner_tabs(",
        "[candidate_section, settings_section, evidence_section]",
        "[plan_section, preview_section]",
        "_large_file_refactor_planner_inner_tab_stack",
        "_large_file_refactor_planner_inner_tab_buttons",
        "layout.addWidget(inner_tabs.root, 1)",
    )
    for fragment in gui_required:
        _require(fragment in gui_source, "Missing Planner child-tab wiring: " + fragment)

    _require(
        "build_planner_two_column_splitter" not in gui_source,
        "Planner GUI still wires the obsolete two-column splitter.",
    )

    layout_required = (
        "from kanda_reasoner_app.templates.inner_tabs_template import (",
        "InnerTabSpec",
        "build_inner_tab_row",
        'InnerTabSpec("Input & Analysis", "largeFilePlannerInputAnalysisTab")',
        'InnerTabSpec("Plan & Actions", "largeFilePlannerPlanActionsTab")',
        "stack = QStackedWidget()",
        "stack.setMinimumWidth(0)",
        "stack.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)",
        "page.setMinimumWidth(0)",
        "page.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)",
        "initial_index=0",
    )
    for fragment in layout_required:
        _require(fragment in layout_source, "Missing inner-tab layout contract: " + fragment)

    forbidden_layout_fragments = (
        "architecture_review_subtabs",
        "workbench_gui",
        "ast_split",
        "write_text(",
        "write_bytes(",
        "open(",
        "Path(",
        "setattr(window",
        "_large_file_refactor_planner_state",
    )
    for fragment in forbidden_layout_fragments:
        _require(
            fragment not in layout_source,
            "Planner layout helper crossed its box-local responsibility: " + fragment,
        )

    template_required = (
        "class InnerTabSpec",
        "def build_inner_tab_row(",
        "def wire_inner_tab_buttons(",
        "def select_inner_tab(",
        "INNER_TAB_ACTIVE_STYLE",
        "INNER_TAB_INACTIVE_STYLE",
    )
    for fragment in template_required:
        _require(fragment in template_source, "Inner-tab blueprint contract missing: " + fragment)

    print("PLANNER_CHILD_TABS: PRESENT")
    print("INPUT_ANALYSIS_PAGE: CANDIDATE_SETTINGS_EVIDENCE")
    print("PLAN_ACTIONS_PAGE: PLAN_PREVIEW_ACTIONS")
    print("INNER_TAB_BLUEPRINT: PUBLIC_CONTRACT_USED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")


def _validate_qt_runtime(project_root: Path) -> None:
    """Exercise the Planner-local child-tab host when PySide6 is available."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication, QGroupBox, QSizePolicy
    except ModuleNotFoundError:
        print("GUI CHILD TAB CHECK: SKIPPED_NO_PYSIDE6")
        return

    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_inner_tabs_layout import (
        build_planner_inner_tabs,
    )

    app = QApplication.instance() or QApplication([])
    result = build_planner_inner_tabs(
        [QGroupBox("Candidate"), QGroupBox("Settings"), QGroupBox("Evidence")],
        [QGroupBox("Plan"), QGroupBox("Actions")],
    )
    _require(result.stack.count() == 2, "Planner child-tab stack must contain two pages.")
    _require(len(result.buttons) == 2, "Planner child-tab row must contain two buttons.")
    _require(result.stack.currentIndex() == 0, "Input & Analysis must be the initial page.")
    _require(result.buttons[0].text() == "Input & Analysis", "Unexpected first child-tab label.")
    _require(result.buttons[1].text() == "Plan & Actions", "Unexpected second child-tab label.")
    result.buttons[1].click()
    app.processEvents()
    _require(result.stack.currentIndex() == 1, "Second child tab did not switch the stack.")
    _require(
        result.stack.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Ignored,
        "Planner child-tab stack must ignore horizontal size hints.",
    )
    for index in range(result.stack.count()):
        _require(
            result.stack.widget(index).sizePolicy().horizontalPolicy()
            == QSizePolicy.Policy.Ignored,
            "Every Planner child page must ignore horizontal size hints.",
        )
    result.root.deleteLater()
    app.processEvents()
    print("GUI CHILD TAB CHECK: PASS")


def validate(project_root: Path) -> None:
    """Run focused static and optional GUI checks."""
    root = project_root.expanduser().resolve()
    _require(root.is_dir(), "Project root is not a directory: " + str(root))
    _validate_static_contract(root)
    _validate_qt_runtime(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    try:
        validate(Path(args.project_root))
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID + " - " + str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
