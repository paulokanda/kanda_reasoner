"""Qt correction lane for blocked Large File Refactor Workbench stages."""
from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QWidget

from .planner_version_state import PLANNER_VERSION_WEB_AI, select_planner_version
from .planner_web_ai_exchange_gui import open_receive_planning_from_web_ai
from .workbench_formatting import format_workbench_intake
from .workbench_dependency_formatting import format_workbench_dependency_readiness
from .workbench_gui_progression import preview_validation_guidance
from .workbench_preflight_backup_formatting import format_preflight_backup_readiness
from .workbench_real_preview_formatting import format_real_preview_result
from .workbench_source_payload_formatting import format_source_apply_payload_readiness
from .workbench_structural_validation_formatting import format_real_preview_structural_validation
from .workbench_heuristic_correction_qt_controller import (
    cancel_heuristic_correction,
    heuristic_execution_state,
    start_heuristic_correction,
)
from .workbench_local_ai_correction_qt_controller import (
    cancel_local_ai_correction,
    local_ai_execution_state,
    start_local_ai_correction,
)
from .workbench_snapshot_bridge import (
    load_latest_snapshot_into_workbench,
    materialize_workbench_owned_plan,
)
from .workbench_stage_correction_route_switch import (
    abandon_heuristic_before_local_ai,
    abandon_local_ai_before_heuristic,
    abandon_workers_before_web_receive,
)
from .workbench_stage_correction_context import (
    WORKBENCH_CORRECTABLE_STAGES,
    build_stage_correction_context,
    stage_correction_needed,
)
from .workbench_aqr_correction_session import note_aqr_correction_candidate
from .workbench_correction_candidate_guard import web_ai_plan_materially_changes
from .workbench_stage_correction_service import (
    HeuristicWorkbenchCorrectionCandidate,
    apply_heuristic_workbench_correction,
    build_web_ai_workbench_correction_prompt,
)

__all__ = [
    "build_workbench_stage_correction_row",
    "sync_workbench_stage_correction_controls",
    "sync_workbench_stage_correction_controls_from_window",
]

_OUTPUT_ATTR = {
    "PLAN_INTAKE": "_large_file_refactor_workbench_intake_output",
    "DEPENDENCY_READINESS": "_large_file_refactor_workbench_dependency_output",
    "REAL_PREVIEW": "_large_file_refactor_workbench_real_preview_output",
    "STRUCTURAL_VALIDATION": "_large_file_refactor_workbench_validation_output",
    "ADVANCED_QUALITY_REVIEW": "_large_file_refactor_workbench_aqr_output",
    "PREFLIGHT_BACKUP": "_large_file_refactor_workbench_preflight_output",
    "SOURCE_PAYLOAD": "_large_file_refactor_workbench_source_payload_output",
    "COMPLETION_EVIDENCE": "_large_file_refactor_workbench_completion_status_output",
}

def build_workbench_stage_correction_row(
    window: object,
    stage: str,
    root_text_callback: Callable[[object], str],
    sync_callback: Callable[[object], None],
) -> QWidget:
    """Build one stage-specific correction row, disabled until failed evidence exists."""
    if stage not in WORKBENCH_CORRECTABLE_STAGES:
        raise ValueError("Unsupported correction stage: " + stage)
    if not hasattr(window, "_large_file_refactor_workbench_global_sync_callback"):
        window._large_file_refactor_workbench_global_sync_callback = sync_callback
    if not hasattr(window, "_large_file_refactor_workbench_root_text_callback"):
        window._large_file_refactor_workbench_root_text_callback = root_text_callback
    effective_sync = getattr(
        window,
        "_large_file_refactor_workbench_global_sync_callback",
        sync_callback,
    )
    host = QWidget()
    layout = QHBoxLayout(host)
    layout.setContentsMargins(0, 0, 0, 0)
    label = QLabel("Correction routes: available only after this stage reports blocked evidence.")
    layout.addWidget(label, 1)
    heuristic = QPushButton("Heuristic Correction")
    cancel_heuristic = QPushButton("Cancel Heuristic Wait")
    local_ai = QPushButton("Local AI Correction")
    cancel_local_ai = QPushButton("Cancel Local AI Wait")
    web_copy = QPushButton("Copy Web AI Correction Package")
    web_receive = QPushButton("Receive Web AI Correction")
    for button in (
        heuristic,
        cancel_heuristic,
        local_ai,
        cancel_local_ai,
        web_copy,
        web_receive,
    ):
        button.setEnabled(False)
        layout.addWidget(button)
    heuristic.clicked.connect(
        lambda: _run_heuristic(window, stage, root_text_callback, effective_sync)
    )
    cancel_heuristic.clicked.connect(
        lambda: _cancel_heuristic(window, stage, effective_sync)
    )
    local_ai.clicked.connect(
        lambda: _start_local_ai(window, stage, root_text_callback, effective_sync)
    )
    cancel_local_ai.clicked.connect(
        lambda: _cancel_local_ai(window, stage, effective_sync)
    )
    web_copy.clicked.connect(
        lambda: _copy_web_ai(window, stage, root_text_callback)
    )
    web_receive.clicked.connect(
        lambda: _receive_web_ai(window, stage, root_text_callback, effective_sync)
    )
    controls = getattr(window, "_large_file_refactor_workbench_correction_controls", None)
    if not isinstance(controls, dict):
        controls = {}
        window._large_file_refactor_workbench_correction_controls = controls
    controls[stage] = {
        "host": host,
        "label": label,
        "heuristic": heuristic,
        "cancel_heuristic": cancel_heuristic,
        "local_ai": local_ai,
        "cancel_local_ai": cancel_local_ai,
        "web_copy": web_copy,
        "web_receive": web_receive,
        "buttons": (
            heuristic,
            cancel_heuristic,
            local_ai,
            cancel_local_ai,
            web_copy,
            web_receive,
        ),
    }
    return host

