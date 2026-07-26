"""Qt GUI integration for Advanced Quality Review in the Workbench."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

from .advanced_quality_review_contract import QualityDecision
from .advanced_quality_review_gui_context import (
    prepare_advanced_quality_review_gui_run,
)
from .advanced_quality_review_gui_formatting import (
    format_advanced_quality_review_failure,
    format_advanced_quality_review_outcome,
    format_advanced_quality_review_progress,
)
from .advanced_quality_review_sonar import (
    finish_aqr_sonar_blocked,
    finish_aqr_sonar_success,
    start_aqr_sonar,
    update_aqr_sonar,
)
from .workbench_stage_correction_gui import build_workbench_stage_correction_row
from .workbench_aqr_correction_session import clear_aqr_correction_session
from .advanced_quality_review_orchestration import AdvancedQualityReviewStage
from .advanced_quality_review_qt_controller import AdvancedQualityReviewController

__all__ = [
    "advanced_quality_review_runtime_running",
    "build_advanced_quality_review_section",
    "cancel_advanced_quality_review_for_window",
    "invalidate_advanced_quality_review_gui",
    "mark_advanced_quality_review_ready_for_run",
    "start_advanced_quality_review_for_window",
    "sync_advanced_quality_review_controls",
]

_STAGE_ORDER = (
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
_READY_DECISIONS = {QualityDecision.PASS, QualityDecision.PASS_WITH_WARNINGS}


def build_advanced_quality_review_section(
    window: object,
    *,
    root_text_callback,
    sync_callback,
) -> QGroupBox:
    """Build the real Advanced Quality Review controls and visible progress."""
    box = QGroupBox("5. Advanced Quality Review")
    layout = QVBoxLayout(box)
    label = QLabel(
        "Run the pinned five-analyzer review on one sealed baseline/Preview pair. "
        "The review is evidence-only, sequential, cancellable, and never mutates source."
    )
    label.setWordWrap(True)
    layout.addWidget(label)

    row = QHBoxLayout()
    run_button = QPushButton("Run Advanced Quality Review")
    run_button.setEnabled(False)
    cancel_button = QPushButton("Cancel")
    cancel_button.setEnabled(False)
    row.addWidget(run_button)
    row.addWidget(cancel_button)
    row.addStretch(1)
    layout.addLayout(row)

    progress_bar = QProgressBar()
    progress_bar.setRange(0, len(_STAGE_ORDER))
    progress_bar.setValue(0)
    progress_bar.setFormat("Advanced Quality Review: %v/%m stages")
    layout.addWidget(progress_bar)

    progress_output = QPlainTextEdit()
    progress_output.setReadOnly(True)
    progress_output.setPlainText(
        format_advanced_quality_review_progress({}, _STAGE_ORDER)
    )
    layout.addWidget(progress_output)

    result_output = QPlainTextEdit()
    result_output.setReadOnly(True)
    result_output.setPlainText(
        "Structural Validation must pass first. The review will then run Environment "
        "Preflight, Ruff, API Review, Import Graph, Type Review, Dead Code, Delta, "
        "Cross-Check, and Persistence."
    )
    layout.addWidget(result_output)
    layout.addWidget(
        build_workbench_stage_correction_row(
            window,
            "ADVANCED_QUALITY_REVIEW",
            root_text_callback,
            sync_callback,
        )
    )

    window._large_file_refactor_workbench_aqr_run_button = run_button
    window._large_file_refactor_workbench_aqr_cancel_button = cancel_button
    window._large_file_refactor_workbench_aqr_progress_bar = progress_bar
    window._large_file_refactor_workbench_aqr_progress_output = progress_output
    window._large_file_refactor_workbench_aqr_output = result_output
    window._large_file_refactor_workbench_aqr_stage_states = {}
    window._large_file_refactor_workbench_aqr_terminal_status = ""
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = ""
    window._large_file_refactor_workbench_aqr_sync_callback = sync_callback
    window._large_file_refactor_workbench_aqr_root_text_callback = root_text_callback

    run_button.clicked.connect(lambda: _start_review(window))
    cancel_button.clicked.connect(lambda: _cancel_review(window))
    return box



def advanced_quality_review_runtime_running(window: object) -> bool:
    """Return whether an existing AQR worker generation is still settling."""
    controller = getattr(window, "_large_file_refactor_workbench_aqr_controller", None)
    return bool(controller is not None and controller.state().running)


def start_advanced_quality_review_for_window(window: object) -> bool:
    """Start one fresh guarded AQR generation and report exact acceptance."""
    if advanced_quality_review_runtime_running(window):
        return False
    return _start_review(window)


def cancel_advanced_quality_review_for_window(window: object) -> bool:
    """Request cancellation through the existing guarded AQR controller."""
    controller = getattr(window, "_large_file_refactor_workbench_aqr_controller", None)
    before = bool(controller is not None and controller.state().running)
    _cancel_review(window)
    return before

def sync_advanced_quality_review_controls(window: object, progression: Any) -> None:
    """Project real button availability from progression and controller state."""
    controller = getattr(window, "_large_file_refactor_workbench_aqr_controller", None)
    state = controller.state() if controller is not None else None
    running = bool(state and state.running)
    cancel_available = bool(
        state
        and state.running
        and not state.cancel_requested
        and not state.terminal_received
    )
    run_button = getattr(window, "_large_file_refactor_workbench_aqr_run_button", None)
    cancel_button = getattr(window, "_large_file_refactor_workbench_aqr_cancel_button", None)
    if run_button is not None:
        run_button.setEnabled(
            bool(getattr(progression, "advanced_quality_review_enabled", False) and not running)
        )
    if cancel_button is not None:
        cancel_button.setEnabled(cancel_available)


def invalidate_advanced_quality_review_gui(window: object, reason: str) -> None:
    """Invalidate current review evidence before card or Preview lineage changes."""
    if str(reason) == "PROJECT_CARD_OR_INTAKE_CHANGED":
        clear_aqr_correction_session(window)
    controller = getattr(window, "_large_file_refactor_workbench_aqr_controller", None)
    if controller is not None and controller.state().running:
        controller.cancel()
    window._large_file_refactor_workbench_advanced_quality_review = None
    window._large_file_refactor_workbench_aqr_identity_hash = ""
    window._large_file_refactor_workbench_aqr_context = None
    window._large_file_refactor_workbench_aqr_stage_states = {}
    window._large_file_refactor_workbench_aqr_terminal_status = ""
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = ""
    progress = getattr(window, "_large_file_refactor_workbench_aqr_progress_output", None)
    if progress is not None:
        progress.setPlainText(format_advanced_quality_review_progress({}, _STAGE_ORDER))
    bar = getattr(window, "_large_file_refactor_workbench_aqr_progress_bar", None)
    if bar is not None:
        bar.setValue(0)
    output = getattr(window, "_large_file_refactor_workbench_aqr_output", None)
    if output is not None:
        output.setPlainText(
            "Advanced Quality Review invalidated: " + str(reason) + "\nRun a fresh review after Structural Validation passes."
        )


def mark_advanced_quality_review_ready_for_run(
    window: object,
    structural_status: str,
) -> None:
    """Project the fresh post-structural AQR handoff without authorizing Preflight."""
    output = getattr(window, "_large_file_refactor_workbench_aqr_output", None)
    if output is not None:
        output.setPlainText(
            "ADVANCED QUALITY REVIEW READY\n\n"
            "Structural status: " + str(structural_status or "missing") + "\n"
            "Next action: Run Advanced Quality Review. Preflight remains closed "
            "until AQR returns SUCCEEDED with PASS or PASS_WITH_WARNINGS."
        )


def _start_review(window: object) -> bool:
    output = getattr(window, "_large_file_refactor_workbench_aqr_output", None)
    try:
        root_callback = window._large_file_refactor_workbench_aqr_root_text_callback
        active_root = str(root_callback(window))
        context = prepare_advanced_quality_review_gui_run(
            window,
            active_project_root=active_root,
            tool_root=str(Path(__file__).resolve().parents[3]),
        )
        window._large_file_refactor_workbench_aqr_context = context
        window._large_file_refactor_workbench_aqr_identity_hash = (
            context.request.analysis_identity.identity_hash
        )
        window._large_file_refactor_workbench_advanced_quality_review = None
        window._large_file_refactor_workbench_aqr_stage_states = {}
        window._large_file_refactor_workbench_aqr_terminal_status = ""
        window._large_file_refactor_workbench_aqr_terminal_diagnostic = ""
        _reset_progress(window)
        _set_preflight_gate_text(
            window,
            "AQR_RUNNING",
            "Advanced Quality Review is running. Preflight remains closed until one terminal SUCCEEDED review returns PASS or PASS_WITH_WARNINGS.",
        )
        controller = _controller(window)
        started = controller.start(context.request, None)
        if not started:
            if output is not None:
                output.setPlainText(
                    "Advanced Quality Review is waiting for the previous worker "
                    "generation to settle. No stale result will be accepted."
                )
            _sync(window)
            return False
        start_aqr_sonar(window)
        if output is not None:
            output.setPlainText(
                "Advanced Quality Review started. Source is read-only; durable evidence "
                "will be persisted only under the selected Project Support root."
            )
    except Exception as error:
        _on_failure(window, type(error).__name__ + ":" + str(error))
        return False
    _sync(window)
    return True


def _cancel_review(window: object) -> None:
    controller = getattr(window, "_large_file_refactor_workbench_aqr_controller", None)
    if controller is None or not controller.cancel():
        return
    window._large_file_refactor_workbench_advanced_quality_review = None
    window._large_file_refactor_workbench_aqr_terminal_status = "CANCEL_REQUESTED"
    update_aqr_sonar(window, "CANCEL_REQUESTED", "Late output will be ignored.")
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = "Cancellation requested by user."
    window._large_file_refactor_workbench_state = "BLOCKED"
    _set_preflight_gate_text(
        window,
        "AQR_CANCEL_REQUESTED",
        "Cancellation is settling. Preflight remains closed and no correction route is opened until the worker reaches a terminal state.",
    )
    output = getattr(window, "_large_file_refactor_workbench_aqr_output", None)
    if output is not None:
        output.setPlainText(
            "Advanced Quality Review cancellation requested. Late output is rejected and "
            "cannot authorize Preflight."
        )
    _sync(window)


def _controller(window: object) -> AdvancedQualityReviewController:
    controller = getattr(window, "_large_file_refactor_workbench_aqr_controller", None)
    if controller is not None:
        return controller
    controller = AdvancedQualityReviewController(
        current_identity_hash=lambda: str(
            getattr(window, "_large_file_refactor_workbench_aqr_identity_hash", "") or ""
        ),
        on_progress=lambda stage, message: _on_progress(window, stage, message),
        on_outcome=lambda outcome: _on_outcome(window, outcome),
        on_failure=lambda diagnostic: _on_failure(window, diagnostic),
        on_settled=lambda cancelled: _on_settled(window, cancelled),
    )
    window._large_file_refactor_workbench_aqr_controller = controller
    return controller


def _on_progress(window: object, stage: str, message: str) -> None:
    states = dict(getattr(window, "_large_file_refactor_workbench_aqr_stage_states", {}) or {})
    if stage in _STAGE_ORDER:
        states[str(stage)] = str(message)
    window._large_file_refactor_workbench_aqr_stage_states = states
    update_aqr_sonar(window, stage, message)
    progress = getattr(window, "_large_file_refactor_workbench_aqr_progress_output", None)
    if progress is not None:
        progress.setPlainText(format_advanced_quality_review_progress(states, _STAGE_ORDER))
    bar = getattr(window, "_large_file_refactor_workbench_aqr_progress_bar", None)
    if bar is not None:
        completed = sum(1 for name in _STAGE_ORDER if name in states and states[name] not in {"START", "WAITING"})
        bar.setValue(completed)
    _sync(window)


def _on_outcome(window: object, outcome: Any) -> None:
    window._large_file_refactor_workbench_advanced_quality_review = outcome
    decision = getattr(getattr(outcome, "cross_check_report", None), "quality_decision", None)
    decision_text = _enum_text(decision)
    execution_text = _enum_text(
        getattr(getattr(outcome, "run_record", None), "execution_status", "")
    )
    window._large_file_refactor_workbench_aqr_terminal_status = (
        decision_text if execution_text == "SUCCEEDED" else (execution_text or decision_text)
    )
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = ""
    ready = decision in _READY_DECISIONS and execution_text == "SUCCEEDED"
    window._large_file_refactor_workbench_state = (
        "ADVANCED_QUALITY_REVIEW_READY" if ready else "BLOCKED"
    )
    if ready:
        clear_aqr_correction_session(window)
        _set_preflight_gate_text(
            window,
            "AQR_READY",
            "Advanced Quality Review completed successfully. Preflight may now be prepared.",
        )
    else:
        _set_preflight_gate_text(
            window,
            "AQR_BLOCKED",
            "Advanced Quality Review reached a terminal non-authorizing result. Use the Stage 5 Correction Routes, then rerun deterministic stages and AQR.",
        )
    output = getattr(window, "_large_file_refactor_workbench_aqr_output", None)
    if output is not None:
        output.setPlainText(format_advanced_quality_review_outcome(outcome))
    if ready:
        finish_aqr_sonar_success(window, "AQR completed with " + decision_text)
    else:
        finish_aqr_sonar_blocked(
            window,
            "AQR ended with execution=" + execution_text + ", decision=" + decision_text,
        )
    _sync(window)


def _on_failure(window: object, diagnostic: str) -> None:
    window._large_file_refactor_workbench_advanced_quality_review = None
    window._large_file_refactor_workbench_aqr_terminal_status = "FAILED"
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = str(diagnostic)
    window._large_file_refactor_workbench_state = "BLOCKED"
    _set_preflight_gate_text(
        window,
        "AQR_FAILED",
        "Advanced Quality Review failed. Preflight remains closed. Stage 5 Correction Routes are now available with the exact failure context.",
    )
    output = getattr(window, "_large_file_refactor_workbench_aqr_output", None)
    if output is not None:
        output.setPlainText(format_advanced_quality_review_failure(diagnostic))
    finish_aqr_sonar_blocked(window, "AQR failure: " + str(diagnostic))
    _sync(window)



def _on_settled(window: object, cancelled: bool) -> None:
    """Refresh controls only after the review worker thread has actually settled."""
    if cancelled:
        window._large_file_refactor_workbench_advanced_quality_review = None
        window._large_file_refactor_workbench_aqr_terminal_status = "CANCELLED"
        window._large_file_refactor_workbench_aqr_terminal_diagnostic = "Review cancelled by user."
        window._large_file_refactor_workbench_state = "BLOCKED"
        _set_preflight_gate_text(
            window,
            "AQR_CANCELLED",
            "Advanced Quality Review was cancelled. Preflight remains closed. Run a fresh review or use correction routes only after a technical blocked result.",
        )
        finish_aqr_sonar_blocked(window, "AQR cancelled by user")
    _sync(window)

def _reset_progress(window: object) -> None:
    progress = getattr(window, "_large_file_refactor_workbench_aqr_progress_output", None)
    if progress is not None:
        progress.setPlainText(format_advanced_quality_review_progress({}, _STAGE_ORDER))
    bar = getattr(window, "_large_file_refactor_workbench_aqr_progress_bar", None)
    if bar is not None:
        bar.setValue(0)


def _sync(window: object) -> None:
    callback = getattr(window, "_large_file_refactor_workbench_aqr_sync_callback", None)
    if callable(callback):
        callback(window)

def _set_preflight_gate_text(window: object, reason: str, detail: str) -> None:
    output = getattr(window, "_large_file_refactor_workbench_preflight_output", None)
    if output is not None:
        output.setPlainText(
            "PREFLIGHT GATE\n\nReason: " + str(reason) + "\n" + str(detail)
        )


def _enum_text(value: Any) -> str:
    return str(getattr(value, "value", value) or "")

