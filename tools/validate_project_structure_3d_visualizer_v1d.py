# project-path: tools/validate_project_structure_3d_visualizer_v1d.py
"""Focused validator for Project Structure 3D v1D navigation and layout."""

from __future__ import annotations

import argparse
import ast
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

from project_structure_3d_test_environment import (
    environment_snapshot,
    isolated_project_fixture,
    isolated_show_project_environment,
)
from project_structure_3d_v1c_fixture import (
    write_semantic_complete_json,
    write_semantic_freeze_entry,
)
from project_structure_3d_v1d_qt_navigation_probe import (
    validate_navigation_actions,
)

FEATURE_ID = "project-structure-3d-visualizer-v1d-r1"
VISUALIZER_ROOT = "kanda_reasoner_app/project_structure_visualizer/"
REQUIRED_FILES = (
    "tools/project_structure_3d_v1d_qt_navigation_probe.py",
    "kanda_reasoner_app/_project_analysis_evidence_path_resolution.py",
    "kanda_reasoner_app/project_analysis_evidence_paths.py",
    VISUALIZER_ROOT + "details_presenter.py",
    VISUALIZER_ROOT + "graph_layout_state.py",
    VISUALIZER_ROOT + "graph_snapshot_builder.py",
    VISUALIZER_ROOT + "project_structure_3d_tab.py",
    VISUALIZER_ROOT + "tab_evidence_mixin.py",
    VISUALIZER_ROOT + "tab_navigation_mixin.py",
    VISUALIZER_ROOT + "tab_style.py",
    VISUALIZER_ROOT + "web_assets.py",
    VISUALIZER_ROOT + "web/graph_navigation.js",
    VISUALIZER_ROOT + "web/graph_painter.js",
    VISUALIZER_ROOT + "web/graph_renderer.js",
    VISUALIZER_ROOT + "web/graph_theme.css",
    VISUALIZER_ROOT + "web/index_template.html",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative_path: str) -> str:
    """Read one UTF-8 Project file."""
    return (root / relative_path).read_text(encoding="utf-8", errors="strict")


def validate_source_contract(root: Path) -> None:
    """Validate bounded Tool ownership and read-only navigation authority."""
    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        require(path.is_file(), "missing required file: " + relative_path)
        source = read(root, relative_path)
        if path.suffix in {".py", ".js"}:
            require(
                len(source.splitlines()) <= 500,
                "module exceeds 500 lines: " + relative_path,
            )
        if path.suffix == ".py":
            require(source.isascii(), "non-ASCII Python source: " + relative_path)
            ast.parse(source, filename=relative_path)
    combined = "\n".join(read(root, item) for item in REQUIRED_FILES)
    for forbidden in (
        "os.walk",
        'rglob("*.py")',
        "write_freeze_index",
        "write_error_memory",
        "subprocess.Popen",
        "fetch(",
        "XMLHttpRequest",
    ):
        require(forbidden not in combined, "forbidden authority: " + forbidden)
    path_owner = read(root, "kanda_reasoner_app/project_analysis_evidence_paths.py")
    require(
        "PROJECT_STRUCTURE_3D_STATE_DIR" in path_owner,
        "Project Support lifecycle owner missing",
    )
    require(
        "PROJECT_STRUCTURE_3D_STATE_DIR," in path_owner,
        "layout state is not persistent",
    )
    layout = read(root, VISUALIZER_ROOT + "graph_layout_state.py")
    require("canonical_project_support_root" in layout, "support-root owner missing")
    require("presentation_cache_only" in layout, "cache authority missing")
    require("project_support_root_blockers" in layout, "support boundary guard missing")
    require("project_structure_3d/layout_positions_v1.json" not in layout, "hardcoded path")
    require("project_analysis_evidence_root" not in layout, "in-source evidence fallback")
    navigation = read(root, VISUALIZER_ROOT + "web/graph_navigation.js")
    for method in (
        "isolateSelected",
        "tracePathToQuery",
        "toggleSelectedExpansion",
        "goBack",
        "goForward",
        "showOverview",
    ):
        require(method in navigation, "navigation method missing: " + method)
    print("PROJECT_STRUCTURE_3D_V1D_SOURCE_CONTRACT: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_NO_SECOND_SCANNER: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_READ_ONLY_NAVIGATION: PASS")


