# project-path: tools/validate_project_structure_3d_visualizer_v1b.py
"""Focused validator for Project Structure 3D v1B evidence integration."""

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

FEATURE_ID = "project-structure-3d-visualizer-v1b-r3-boundary"
REQUIRED_FILES = (
    "kanda_reasoner_app/project_structure_visualizer/details_presenter.py",
    "kanda_reasoner_app/project_structure_visualizer/fixture_graph.py",
    "kanda_reasoner_app/project_structure_visualizer/graph_schema.py",
    "kanda_reasoner_app/project_structure_visualizer/graph_snapshot_builder.py",
    "kanda_reasoner_app/project_structure_visualizer/graph_snapshot_primitives.py",
    "kanda_reasoner_app/project_structure_visualizer/graph_view_filters.py",
    "kanda_reasoner_app/project_structure_visualizer/project_structure_3d_tab.py",
    "kanda_reasoner_app/project_structure_visualizer/tab_evidence_mixin.py",
    "kanda_reasoner_app/project_structure_visualizer/web/graph_renderer.js",
    "kanda_reasoner_app/project_structure_visualizer/web/index_template.html",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative_path: str) -> str:
    """Read one UTF-8 project file."""
    return (root / relative_path).read_text(encoding="utf-8", errors="strict")


def validate_source_contract(root: Path) -> None:
    """Validate syntax, size, authority, and canonical-evidence imports."""
    forbidden_runtime_imports = {"socket", "subprocess"}
    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        require(path.is_file(), "missing required file: " + relative_path)
        source = path.read_text(encoding="utf-8", errors="strict")
        if path.suffix in {".py", ".js"}:
            require(
                len(source.splitlines()) <= 500,
                "module exceeds 500 lines: " + relative_path,
            )
        if path.suffix != ".py":
            continue
        require(source.isascii(), "non-ASCII Python source: " + relative_path)
        tree = ast.parse(source, filename=relative_path)
        imports = {
            alias.name.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imports.update(
            str(node.module or "").split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        )
        if not relative_path.startswith("tools/"):
            require(
                not imports.intersection(forbidden_runtime_imports),
                "forbidden runtime authority import: " + relative_path,
            )
    builder = read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/graph_snapshot_builder.py",
    )
    require("collect_reasoner_symbol_atlas_complete_json_files" in builder, "adapter")
    require("load_reasoner_symbol_atlas_complete_json" in builder, "loader")
    require("os.walk" not in builder, "new source scanner")
    require("rglob(\"*.py\")" not in builder, "new Python scanner")
    require("analysis_json_complete_dir" in builder, "Project Support path owner")
    require("project_analysis_evidence_root" in builder, "Project Support containment owner")
    print("PROJECT_STRUCTURE_3D_V1B_SOURCE_CONTRACT: PASS")
    print("PROJECT_STRUCTURE_3D_V1B_NO_SECOND_SCANNER: PASS")


