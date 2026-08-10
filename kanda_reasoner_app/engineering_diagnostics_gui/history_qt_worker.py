# project-path: kanda_reasoner_app/engineering_diagnostics_gui/history_qt_worker.py
"""Qt worker for one read-only Engineering Diagnostics history view load."""

from __future__ import annotations

from dataclasses import dataclass
import traceback

from PySide6.QtCore import QObject, QThread, Signal, Slot

__all__ = [
    "EngineeringDiagnosticsHistoryOutcome",
    "EngineeringDiagnosticsHistoryWorker",
]


@dataclass(frozen=True, slots=True)
class EngineeringDiagnosticsHistoryOutcome:
    """Immutable worker result bound to one Project, run, and generation."""

    generation: int
    project_root: str
    run_id: str
    view: object | None = None
    error_type: str = ""
    error_message: str = ""
    traceback_text: str = ""

    @property
    def ok(self) -> bool:
        """Return whether the worker produced a run view."""
        return self.view is not None and not self.error_type


class EngineeringDiagnosticsHistoryWorker(QObject):
    """Load one diagnostic run view outside the Qt GUI thread."""

    result_ready = Signal(object)
    finished = Signal()

    def __init__(
        self,
        *,
        controller: object,
        project_root: str,
        run_id: str,
        generation: int,
    ) -> None:
        super().__init__()
        self._controller = controller
        self._project_root = str(project_root)
        self._run_id = str(run_id)
        self._generation = int(generation)

    @Slot()
    def run(self) -> None:
        """Execute the blocking controller read and emit one immutable outcome."""
        thread = QThread.currentThread()
        try:
            if thread.isInterruptionRequested():
                return
            view = self._controller.load_run_view(
                self._project_root,
                self._run_id,
            )
            if thread.isInterruptionRequested():
                return
            outcome = EngineeringDiagnosticsHistoryOutcome(
                generation=self._generation,
                project_root=self._project_root,
                run_id=self._run_id,
                view=view,
            )
            self.result_ready.emit(outcome)
        except Exception as exc:  # noqa: BLE001
            if not thread.isInterruptionRequested():
                self.result_ready.emit(
                    EngineeringDiagnosticsHistoryOutcome(
                        generation=self._generation,
                        project_root=self._project_root,
                        run_id=self._run_id,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                        traceback_text=traceback.format_exc(),
                    )
                )
        finally:
            self.finished.emit()
