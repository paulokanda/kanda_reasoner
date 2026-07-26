"""Validate explicit boundary failures for worker and headless execution."""

from __future__ import annotations

import argparse
import ast
import contextlib
import importlib
import importlib.util
import io
import json
import sys
import tempfile
import types
import zipfile
from pathlib import Path
from typing import Any

__all__ = ["main"]

FEATURE_ID = "boundary-error-contract-worker-and-headless-unlink-v1"
WORKER_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "main_workbench_stage_worker.py"
)
SCENARIO_RELATIVE = Path(
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_scenarios.py"
)
VALIDATOR_RELATIVE = Path(
    "tools/validate_boundary_error_contract_worker_and_headless_unlink_v1.py"
)
ROOT_MEMBERS = {
    "FREEZE.ps1",
    "INSTALL.ps1",
    "KANDA_FREEZE_HINT.json",
    "PATCH_README.txt",
    "VALIDATE.ps1",
}
EXPECTED_MEMBERS = ROOT_MEMBERS | {
    WORKER_RELATIVE.as_posix(),
    SCENARIO_RELATIVE.as_posix(),
    VALIDATOR_RELATIVE.as_posix(),
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read_ascii(path: Path) -> str:
    data = path.read_bytes()
    data.decode("ascii")
    return data.decode("utf-8")


def _validate_source_fitness(project_root: Path) -> None:
    for relative in (WORKER_RELATIVE, SCENARIO_RELATIVE, VALIDATOR_RELATIVE):
        path = project_root / relative
        _require(path.is_file(), f"Missing source file: {relative}")
        source = _read_ascii(path)
        ast.parse(source, filename=str(relative))
        line_count = len(source.splitlines())
        _require(
            line_count <= 500,
            f"Module exceeds 500 lines: {relative}: {line_count}",
        )
        print(f"MODULE_MAX_500_LINES:{relative.as_posix()}: PASS")
    print("PYTHON_SYNTAX_ASCII_MODULE_SIZE: PASS")


def _function_node(source: str, function_name: str) -> ast.FunctionDef:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return node
    raise AssertionError(f"Function not found: {function_name}")


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _validate_worker_ast(project_root: Path) -> None:
    source = (project_root / WORKER_RELATIVE).read_text(encoding="utf-8")
    function = _function_node(source, "run")
    handlers = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.ExceptHandler)
    ]
    _require(len(handlers) == 1, "Worker run must have one exception handler.")
    calls = {
        _call_name(node.func)
        for node in ast.walk(handlers[0])
        if isinstance(node, ast.Call)
    }
    _require(
        "LOGGER.exception" in calls,
        "Worker failure must be logged with exception severity.",
    )
    _require(
        "self.failure.emit" in calls,
        "Worker failure signal must remain present.",
    )
    _require(
        "self.finished.emit" in {
            _call_name(node.func)
            for node in ast.walk(function)
            if isinstance(node, ast.Call)
        },
        "Worker finished signal must remain present.",
    )
    print("WORKER_EXCEPTION_LOG_SURFACE: PASS")
    print("WORKER_FAILURE_SIGNAL_PRESERVED: PASS")
    print("WORKER_FINISHED_SIGNAL_PRESERVED: PASS")


class _BoundSignal:
    def __init__(self) -> None:
        self.emissions: list[tuple[Any, ...]] = []

    def emit(self, *values: Any) -> None:
        self.emissions.append(tuple(values))

    def connect(self, *args: Any, **kwargs: Any) -> None:
        del args, kwargs


class _SignalDescriptor:
    def __init__(self, *types_: object) -> None:
        del types_
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        del owner
        self._name = name

    def __get__(self, instance: object, owner: type) -> Any:
        del owner
        if instance is None:
            return self
        storage_name = "_fake_signal_" + self._name
        signal = getattr(instance, storage_name, None)
        if signal is None:
            signal = _BoundSignal()
            setattr(instance, storage_name, signal)
        return signal


class _FakeQObject:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        del args, kwargs

    def moveToThread(self, thread: object) -> None:
        del thread

    def deleteLater(self) -> None:
        return None


class _FakeQThread:
    def requestInterruption(self) -> None:
        return None

    def isRunning(self) -> bool:
        return False

    def start(self) -> None:
        return None

    def quit(self) -> None:
        return None

    def deleteLater(self) -> None:
        return None


