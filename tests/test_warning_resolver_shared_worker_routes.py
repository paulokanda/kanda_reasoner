from __future__ import annotations

import importlib
import sys
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


def _slot(*types_):
    def decorator(function):
        return function
    return decorator


def _install_fake_qt_core() -> None:
    pyside = types.ModuleType("PySide6")
    core = types.ModuleType("PySide6.QtCore")
    core.QObject = _QObject
    core.Signal = _SignalDescriptor
    core.Slot = _slot
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtCore"] = core


def test_shared_worker_dispatches_heuristic_and_model_routes() -> None:
    _install_fake_qt_core()
    module_name = (
        "kanda_reasoner_app.manage_architecture."
        "warning_heuristic_resolver_qt_worker"
    )
    sys.modules.pop(module_name, None)
    module = importlib.import_module(module_name)

    calls: list[tuple[str, str]] = []
    heuristic_plan = object()
    model_plan = object()

    def fake_heuristic(project_root, findings, *, progress_callback=None):
        calls.append(("heuristic", ""))
        return heuristic_plan

    def fake_model(
        project_root,
        findings,
        *,
        model_selection,
        progress_callback=None,
    ):
        calls.append(("model", model_selection))
        return model_plan

    module.build_test_protection_gap_plan = fake_heuristic
    module.build_model_test_protection_plan = fake_model

    heuristic_results = []
    heuristic_worker = module.WarningHeuristicResolverWorker(
        project_root=".",
        findings=(),
        route="heuristic",
    )
    heuristic_worker.result_ready.connect(heuristic_results.append)
    heuristic_worker.run()

    model_results = []
    model_worker = module.WarningHeuristicResolverWorker(
        project_root=".",
        findings=(),
        route="model",
        model_selection="qwen3-coder:30b",
    )
    model_worker.result_ready.connect(model_results.append)
    model_worker.run()

    assert calls == [
        ("heuristic", ""),
        ("model", "qwen3-coder:30b"),
    ]
    assert heuristic_results == [heuristic_plan]
    assert model_results == [model_plan]


def main() -> int:
    test_shared_worker_dispatches_heuristic_and_model_routes()
    print("WARNING_RESOLVER_SHARED_QTHREAD_ROUTE_DISPATCH: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
