"""Validate green sonar monitor rollout for the remaining processing tabs."""

from __future__ import annotations

import ast
from pathlib import Path

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "processing-tabs-green-sonar-monitor-v1"


def _read(rel_path: str) -> str:
    path = PROJECT_ROOT / rel_path
    if not path.is_file():
        raise AssertionError("missing file: " + rel_path)
    return path.read_text(encoding="utf-8")


def _assert_contains(text: str, fragment: str, rel_path: str) -> None:
    if fragment not in text:
        raise AssertionError("missing fragment in " + rel_path + ": " + fragment)


def _assert_absent(text: str, fragment: str, rel_path: str) -> None:
    if fragment in text:
        raise AssertionError("forbidden fragment in " + rel_path + ": " + fragment)


def _line_count(rel_path: str) -> int:
    return len(_read(rel_path).splitlines())


def _parse(rel_path: str) -> ast.AST:
    return ast.parse(_read(rel_path), filename=rel_path)


def validate_shared_monitor() -> None:
    expected_fragments = {
        "kanda_reasoner_app/templates/green_sonar_monitor.py": (
            "from ._green_sonar_activity_monitor import _GreenSonarActivityMonitor",
            "class GreenSonarActivityMonitor(_GreenSonarActivityMonitor)",
            "__all__ = [\"GreenSonarActivityMonitor\"]",
        ),
        "kanda_reasoner_app/templates/_green_sonar_runtime.py": (
            "SONAR_BORDER = \"#00CC66\"",
            "QColor = _qt_gui_attr(\"QColor\")",
            "QEvent = _qt_core_attr(\"QEvent\")",
            "_PANEL_WIDTH = 390",
        ),
        "kanda_reasoner_app/templates/_green_sonar_scope.py": (
            "class _SonarScope(QWidget)",
            "_energize_crossed_blips",
            "_draw_waves",
        ),
        "kanda_reasoner_app/templates/_green_sonar_panel.py": (
            "from ._green_sonar_scope import _SonarScope",
            "class _SonarPanel(QFrame)",
            "greenSonarActivityPanel",
            "_SonarScope(self)",
        ),
        "kanda_reasoner_app/templates/_green_sonar_activity_monitor.py": (
            "from ._green_sonar_panel import _SonarPanel",
            "class _GreenSonarActivityMonitor(QObject)",
            "installEventFilter",
            "_panel.scope.tick(0.025)",
        ),
    }

    for rel, fragments in expected_fragments.items():
        text = _read(rel)
        _parse(rel)
        for fragment in fragments:
            _assert_contains(text, fragment, rel)
        if _line_count(rel) > 400:
            raise AssertionError(rel + " exceeds 400-line practical target")

    facade_rel = "kanda_reasoner_app/templates/green_sonar_monitor.py"
    facade_text = _read(facade_rel)
    _assert_absent(facade_text, "from ._green_sonar_panel import _SonarPanel", facade_rel)
    _assert_absent(facade_text, "from ._green_sonar_scope import _SonarScope", facade_rel)
    print("GREEN_SONAR_PUBLIC_FACADE_SLIM: PASS")
    print("GREEN_SONAR_DEPENDENCY_TOPOLOGY_CURRENT: PASS")


def validate_workflow_review() -> None:
    rel = "kanda_reasoner_app/manage_workflows/ai_review/running_indicator.py"
    text = _read(rel)
    _parse(rel)
    _assert_contains(text, "GreenSonarActivityMonitor", rel)
    _assert_contains(text, "Workflow Review", rel)
    _assert_contains(text, "start_deterministic", rel)
    _assert_contains(text, "start_ai_review", rel)
    _assert_absent(text, "QProgressBar", rel)
    _assert_absent(text, "setRange(0, 0)", rel)
    _assert_absent(text, "_advance_animation", rel)


def validate_docstring_assistant() -> None:
    rel = "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py"
    text = _read(rel)
    _parse(rel)
    _assert_contains(text, "GreenSonarActivityMonitor", rel)
    _assert_contains(text, "Docstring Assistant", rel)
    _assert_contains(text, "_start_tab3_sonar", rel)
    _assert_contains(text, "_finish_tab3_sonar_success", rel)
    _assert_contains(text, "_finish_tab3_sonar_error", rel)
    _assert_absent(text, "setRange(0, 0)", rel)
    _assert_contains(text, "self._progress.setRange(0, 1)\n    self._progress.setValue(0)\n    self._progress.setFormat('Running...')", rel)
    _assert_contains(text, "self._progress.setRange(0, total)", rel)


def validate_show_project_to_ai() -> None:
    rel = "kanda_reasoner_app/reasoner_tools_shell/runner.py"
    text = _read(rel)
    _parse(rel)
    for fragment in (
        "_kanda_show_project_sonar",
        "GreenSonarActivityMonitor",
        "Show Project to AI",
        "CollectorRunnerWindow._start_busy_animation = _kanda_start_busy_animation",
        "CollectorRunnerWindow._stop_busy_animation = _kanda_stop_busy_animation",
        "CollectorRunnerWindow._tick_busy_animation = _kanda_tick_busy_animation",
    ):
        _assert_contains(text, fragment, rel)
    _assert_absent(text, "Project Reasoner v10 - Data Collector {frame}", rel)


def main() -> int:
    validate_shared_monitor()
    validate_workflow_review()
    validate_docstring_assistant()
    validate_show_project_to_ai()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
