"""Validate the real PySide Workbench Page Code button and dialog."""

from __future__ import annotations

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QDialog, QPlainTextEdit, QWidget

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_page_code_gui import (
    build_workbench_page_code_button,
)


FEATURE_ID = "large-file-refactor-workbench-page-code-real-widget-v1"


class _RootEdit:
    def text(self) -> str:
        return r"E:\kanda_reasoner"


class _Window(QWidget):
    pass


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    app = QApplication.instance() or QApplication([])
    window = _Window()
    window._root_path_edit = _RootEdit()
    window._large_file_refactor_workbench_state = "READY_FOR_REAL_PREVIEW"
    intake = QPlainTextEdit()
    intake.setPlainText("REAL_WIDGET_PLAN_INTAKE_TOKEN")
    dependency = QPlainTextEdit()
    dependency.setPlainText("REAL_WIDGET_DEPENDENCY_TOKEN")
    window._large_file_refactor_workbench_intake_output = intake
    window._large_file_refactor_workbench_dependency_output = dependency

    button = build_workbench_page_code_button(window)
    _assert(button.text() == "Get Page Code", "Unexpected button label")
    print("WORKBENCH_PAGE_CODE_REAL_WIDGET_BUTTON_PRESENT: PASS")

    result = {"checked": False}

    def inspect_dialog() -> None:
        dialogs = [item for item in QApplication.topLevelWidgets() if isinstance(item, QDialog)]
        _assert(bool(dialogs), "Page Code dialog not found")
        dialog = dialogs[-1]
        outputs = dialog.findChildren(QPlainTextEdit)
        _assert(len(outputs) == 1, "Expected one Page Code text window")
        output = outputs[0]
        _assert(output.isReadOnly(), "Page Code text window must be read-only")
        text = output.toPlainText()
        _assert("REAL_WIDGET_PLAN_INTAKE_TOKEN" in text, "Plan Intake text missing")
        _assert("REAL_WIDGET_DEPENDENCY_TOKEN" in text, "Dependency text missing")
        _assert("Origin: " in text, "Origin explanations missing")
        result["checked"] = True
        dialog.accept()

    QTimer.singleShot(0, inspect_dialog)
    button.click()
    app.processEvents()
    _assert(result["checked"], "Real dialog inspection did not complete")
    print("WORKBENCH_PAGE_CODE_REAL_WIDGET_READ_ONLY_TEXT_WINDOW: PASS")
    print("WORKBENCH_PAGE_CODE_REAL_WIDGET_CURRENT_TEXT_CAPTURE: PASS")
    print("WORKBENCH_PAGE_CODE_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
