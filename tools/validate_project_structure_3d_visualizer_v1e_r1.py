# project-path: tools/validate_project_structure_3d_visualizer_v1e_r1.py
"""Validate hidden-tab WebGL activation recovery for Project Structure 3D."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

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

FEATURE_ID = "project-structure-3d-visualizer-v1e-r1-hidden-tab-recovery"
ROOT = "kanda_reasoner_app/project_structure_visualizer/"
FILES = (
    ROOT + "project_structure_3d_tab.py",
    ROOT + "tab_viewport_activation_mixin.py",
    ROOT + "web/graph_renderer.js",
)


def read(root: Path, relative: str) -> str:
    """Read one strict UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8", errors="strict")


def validate_static(root: Path) -> None:
    """Validate the narrow production recovery contract."""
    for relative in FILES:
        path = root / relative
        require(path.is_file(), "missing file: " + relative)
        source = read(root, relative)
        require(len(source.splitlines()) <= 500, "module too large: " + relative)
        if path.suffix == ".py":
            require(source.isascii(), "non-ASCII Python: " + relative)
            ast.parse(source, filename=relative)

    tab = read(root, FILES[0])
    mixin = read(root, FILES[1])
    renderer = read(root, FILES[2])
    require("ProjectStructureViewportActivationMixin" in tab, "mixin owner missing")
    require("self._initialize_viewport_activation()" in tab, "timer init missing")
    require("self._schedule_viewport_activation(force_fit=True)" in tab, "ready recovery missing")
    require("def showEvent" in mixin and "def resizeEvent" in mixin, "visibility hooks missing")
    require("JSON.stringify(window.kandaProjectGraph" in mixin, "stable JS envelope missing")
    require("self._viewport_activation_attempts < 10" in mixin, "bounded retry missing")
    require("activateViewport" in renderer, "renderer activation API missing")
    require("rendererDiagnostics" in renderer, "renderer diagnostics missing")
    require("visibilitychange" in renderer, "document visibility recovery missing")
    require("ResizeObserver" in renderer, "resize observation missing")
    require("resumeAnimation()" in renderer, "render cycle resume missing")
    require("[80, 320, 900]" in renderer, "late fit retries missing")
    require(".cooldownTicks(1)" in renderer, "one render tick guard missing")
    require("getContext(\"2d\"" not in renderer, "parallel canvas renderer reintroduced")
    for forbidden in ("fetch(", "XMLHttpRequest", "https://", "http://"):
        require(forbidden not in renderer, "remote renderer authority: " + forbidden)
    print("PROJECT_STRUCTURE_3D_HIDDEN_TAB_RECOVERY_SOURCE: PASS")
    print("PROJECT_STRUCTURE_3D_VISIBILITY_RESIZE_HANDSHAKE: PASS")
    print("PROJECT_STRUCTURE_3D_LATE_FIT_RETRY: PASS")
    print("PROJECT_STRUCTURE_3D_GRAPH_TRUTH_UNCHANGED: PASS")


def validate_real_qt(root: Path) -> None:
    """Reproduce the real inactive-tab lifecycle and assert visible scene state."""
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
        with isolated_project_fixture("kanda_visualizer_v1e_r1_qt_") as (project_root, _):
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
            app.processEvents()
            widget.set_project_root(project_root)
            wait_until(app, lambda: bool(widget._page_load_ok), 30.0)
            host.setCurrentIndex(1)
            require(wait_until(app, lambda: bool(widget._renderer_ready), 60.0), "renderer ready")
            require(
                wait_until(
                    app,
                    lambda: bool(widget._last_viewport_diagnostics.get("ready")),
                    20.0,
                ),
                "hidden-tab activation did not recover",
            )
            page = widget._web_view.page()
            diagnostics = run_javascript(
                app,
                page,
                "window.kandaProjectGraph.rendererDiagnostics()",
            )
            require(diagnostics.get("ready") is True, "viewport not ready")
            require(int(diagnostics.get("hostWidth", 0)) > 300, "host width")
            require(int(diagnostics.get("hostHeight", 0)) > 300, "host height")
            require(int(diagnostics.get("canvasWidth", 0)) > 300, "canvas width")
            require(int(diagnostics.get("canvasHeight", 0)) > 300, "canvas height")
            require(int(diagnostics.get("graphNodeCount", 0)) > 0, "graph nodes absent")
            require(int(diagnostics.get("sceneChildCount", 0)) > 0, "scene content absent")

            host.setCurrentIndex(0)
            app.processEvents()
            host.setCurrentIndex(1)
            require(
                wait_until(
                    app,
                    lambda: bool(widget._last_viewport_diagnostics.get("ready")),
                    10.0,
                ),
                "second activation failed",
            )
            diagnostics = run_javascript(
                app,
                page,
                "window.kandaProjectGraph.activateViewport(true)",
            )
            require(diagnostics.get("ready") is True, "explicit activation failed")
            require(int(diagnostics.get("canvasWidth", 0)) > 300, "drawing buffer lost")
            host.close()
            host.deleteLater()
            app.processEvents()
    require(environment_snapshot() == ambient, "Qt fixture environment changed")
    print("REAL_QT_PROJECT_STRUCTURE_3D_HIDDEN_TAB_ACTIVATION: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_VISIBLE_DRAWING_BUFFER: PASS")
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
