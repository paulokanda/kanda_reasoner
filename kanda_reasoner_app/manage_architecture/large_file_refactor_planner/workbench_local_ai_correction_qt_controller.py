"""Qt-native lifecycle controller for bounded Workbench Local AI corrections."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QObject, QThread, QTimer, Slot

from .workbench_local_ai_correction_models import (
    LocalAIWorkbenchCorrectionCandidate,
)
from .workbench_local_ai_correction_qt_worker import (
    WorkbenchLocalAICorrectionWorker,
)
from .workbench_local_ai_correction_sonar import (
    finish_local_ai_correction_sonar_error,
    finish_local_ai_correction_sonar_success,
    start_local_ai_correction_sonar,
    update_local_ai_correction_sonar,
)
from .workbench_stage_correction_context import WorkbenchStageCorrectionContext
from .workbench_stage_correction_service import apply_local_ai_workbench_correction

__all__ = [
    "LocalAIExecutionState",
    "cancel_local_ai_correction",
    "local_ai_execution_state",
    "start_local_ai_correction",
]

_LOCAL_AI_TIMEOUT_MS = 120_000

RenderResult = Callable[[object, str, str], None]
RenderIntake = Callable[[object, object], None]
SyncCallback = Callable[[object], None]


@dataclass(frozen=True)
class LocalAIExecutionState:
    """GUI projection of one window's Local AI correction lifecycle."""

    waiting: bool
    active_stage: str
    progress_phase: str
    background_job_alive: bool


class _GuiReceiver(QObject):
    """Receive Local AI worker signals on the GUI thread."""

    def __init__(
        self,
        *,
        window: object,
        stage: str,
        generation: int,
        context: WorkbenchStageCorrectionContext,
        render_result: RenderResult,
        render_intake: RenderIntake,
        sync_callback: SyncCallback,
    ) -> None:
        super().__init__()
        self._window = window
        self._stage = stage
        self._generation = generation
        self._context = context
        self._render_result = render_result
        self._render_intake = render_intake
        self._sync_callback = sync_callback

    @Slot(str)
    def on_progress(self, phase: str) -> None:
        _handle_progress(
            self._window,
            self._generation,
            phase,
            self._sync_callback,
        )

    @Slot(object)
    def on_result(self, candidate: object) -> None:
        _handle_result(
            self._window,
            self._stage,
            self._generation,
            self._context,
            candidate,
            self._render_result,
            self._render_intake,
            self._sync_callback,
        )


def start_local_ai_correction(
    *,
    window: object,
    stage: str,
    plan: Any,
    proposals: list[Any],
    context: WorkbenchStageCorrectionContext,
    render_result: RenderResult,
    render_intake: RenderIntake,
    sync_callback: SyncCallback,
) -> bool:
    """Start one bounded Local AI Qt worker generation."""
    state = local_ai_execution_state(window)
    if state.waiting:
        return False

    generation = int(
        getattr(window, "_workbench_stage_local_ai_generation", 0) or 0
    ) + 1
    window._workbench_stage_local_ai_generation = generation
    window._workbench_stage_local_ai_correction_running = True
    window._workbench_stage_local_ai_active_stage = stage
    window._workbench_stage_local_ai_progress_phase = "STARTING_QTHREAD_WORKER"

    thread = QThread()
    worker = WorkbenchLocalAICorrectionWorker(
        plan=plan,
        proposals=proposals,
        context=context,
    )
    receiver = _GuiReceiver(
        window=window,
        stage=stage,
        generation=generation,
        context=context,
        render_result=render_result,
        render_intake=render_intake,
        sync_callback=sync_callback,
    )
    worker.moveToThread(thread)

    watchdog = QTimer()
    watchdog.setSingleShot(True)
    watchdog.setInterval(_LOCAL_AI_TIMEOUT_MS)

    jobs = _jobs(window)
    jobs[generation] = {
        "thread": thread,
        "worker": worker,
        "receiver": receiver,
        "watchdog": watchdog,
        "stage": stage,
        "accept_result": True,
        "result_delivered": False,
        "thread_finished": False,
        "sync_callback": sync_callback,
    }

    thread.started.connect(worker.run)
    worker.progress.connect(receiver.on_progress)
    worker.result_ready.connect(receiver.on_result)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(
        lambda generation=generation: _mark_thread_finished(window, generation)
    )
    watchdog.timeout.connect(
        lambda generation=generation: _timeout_job(
            window,
            stage,
            generation,
            render_result,
            sync_callback,
        )
    )

    start_local_ai_correction_sonar(window, stage)
    thread.start()
    watchdog.start()
    sync_callback(window)
    return True