def sync_workbench_stage_correction_controls(
    window: object,
    root_text_callback: Callable[[object], str],
) -> None:
    """Project blocked-stage correction controls from exact worker and evidence state."""
    controls = getattr(window, "_large_file_refactor_workbench_correction_controls", {})
    heuristic_state = heuristic_execution_state(window)
    heuristic_running = heuristic_state.waiting
    active_stage = heuristic_state.active_stage
    heuristic_job_alive = heuristic_state.background_job_alive
    local_state = local_ai_execution_state(window)
    local_running = local_state.waiting
    local_active_stage = local_state.active_stage
    local_progress_phase = local_state.progress_phase
    local_job_alive = local_state.background_job_alive
    root = str(root_text_callback(window))
    progress_phase = heuristic_state.progress_phase

    for stage, bundle in controls.items():
        needed = stage_correction_needed(window, stage, root)
        heuristic = bundle.get("heuristic")
        if heuristic is not None:
            heuristic.setEnabled(bool(needed and not heuristic_running))
        cancel = bundle.get("cancel_heuristic")
        if cancel is not None:
            cancel.setEnabled(bool(heuristic_running and active_stage == stage))

        local_button = bundle.get("local_ai")
        if local_button is not None:
            local_button.setEnabled(bool(needed and not local_running))
        cancel_local = bundle.get("cancel_local_ai")
        if cancel_local is not None:
            cancel_local.setEnabled(bool(local_running and local_active_stage == stage))
        for key in ("web_copy", "web_receive"):
            button = bundle.get(key)
            if button is not None:
                button.setEnabled(bool(needed))

        label = bundle.get("label")
        if label is None:
            continue
        if heuristic_running and active_stage == stage:
            phase_text = progress_phase or "STARTING_QTHREAD_WORKER"
            label.setText(
                "Heuristic correction worker active: "
                + phase_text
                + ". Other correction routes remain available; choosing another worker route abandons this result fail-closed."
            )
        elif local_running and local_active_stage == stage:
            phase_text = local_progress_phase or "STARTING_QTHREAD_WORKER"
            label.setText(
                "Local AI correction worker active: "
                + phase_text
                + ". Other correction routes remain available; choosing Heuristic abandons this Local AI result fail-closed."
            )
        elif local_job_alive:
            label.setText(
                "A canceled or timed-out Local AI worker is settling in the background. "
                "Its result is stale; all correction routes remain reusable for the current blocker."
            )
        elif needed:
            label.setText(
                "Blocked evidence detected. Heuristic, Local AI, and Web AI routes remain reusable until one accepted replacement retires this blocker."
            )
        else:
            label.setText(
                "Correction routes: available only after this stage reports blocked evidence."
            )

def sync_workbench_stage_correction_controls_from_window(window: object) -> None:
    """Refresh correction controls from callbacks owned by the Workbench shell."""
    root_callback = getattr(
        window,
        "_large_file_refactor_workbench_root_text_callback",
        None,
    )
    if callable(root_callback):
        sync_workbench_stage_correction_controls(window, root_callback)