class _FakeConnectionType:
    DirectConnection = object()
    QueuedConnection = object()


class _FakeQt:
    ConnectionType = _FakeConnectionType


def _fake_slot(*types_: object):
    del types_

    def decorate(function):
        return function

    return decorate


def _load_worker_module(path: Path):
    package = types.ModuleType("PySide6")
    core = types.ModuleType("PySide6.QtCore")
    core.QObject = _FakeQObject
    core.QThread = _FakeQThread
    core.Qt = _FakeQt
    core.Signal = _SignalDescriptor
    core.Slot = _fake_slot
    old_package = sys.modules.get("PySide6")
    old_core = sys.modules.get("PySide6.QtCore")
    sys.modules["PySide6"] = package
    sys.modules["PySide6.QtCore"] = core
    module_name = "_kanda_boundary_worker_probe"
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        _require(spec is not None and spec.loader is not None, "Worker loader missing.")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.modules.pop(module_name, None)
        if old_package is None:
            sys.modules.pop("PySide6", None)
        else:
            sys.modules["PySide6"] = old_package
        if old_core is None:
            sys.modules.pop("PySide6.QtCore", None)
        else:
            sys.modules["PySide6.QtCore"] = old_core


class _LoggerProbe:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    def exception(self, message: str, *args: Any) -> None:
        self.calls.append((message, tuple(args)))


def _validate_worker_runtime(project_root: Path) -> None:
    module = _load_worker_module(project_root / WORKER_RELATIVE)
    logger = _LoggerProbe()
    module.LOGGER = logger

    def fail_execute(request: Any) -> Any:
        del request
        raise RuntimeError("boom")

    worker = module.MainWorkbenchStageWorker(
        generation=7,
        stage="structural",
        request={"value": 1},
        execute=fail_execute,
    )
    worker.run()
    _require(len(logger.calls) == 1, "Worker failure was not logged.")
    _require(
        worker.failure.emissions
        == [(7, "structural", "RuntimeError:boom")],
        "Worker failure signal payload changed.",
    )
    _require(worker.finished.emissions == [()], "Worker did not finish.")
    _require(not worker.result_ready.emissions, "Failure produced a result.")

    success = module.MainWorkbenchStageWorker(
        generation=8,
        stage="preflight",
        request="request",
        execute=lambda request: {"request": request},
    )
    success.run()
    _require(
        success.result_ready.emissions
        == [(8, "preflight", {"request": "request"})],
        "Worker success signal payload changed.",
    )
    _require(not success.failure.emissions, "Success emitted failure.")
    _require(success.finished.emissions == [()], "Success did not finish.")
    print("WORKER_FAILURE_RUNTIME_CONTRACT: PASS")
    print("WORKER_SUCCESS_RUNTIME_CONTRACT: PASS")


class _HeadlessBindingsProbe:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.configure_calls = 0

    def resolve_headless_config(self) -> dict[str, Any]:
        return {
            "project_root": self.output_path.parent,
            "output_json": self.output_path,
            "overwrite": True,
            "entry_script": None,
            "scenario_module": "",
            "execute_entry_script": False,
        }

    def configure_runtime_trace(self, **kwargs: Any) -> None:
        del kwargs
        self.configure_calls += 1

    def save_runtime_trace(self) -> Path:
        self.output_path.write_text("{}", encoding="utf-8")
        return self.output_path


