"""Real Qt event-loop validation for Workbench Local AI correction lifecycle."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QWidget

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_local_ai_correction_qt_controller as controller,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_local_ai_correction_qt_worker as worker_module,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_local_ai_correction_models import (
    LocalAIWorkbenchCorrectionCandidate,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_context import (
    WorkbenchStageCorrectionContext,
)

FEATURE_ID = "workbench-local-ai-correction-qthread-bounded-runtime-sonar-v1"


def _context() -> WorkbenchStageCorrectionContext:
    return WorkbenchStageCorrectionContext(
        stage="ADVANCED_QUALITY_REVIEW",
        next_phase_goal="PREFLIGHT_BACKUP",
        active_project_root=str(ROOT),
        target_file=str(ROOT / "kanda_reasoner_app" / "__init__.py"),
        status="INDETERMINATE",
        blockers=("ruff:FAILED",),
        warnings=(),
        stage_output="controlled",
        evidence_chain=(("ADVANCED_QUALITY_REVIEW", "INDETERMINATE"),),
        correction_objective="controlled test",
    )


def _pump_until(app: QApplication, predicate, timeout: float = 4.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("Qt lifecycle predicate did not settle")


def main() -> None:
    app = QApplication.instance() or QApplication([])
    window = QWidget()
    window.resize(900, 700)
    window.show()
    rendered: list[str] = []
    sync_count = {"value": 0}
    heartbeat = {"value": 0}

    original_builder = worker_module.build_bounded_local_ai_workbench_correction_candidate
    original_apply = controller.apply_local_ai_workbench_correction

    def fake_builder(**kwargs):
        progress = kwargs["progress_callback"]
        interrupt = kwargs["interruption_check"]
        progress("CONTROLLED_MODEL_CALL")
        for _ in range(25):
            time.sleep(0.01)
            interrupt()
        return LocalAIWorkbenchCorrectionCandidate(False, "controlled terminal result")

    def fake_apply(_window, _context, candidate):
        return type("ControlledResult", (), {"ok": False, "intake": None, "message": candidate.message})()

    worker_module.build_bounded_local_ai_workbench_correction_candidate = fake_builder
    controller.apply_local_ai_workbench_correction = fake_apply

    timer = QTimer()
    timer.setInterval(20)
    timer.timeout.connect(lambda: heartbeat.__setitem__("value", heartbeat["value"] + 1))
    timer.start()

    try:
        started = controller.start_local_ai_correction(
            window=window,
            stage="ADVANCED_QUALITY_REVIEW",
            plan=object(),
            proposals=[],
            context=_context(),
            render_result=lambda _w, _s, text: rendered.append(text),
            render_intake=lambda _w, _i: None,
            sync_callback=lambda _w: sync_count.__setitem__("value", sync_count["value"] + 1),
        )
        assert started
        monitor = getattr(window, "_workbench_local_ai_correction_sonar_monitor", None)
        assert monitor is not None
        assert monitor.widget().isVisible()
        assert monitor._timer.isActive()
        print("LOCAL_AI_CORRECTION_REAL_WIDGET_SONAR_RUNNING: PASS")
        _pump_until(app, lambda: not controller.local_ai_execution_state(window).waiting)
        assert not monitor._timer.isActive()
        print("LOCAL_AI_CORRECTION_REAL_WIDGET_SONAR_SETTLES: PASS")
        assert heartbeat["value"] >= 2
        assert any("controlled terminal result" in item for item in rendered)
        print("LOCAL_AI_CORRECTION_REAL_WIDGET_HEARTBEAT: PASS")
        print("LOCAL_AI_CORRECTION_REAL_WIDGET_TERMINAL_SETTLEMENT: PASS")

        rendered.clear()
        started = controller.start_local_ai_correction(
            window=window,
            stage="ADVANCED_QUALITY_REVIEW",
            plan=object(),
            proposals=[],
            context=_context(),
            render_result=lambda _w, _s, text: rendered.append(text),
            render_intake=lambda _w, _i: None,
            sync_callback=lambda _w: None,
        )
        assert started
        QTimer.singleShot(
            40,
            lambda: controller.cancel_local_ai_correction(
                window,
                "ADVANCED_QUALITY_REVIEW",
                lambda _w, _s, text: rendered.append(text),
                lambda _w: None,
            ),
        )
        _pump_until(app, lambda: not controller.local_ai_execution_state(window).waiting)
        _pump_until(app, lambda: not controller.local_ai_execution_state(window).background_job_alive)
        assert any("WAIT CANCELED" in item for item in rendered)
        assert not any("controlled terminal result" in item for item in rendered)
        print("LOCAL_AI_CORRECTION_REAL_WIDGET_CANCEL_FAILS_CLOSED: PASS")
        print("LOCAL_AI_CORRECTION_REAL_WIDGET_LATE_RESULT_DISCARDED: PASS")
    finally:
        timer.stop()
        window.close()
        worker_module.build_bounded_local_ai_workbench_correction_candidate = original_builder
        controller.apply_local_ai_workbench_correction = original_apply

    print("WORKBENCH_LOCAL_AI_CORRECTION_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
