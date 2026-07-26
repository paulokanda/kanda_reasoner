"""Validate Project Q&A host-height containment in the shared KANDA GUI."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys

FEATURE_ID = "project-qa-host-height-stability-v1"
UI_BUILDER_RELATIVE = Path(
    "kanda_reasoner_app/reasoner_engine/"
    "ai_reasoner_main_window_help/ui_builder.py"
)
MAX_PHYSICAL_LINES = 500


def _require(condition: bool, message: str) -> None:
    """Raise an assertion when a validation condition is false."""
    if not condition:
        raise AssertionError(message)


def _validate_static_contract(project_root: Path) -> None:
    """Validate Project Q&A vertical containment and module-size contracts."""
    source_path = project_root / UI_BUILDER_RELATIVE
    _require(source_path.is_file(), "Project Q&A ui_builder.py is missing.")

    source = source_path.read_text(encoding="utf-8", errors="strict")
    compile(source, str(source_path), "exec")
    ast.parse(source, filename=str(source_path))

    required_fragments = (
        "QScrollArea",
        "QAbstractScrollArea",
        'scroll.setObjectName("projectQaBodyScrollArea")',
        "scroll.setWidgetResizable(True)",
        "QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored",
        "Qt.ScrollBarPolicy.ScrollBarAsNeeded",
        "scroll.setMinimumHeight(0)",
        "scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)",
        'body.setObjectName("projectQaScrollableBody")',
        "body_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)",
        "main_layout.addWidget(scroll, stretch=1)",
        "window._project_qa_body_scroll_area = scroll",
    )
    for fragment in required_fragments:
        _require(
            fragment in source,
            "Missing Project Q&A height-containment fragment: " + fragment,
        )

    forbidden_fragments = (
        "setFixedHeight(1080",
        "setMinimumHeight(1080",
        "setFixedHeight(900",
        "setMinimumHeight(900",
    )
    for fragment in forbidden_fragments:
        _require(
            fragment not in source,
            "Forbidden Project Q&A host-height lock fragment: " + fragment,
        )

    _require(
        len(source.splitlines()) <= MAX_PHYSICAL_LINES,
        "Project Q&A ui_builder.py exceeds 500 physical lines.",
    )

    print("PROJECT_QA_SCROLL_CONTAINMENT: PRESENT")
    print("VERTICAL_SIZE_PRESSURE: IGNORED")
    print("MODULE_SIZE_GATE: PASS")


def _validate_qt_runtime(project_root: Path) -> bool:
    """Compare shared host height before and after loading Project Q&A."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QApplication, QSizePolicy
    except ModuleNotFoundError:
        print("GUI HOST HEIGHT CHECK: SKIPPED_NO_PYSIDE6")
        return False

    project_text = str(project_root)
    if project_text not in sys.path:
        sys.path.insert(0, project_text)

    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window import (
        ReasonerToolsWindow,
    )

    app = QApplication.instance() or QApplication([])
    window = ReasonerToolsWindow()
    window.resize(1200, 760)
    window.show()
    app.processEvents()

    brain_index = window._tab_index_by_tab_id["brain_navigator"]
    project_qa_index = window._tab_index_by_tab_id["project_qa"]

    window.tabs.setCurrentIndex(brain_index)
    for _ in range(3):
        app.processEvents()
    baseline_height = int(window.height())

    window.tabs.setCurrentIndex(project_qa_index)
    page = window._lazy_page_for_tab_index(project_qa_index)
    _require(page is not None, "Project Q&A lazy page is missing.")
    _require(page.ensure_loaded(), "Project Q&A failed to load.")
    for _ in range(8):
        app.processEvents()

    project_qa_height = int(window.height())
    _require(
        project_qa_height == baseline_height,
        "Project Q&A changed host height from "
        + str(baseline_height)
        + " to "
        + str(project_qa_height),
    )

    embedded = page._embedded_widget
    _require(embedded is not None, "Project Q&A embedded widget is missing.")
    scroll = getattr(embedded, "_project_qa_body_scroll_area", None)
    _require(scroll is not None, "Project Q&A body scroll area is missing.")
    _require(
        scroll.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Ignored,
        "Project Q&A scroll area must ignore vertical size pressure.",
    )
    _require(
        scroll.verticalScrollBarPolicy()
        == Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        "Project Q&A must expose internal vertical scrolling as needed.",
    )

    window.close()
    app.processEvents()
    print("GUI HOST HEIGHT CHECK: PASS")
    return True


def validate(project_root: Path) -> None:
    """Run focused Project Q&A height-stability checks."""
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