def _validate_headless_runtime(project_root: Path) -> None:
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    module_name = (
        "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help."
        "_runtime_runner_part_2_scenarios"
    )
    module = importlib.import_module(module_name)
    original_unlink = module.unlink
    original_runner = module.run_rich_automatic_scenario
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "runtime.json"
            output_path.write_text("old", encoding="utf-8")
            bindings = _HeadlessBindingsProbe(output_path)

            def fail_unlink(path: Path) -> None:
                del path
                raise PermissionError("locked output")

            module.unlink = fail_unlink
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = module.run_headless_scenario(bindings)
            _require(exit_code == 1, "Unlink failure must return exit code 1.")
            _require(
                "PermissionError" in stderr.getvalue()
                and "locked output" in stderr.getvalue(),
                "Unlink failure traceback was not surfaced.",
            )
            _require(
                bindings.configure_calls == 0,
                "Headless execution continued after unlink failure.",
            )

            module.unlink = lambda path: Path(path).unlink()
            module.run_rich_automatic_scenario = (
                lambda *args, **kwargs: "validation_probe"
            )
            output_path.write_text("old", encoding="utf-8")
            bindings = _HeadlessBindingsProbe(output_path)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = module.run_headless_scenario(bindings)
            _require(exit_code == 0, "Successful headless run must return 0.")
            payload = json.loads(stdout.getvalue())
            _require(payload["ok"] is True, "Headless payload lost ok=true.")
            _require(
                payload["overwrote_existing"] is True,
                "Headless overwrite evidence changed.",
            )
            _require(not stderr.getvalue(), "Successful headless run wrote stderr.")
    finally:
        module.unlink = original_unlink
        module.run_rich_automatic_scenario = original_runner
    print("HEADLESS_UNLINK_FAILURE_RETURNS_NONZERO: PASS")
    print("HEADLESS_UNLINK_FAILURE_TRACEBACK_SURFACED: PASS")
    print("HEADLESS_SUCCESS_CONTRACT_PRESERVED: PASS")


def _validate_detector_result(project_root: Path) -> None:
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        fixture_root = Path(temp_dir)
        for relative in (WORKER_RELATIVE, SCENARIO_RELATIVE):
            target = fixture_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                (project_root / relative).read_text(encoding="utf-8"),
                encoding="utf-8",
                newline="\n",
            )
        warning_path = fixture_root / "kanda_reasoner_app/example_runner.py"
        warning_path.parent.mkdir(parents=True, exist_ok=True)
        warning_path.write_text(
            "def run_task():\n"
            "    try:\n"
            "        return work()\n"
            "    except Exception:\n"
            "        pass\n",
            encoding="utf-8",
            newline="\n",
        )
        _modules, issues, _manifest, _outputs = module.scan_project(fixture_root)
        target_paths = {
            WORKER_RELATIVE.as_posix(),
            SCENARIO_RELATIVE.as_posix(),
        }
        target_issues = [
            issue
            for issue in issues
            if issue.code == "BOUNDARY_ERROR_CONTRACT"
            and issue.path in target_paths
        ]
        _require(
            not target_issues,
            "Patched boundary owners still produce warnings: "
            + repr([issue.message for issue in target_issues]),
        )
        retained = [
            issue
            for issue in issues
            if issue.code == "BOUNDARY_ERROR_CONTRACT"
            and issue.path == "kanda_reasoner_app/example_runner.py"
        ]
        _require(retained, "Real swallowed boundary exception was not retained.")
    print("TARGET_BOUNDARY_WARNINGS_REMOVED: PASS")
    print("REAL_BOUNDARY_WARNING_RETENTION: PASS")


def _validate_current_project_detector_result(project_root: Path) -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    _modules, issues, _manifest, _outputs = module.scan_project(project_root)
    target_paths = {
        WORKER_RELATIVE.as_posix(),
        SCENARIO_RELATIVE.as_posix(),
    }
    target_issues = [
        issue
        for issue in issues
        if issue.code == "BOUNDARY_ERROR_CONTRACT"
        and issue.path in target_paths
    ]
    _require(
        not target_issues,
        "Current project still reports target boundary warnings: "
        + repr([issue.message for issue in target_issues]),
    )
    print("CURRENT_PROJECT_TARGET_BOUNDARY_WARNING_SET: PASS")


def _validate_zip(patch_zip: Path) -> None:
    _require(patch_zip.is_file(), f"Patch ZIP is missing: {patch_zip}")
    with zipfile.ZipFile(patch_zip) as archive:
        members = {info.filename for info in archive.infolist() if not info.is_dir()}
    _require(
        members == EXPECTED_MEMBERS,
        "Patch ZIP member set changed: "
        + repr(sorted(members.symmetric_difference(EXPECTED_MEMBERS))),
    )
    print("PATCH_ZIP_EXACT_MEMBER_SET: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    _validate_source_fitness(project_root)
    _validate_worker_ast(project_root)
    _validate_worker_runtime(project_root)
    _validate_headless_runtime(project_root)
    _validate_detector_result(project_root)
    _validate_current_project_detector_result(project_root)
    if args.patch_zip:
        _validate_zip(Path(args.patch_zip).resolve())
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
