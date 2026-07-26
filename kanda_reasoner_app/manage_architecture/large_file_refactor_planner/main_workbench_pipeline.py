# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_pipeline.py
"""Schedule Workbench stages without owning source mutation or transaction authority."""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QObject, QTimer, Slot

from .advanced_quality_review_gui import (
    advanced_quality_review_runtime_running,
    cancel_advanced_quality_review_for_window,
    start_advanced_quality_review_for_window,
)
from .main_workbench_aqr_retry import (
    AQR_RETRY_READY,
    AQR_RETRY_TIMEOUT,
    AqrStartSettlementGate,
)
from .main_workbench_pipeline_models import (
    MAIN_WORKBENCH_CANCELLED,
    MAIN_WORKBENCH_FAILED,
    MAIN_WORKBENCH_READY,
    MAIN_WORKBENCH_STALE,
    MAIN_WORKBENCH_WEB_AI_BLOCKED,
    MainWorkbenchControllerState,
    aqr_is_ready,
    aqr_is_terminal,
    result_blockers,
)
from .main_workbench_state_store import (
    MainWorkbenchTerminalSeal,
    build_main_workbench_terminal_seal,
    write_main_workbench_terminal_seal,
)
from .main_workbench_stage_adapters import (
    apply_dependency_stage_result,
    apply_preview_stage_result,
    apply_structural_stage_result,
    capture_dependency_stage_request,
    capture_preview_stage_request,
    capture_structural_stage_request,
    execute_dependency_stage,
    execute_preview_stage,
    execute_structural_stage,
)
from .main_workbench_stage_worker import (
    MainWorkbenchStageJob,
    launch_main_workbench_stage_job,
)
from .workbench_snapshot_bridge import workbench_source_transaction_open
from .workbench_gui import (
    recheck_workbench_pipeline_source,
    run_workbench_plan_intake_stage,
    sync_workbench_controls,
)

__all__ = ["MainWorkbenchController"]

StatusCallback = Callable[["MainWorkbenchControllerState"], None]
RootCallback = Callable[[object], str]


