# project-path: kanda_reasoner_app/freeze_after_update_gui/_local_freeze_bootstrap_worker.py
"""Qt worker for responsive Local Freeze Entry bootstrap."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from PySide6.QtCore import QObject, QThread, Qt, Signal, Slot

from kanda_reasoner_app.freeze_after_update.contract import (
    preview_freeze_entry,
    validate_freeze_entry_preview,
)
from kanda_reasoner_app.freeze_hint_intake import (
    build_freeze_form_inputs_from_latest_hint,
)

__all__ = [
    "LocalFreezeBootstrapJob",
    "LocalFreezeBootstrapRequest",
    "create_local_freeze_bootstrap_job",
]


@dataclass(frozen=True)
class LocalFreezeBootstrapRequest:
    """Immutable identity and fallback data for one bootstrap request."""

    generation: int
    project_root: str
    fallback_inputs: Mapping[str, str]


class _LocalFreezeBootstrapWorker(QObject):
    """Build intake and preview data outside the Qt GUI thread."""

    result_ready = Signal(object)
    failure = Signal(str)
    cancelled = Signal()
    finished = Signal()

    def __init__(self, request: LocalFreezeBootstrapRequest) -> None:
        super().__init__()
        self._request = request

    @Slot()
    def run(self) -> None:
        """Execute the bounded bootstrap and emit one terminal outcome."""
        try:
            if QThread.currentThread().isInterruptionRequested():
                self.cancelled.emit()
                return
            project_root = Path(self._request.project_root)
            inputs = build_freeze_form_inputs_from_latest_hint(
                project_root,
                dict(self._request.fallback_inputs),
            )
            if QThread.currentThread().isInterruptionRequested():
                self.cancelled.emit()
                return
            preview = preview_freeze_entry(project_root, inputs)
            validation: dict[str, Any] | None = None
            if preview.get("ok") and preview.get("is_writable"):
                validation = validate_freeze_entry_preview(project_root, preview)
            if QThread.currentThread().isInterruptionRequested():
                self.cancelled.emit()
                return
            self.result_ready.emit(
                {
                    "inputs": dict(inputs),
                    "preview": dict(preview),
                    "validation": dict(validation or {}),
                }
            )
        except Exception as exc:
            self.failure.emit(exc.__class__.__name__ + ": " + str(exc))
        finally:
            self.finished.emit()


class _BootstrapSettlementRelay(QObject):
    """Deliver settlement on the GUI thread after the worker stops."""

    def __init__(
        self,
        *,
        generation: int,
        callback: Callable[[int], None],
    ) -> None:
        super().__init__()
        self._generation = int(generation)
        self._callback = callback

    @Slot()
    def settle(self) -> None:
        """Notify the GUI owner after QThread shutdown."""
        self._callback(self._generation)


@dataclass
class LocalFreezeBootstrapJob:
    """Keep worker objects and terminal data alive until settlement."""

    request: LocalFreezeBootstrapRequest
    thread: QThread
    worker: _LocalFreezeBootstrapWorker
    settlement_relay: _BootstrapSettlementRelay
    result: dict[str, Any] | None = None
    failure_text: str = ""
    was_cancelled: bool = False

    def start(self) -> None:
        """Start the worker after the owner stores this job."""
        self.thread.start()

    def request_cancel(self) -> None:
        """Request cooperative interruption and quarantine late output."""
        self.thread.requestInterruption()

    def running(self) -> bool:
        """Return whether the worker thread remains active."""
        return bool(self.thread.isRunning())


def create_local_freeze_bootstrap_job(
    request: LocalFreezeBootstrapRequest,
    *,
    settled_callback: Callable[[int], None],
) -> LocalFreezeBootstrapJob:
    """Create one stopped-thread-settled Local Freeze bootstrap job."""
    thread = QThread()
    worker = _LocalFreezeBootstrapWorker(request)
    worker.moveToThread(thread)
    relay = _BootstrapSettlementRelay(
        generation=request.generation,
        callback=settled_callback,
    )
    job = LocalFreezeBootstrapJob(
        request=request,
        thread=thread,
        worker=worker,
        settlement_relay=relay,
    )

    def store_result(result: object) -> None:
        job.result = dict(result or {})

    def store_failure(message: str) -> None:
        job.failure_text = str(message)

    def store_cancelled() -> None:
        job.was_cancelled = True

    direct = Qt.ConnectionType.DirectConnection
    thread.started.connect(worker.run)
    worker.result_ready.connect(store_result, direct)
    worker.failure.connect(store_failure, direct)
    worker.cancelled.connect(store_cancelled, direct)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(relay.settle, Qt.ConnectionType.QueuedConnection)
    thread.finished.connect(thread.deleteLater)
    return job
