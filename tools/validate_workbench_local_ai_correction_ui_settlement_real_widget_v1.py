"""Real Qt validation for Local AI correction settlement control projection."""
from __future__ import annotations

import os
import sys
import time
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLineEdit, QWidget

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.docstring_planner import (
    build_docstring_proposals,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    PlannerSettings,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_bounded_refinement import (
    attach_docstring_proposals_to_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    initialize_planner_version_state,
    select_planner_version,
    store_heuristic_version,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
    build_split_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_gui,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_local_ai_correction_qt_controller as controller,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_local_ai_correction_qt_worker as worker_module,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_local_ai_correction_models import (
    LocalAIWorkbenchCorrectionCandidate,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_snapshot_bridge import (
    load_latest_snapshot_into_workbench,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_aqr_correction_session import (
    current_aqr_correction_session,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_gui import (
    sync_workbench_stage_correction_controls,
)

FEATURE_ID = "workbench-local-ai-correction-ui-settlement-projection-repair-v1"


def _pump_until(app: QApplication, predicate, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("Qt settlement predicate did not complete")


def main() -> None:
    app = QApplication.instance() or QApplication([])
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    assert target.is_file(), "CONTROLLED_RUNTIME_TARGET_MISSING"

    class TestWindow(QWidget):
        pass

    window = TestWindow()
    window._root_path_edit = QLineEdit(str(ROOT), window)
    page = workbench_gui.build_large_file_refactor_workbench_page(window)
    page.setParent(window)
    initialize_planner_version_state(window)

    report = analyze_python_file(target)
    plan = build_split_plan(report, PlannerSettings(), source_path=None)
    proposals = build_docstring_proposals(report, plan)
    plan = attach_docstring_proposals_to_plan(plan, proposals)

    window._large_file_refactor_last_analysis = report
    window._large_file_refactor_planner_candidates = [
        SimpleNamespace(path=str(target))
    ]
    store_heuristic_version(window, plan, proposals)
    select_planner_version(window, PLANNER_VERSION_HEURISTIC)

    intake, message = load_latest_snapshot_into_workbench(window, str(ROOT))
    assert intake is not None and intake.ready_for_real_preview, message
    workbench_gui._store_and_render_intake(window, intake)

    failed_value = SimpleNamespace(value="FAILED")
    indeterminate_value = SimpleNamespace(value="INDETERMINATE")
    window._large_file_refactor_workbench_advanced_quality_review = SimpleNamespace(
        run_record=SimpleNamespace(execution_status=failed_value),
        cross_check_report=SimpleNamespace(
            quality_decision=indeterminate_value,
            rule_results=(),
        ),
    )
    window._large_file_refactor_workbench_aqr_stage_states = {
        "ruff": "FAILED",
    }
    window._large_file_refactor_workbench_aqr_output.setPlainText(
        "ADVANCED QUALITY REVIEW COMPLETE\nExecution status: FAILED"
    )
    sync_workbench_stage_correction_controls(
        window,
        lambda current: current._root_path_edit.text(),
    )

    controls = window._large_file_refactor_workbench_correction_controls[
        "ADVANCED_QUALITY_REVIEW"
    ]
    local_button = controls["local_ai"]
    assert local_button.isEnabled(), "LOCAL_AI_CORRECTION_BUTTON_NOT_ENABLED"

    original_builder = (
        worker_module.build_bounded_local_ai_workbench_correction_candidate
    )
    material_plan = replace(
        plan,
        risks=list(plan.risks) + ["CONTROLLED_REAL_WIDGET_MATERIAL_CHANGE"],
    )

    def controlled_builder(**_kwargs):
        return LocalAIWorkbenchCorrectionCandidate(
            ok=True,
            message="controlled materially changed Local AI candidate",
            report=report,
            corrected_plan=material_plan,
            proposals=tuple(proposals),
            review_status="validated",
            corrections_applied=1,
            model_name="controlled",
        )

    worker_module.build_bounded_local_ai_workbench_correction_candidate = (
        controlled_builder
    )
    try:
        local_button.click()
        _pump_until(
            app,
            lambda: not controller.local_ai_execution_state(window).waiting,
        )
        _pump_until(
            app,
            lambda: not controller.local_ai_execution_state(
                window
            ).background_job_alive,
        )
        app.processEvents()

        assert (
            window._large_file_refactor_workbench_state
            == "READY_FOR_REAL_PREVIEW"
        )
        print("LOCAL_AI_ACCEPTED_RESULT_RETURNS_READY_FOR_REAL_PREVIEW: PASS")

        dependency_button = (
            window._large_file_refactor_workbench_dependency_button
        )
        assert dependency_button.isEnabled(), (
            "DEPENDENCY_READINESS_BUTTON_NOT_RESTORED_AFTER_LOCAL_AI_SUCCESS"
        )
        print("LOCAL_AI_SETTLEMENT_RESTORES_DEPENDENCY_READINESS_BUTTON: PASS")

        assert not window._large_file_refactor_workbench_real_preview_button.isEnabled()
        assert not window._large_file_refactor_workbench_validate_button.isEnabled()
        assert not window._large_file_refactor_workbench_aqr_run_button.isEnabled()
        assert not window._large_file_refactor_workbench_preflight_button.isEnabled()
        print("LOCAL_AI_SETTLEMENT_PRESERVES_SEQUENTIAL_DOWNSTREAM_GATES: PASS")

        session = current_aqr_correction_session(window)
        assert session is not None, "AQR_CORRECTION_SESSION_RETIRED_BEFORE_FRESH_PASS"
        print("LOCAL_AI_SETTLEMENT_PRESERVES_AQR_CORRECTION_SESSION: PASS")

        assert local_button.isEnabled()
        assert controls["heuristic"].isEnabled()
        assert controls["web_copy"].isEnabled()
        assert controls["web_receive"].isEnabled()
        print("LOCAL_AI_SETTLEMENT_PRESERVES_REUSABLE_CORRECTION_ROUTES: PASS")

        monitor = getattr(
            window,
            "_workbench_local_ai_correction_sonar_monitor",
            None,
        )
        assert monitor is not None
        assert not monitor._timer.isActive()
        print("LOCAL_AI_SETTLEMENT_SONAR_AND_CONTROL_PROJECTION_AGREE: PASS")
    finally:
        worker_module.build_bounded_local_ai_workbench_correction_candidate = (
            original_builder
        )
        window.close()
        page.close()
        app.processEvents()

    print("WORKBENCH_LOCAL_AI_CORRECTION_UI_SETTLEMENT_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
