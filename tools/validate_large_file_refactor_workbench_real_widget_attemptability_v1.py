"""Validate the real PySide Workbench widget chain without synthetic-only state tests."""
from __future__ import annotations

import os
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _configure_offscreen_font_directory() -> str:
    """Configure a real font directory before the offscreen Qt import."""
    if os.name != "nt":
        return "NOT_REQUIRED_NON_WINDOWS"

    configured = os.environ.get("QT_QPA_FONTDIR", "").strip()
    if configured:
        configured_path = Path(configured)
        if not configured_path.is_dir():
            raise RuntimeError(
                "QT_QPA_FONTDIR_DOES_NOT_EXIST:" + str(configured_path)
            )
        return str(configured_path)

    candidates: list[Path] = []
    for variable_name in ("WINDIR", "SystemRoot"):
        value = os.environ.get(variable_name, "").strip()
        if value:
            candidate = Path(value) / "Fonts"
            if candidate not in candidates:
                candidates.append(candidate)

    for candidate in candidates:
        if candidate.is_dir():
            os.environ["QT_QPA_FONTDIR"] = str(candidate)
            return str(candidate)

    raise RuntimeError(
        "QT_OFFSCREEN_FONT_DIRECTORY_NOT_FOUND:"
        + "|".join(str(candidate) for candidate in candidates)
    )


QT_OFFSCREEN_FONTDIR = _configure_offscreen_font_directory()
print("QT_OFFSCREEN_FONTDIR_READY: PASS")
print("QT_OFFSCREEN_FONTDIR: " + QT_OFFSCREEN_FONTDIR)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOLS_ROOT = PROJECT_ROOT / "tools"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow  # noqa: E402

