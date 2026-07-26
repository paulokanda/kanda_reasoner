"""Validate Architecture Review AST split target-row overlap containment."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

FEATURE_ID = "architecture-review-ast-split-target-overlap-v1"
SOURCE_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    return parser.parse_args()


def _require(text: str, marker: str, message: str) -> None:
    if marker not in text:
        raise RuntimeError(message)


def _validate_source(project_root: Path) -> None:
    source_path = project_root / SOURCE_RELATIVE
    if not source_path.is_file():
        raise RuntimeError(f"Source file missing: {source_path}")

    source = source_path.read_text(encoding="utf-8")
    physical_lines = len(source.splitlines())
    if physical_lines > 500:
        raise RuntimeError(
            f"Module size gate failed: {SOURCE_RELATIVE} has {physical_lines} lines"
        )

    _require(
        source,
        "target_row.addWidget(window._large_module_target_edit, stretch=1)",
        "Target path edit is not owned by the dedicated target row.",
    )
    _require(
        source,
        "page_layout.addLayout(target_row)",
        "Dedicated target row is not attached to the split-audit page.",
    )
    _require(
        source,
        "target_actions_row.addWidget(window._large_module_target_count_label)",
        "Large-module counter is not owned by the separate actions row.",
    )
    _require(
        source,
        "page_layout.addLayout(target_actions_row)",
        "Dedicated target actions row is not attached to the split-audit page.",
    )
    _require(
        source,
        "_contain_subtab_horizontal_size_pressure(window)",
        "Existing Architecture Review host-width containment is not preserved.",
    )
    if "split_header.addWidget(window._large_module_target_count_label)" in source:
        raise RuntimeError(
            "Regression: large-module counter remains in the old shared target row."
        )

    print("TARGET_PATH_ROW: SEPARATE")
    print("MODULE_COUNTER_ROW: SEPARATE")
    print("OVERLAP_GUARD: PRESENT")
    print("HOST_WIDTH_CONTAINMENT: PRESERVED")
    print("MODULE_SIZE_GATE: PASS")


def _validate_gui_if_available(project_root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QPoint, QRect
        from PySide6.QtWidgets import QApplication
    except ModuleNotFoundError:
        print("GUI TARGET COUNT OVERLAP CHECK: SKIPPED_NO_PYSIDE6")
        return

    sys.path.insert(0, str(project_root))
    from kanda_reasoner_app.manage_architecture import architecture_review_subtabs

    class _DummyWindow:
        def copy_large_module_target_path_to_clipboard(self) -> None:
            return None

        def _move_large_module_target(self, _step: int) -> None:
            return None

        def browse_large_module_target(self) -> None:
            return None

        def run_large_module_split_audit_from_gui(self) -> None:
            return None

        def copy_large_module_split_handoff(self) -> None:
            return None

        def _sync_large_module_target_controls(self) -> None:
            return None

    app = QApplication.instance() or QApplication([])
    window = _DummyWindow()
    page = architecture_review_subtabs._build_split_audit_page(window)
    page.resize(900, 640)
    page.show()
    app.processEvents()

    edit = window._large_module_target_edit
    counter = window._large_module_target_count_label
    edit_top_left = edit.mapTo(page, QPoint(0, 0))
    counter_top_left = counter.mapTo(page, QPoint(0, 0))
    edit_rect = QRect(edit_top_left, edit.size())
    counter_rect = QRect(counter_top_left, counter.size())

    if edit_rect.intersects(counter_rect):
        raise RuntimeError(
            "GUI overlap regression: target path edit intersects large-module counter."
        )
    if counter_rect.top() <= edit_rect.bottom():
        raise RuntimeError(
            "GUI row separation failed: large-module counter is not below target path row."
        )

    page.close()
    app.processEvents()
    print("GUI TARGET COUNT OVERLAP CHECK: PASS")


def main() -> int:
    args = _parse_args()
    project_root = Path(args.project_root).resolve()
    _validate_source(project_root)
    _validate_gui_if_available(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