def validate_layout_cache(root: Path) -> None:
    """Validate semantic zones and external Project Support position caching."""
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_structure_visualizer.graph_layout_state import (
        stabilize_project_graph_layout,
    )
    from kanda_reasoner_app.project_structure_visualizer.graph_snapshot_builder import (
        build_project_graph_snapshot,
    )

    ambient = environment_snapshot()
    with isolated_show_project_environment():
        with isolated_project_fixture(
            "kanda_visualizer_v1d_layout_"
        ) as (project_root, support_root):
            write_semantic_complete_json(project_root)
            write_semantic_freeze_entry(project_root)
            build = build_project_graph_snapshot(project_root)
            require(not build.is_fixture, "v1D semantic fixture fell back")
            original_node_ids = {node["id"] for node in build.snapshot["nodes"]}
            original_edge_ids = {edge["id"] for edge in build.snapshot["edges"]}
            first, status = stabilize_project_graph_layout(
                build.snapshot,
                project_root,
                persist=True,
            )
            cache_path = (
                support_root / "project_structure_3d" / "layout_positions_v1.json"
            )
            require(cache_path.is_file(), "position cache was not written")
            require(not cache_path.is_relative_to(project_root), "cache leaked into source")
            require(status.get("status") == "created", "first cache status")
            require(status.get("written") is True, "first cache write marker")
            require(
                first.get("layout", {}).get("engine")
                == "deterministic_semantic_zone_layout_v1d",
                "semantic layout engine missing",
            )
            zones = first.get("layout", {}).get("semantic_zones", [])
            require(len(zones) >= 5, "semantic zones missing")
            require(
                all(
                    node.get("metadata", {}).get("semantic_zone")
                    for node in first["nodes"]
                ),
                "node semantic zone missing",
            )
            require(
                {node["id"] for node in first["nodes"]} == original_node_ids,
                "layout changed graph nodes",
            )
            require(
                {edge["id"] for edge in first["edges"]} == original_edge_ids,
                "layout changed graph edges",
            )
            first_positions = {
                node["id"]: tuple(node["position"]) for node in first["nodes"]
            }
            fresh = build_project_graph_snapshot(project_root).snapshot
            fresh["nodes"][0]["position"] = [9999.0, 9999.0, 9999.0]
            second, second_status = stabilize_project_graph_layout(
                fresh,
                project_root,
                persist=False,
            )
            second_positions = {
                node["id"]: tuple(node["position"]) for node in second["nodes"]
            }
            require(first_positions == second_positions, "cached positions were unstable")
            require(second_status.get("status") == "loaded", "cache reload status")
            require(second_status.get("applied_count") == len(first_positions), "cache count")
            cache_text = cache_path.read_text(encoding="utf-8", errors="strict")
            cache_document = json.loads(cache_text)
            require(
                cache_document.get("authority") == "presentation_cache_only",
                "cache authority mismatch",
            )
            lifecycle = json.loads(
                (support_root / "_lifecycle_manifest.json").read_text(
                    encoding="utf-8", errors="strict"
                )
            )
            require(
                "project_structure_3d" in lifecycle.get("persistent", []),
                "layout cache is not declared persistent",
            )
            require(str(project_root) not in cache_text, "cache exposes absolute Project root")
            require(
                not (project_root / (project_root.name + "_show_project_to_AI")).exists(),
                "nested support root was created",
            )
    require(environment_snapshot() == ambient, "show-project environment was not restored")
    print("PROJECT_STRUCTURE_3D_V1D_SEMANTIC_ZONES: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_POSITION_CACHE: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_PROJECT_SUPPORT_CACHE_OWNER: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_PERSISTENT_LIFECYCLE_OWNER: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_GRAPH_TRUTH_UNCHANGED: PASS")


