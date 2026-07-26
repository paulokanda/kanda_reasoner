"""Validate Advanced Quality Review GUI integration without importing PySide6."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PACKAGE = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_gui_context import prepare_advanced_quality_review_gui_run
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui_progression import build_workbench_gui_progression

FEATURE_ID = "advanced-quality-review-gui-integration-contract-v1"


def main() -> None:
    _validate_context_views()
    _validate_progression()
    _validate_gui_source_contract()
    _validate_worker_bootstrap_contract()
    _validate_cancel_lifecycle_contract()
    _validate_sizes_and_encoding()
    print("ADVANCED_QUALITY_REVIEW_GUI_CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def _validate_context_views() -> None:
    fixture = ROOT.parent / (ROOT.name + "_delete_after_daily_work") / "aqr_gui_contract_fixture"
    if fixture.exists():
        shutil.rmtree(fixture)
    project = fixture / "sample_project"
    target = project / "pkg/mod.py"
    target.parent.mkdir(parents=True)
    target.write_text('"""Baseline."""\n\ndef value() -> int:\n    return 1\n', encoding="utf-8")
    (project / "pkg/__init__.py").write_text("from .mod import value\n", encoding="utf-8")
    support = project.parent / (project.name + "_show_project_to_AI")
    preview_root = support / "large_file_refactor_workbench/preview/p1"
    preview_root.mkdir(parents=True)
    (preview_root / "mod.py").write_text('"""Preview."""\n\ndef value() -> int:\n    return 2\n', encoding="utf-8")
    snapshot = SimpleNamespace(
        snapshot_hash="card-001",
        plan_json='{"target_file":"pkg/mod.py"}',
        integrity_valid=lambda: True,
    )
    window = SimpleNamespace(
        _large_file_refactor_workbench_plan_snapshot=snapshot,
        _large_file_refactor_workbench_intake=SimpleNamespace(
            status="plan_intake_ready",
            source_hash_fresh=True,
            target_file=str(target),
            snapshot_hash="card-001",
        ),
        _large_file_refactor_workbench_real_preview=SimpleNamespace(
            status="real_preview_written",
            preview_root=str(preview_root),
            blockers=(),
            files=(SimpleNamespace(relative_path="mod.py"),),
        ),
        _large_file_refactor_workbench_structural_validation=SimpleNamespace(
            status="passed", blockers=()
        ),
    )
    before = target.read_bytes()
    context = prepare_advanced_quality_review_gui_run(
        window,
        active_project_root=str(project),
        tool_root=str(ROOT),
    )
    daily = project.parent / (project.name + "_delete_after_daily_work")
    baseline = Path(context.baseline_view_root)
    preview = Path(context.preview_view_root)
    assert baseline.is_relative_to(daily)
    assert preview.is_relative_to(daily)
    assert not baseline.is_relative_to(project)
    assert not preview.is_relative_to(project)
    assert context.request.analysis_identity.baseline_hash != context.request.analysis_identity.preview_hash
    assert context.package_name == "pkg"
    assert target.read_bytes() == before
    print("AQR_GUI_ANALYSIS_VIEWS_DAILY_WORK_ONLY: PASS")
    print("AQR_GUI_VIEW_PREPARATION_SOURCE_IMMUTABLE: PASS")
    print("AQR_GUI_ANALYSIS_IDENTITY_BINDS_SEALED_VIEWS: PASS")


def _validate_progression() -> None:
    base = dict(
        intake=SimpleNamespace(status="plan_intake_ready", ready_for_real_preview=True, source_hash_fresh=True),
        dependency_readiness=SimpleNamespace(status="dependency_readiness_ready", ready_for_real_preview_writer=True),
        preview=SimpleNamespace(status="real_preview_written", files=(1,), written_files=(1,), blockers=()),
        structural_validation=SimpleNamespace(status="passed", structural_status="STRUCTURAL_PASS", blockers=()),
    )
    state = build_workbench_gui_progression(**base)
    assert state.advanced_quality_review_enabled
    assert not state.preflight_enabled
    assert state.current_stage == "ADVANCED_QUALITY_REVIEW"
    ready_outcome = SimpleNamespace(
        cross_check_report=SimpleNamespace(quality_decision=SimpleNamespace(value="PASS")),
        run_record=SimpleNamespace(execution_status=SimpleNamespace(value="SUCCEEDED")),
    )
    state = build_workbench_gui_progression(**base, advanced_quality_review=ready_outcome)
    assert state.advanced_quality_review_ready
    assert state.preflight_enabled
    blocked = SimpleNamespace(
        cross_check_report=SimpleNamespace(quality_decision=SimpleNamespace(value="BLOCKED")),
        run_record=SimpleNamespace(execution_status=SimpleNamespace(value="SUCCEEDED")),
    )
    state = build_workbench_gui_progression(**base, advanced_quality_review=blocked)
    assert not state.preflight_enabled
    print("STRUCTURAL_TO_AQR_TO_PREFLIGHT_PROGRESSION: PASS")
    print("AQR_BLOCKED_DECISION_KEEPS_PREFLIGHT_CLOSED: PASS")


def _validate_gui_source_contract() -> None:
    gui = (PACKAGE / "advanced_quality_review_gui.py").read_text(encoding="ascii")
    workbench = (PACKAGE / "workbench_gui.py").read_text(encoding="ascii")
    stage_adapters = (PACKAGE / "main_workbench_stage_adapters.py").read_text(encoding="ascii")
    required_gui = (
        'QGroupBox("5. Advanced Quality Review")',
        'QPushButton("Run Advanced Quality Review")',
        'QPushButton("Cancel")',
        "QProgressBar()",
        "controller.start(context.request, None)",
        "invalidate_advanced_quality_review_gui",
        "cancellation requested",
    )
    for marker in required_gui:
        assert marker in gui, marker
    assert workbench.index("_build_validation_section(window)") < workbench.index("build_advanced_quality_review_section(")
    assert workbench.index("build_advanced_quality_review_section(") < workbench.index("_build_apply_section(window)")
    assert 'advanced_quality_review=getattr(window, "_large_file_refactor_workbench_advanced_quality_review", None)' in workbench
    assert 'invalidate_advanced_quality_review_gui(window, "REAL_PREVIEW_REGENERATED")' in stage_adapters
    assert 'invalidate_advanced_quality_review_gui(window, "STRUCTURAL_VALIDATION_RERUN")' in stage_adapters
    assert 'mark_advanced_quality_review_ready_for_run(window, status)' in stage_adapters
    print("AQR_GUI_REAL_BUTTON_PROGRESS_CANCEL_WIRING: PASS")
    print("AQR_GUI_LINEAGE_INVALIDATION_WIRING: PASS")


def _validate_worker_bootstrap_contract() -> None:
    worker = (PACKAGE / "advanced_quality_review_qt_worker.py").read_text(encoding="ascii")
    controller = (PACKAGE / "advanced_quality_review_qt_controller.py").read_text(encoding="ascii")
    assert 'plan: AdvancedQualityReviewExecutionPlan | None' in worker
    assert 'build_pinned_review_execution_plan(self._request)' in worker
    assert 'self.progress.emit("ENVIRONMENT_PREFLIGHT", "START")' in worker
    assert 'plan: AdvancedQualityReviewExecutionPlan | None' in controller
    assert "QThread()" in controller
    assert "ProcessPoolExecutor" not in controller
    print("AQR_ENVIRONMENT_PREFLIGHT_RUNS_OFF_GUI_THREAD: PASS")
    print("AQR_SINGLE_QTHREAD_CONTROLLER_PRESERVED: PASS")



def _validate_cancel_lifecycle_contract() -> None:
    gui = (PACKAGE / "advanced_quality_review_gui.py").read_text(encoding="ascii")
    controller = (PACKAGE / "advanced_quality_review_qt_controller.py").read_text(encoding="ascii")
    cancel_start = controller.index("    def cancel(self) -> bool:")
    state_start = controller.index("    def state(self)", cancel_start)
    cancel_body = controller[cancel_start:state_start]
    assert "self._running = False" not in cancel_body
    assert "self._cancel_requested = True" in cancel_body
    assert "or self._terminal_received" in cancel_body
    finished_start = controller.index("    def _handle_thread_finished")
    finished_body = controller[finished_start:]
    assert "self._running = False" in finished_body
    assert "self._on_settled(cancelled)" in finished_body
    assert 'window._large_file_refactor_workbench_advanced_quality_review = None' in gui
    assert 'window._large_file_refactor_workbench_state = "BLOCKED"' in gui
    print("AQR_CANCEL_RUNNING_UNTIL_THREAD_SETTLED: PASS")
    print("AQR_CANCEL_IMMEDIATE_AUTHORIZATION_CLEAR: PASS")

def _validate_sizes_and_encoding() -> None:
    touched = (
        PACKAGE / "advanced_quality_review_gui_context.py",
        PACKAGE / "advanced_quality_review_gui_formatting.py",
        PACKAGE / "advanced_quality_review_gui.py",
        PACKAGE / "advanced_quality_review_qt_worker.py",
        PACKAGE / "advanced_quality_review_qt_controller.py",
        PACKAGE / "workbench_gui_progression.py",
        PACKAGE / "workbench_gui.py",
        PACKAGE / "workbench_completion_gui.py",
        ROOT / "tools/validate_advanced_quality_review_gui_integration_v1.py",
        Path(__file__).resolve(),
    )
    for path in touched:
        data = path.read_bytes()
        data.decode("ascii")
        assert not data.startswith(b"\xef\xbb\xbf")
        ast.parse(data.decode("ascii"), filename=str(path))
        lines = len(data.decode("ascii").splitlines())
        assert lines <= 500, f"MODULE_TOO_LARGE:{path.relative_to(ROOT)}:{lines}"
    print("AQR_GUI_SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("AQR_GUI_TOUCHED_MODULES_MAX_500: PASS")


if __name__ == "__main__":
    main()
