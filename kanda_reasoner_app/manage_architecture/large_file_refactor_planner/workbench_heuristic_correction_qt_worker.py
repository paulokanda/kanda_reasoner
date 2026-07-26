"""Qt-native worker for bounded Workbench Heuristic correction generation."""
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, QThread, Signal, Slot

from .workbench_stage_correction_context import WorkbenchStageCorrectionContext
from .workbench_stage_correction_service import (
    HeuristicWorkbenchCorrectionCandidate,
    build_heuristic_workbench_correction_candidate,
)

__all__ = ["WorkbenchHeuristicCorrectionWorker"]


class WorkbenchHeuristicCorrectionWorker(QObject):
    """Build one bounded correction candidate outside the Qt GUI thread."""

    progress = Signal(str)
    result_ready = Signal(object)
    finished = Signal()

    def __init__(
        self,
        *,
        plan: Any,
        context: WorkbenchStageCorrectionContext,
    ) -> None:
        super().__init__()
        self._plan = plan
        self._context = context

    @Slot()
    def run(self) -> None:
        """Run candidate generation and always emit a terminal worker signal."""
        try:
            candidate = build_heuristic_workbench_correction_candidate(
                plan=self._plan,
                context=self._context,
                progress_callback=self._emit_progress,
            )
        except Exception as exc:  # boundary: never strand the QThread event loop
            candidate = HeuristicWorkbenchCorrectionCandidate(
                ok=False,
                message="Heuristic correction worker failed: " + str(exc),
            )
        self.result_ready.emit(candidate)
        self.finished.emit()

    def _emit_progress(self, phase: str) -> None:
        """Emit progress and honor cooperative interruption between bounded phases."""
        if QThread.currentThread().isInterruptionRequested():
            raise RuntimeError("HEURISTIC_CORRECTION_INTERRUPTED")
        self.progress.emit(str(phase))
