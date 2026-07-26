"""Qt-native worker for bounded Workbench Local AI correction generation."""
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, QThread, Signal, Slot

from .workbench_local_ai_correction_models import (
    LocalAIWorkbenchCorrectionCandidate,
)
from .workbench_local_ai_correction_runtime import (
    build_bounded_local_ai_workbench_correction_candidate,
)
from .workbench_stage_correction_context import WorkbenchStageCorrectionContext

__all__ = ["WorkbenchLocalAICorrectionWorker"]


class WorkbenchLocalAICorrectionWorker(QObject):
    """Build one bounded Local AI correction candidate outside the GUI thread."""

    progress = Signal(str)
    result_ready = Signal(object)
    finished = Signal()

    def __init__(
        self,
        *,
        plan: Any,
        proposals: list[Any],
        context: WorkbenchStageCorrectionContext,
    ) -> None:
        super().__init__()
        self._plan = plan
        self._proposals = list(proposals)
        self._context = context

    @Slot()
    def run(self) -> None:
        """Run bounded correction and always emit terminal worker signals."""
        try:
            candidate = build_bounded_local_ai_workbench_correction_candidate(
                plan=self._plan,
                proposals=self._proposals,
                context=self._context,
                progress_callback=self._emit_progress,
                interruption_check=self._check_interruption,
            )
        except Exception as exc:  # boundary: never strand the QThread lifecycle
            candidate = LocalAIWorkbenchCorrectionCandidate(
                ok=False,
                message="Local AI correction worker failed: " + str(exc),
            )
        self.result_ready.emit(candidate)
        self.finished.emit()

    def _emit_progress(self, phase: str) -> None:
        self._check_interruption()
        self.progress.emit(str(phase))

    @staticmethod
    def _check_interruption() -> None:
        if QThread.currentThread().isInterruptionRequested():
            raise RuntimeError("LOCAL_AI_CORRECTION_INTERRUPTED")