def synthetic_complete_json(project_root: Path) -> Path:
    """Write one deterministic complete JSON evidence fixture."""
    from kanda_reasoner_app.project_analysis_evidence_paths import (
        analysis_json_complete_dir,
    )

    evidence = analysis_json_complete_dir(project_root)
    evidence.mkdir(parents=True, exist_ok=True)
    path = evidence / (project_root.name + "__complete.json")
    payload = {
        "source_file_index": {
            "app/__init__.py": {
                "file": "app/__init__.py",
                "module_name": "app.__init__",
                "line_count": 2,
                "symbol_count": 0,
            },
            "app/main.py": {
                "file": "app/main.py",
                "module_name": "app.main",
                "line_count": 80,
                "symbol_count": 3,
            },
            "app/gui/window.py": {
                "file": "app/gui/window.py",
                "module_name": "app.gui.window",
                "line_count": 120,
                "symbol_count": 5,
            },
            "tools/validate_app.py": {
                "file": "tools/validate_app.py",
                "module_name": "tools.validate_app",
                "line_count": 40,
                "symbol_count": 1,
            },
            "backup/old.py": {
                "file": "backup/old.py",
                "module_name": "backup.old",
                "line_count": 90,
                "symbol_count": 2,
            },
        },
        "symbol_index": {"main": {"file": "app/main.py", "kind": "function"}},
        "primary_definition_index": {"main": "app/main.py"},
        "import_graph": {
            "app.__init__": [],
            "app.main": ["app.gui.window", "PySide6.QtWidgets", "json"],
            "app.gui.window": ["app.main"],
            "tools.validate_app": ["app.main"],
        },
        "web_ai_file_responsibility_index": {
            "app/main.py": {"primary_responsibility": "Application entry point."},
            "app/gui/window.py": {"primary_responsibility": "Main GUI window."},
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def validate_snapshot_builder(root: Path) -> None:
    """Validate canonical evidence, fallback, filtering, and stable IDs."""
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_structure_visualizer.graph_snapshot_builder import (
        build_project_graph_snapshot,
    )
    from kanda_reasoner_app.project_structure_visualizer.graph_view_filters import (
        filter_graph_snapshot,
    )

    ambient = environment_snapshot()
    with isolated_show_project_environment():
        require(
            all(value is None for value in environment_snapshot().values()),
            "show-project environment isolation failed",
        )
        with isolated_project_fixture(
            "kanda_visualizer_v1b_static_"
        ) as (project_root, support_root):
            evidence_path = synthetic_complete_json(project_root)
            require(
                evidence_path.is_relative_to(support_root),
                "complete JSON fixture escaped Project Support",
            )
            require(
                not evidence_path.is_relative_to(project_root),
                "complete JSON fixture leaked into project source",
            )
            build = build_project_graph_snapshot(project_root)
            require(not build.is_fixture, "canonical evidence unexpectedly fell back")
            require(
                build.source_label == "second_prompt_files/" + evidence_path.name,
                "wrong Project Support evidence file",
            )
            provenance = build.snapshot.get("source_provenance", {})
            require(provenance.get("authoritative") is False, "generated evidence authority")
            require(
                provenance.get("support_owner") == "project_support.second_prompt_files",
                "Project Support owner missing",
            )
            snapshot = build.snapshot
            node_ids = {node["id"] for node in snapshot["nodes"]}
            require("module:app/main.py" in node_ids, "main module missing")
            require("module:app/gui/window.py" in node_ids, "GUI module missing")
            require("module:backup/old.py" not in node_ids, "inactive backup leaked")
            require("external:PySide6" in node_ids, "external dependency missing")
            import_edges = [
                edge for edge in snapshot["edges"] if edge["relationship"] == "imports"
            ]
            require(import_edges, "import relationships missing")
            require(
                any(edge["target"] == "module:app/gui/window.py" for edge in import_edges),
                "internal import resolution missing",
            )
            architecture = filter_graph_snapshot(
                snapshot,
                mode="architecture",
                show_imports=True,
                show_external=True,
            )
            require(
                all(node["kind"] in {"project", "package", "external"} for node in architecture["nodes"]),
                "architecture filter leaked modules",
            )
            no_imports = filter_graph_snapshot(
                snapshot,
                mode="structure",
                show_imports=False,
                show_external=False,
            )
            require(
                all(edge["relationship"] != "imports" for edge in no_imports["edges"]),
                "imports filter failed",
            )
            require(
                all(not node.get("external") for node in no_imports["nodes"]),
                "external filter failed",
            )

        with isolated_project_fixture(
            "kanda_visualizer_v1b_empty_"
        ) as (empty_root, _empty_support_root):
            fallback = build_project_graph_snapshot(empty_root)
            require(fallback.is_fixture, "missing evidence did not use fixture")
            require(fallback.fallback_reason, "fallback reason missing")
    require(
        environment_snapshot() == ambient,
        "show-project environment was not restored",
    )
    print("PROJECT_STRUCTURE_3D_V1B_DYNAMIC_SUPPORT_EVIDENCE: PASS")
    print("PROJECT_STRUCTURE_3D_V1B_COMPLETE_JSON_ADAPTER: PASS")
    print("PROJECT_STRUCTURE_3D_V1B_FILTERS: PASS")
    print("PROJECT_STRUCTURE_3D_V1B_FIXTURE_FALLBACK: PASS")


def validate_ui_contract(root: Path) -> None:
    """Validate the visible controls and renderer-neutral filter route."""
    tab = read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/project_structure_3d_tab.py",
    )
    mixin = read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/tab_evidence_mixin.py",
    )
    details = read(
        root,
        "kanda_reasoner_app/project_structure_visualizer/details_presenter.py",
    )
    require("Refresh evidence" in tab, "refresh control")
    require("Architecture" in tab and "Structure" in tab, "view modes")
    require('QCheckBox("Imports")' in tab, "imports filter")
    require('QCheckBox("External")' in tab, "external filter")
    require("build_project_graph_snapshot" in mixin, "evidence builder route")
    require("filter_graph_snapshot" in mixin, "filter route")
    require("window.kandaProjectGraph.setGraph" in mixin, "renderer update route")
    require("Project source remains authoritative" in details, "provenance")
    print("PROJECT_STRUCTURE_3D_V1B_UI_CONTRACT: PASS")