def cancel_local_ai_correction(
    window: object,
    stage: str,
    render_result: RenderResult,
    sync_callback: SyncCallback,
) -> None:
    """Abandon the current Local AI result without opening downstream gates."""
    generation = int(
        getattr(window, "_workbench_stage_local_ai_generation", 0) or 0
    )
    job = _jobs(window).get(generation)
    if not job or str(job.get("stage", "")) != stage:
        return
    _abandon_job(window, job)
    message = (
        "LOCAL AI CORRECTION WAIT CANCELED\n"
        "The current Local AI result is stale and will be ignored. No PASS was "
        "synthesized and no downstream gate was opened. Heuristic and Web AI "
        "correction routes remain available."
    )
    render_result(window, stage, message)
    finish_local_ai_correction_sonar_error(window, message)
    sync_callback(window)


def local_ai_execution_state(window: object) -> LocalAIExecutionState:
    """Return exact Local AI worker lifecycle state for GUI projection."""
    waiting = bool(
        getattr(window, "_workbench_stage_local_ai_correction_running", False)
    )
    active_stage = str(
        getattr(window, "_workbench_stage_local_ai_active_stage", "") or ""
    )
    progress_phase = str(
        getattr(window, "_workbench_stage_local_ai_progress_phase", "") or ""
    )
    alive = any(
        bool(job.get("thread") and job["thread"].isRunning())
        for job in _jobs(window).values()
        if isinstance(job, dict)
    )
    return LocalAIExecutionState(
        waiting=waiting,
        active_stage=active_stage,
        progress_phase=progress_phase,
        background_job_alive=alive,
    )


def _handle_progress(
    window: object,
    generation: int,
    phase: str,
    sync_callback: SyncCallback,
) -> None:
    job = _jobs(window).get(generation)
    if not job or not bool(job.get("accept_result", False)):
        return
    if generation != int(
        getattr(window, "_workbench_stage_local_ai_generation", 0) or 0
    ):
        return
    window._workbench_stage_local_ai_progress_phase = str(phase)
    update_local_ai_correction_sonar(
        window,
        str(job.get("stage", "")),
        str(phase),
    )
    sync_callback(window)


def _handle_result(
    window: object,
    stage: str,
    generation: int,
    context: WorkbenchStageCorrectionContext,
    candidate: object,
    render_result: RenderResult,
    render_intake: RenderIntake,
    sync_callback: SyncCallback,
) -> None:
    job = _jobs(window).get(generation)
    if not job:
        return
    job["result_delivered"] = True
    if not bool(job.get("accept_result", False)):
        _cleanup_if_terminal(window, generation)
        return
    if generation != int(
        getattr(window, "_workbench_stage_local_ai_generation", 0) or 0
    ):
        job["accept_result"] = False
        _cleanup_if_terminal(window, generation)
        return

    job["accept_result"] = False
    job["ui_result_settled"] = True
    watchdog = job.get("watchdog")
    if watchdog is not None:
        watchdog.stop()
    _clear_waiting_state(window)

    if not isinstance(candidate, LocalAIWorkbenchCorrectionCandidate):
        message = (
            "LOCAL AI CORRECTION FAILED\n"
            "Worker returned an unsupported result object."
        )
        render_result(window, stage, message)
        finish_local_ai_correction_sonar_error(window, message)
    else:
        result = apply_local_ai_workbench_correction(window, context, candidate)
        if result.intake is not None:
            render_intake(window, result.intake)
        render_result(window, stage, result.message)
        if result.ok:
            finish_local_ai_correction_sonar_success(window, result.message)
        else:
            finish_local_ai_correction_sonar_error(window, result.message)
    _request_thread_quit(job)
    sync_callback(window)
    QTimer.singleShot(
        0,
        lambda: _sync_after_result(window, generation, sync_callback),
    )
    _cleanup_if_terminal(window, generation)


