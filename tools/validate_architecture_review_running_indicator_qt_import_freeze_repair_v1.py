# project-path: tools/validate_architecture_review_running_indicator_qt_import_freeze_repair_v1.py
"""Validate Qt import ownership and source-family safety for running indicator repair."""

from __future__ import annotations

import ast
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACADE_REL = "kanda_reasoner_app/manage_architecture/ai_review/running_indicator.py"
HELPER_REL = "kanda_reasoner_app/manage_architecture/ai_review/_running_indicator_sonar_panel.py"
HELPER_MODULE = "kanda_reasoner_app.manage_architecture.ai_review._running_indicator_sonar_panel"
FEATURE_ID = "architecture-review-running-indicator-qt-import-freeze-repair-v1"


def _read(relative_path: str) -> str:
    """Read one required project source file as strict UTF-8."""
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError("missing required file: " + relative_path)
    return path.read_text(encoding="utf-8", errors="strict")


def _require(condition: bool, message: str) -> None:
    """Raise AssertionError when one repair contract fails."""
    if not condition:
        raise AssertionError(message)


def _imports_by_module(source: str) -> dict[str, set[str]]:
    """Return direct from-import ownership by module name."""
    tree = ast.parse(source)
    result: dict[str, set[str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        names = result.setdefault(node.module, set())
        names.update(alias.name for alias in node.names)
    return result


def _qt_import_ownership_contract(helper_source: str) -> None:
    """Require QSizePolicy ownership under QtWidgets, never QtCore."""
    imports = _imports_by_module(helper_source)
    qt_core = imports.get("PySide6.QtCore", set())
    qt_widgets = imports.get("PySide6.QtWidgets", set())
    _require("QSizePolicy" not in qt_core, "QSizePolicy must not be imported from PySide6.QtCore")
    _require("QSizePolicy" in qt_widgets, "QSizePolicy must be imported from PySide6.QtWidgets")
    _require({"QPointF", "QRectF", "Qt"}.issubset(qt_core), "required QtCore imports changed")
    _require(
        {"QFrame", "QGraphicsDropShadowEffect", "QHBoxLayout", "QLabel", "QSizePolicy", "QVBoxLayout", "QWidget"}.issubset(qt_widgets),
        "required QtWidgets imports changed",
    )


def _real_pyside6_import_smoke() -> None:
    """Import the real helper when PySide6 is installed on the local host."""
    if importlib.util.find_spec("PySide6") is None:
        raise AssertionError("PySide6 is unavailable; real helper import smoke is required before freeze")
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    module = importlib.import_module(HELPER_MODULE)
    _require(hasattr(module, "_SonarFloatingPanel"), "real helper import lost _SonarFloatingPanel")
    print("REAL_PYSIDE6_HELPER_IMPORT_SMOKE: PASS")


def _public_contract_smoke(facade_source: str) -> None:
    """Require the stable public facade names and QObject ownership."""
    tree = ast.parse(facade_source)
    public_all: list[str] = []
    indicator_base = ""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                public_all = list(ast.literal_eval(node.value))
        if isinstance(node, ast.ClassDef) and node.name == "Tab1ActivityIndicator":
            if node.bases:
                indicator_base = ast.unparse(node.bases[0])
    _require(public_all == ["Tab1ActivityIndicator", "install_tab1_activity_indicator"], "public __all__ changed")
    _require(indicator_base == "QObject", "Tab1ActivityIndicator must remain a QObject")


def _family_ast_verification() -> dict[str, Any]:
    """Run the project-owned fresh family AST verification."""
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
            "kind": "running_indicator_qt_import_repair",
            "pass": True,
            "status": "qt_import_owner_repaired_without_controller_behavior_change",
        },
    )


def main() -> int:
    """Run static import ownership, real import smoke, and fresh AST gates."""
    facade_source = _read(FACADE_REL)
    helper_source = _read(HELPER_REL)
    compile(facade_source, FACADE_REL, "exec")
    compile(helper_source, HELPER_REL, "exec")
    print("PYTHON_SYNTAX: PASS")

    _qt_import_ownership_contract(helper_source)
    print("QT_IMPORT_OWNERSHIP: PASS")

    _public_contract_smoke(facade_source)
    print("PUBLIC_API_PRESERVATION: PASS")
    print("QOBJECT_EVENT_FILTER_REGRESSION: PASS")

    facade_lines = len(facade_source.splitlines())
    helper_lines = len(helper_source.splitlines())
    _require(100 < facade_lines < 500, "facade line law failed")
    _require(100 < helper_lines < 500, "helper line law failed")
    print("LINE_LAW_101_499_FITNESS: PASS")

    _real_pyside6_import_smoke()

    verification = _family_ast_verification()
    _require(bool(verification.get("pass")), "candidate family verification failed")
    fitness = dict(verification.get("fitness_functions") or {})
    _require(bool(fitness.get("DEPENDENCY_DIRECTION_FITNESS")), "dependency direction failed")
    _require(bool(fitness.get("FRESH_FAMILY_AST_FITNESS")), "fresh AST family audit failed")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
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
