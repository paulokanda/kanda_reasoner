# project-path: kanda_reasoner_app/engineering_diagnostics_gui/history_async.py
"""Qt-owned asynchronous history loading for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6.QtCore import QCoreApplication, QObject, QThread, QTimer, Signal, Slot

from .history_qt_worker import (
    EngineeringDiagnosticsHistoryOutcome,
    EngineeringDiagnosticsHistoryWorker,
)
from .run_summary import build_diagnostic_run_summary

__all__ = ["EngineeringDiagnosticsHistoryActions", "bind_async_history"]

_HISTORY_TIMEOUT_MS = 30_000


@dataclass(frozen=True, slots=True)
class _HistoryRequest:
    generation: int
    project_root: str
    run_id: str


@dataclass(slots=True)
class EngineeringDiagnosticsHistoryActions:
    """Bound history actions exposed to the owning Engineering Diagnostics panel."""

    render_run: Callable[[str], None]
    refresh_history: Callable[[str], None]
    cancel: Callable[[], None]
    close: Callable[[], bool]
    shutdown_ready: Callable[[], bool]
    runtime: object


class _EngineeringDiagnosticsHistoryRuntime(QObject):
    """Own one serialized QThread history lane with stale-result rejection."""

    settled = Signal()

    def __init__(
        self,
        *,
        controller: object,
        apply_view: Callable[[object, str], None],
        apply_failure: Callable[[str, str], None],
        apply_status: Callable[[str], None],
    ) -> None:
        app = QCoreApplication.instance()
        super().__init__(app)
        self._controller = controller
        self._apply_view = apply_view
        self._apply_failure = apply_failure
        self._apply_status = apply_status
        self._generation = 0
        self._active_job: dict[str, object] | None = None
        self._pending: _HistoryRequest | None = None
        self._closed = False
        self._delete_requested = False

    def load(self, project_root: str, run_id: str) -> None:
        """Queue the newest run view while allowing at most one heavy worker."""
        if self._closed:
            return
        self._generation += 1
        request = _HistoryRequest(
            generation=self._generation,
            project_root=str(project_root),
            run_id=str(run_id),
        )
        self._pending = request
        active = self._active_job
        if active is not None:
            active["accept_result"] = False
            thread = active.get("thread")
            if isinstance(thread, QThread):
                thread.requestInterruption()
            self._apply_status(
                "Waiting for the current history worker to settle; "
                "the older result is stale."
            )
            return
        self._start_pending()

    def cancel(self) -> None:
        """Reject pending and late results without blocking the GUI thread."""
        self._generation += 1
        self._pending = None
        active = self._active_job
        if active is None:
            return
        active["accept_result"] = False
        thread = active.get("thread")
        if isinstance(thread, QThread):
            thread.requestInterruption()
        watchdog = active.get("watchdog")
        if isinstance(watchdog, QTimer):
            watchdog.stop()

    def shutdown_ready(self) -> bool:
        """Return whether no Engineering Diagnostics history QThread remains."""
        return self._active_job is None

    def _request_delete_once(self) -> None:
        """Schedule QObject deletion at most once, including late hooks."""
        if self._delete_requested:
            return
        self._delete_requested = True
        try:
            self.deleteLater()
        except RuntimeError:
            return

    def close(self) -> bool:
        """Reject late results and remain safe when cleanup is requested twice."""
        if self._delete_requested:
            return True
        if not self._closed:
            self._closed = True
            self.cancel()
        if self._active_job is None:
            self._request_delete_once()
            return True
        return False

    def _start_pending(self) -> None:
        request = self._pending
        if self._closed or request is None or self._active_job is not None:
            return
        self._pending = None

        thread = QThread()
        thread.setObjectName("engineering_diagnostics_history")
        worker = EngineeringDiagnosticsHistoryWorker(
            controller=self._controller,
            project_root=request.project_root,
            run_id=request.run_id,
            generation=request.generation,
        )
        worker.moveToThread(thread)

        watchdog = QTimer(self)
        watchdog.setSingleShot(True)
        watchdog.setInterval(_HISTORY_TIMEOUT_MS)

        self._active_job = {
            "request": request,
            "thread": thread,
            "worker": worker,
            "watchdog": watchdog,
            "accept_result": True,
        }

        thread.started.connect(worker.run)
        worker.result_ready.connect(self._on_result)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(self._on_thread_finished)
        watchdog.timeout.connect(
            lambda generation=request.generation: self._on_timeout(generation)
        )

        self._apply_status("Loading diagnostic history off the GUI thread...")
        thread.start()
        watchdog.start()

    @Slot(object)
    def _on_result(self, outcome: object) -> None:
        if not isinstance(outcome, EngineeringDiagnosticsHistoryOutcome):
            return
        active = self._active_job
        if active is None or not bool(active.get("accept_result", False)):
            return
        request = active.get("request")
        if not isinstance(request, _HistoryRequest):
            return
        if outcome.generation != self._generation:
            return
        if outcome.generation != request.generation:
            return
        if outcome.project_root != request.project_root:
            return
        if outcome.run_id != request.run_id:
            return

        active["accept_result"] = False
        watchdog = active.get("watchdog")
        if isinstance(watchdog, QTimer):
            watchdog.stop()

        if outcome.ok:
            self._apply_view(outcome.view, outcome.run_id)
            return
        message = outcome.error_type
        if outcome.error_message:
            message += ": " + outcome.error_message
        self._apply_failure(message, outcome.traceback_text)

    def _on_timeout(self, generation: int) -> None:
        active = self._active_job
        if active is None:
            return
        request = active.get("request")
        if not isinstance(request, _HistoryRequest):
            return
        if request.generation != generation:
            return
        active["accept_result"] = False
        thread = active.get("thread")
        if isinstance(thread, QThread):
            thread.requestInterruption()
        self._apply_status(
            "Diagnostic history load exceeded 30 seconds. "
            "The late result will be ignored."
        )

    @Slot()
    def _on_thread_finished(self) -> None:
        active = self._active_job
        if active is None:
            return
        request = active.get("request")
        if not isinstance(request, _HistoryRequest):
            return

        watchdog = active.get("watchdog")
        if isinstance(watchdog, QTimer):
            watchdog.stop()
            watchdog.deleteLater()
        thread = active.get("thread")
        if isinstance(thread, QThread):
            thread.deleteLater()

        self._active_job = None
        if self._closed:
            self.settled.emit()
            self._request_delete_once()
            return
        self._start_pending()


def bind_async_history(
    *,
    controller: object,
    current_project_root: Callable[[], str],
    selected_producer_id: Callable[[], str],
    run_combo: object,
    model: object,
    summary_label: object,
    status_label: object,
    detail: object,
    apply_filters: Callable[[], None],
) -> EngineeringDiagnosticsHistoryActions:
    """Bind history widgets to one serialized Qt-native history worker lane."""

    def apply_view(view: object, run_id: str) -> None:
        model.set_rows(view.findings)
        summary_label.setText(build_diagnostic_run_summary(view))
        status_label.setText("History loaded: " + str(run_id)[:12])
        apply_filters()

    def apply_failure(message: str, traceback_text: str) -> None:
        status_label.setText("Could not load diagnostic run: " + message)
        detail.setPlainText(traceback_text or message)

    runtime = _EngineeringDiagnosticsHistoryRuntime(
        controller=controller,
        apply_view=apply_view,
        apply_failure=apply_failure,
        apply_status=status_label.setText,
    )

    def render_run(run_id: str) -> None:
        selected = str(run_id or "")
        if not selected:
            runtime.cancel()
            model.set_rows(())
            summary_label.setText("No diagnostic run selected.")
            return
        runtime.load(current_project_root(), selected)

    def refresh_history(preferred_run_id: str = "") -> None:
        try:
            runs = controller.list_runs(
                current_project_root(),
                producer_id=selected_producer_id(),
                limit=200,
            )
        except Exception as exc:  # noqa: BLE001
            runtime.cancel()
            run_combo.clear()
            model.set_rows(())
            status_label.setText("Diagnostics unavailable: " + str(exc))
            return

        run_combo.blockSignals(True)
        run_combo.clear()
        for run in runs:
            label = (
                run.completed_at_utc
                + " | "
                + str(run.finding_count)
                + " findings | "
                + run.run_id[:12]
            )
            run_combo.addItem(label, run.run_id)
        target = str(preferred_run_id or "")
        if target:
            index = run_combo.findData(target)
            if index >= 0:
                run_combo.setCurrentIndex(index)
        run_combo.blockSignals(False)

        selected = str(run_combo.currentData() or "")
        if selected:
            render_run(selected)
        else:
            render_run("")
            status_label.setText("History refreshed; no completed runs.")

    return EngineeringDiagnosticsHistoryActions(
        render_run=render_run,
        refresh_history=refresh_history,
        cancel=runtime.cancel,
        close=runtime.close,
        shutdown_ready=runtime.shutdown_ready,
        runtime=runtime,
    )