class MainWorkbenchController(QObject):
    """Schedule existing Workbench stages and reject stale generations."""

    def __init__(
        self,
        *,
        window: object,
        root_callback: RootCallback,
        status_callback: StatusCallback,
    ) -> None:
        super().__init__()
        self._window = window
        self._root_callback = root_callback
        self._status_callback = status_callback
        self._generation = 0
        self._running = False
        self._cancel_requested = False
        self._stage = "IDLE"
        self._terminal_status = ""
        self._message = "Main Workbench has not run."
        self._blockers: tuple[str, ...] = ()
        self._seal: MainWorkbenchTerminalSeal | None = None
        self._aqr_poll_generation = 0
        self._aqr_poll_timer = QTimer(self)
        self._aqr_poll_timer.setInterval(180)
        self._aqr_poll_timer.timeout.connect(self._poll_aqr)
        self._aqr_start_gate = AqrStartSettlementGate()
        self._stage_job: MainWorkbenchStageJob | None = None

    def start(self) -> bool:
        """Start one pipeline generation when no generation is active."""
        if self._running or workbench_source_transaction_open(self._window):
            return False
        self._generation += 1
        self._running = True
        self._cancel_requested = False
        self._terminal_status = ""
        self._blockers = ()
        self._seal = None
        self._set_stage("PLAN_INTAKE", "Capturing the selected Planner plan.")
        QTimer.singleShot(
            0,
            lambda: self._run_stage(self._generation, "PLAN_INTAKE"),
        )
        return True

    def cancel(self) -> bool:
        """Request cooperative cancellation and cancel AQR when active."""
        if not self._running or self._cancel_requested:
            return False
        self._cancel_requested = True
        if self._stage == "ADVANCED_QUALITY_REVIEW":
            cancel_advanced_quality_review_for_window(self._window)
        if self._stage_job is not None:
            self._stage_job.request_cancel()
        self._publish("Cancellation requested. No new stage will be scheduled.")
        return True

    def state(self) -> MainWorkbenchControllerState:
        return MainWorkbenchControllerState(
            generation=self._generation,
            running=self._running,
            cancel_requested=self._cancel_requested,
            stage=self._stage,
            terminal_status=self._terminal_status,
            message=self._message,
            blockers=self._blockers,
        )

    def terminal_seal(self) -> MainWorkbenchTerminalSeal | None:
        return self._seal

    def _run_stage(self, generation: int, stage: str) -> None:
        if not self._accept_generation(generation):
            return
        if self._cancel_requested:
            self._finish(MAIN_WORKBENCH_CANCELLED, "Pipeline cancelled.")
            return
        if stage != "PLAN_INTAKE" and not self._source_fresh():
            self._finish_stale()
            return
        try:
            if stage == "PLAN_INTAKE":
                self._run_plan_intake(generation)
            elif stage == "DEPENDENCY_READINESS":
                self._run_dependency(generation)
            elif stage == "REAL_PREVIEW":
                self._run_preview(generation)
            elif stage == "STRUCTURAL_VALIDATION":
                self._run_structural(generation)
            elif stage == "ADVANCED_QUALITY_REVIEW":
                self._start_aqr(generation)
            else:
                self._finish(
                    MAIN_WORKBENCH_FAILED,
                    "Unknown pipeline stage: " + stage,
                )
        except Exception as error:
            self._finish(
                MAIN_WORKBENCH_FAILED,
                type(error).__name__ + ":" + str(error),
                blockers=("PIPELINE_STAGE_EXCEPTION:" + stage,),
            )

    def _run_plan_intake(self, generation: int) -> None:
        result = run_workbench_plan_intake_stage(self._window)
        if result is None or not bool(
            getattr(result, "workbench_snapshot_owned", False)
        ):
            self._finish_failed(
                "Plan Intake did not transfer Workbench ownership.",
                result,
            )
            return
        if not bool(getattr(result, "ready_for_real_preview", False)):
            self._finish_failed(
                "Planner plan is not ready for automatic Preview.",
                result,
            )
            return
        self._schedule_next(generation, "DEPENDENCY_READINESS")

    def _run_dependency(self, generation: int) -> None:
        request = capture_dependency_stage_request(self._window)
        self._start_background_stage(
            generation=generation,
            stage="DEPENDENCY_READINESS",
            request=request,
            execute=execute_dependency_stage,
        )

    def _run_preview(self, generation: int) -> None:
        request = capture_preview_stage_request(
            self._window,
            self._root_callback,
        )
        self._start_background_stage(
            generation=generation,
            stage="REAL_PREVIEW",
            request=request,
            execute=execute_preview_stage,
        )

    def _run_structural(self, generation: int) -> None:
        request = capture_structural_stage_request(
            self._window,
            self._root_callback,
        )
        self._start_background_stage(
            generation=generation,
            stage="STRUCTURAL_VALIDATION",
            request=request,
            execute=execute_structural_stage,
        )

    def _start_background_stage(
        self,
        *,
        generation: int,
        stage: str,
        request: object,
        execute: Callable[[object], object],
    ) -> None:
        if self._stage_job is not None and self._stage_job.running():
            raise RuntimeError("MAIN_WORKBENCH_STAGE_WORKER_ALREADY_RUNNING")
        self._stage_job = launch_main_workbench_stage_job(
            generation=generation,
            stage=stage,
            request=request,
            execute=execute,
            settled_callback=self._stage_worker_settled,
        )

    @Slot(int, str)
    def _stage_worker_settled(self, generation: int, stage: str) -> None:
        job = self._stage_job
        if job is None or job.generation != generation or job.stage != stage:
            return
        self._stage_job = None
        if not self._accept_generation(generation):
            return
        if self._cancel_requested:
            self._finish(MAIN_WORKBENCH_CANCELLED, "Pipeline cancelled.")
            return
        if not self._source_fresh():
            self._finish_stale()
            return
        if job.failure_text:
            self._finish(
                MAIN_WORKBENCH_FAILED,
                job.failure_text,
                blockers=("PIPELINE_STAGE_EXCEPTION:" + stage,),
            )
            return
        if not job.result_received:
            self._finish(
                MAIN_WORKBENCH_FAILED,
                "Stage worker settled without a result: " + stage,
                blockers=("PIPELINE_STAGE_RESULT_MISSING:" + stage,),
            )
            return
        self._apply_background_stage_result(generation, stage, job.result)

    def _apply_background_stage_result(
        self,
        generation: int,
        stage: str,
        result: object,
    ) -> None:
        if stage == "DEPENDENCY_READINESS":
            apply_dependency_stage_result(
                self._window,
                result,
                sync_workbench_controls,
            )
            if not bool(getattr(result, "ready_for_real_preview_writer", False)):
                self._finish_failed("Dependency Readiness is blocked.", result)
                return
            self._schedule_next(generation, "REAL_PREVIEW")
            return
        if stage == "REAL_PREVIEW":
            apply_preview_stage_result(
                self._window,
                result,
                sync_workbench_controls,
            )
            if str(getattr(result, "status", "")) != "real_preview_written":
                self._finish_failed("Real Preview was not written.", result)
                return
            if tuple(getattr(result, "blockers", ()) or ()):
                self._finish_failed("Real Preview contains blocking evidence.", result)
                return
            self._schedule_next(generation, "STRUCTURAL_VALIDATION")
            return
        if stage == "STRUCTURAL_VALIDATION":
            apply_structural_stage_result(
                self._window,
                result,
                sync_workbench_controls,
            )
            if not str(getattr(result, "status", "")).startswith("passed"):
                self._finish_packageable(
                    "Structural Validation is blocked. The complete Preview and "
                    "blocker evidence can be sent to Web AI.",
                    result,
                )
                return
            self._schedule_next(generation, "ADVANCED_QUALITY_REVIEW")
            return
        self._finish(
            MAIN_WORKBENCH_FAILED,
            "Unknown completed worker stage: " + stage,
        )

    def _schedule_next(self, generation: int, stage: str) -> None:
        self._set_stage(
            stage,
            "Running " + stage.replace("_", " ").title() + ".",
        )
        QTimer.singleShot(0, lambda: self._run_stage(generation, stage))

    def _start_aqr(self, generation: int) -> None:
        self._set_stage("ADVANCED_QUALITY_REVIEW", "Advanced Quality Review is running.")
        started = start_advanced_quality_review_for_window(self._window)
        if not started and advanced_quality_review_runtime_running(self._window):
            self._aqr_start_gate.begin()
            self._aqr_poll_generation = generation
            self._aqr_poll_timer.start()
            self._publish("Waiting for the previous AQR generation to settle.")
            return
        if not started:
            terminal = self._aqr_terminal_status()
            if terminal:
                self._evaluate_aqr_terminal(terminal)
                return
            self._finish(
                MAIN_WORKBENCH_FAILED,
                "Advanced Quality Review could not start.",
                blockers=("AQR_START_BLOCKED",),
            )
            return
        self._aqr_start_gate.reset()
        self._aqr_poll_generation = generation
        self._aqr_poll_timer.start()

    def _poll_aqr(self) -> None:
        if not self._accept_generation(self._aqr_poll_generation):
            self._aqr_poll_timer.stop()
            return
        if self._aqr_start_gate.pending:
            transition = self._aqr_start_gate.observe(
                advanced_quality_review_runtime_running(self._window)
            )
            if transition == AQR_RETRY_TIMEOUT:
                self._finish(
                    MAIN_WORKBENCH_FAILED,
                    "Previous AQR generation did not settle before retry timeout.",
                    blockers=("AQR_PREVIOUS_GENERATION_SETTLEMENT_TIMEOUT",),
                )
                return
            if transition == AQR_RETRY_READY:
                self._aqr_poll_timer.stop()
                self._start_aqr(self._aqr_poll_generation)
            return
        terminal = self._aqr_terminal_status()
        if not terminal or terminal == "CANCEL_REQUESTED":
            return
        if not aqr_is_terminal(terminal):
            return
        self._aqr_poll_timer.stop()
        if not self._source_fresh():
            self._finish_stale()
            return
        if self._cancel_requested or terminal == "CANCELLED":
            self._finish(
                MAIN_WORKBENCH_CANCELLED,
                "Advanced Quality Review was cancelled.",
            )
            return
        self._evaluate_aqr_terminal(terminal)

    def _evaluate_aqr_terminal(self, terminal: str) -> None:
        if aqr_is_ready(terminal):
            self._finish(
                MAIN_WORKBENCH_READY,
                "Deterministic Workbench evidence is sealed and ready for Web AI.",
            )
            return
        outcome = getattr(
            self._window,
            "_large_file_refactor_workbench_advanced_quality_review",
            None,
        )
        self._finish_packageable(
            "Advanced Quality Review requires external semantic review. The complete "
            "candidate family and exact blocker evidence can be sent to Web AI.",
            outcome,
        )

    def _aqr_terminal_status(self) -> str:
        return str(
            getattr(
                self._window,
                "_large_file_refactor_workbench_aqr_terminal_status",
                "",
            )
            or ""
        )

    def _source_fresh(self) -> bool:
        intake = recheck_workbench_pipeline_source(self._window)
        return bool(intake and getattr(intake, "source_hash_fresh", False))

    def _finish_stale(self) -> None:
        self._finish(
            MAIN_WORKBENCH_STALE,
            "The project source changed outside this Workbench transaction. "
            "Reload the card and create a fresh pipeline.",
            blockers=("STALE_SOURCE",),
        )

    def _finish_failed(self, message: str, result: object | None) -> None:
        self._finish(
            MAIN_WORKBENCH_FAILED,
            message,
            blockers=result_blockers(result),
        )

    def _finish_packageable(self, message: str, result: object | None) -> None:
        preview = getattr(
            self._window,
            "_large_file_refactor_workbench_real_preview",
            None,
        )
        if preview is None or str(getattr(preview, "status", "")) != "real_preview_written":
            self._finish_failed(message, result)
            return
        self._finish(
            MAIN_WORKBENCH_WEB_AI_BLOCKED,
            message,
            blockers=result_blockers(result),
        )

    def _finish(
        self,
        terminal_status: str,
        message: str,
        *,
        blockers: tuple[str, ...] = (),
    ) -> None:
        self._aqr_poll_timer.stop()
        self._aqr_start_gate.reset()
        normalized_blockers = tuple(sorted(set(blockers)))
        if terminal_status in {
            MAIN_WORKBENCH_READY,
            MAIN_WORKBENCH_WEB_AI_BLOCKED,
        } and not self._source_fresh():
            terminal_status = MAIN_WORKBENCH_STALE
            message = (
                "The project source changed outside this Workbench transaction. "
                "Reload the card and create a fresh pipeline."
            )
            normalized_blockers = tuple(
                sorted(set(normalized_blockers + ("STALE_SOURCE",)))
            )
        self._running = False
        self._stage = "TERMINAL"
        self._terminal_status = terminal_status
        self._message = message
        self._blockers = normalized_blockers
        if terminal_status in {
            MAIN_WORKBENCH_READY,
            MAIN_WORKBENCH_WEB_AI_BLOCKED,
        }:
            self._seal = build_main_workbench_terminal_seal(
                self._window,
                active_project_root=self._root_callback(self._window),
                generation=self._generation,
                terminal_status=terminal_status,
                blockers=self._blockers,
            )
            write_main_workbench_terminal_seal(self._seal)
        self._publish(message)

    def _set_stage(self, stage: str, message: str) -> None:
        self._stage = stage
        self._publish(message)

    def _publish(self, message: str) -> None:
        self._message = message
        self._status_callback(self.state())

    def _accept_generation(self, generation: int) -> bool:
        return bool(self._running and generation == self._generation)
