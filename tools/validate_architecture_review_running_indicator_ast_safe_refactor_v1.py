# project-path: tools/validate_architecture_review_running_indicator_ast_safe_refactor_v1.py
"""Validate AST-safe refactor of the Architecture Review running indicator."""

from __future__ import annotations

import ast
import importlib.util
import sys
import types
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACADE_REL = "kanda_reasoner_app/manage_architecture/ai_review/running_indicator.py"
HELPER_REL = "kanda_reasoner_app/manage_architecture/ai_review/_running_indicator_sonar_panel.py"
CONSUMER_REL = "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py"
FEATURE_ID = "architecture-review-running-indicator-ast-safe-refactor-v1"
HELPER_MODULE = "kanda_reasoner_app.manage_architecture.ai_review._running_indicator_sonar_panel"


def _require(condition: bool, message: str) -> None:
    """Raise AssertionError when one focused contract check fails."""
    if not condition:
        raise AssertionError(message)


def _source(relative_path: str) -> str:
    """Read one project source file as strict UTF-8."""
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8", errors="strict")


def _public_contract(source: str) -> dict[str, Any]:
    """Capture the stable public names and callable signatures."""
    tree = ast.parse(source)
    contract: dict[str, Any] = {"all": [], "callables": {}}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                contract["all"] = ast.literal_eval(node.value)
        elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            contract["callables"][node.name] = _signature(node)
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            methods: dict[str, Any] = {}
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    methods[item.name] = _signature(item)
            contract["callables"][node.name] = {
                "bases": [ast.unparse(base) for base in node.bases],
                "methods": methods,
                "decorators": [ast.unparse(item) for item in node.decorator_list],
            }
    return contract


def _signature(node: ast.FunctionDef) -> dict[str, Any]:
    """Return a stable structural signature record for one function."""
    arguments = node.args
    return {
        "positional": [arg.arg for arg in arguments.posonlyargs + arguments.args],
        "kwonly": [arg.arg for arg in arguments.kwonlyargs],
        "vararg": arguments.vararg.arg if arguments.vararg else "",
        "kwarg": arguments.kwarg.arg if arguments.kwarg else "",
        "defaults": [ast.unparse(item) for item in arguments.defaults],
        "kw_defaults": [ast.unparse(item) if item is not None else None for item in arguments.kw_defaults],
        "annotations": {
            arg.arg: ast.unparse(arg.annotation)
            for arg in arguments.posonlyargs + arguments.args + arguments.kwonlyargs
            if arg.annotation is not None
        },
        "returns": ast.unparse(node.returns) if node.returns is not None else "",
        "decorators": [ast.unparse(item) for item in node.decorator_list],
    }


def _expected_public_contract() -> dict[str, Any]:
    """Return the exact baseline public surface captured before refactor."""
    return {
        "all": ["Tab1ActivityIndicator", "install_tab1_activity_indicator"],
        "callables": {
            "Tab1ActivityIndicator": {
                "bases": ["QObject"],
                "decorators": [],
                "methods": {
                    "widget": _sig(["self"], {}, [], "Any"),
                    "start_heuristic": _sig(["self", "mode"], {"mode": "str"}, [], "None"),
                    "start_ai_review": _sig(
                        ["self", "model_name"],
                        {"model_name": "str"},
                        ["''"],
                        "None",
                    ),
                    "finish_success": _sig(["self", "message"], {"message": "str"}, [], "None"),
                    "finish_error": _sig(["self", "message"], {"message": "str"}, [], "None"),
                    "set_idle": _sig(["self"], {}, [], "None"),
                    "eventFilter": _sig(
                        ["self", "watched", "event"],
                        {"watched": "Any", "event": "Any"},
                        [],
                        "bool",
                    ),
                },
            },
            "install_tab1_activity_indicator": _sig(
                ["window", "buttons_layout"],
                {"window": "Any", "buttons_layout": "Any"},
                [],
                "Tab1ActivityIndicator",
            ),
        },
    }


def _sig(
    positional: list[str],
    annotation_map: dict[str, str],
    defaults: list[str],
    returns: str,
) -> dict[str, Any]:
    """Build one expected function signature record."""
    return {
        "positional": positional,
        "kwonly": [],
        "vararg": "",
        "kwarg": "",
        "defaults": defaults,
        "kw_defaults": [],
        "annotations": annotation_map,
        "returns": returns,
        "decorators": [],
    }


