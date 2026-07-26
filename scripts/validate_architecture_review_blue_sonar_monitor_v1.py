# project-path: scripts/validate_architecture_review_blue_sonar_monitor_v1.py
"""Validate the Architecture Review sonar monitor source-family contract."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AI_REVIEW = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "ai_review"
RUNNING_INDICATOR = AI_REVIEW / "running_indicator.py"
SONAR_PANEL = AI_REVIEW / "_running_indicator_sonar_panel.py"
GUI_INTEGRATION = AI_REVIEW / "gui_integration.py"
ARCH_GUI = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture_gui.py"


def _read(path: Path) -> str:
    """Return strict UTF-8 source for one required project file."""
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="strict")


def _require(condition: bool, message: str) -> None:
    """Raise AssertionError when one regression condition is not met."""
    if not condition:
        raise AssertionError(message)


def _function_names(source: str) -> set[str]:
    """Return all function names from one Python source string."""
    tree = ast.parse(source)
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _check_line_law(path: Path, source: str) -> None:
    """Require the project 101-499 physical-line law."""
    line_count = len(source.splitlines())
    _require(100 < line_count < 500, f"line law failed for {path.name}: {line_count}")


def main() -> int:
    """Validate public facade, visual helper, and integration call sites."""
    facade = _read(RUNNING_INDICATOR)
    helper = _read(SONAR_PANEL)
    family = facade + "\n" + helper
    functions = _function_names(facade)

    _check_line_law(RUNNING_INDICATOR, facade)
    _check_line_law(SONAR_PANEL, helper)

    _require("QProgressBar" not in family, "old QProgressBar processing animation is still present")
    _require("setRange(0, 0)" not in family, "old indeterminate progress-bar animation remains")
    _require("_COLOR_STEPS" not in family, "old color-step pulse implementation remains")
    _require("buttons_layout.addWidget" not in family, "indicator is still inserted into button row")

    facade_fragments = [
        "_MODE_CONTEXT",
        "Architecture Review",
        "Advisory AI review running",
        "Deterministic checks remain authoritative",
        "No automatic write is performed by this monitor",
        "install_tab1_activity_indicator",
        "_SonarFloatingPanel",
    ]
    for fragment in facade_fragments:
        _require(fragment in facade, "missing facade sonar monitor fragment: " + fragment)

    helper_fragments = [
        "_BlueSonarScope",
        "_SonarFloatingPanel",
        "QGraphicsDropShadowEffect",
        "_GRID_LINE",
        "_PANEL_WIDTH",
        "_PANEL_HEIGHT",
    ]
    for fragment in helper_fragments:
        _require(fragment in helper, "missing visual sonar monitor fragment: " + fragment)

    for method_name in (
        "start_heuristic",
        "start_ai_review",
        "finish_success",
        "finish_error",
        "set_idle",
        "_reposition",
        "eventFilter",
        "timerEvent",
    ):
        _require(method_name in functions, "missing required method: " + method_name)

    gui_integration = _read(GUI_INTEGRATION)
    arch_gui = _read(ARCH_GUI)
    _require("indicator.start_ai_review" in gui_integration, "AI review no longer starts indicator")
    _require("indicator.finish_success" in gui_integration, "AI review no longer finishes success indicator")
    _require("indicator.finish_error" in gui_integration, "AI review no longer finishes error indicator")
    _require("indicator.start_heuristic" in arch_gui, "heuristic run no longer starts indicator")
    _require("indicator.finish_success" in arch_gui, "heuristic run no longer finishes success indicator")
    _require("indicator.finish_error" in arch_gui, "heuristic run no longer finishes error indicator")

    print("VALIDATION OK: architecture-review-blue-sonar-monitor-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
