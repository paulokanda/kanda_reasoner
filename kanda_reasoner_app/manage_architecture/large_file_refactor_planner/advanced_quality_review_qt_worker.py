# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_review_qt_worker.py
"""Qt worker shell for Advanced Quality Review orchestration."""
from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot

from .advanced_quality_review_orchestration import (
    AdvancedQualityReviewExecutionPlan,
    AdvancedQualityReviewRequest,
    build_pinned_review_execution_plan,
    run_advanced_quality_review,
)
from .analyzer_process_runtime import CancellationToken

__all__ = ["AdvancedQualityReviewWorker"]


class AdvancedQualityReviewWorker(QObject):
    """Run the pure orchestration service outside the GUI thread."""

    progress = Signal(str, str)
    result_ready = Signal(object)
    failed = Signal(str)
    finished = Signal()

    def __init__(
        self,
        *,
        request: AdvancedQualityReviewRequest,
        plan: AdvancedQualityReviewExecutionPlan | None,
        cancellation_token: CancellationToken,
    ) -> None:
        super().__init__()
        self._request = request
        self._plan = plan
        self._token = cancellation_token

    @Slot()
    def run(self) -> None:
        """Execute one bounded orchestration request and emit terminal evidence."""
        try:
            self.progress.emit("ENVIRONMENT_PREFLIGHT", "START")
            plan = self._plan or build_pinned_review_execution_plan(self._request)
            outcome = run_advanced_quality_review(
                self._request,
                plan,
                cancellation_token=self._token,
                progress_callback=self._emit_progress,
            )
        except Exception as error:  # Qt boundary converts failures to signal evidence.
            self.failed.emit(type(error).__name__ + ":" + str(error))
        else:
            self.result_ready.emit(outcome)
        finally:
            self.finished.emit()

    def request_cancel(self) -> None:
        """Request cooperative cancellation through the frozen runtime token."""
        self._token.cancel()

    def _emit_progress(self, stage: str, message: str) -> None:
        self.progress.emit(str(stage), str(message))
