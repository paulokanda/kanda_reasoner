"""Validate Audit Project host-width stability and nested tab containment."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
import time

__all__ = ["main"]

FEATURE_ID = "architecture-review-host-width-stability-v2"
MAX_PHYSICAL_LINES = 500
SUBTABS_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
SIBLINGS_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py"
)
WORKBENCH_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_gui_layout.py"
)


def _configure_qt_runtime_environment() -> None:
    """Configure a deterministic offscreen Qt environment on Windows."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name != "nt" or os.environ.get("QT_QPA_FONTDIR"):
        return
    system_root = Path(os.environ.get("SystemRoot", r"C:\Windows"))
    font_directory = system_root / "Fonts"
    if font_directory.is_dir():
        os.environ["QT_QPA_FONTDIR"] = str(font_directory)


def _require(condition: bool, message: str) -> None:
    """Raise when one validation condition is false."""
    if not condition:
        raise AssertionError(message)


def _read_python(root: Path, relative: Path) -> str:
    """Read, compile, and parse one Python source file."""
    path = root / relative
    _require(path.is_file(), "Missing source file: " + str(relative))
    source = path.read_text(encoding="utf-8", errors="strict")
    compile(source, str(path), "exec")
    ast.parse(source, filename=str(path))
    _require(
        len(source.splitlines()) <= MAX_PHYSICAL_LINES,
        str(relative) + " exceeds 500 physical lines.",
    )
    return source


def _require_fragments(source: str, fragments: tuple[str, ...], owner: str) -> None:
    """Require semantic contract fragments without pinning incidental layout."""
    for fragment in fragments:
        _require(fragment in source, owner + " missing fragment: " + fragment)


def _validate_static_contract(project_root: Path) -> None:
    """Validate width containment and current nested-tab ownership."""
    subtabs = _read_python(project_root, SUBTABS_RELATIVE)
    siblings = _read_python(project_root, SIBLINGS_RELATIVE)
    workbench = _read_python(project_root, WORKBENCH_RELATIVE)

    _require_fragments(
        subtabs,
        (
            "def _contain_subtab_horizontal_size_pressure",
            "window._audit_project_subtab_widget",
            "window._architecture_review_page",
            "window._architecture_review_subtab_stack",
            "window._architecture_review_general_page",
            "window._architecture_review_dismissed_findings_page",
            "window._architecture_review_split_page",
            "window._architecture_review_refactor_planner_page",
            "window._architecture_review_refactor_workbench_page",
            "window._engineering_safety_page",
            "window._engineering_diagnostics_page",
            "window._workflow_review_page",
            "window._workflow_review_page.centralWidget()",
            "container.setMinimumSize(0, 0)",
            "container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)",
            "_contain_subtab_horizontal_size_pressure(window)",
            '"Check Update Architecture"',
            '"Dismissed Findings"',
            '"Large Module AST Split Audit"',
            '"Large File Refactor Planner"',
            '"Large File Refactor WorkBench"',
        ),
        "Architecture Review host",
    )
    _require_fragments(
        siblings,
        (
            '_ENGINEERING_SAFETY_LABEL = "Engineering Safety"',
            '_WORKFLOW_REVIEW_LABEL = "Workflow Review"',
            "tab_widget.addTab(window._engineering_safety_page",
            "tab_widget.addTab(window._workflow_review_page",
        ),
        "Audit Project siblings",
    )
    _require_fragments(
        workbench,
        (
            "ScrollBarAlwaysOff",
            "AdjustIgnored",
            "content.setMinimumWidth(0)",
            "content.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum)",
            "label.setWordWrap(True)",
            "label.setMinimumWidth(0)",
        ),
        "Workbench containment",
    )

    for fragment in (
        "setFixedWidth(1200",
        "setFixedWidth(1400",
        "setMinimumWidth(1200",
        "setMinimumWidth(1400",
    ):
        _require(fragment not in subtabs, "Forbidden host-width lock: " + fragment)

    print("STACK_PAGE_POLICY: HORIZONTAL_IGNORED")
    print("WORKBENCH_CONTAINMENT: PRESERVED")
    print("AUDIT_PROJECT_SIBLING_WIDTH_OWNERSHIP: PASS")
    print("MODULE_SIZE_GATE: PASS")


