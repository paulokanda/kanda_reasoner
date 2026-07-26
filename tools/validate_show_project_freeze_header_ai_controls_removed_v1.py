#!/usr/bin/env python3
"""Validate legacy AI header control removal from two lazy tool tabs."""

from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
from typing import Iterable

FEATURE_ID = "show-project-freeze-header-ai-controls-removal-v1"
LAZY_TABS_PATH = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"
)
HEADER_TEMPLATE_PATH = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/tab_header_template.py"
)
EXPECTED_LEGACY_SOURCES = {
    "_ENGINEERING_SAFETY_GUI_SOURCE",
    "_DAILY_REFACTOR_GUI_SOURCE",
}
TARGET_TITLES = (
    "Show Project to AI",
    "Freeze Feature After Update",
)


def require(condition: bool, message: str) -> None:
    """Raise one focused assertion when a contract is not met."""
    if not condition:
        raise AssertionError(message)


def read_text(root: Path, relative: Path) -> str:
    """Read one required UTF-8 project source file."""
    path = root / relative
    require(path.is_file(), "Required source file is missing: " + str(path))
    return path.read_text(encoding="utf-8-sig")


def assigned_name_set(tree: ast.AST, assignment_name: str) -> set[str]:
    """Return names assigned to one literal set or frozenset expression."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == assignment_name
            for target in node.targets
        ):
            continue
        value = node.value
        if isinstance(value, ast.Set):
            elements: Iterable[ast.expr] = value.elts
        elif (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "frozenset"
            and len(value.args) == 1
            and isinstance(value.args[0], (ast.Set, ast.List, ast.Tuple))
        ):
            elements = value.args[0].elts
        else:
            raise AssertionError(
                assignment_name + " must use one literal set or frozenset."
            )
        names = {
            element.id
            for element in elements
            if isinstance(element, ast.Name)
        }
        require(
            len(names) == len(tuple(elements)),
            assignment_name + " contains a non-name entry.",
        )
        return names
    raise AssertionError("Assignment was not found: " + assignment_name)


def validate_static_contract(root: Path) -> None:
    """Validate exact source ownership and unaffected header contracts."""
    lazy_source = read_text(root, LAZY_TABS_PATH)
    header_source = read_text(root, HEADER_TEMPLATE_PATH)
    tree = ast.parse(lazy_source, filename=str(LAZY_TABS_PATH))

    sources = assigned_name_set(tree, "_LEGACY_HEADER_AI_GROUP_SOURCES")
    require(
        sources == EXPECTED_LEGACY_SOURCES,
        "Legacy AI header source set changed: " + repr(sorted(sources)),
    )
    require(
        "_CONTEXT_COLLECTOR_GUI_SOURCE" not in lazy_source,
        "Show Project to AI remains connected to the legacy AI header group.",
    )
    require(
        "review_handler = self._freeze_feature_ai_review_first_check"
        not in lazy_source,
        "Freeze Feature After Update remains connected to AI Review First Check.",
    )
    require(
        "review_handler = self._show_project_ai_review_first_check"
        not in lazy_source,
        "Show Project to AI remains connected to AI Review First Check.",
    )
    require(
        "if spec.source_hint == _FREEZE_AFTER_UPDATE_GUI_SOURCE:" in lazy_source,
        "Freeze Help routing was removed with the legacy AI controls.",
    )
    require(
        "help_handler = self._open_freeze_feature_help" in lazy_source,
        "Freeze Help action no longer uses its existing owner.",
    )
    require(
        "title_font.setBold(True)" in header_source,
        "The shared bold tab title contract changed.",
    )
    require(
        "self.project_root_host" in header_source,
        "The shared Project Root host contract changed.",
    )
    require(
        "self.help_button = QPushButton(TAB_HEADER_HELP_FILE_TEXT)" in header_source,
        "The shared Help action contract changed.",
    )
    print("TARGET_HEADER_AI_CONTROLS_STATIC_REMOVAL: PASS")
    print("SHOW_PROJECT_HEADER_HELP_AND_PROJECT_ROOT_PRESERVED: PASS")
    print("FREEZE_HEADER_HELP_AND_PROJECT_ROOT_PRESERVED: PASS")
    print("NON_TARGET_LEGACY_HEADER_SOURCE_SET_PRESERVED: PASS")


def validate_real_qt(root: Path, allow_no_qt: bool) -> None:
    """Construct real lazy headers and verify target/non-target behavior."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication
    except ImportError:
        if allow_no_qt:
            print("REAL_QT_HEADER_VALIDATION: SKIPPED_NO_PYSIDE6")
            return
        raise RuntimeError("PySide6 is required for real header validation.")

    from kanda_reasoner_app.reasoner_tools_gui_shell._lazy_tab_shell_chrome import (
        _DAILY_REFACTOR_GUI_SOURCE,
        _ENGINEERING_SAFETY_GUI_SOURCE,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs import LazyToolTab
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import (
        TOOLS,
        ToolSpec,
    )

    app = QApplication.instance() or QApplication([])
    widgets = []
    try:
        by_title = {spec.step_title: spec for spec in TOOLS}
        for title in TARGET_TITLES:
            require(title in by_title, "Tool registry title is missing: " + title)
            widget = LazyToolTab(by_title[title], lambda *_args: None)
            widgets.append(widget)
            header = widget.tab_header_template
            require(
                header.title_label.text() == title,
                "Header title changed for " + title,
            )
            require(
                header.title_label.font().bold(),
                "Header title is not bold for " + title,
            )
            require(
                header.project_root_host is not None,
                "Project Root host is missing for " + title,
            )
            require(
                header.help_button is not None,
                "Help action is missing for " + title,
            )
            require(
                header.ai_model_label is None,
                "AI model label remains for " + title,
            )
            require(
                header.ai_model_combo is None,
                "AI model dropdown remains for " + title,
            )
            require(
                header.refresh_ai_models_button is None,
                "Refresh AI Models remains for " + title,
            )
            require(
                header.ai_review_first_check_button is None,
                "AI Review First Check remains for " + title,
            )
            require(
                header.ai_group_layout.count() == 0,
                "Legacy AI group layout is not empty for " + title,
            )

        engineering_spec = ToolSpec(
            step_title="Engineering Safety validation fixture",
            source_hint=_ENGINEERING_SAFETY_GUI_SOURCE,
        )
        engineering = LazyToolTab(engineering_spec, lambda *_args: None)
        widgets.append(engineering)
        engineering_header = engineering.tab_header_template
        require(
            engineering_header.ai_model_combo is not None,
            "Engineering Safety lost its legacy AI model dropdown.",
        )
        require(
            engineering_header.refresh_ai_models_button is not None,
            "Engineering Safety lost Refresh AI Models.",
        )
        require(
            engineering_header.ai_review_first_check_button is not None,
            "Engineering Safety lost AI Review First Check.",
        )

        daily_spec = ToolSpec(
            step_title="Daily Refactor validation fixture",
            source_hint=_DAILY_REFACTOR_GUI_SOURCE,
        )
        daily = LazyToolTab(daily_spec, lambda *_args: None)
        widgets.append(daily)
        daily_header = daily.tab_header_template
        require(
            daily_header.ai_model_combo is not None,
            "Daily Refactor lost its legacy AI model dropdown.",
        )
        require(
            daily_header.refresh_ai_models_button is not None,
            "Daily Refactor lost Refresh AI Models.",
        )
        require(
            daily_header.ai_review_first_check_button is None,
            "Daily Refactor unexpectedly gained AI Review First Check.",
        )
        print("REAL_QT_TARGET_HEADERS_HAVE_NO_LEGACY_AI_CONTROLS: PASS")
        print("REAL_QT_TARGET_TITLES_BOLD: PASS")
        print("REAL_QT_TARGET_HELP_AND_PROJECT_ROOT_PRESERVED: PASS")
        print("REAL_QT_NON_TARGET_LEGACY_HEADERS_PRESERVED: PASS")
    finally:
        for widget in widgets:
            widget.close()
            widget.deleteLater()
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        app.processEvents()


def parse_args() -> argparse.Namespace:
    """Parse validator arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root")
    parser.add_argument("--allow-no-qt", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Run static and real-Qt validation."""
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=False)
    validate_static_contract(root)
    validate_real_qt(root, bool(args.allow_no_qt))
    for relative in (LAZY_TABS_PATH, Path(__file__).resolve().relative_to(root)):
        line_count = len((root / relative).read_text(encoding="utf-8-sig").splitlines())
        require(line_count <= 500, relative.as_posix() + " exceeds 500 lines.")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(exc.__class__.__name__ + ": " + str(exc))
        raise SystemExit(1)
