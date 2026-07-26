"""Validate Qt-native bounded Local AI correction runtime contracts."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
FEATURE_ID = "workbench-local-ai-correction-qthread-bounded-runtime-sonar-v1"


def _read(name: str) -> str:
    return (PKG / name).read_text(encoding="utf-8")


def main() -> None:
    gui = _read("workbench_stage_correction_gui.py")
    controller = _read("workbench_local_ai_correction_qt_controller.py")
    worker = _read("workbench_local_ai_correction_qt_worker.py")
    runtime = _read("workbench_local_ai_correction_runtime.py")
    protocol = _read("planner_local_ai_staged_protocol.py")
    service = _read("workbench_stage_correction_service.py")
    sonar = _read("workbench_local_ai_correction_sonar.py")

    assert "threading.Thread(" not in gui
    assert "queue.Queue" not in gui
    assert "start_local_ai_correction(" in gui
    assert "Cancel Local AI Wait" in gui
    print("LOCAL_AI_CORRECTION_DEPRECATED_THREAD_TIMER_ROUTE_REMOVED: PASS")

    for marker in (
        "QThread()",
        "_LOCAL_AI_TIMEOUT_MS = 120_000",
        '"accept_result": True',
        "requestInterruption()",
        "generation != int(",
        "LOCAL AI CORRECTION TIMEOUT",
        "late result will be ignored",
    ):
        assert marker in controller, marker
    print("LOCAL_AI_CORRECTION_QTHREAD_SIGNAL_LIFECYCLE: PASS")
    print("LOCAL_AI_CORRECTION_TIMEOUT_CANCEL_LATE_RESULT_DISCARD: PASS")

    for sonar_marker in (
        "GreenSonarActivityMonitor",
        "start_local_ai_correction_sonar",
        "update_local_ai_correction_sonar",
        "finish_local_ai_correction_sonar_success",
        "finish_local_ai_correction_sonar_error",
        '"ANALYZE_SOURCE": "Analyzing source structure"',
        '"VALIDATE_CORRECTED_PLAN": "Validating corrected plan"',
    ):
        assert sonar_marker in sonar, sonar_marker
    for controller_marker in (
        "start_local_ai_correction_sonar(window, stage)",
        "update_local_ai_correction_sonar(",
        "finish_local_ai_correction_sonar_success(window, result.message)",
        "finish_local_ai_correction_sonar_error(window, message)",
    ):
        assert controller_marker in controller, controller_marker
    print("LOCAL_AI_CORRECTION_GREEN_SONAR_LIFECYCLE: PASS")

    assert "WorkbenchLocalAICorrectionWorker(QObject)" in worker
    assert "progress = Signal(str)" in worker
    assert "result_ready = Signal(object)" in worker
    assert "QThread.currentThread().isInterruptionRequested()" in worker
    print("LOCAL_AI_CORRECTION_PROGRESS_AND_INTERRUPTION_CHECKPOINTS: PASS")

    assert "review_plan_with_local_ai_tournament" not in runtime
    for marker in (
        "review_plan_with_staged_local_ai(",
        "max_rounds=2",
        "include_naming_review=False",
        "include_final_audit=False",
        "strategy_instruction=context.prompt_text()",
    ):
        assert marker in runtime, marker
    print("LOCAL_AI_CORRECTION_SINGLE_TRACK_BOUNDED_PROTOCOL: PASS")

    for marker in (
        "progress_callback:",
        "interruption_check:",
        "include_naming_review: bool = True",
        "include_final_audit: bool = True",
        'progress("RESPONSIBILITY_ANALYSIS")',
        'progress("TARGETED_REPAIR_ATTEMPT_" + str(attempt))',
        '"skipped_bounded_correction_lane"',
    ):
        assert marker in protocol, marker
    print("LOCAL_AI_STAGED_PROTOCOL_COOPERATIVE_BOUNDARY: PASS")

    assert "build_bounded_local_ai_workbench_correction_candidate(" in service
    assert "load_latest_snapshot_into_workbench(" in service
    assert "setEnabled(True)" not in runtime
    assert "setEnabled(True)" not in controller
    print("LOCAL_AI_CORRECTION_ATOMIC_RELOAD_AND_FAIL_CLOSED_GATES: PASS")

    touched = (
        "workbench_stage_correction_gui.py",
        "workbench_stage_correction_service.py",
        "workbench_local_ai_correction_models.py",
        "workbench_local_ai_correction_runtime.py",
        "workbench_local_ai_correction_qt_worker.py",
        "workbench_local_ai_correction_qt_controller.py",
        "planner_local_ai_staged_protocol.py",
        "workbench_local_ai_correction_sonar.py",
    )
    for name in touched:
        path = PKG / name
        text = path.read_text(encoding="utf-8")
        ast.parse(text, filename=str(path))
        line_count = len(text.splitlines())
        assert 1 <= line_count <= 500, (name, line_count)
        text.encode("ascii")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")

    print("WORKBENCH_LOCAL_AI_CORRECTION_QTHREAD_BOUNDED_RUNTIME: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