def _validate_qt_runtime(project_root: Path) -> bool:
    """Verify width containment with a QThread-free real-Qt fixture."""
    _configure_qt_runtime_environment()
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QLabel,
            QMainWindow,
            QSizePolicy,
            QTabWidget,
            QVBoxLayout,
            QWidget,
        )
    except ModuleNotFoundError:
        print("GUI HOST WIDTH CHECK: SKIPPED_NO_PYSIDE6")
        return False

    project_text = str(project_root)
    if project_text not in sys.path:
        sys.path.insert(0, project_text)

    from kanda_reasoner_app.manage_architecture.architecture_review_subtabs import (
        _contain_subtab_horizontal_size_pressure,
    )

    app = QApplication.instance() or QApplication([])
    previous_quit = app.quitOnLastWindowClosed()
    app.setQuitOnLastWindowClosed(False)
    host = QMainWindow()
    central = QWidget(host)
    layout = QVBoxLayout(central)
    host.setCentralWidget(central)

    outer_tabs = QTabWidget(central)
    architecture_page = QWidget(outer_tabs)
    architecture_layout = QVBoxLayout(architecture_page)
    inner_tabs = QTabWidget(architecture_page)
    architecture_layout.addWidget(inner_tabs)

    inner_labels = (
        "Check Update Architecture",
        "Dismissed Findings",
        "Large Module AST Split Audit",
        "Large File Refactor Planner",
        "Large File Refactor WorkBench",
    )
    inner_pages = tuple(QWidget(inner_tabs) for _ in inner_labels)
    for page, label in zip(inner_pages, inner_labels, strict=True):
        inner_tabs.addTab(page, label)

    pressure_layout = QVBoxLayout(inner_pages[1])
    pressure_layout.addWidget(QLabel("W" * 500, inner_pages[1]))

    engineering_page = QWidget(outer_tabs)
    engineering_page.engineering_safety_audit_tabs = QTabWidget(engineering_page)
    engineering_page.engineering_safety_full_audit_page = QWidget(engineering_page)
    engineering_page.engineering_safety_pontual_audit_page = QWidget(engineering_page)
    diagnostics_page = QWidget(engineering_page)

    workflow_page = QMainWindow(outer_tabs)
    workflow_page.setCentralWidget(QWidget(workflow_page))

    outer_tabs.addTab(architecture_page, "Architecture Review")
    outer_tabs.addTab(engineering_page, "Engineering Safety")
    outer_tabs.addTab(workflow_page, "Workflow Review")
    layout.addWidget(outer_tabs)

    class _Probe:
        pass

    probe = _Probe()
    probe._audit_project_subtab_widget = outer_tabs
    probe._architecture_review_page = architecture_page
    probe._architecture_review_subtab_stack = inner_tabs
    (
        probe._architecture_review_general_page,
        probe._architecture_review_dismissed_findings_page,
        probe._architecture_review_split_page,
        probe._architecture_review_refactor_planner_page,
        probe._architecture_review_refactor_workbench_page,
    ) = inner_pages
    probe._engineering_safety_page = engineering_page
    probe._engineering_diagnostics_page = diagnostics_page
    probe._workflow_review_page = workflow_page

    _contain_subtab_horizontal_size_pressure(probe)

    containers = (
        outer_tabs,
        architecture_page,
        inner_tabs,
        *inner_pages,
        engineering_page,
        engineering_page.engineering_safety_audit_tabs,
        engineering_page.engineering_safety_full_audit_page,
        engineering_page.engineering_safety_pontual_audit_page,
        diagnostics_page,
        workflow_page,
        workflow_page.centralWidget(),
    )

    try:
        host.resize(1200, 800)
        host.show()
        for _ in range(4):
            app.processEvents()
        baseline_width = int(host.width())

        for container in containers:
            _require(
                container.minimumWidth() == 0 and container.minimumHeight() == 0,
                "Nested Audit Project container minimum size is not zero.",
            )
            _require(
                container.sizePolicy().horizontalPolicy()
                == QSizePolicy.Policy.Ignored,
                "Nested Audit Project container does not ignore horizontal hints.",
            )

        for index in range(inner_tabs.count()):
            inner_tabs.setCurrentIndex(index)
            app.processEvents()
            _require(
                int(host.width()) == baseline_width,
                "Architecture Review child tab widened the host.",
            )

        for index in range(outer_tabs.count()):
            outer_tabs.setCurrentIndex(index)
            app.processEvents()
            _require(
                int(host.width()) == baseline_width,
                "Audit Project sibling tab widened the host.",
            )

        print("GUI HOST WIDTH CHECK: PASS")
        print("GUI HOST WIDTH FIXTURE: NO_BACKGROUND_QTHREADS")
        return True
    finally:
        host.close()
        host.deleteLater()
        for _ in range(6):
            app.processEvents()
        app.setQuitOnLastWindowClosed(previous_quit)


def validate(project_root: Path) -> None:
    """Run focused host-width stability checks."""
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