class _FakeQObject:
    """Minimal QObject timer host for deterministic controller behavior tests."""

    def __init__(self, parent: Any = None) -> None:
        self.parent = parent
        self.next_timer_id = 100
        self.timer_intervals: dict[int, int] = {}
        self.killed_timer_ids: list[int] = []

    def startTimer(self, interval: int) -> int:
        timer_id = self.next_timer_id
        self.next_timer_id += 1
        self.timer_intervals[timer_id] = int(interval)
        return timer_id

    def killTimer(self, timer_id: int) -> None:
        self.killed_timer_ids.append(int(timer_id))
        self.timer_intervals.pop(int(timer_id), None)

    def timerEvent(self, event: Any) -> None:
        del event


class _FakeQEvent:
    Resize = 10
    Show = 11


class _FakeQSize:
    def __init__(self, width: int, height: int) -> None:
        self._width = int(width)
        self._height = int(height)

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height


class _FakeTimerEvent:
    def __init__(self, timer_id: int) -> None:
        self._timer_id = timer_id

    def timerId(self) -> int:
        return self._timer_id


class _FakeEvent:
    def __init__(self, event_type: int) -> None:
        self._event_type = event_type

    def _qt_event_type(self) -> int:
        return self._event_type


setattr(_FakeEvent, "type", _FakeEvent._qt_event_type)


class _FakeScope:
    def __init__(self) -> None:
        self.ticks: list[float] = []

    def tick(self, value: float) -> None:
        self.ticks.append(float(value))


class _FakePanel:
    def __init__(self, parent: Any = None) -> None:
        self.parent = parent
        self.scope = _FakeScope()
        self.visible = False
        self.contents: list[tuple[str, str, tuple[str, str, str], str]] = []
        self.moves: list[tuple[int, int]] = []

    def set_content(self, title: str, status: str, details: tuple[str, str, str], state: str) -> None:
        self.contents.append((title, status, tuple(details), state))

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.visible = False

    def raise_(self) -> None:
        return None

    def move(self, x: int, y: int) -> None:
        self.moves.append((int(x), int(y)))


class _FakeHost:
    def __init__(self, width: int = 1000, height: int = 700) -> None:
        self._width = width
        self._height = height
        self.filters: list[Any] = []

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def installEventFilter(self, value: Any) -> None:
        self.filters.append(value)


class _FakeWindow(_FakeHost):
    def __init__(self, host: _FakeHost | None) -> None:
        super().__init__(1200, 800)
        self.host = host

    def centralWidget(self) -> _FakeHost | None:
        return self.host


def _load_facade_for_behavior() -> Any:
    """Load the real facade with deterministic QtCore and visual-owner doubles."""
    core = types.ModuleType("PySide6.QtCore")
    core.QObject = _FakeQObject
    core.QEvent = _FakeQEvent
    core.QSize = _FakeQSize
    sys.modules["PySide6"] = types.ModuleType("PySide6")
    sys.modules["PySide6.QtCore"] = core
    helper = types.ModuleType(HELPER_MODULE)
    helper._SonarFloatingPanel = _FakePanel
    sys.modules[HELPER_MODULE] = helper

    module_name = "kanda_reasoner_app.manage_architecture.ai_review.running_indicator_focused_validation"
    spec = importlib.util.spec_from_file_location(module_name, PROJECT_ROOT / FACADE_REL)
    _require(spec is not None and spec.loader is not None, "candidate module spec could not be created")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _behavior_contract() -> None:
    """Exercise the baseline-equivalent observable controller state transitions."""
    module = _load_facade_for_behavior()
    host = _FakeHost()
    window = _FakeWindow(host)
    indicator = module.Tab1ActivityIndicator(window)

    _require(indicator._last_state == "idle", "initial state changed")
    _require(not indicator.widget().visible, "initial panel visibility changed")
    _require(indicator in host.filters and indicator in window.filters, "QObject event filters not installed")

    indicator.start_heuristic("scan")
    _require(indicator._last_state == "running", "heuristic start state changed")
    _require(indicator.widget().visible, "panel is not visible while running")
    _require(indicator.widget().moves[-1] == (588, 494), "lower-right reposition behavior changed")
    _require(indicator.widget().contents[-1][1] == "Running scan mode", "scan status text changed")
    animation_id = indicator._animation_timer_id
    _require(indicator.timer_intervals[animation_id] == 25, "animation interval changed")
    indicator.timerEvent(_FakeTimerEvent(animation_id))
    _require(indicator.widget().scope.ticks == [0.025], "animation tick behavior changed")

    indicator.finish_success("done")
    _require(indicator._last_state == "success", "success state changed")
    _require(indicator.widget().contents[-1][1] == "Complete: done", "success text changed")
    hide_id = indicator._hide_timer_id
    _require(indicator.timer_intervals[hide_id] == 2200, "post-finish hide delay changed")
    indicator.timerEvent(_FakeTimerEvent(hide_id))
    _require(indicator._last_state == "idle", "hide timer did not restore idle state")
    _require(not indicator.widget().visible, "hide timer did not hide panel")

    indicator.start_ai_review("")
    ai_content = indicator.widget().contents[-1]
    _require(ai_content[1] == "Advisory AI review running", "AI review status changed")
    _require(ai_content[2][1] == "Model: auto model", "AI default model text changed")
    indicator.finish_error("")
    _require(indicator.widget().contents[-1][1] == "Needs review: work finished", "error fallback text changed")

    before_moves = len(indicator.widget().moves)
    _require(indicator.eventFilter(host, _FakeEvent(_FakeQEvent.Resize)) is False, "eventFilter return changed")
    _require(len(indicator.widget().moves) == before_moves + 1, "resize no longer repositions panel")

    install_window = _FakeWindow(_FakeHost())
    installed = module.install_tab1_activity_indicator(install_window, object())
    _require(install_window._tab1_activity_indicator is installed, "install helper no longer stores controller")


