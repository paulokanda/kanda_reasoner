"""Validate real PySide Advanced Quality Review GUI integration."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import sys
import threading
import time
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PySide6.QtCore import QTimer  # noqa: E402
from PySide6.QtWidgets import QApplication, QWidget  # noqa: E402

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import advanced_quality_review_qt_worker as worker_module  # noqa: E402
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (  # noqa: E402
    AnalysisExecutionStatus,
    QualityDecision,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_gui import (  # noqa: E402
    build_advanced_quality_review_section,
    invalidate_advanced_quality_review_gui,
    sync_advanced_quality_review_controls,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_gui_context import (  # noqa: E402
    prepare_advanced_quality_review_gui_run,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_orchestration import (  # noqa: E402
    AdvancedQualityReviewOutcome,
    AdvancedQualityReviewStage,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui_progression import (  # noqa: E402
    build_workbench_gui_progression,
)

FEATURE_ID = "advanced-quality-review-real-gui-integration-v1"
_VALIDATOR_TIMEOUT_SECONDS = 600
STAGES = (
    AdvancedQualityReviewStage.ENVIRONMENT_PREFLIGHT,
    AdvancedQualityReviewStage.RUFF,
    AdvancedQualityReviewStage.API_REVIEW,
    AdvancedQualityReviewStage.IMPORT_GRAPH,
    AdvancedQualityReviewStage.TYPE_REVIEW,
    AdvancedQualityReviewStage.DEAD_CODE,
    AdvancedQualityReviewStage.DELTA,
    AdvancedQualityReviewStage.CROSS_CHECK,
    AdvancedQualityReviewStage.PERSISTENCE,
)


def main() -> None:
    _start_watchdog()
    _print_stage("AQR_REAL_WIDGET_STAGE_START: QApplication")
    app = QApplication.instance() or QApplication([])
    _print_stage("AQR_REAL_WIDGET_STAGE_PASS: QApplication")
    project, preview_root, window = _fixture()
    source_before = (project / "pkg" / "mod.py").read_bytes()
    context = prepare_advanced_quality_review_gui_run(
        window,
        active_project_root=str(project),
        tool_root=str(ROOT),
    )
    daily = project.parent / (project.name + "_delete_after_daily_work")
    assert Path(context.baseline_view_root).is_relative_to(daily)
    assert Path(context.preview_view_root).is_relative_to(daily)
    assert not Path(context.baseline_view_root).is_relative_to(project)
    assert context.request.analysis_identity.baseline_hash != context.request.analysis_identity.preview_hash
    assert context.package_name == "pkg"
    assert (project / "pkg" / "mod.py").read_bytes() == source_before
    print("AQR_GUI_ANALYSIS_VIEWS_DAILY_WORK_ONLY: PASS")
    print("AQR_GUI_VIEW_PREPARATION_SOURCE_IMMUTABLE: PASS")

    _validate_progression(window)
    _validate_real_widgets(app, window, project)
    _validate_sources()
    print("ADVANCED_QUALITY_REVIEW_REAL_GUI_INTEGRATION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def _fixture():
    root = ROOT.parent / (ROOT.name + "_delete_after_daily_work") / "aqr_gui_fixture"
    if root.exists():
        shutil.rmtree(root)
    project = root / "sample_project"
    (project / "pkg").mkdir(parents=True)
    (project / "pkg" / "__init__.py").write_text("from .mod import add\n", encoding="utf-8")
    (project / "pkg" / "mod.py").write_text(
        '"""Baseline module."""\n\ndef add(a: int, b: int) -> int:\n    return a + b\n',
        encoding="utf-8",
    )
    support = project.parent / (project.name + "_show_project_to_AI")
    preview_root = support / "large_file_refactor_workbench" / "preview" / "p1"
    preview_root.mkdir(parents=True)
    (preview_root / "mod.py").write_text(
        '"""Preview module."""\n\ndef add(a: int, b: int) -> int:\n    return a + b\n',
        encoding="utf-8",
    )
    snapshot = SimpleNamespace(
        snapshot_hash="card-identity-001",
        plan_json='{"target_file":"pkg/mod.py","strategy":"split"}',
        integrity_valid=lambda: True,
    )
    intake = SimpleNamespace(
        status="plan_intake_ready",
        source_hash_fresh=True,
        target_file=str(project / "pkg" / "mod.py"),
        snapshot_hash=snapshot.snapshot_hash,
    )
    preview = SimpleNamespace(
        status="real_preview_written",
        preview_root=str(preview_root),
        blockers=(),
        files=(SimpleNamespace(relative_path="mod.py"),),
    )
    structural = SimpleNamespace(status="passed", blockers=())
    window = QWidget()
    window._large_file_refactor_workbench_plan_snapshot = snapshot
    window._large_file_refactor_workbench_intake = intake
    window._large_file_refactor_workbench_real_preview = preview
    window._large_file_refactor_workbench_structural_validation = structural
    return project, preview_root, window


def _validate_progression(window) -> None:
    structural = build_workbench_gui_progression(
        intake=window._large_file_refactor_workbench_intake,
        dependency_readiness=SimpleNamespace(
            status="dependency_readiness_ready",
            ready_for_real_preview_writer=True,
        ),
        preview=SimpleNamespace(
            status="real_preview_written",
            files=(1,),
            written_files=(1,),
            blockers=(),
        ),
        structural_validation=window._large_file_refactor_workbench_structural_validation,
    )
    assert structural.advanced_quality_review_enabled
    assert not structural.preflight_enabled
    outcome = _outcome("identity")
    ready = build_workbench_gui_progression(
        intake=window._large_file_refactor_workbench_intake,
        dependency_readiness=SimpleNamespace(
            status="dependency_readiness_ready",
            ready_for_real_preview_writer=True,
        ),
        preview=SimpleNamespace(status="real_preview_written", files=(1,), written_files=(1,), blockers=()),
        structural_validation=window._large_file_refactor_workbench_structural_validation,
        advanced_quality_review=outcome,
    )
    assert ready.preflight_enabled
    print("STRUCTURAL_TO_AQR_TO_PREFLIGHT_PROGRESSION: PASS")


def _validate_real_widgets(app, window, project: Path) -> None:
    sync_calls = []

    def project_controls(target_window) -> None:
        progression = build_workbench_gui_progression(
            intake=target_window._large_file_refactor_workbench_intake,
            dependency_readiness=SimpleNamespace(
                status="dependency_readiness_ready",
                ready_for_real_preview_writer=True,
            ),
            preview=SimpleNamespace(
                status="real_preview_written",
                files=(1,),
                written_files=(1,),
                blockers=(),
            ),
            structural_validation=(
                target_window._large_file_refactor_workbench_structural_validation
            ),
            advanced_quality_review=getattr(
                target_window,
                "_large_file_refactor_workbench_advanced_quality_review",
                None,
            ),
        )
        sync_advanced_quality_review_controls(target_window, progression)
        sync_calls.append("sync")

    section = build_advanced_quality_review_section(
        window,
        root_text_callback=lambda _window: str(project),
        sync_callback=project_controls,
    )
    section.show()
    app.processEvents()

    original_build = worker_module.build_pinned_review_execution_plan
    original_run = worker_module.run_advanced_quality_review
    worker_module.build_pinned_review_execution_plan = lambda request: SimpleNamespace()

    def fake_run(request, plan, *, cancellation_token, progress_callback):
        for stage in STAGES:
            if cancellation_token.cancelled:
                raise RuntimeError("CONTROLLED_CANCELLED")
            progress_callback(stage, "START")
            time.sleep(0.015)
            progress_callback(stage, "PASS")
        return _outcome(request.analysis_identity.identity_hash)

    worker_module.run_advanced_quality_review = fake_run
    heartbeat = {"count": 0}
    timer = QTimer()
    timer.timeout.connect(lambda: heartbeat.__setitem__("count", heartbeat["count"] + 1))
    timer.start(5)
    try:
        _print_stage("AQR_REAL_WIDGET_STAGE_START: success_generation")
        window._large_file_refactor_workbench_aqr_run_button.setEnabled(True)
        window._large_file_refactor_workbench_aqr_run_button.click()
        _wait_until(app, lambda: _controller_idle(window))
        assert heartbeat["count"] >= 3
        assert window._large_file_refactor_workbench_advanced_quality_review is not None
        text = window._large_file_refactor_workbench_aqr_progress_output.toPlainText()
        assert all(stage + ": PASS" in text for stage in STAGES)
        assert window._large_file_refactor_workbench_aqr_progress_bar.value() == len(STAGES)
        print("AQR_REAL_PYSIDE_EVENT_LOOP_RESPONSIVE: PASS")
        print("AQR_VISIBLE_NINE_STAGE_PROGRESS: PASS")
        _print_stage("AQR_REAL_WIDGET_STAGE_PASS: success_generation")

        _print_stage("AQR_REAL_WIDGET_STAGE_START: cancel_generation")
        invalidate_advanced_quality_review_gui(window, "CONTROLLED_CANCEL_TEST")
        window._large_file_refactor_workbench_aqr_run_button.setEnabled(True)
        window._large_file_refactor_workbench_aqr_run_button.click()
        _wait_until(app, lambda: window._large_file_refactor_workbench_aqr_controller.state().running)
        assert window._large_file_refactor_workbench_aqr_cancel_button.isEnabled()
        print("AQR_REAL_WIDGET_CONTROL_PROJECTION_PRODUCTION_PATH: PASS")
        window._large_file_refactor_workbench_aqr_cancel_button.click()
        cancel_state = window._large_file_refactor_workbench_aqr_controller.state()
        assert cancel_state.running
        assert cancel_state.cancel_requested
        assert not window._large_file_refactor_workbench_aqr_cancel_button.isEnabled()
        print("AQR_CANCEL_RUNNING_UNTIL_THREAD_SETTLED: PASS")
        _wait_until(app, lambda: _controller_idle(window))
        app.processEvents()
        settled_state = window._large_file_refactor_workbench_aqr_controller.state()
        assert not settled_state.running
        assert settled_state.cancel_requested
        assert window._large_file_refactor_workbench_advanced_quality_review is None
        assert "cancellation requested" in window._large_file_refactor_workbench_aqr_output.toPlainText().lower()
        print("AQR_GUI_CANCEL_FAILS_CLOSED: PASS")
        print("AQR_GUI_CANCEL_LATE_RESULT_DISCARDED: PASS")
        _print_stage("AQR_REAL_WIDGET_STAGE_PASS: cancel_generation")
    finally:
        timer.stop()
        controller = getattr(
            window,
            "_large_file_refactor_workbench_aqr_controller",
            None,
        )
        if controller is not None and controller.state().running:
            controller.cancel()
            _wait_until(app, lambda: _controller_idle(window))
        worker_module.build_pinned_review_execution_plan = original_build
        worker_module.run_advanced_quality_review = original_run
        section.close()
        app.processEvents()


def _outcome(identity_hash: str) -> AdvancedQualityReviewOutcome:
    report = SimpleNamespace(
        quality_decision=QualityDecision.PASS,
        rule_results=(),
    )
    record = SimpleNamespace(
        execution_status=AnalysisExecutionStatus.SUCCEEDED,
        run_id="controlled-run",
    )
    receipt = SimpleNamespace(run_root="controlled/project-support/evidence")
    return AdvancedQualityReviewOutcome(
        analysis_identity_hash=identity_hash,
        cross_check_report=report,
        run_record=record,
        persistence_receipt=receipt,
        ruff=None,
        griffe=None,
        grimp=None,
        mypy=None,
        vulture=None,
    )



def _print_stage(marker: str) -> None:
    print(marker, flush=True)


def _start_watchdog() -> None:
    def watchdog() -> None:
        time.sleep(_VALIDATOR_TIMEOUT_SECONDS)
        _print_stage("AQR_REAL_WIDGET_VALIDATOR_TIMEOUT")
        os._exit(124)

    threading.Thread(
        target=watchdog,
        name="aqr-real-widget-validator-watchdog",
        daemon=True,
    ).start()


def _controller_idle(window) -> bool:
    controller = window._large_file_refactor_workbench_aqr_controller
    if controller.state().running:
        return False
    jobs = getattr(controller, "_jobs", {})
    return not any(job.get("thread") and job["thread"].isRunning() for job in jobs.values())

def _wait_until(app, predicate, timeout: float = 8.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return
        time.sleep(0.005)
    raise AssertionError("AQR_GUI_WAIT_TIMEOUT")


def _validate_sources() -> None:
    package = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
    touched = (
        package / "advanced_quality_review_gui_context.py",
        package / "advanced_quality_review_gui_formatting.py",
        package / "advanced_quality_review_gui.py",
        package / "advanced_quality_review_qt_worker.py",
        package / "advanced_quality_review_qt_controller.py",
        package / "workbench_gui_progression.py",
        package / "workbench_gui.py",
        package / "workbench_completion_gui.py",
        Path(__file__).resolve(),
    )
    for path in touched:
        data = path.read_bytes()
        data.decode("ascii")
        assert not data.startswith(b"\xef\xbb\xbf")
        lines = len(data.decode("ascii").splitlines())
        assert lines <= 500, f"MODULE_TOO_LARGE:{path}:{lines}"
    orchestration = (package / "advanced_quality_review_orchestration.py").read_text(encoding="ascii")
    assert "PySide6" not in orchestration
    print("AQR_GUI_SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("AQR_GUI_TOUCHED_MODULES_MAX_500: PASS")
    print("PURE_ORCHESTRATION_REMAINS_GUI_FREE: PASS")


if __name__ == "__main__":
    main()
