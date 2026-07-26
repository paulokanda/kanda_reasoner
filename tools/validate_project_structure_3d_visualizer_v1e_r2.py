# project-path: tools/validate_project_structure_3d_visualizer_v1e_r2.py
"""Validate embedded-scene height recovery for Project Structure 3D."""

from __future__ import annotations

import argparse
import ast
import sys
import time
from pathlib import Path
from typing import Any

from project_structure_3d_test_environment import (
    environment_snapshot,
    isolated_project_fixture,
    isolated_show_project_environment,
)
from project_structure_3d_v1c_fixture import (
    write_semantic_complete_json,
    write_semantic_freeze_entry,
)
from validate_project_structure_3d_visualizer_v1e import (
    require,
    run_javascript,
    runtime_provenance,
    wait_until,
)

FEATURE_ID = "project-structure-3d-visualizer-v1e-r2-embedded-scene-height-recovery"
ROOT = "kanda_reasoner_app/project_structure_visualizer/"
CSS = ROOT + "web/graph_theme.css"
R1_VALIDATOR = "tools/validate_project_structure_3d_visualizer_v1e_r1.py"


def read(root: Path, relative: str) -> str:
    """Read one strict UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8", errors="strict")


def validate_static(root: Path) -> None:
    """Validate the embedded layout owner and retained recovery safeguards."""
    css_path = root / CSS
    validator_path = root / R1_VALIDATOR
    require(css_path.is_file(), "graph theme missing")
    require(validator_path.is_file(), "v1E-r1 validator missing")
    css = read(root, CSS)
    validator = read(root, R1_VALIDATOR)
    require(len(css.splitlines()) <= 500, "graph theme too large")
    require(len(validator.splitlines()) <= 500, "v1E-r1 validator too large")
    ast.parse(validator, filename=R1_VALIDATOR)
    require(
        ".visualizer-root.embedded {\n  display: grid;" in css,
        "embedded root no longer preserves grid height",
    )
    require(
        "grid-template-columns: minmax(0, 1fr);" in css,
        "embedded grid column contract missing",
    )
    require(
        ".visualizer-root.embedded .scene-shell {\n  width: 100%;\n  height: 100%;\n}" in css,
        "embedded scene-shell height owner missing",
    )
    require(
        ".visualizer-root.embedded {\n  display: block;" not in css,
        "zero-height embedded block regression remains",
    )
    require("HIDDEN_TAB_ACTIVATION" in validator, "r1 activation regression missing")
    print("PROJECT_STRUCTURE_3D_EMBEDDED_SCENE_HEIGHT_SOURCE: PASS")
    print("PROJECT_STRUCTURE_3D_ABSOLUTE_CHILD_HEIGHT_OWNER: PASS")
    print("PROJECT_STRUCTURE_3D_ZERO_HEIGHT_BLOCK_REGRESSION_REJECTED: PASS")
    print("PROJECT_STRUCTURE_3D_HIDDEN_TAB_RECOVERY_RETAINED: PASS")


def _layout_probe(app: Any, page: Any) -> dict[str, Any]:
    """Return observable embedded layout and renderer dimensions."""
    expression = """