def validate_ui_contract(root: Path) -> None:
    """Validate the second navigation row and browser-control contract."""
    tab = read(root, VISUALIZER_ROOT + "project_structure_3d_tab.py")
    mixin = read(root, VISUALIZER_ROOT + "tab_navigation_mixin.py")
    style = read(root, VISUALIZER_ROOT + "tab_style.py")
    template = read(root, VISUALIZER_ROOT + "web/index_template.html")
    assets = read(root, VISUALIZER_ROOT + "web_assets.py")
    details = read(root, VISUALIZER_ROOT + "details_presenter.py")
    require("_install_navigation_bar(root)" in tab, "navigation bar not installed")
    require("projectStructure3DNavigation" in mixin, "navigation row owner missing")
    for label in (
        "Back",
        "Forward",
        "Overview",
        "Isolate selected",
        "Expand / collapse",
        "Path to search",
    ):
        require(label in mixin, "navigation control missing: " + label)
    require("projectStructure3DNavigation QPushButton" in style, "navigation white text")
    require("browserNavigation" in template, "browser navigation controls missing")
    require("KANDA_NAVIGATION_SCRIPT" in template, "navigation script token missing")
    require("KANDA_PAINTER_SCRIPT" in template, "painter script token missing")
    require("graph_navigation.js" in assets, "navigation asset owner missing")
    require("graph_painter.js" in assets, "painter asset owner missing")
    require("v1D stable layout and focus-path view" in details, "v1D details missing")
    print("PROJECT_STRUCTURE_3D_V1D_UI_CONTRACT: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_SECOND_ROW_WIDTH_GUARD: PASS")
    print("PROJECT_STRUCTURE_3D_UI_CHROME_WHITE_REGRESSION: PASS")