def _run_heuristic(
    window: object,
    stage: str,
    root_text_callback: Callable[[object], str],
    sync_callback: Callable[[object], None],
) -> None:
    """Capture current card context and launch the Qt-native Heuristic worker."""
    abandon_local_ai_before_heuristic(
        window,
        _render_correction_result,
        sync_callback,
    )
    context = build_stage_correction_context(
        window,
        stage,
        root_text_callback(window),
    )
    plan = materialize_workbench_owned_plan(window)
    _render_correction_result(
        window,
        stage,
        "HEURISTIC CORRECTION STARTED\n"
        "A Qt-native worker is building a bounded AST/static candidate. "
        "Correction-time Git history re-query is intentionally skipped. "
        "No downstream gate will open until deterministic rerun evidence passes.",
    )
    started = start_heuristic_correction(
        window=window,
        stage=stage,
        plan=plan,
        context=context,
        render_result=_render_correction_result,
        render_intake=_render_new_intake,
        render_replay=_render_replay_evidence,
        sync_callback=sync_callback,
    )
    if not started:
        _render_correction_result(
            window,
            stage,
            "HEURISTIC CORRECTION NOT STARTED\nAnother Heuristic worker is still alive or a correction route already owns the stage.",
        )
    sync_callback(window)

def _cancel_heuristic(
    window: object,
    stage: str,
    sync_callback: Callable[[object], None],
) -> None:
    """Abandon the current Heuristic wait without accepting late results."""
    cancel_heuristic_correction(
        window,
        stage,
        _render_correction_result,
        sync_callback,
    )

def _start_local_ai(
    window: object,
    stage: str,
    root_text_callback: Callable[[object], str],
    sync_callback: Callable[[object], None],
) -> None:
    """Launch one bounded Qt-native Local AI correction generation."""
    abandon_heuristic_before_local_ai(
        window,
        _render_correction_result,
        sync_callback,
    )
    state = local_ai_execution_state(window)
    if state.waiting:
        return
    context = build_stage_correction_context(
        window,
        stage,
        root_text_callback(window),
    )
    plan = materialize_workbench_owned_plan(window)
    proposals = list(
        getattr(window, "_large_file_refactor_docstring_proposals", []) or []
    )
    _render_correction_result(
        window,
        stage,
        "LOCAL AI CORRECTION STARTED\n"
        "The exact blocker context and PASS objective are running through a "
        "bounded single-track Qt worker. Tournament fan-out is disabled for "
        "this recovery lane. No downstream gate opens until deterministic "
        "rerun evidence passes.",
    )
    started = start_local_ai_correction(
        window=window,
        stage=stage,
        plan=plan,
        proposals=proposals,
        context=context,
        render_result=_render_correction_result,
        render_intake=_render_new_intake,
        sync_callback=sync_callback,
    )
    if not started:
        _render_correction_result(
            window,
            stage,
            "LOCAL AI CORRECTION NOT STARTED\n"
            "Another Local AI worker is still alive or the route already owns "
            "the current generation.",
        )
    sync_callback(window)

def _cancel_local_ai(
    window: object,
    stage: str,
    sync_callback: Callable[[object], None],
) -> None:
    """Abandon the current Local AI wait without accepting late results."""
    cancel_local_ai_correction(
        window,
        stage,
        _render_correction_result,
        sync_callback,
    )

def _copy_web_ai(
    window: object,
    stage: str,
    root_text_callback: Callable[[object], str],
) -> None:
    context = build_stage_correction_context(window, stage, root_text_callback(window))
    try:
        prompt = build_web_ai_workbench_correction_prompt(window, context)
    except Exception as exc:
        _render_correction_result(window, stage, "WEB AI CORRECTION PACKAGE BLOCKED\n" + str(exc))
        return
    QApplication.clipboard().setText(prompt)
    _render_correction_result(
        window,
        stage,
        "WEB AI CORRECTION PACKAGE COPIED\nThe package contains the exact stage, status, blockers, warnings, evidence-chain statuses, target identity, error output, and the objective required to reach the next governed phase. Install the returned Web AI version, then use Receive Web AI Correction.",
    )

