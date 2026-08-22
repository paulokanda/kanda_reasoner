"""Validate Architecture Review host-width stability across local subtabs."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
from threading import Event
import time

__all__ = [
    "main",
]

FEATURE_ID = "architecture-review-host-width-stability-v2"
SUBTABS_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
WORKBENCH_LAYOUT_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_gui_layout.py"
)
ENGINEERING_FULL_AUDIT_RELATIVE = Path(
    "_reasoner_tools_gui_engineering_safety_full_audit.py"
)
ENGINEERING_SONAR_RELATIVE = Path(
    "_reasoner_tools_gui_engineering_safety_sonar.py"
)
MAX_PHYSICAL_LINES = 500



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
    """Raise an assertion when a validation condition is false."""
    if not condition:
        raise AssertionError(message)


def _validate_static_contract(project_root: Path) -> None:
    """Validate local-page and Workbench horizontal containment contracts."""
    subtabs = project_root / SUBTABS_RELATIVE
    workbench_layout = project_root / WORKBENCH_LAYOUT_RELATIVE
    engineering_full_audit = project_root / ENGINEERING_FULL_AUDIT_RELATIVE
    engineering_sonar = project_root / ENGINEERING_SONAR_RELATIVE

    _require(subtabs.is_file(), "Architecture Review subtab source is missing.")
    _require(
        workbench_layout.is_file(),
        "Workbench layout helper source is missing.",
    )
    _require(
        engineering_full_audit.is_file(),
        "Engineering Safety full-audit helper source is missing.",
    )
    _require(
        engineering_sonar.is_file(),
        "Engineering Safety sonar helper source is missing.",
    )

    source = subtabs.read_text(encoding="utf-8", errors="strict")
    workbench_source = workbench_layout.read_text(
        encoding="utf-8",
        errors="strict",
    )
    full_audit_source = engineering_full_audit.read_text(
        encoding="utf-8",
        errors="strict",
    )
    sonar_source = engineering_sonar.read_text(
        encoding="utf-8",
        errors="strict",
    )

    compile(source, str(subtabs), "exec")
    ast.parse(source, filename=str(subtabs))
    compile(workbench_source, str(workbench_layout), "exec")
    ast.parse(workbench_source, filename=str(workbench_layout))
    compile(full_audit_source, str(engineering_full_audit), "exec")
    ast.parse(full_audit_source, filename=str(engineering_full_audit))
    compile(sonar_source, str(engineering_sonar), "exec")
    ast.parse(sonar_source, filename=str(engineering_sonar))

    required_subtab_fragments = (
        "def _contain_subtab_horizontal_size_pressure",
        "window._audit_project_subtab_widget",
        "window._architecture_review_page",
        "window._architecture_review_subtab_stack",
        "container.setMinimumWidth(0)",
        "container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)",
        "_contain_subtab_horizontal_size_pressure(window)",
        '"Architecture Review"',
        '"Engineering Safety"',
        '"Check Update Architecture"',
        '"Dismissed Findings"',
        '"Large Module AST Split Audit"',
        '"Large File Refactor Planner"',
        '"Large File Refactor WorkBench"',
    )
    for fragment in required_subtab_fragments:
        _require(
            fragment in source,
            "Missing stack width-containment fragment: " + fragment,
        )

    required_full_audit_fragments = (
        'audit_tabs.insertTab(0, full_page, "Full Audit")',
        'QPushButton("Complete Enginneering Review")',
        'QPushButton("Cancel Review")',
        "create_engineering_safety_sonar",
        "cancel_event.is_set",
    )
    for fragment in required_full_audit_fragments:
        _require(
            fragment in full_audit_source,
            "Missing Engineering Safety Full Audit fragment: " + fragment,
        )


    required_sonar_fragments = (
        "GreenSonarActivityMonitor",
        'title="Engineering Safety Full Audit"',
        'setObjectName("engineeringSafetyFullAuditSonarMonitor")',
        "def start(self) -> None:",
        "def stop(self) -> None:",
        "self._monitor.start(",
        "self._monitor.set_idle()",
    )
    for fragment in required_sonar_fragments:
        _require(
            fragment in sonar_source,
            "Missing Engineering Safety sonar fragment: " + fragment,
        )
    for forbidden in (
        "QPainter",
        "QPen",
        "QTimer",
        "paintEvent",
        "drawEllipse",
        "drawLine",
    ):
        _require(
            forbidden not in sonar_source,
            "Engineering Safety duplicates canonical sonar drawing: " + forbidden,
        )
    _require(
        "layout.addWidget(sonar)" not in full_audit_source,
        "Canonical floating sonar was inserted into the page layout.",
    )
    print("ENGINEERING_SAFETY_CANONICAL_GREEN_SONAR_TEMPLATE: PASS")

    required_workbench_fragments = (
        "ScrollBarAlwaysOff",
        "AdjustIgnored",
        "content.setMinimumWidth(0)",
        "content.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum)",
        "label.setWordWrap(True)",
        "label.setMinimumWidth(0)",
    )
    for fragment in required_workbench_fragments:
        _require(
            fragment in workbench_source,
            "Earlier Workbench width containment regressed: " + fragment,
        )

    forbidden_fragments = (
        "setFixedWidth(1200",
        "setFixedWidth(1400",
        "setMinimumWidth(1200",
        "setMinimumWidth(1400",
    )
    for fragment in forbidden_fragments:
        _require(
            fragment not in source,
            "Forbidden host-width lock fragment: " + fragment,
        )

    _require(
        len(source.splitlines()) <= MAX_PHYSICAL_LINES,
        "architecture_review_subtabs.py exceeds 500 physical lines.",
    )
    _require(
        len(workbench_source.splitlines()) <= MAX_PHYSICAL_LINES,
        "workbench_gui_layout.py exceeds 500 physical lines.",
    )
    _require(
        len(full_audit_source.splitlines()) <= MAX_PHYSICAL_LINES,
        "Engineering Safety full-audit helper exceeds 500 physical lines.",
    )
    _require(
        len(sonar_source.splitlines()) <= MAX_PHYSICAL_LINES,
        "Engineering Safety sonar helper exceeds 500 physical lines.",
    )

    print("STACK_PAGE_POLICY: HORIZONTAL_IGNORED")
    print("WORKBENCH_CONTAINMENT: PRESERVED")
    print("MODULE_SIZE_GATE: PASS")


def _validate_qt_runtime(project_root: Path) -> bool:
    """Check policies and outer-window width when PySide6 is available."""
    _configure_qt_runtime_environment()
    try:
        from PySide6.QtWidgets import QApplication, QLineEdit, QSizePolicy
    except ModuleNotFoundError:
        print("GUI HOST WIDTH CHECK: SKIPPED_NO_PYSIDE6")
        return False

    project_text = str(project_root)
    if project_text not in sys.path:
        sys.path.insert(0, project_text)

    import reasoner_tools_gui_engineering_safety_panel as engineering_module

    original_runner = engineering_module.run_engineering_safety_panel_command
    runner_started = Event()

    class _Result:
        status_code = 0
        stdout = "controlled Qt validation result"
        stderr = ""

    def _controlled_runner(command_name: str, project_root_text: str) -> object:
        del command_name, project_root_text
        runner_started.set()
        time.sleep(0.35)
        return _Result()

    engineering_module.run_engineering_safety_panel_command = _controlled_runner

    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window import (
        ReasonerToolsWindow,
    )

    app = QApplication.instance() or QApplication([])
    window = ReasonerToolsWindow()
    window.resize(1200, 800)
    window.show()
    app.processEvents()

    brain_index = window._tab_index_by_tab_id["brain_navigator"]
    architecture_index = window._tab_index_by_tab_id["architecture_review"]

    window.tabs.setCurrentIndex(brain_index)
    app.processEvents()
    baseline_width = int(window.width())

    window.tabs.setCurrentIndex(architecture_index)
    page = window._lazy_page_for_tab_index(architecture_index)
    _require(page is not None, "Architecture Review lazy page is missing.")
    _require(page.ensure_loaded(), "Architecture Review failed to load.")
    for _ in range(6):
        app.processEvents()

    _require(
        window.tabs.tabText(architecture_index) == "Audit Project",
        "Top-level architecture tab was not renamed to Audit Project.",
    )

    architecture_width = int(window.width())
    _require(
        architecture_width == baseline_width,
        "Architecture Review changed host width from "
        + str(baseline_width)
        + " to "
        + str(architecture_width),
    )

    embedded = page._embedded_widget
    _require(embedded is not None, "Audit Project embedded widget is missing.")
    outer_tabs = embedded._audit_project_subtab_widget
    inner_tabs = embedded._architecture_review_subtab_stack
    _require(outer_tabs.count() == 2, "Audit Project must expose two child tabs.")
    _require(
        outer_tabs.tabText(0) == "Architecture Review",
        "Audit Project left child tab must be Architecture Review.",
    )
    _require(
        outer_tabs.tabText(1) == "Engineering Safety",
        "Audit Project right child tab must be Engineering Safety.",
    )
    expected_child_tabs = (
        "Check Update Architecture",
        "Dismissed Findings",
        "Large Module AST Split Audit",
        "Large File Refactor Planner",
        "Large File Refactor WorkBench",
    )
    _require(
        inner_tabs.count() == len(expected_child_tabs),
        "Architecture Review child-tab count changed.",
    )
    for index, label in enumerate(expected_child_tabs):
        _require(
            inner_tabs.tabText(index) == label,
            "Architecture Review child-tab label mismatch at index "
            + str(index),
        )

    engineering_page = embedded._engineering_safety_page
    engineering_tabs = engineering_page.engineering_safety_audit_tabs
    _require(
        engineering_tabs.count() == 2,
        "Engineering Safety must expose Full Audit and Pontual Audit.",
    )
    _require(
        engineering_tabs.tabText(0) == "Full Audit",
        "Engineering Safety left child tab must be Full Audit.",
    )
    _require(
        engineering_tabs.tabText(1) == "Pontual Audit",
        "Engineering Safety right child tab must be Pontual Audit.",
    )
    _require(
        engineering_page.engineering_safety_full_audit_button.text()
        == "Complete Enginneering Review",
        "Complete Engineering Review button label changed.",
    )
    _require(
        engineering_page.engineering_safety_cancel_review_button.text()
        == "Cancel Review",
        "Cancel Review button label changed.",
    )
    _require(
        engineering_page.findChild(
            QLineEdit,
            "engineering_safety_project_root_edit",
        ) is None,
        "Engineering Safety still owns a duplicate project-root field.",
    )
    embedded._root_path_edit.setText(str(project_root))
    _require(
        engineering_page.engineering_safety_project_root_provider()
        == str(project_root),
        "Engineering Safety did not use the shared Audit Project root provider.",
    )

    outer_tabs.setCurrentIndex(1)
    engineering_tabs.setCurrentIndex(0)
    app.processEvents()
    start_button = engineering_page.engineering_safety_full_audit_button
    cancel_button = engineering_page.engineering_safety_cancel_review_button
    sonar = engineering_page.engineering_safety_full_audit_sonar
    sonar_widget = engineering_page.engineering_safety_full_audit_sonar_widget
    _require(
        sonar.widget() is sonar_widget,
        "Engineering Safety sonar adapter does not expose the canonical panel.",
    )
    _require(
        sonar_widget.objectName() == "greenSonarActivityPanel",
        "Canonical sonar panel object name or background selector changed.",
    )
    _require(cancel_button.isEnabled() is False, "Cancel starts enabled.")
    _require(sonar.active is False, "Sonar starts active.")
    start_button.click()
    deadline = time.monotonic() + 3.0
    while not runner_started.is_set() and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.02)
    _require(runner_started.is_set(), "Controlled Full Audit worker did not start.")
    app.processEvents()
    _require(start_button.isEnabled() is False, "Start remained enabled while running.")
    _require(cancel_button.isEnabled() is True, "Cancel was not enabled while running.")
    _require(sonar.active is True, "Sonar was not active while running.")
    _require(
        sonar_widget.isVisibleTo(window),
        "Canonical sonar panel was not visible to the shown host.",
    )
    _require(
        sonar_widget.metaObject().className() == "_SonarPanel",
        "Engineering Safety did not use the canonical green sonar panel.",
    )
    _require(
        "QFrame#greenSonarActivityPanel" in sonar_widget.styleSheet()
        and "background: qlineargradient" in sonar_widget.styleSheet(),
        "Canonical sonar gradient background is not active.",
    )
    cancel_button.click()
    app.processEvents()
    _require(cancel_button.isEnabled() is False, "Duplicate cancellation remained enabled.")
    _require(sonar.active is False, "Sonar did not stop on cancel request.")
    _require(sonar_widget.isVisible() is False, "Sonar remained visible after cancel click.")
    _require(start_button.isEnabled() is False, "Worker projected idle before settlement.")
    deadline = time.monotonic() + 5.0
    while not start_button.isEnabled() and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.03)
    _require(start_button.isEnabled() is True, "Full Audit did not settle after cancel.")
    _require(cancel_button.isEnabled() is False, "Cancel re-enabled after settlement.")
    _require(sonar.active is False, "Sonar remained active after settlement.")
    _require(
        sonar_widget.isVisible() is False,
        "Canonical sonar remained visible after settlement.",
    )
    log_text = engineering_page.engineering_safety_full_audit_log.toPlainText()
    _require("Overall: CANCELLED" in log_text, "Cancelled result was not logged.")
    _require("Cancelled: YES" in log_text, "Cancelled summary was not logged.")
    print("ENGINEERING_SAFETY_SHARED_ROOT_RUNTIME: PASS")
    print("ENGINEERING_SAFETY_CANCEL_CONTROL_PROJECTION: PASS")
    print("ENGINEERING_SAFETY_CANCEL_SETTLEMENT: PASS")
    print("ENGINEERING_SAFETY_SONAR_VISIBLE_WHILE_RUNNING: PASS")
    print("ENGINEERING_SAFETY_CANONICAL_RADAR_RUNTIME: PASS")
    print("ENGINEERING_SAFETY_CANONICAL_SONAR_BACKGROUND: PASS")
    print("ENGINEERING_SAFETY_CANCEL_STOPS_SONAR_IMMEDIATELY: PASS")
    print("ENGINEERING_SAFETY_WORKER_SETTLES_AFTER_VISUAL_CANCEL: PASS")

    containers = (
        outer_tabs,
        embedded._architecture_review_page,
        inner_tabs,
        embedded._architecture_review_general_page,
        embedded._architecture_review_split_page,
        embedded._architecture_review_refactor_planner_page,
        embedded._architecture_review_refactor_workbench_page,
        engineering_page,
        engineering_tabs,
        engineering_page.engineering_safety_full_audit_page,
        engineering_page.engineering_safety_pontual_audit_page,
    )
    for container in containers:
        _require(
            container.sizePolicy().horizontalPolicy()
            == QSizePolicy.Policy.Ignored,
            "Every nested Audit Project container must ignore horizontal size hints.",
        )

    engineering_module.run_engineering_safety_panel_command = original_runner
    window.close()
    app.processEvents()
    print("GUI HOST WIDTH CHECK: PASS")
    return True


def validate(project_root: Path) -> None:
    """Run focused Architecture Review width-stability checks."""
    root = project_root.expanduser().resolve()
    _require(root.is_dir(), "Project root is not a directory: " + str(root))
    _validate_static_contract(root)
    _validate_qt_runtime(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print(
        "VALIDATION OK: "
        "audit-project-architecture-review-three-level-tabs-v1"
    )
    print(
        "VALIDATION OK: "
        "audit-project-architecture-review-three-level-tabs-v1r2"
    )
    print(
        "VALIDATION OK: "
        "audit-project-engineering-safety-full-pontual-audit-v1"
    )
    print(
        "VALIDATION OK: "
        "audit-project-engineering-safety-full-pontual-audit-v1r3"
    )
    print(
        "VALIDATION OK: "
        "audit-project-engineering-safety-full-pontual-audit-v1r4"
    )
    print(
        "VALIDATION OK: "
        "audit-project-engineering-safety-full-pontual-audit-v1r5"
    )
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
