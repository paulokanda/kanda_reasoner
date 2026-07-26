# project-path: tools/validate_workbench_legacy_behavior_panel_removal_real_widget_v1.py
"""Validate legacy behavior-panel removal on the real PySide Workbench widget tree."""
from __future__ import annotations

import os
from pathlib import Path
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _configure_offscreen_font_directory() -> str:
    """Resolve a valid Windows font directory before importing PySide6."""
    if os.name != "nt":
        return "NOT_REQUIRED_NON_WINDOWS"
    configured = os.environ.get("QT_QPA_FONTDIR", "").strip()
    if configured:
        path = Path(configured)
        if not path.is_dir():
            raise RuntimeError("QT_QPA_FONTDIR_DOES_NOT_EXIST:" + str(path))
        return str(path)
    candidates: list[Path] = []
    for variable_name in ("WINDIR", "SystemRoot"):
        value = os.environ.get(variable_name, "").strip()
        if value:
            candidate = Path(value) / "Fonts"
            if candidate not in candidates:
                candidates.append(candidate)
    for candidate in candidates:
        if candidate.is_dir():
            os.environ["QT_QPA_FONTDIR"] = str(candidate)
            return str(candidate)
    raise RuntimeError(
        "QT_OFFSCREEN_FONT_DIRECTORY_NOT_FOUND:"
        + "|".join(str(candidate) for candidate in candidates)
    )


QT_OFFSCREEN_FONTDIR = _configure_offscreen_font_directory()
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtWidgets import (  # noqa: E402
    QApplication,
    QGroupBox,
    QLineEdit,
    QMainWindow,
    QPushButton,
)

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (  # noqa: E402
    workbench_gui,
)

FEATURE_ID = "large-file-refactor-workbench-legacy-behavior-panel-removal-v1"


def main() -> None:
    """Build the real Workbench page and verify the visible control inventory."""
    app = QApplication.instance() or QApplication([])
    window = QMainWindow()
    window._root_path_edit = QLineEdit(str(PROJECT_ROOT))
    page = workbench_gui.build_large_file_refactor_workbench_page(window)
    window.setCentralWidget(page)
    window.show()
    app.processEvents()

    group_titles = {group.title() for group in page.findChildren(QGroupBox)}
    button_texts = {button.text() for button in page.findChildren(QPushButton)}
    line_edits = page.findChildren(QLineEdit)

    assert not any("Legacy Compatibility" in title for title in group_titles)
    assert "Run Optional Behavior Validation" not in button_texts
    assert not hasattr(window, "_large_file_refactor_workbench_behavior_command_edit")
    assert not hasattr(window, "_large_file_refactor_workbench_behavior_button")
    assert not hasattr(window, "_large_file_refactor_workbench_behavior_gate_label")
    assert not hasattr(window, "_large_file_refactor_workbench_behavior_output")

    required_buttons = {
        "Load Latest Planner Plan",
        "Recheck Source Hash",
        "Analyze Dependency Readiness",
        "Generate Real Preview",
        "Validate Real Preview",
        "Run Advanced Quality Review",
        "Cancel",
        "Prepare Preflight Backup Readiness",
        "Build Source Apply Payload",
        "Prepare Completion Evidence",
        "Prepare Transaction Summary",
        "Refactor Large Module",
        "Rollback Journaled Transaction",
        "Heuristic",
        "Local AI",
        "Web AI",
        "Receive From Web AI",
        "Copy Candidates to AI",
        "Import AI Answer",
        "Refactoring Folder",
        "Refactoring Folder Path",
        "Clean Refactoring Folder",
    }
    missing = sorted(required_buttons - button_texts)
    assert not missing, "MISSING_CURRENT_BUTTONS:" + "|".join(missing)

    editable_fields = [edit for edit in line_edits if edit is not window._root_path_edit]
    assert not editable_fields, "UNEXPECTED_WORKBENCH_LINE_EDIT_COUNT:" + str(len(editable_fields))

    window.close()
    app.processEvents()

    print("WORKBENCH_LEGACY_BEHAVIOR_GROUP_ABSENT_REAL_WIDGET: PASS")
    print("WORKBENCH_LEGACY_BEHAVIOR_BUTTON_ABSENT_REAL_WIDGET: PASS")
    print("WORKBENCH_LEGACY_BEHAVIOR_COMMAND_FIELD_ABSENT_REAL_WIDGET: PASS")
    print("WORKBENCH_CURRENT_BUTTON_INVENTORY_PRESERVED_REAL_WIDGET: PASS")
    print("WORKBENCH_NO_UNEXPECTED_EDITABLE_FIELDS_REAL_WIDGET: PASS")
    print("WORKBENCH_LEGACY_BEHAVIOR_PANEL_REMOVAL_REAL_WIDGET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
