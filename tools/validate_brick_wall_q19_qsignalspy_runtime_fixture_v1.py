"""Run an isolated real Qt QSignalSpy queued-delivery fixture."""

from __future__ import annotations

import argparse
import os
import sys
import time

FEATURE_ID = "brick-wall-q19-qsignalspy-runtime-fixture-v1"


def _deferred() -> int:
    print("Q19_PYSIDE6_RUNTIME_AVAILABLE: NO")
    print("Q19_QSIGNALSPY_RUNTIME_DEFERRED_TO_USER_LOCAL: PASS")
    print("STATUS: DEFERRED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-pyside", action="store_true")
    args = parser.parse_args()
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import (
            QCoreApplication,
            QObject,
            QThread,
            Qt,
            Signal,
            Slot,
        )
        from PySide6.QtTest import QSignalSpy
    except ModuleNotFoundError:
        if args.require_pyside:
            raise RuntimeError("PySide6 is required for the local Q19 runtime fixture")
        return _deferred()

    class Worker(QObject):
        result_ready = Signal(int, str, bool)
        finished = Signal()

        @Slot()
        def run(self) -> None:
            in_worker = QThread.currentThread() is self.thread()
            self.result_ready.emit(7, "queued-result", in_worker)
            self.finished.emit()

    class Receiver(QObject):
        received = Signal(int, str, bool, bool)

        @Slot(int, str, bool)
        def accept(self, number: int, text: str, in_worker: bool) -> None:
            in_main = QThread.currentThread() is app.thread()
            self.received.emit(number, text, in_worker, in_main)

    app = QCoreApplication.instance() or QCoreApplication([])
    thread = QThread()
    worker = Worker()
    receiver = Receiver()
    worker.moveToThread(thread)
    worker.result_ready.connect(
        receiver.accept,
        Qt.ConnectionType.QueuedConnection,
    )
    worker.finished.connect(thread.quit)
    thread.started.connect(worker.run)
    result_spy = QSignalSpy(receiver.received)
    finished_spy = QSignalSpy(thread.finished)
    thread.start()
    deadline = time.monotonic() + 5.0
    while (
        result_spy.count() < 1 or thread.isRunning()
    ) and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.005)
    thread.wait(1000)
    app.processEvents()
    if thread.isRunning():
        thread.requestInterruption()
        thread.quit()
        thread.wait(1000)
        raise AssertionError("QThread did not settle before watchdog")
    if result_spy.count() != 1:
        raise AssertionError("Expected exactly one queued result signal")
    if finished_spy.count() != 1:
        raise AssertionError("Expected exactly one QThread finished signal")
    payload = list(result_spy.at(0))
    if payload != [7, "queued-result", True, True]:
        raise AssertionError("Unexpected queued signal payload: " + repr(payload))
    print("Q19_QSIGNALSPY_IMPORT: PASS")
    print("Q19_REAL_QT_QUEUED_SIGNAL_DELIVERY: PASS")
    print("Q19_SIGNAL_COUNT_ORDER_PAYLOAD: PASS")
    print("Q19_RECEIVER_MAIN_THREAD_AFFINITY: PASS")
    print("Q19_QTHREAD_SETTLEMENT: PASS")
    print("Q19_QSIGNALSPY_WATCHDOG: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