(() => {
  const root = document.getElementById('visualizerRoot');
  const shell = document.querySelector('.scene-shell');
  const host = document.getElementById('graph3dHost');
  const canvas = host && host.querySelector('canvas');
  const diagnostics = window.kandaProjectGraph &&
    window.kandaProjectGraph.rendererDiagnostics ?
    window.kandaProjectGraph.rendererDiagnostics() : {};
  const rect = (element) => element ? element.getBoundingClientRect() :
    {width: 0, height: 0};
  const rootRect = rect(root);
  const shellRect = rect(shell);
  const hostRect = rect(host);
  const canvasRect = rect(canvas);
  return {
    rootDisplay: root ? getComputedStyle(root).display : '',
    rootWidth: Math.floor(rootRect.width),
    rootHeight: Math.floor(rootRect.height),
    shellWidth: Math.floor(shellRect.width),
    shellHeight: Math.floor(shellRect.height),
    hostWidth: Math.floor(hostRect.width),
    hostHeight: Math.floor(hostRect.height),
    canvasClientWidth: Math.floor(canvasRect.width),
    canvasClientHeight: Math.floor(canvasRect.height),
    diagnostics: diagnostics || {}
  };
})()
"""
    value = run_javascript(app, page, expression)
    require(isinstance(value, dict), "layout probe did not return an object")
    return value


def _wait_for_visible_scene(app: Any, page: Any, timeout: float) -> dict[str, Any]:
    """Wait for non-zero embedded layout and rendered scene content."""
    deadline = time.monotonic() + timeout
    last: dict[str, Any] = {}
    while time.monotonic() < deadline:
        app.processEvents()
        try:
            last = _layout_probe(app, page)
        except (AssertionError, RuntimeError, ValueError):
            time.sleep(0.05)
            continue
        diagnostics = last.get("diagnostics") or {}
        if (
            last.get("rootDisplay") == "grid"
            and int(last.get("shellHeight", 0)) > 300
            and int(last.get("hostHeight", 0)) > 300
            and int(last.get("canvasClientHeight", 0)) > 300
            and diagnostics.get("ready") is True
            and int(diagnostics.get("canvasHeight", 0)) > 300
            and int(diagnostics.get("graphNodeCount", 0)) > 0
            and int(diagnostics.get("sceneChildCount", 0)) > 0
        ):
            return last
        time.sleep(0.05)
    raise AssertionError("embedded scene did not become visible; last=" + repr(last))


def validate_real_qt(root: Path) -> None:
    """Reproduce inactive-tab activation and assert the actual CSS height owner."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt
        from PySide6.QtWidgets import QApplication, QTabWidget, QWidget
    except ImportError as exc:
        raise AssertionError("PySide6 import failed: " + str(exc)) from exc

    if QApplication.instance() is None:
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_structure_visualizer import ProjectStructure3DWidget

    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    ambient = environment_snapshot()
    with isolated_show_project_environment():
        with isolated_project_fixture("kanda_visualizer_v1e_r2_qt_") as (project_root, _):
            write_semantic_complete_json(project_root)
            write_semantic_freeze_entry(project_root)
            host = QTabWidget()
            placeholder = QWidget()
            widget = ProjectStructure3DWidget()
            host.addTab(placeholder, "Other")
            host.addTab(widget, "Project Structure 3D")
            host.resize(1500, 900)
            host.setCurrentIndex(0)
            host.show()
            require(wait_until(app, host.isVisible, 5.0), "fixture host not visible")
            widget.set_project_root(project_root)
            require(wait_until(app, lambda: bool(widget._page_load_ok), 30.0), "page load")
            host.setCurrentIndex(1)
            require(wait_until(app, lambda: widget.isVisibleTo(host), 5.0), "tab page not visible")
            require(wait_until(app, lambda: bool(widget._renderer_ready), 60.0), "renderer ready")
            page = widget._web_view.page()
            run_javascript(app, page, "window.kandaProjectGraph.activateViewport(true)")
            first = _wait_for_visible_scene(app, page, 25.0)
            require(first.get("rootDisplay") == "grid", "embedded root display")
            require(int(first.get("shellHeight", 0)) > 300, "scene shell height")
            require(int(first.get("hostHeight", 0)) > 300, "graph host height")

            host.setCurrentIndex(0)
            app.processEvents()
            host.setCurrentIndex(1)
            require(wait_until(app, lambda: widget.isVisibleTo(host), 5.0), "reactivated tab not visible")
            run_javascript(app, page, "window.kandaProjectGraph.activateViewport(true)")
            second = _wait_for_visible_scene(app, page, 15.0)
            require(int(second.get("hostHeight", 0)) > 300, "reactivated graph host height")
            host.close()
            host.deleteLater()
            app.processEvents()
    require(environment_snapshot() == ambient, "Qt fixture environment changed")
    print("REAL_QT_PROJECT_STRUCTURE_3D_EMBEDDED_SCENE_HEIGHT: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_VISIBLE_GRAPH_HOST: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_SCENE_CONTENT: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_REACTIVATION: PASS")
    print("VALIDATED_PYTHON_EXECUTABLE: " + str(Path(sys.executable).resolve()))
    print("RUNTIME_PROVENANCE: " + runtime_provenance())


def main() -> int:
    """Run static or real-Qt validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--real-qt-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.real_qt_only:
        validate_real_qt(root)
    elif args.static_only:
        validate_static(root)
    else:
        validate_static(root)
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
