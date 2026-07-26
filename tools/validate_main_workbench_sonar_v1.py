"""Focused validation for Main Workbench sonar lifecycle integration."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import importlib.util
import os
from pathlib import Path
import py_compile
import sys
from types import ModuleType
from typing import Any

__all__ = [
    "main",
]

FEATURE_ID = "main-workbench-complete-web-ai-orchestration-sonar-v1"
BOX = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
)
SONAR = BOX / "main_workbench_sonar.py"
GUI = BOX / "main_workbench_gui.py"
AQR_SONAR = BOX / "advanced_quality_review_sonar.py"
TOUCHED = (SONAR, GUI, AQR_SONAR)

READY = "READY_FOR_WEB_AI"
WEB_AI_BLOCKED = "WEB_AI_REQUIRED_WITH_BLOCKERS"
FAILED = "FAILED_LOCAL_PIPELINE"
STALE = "STALE_AFTER_EXTERNAL_SOURCE_MUTATION"
CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class FakeState:
    generation: int
    running: bool
    cancel_requested: bool
    stage: str
    terminal_status: str
    message: str
    blockers: tuple[str, ...]


class FakeMonitor:
    """Capture sonar calls without requiring PySide6 in the build runtime."""

    instances: list["FakeMonitor"] = []

    def __init__(self, window: Any, *, title: str, host: Any = None) -> None:
        self.window = window
        self.title = title
        self.host = host
        self.calls: list[tuple[str, str, tuple[str, str, str]]] = []
        self.__class__.instances.append(self)

    def start(self, status: str, details: tuple[str, str, str]) -> None:
        self.calls.append(("start", status, details))

    def finish_success(
        self,
        status: str,
        details: tuple[str, str, str],
    ) -> None:
        self.calls.append(("success", status, details))

    def finish_error(
        self,
        status: str,
        details: tuple[str, str, str],
    ) -> None:
        self.calls.append(("error", status, details))


class FakeWindow:
    pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--require-pyside", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    _assert_files(root)
    _assert_syntax_and_line_law(root)
    _assert_gui_integration(root)
    _assert_fake_runtime(root)
    _assert_aqr_sonar_suppression(root)
    _assert_real_pyside_smoke(root, required=args.require_pyside)

    print("MAIN_WORKBENCH_SONAR_STAGE_PROJECTION: PASS")
    print("MAIN_WORKBENCH_SONAR_TERMINAL_SETTLEMENT: PASS")
    print("MAIN_WORKBENCH_PACKAGE_SONAR_LIFECYCLE: PASS")
    print("AQR_DUPLICATE_SONAR_SUPPRESSION: PASS")
    print("TOUCHED_MODULE_LINE_LAW_101_499: PASS")
    print("TOUCHED_MODULE_PYTHON_COMPILE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _assert_files(root: Path) -> None:
    for relative in TOUCHED:
        path = root / relative
        if not path.is_file():
            raise AssertionError("TOUCHED_FILE_MISSING:" + relative.as_posix())


def _assert_syntax_and_line_law(root: Path) -> None:
    for relative in TOUCHED:
        path = root / relative
        text = path.read_text(encoding="utf-8-sig")
        ast.parse(text, filename=str(path))
        py_compile.compile(str(path), doraise=True)
        line_count = len(text.splitlines())
        if not 101 <= line_count <= 499:
            raise AssertionError(
                "LINE_LAW_101_499_FAILED:"
                + relative.as_posix()
                + ":"
                + str(line_count)
            )


def _assert_gui_integration(root: Path) -> None:
    text = (root / GUI).read_text(encoding="utf-8-sig")
    required = (
        "from .main_workbench_sonar import (",
        "sync_main_workbench_sonar(window, state)",
        "start_main_workbench_package_sonar(window)",
        "update_main_workbench_package_sonar(window, status)",
        "finish_main_workbench_package_sonar(",
    )
    for marker in required:
        if marker not in text:
            raise AssertionError("GUI_SONAR_INTEGRATION_MISSING:" + marker)


def _assert_fake_runtime(root: Path) -> None:
    FakeMonitor.instances.clear()
    module = _load_sonar_module(root)
    window = FakeWindow()
    running = FakeState(
        generation=3,
        running=True,
        cancel_requested=False,
        stage="PLAN_INTAKE",
        terminal_status="",
        message="Capturing the selected Planner plan.",
        blockers=(),
    )
    module.sync_main_workbench_sonar(window, running)
    if not module.main_workbench_sonar_is_active(window):
        raise AssertionError("SONAR_ACTIVE_FLAG_NOT_SET")
    monitor = getattr(window, module._MONITOR_ATTR, None)
    if monitor is None or monitor.calls[-1][0] != "start":
        raise AssertionError("SONAR_RUNNING_CALL_MISSING")

    aqr = FakeState(
        generation=3,
        running=True,
        cancel_requested=False,
        stage="ADVANCED_QUALITY_REVIEW",
        terminal_status="",
        message="Advanced Quality Review is running.",
        blockers=(),
    )
    module.sync_main_workbench_sonar(window, aqr)
    if "guarded quality review" not in monitor.calls[-1][2][0].lower():
        raise AssertionError("SONAR_AQR_STAGE_LABEL_MISSING")

    ready = FakeState(
        generation=3,
        running=False,
        cancel_requested=False,
        stage="TERMINAL",
        terminal_status=READY,
        message="Ready.",
        blockers=(),
    )
    module.sync_main_workbench_sonar(window, ready)
    if module.main_workbench_sonar_is_active(window):
        raise AssertionError("SONAR_ACTIVE_FLAG_NOT_CLEARED")
    if monitor.calls[-1][0] != "success":
        raise AssertionError("SONAR_READY_SETTLEMENT_NOT_SUCCESS")

    failed = FakeState(
        generation=4,
        running=False,
        cancel_requested=False,
        stage="TERMINAL",
        terminal_status=FAILED,
        message="Pipeline failed.",
        blockers=("EXACT_BLOCKER",),
    )
    module.sync_main_workbench_sonar(window, failed)
    if monitor.calls[-1][0] != "error":
        raise AssertionError("SONAR_FAILURE_SETTLEMENT_NOT_ERROR")

    module.start_main_workbench_package_sonar(window)
    module.update_main_workbench_package_sonar(window, "CANCEL_REQUESTED")
    module.finish_main_workbench_package_sonar(
        window,
        "READY",
        "Exchange EXCH-0001 is verified and ready.",
    )
    if monitor.calls[-1][0] != "success":
        raise AssertionError("PACKAGE_SONAR_READY_NOT_SUCCESS")
    if module.main_workbench_sonar_is_active(window):
        raise AssertionError("PACKAGE_SONAR_ACTIVE_FLAG_NOT_CLEARED")
    if len(FakeMonitor.instances) != 1:
        raise AssertionError("MAIN_WORKBENCH_MONITOR_NOT_REUSED")


def _assert_aqr_sonar_suppression(root: Path) -> None:
    FakeMonitor.instances.clear()
    module = _load_aqr_sonar_module(root)
    window = FakeWindow()
    setattr(window, "_large_file_refactor_main_workbench_sonar_active", True)
    module.start_aqr_sonar(window)
    if FakeMonitor.instances:
        raise AssertionError("AQR_DUPLICATE_MONITOR_CREATED")
    setattr(window, "_large_file_refactor_main_workbench_sonar_active", False)
    module.start_aqr_sonar(window)
    if len(FakeMonitor.instances) != 1:
        raise AssertionError("AQR_MANUAL_MONITOR_NOT_AVAILABLE")


def _load_sonar_module(root: Path) -> ModuleType:
    package = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    _install_fake_packages(package)
    models = ModuleType(package + ".main_workbench_pipeline_models")
    models.MAIN_WORKBENCH_CANCELLED = CANCELLED
    models.MAIN_WORKBENCH_FAILED = FAILED
    models.MAIN_WORKBENCH_READY = READY
    models.MAIN_WORKBENCH_STALE = STALE
    models.MAIN_WORKBENCH_WEB_AI_BLOCKED = WEB_AI_BLOCKED
    models.MainWorkbenchControllerState = FakeState
    sys.modules[models.__name__] = models
    return _load_module(
        package + ".main_workbench_sonar",
        root / SONAR,
    )


def _load_aqr_sonar_module(root: Path) -> ModuleType:
    package = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    _install_fake_packages(package)
    return _load_module(package + ".advanced_quality_review_sonar", root / AQR_SONAR)


def _install_fake_packages(package: str) -> None:
    parts = package.split(".")
    for index in range(1, len(parts) + 1):
        name = ".".join(parts[:index])
        if name not in sys.modules:
            module = ModuleType(name)
            module.__path__ = []
            sys.modules[name] = module
    templates = "kanda_reasoner_app.templates"
    if templates not in sys.modules:
        module = ModuleType(templates)
        module.__path__ = []
        sys.modules[templates] = module
    green = ModuleType(templates + ".green_sonar_monitor")
    green.GreenSonarActivityMonitor = FakeMonitor
    sys.modules[green.__name__] = green


def _load_module(name: str, path: Path) -> ModuleType:
    sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("MODULE_SPEC_UNAVAILABLE:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _assert_real_pyside_smoke(root: Path, *, required: bool) -> None:
    try:
        import PySide6  # noqa: F401
    except ImportError:
        if required:
            raise AssertionError("REAL_PYSIDE6_GUI_IMPORT_SMOKE_REQUIRED")
        print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: SKIP_UNAVAILABLE")
        return
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, str(root))
    try:
        from PySide6.QtWidgets import QApplication, QWidget
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_sonar import (
            sync_main_workbench_sonar,
        )

        app = QApplication.instance() or QApplication([])
        widget = QWidget()
        state = FakeState(
            generation=1,
            running=True,
            cancel_requested=False,
            stage="PLAN_INTAKE",
            terminal_status="",
            message="Real PySide6 smoke.",
            blockers=(),
        )
        sync_main_workbench_sonar(widget, state)
        app.processEvents()
        if not hasattr(widget, "_large_file_refactor_main_workbench_sonar_monitor"):
            raise AssertionError("REAL_PYSIDE6_SONAR_MONITOR_NOT_CREATED")
        print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: PASS")
    finally:
        try:
            sys.path.remove(str(root))
        except ValueError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
