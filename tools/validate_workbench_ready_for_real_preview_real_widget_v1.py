# project-path: tools/validate_workbench_ready_for_real_preview_real_widget_v1.py
"""Real-widget proof for READY_FOR_REAL_PREVIEW button projection."""
from __future__ import annotations

import os
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPushButton

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui import (
    _sync_workbench_buttons,
)

FEATURE_ID = "workbench-patch5-executor-proof-status-projection-v1"


def main() -> int:
    app = QApplication.instance() or QApplication([])
    window = SimpleNamespace()
    window._large_file_refactor_workbench_state = "READY_FOR_REAL_PREVIEW"
    window._large_file_refactor_workbench_intake = SimpleNamespace(
        status="plan_intake_ready",
        ready_for_real_preview=True,
        source_hash_fresh=True,
    )
    window._large_file_refactor_workbench_dependency_readiness = None
    window._large_file_refactor_workbench_real_preview = None
    window._large_file_refactor_workbench_structural_validation = None
    window._large_file_refactor_workbench_advanced_quality_review = None
    window._large_file_refactor_workbench_preflight_backup = None
    window._large_file_refactor_workbench_source_payload = None
    window._large_file_refactor_workbench_completion_evidence = None
    window._large_file_refactor_workbench_completion_transaction = None
    window._large_file_refactor_workbench_completion_apply_outcome = None
    window._large_file_refactor_workbench_correction_controls = {}

    attrs = (
        "_large_file_refactor_workbench_dependency_button",
        "_large_file_refactor_workbench_real_preview_button",
        "_large_file_refactor_workbench_validate_button",
        "_large_file_refactor_workbench_preflight_button",
        "_large_file_refactor_workbench_source_payload_button",
        "_large_file_refactor_workbench_completion_prepare_button",
    )
    for attr in attrs:
        setattr(window, attr, QPushButton(attr))

    _sync_workbench_buttons(window)
    app.processEvents()

    assert window._large_file_refactor_workbench_dependency_button.isEnabled()
    print("READY_FOR_REAL_PREVIEW_REAL_WIDGET_DEPENDENCY_ACTION_ENABLED: PASS")

    for attr in attrs[1:]:
        assert not getattr(window, attr).isEnabled(), attr
    print("READY_FOR_REAL_PREVIEW_REAL_WIDGET_DOWNSTREAM_STAGES_CLOSED: PASS")

    print("WORKBENCH_READY_FOR_REAL_PREVIEW_REAL_WIDGET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
