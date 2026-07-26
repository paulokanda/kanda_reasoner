"""Validate compact Planner Settings layout and local-AI visual emphasis."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys

__all__ = [
    "main",
]

FEATURE_ID = "large-file-refactor-planner-compact-settings-ai-highlight-v1"
MAX_PHYSICAL_LINES = 500
BASE = Path("kanda_reasoner_app/manage_architecture/large_file_refactor_planner")
GUI_SHELL_RELATIVE = BASE / "gui_shell.py"
INNER_TABS_RELATIVE = BASE / "planner_inner_tabs_layout.py"
PRESENTATION_RELATIVE = BASE / "planner_settings_panel_presentation.py"


def _require(condition: bool, message: str) -> None:
    """Raise an assertion for one failed focused contract check."""
    if not condition:
        raise AssertionError(message)


def _read_source(path: Path) -> str:
    """Read, compile, parse, and size-check one Python source file."""
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
    """Check compact sizing, isolated styling, and box-local ownership."""
    gui_source = _read_source(project_root / GUI_SHELL_RELATIVE)
    inner_tabs_source = _read_source(project_root / INNER_TABS_RELATIVE)
    presentation_source = _read_source(project_root / PRESENTATION_RELATIVE)

    gui_required = (
        "from .planner_settings_panel_presentation import apply_settings_panel_presentation",
        'use_llm = _add_checked_box(row, "Use local AI when available", True)',
        "apply_settings_panel_presentation(box, row, use_llm)",
        "build_planner_inner_tabs(",
    )
    for fragment in gui_required:
        _require(fragment in gui_source, "Missing Planner GUI wiring: " + fragment)

    presentation_required = (
        "settings_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)",
        "settings_row.setContentsMargins(8, 4, 8, 4)",
        "settings_row.setSpacing(6)",
        "settings_row.setAlignment(Qt.AlignVCenter)",
        'local_ai_checkbox.setObjectName(_LOCAL_AI_OBJECT_NAME)',
        "font.setBold(True)",
        "local_ai_checkbox.setFont(font)",
        "local_ai_checkbox.setStyleSheet(_LOCAL_AI_STYLE)",
        "color: #16843A;",
        "border: 1px solid #000000;",
    )
    for fragment in presentation_required:
        _require(
            fragment in presentation_source,
            "Missing compact Settings presentation contract: " + fragment,
        )

    forbidden_fragments = (
        "architecture_review_subtabs",
        "workbench_gui",
        "ast_split",
        "planner_local_ai_plan_review",
        "write_text(",
        "write_bytes(",
        "open(",
        "Path(",
        "setattr(window",
        "_large_file_refactor_planner_state",
    )
    for fragment in forbidden_fragments:
        _require(
            fragment not in presentation_source,
            "Presentation helper crossed its box-local responsibility: " + fragment,
        )

    _require(
        "stack.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)"
        in inner_tabs_source,
        "Child-tab horizontal containment was regressed.",
    )
    _require(
        "page.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)"
        in inner_tabs_source,
        "Child-page horizontal containment was regressed.",
    )

    print("PLANNER_SETTINGS_HEIGHT: SINGLE_ROW_COMPACT")
    print("LOCAL_AI_LABEL: BOLD_GREEN_BLACK_FRAME")
    print("STYLE_SCOPE: OBJECT_NAME_ISOLATED")
    print("CHILD_TAB_HORIZONTAL_CONTAINMENT: PRESERVED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")


def _validate_qt_runtime(project_root: Path) -> None:
    """Check real Qt size policy and local checkbox styling when available."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication, QCheckBox, QGroupBox, QHBoxLayout, QSizePolicy
    except ModuleNotFoundError:
        print("GUI SETTINGS CHECK: SKIPPED_NO_PYSIDE6")
        return

    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_settings_panel_presentation import (
        apply_settings_panel_presentation,
    )

    app = QApplication.instance() or QApplication([])
    box = QGroupBox("2. Settings panel")
    row = QHBoxLayout(box)
    checkbox = QCheckBox("Use local AI when available")
    row.addWidget(checkbox)
    apply_settings_panel_presentation(box, row, checkbox)
    app.processEvents()

    _require(
        box.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Fixed,
        "Settings group must use fixed vertical size policy.",
    )
    _require(checkbox.font().bold(), "Local-AI checkbox font must be bold.")
    style = checkbox.styleSheet()
    _require("#16843A" in style, "Local-AI checkbox green text style is missing.")
    _require("#000000" in style, "Local-AI checkbox black frame style is missing.")
    _require(
        checkbox.objectName() == "largeFileRefactorUseLocalAI",
        "Local-AI style selector must remain object-name scoped.",
    )
    margins = row.contentsMargins()
    _require(
        (margins.left(), margins.top(), margins.right(), margins.bottom()) == (8, 4, 8, 4),
        "Settings row compact margins changed unexpectedly.",
    )

    box.deleteLater()
    app.processEvents()
    print("GUI SETTINGS CHECK: PASS")


def validate(project_root: Path) -> None:
    """Run focused static and optional Qt checks."""
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
