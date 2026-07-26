# project-path: scripts/validate_architecture_review_green_sonar_ripple_v2.py
"""Validate the green sonar ripple source-family behavior contract."""

from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AI_REVIEW = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "ai_review"
RUNNING_INDICATOR = AI_REVIEW / "running_indicator.py"
SONAR_PANEL = AI_REVIEW / "_running_indicator_sonar_panel.py"


def _read(path: Path) -> str:
    """Return strict UTF-8 source for one required project file."""
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="strict")


def _require(condition: bool, message: str) -> None:
    """Raise AssertionError when one regression condition fails."""
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


def _imports_module(source: str, suffix: str) -> bool:
    """Return whether one source file imports the requested relative module."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").endswith(suffix):
            return True
    return False


def main() -> int:
    """Validate controller lifecycle plus private visual ripple implementation."""
    facade = _read(RUNNING_INDICATOR)
    helper = _read(SONAR_PANEL)
    family = facade + "\n" + helper
    functions = _function_names(facade)

    facade_lines = len(facade.splitlines())
    helper_lines = len(helper.splitlines())
    _require(100 < facade_lines < 500, f"running_indicator.py line law failed: {facade_lines}")
    _require(100 < helper_lines < 500, f"sonar helper line law failed: {helper_lines}")
    _require("QProgressBar" not in family, "old QProgressBar processing animation returned")
    _require("setRange(0, 0)" not in family, "old indeterminate progress-bar animation returned")
    _require("class Tab1ActivityIndicator(QObject):" in facade, "QObject event-filter repair regressed")
    _require("super().__init__(window)" in facade, "QObject base initialization regressed")

    required_helper_fragments = [
        '"#040A06"',
        '"#00CC66"',
        '"#AAFFCC"',
        "_GRID_LINE",
        "_waves: list[dict[str, float]]",
        "_sweep_crossed",
        "_energize_crossed_blips",
        "_draw_blip_waves",
        'wave["radius"] += dt * 0.72',
        "self._waves.append",
    ]
    for fragment in required_helper_fragments:
        _require(fragment in helper, "missing green sonar ripple fragment: " + fragment)

    for fragment in ("Floating green sonar monitor", "Architecture Review"):
        _require(fragment in facade, "missing green sonar controller fragment: " + fragment)

    for method_name in (
        "start_heuristic",
        "start_ai_review",
        "finish_success",
        "finish_error",
        "set_idle",
        "eventFilter",
        "timerEvent",
        "_reposition",
    ):
        _require(method_name in functions, "missing public indicator method: " + method_name)

    _require('_BLUE_BG = "#07111F"' not in family, "old blue background palette still active")
    _require('_BLUE_BORDER = "#38BDF8"' not in family, "old blue border palette still active")
    _require("buttons_layout.addWidget" not in family, "indicator returned to inline button-row layout")
    _require(_imports_module(facade, "_running_indicator_sonar_panel"), "facade no longer imports visual owner")
    _require(not _imports_module(helper, "running_indicator"), "visual owner must not import public facade")

    print("VALIDATION OK: architecture-review-green-sonar-ripple-v2")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
