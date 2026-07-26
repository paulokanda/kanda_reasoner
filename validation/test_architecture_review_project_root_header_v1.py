#!/usr/bin/env python3
"""Validate Architecture Review project-root header relocation v1."""

from __future__ import annotations

import py_compile
from pathlib import Path

FEATURE_ID = "architecture-review-project-root-header-v1"


def require(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear message when condition is false."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read a UTF-8 source file."""
    return path.read_text(encoding="utf-8")


def test_manage_architecture_gui(project_root: Path) -> None:
    source = project_root / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture_gui.py"
    require(source.exists(), f"Missing source file: {source}")
    py_compile.compile(str(source), doraise=True)
    text = read_text(source)

    require(
        'self._root_path_label = QLabel("Project Root:")' in text,
        "Project Root label is not defined for the Architecture Review header row",
    )
    require(
        'self._browse_root_btn = QPushButton("Browse...")' in text,
        "Project root Browse button is not owned as a movable root control",
    )
    require(
        "def move_project_root_controls_to_layout(" in text,
        "Architecture Review does not expose a project-root mover",
    )
    require(
        "destination_layout.insertWidget(insert_index + 1, self._root_path_label, 0)" in text,
        "Project Root label is not inserted into the host status/source row",
    )
    require(
        "destination_layout.insertWidget(insert_index + 2, self._root_path_edit, 0)" in text,
        "Project root path widget is not inserted into the host status/source row",
    )
    require(
        "destination_layout.insertWidget(insert_index + 3, self._browse_root_btn, 0)" in text,
        "Project root Browse button is not inserted into the host status/source row",
    )
    require(
        'form.addRow("Run options", mode_row)' in text,
        "Run options row was not preserved after removing Project root from the form",
    )
    require(
        'form.addRow("Project root", root_row)' not in text,
        "Old Project root form row is still present",
    )
    require(
        "def move_script_selector_to_layout(" not in text,
        "Architecture Review still exposes the old worker-script mover",
    )
    require(
        'self._script_host_label = QLabel("Worker Script:")' not in text,
        "Old Worker Script host label is still created by Architecture Review",
    )
    require(
        'toolbar = QToolBar("Main")' in text,
        "The movable Main toolbar was unexpectedly removed",
    )
    for action_name in ("Run", "Clear Output", "Save Output", "Mode Help"):
        require(
            f'QAction("{action_name}", self)' in text,
            f"Toolbar action was unexpectedly removed: {action_name}",
        )


def test_lazy_tab_host(project_root: Path) -> None:
    source = project_root / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
    require(source.exists(), f"Missing source file: {source}")
    py_compile.compile(str(source), doraise=True)
    text = read_text(source)

    require(
        "self.python_executable_label.setStyleSheet(" in text,
        "Python executable label does not receive a frame stylesheet",
    )
    require(
        '"border: 1px solid black; padding: 2px 6px;"' in text,
        "Python executable label does not have the requested black frame",
    )
    require(
        "def _move_tab1_project_root_controls_to_status_row(self, widget) -> None:" in text,
        "Lazy tab host does not have the Tab 1 project-root mover",
    )
    require(
        'mover = getattr(widget, "move_project_root_controls_to_layout", None)' in text,
        "Lazy tab host does not request the Architecture Review project-root mover",
    )
    require(
        "self._move_tab1_project_root_controls_to_status_row(widget)" in text,
        "Lazy tab load path does not move Project Root into the host row",
    )
    require(
        "self._move_tab1_worker_script_selector_to_status_row(widget)" not in text,
        "Lazy tab load path still moves the old Architecture Review worker script selector",
    )
    require(
        "def _move_tab2_worker_script_selector_to_status_row(self, widget: QWidget) -> None:" in text,
        "Tab 2 worker-script mover was accidentally removed",
    )
    require(
        'mover = getattr(widget, "move_script_selector_to_layout", None)' in text,
        "Worker-script mover support for other tabs was accidentally removed",
    )


def main() -> int:
    project_root = Path.cwd()
    test_manage_architecture_gui(project_root)
    test_lazy_tab_host(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
