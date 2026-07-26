"""Generation-tagged Qt worker for non-GUI Main Workbench stage computation."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QObject, QThread, Qt, Signal, Slot

__all__ = [
    "MainWorkbenchStageJob",
    "MainWorkbenchStageWorker",
    "launch_main_workbench_stage_job",
]

StageCallable = Callable[[Any], Any]

LOGGER = logging.getLogger(__name__)


class MainWorkbenchStageWorker(QObject):
    """Run one pure stage computation outside the GUI thread."""

    result_ready = Signal(int, str, object)
    failure = Signal(int, str, str)
    finished = Signal()

    def __init__(
        self,
        *,
        generation: int,
        stage: str,
        request: Any,
        execute: StageCallable,
    ) -> None:
        super().__init__()
        self._generation = int(generation)
        self._stage = str(stage)
        self._request = request
        self._execute = execute

    @Slot()
    def run(self) -> None:
        """Execute the stage and emit one generation-tagged terminal signal."""
        try:
            result = self._execute(self._request)
        except Exception as error:
            LOGGER.exception(
                "Main Workbench stage %s failed in generation %s.",
                self._stage,
                self._generation,
            )
            self.failure.emit(
                self._generation,
                self._stage,
                type(error).__name__ + ":" + str(error),
            )
        else:
            self.result_ready.emit(
                self._generation,
                self._stage,
                result,
            )
        finally:
            self.finished.emit()


class _StageSettlementRelay(QObject):
    """Queue settlement on the GUI thread only after the worker thread stops."""

    def __init__(
        self,
        *,
        generation: int,
        stage: str,
        callback: Callable[[int, str], None],
    ) -> None:
        super().__init__()
        self._generation = int(generation)
        self._stage = str(stage)
        self._callback = callback

    @Slot()
    def settle(self) -> None:
        """Deliver one stopped-thread settlement to the owning controller."""
        self._callback(self._generation, self._stage)


@dataclass
class MainWorkbenchStageJob:
    """Keep one worker, thread, and accepted result alive until settlement."""

    generation: int
    stage: str
    thread: QThread
    worker: MainWorkbenchStageWorker
    settlement_relay: _StageSettlementRelay
    result: Any = None
    failure_text: str = ""
    result_received: bool = False

    def request_cancel(self) -> None:
        """Request cooperative interruption and quarantine the eventual result."""
        self.thread.requestInterruption()

    def running(self) -> bool:
        """Return whether the worker thread remains alive."""
        return bool(self.thread.isRunning())


def launch_main_workbench_stage_job(
    *,
    generation: int,
    stage: str,
    request: Any,
    execute: StageCallable,
    settled_callback: Callable[[int, str], None],
) -> MainWorkbenchStageJob:
    """Launch one stage and settle after its QThread has fully stopped."""
    thread = QThread()
    worker = MainWorkbenchStageWorker(
        generation=generation,
        stage=stage,
        request=request,
        execute=execute,
    )
    worker.moveToThread(thread)
    settlement_relay = _StageSettlementRelay(
        generation=generation,
        stage=stage,
        callback=settled_callback,
    )
    job = MainWorkbenchStageJob(
        generation=generation,
        stage=stage,
        thread=thread,
        worker=worker,
        settlement_relay=settlement_relay,
    )
    def store_result(_generation: int, _stage: str, result: Any) -> None:
        job.result = result
        job.result_received = True

    def store_failure(_generation: int, _stage: str, diagnostic: str) -> None:
        job.failure_text = str(diagnostic)

    direct = Qt.ConnectionType.DirectConnection
    thread.started.connect(worker.run)
    worker.result_ready.connect(store_result, direct)
    worker.failure.connect(store_failure, direct)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(
        settlement_relay.settle,
        Qt.ConnectionType.QueuedConnection,
    )
    thread.finished.connect(thread.deleteLater)
    thread.start()
    return job