def _request_thread_quit(job: dict[str, object]) -> None:
    """Ensure a result-bearing worker thread leaves its event loop."""
    thread = job.get("thread")
    if thread is not None and thread.isRunning():
        thread.quit()


def _sync_after_result(
    window: object,
    generation: int,
    sync_callback: SyncCallback,
) -> None:
    """Reproject Workbench controls after queued intake/render events settle."""
    current = int(
        getattr(window, "_workbench_stage_local_ai_generation", 0) or 0
    )
    if generation == current:
        sync_callback(window)


def _timeout_job(
    window: object,
    stage: str,
    generation: int,
    render_result: RenderResult,
    sync_callback: SyncCallback,
) -> None:
    job = _jobs(window).get(generation)
    if not job or not bool(job.get("accept_result", False)):
        return
    _abandon_job(window, job)
    message = (
        "LOCAL AI CORRECTION TIMEOUT\n"
        "The bounded correction route did not settle within 120 seconds. The "
        "late result will be ignored. No PASS was synthesized and no downstream "
        "gate was opened. Heuristic and Web AI correction routes remain available."
    )
    render_result(window, stage, message)
    finish_local_ai_correction_sonar_error(window, message)
    sync_callback(window)


def _abandon_job(window: object, job: dict[str, object]) -> None:
    job["accept_result"] = False
    thread = job.get("thread")
    if thread is not None:
        thread.requestInterruption()
    watchdog = job.get("watchdog")
    if watchdog is not None:
        watchdog.stop()
    _clear_waiting_state(window)


def _clear_waiting_state(window: object) -> None:
    window._workbench_stage_local_ai_correction_running = False
    window._workbench_stage_local_ai_active_stage = ""
    window._workbench_stage_local_ai_progress_phase = ""


def _mark_thread_finished(window: object, generation: int) -> None:
    job = _jobs(window).get(generation)
    if not job:
        return
    job["thread_finished"] = True
    _cleanup_if_terminal(window, generation)


def _cleanup_if_terminal(window: object, generation: int) -> None:
    job = _jobs(window).get(generation)
    if not job or not bool(job.get("thread_finished", False)):
        return
    if bool(job.get("accept_result", False)) and not bool(
        job.get("result_delivered", False)
    ):
        QTimer.singleShot(0, lambda: _cleanup_if_terminal(window, generation))
        return
    _cleanup_job(window, generation)


def _cleanup_job(window: object, generation: int) -> None:
    job = _jobs(window).pop(generation, None)
    if not job:
        return
    watchdog = job.get("watchdog")
    if watchdog is not None:
        watchdog.stop()
        watchdog.deleteLater()
    receiver = job.get("receiver")
    if receiver is not None:
        receiver.deleteLater()
    thread = job.get("thread")
    if thread is not None:
        thread.deleteLater()
    sync_callback = job.get("sync_callback")
    if callable(sync_callback):
        sync_callback(window)


def _jobs(window: object) -> dict[int, dict[str, object]]:
    jobs = getattr(window, "_workbench_stage_local_ai_jobs", None)
    if not isinstance(jobs, dict):
        jobs = {}
        window._workbench_stage_local_ai_jobs = jobs
    return jobs
