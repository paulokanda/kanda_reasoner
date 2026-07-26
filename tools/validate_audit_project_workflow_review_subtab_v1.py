# project-path: tools/validate_audit_project_workflow_review_subtab_v1.py
"""Validate Workflow Review as the rightmost Audit Project child tab."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

FEATURE_ID = "audit-project-workflow-review-subtab-v1"
EXPECTED_TABS = ["Architecture Review", "Engineering Safety", "Workflow Review"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(root: Path, relative: str) -> str:
    path = root / relative
    _require(path.is_file(), "Missing file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    subtabs = _read(
        root,
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
    )
    adapter = _read(
        root,
        "kanda_reasoner_app/manage_architecture/audit_project_workflow_review.py",
    )
    specs = _read(
        root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
    )
    mapping = _read(
        root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/_mapping_data.py",
    )

    for fragment in (
        '_AUDIT_PROJECT_WORKFLOW_REVIEW_TAB_LABEL = "Workflow Review"',
        "create_embedded_workflow_review(",
        "window._workflow_review_page",
        "window._root_path_edit.textChanged.connect",
    ):
        _require(fragment in subtabs, "Workflow subtab contract missing: " + fragment)

    architecture_index = subtabs.index("_AUDIT_PROJECT_ARCHITECTURE_TAB_LABEL")
    engineering_index = subtabs.index(
        "_AUDIT_PROJECT_ENGINEERING_SAFETY_TAB_LABEL",
        architecture_index,
    )
    workflow_index = subtabs.index(
        "_AUDIT_PROJECT_WORKFLOW_REVIEW_TAB_LABEL",
        engineering_index,
    )
    _require(
        architecture_index < engineering_index < workflow_index,
        "Audit Project child tab order changed.",
    )

    for fragment in (
        'setObjectName("audit_project_workflow_review_page")',
        'page.setWindowTitle("Workflow Review")',
        'control.setVisible(False)',
        'root_combo.setCurrentText(selected)',
    ):
        _require(fragment in adapter, "Embedding adapter missing: " + fragment)

    start = specs.index('step_title="Workflow Review"')
    end = specs.find("    ToolSpec(", start + 1)
    workflow_spec = specs[start:end]
    _require('tab_id="workflow_review"' in workflow_spec, "Workflow tab ID changed.")
    _require(
        'visible_in_shell=False' in workflow_spec,
        "Workflow Review remains visible as a duplicate top-level tab.",
    )
    _require(
        '"target_tab_id": "architecture_review"' in mapping
        and 'Audit Project > Workflow Review' in mapping,
        "Brain navigation does not route nested Workflow Review through Audit Project.",
    )
    print("AUDIT_PROJECT_WORKFLOW_REVIEW_STATIC_CONTRACT: PASS")
    print("WORKFLOW_REVIEW_TOP_LEVEL_REMOVED: PASS")
    print("WORKFLOW_REVIEW_STABLE_ID_PRESERVED: PASS")


def validate_runtime(root: Path) -> None:
    try:
        from PySide6.QtWidgets import QApplication, QSizePolicy
    except ModuleNotFoundError:
        print("AUDIT_PROJECT_WORKFLOW_REVIEW_RUNTIME: SKIPPED_NO_PYSIDE6")
        return

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    import sys

    sys.path.insert(0, str(root))
    from kanda_reasoner_app.manage_architecture.manage_architecture_gui import (
        ArchitectureManagerWindow,
    )

    app = QApplication.instance() or QApplication([])
    window = ArchitectureManagerWindow()
    window.show()
    app.processEvents()

    tabs = window._audit_project_subtab_widget
    labels = [tabs.tabText(index) for index in range(tabs.count())]
    _require(labels == EXPECTED_TABS, "Audit Project tab order mismatch: " + repr(labels))

    workflow = window._workflow_review_page
    _require(
        workflow.objectName() == "audit_project_workflow_review_page",
        "Embedded Workflow Review identity changed.",
    )
    _require(workflow.centralWidget() is not None, "Workflow Review central widget missing.")
    _require(hasattr(workflow, "_output"), "Workflow Review output panel missing.")
    for attribute in ("_root_path_label", "_root_combo", "_browse_root_btn"):
        _require(
            getattr(workflow, attribute).isHidden(),
            "Embedded Workflow Review duplicates shared root control: " + attribute,
        )

    test_root = str(root / "workflow-review-root-sync-probe")
    window._root_path_edit.setText(test_root)
    app.processEvents()
    _require(
        workflow._root_combo.currentText() == test_root,
        "Shared Audit Project root did not synchronize to Workflow Review.",
    )
    _require(
        workflow.sizePolicy().horizontalPolicy() == QSizePolicy.Ignored,
        "Workflow Review can widen the Audit Project host.",
    )
    _require(
        workflow.centralWidget().sizePolicy().horizontalPolicy()
        == QSizePolicy.Ignored,
        "Workflow Review central widget can widen the Audit Project host.",
    )

    window.close()
    app.processEvents()
    print("AUDIT_PROJECT_WORKFLOW_REVIEW_RUNTIME: PASS")
    print("WORKFLOW_REVIEW_SHARED_ROOT_RUNTIME: PASS")
    print("WORKFLOW_REVIEW_HOST_WIDTH_POLICY: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    try:
        validate_static(root)
        validate_runtime(root)
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID + " - " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