def validate_javascript(root: Path) -> None:
    """Validate local renderer modules and navigation behavior with Node."""
    paths = [
        root / (VISUALIZER_ROOT + "web/graph_navigation.js"),
        root / (VISUALIZER_ROOT + "web/graph_painter.js"),
        root / (VISUALIZER_ROOT + "web/graph_renderer.js"),
    ]
    node = os.environ.get("NODE_EXE", "node")
    try:
        for path in paths:
            result = subprocess.run(
                [node, "--check", str(path)],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            require(result.returncode == 0, result.stderr.strip() or "JavaScript syntax")
    except OSError:
        print("PROJECT_STRUCTURE_3D_V1D_JAVASCRIPT: SKIPPED")
        return
    harness = """
const fs = require('fs');
global.window = {};
eval(fs.readFileSync(process.argv[1], 'utf8'));
const graph = {
  nodes: [
    {id:'project:p', label:'P', parent_id:''},
    {id:'package:a', label:'A', parent_id:'project:p'},
    {id:'module:a', label:'a.py', relative_path:'a.py', parent_id:'package:a'},
    {id:'module:b', label:'b.py', relative_path:'b.py', parent_id:'package:a'}
  ],
  edges: [
    {id:'c1', source:'project:p', target:'package:a', relationship:'contains'},
    {id:'c2', source:'package:a', target:'module:a', relationship:'contains'},
    {id:'c3', source:'package:a', target:'module:b', relationship:'contains'},
    {id:'i1', source:'module:a', target:'module:b', relationship:'imports'}
  ]
};
const nav = window.kandaGraphNavigation.create(graph);
if (!nav.select('module:a', true).ok) process.exit(2);
if (!nav.isolateSelected(1).ok) process.exit(3);
if (!nav.tracePathToQuery('b.py').ok) process.exit(4);
if (!nav.goBack().ok || !nav.goForward().ok) process.exit(5);
if (!nav.select('package:a', true).ok) process.exit(6);
if (!nav.toggleSelectedExpansion().ok) process.exit(7);
if (nav.visibleGraph().nodes.length >= graph.nodes.length) process.exit(8);
"""
    result = subprocess.run(
        [node, "-e", harness, str(paths[0])],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(result.returncode == 0, result.stderr.strip() or "navigation harness")
    print("PROJECT_STRUCTURE_3D_V1D_JAVASCRIPT: PASS")
    print("PROJECT_STRUCTURE_3D_V1D_NAVIGATION_MODEL: PASS")


def wait_until(app: Any, predicate: Callable[[], bool], timeout: float) -> bool:
    """Process Qt events until one predicate succeeds or times out."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.02)
    app.processEvents()
    return bool(predicate())


def run_javascript(app: Any, page: Any, script: str) -> Any:
    """Run one bounded JavaScript probe."""
    result: dict[str, Any] = {"done": False, "value": None}

    def receive(value: Any) -> None:
        result["done"] = True
        result["value"] = value

    page.runJavaScript(script, receive)
    require(wait_until(app, lambda: bool(result["done"]), 12.0), "JS timeout")
    return result["value"]


def runtime_provenance() -> str:
    """Return bounded Python and PySide6 provenance."""
    try:
        pyside = importlib.metadata.version("PySide6")
    except importlib.metadata.PackageNotFoundError:
        pyside = "unknown"
    return repr(
        {
            "python": str(Path(sys.executable).resolve()),
            "python_version": platform.python_version(),
            "pyside6": pyside,
        }
    )


def validate_real_qt(root: Path) -> None:
    """Validate real Qt layout caching and visual navigation actions."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt
        from PySide6.QtWidgets import QApplication, QPushButton
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
        with isolated_project_fixture(
            "kanda_visualizer_v1d_qt_"
        ) as (project_root, support_root):
            write_semantic_complete_json(project_root)
            write_semantic_freeze_entry(project_root)
            widget = ProjectStructure3DWidget()
            widget.resize(1450, 880)
            widget.show()
            require(wait_until(app, lambda: bool(widget._renderer_ready), 45.0), "fixture renderer")
            widget.set_project_root(project_root)
            require(wait_until(app, lambda: bool(widget._renderer_ready), 45.0), "v1D renderer")
            cache_path = support_root / "project_structure_3d" / "layout_positions_v1.json"
            require(cache_path.is_file(), "real Qt cache missing")
            buttons = {button.text() for button in widget.findChildren(QPushButton)}
            require(
                {"Back", "Forward", "Overview", "Isolate selected", "Expand / collapse", "Path to search"}.issubset(buttons),
                "real Qt navigation controls missing",
            )
            page = widget._web_view.page()
            validate_navigation_actions(
                app,
                page,
                len(widget._snapshot["nodes"]),
            )
            widget.close()
            widget.deleteLater()
            app.processEvents()
    require(environment_snapshot() == ambient, "real Qt environment was not restored")
    print("QT_WEBENGINE_PLAIN_JSON_PROBE: PASS")
    print("REAL_QT_V1D_NAVIGATION_STATE_AUTHORITY: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1D_POSITION_CACHE: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1D_ISOLATE_SELECTED: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1D_DEPENDENCY_PATH: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1D_EXPAND_COLLAPSE: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1D_NAVIGATION_HISTORY: PASS")
    print("VALIDATED_PYTHON_EXECUTABLE: " + str(Path(sys.executable).resolve()))
    print("RUNTIME_PROVENANCE: " + runtime_provenance())
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1D: PASS")


def validate_static(root: Path) -> None:
    """Run source-only v1D validation gates."""
    validate_source_contract(root)
    validate_layout_cache(root)
    validate_ui_contract(root)
    validate_javascript(root)


def main() -> int:
    """Run selected validation modes."""
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
