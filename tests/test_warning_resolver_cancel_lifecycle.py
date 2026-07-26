from __future__ import annotations

import importlib
from pathlib import Path
import sys
import threading
import time
import types


class _BoundSignal:
    def __init__(self) -> None:
        self._callbacks = []

    def connect(self, callback) -> None:
        self._callbacks.append(callback)

    def emit(self, *args) -> None:
        for callback in list(self._callbacks):
            callback(*args)


class _SignalDescriptor:
    def __init__(self, *types_) -> None:
        self._name = ""

    def __set_name__(self, owner, name: str) -> None:
        self._name = "__signal_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        signal = instance.__dict__.get(self._name)
        if signal is None:
            signal = _BoundSignal()
            instance.__dict__[self._name] = signal
        return signal


class _QObject:
    def __init__(self, parent=None) -> None:
        self.parent = parent

    def moveToThread(self, thread) -> None:
        self.thread = thread

    def deleteLater(self) -> None:
        return None


def _slot(*types_):
    def decorator(function):
        return function

    return decorator


class _QThread(_QObject):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.started = _BoundSignal()
        self.finished = _BoundSignal()
        self._interruption_requested = False
        self._thread = None

    def start(self) -> None:
        def target() -> None:
            self.started.emit()
            self.finished.emit()

        self._thread = threading.Thread(target=target, daemon=True)
        self._thread.start()

    def quit(self) -> None:
        return None

    def requestInterruption(self) -> None:
        self._interruption_requested = True

    def wait(self, timeout_ms: int = 1000) -> bool:
        thread = self._thread
        if thread is None:
            return True
        thread.join(timeout=max(timeout_ms, 0) / 1000.0)
        return not thread.is_alive()


def _install_fake_qt_core() -> None:
    pyside = types.ModuleType("PySide6")
    core = types.ModuleType("PySide6.QtCore")
    core.QObject = _QObject
    core.QThread = _QThread
    core.Signal = _SignalDescriptor
    core.Slot = _slot
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtCore"] = core


def _load_modules():
    _install_fake_qt_core()
    worker_name = (
        "kanda_reasoner_app.manage_architecture."
        "warning_heuristic_resolver_qt_worker"
    )
    controller_name = (
        "kanda_reasoner_app.manage_architecture."
        "warning_heuristic_resolver_qt_controller"
    )
    sys.modules.pop(controller_name, None)
    sys.modules.pop(worker_name, None)
    worker_module = importlib.import_module(worker_name)
    controller_module = importlib.import_module(controller_name)
    return worker_module, controller_module


def _wait_until(predicate, timeout_seconds: float = 2.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.005)
    raise AssertionError("condition did not become true before timeout")


def test_cancel_revokes_late_result_and_settles_once() -> None:
    worker_module, controller_module = _load_modules()
    plan = object()

    def slow_plan(project_root, findings, *, progress_callback=None):
        del project_root, findings
        for index in range(200):
            time.sleep(0.002)
            if progress_callback is not None:
                progress_callback(200, 199 - index, index + 1, 0, "owner.py", "scan")
        return plan

    worker_module.build_test_protection_gap_plan = slow_plan
    controller = controller_module.WarningHeuristicResolverController(_QObject())
    states = []
    results = []
    failures = []
    cancelled = []
    controller.state_changed.connect(lambda *state: states.append(state))
    controller.result_ready.connect(results.append)
    controller.failed.connect(failures.append)
    controller.cancelled.connect(lambda: cancelled.append(True))

    assert controller.start(Path.cwd(), (), route="heuristic") is True
    _wait_until(lambda: controller.running)
    time.sleep(0.02)
    assert controller.cancel() is True
    assert controller.cancel_requested is True
    _wait_until(lambda: not controller.running)

    assert results == []
    assert failures == []
    assert cancelled == [True]
    assert (True, False, True) in states
    assert (True, True, True) in states
    assert states[-1] == (False, False, False)


def test_confirmed_apply_verify_route_is_not_cancellable() -> None:
    worker_module, controller_module = _load_modules()

    def slow_apply(plan, *, progress_callback=None):
        del plan
        if progress_callback is not None:
            progress_callback(1, 1, 0, 0, "Live project", "guarded_apply")
        time.sleep(0.05)
        return object()

    worker_module.apply_and_verify_model_plan = slow_apply
    controller = controller_module.WarningHeuristicResolverController(_QObject())
    assert controller.start(
        Path.cwd(),
        (),
        route="model_apply_verify",
        apply_plan=object(),
    ) is True
    _wait_until(lambda: controller.running)
    assert controller.cancellable is False
    assert controller.cancel() is False
    _wait_until(lambda: not controller.running)



def test_cancellable_fresh_audit_runner_reaps_child_process() -> None:
    worker_module, _ = _load_modules()
    worker = worker_module.WarningHeuristicResolverWorker(
        project_root=Path.cwd(),
        findings=(),
        route="heuristic",
    )
    errors = []

    def run_child() -> None:
        try:
            worker._cancellable_runner(
                [sys.executable, "-c", "import time; time.sleep(10)"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        except Exception as exc:
            errors.append(type(exc).__name__)

    thread = threading.Thread(target=run_child, daemon=True)
    thread.start()
    time.sleep(0.2)
    worker.request_cancel()
    thread.join(timeout=3.0)
    assert thread.is_alive() is False
    assert errors == ["_WarningResolverCancelled"]


def main() -> int:
    test_cancel_revokes_late_result_and_settles_once()
    test_confirmed_apply_verify_route_is_not_cancellable()
    test_cancellable_fresh_audit_runner_reaps_child_process()
    print("WARNING_RESOLVER_CANCEL_LIFECYCLE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