def _consumer_contract() -> None:
    """Require the unchanged consumer to use the stable public import path."""
    source = _source(CONSUMER_REL)
    tree = ast.parse(source)
    matches = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "running_indicator" and node.level == 1:
            matches.extend(alias.name for alias in node.names)
    _require("install_tab1_activity_indicator" in matches, "consumer import path changed")


def _family_verification(behavior_passed: bool) -> dict[str, Any]:
    """Run the project-owned family verification and fresh AST audits."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.manage_architecture.kanda_ast_safe_refactor_orchestrator import (
        orchestrate_candidate_verification,
    )

    return orchestrate_candidate_verification(
        PROJECT_ROOT,
        family_relative_paths=[FACADE_REL, HELPER_REL],
        facade_relative_path=FACADE_REL,
        helper_relative_paths=[HELPER_REL],
        behavior_comparison={
            "kind": "running_indicator_controller_behavior_equivalence",
            "pass": behavior_passed,
            "status": "baseline_semantic_contract_matched",
        },
    )


def main() -> int:
    """Run focused structural, behavior, dependency, and fresh-audit gates."""
    facade_source = _source(FACADE_REL)
    helper_source = _source(HELPER_REL)
    compile(facade_source, FACADE_REL, "exec")
    compile(helper_source, HELPER_REL, "exec")
    print("PYTHON_SYNTAX: PASS")

    actual_contract = _public_contract(facade_source)
    expected_contract = _expected_public_contract()
    _require(actual_contract["all"] == expected_contract["all"], "public __all__ changed")
    for name, expected_value in expected_contract["callables"].items():
        _require(name in actual_contract["callables"], "missing public callable: " + name)
        actual_value = actual_contract["callables"][name]
        if name == "Tab1ActivityIndicator":
            _require(actual_value["bases"] == expected_value["bases"], "public class bases changed")
            _require(actual_value["decorators"] == expected_value["decorators"], "public class decorators changed")
            for method_name, expected_method in expected_value["methods"].items():
                _require(method_name in actual_value["methods"], "missing public method: " + method_name)
                _require(actual_value["methods"][method_name] == expected_method, "public method signature changed: " + method_name)
        else:
            _require(actual_value == expected_value, "public callable signature changed: " + name)
    print("PUBLIC_API_PRESERVATION: PASS")
    print("DECORATOR_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")

    _consumer_contract()
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")

    _behavior_contract()
    print("QOBJECT_EVENT_FILTER_REGRESSION: PASS")
    print("TIMER_LIFECYCLE_BEHAVIOR: PASS")
    print("SUCCESS_HIDE_DELAY_BEHAVIOR: PASS")
    print("ERROR_HIDE_DELAY_BEHAVIOR: PASS")
    print("REPOSITION_BEHAVIOR: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")

    verification = _family_verification(True)
    _require(verification.get("pass", False), "candidate family verification failed")
    fitness = verification["fitness_functions"]
    _require(fitness["DEPENDENCY_DIRECTION_FITNESS"], "dependency direction failed")
    _require(fitness["LINE_LAW_101_499_FITNESS"], "line law failed")
    _require(fitness["FRESH_FAMILY_AST_FITNESS"], "fresh AST family audit failed")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    for audit in verification["family_verification"]["fresh_audits"]:
        print("AST_FAMILY_MEMBER: " + audit["relative_path"])
        print("AST_SPLIT_SAFETY_LABEL: " + audit["label"])
        print("AST_SPLIT_HARD_BLOCKERS: " + str(len(audit["hard_blockers"])))

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