def _receive_web_ai(
    window: object,
    stage: str,
    root_text_callback: Callable[[object], str],
    sync_callback: Callable[[object], None],
) -> None:
    abandon_workers_before_web_receive(
        window,
        _render_correction_result,
        sync_callback,
    )
    current_plan = materialize_workbench_owned_plan(window)
    open_receive_planning_from_web_ai(window, refresh_callback=lambda _window: None, base_plan=current_plan, base_docstring_proposals=list(getattr(current_plan, "docstring_proposals", ()) or ()))
    if not bool(getattr(window, "_large_file_refactor_web_ai_proposal_applied", False)):
        _render_correction_result(window, stage, "No imported Web AI correction was loaded.")
        sync_callback(window)
        return
    if not web_ai_plan_materially_changes(window, current_plan):
        _render_correction_result(
            window,
            stage,
            "Imported Web AI correction was rejected as a no-op. The current blocker remains active and all correction routes remain reusable.",
        )
        sync_callback(window)
        return
    select_planner_version(window, PLANNER_VERSION_WEB_AI)
    intake, message = load_latest_snapshot_into_workbench(window, root_text_callback(window))
    if intake is None:
        _render_correction_result(
            window,
            stage,
            "Imported Web AI correction was accepted, but Workbench reload was blocked. " + message,
        )
    else:
        _render_new_intake(window, intake)
        if stage == "ADVANCED_QUALITY_REVIEW":
            note_aqr_correction_candidate(window, "web_ai")
        _render_correction_result(
            window,
            stage,
            "Imported Web AI correction loaded into Workbench ownership. The unresolved AQR correction session remains active; rerun deterministic stages while Heuristic, Local AI, and Web AI alternatives remain reusable until a fresh AQR PASS retires the blocker.",
        )
    sync_callback(window)

def _render_new_intake(window: object, intake: object) -> None:
    window._large_file_refactor_workbench_intake = intake
    window._large_file_refactor_workbench_state = (
        "READY_FOR_REAL_PREVIEW"
        if bool(getattr(intake, "ready_for_real_preview", False))
        else "BLOCKED"
    )
    output = getattr(window, "_large_file_refactor_workbench_intake_output", None)
    if output is not None:
        output.setPlainText(format_workbench_intake(intake))
    _schedule_global_workbench_projection(window)

def _schedule_global_workbench_projection(window: object) -> None:
    """Project the accepted intake now and once after the Qt event turn."""
    callback = getattr(
        window,
        "_large_file_refactor_workbench_global_sync_callback",
        None,
    )
    if not callable(callback):
        return
    callback(window)
    QTimer.singleShot(0, lambda: callback(window))

def _render_replay_evidence(window: object, replay: object) -> None:
    """Render exact accepted replay evidence into the same Workbench panels as normal execution."""
    dependency = getattr(replay, "dependency_readiness", None)
    if dependency is not None:
        output = getattr(window, "_large_file_refactor_workbench_dependency_output", None)
        if output is not None:
            output.setPlainText(format_workbench_dependency_readiness(dependency))

    preview = getattr(replay, "real_preview", None)
    if preview is not None:
        output = getattr(window, "_large_file_refactor_workbench_real_preview_output", None)
        if output is not None:
            output.setPlainText(format_real_preview_result(preview))

    structural = getattr(replay, "structural_validation", None)
    validation_output = getattr(
        window,
        "_large_file_refactor_workbench_validation_output",
        None,
    )
    if structural is not None and validation_output is not None:
        validation_output.setPlainText(
            format_real_preview_structural_validation(structural)
        )
    elif preview is not None and validation_output is not None:
        validation_output.setPlainText(preview_validation_guidance(preview))

    preflight = getattr(replay, "preflight_backup", None)
    if preflight is not None:
        output = getattr(window, "_large_file_refactor_workbench_preflight_output", None)
        if output is not None:
            output.setPlainText(format_preflight_backup_readiness(preflight))

    source_payload = getattr(replay, "source_payload", None)
    if source_payload is not None:
        output = getattr(
            window,
            "_large_file_refactor_workbench_source_payload_output",
            None,
        )
        if output is not None:
            output.setPlainText(
                format_source_apply_payload_readiness(source_payload)
            )

    completion = getattr(replay, "completion_evidence", None)
    if completion is not None:
        output = getattr(
            window,
            "_large_file_refactor_workbench_completion_status_output",
            None,
        )
        if output is not None:
            output.setPlainText(
                "COMPLETION EVIDENCE RESTORED FROM ACCEPTED HEURISTIC REPLAY\n"
                "The Workbench state was projected only from target-stage PASS evidence."
            )

def _render_correction_result(window: object, stage: str, message: str) -> None:
    """Append correction status without copying and replacing the whole output buffer."""
    output = getattr(window, _OUTPUT_ATTR[stage], None)
    if output is None:
        return
    output.appendPlainText("\n--- CORRECTION LANE ---\n" + str(message))