from patch6_controlled_real_module_support import (  # noqa: E402
    build_approved_controlled_plan,
    prepare_controlled_project,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import workbench_gui  # noqa: E402
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (  # noqa: E402
    export_latest_planner_workbench_handoff,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (  # noqa: E402
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (  # noqa: E402
    build_workbench_plan_snapshot,
)


_VALIDATOR_TIMEOUT_SECONDS = 600


def _print_stage(marker: str) -> None:
    """Emit one unbuffered progress marker for live validation observability."""
    print(marker, flush=True)


def _start_validator_watchdog() -> None:
    """Terminate a globally stuck validator instead of hanging forever."""
    def _watchdog() -> None:
        time.sleep(_VALIDATOR_TIMEOUT_SECONDS)
        _print_stage(
            "REAL_WIDGET_VALIDATOR_TIMEOUT: exceeded "
            + str(_VALIDATOR_TIMEOUT_SECONDS)
            + " seconds"
        )
        os._exit(124)

    threading.Thread(
        target=_watchdog,
        name="real-widget-validator-watchdog",
        daemon=True,
    ).start()

FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-"
    "real-widget-attemptable-actions-v1"
)

_SEQUENTIAL_BUTTONS = (
    "_large_file_refactor_workbench_dependency_button",
    "_large_file_refactor_workbench_real_preview_button",
    "_large_file_refactor_workbench_validate_button",
    "_large_file_refactor_workbench_preflight_button",
    "_large_file_refactor_workbench_source_payload_button",
    "_large_file_refactor_workbench_completion_prepare_button",
    "_large_file_refactor_workbench_transaction_prepare_button",
)

_HARD_GATED_BUTTONS = (
    "_large_file_refactor_workbench_refactor_large_module_button",
    "_large_file_refactor_workbench_transaction_rollback_button",
)


def run_validation() -> None:
    """Build the actual widget tree and click the real preparation chain."""
    _start_validator_watchdog()
    _print_stage("REAL_WIDGET_STAGE_START: QApplication")
    app = QApplication.instance() or QApplication([])
    _print_stage("REAL_WIDGET_STAGE_PASS: QApplication")
    _print_stage("REAL_WIDGET_STAGE_START: prepare_controlled_project")
    paths = prepare_controlled_project(PROJECT_ROOT)
    _print_stage("REAL_WIDGET_STAGE_PASS: prepare_controlled_project")
    _print_stage("REAL_WIDGET_STAGE_START: build_approved_controlled_plan")
    analysis, plan = build_approved_controlled_plan(paths.controlled_target)
    _print_stage("REAL_WIDGET_STAGE_PASS: build_approved_controlled_plan")
    snapshot = _build_snapshot(plan, analysis, paths.controlled_target)
    intake = build_workbench_plan_intake(
        snapshot=snapshot,
        active_project_root=str(paths.controlled_project_root),
    )
    if intake.status != "plan_intake_ready" or intake.blockers:
        raise AssertionError("REAL_WIDGET_INTAKE_BLOCKED:" + "|".join(intake.blockers))

    _print_stage("REAL_WIDGET_STAGE_START: build_widget_tree")
    window = QMainWindow()
    window._root_path_edit = QLineEdit(str(paths.controlled_project_root))
    page = workbench_gui.build_large_file_refactor_workbench_page(window)
    window.setCentralWidget(page)
    window.show()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: build_widget_tree")

    _assert_initial_sequential_gates_closed(window)
    _assert_hard_gates_closed(window)
    print("REAL_WIDGET_INITIAL_SEQUENTIAL_GATES_CLOSED: PASS")

    validate_button = window._large_file_refactor_workbench_validate_button
    window._large_file_refactor_workbench_plan_snapshot = snapshot
    workbench_gui._store_and_render_intake(window, intake)
    app.processEvents()

    _assert_only_next_stage_enabled(
        window,
        "_large_file_refactor_workbench_dependency_button",
    )
    print("REAL_WIDGET_PLAN_INTAKE_ENABLES_DEPENDENCY: PASS")

    _print_stage("REAL_WIDGET_STAGE_START: dependency_readiness_click")
    window._large_file_refactor_workbench_dependency_button.click()
    app.processEvents()
    readiness = window._large_file_refactor_workbench_dependency_readiness
    _print_stage("REAL_WIDGET_STAGE_PASS: dependency_readiness_click")
    if readiness.status != "dependency_readiness_ready" or readiness.blockers:
        raise AssertionError("REAL_WIDGET_DEPENDENCY_BLOCKED:" + "|".join(readiness.blockers))

    _print_stage("REAL_WIDGET_STAGE_START: real_preview_click")
    window._large_file_refactor_workbench_real_preview_button.click()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: real_preview_click")
    preview = window._large_file_refactor_workbench_real_preview
    if preview.status != "real_preview_written" or preview.blockers:
        raise AssertionError("REAL_WIDGET_PREVIEW_BLOCKED:" + "|".join(preview.blockers))
    if not validate_button.isEnabled() or not validate_button.isEnabledTo(page):
        raise AssertionError("REAL_WIDGET_STRUCTURAL_NOT_INTERACTIVE_AFTER_PREVIEW")
    print("REAL_PREVIEW_TO_STRUCTURAL_REAL_WIDGET: PASS")

    _print_stage("REAL_WIDGET_STAGE_START: structural_validation_click")
    validate_button.click()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: structural_validation_click")
    structural = window._large_file_refactor_workbench_structural_validation
    if not structural.status.startswith("passed") or structural.blockers:
        raise AssertionError("REAL_WIDGET_STRUCTURAL_BLOCKED:" + "|".join(structural.blockers))
    print("STRUCTURAL_REAL_WIDGET_CLICK: PASS")

    _print_stage("REAL_WIDGET_STAGE_START: preflight_click")
    window._large_file_refactor_workbench_preflight_button.click()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: preflight_click")
    preflight = window._large_file_refactor_workbench_preflight_backup
    if preflight.status != "preflight_backup_ready" or preflight.blockers:
        raise AssertionError("REAL_WIDGET_PREFLIGHT_BLOCKED:" + "|".join(preflight.blockers))

    _print_stage("REAL_WIDGET_STAGE_START: source_payload_click")
    window._large_file_refactor_workbench_source_payload_button.click()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: source_payload_click")
    payload = window._large_file_refactor_workbench_source_payload
    if payload.status != "source_apply_payload_ready" or payload.blockers:
        raise AssertionError("REAL_WIDGET_PAYLOAD_BLOCKED:" + "|".join(payload.blockers))
    print("STRUCTURAL_TO_PREFLIGHT_TO_PAYLOAD_REAL_WIDGET: PASS")

    completion_button = window._large_file_refactor_workbench_completion_prepare_button
    if not completion_button.isEnabled():
        raise AssertionError("COMPLETION_EVIDENCE_BUTTON_NOT_ATTEMPTABLE")
    _print_stage("REAL_WIDGET_STAGE_START: completion_evidence_click")
    completion_button.click()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: completion_evidence_click")
    evidence = window._large_file_refactor_workbench_completion_evidence
    if evidence is None:
        output = window._large_file_refactor_workbench_completion_status_output.toPlainText()
        raise AssertionError("REAL_WIDGET_COMPLETION_EVIDENCE_BLOCKED:" + output)
    print("COMPLETION_EVIDENCE_REAL_WIDGET_CLICK: PASS")

    review = window._large_file_refactor_workbench_semantic_review_check
    warnings = window._large_file_refactor_workbench_warning_ack_check
    if not review.isEnabled() or not warnings.isEnabled():
        raise AssertionError("HUMAN_REVIEW_CONTROLS_NOT_ENABLED_AFTER_EVIDENCE")

    assistant_buttons = (
        window._large_file_refactor_workbench_diff_review_heuristic_button,
        window._large_file_refactor_workbench_diff_review_local_ai_button,
        window._large_file_refactor_workbench_diff_review_web_ai_button,
        window._large_file_refactor_workbench_diff_review_receive_button,
    )
    if not all(button.isEnabled() for button in assistant_buttons):
        raise AssertionError("ASSISTED_DIFF_REVIEW_BUTTON_NOT_ENABLED_AFTER_EVIDENCE")
    _print_stage("REAL_WIDGET_STAGE_START: assisted_heuristic_review_click")
    window._large_file_refactor_workbench_diff_review_heuristic_button.click()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: assisted_heuristic_review_click")
    semantic_text = window._large_file_refactor_workbench_semantic_diff_output.toPlainText()
    text_diff_text = window._large_file_refactor_workbench_text_diff_output.toPlainText()
    if "--- ASSISTED REVIEW: HEURISTIC ---" not in semantic_text:
        raise AssertionError("HEURISTIC_REVIEW_NOT_APPENDED_TO_SEMANTIC_DIFF")
    if "--- ASSISTED REVIEW: HEURISTIC ---" not in text_diff_text:
        raise AssertionError("HEURISTIC_REVIEW_NOT_APPENDED_TO_TEXT_DIFF")
    if review.isChecked() or warnings.isChecked():
        raise AssertionError("ASSISTED_REVIEW_AUTO_CONFIRMED_HUMAN_GATE")
    print("ASSISTED_DIFF_REVIEW_REAL_WIDGET: PASS")

    review.setChecked(True)
    warnings.setChecked(True)
    app.processEvents()

    transaction_button = window._large_file_refactor_workbench_transaction_prepare_button
    if not transaction_button.isEnabled():
        raise AssertionError("TRANSACTION_SUMMARY_BUTTON_NOT_ATTEMPTABLE")
    _print_stage("REAL_WIDGET_STAGE_START: transaction_summary_click")
    transaction_button.click()
    app.processEvents()
    _print_stage("REAL_WIDGET_STAGE_PASS: transaction_summary_click")
    transaction = window._large_file_refactor_workbench_completion_transaction
    if transaction is None:
        output = window._large_file_refactor_workbench_completion_status_output.toPlainText()
        raise AssertionError("REAL_WIDGET_TRANSACTION_SUMMARY_BLOCKED:" + output)

    confirm = window._large_file_refactor_workbench_transaction_confirm_check
    if not confirm.isEnabled():
        raise AssertionError("TRANSACTION_CONFIRMATION_NOT_ENABLED")
    confirm.setChecked(True)
    app.processEvents()
    final_button = window._large_file_refactor_workbench_refactor_large_module_button
    if not final_button.isEnabled():
        gate_text = window._large_file_refactor_workbench_refactor_gate_output.toPlainText()
        raise AssertionError("FINAL_REAL_WIDGET_GATE_NOT_ENABLED:" + gate_text)
    print("COMPLETION_REVIEW_TO_FINAL_GATE_REAL_WIDGET: PASS")

    if hasattr(window, "_large_file_refactor_workbench_apply_button"):
        raise AssertionError("LEGACY_APPLY_CONTROL_REINTRODUCED")
    if window._large_file_refactor_workbench_transaction_rollback_button.isEnabled():
        raise AssertionError("ROLLBACK_ENABLED_WITHOUT_APPLIED_STATE")
    print("MUTATION_AND_RECOVERY_GATES_REMAIN_FAIL_CLOSED: PASS")

    live_target = PROJECT_ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    if live_target.read_bytes() != (paths.live_project_root / live_target.relative_to(PROJECT_ROOT)).read_bytes():
        raise AssertionError("LIVE_SOURCE_IDENTITY_CHECK_FAILED")
    print("LIVE_PROJECT_SOURCE_UNCHANGED: PASS")
    _print_stage(f"VALIDATION OK: {FEATURE_ID}")


def _build_snapshot(plan, analysis, target: Path):
    """Build one immutable Workbench snapshot through the public handoff seam."""
    planner_window = SimpleNamespace(
        _large_file_refactor_last_plan=plan,
        _large_file_refactor_last_analysis=analysis,
        _large_file_refactor_planner_candidates=[SimpleNamespace(path=str(target))],
    )
    return build_workbench_plan_snapshot(
        export_latest_planner_workbench_handoff(planner_window)
    )


def _assert_initial_sequential_gates_closed(window: object) -> None:
    """Require sequential actions to remain closed before Plan Intake is loaded."""
    for attribute in _SEQUENTIAL_BUTTONS:
        button = getattr(window, attribute, None)
        if button is None:
            raise AssertionError("SEQUENTIAL_BUTTON_MISSING:" + attribute)
        if button.isEnabled():
            raise AssertionError("SEQUENTIAL_BUTTON_OPEN_BEFORE_INTAKE:" + attribute)


def _assert_only_next_stage_enabled(window: object, expected: str) -> None:
    """Require the next sequential stage to open without skipping later stages."""
    for attribute in _SEQUENTIAL_BUTTONS:
        button = getattr(window, attribute, None)
        if button is None:
            raise AssertionError("SEQUENTIAL_BUTTON_MISSING:" + attribute)
        should_be_enabled = attribute == expected
        if button.isEnabled() != should_be_enabled:
            raise AssertionError(
                "SEQUENTIAL_STAGE_STATE_MISMATCH:"
                + attribute
                + ":expected="
                + str(should_be_enabled)
                + ":actual="
                + str(button.isEnabled())
            )


def _assert_hard_gates_closed(window: object) -> None:
    """Require mutation and recovery actions to remain unavailable initially."""
    for attribute in _HARD_GATED_BUTTONS:
        button = getattr(window, attribute, None)
        if button is None:
            raise AssertionError("HARD_GATED_BUTTON_MISSING:" + attribute)
        if button.isEnabled():
            raise AssertionError("HARD_GATED_BUTTON_OPEN_TOO_EARLY:" + attribute)


if __name__ == "__main__":
    run_validation()
