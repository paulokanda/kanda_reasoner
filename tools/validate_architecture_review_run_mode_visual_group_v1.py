#!/usr/bin/env python3
"""Validate the cosmetic Architecture Review Run options/Mode grouping."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path

FEATURE_ID = "architecture-review-run-mode-visual-group-v1"
SOURCE = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
MAX_LINES = 500

__all__ = ["main"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(root: Path) -> str:
    return (root / SOURCE).read_text(encoding="utf-8-sig")


def validate_static(root: Path) -> None:
    source = _read(root)
    ast.parse(source, filename=str(root / SOURCE))
    _require(
        len(source.splitlines()) <= MAX_LINES,
        f"{SOURCE.as_posix()} exceeds {MAX_LINES} physical lines",
    )
    _require(
        'window._run_options_toolbar_label = QLabel("Run options")' in source,
        "Run options label changed or disappeared",
    )
    _require(
        'window._mode_toolbar_label = QLabel("Mode")' in source,
        "Mode label changed or disappeared",
    )
    _require(
        'window._run_mode_selector_widget = QWidget(' in source
        and '"architecture_review_run_mode_selector_group"' in source,
        "Run options/Mode visual group is missing",
    )
    expected_group_order = (
        "run_mode_selector_layout.addWidget(window._run_options_toolbar_label)\n"
        "    run_mode_selector_layout.addWidget(window._mode_toolbar_label)\n"
        "    run_mode_selector_layout.addWidget(window._mode_combo)"
    )
    _require(
        expected_group_order in source,
        "Run options, Mode, and the dropdown are not grouped in the requested order",
    )
    _require(
        "run_options_layout.addWidget(window._run_mode_selector_widget)" in source,
        "Grouped Run options/Mode selector is not installed in the existing toolbar row",
    )
    for forbidden in (
        "run_options_layout.addWidget(window._run_options_toolbar_label)",
        "run_options_layout.addWidget(window._mode_toolbar_label)",
        "run_options_layout.addWidget(window._mode_combo)",
    ):
        _require(forbidden not in source, "Ungrouped legacy placement remains: " + forbidden)
    _require(
        'window._mode_combo.addItems(["validate", "diff", "scan", "write"])'
        in source,
        "Architecture Review technical modes changed",
    )
    _require(
        "bind_mode_action_button(window._mode_combo, window._run_button)" in source,
        "Mode-to-action label binding changed",
    )
    _require(
        'window._strict_write_checkbox = QCheckBox("Require confirm before write")'
        in source
        and "window._strict_write_checkbox.setChecked(True)" in source,
        "Write confirmation control changed",
    )
    _require(
        "window._run_button.clicked.connect(window.run_selected_mode)" in source,
        "Run behavior connection changed",
    )
    _require(
        "window._cancel_operation_button.clicked.connect(window.cancel_running_operation)"
        in source,
        "Cancel behavior connection changed",
    )
    _require(
        "install_ai_controls(window, run_options_layout)" in source,
        "Architecture Review AI controls installation changed",
    )
    print("ARCHITECTURE_RUN_OPTIONS_AND_MODE_GROUPED: PASS")
    print("ARCHITECTURE_MODE_DROPDOWN_OPTIONS_UNCHANGED: PASS")
    print("ARCHITECTURE_RUN_CANCEL_CONFIRM_BEHAVIOR_UNCHANGED: PASS")
    print("ARCHITECTURE_AI_CONTROLS_UNCHANGED: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def _is_missing_pyside6_dependency(exc: ImportError) -> bool:
    """Return True only for an unavailable PySide6 or shiboken6 dependency."""
    module_name = str(getattr(exc, "name", "") or "")
    message = str(exc)
    return (
        module_name == "PySide6"
        or module_name.startswith("PySide6.")
        or module_name == "shiboken6"
        or module_name.startswith("shiboken6.")
        or "PySide6" in message
        or "shiboken6" in message
    )


def validate_real_qt(root: Path) -> bool:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        if not _is_missing_pyside6_dependency(exc):
            raise
        print("REAL_QT_ARCHITECTURE_RUN_MODE_GROUP: SKIPPED_NO_PYSIDE6")
        return False

    import sys

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.manage_architecture.architecture_review_subtabs import (
        _build_general_audit_page,
    )

    class FakeWindow:
        def __init__(self) -> None:
            self.run_selected_mode = lambda: None
            self.cancel_running_operation = lambda: None
            self.save_output = lambda: None
            self.show_mode_help = lambda: None
            self.copy_audit_to_clipboard = lambda: None
            self.run_warning_heuristic_resolver = lambda: None
            self.run_warning_model_resolver = lambda: None
            self.run_warning_web_ai_resolver = lambda: None
            self.copy_large_module_protocol_to_clipboard = lambda: None

    app = QApplication.instance() or QApplication([])
    window = FakeWindow()
    page = _build_general_audit_page(window, lambda _window, _layout: None)
    app.processEvents()

    group = window._run_mode_selector_widget
    group_layout = group.layout()
    _require(group.objectName() == "architecture_review_run_mode_selector_group", "Wrong group object name")
    _require(group_layout is not None and group_layout.count() == 3, "Visual group must contain exactly three controls")
    _require(group_layout.itemAt(0).widget() is window._run_options_toolbar_label, "Run options label is not first")
    _require(group_layout.itemAt(1).widget() is window._mode_toolbar_label, "Mode label is not second")
    _require(group_layout.itemAt(2).widget() is window._mode_combo, "Mode dropdown is not third")
    _require(window._run_options_toolbar_label.parentWidget() is group, "Run options label is outside the group")
    _require(window._mode_toolbar_label.parentWidget() is group, "Mode label is outside the group")
    _require(window._mode_combo.parentWidget() is group, "Mode dropdown is outside the group")
    _require(
        [window._mode_combo.itemText(i) for i in range(window._mode_combo.count())]
        == ["validate", "diff", "scan", "write"],
        "Runtime mode choices changed",
    )
    _require(window._strict_write_checkbox.isChecked(), "Write confirmation default changed")
    print("REAL_QT_ARCHITECTURE_RUN_MODE_GROUP: PASS")

    expected = {
        "validate": "Validate Project",
        "diff": "Preview Changes",
        "scan": "Scan Project",
        "write": "Write Architecture Files",
    }
    for mode, label in expected.items():
        window._mode_combo.setCurrentText(mode)
        app.processEvents()
        _require(window._run_button.text() == label, f"Action label changed for {mode}")
    print("REAL_QT_ARCHITECTURE_MODE_ACTION_SYNC: PASS")

    page.close()
    page.deleteLater()
    for _ in range(4):
        app.processEvents()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    print("REAL_QT_ARCHITECTURE_RUN_MODE_TEARDOWN_CLEAN: PASS")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    validate_static(root)
    validate_real_qt(root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
