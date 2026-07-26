# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_review_qt_controller.py
"""Qt lifecycle controller for one Advanced Quality Review generation."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtCore import QObject, QThread, Slot

from .advanced_quality_review_orchestration import (
    AdvancedQualityReviewExecutionPlan,
    AdvancedQualityReviewOutcome,
    AdvancedQualityReviewRequest,
)
from .advanced_quality_review_qt_worker import AdvancedQualityReviewWorker
from .analyzer_process_runtime import CancellationToken

__all__ = [
    "AdvancedQualityReviewController",
    "AdvancedQualityReviewControllerState",
]

ProgressCallback = Callable[[str, str], None]
OutcomeCallback = Callable[[AdvancedQualityReviewOutcome], None]
FailureCallback = Callable[[str], None]
SettledCallback = Callable[[bool], None]
CurrentIdentityHash = Callable[[], str]


@dataclass(frozen=True)
class AdvancedQualityReviewControllerState:
    """Project one controller lifecycle without owning GUI widget state."""

    generation: int
    running: bool
    cancel_requested: bool
    terminal_received: bool
    progress_stage: str
    progress_message: str


class _ReviewReceiver(QObject):
    """Receive worker signals on the GUI thread and enforce lineage freshness."""

    def __init__(
        self,
        *,
        controller: "AdvancedQualityReviewController",
        generation: int,
        expected_identity_hash: str,
    ) -> None:
        super().__init__()
        self._controller = controller
        self._generation = generation
        self._expected_identity_hash = expected_identity_hash

    @Slot(str, str)
    def on_progress(self, stage: str, message: str) -> None:
        self._controller._handle_progress(self._generation, stage, message)

    @Slot(object)
    def on_result(self, outcome: object) -> None:
        self._controller._handle_result(
            self._generation,
            self._expected_identity_hash,
            outcome,
        )

    @Slot(str)
    def on_failure(self, diagnostic: str) -> None:
        self._controller._handle_failure(self._generation, diagnostic)


class AdvancedQualityReviewController(QObject):
    """Own one QThread worker at a time and reject stale late results."""

    def __init__(
        self,
        *,
        current_identity_hash: CurrentIdentityHash,
        on_progress: ProgressCallback,
        on_outcome: OutcomeCallback,
        on_failure: FailureCallback,
        on_settled: SettledCallback | None = None,
    ) -> None:
        super().__init__()
        self._current_identity_hash = current_identity_hash
        self._on_progress = on_progress
        self._on_outcome = on_outcome
        self._on_failure = on_failure
        self._on_settled = on_settled or (lambda _cancelled: None)
        self._generation = 0
        self._running = False
        self._cancel_requested = False
        self._terminal_received = False
        self._progress_stage = ""
        self._progress_message = ""
        self._jobs: dict[int, dict[str, object]] = {}

    def start(
        self,
        request: AdvancedQualityReviewRequest,
        plan: AdvancedQualityReviewExecutionPlan | None,
    ) -> bool:
        """Start one review generation; reject overlapping execution."""
        if self._running or any(
            bool(job.get("thread") and job["thread"].isRunning())
            for job in self._jobs.values()
        ):
            return False
        self._generation += 1
        generation = self._generation
        expected_hash = request.analysis_identity.identity_hash
        token = CancellationToken()
        thread = QThread()
        worker = AdvancedQualityReviewWorker(
            request=request,
            plan=plan,
            cancellation_token=token,
        )
        receiver = _ReviewReceiver(
            controller=self,
            generation=generation,
            expected_identity_hash=expected_hash,
        )
        worker.moveToThread(thread)
        self._jobs[generation] = {
            "thread": thread,
            "worker": worker,
            "receiver": receiver,
            "token": token,
            "accept_result": True,
        }
        thread.started.connect(worker.run)
        worker.progress.connect(receiver.on_progress)
        worker.result_ready.connect(receiver.on_result)
        worker.failed.connect(receiver.on_failure)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(
            lambda generation=generation: self._handle_thread_finished(generation)
        )
        self._running = True
        self._cancel_requested = False
        self._terminal_received = False
        self._progress_stage = "STARTING"
        self._progress_message = "QThread worker starting."
        thread.start()
        self._on_progress(self._progress_stage, self._progress_message)
        return True

    def cancel(self) -> bool:
        """Request cancellation without synthesizing PASS or accepting late output."""
        job = self._jobs.get(self._generation)
        if (
            not self._running
            or not job
            or self._cancel_requested
            or self._terminal_received
        ):
            return False
        job["accept_result"] = False
        token = job.get("token")
        if isinstance(token, CancellationToken):
            token.cancel()
        worker = job.get("worker")
        if isinstance(worker, AdvancedQualityReviewWorker):
            worker.request_cancel()
        self._cancel_requested = True
        self._progress_stage = "CANCEL_REQUESTED"
        self._progress_message = "Late result will be ignored."
        self._on_progress(self._progress_stage, self._progress_message)
        return True


    def abandon_current_generation(self) -> bool:
        """Retire the current AQR generation after snapshot lineage replacement."""
        job = self._jobs.get(self._generation)
        if not self._running or not job:
            return False
        job["accept_result"] = False
        job["suppress_settled"] = True
        token = job.get("token")
        if isinstance(token, CancellationToken):
            token.cancel()
        worker = job.get("worker")
        if isinstance(worker, AdvancedQualityReviewWorker):
            worker.request_cancel()
        self._progress_stage = "RETIRED_FOR_SNAPSHOT_CHANGE"
        self._progress_message = (
            "Snapshot lineage changed. Late progress and terminal output are discarded."
        )
        return True

    def state(self) -> AdvancedQualityReviewControllerState:
        """Return immutable controller state for future GUI projection."""
        return AdvancedQualityReviewControllerState(
            generation=self._generation,
            running=self._running,
            cancel_requested=self._cancel_requested,
            terminal_received=self._terminal_received,
            progress_stage=self._progress_stage,
            progress_message=self._progress_message,
        )

    def _handle_progress(self, generation: int, stage: str, message: str) -> None:
        job = self._jobs.get(generation)
        if generation != self._generation or not job or not job.get("accept_result"):
            return
        self._progress_stage = str(stage)
        self._progress_message = str(message)
        self._on_progress(self._progress_stage, self._progress_message)

    def _handle_result(
        self,
        generation: int,
        expected_identity_hash: str,
        outcome: object,
    ) -> None:
        job = self._jobs.get(generation)
        if generation != self._generation or not job or not job.get("accept_result"):
            return
        job["accept_result"] = False
        self._terminal_received = True
        if not isinstance(outcome, AdvancedQualityReviewOutcome):
            self._on_failure("AQR_QT_RESULT_TYPE_INVALID")
            return
        if outcome.analysis_identity_hash != expected_identity_hash:
            self._on_failure("AQR_QT_RESULT_IDENTITY_MISMATCH")
            return
        if self._current_identity_hash() != expected_identity_hash:
            self._on_failure("AQR_QT_LATE_RESULT_STALE")
            return
        self._on_outcome(outcome)

    def _handle_failure(self, generation: int, diagnostic: str) -> None:
        job = self._jobs.get(generation)
        if generation != self._generation or not job or not job.get("accept_result"):
            return
        job["accept_result"] = False
        self._terminal_received = True
        self._on_failure(str(diagnostic))

    def _handle_thread_finished(self, generation: int) -> None:
        job = self._jobs.pop(generation, None)
        is_current = generation == self._generation and job is not None
        cancelled = bool(is_current and self._cancel_requested)
        if is_current:
            self._running = False
        if job is not None:
            thread = job.get("thread")
            if thread is not None:
                thread.deleteLater()
        if is_current and not bool(job.get("suppress_settled")):
            self._on_settled(cancelled)
