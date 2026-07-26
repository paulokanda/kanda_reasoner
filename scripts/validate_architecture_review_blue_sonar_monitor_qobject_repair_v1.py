# project-path: scripts/validate_architecture_review_blue_sonar_monitor_qobject_repair_v1.py
"""Validate the sonar QObject event-filter repair after source-family split."""

from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AI_REVIEW = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "ai_review"
RUNNING_INDICATOR = AI_REVIEW / "running_indicator.py"
SONAR_PANEL = AI_REVIEW / "_running_indicator_sonar_panel.py"


def _read(path: Path) -> str:
    """Return strict UTF-8 text for one required file."""
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="strict")


def _require(condition: bool, message: str) -> None:
    """Raise AssertionError for one failed contract condition."""
    if not condition:
        raise AssertionError(message)


def _class_bases(source: str, class_name: str) -> list[str]:
    """Return simple base names for the selected class."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            bases: list[str] = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute):
                    bases.append(base.attr)
            return bases
    raise AssertionError(f"missing class: {class_name}")


def _method_body_source(source: str, class_name: str, method_name: str) -> str:
    """Return exact source lines for one class method."""
    tree = ast.parse(source)
    lines = source.splitlines()
    for cls in ast.walk(tree):
        if isinstance(cls, ast.ClassDef) and cls.name == class_name:
            for item in cls.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    start = item.lineno - 1
                    end = getattr(item, "end_lineno", item.lineno)
                    return "\n".join(lines[start:end])
    raise AssertionError(f"missing method: {class_name}.{method_name}")


def _qt_core_imports(source: str) -> set[str]:
    """Return names imported directly from PySide6.QtCore."""
    tree = ast.parse(source)
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "PySide6.QtCore":
            names.update(alias.asname or alias.name for alias in node.names)
    return names


def main() -> int:
    """Require QObject ownership and preserved event-filter installation."""
    facade = _read(RUNNING_INDICATOR)
    helper = _read(SONAR_PANEL)
    family = facade + "\n" + helper

    facade_lines = len(facade.splitlines())
    helper_lines = len(helper.splitlines())
    _require(100 < facade_lines < 500, f"running_indicator.py line law failed: {facade_lines}")
    _require(100 < helper_lines < 500, f"sonar helper line law failed: {helper_lines}")

    qt_core_imports = _qt_core_imports(facade)
    _require("QObject" in qt_core_imports, "QObject direct import is missing")
    _require("QEvent" in qt_core_imports, "QEvent direct import is missing")
    _require("QSize" in qt_core_imports, "QSize direct import is missing")
    _require("class Tab1ActivityIndicator(QObject):" in facade, "Tab1ActivityIndicator must inherit QObject")
    _require("super().__init__(window)" in facade, "Tab1ActivityIndicator must initialize QObject base")
    _require("install(self)" in facade, "event filter installation must still install the activity indicator object")
    _require("def eventFilter" in facade, "eventFilter method is missing")

    bases = _class_bases(facade, "Tab1ActivityIndicator")
    _require("QObject" in bases, "Tab1ActivityIndicator class base is not QObject")
    init_source = _method_body_source(facade, "Tab1ActivityIndicator", "__init__")
    _require("super().__init__(window)" in init_source, "QObject base initialization missing from __init__")

    _require("QProgressBar" not in family, "old QProgressBar processing animation returned")
    _require("setRange(0, 0)" not in family, "old indeterminate progress-bar animation returned")
    _require("_BlueSonarScope" in helper, "blue sonar scope missing from visual owner")
    _require("_SonarFloatingPanel" in helper, "floating sonar panel missing from visual owner")
    _require("Architecture Review" in facade, "Architecture Review contextual text missing")

    print("VALIDATION OK: architecture-review-blue-sonar-monitor-qobject-repair-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
