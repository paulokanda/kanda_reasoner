#!/usr/bin/env python3
"""Validate Architecture Review run options toolbar relocation v1."""

from __future__ import annotations

import py_compile
from pathlib import Path

FEATURE_ID = "architecture-review-run-options-toolbar-left-v1"


def require(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear message when condition is false."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read a UTF-8 source file."""
    return path.read_text(encoding="utf-8")


def test_manage_architecture_gui(project_root: Path) -> None:
    source = (
        project_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "manage_architecture_gui.py"
    )
    require(source.exists(), f"Missing source file: {source}")
    py_compile.compile(str(source), doraise=True)
    text = read_text(source)

    toolbar_index = text.index('toolbar = QToolBar("Main")')
    run_options_index = text.index("self._run_options_toolbar_widget = QWidget(self)")
    add_widget_index = text.index("toolbar.addWidget(self._run_options_toolbar_widget)")
    separator_index = text.index("toolbar.addSeparator()")
    run_action_index = text.index('run_action = QAction("Run", self)')
    clear_action_index = text.index('clear_action = QAction("Clear Output", self)')
    save_action_index = text.index('save_action = QAction("Save Output", self)')
    help_action_index = text.index('help_action = QAction("Mode Help", self)')

    require(
        toolbar_index < run_options_index < add_widget_index < separator_index < run_action_index,
        "Run options controls are not inserted to the left of the Main toolbar actions",
    )
    require(
        run_action_index < clear_action_index < save_action_index < help_action_index,
        "Main toolbar action order was unexpectedly changed",
    )
    require(
        'self._run_options_toolbar_widget.setObjectName(\n'
        '            "architecture_review_run_options_toolbar_widget"\n'
        '        )' in text,
        "Run options toolbar widget object name is missing",
    )
    require(
        'self._run_options_toolbar_label = QLabel("Run options")' in text,
        "Run options label is not in the toolbar widget",
    )
    require(
        'self._mode_toolbar_label = QLabel("Mode")' in text,
        "Mode label is not in the toolbar widget",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._mode_combo)" in text,
        "Mode dropdown is not placed in the toolbar widget",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._strict_write_checkbox)" in text,
        "Require confirm before write checkbox is not placed in the toolbar widget",
    )
    require(
        'form.addRow("Run options", mode_row)' not in text,
        "Old Run options form row is still present in the body",
    )
    require(
        "mode_row = QHBoxLayout()" not in text,
        "Old body mode_row layout is still present",
    )
    require(
        "QFormLayout" not in text,
        "QFormLayout import or use should not remain after moving Run options to toolbar",
    )
    require(
        'self._strict_write_checkbox = QCheckBox("Require confirm before write")' in text,
        "Require confirm before write checkbox was unexpectedly renamed or removed",
    )
    require(
        "if mode == \"write\" and self._strict_write_checkbox.isChecked():" in text,
        "Write confirmation guard was unexpectedly changed",
    )
    require(
        'self._root_path_label = QLabel("Project Root:")' in text,
        "Project Root label from the prior header patch was unexpectedly removed",
    )
    require(
        "def move_project_root_controls_to_layout(" in text,
        "Project Root host-row mover from the prior patch was unexpectedly removed",
    )
    require(
        'self._script_host_label = QLabel("Worker Script:")' not in text,
        "Old Architecture Review Worker Script label was accidentally restored",
    )
    require(
        "def move_script_selector_to_layout(" not in text,
        "Old Architecture Review worker-script mover was accidentally restored",
    )


def test_lazy_tab_host_is_shielded(project_root: Path) -> None:
    source = project_root / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
    require(source.exists(), f"Missing source file: {source}")
    py_compile.compile(str(source), doraise=True)
    text = read_text(source)

    require(
        "def _move_tab1_project_root_controls_to_status_row(self, widget) -> None:" in text,
        "Tab 1 Project Root host-row mover was unexpectedly removed",
    )
    require(
        'mover = getattr(widget, "move_project_root_controls_to_layout", None)' in text,
        "Lazy tab host no longer requests the Architecture Review Project Root mover",
    )
    require(
        '"border: 1px solid black; padding: 2px 6px;"' in text,
        "Python executable black frame from prior patch was unexpectedly removed",
    )
    require(
        "def _move_tab2_worker_script_selector_to_status_row(self, widget: QWidget) -> None:" in text,
        "Tab 2 worker-script relocation support was accidentally removed",
    )


def main() -> int:
    """Run all validation checks."""
    project_root = Path.cwd()
    test_manage_architecture_gui(project_root)
    test_lazy_tab_host_is_shielded(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