def validate_javascript(root: Path) -> None:
    """Use Node syntax validation when available."""
    path = root / "kanda_reasoner_app/project_structure_visualizer/web/graph_renderer.js"
    try:
        result = subprocess.run(
            [os.environ.get("NODE_EXE", "node"), "--check", str(path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        print("PROJECT_STRUCTURE_3D_V1B_JAVASCRIPT: SKIPPED")
        return
    require(result.returncode == 0, result.stderr.strip() or "JavaScript syntax")
    print("PROJECT_STRUCTURE_3D_V1B_JAVASCRIPT: PASS")


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
    require(wait_until(app, lambda: bool(result["done"]), 10.0), "JS timeout")
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
    """Validate real evidence load, filters, search, and stale generations."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt
        from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox
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
        require(
            all(value is None for value in environment_snapshot().values()),
            "real Qt show-project environment isolation failed",
        )
        with isolated_project_fixture(
            "kanda_visualizer_v1b_qt_"
        ) as (project_root, support_root):
            evidence_path = synthetic_complete_json(project_root)
            require(
                evidence_path.is_relative_to(support_root),
                "real Qt complete JSON escaped Project Support",
            )
            require(
                not evidence_path.is_relative_to(project_root),
                "real Qt complete JSON leaked into project source",
            )
            widget = ProjectStructure3DWidget()
            widget.resize(1200, 760)
            widget.show()
            require(wait_until(app, lambda: bool(widget._renderer_ready), 45.0), "initial renderer")
            old_generation = widget._generation_id
            widget.set_project_root(project_root)
            require(wait_until(app, lambda: bool(widget._renderer_ready), 45.0), "evidence renderer")
            require(not widget._build_result.is_fixture, "real Qt evidence fallback")
            require(
                widget._build_result.source_label
                == "second_prompt_files/" + evidence_path.name,
                "real Qt Project Support provenance mismatch",
            )
            provenance = widget._source_snapshot.get("source_provenance", {})
            require(provenance.get("authoritative") is False, "real Qt evidence authority")
            require("LIVE EVIDENCE" in widget.source_badge.text(), "live badge")
            require(
                bool(run_javascript(app, widget._web_view.page(), "window.kandaProjectGraph.focusByQuery('main.py')")),
                "real evidence search",
            )
            require(
                wait_until(app, lambda: "main.py" in widget.details.toPlainText(), 8.0),
                "QWebChannel selection",
            )
            widget._on_node_selected(old_generation, "module:app/main.py")
            require("Application entry point" in widget.details.toPlainText(), "stale mutation")
            mode = widget.findChild(QComboBox, "projectStructure3DViewMode")
            require(mode is not None, "mode control")
            mode.setCurrentIndex(0)
            require(
                all(node["kind"] in {"project", "package", "external"} for node in widget._snapshot["nodes"]),
                "real Qt architecture filter",
            )
            imports = next(
                item for item in widget.findChildren(QCheckBox) if item.text() == "Imports"
            )
            imports.setChecked(False)
            require(
                all(edge["relationship"] != "imports" for edge in widget._snapshot["edges"]),
                "real Qt imports filter",
            )
            widget.close()
            widget.deleteLater()
            app.processEvents()
    require(
        environment_snapshot() == ambient,
        "real Qt show-project environment was not restored",
    )
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1B_DYNAMIC_SUPPORT_EVIDENCE: PASS")
    print("VALIDATED_PYTHON_EXECUTABLE: " + str(Path(sys.executable).resolve()))
    print("RUNTIME_PROVENANCE: " + runtime_provenance())
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1B: PASS")


def validate_static(root: Path) -> None:
    """Run source-only validation gates."""
    validate_source_contract(root)
    validate_snapshot_builder(root)
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
