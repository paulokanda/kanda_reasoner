# project-path: tools/validate_project_structure_3d_visualizer_v1c.py
"""Focused validator for Project Structure 3D v1C semantic evidence."""

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

FEATURE_ID = "project-structure-3d-visualizer-v1c-r3"
VISUALIZER_ROOT = "kanda_reasoner_app/project_structure_visualizer/"
REQUIRED_FILES = (
    VISUALIZER_ROOT + "details_presenter.py",
    VISUALIZER_ROOT + "graph_protection_status.py",
    VISUALIZER_ROOT + "graph_schema.py",
    VISUALIZER_ROOT + "graph_semantic_edges.py",
    VISUALIZER_ROOT + "graph_semantic_enrichment.py",
    VISUALIZER_ROOT + "graph_snapshot_builder.py",
    VISUALIZER_ROOT + "graph_snapshot_primitives.py",
    VISUALIZER_ROOT + "graph_symbol_nodes.py",
    VISUALIZER_ROOT + "graph_view_filters.py",
    VISUALIZER_ROOT + "project_structure_3d_tab.py",
    VISUALIZER_ROOT + "tab_evidence_mixin.py",
    VISUALIZER_ROOT + "tab_style.py",
    VISUALIZER_ROOT + "web/graph_renderer.js",
)
SEMANTIC_RELATIONSHIPS = {"calls", "inherits", "validates", "protects"}

def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative_path: str) -> str:
    """Read one UTF-8 project file."""
    return (root / relative_path).read_text(encoding="utf-8", errors="strict")


def validate_source_contract(root: Path) -> None:
    """Validate syntax, module size, read-only authority, and no scanner."""
    forbidden_runtime_imports = {"socket", "subprocess"}
    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        require(path.is_file(), "missing required file: " + relative_path)
        source = read(root, relative_path)
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
    combined = "\n".join(
        read(root, relative_path)
        for relative_path in REQUIRED_FILES
        if relative_path.endswith(".py")
    )
    for forbidden in ("os.walk", 'rglob("*.py")', "write_freeze_index"):
        require(forbidden not in combined, "parallel scanner/write authority: " + forbidden)
    require("build_freezes" in combined, "read-only Freeze owner is missing")
    require("enrich_graph_semantics" in combined, "semantic owner is missing")
    require("call_edges" in combined, "call evidence is missing")
    require("web_ai_test_protection_index" in combined, "test protection evidence is missing")
    print("PROJECT_STRUCTURE_3D_V1C_SOURCE_CONTRACT: PASS")
    print("PROJECT_STRUCTURE_3D_V1C_NO_SECOND_SCANNER: PASS")
    print("PROJECT_STRUCTURE_3D_V1C_READ_ONLY_FREEZE_EVIDENCE: PASS")

def validate_semantic_snapshot(root: Path) -> None:
    """Validate symbols, calls, inheritance, tests, Freeze, and filters."""
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
            "kanda_visualizer_v1c_static_"
        ) as (project_root, support_root):
            evidence_path = write_semantic_complete_json(project_root)
            freeze_entry = write_semantic_freeze_entry(project_root)
            require(
                evidence_path.is_relative_to(support_root),
                "complete JSON fixture escaped the resolved support root",
            )
            require(
                not evidence_path.is_relative_to(project_root),
                "complete JSON fixture leaked into project source",
            )
            require(
                freeze_entry.is_relative_to(support_root),
                "Freeze fixture escaped the resolved support root",
            )
            build = build_project_graph_snapshot(project_root)
            require(not build.is_fixture, "semantic complete JSON fell back")
            require(
                build.source_label == "second_prompt_files/" + evidence_path.name,
                "Project Support provenance label mismatch",
            )
            snapshot = build.snapshot
            provenance = snapshot.get("source_provenance", {})
            require(provenance.get("authoritative") is False, "generated evidence authority")
            require(
                provenance.get("support_owner") == "project_support.second_prompt_files",
                "Project Support owner missing",
            )
            node_ids = {node["id"] for node in snapshot["nodes"]}
            required_nodes = {
                "class:app/base.py:Base",
                "class:app/child.py:Child",
                "function:app/child.py:Child.run",
                "function:app/helpers.py:helper",
                "module:tests/test_child.py",
            }
            require(required_nodes.issubset(node_ids), "semantic nodes missing")
            by_id = {node["id"]: node for node in snapshot["nodes"]}
            require(by_id["module:tests/test_child.py"]["kind"] == "validator", "test kind")
            require(by_id["module:app/child.py"]["protected"], "test protection missing")
            require(by_id["module:app/child.py"]["frozen"], "Freeze status missing")
            require(by_id["class:app/child.py:Child"]["frozen"], "class Freeze status")
            relationships = {edge["relationship"] for edge in snapshot["edges"]}
            require(SEMANTIC_RELATIONSHIPS.issubset(relationships), "semantic edges missing")
            require(snapshot["statistics"]["class_count"] >= 2, "class statistics")
            require(snapshot["statistics"]["function_count"] >= 3, "function statistics")
            no_symbols = filter_graph_snapshot(
                snapshot,
                mode="structure",
                show_imports=True,
                show_external=True,
                show_symbols=False,
                show_semantic=True,
            )
            require(
                all(node["kind"] not in {"class", "function"} for node in no_symbols["nodes"]),
                "symbols filter failed",
            )
            no_semantic = filter_graph_snapshot(
                snapshot,
                mode="structure",
                show_imports=True,
                show_external=True,
                show_symbols=True,
                show_semantic=False,
            )
            require(
                all(edge["relationship"] not in SEMANTIC_RELATIONSHIPS for edge in no_semantic["edges"]),
                "semantic relationship filter failed",
            )
    require(
        environment_snapshot() == ambient,
        "show-project environment was not restored",
    )
    print("V1C_FREEZE_FIXTURE_ENV_ISOLATION: PASS")
    print("V1C_WINDOWS_SHOW_PROJECT_ROOT_ISOLATION: PASS")
    print("PROJECT_STRUCTURE_3D_DYNAMIC_SUPPORT_EVIDENCE: PASS")
    print("PROJECT_STRUCTURE_3D_GENERATED_EVIDENCE_NON_AUTHORITATIVE: PASS")
    print("PROJECT_STRUCTURE_3D_V1C_SYMBOL_NODES: PASS")
    print("PROJECT_STRUCTURE_3D_V1C_CALLS_AND_INHERITANCE: PASS")
    print("PROJECT_STRUCTURE_3D_V1C_VALIDATOR_COVERAGE: PASS")
    print("PROJECT_STRUCTURE_3D_V1C_FREEZE_STATUS: PASS")
    print("PROJECT_STRUCTURE_3D_V1C_FILTERS: PASS")


def validate_ui_contract(root: Path) -> None:
    """Validate compact controls and preserved scoped white-text styling."""
    tab = read(root, VISUALIZER_ROOT + "project_structure_3d_tab.py")
    style = read(root, VISUALIZER_ROOT + "tab_style.py")
    mixin = read(root, VISUALIZER_ROOT + "tab_evidence_mixin.py")
    details = read(root, VISUALIZER_ROOT + "details_presenter.py")
    require('QCheckBox("Symbols")' in tab, "Symbols control")
    require('QCheckBox("Semantic")' in tab, "Semantic control")
    require("project_structure_3d_style" in tab, "style owner")
    require("placeholder-text-color: #ffffff" in style, "white placeholder QSS")
    require("projectStructure3DToolbar QPushButton" in style and "color: #ffffff;" in style, "white buttons")
    require("_show_symbols" in mixin and "_show_semantic" in mixin, "filter state")
    require("read-only semantic view" in details or "v1D stable layout" in details, "semantic details")
    require("Project source remains authoritative" in details, "provenance")
    print("PROJECT_STRUCTURE_3D_V1C_UI_CONTRACT: PASS")
    print("PROJECT_STRUCTURE_3D_UI_CHROME_WHITE_REGRESSION: PASS")


def validate_javascript(root: Path) -> None:
    """Validate the unchanged renderer syntax when Node is available."""
    path = root / (VISUALIZER_ROOT + "web/graph_renderer.js")
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
        print("PROJECT_STRUCTURE_3D_V1C_JAVASCRIPT: SKIPPED")
        return
    require(result.returncode == 0, result.stderr.strip() or "JavaScript syntax")
    print("PROJECT_STRUCTURE_3D_V1C_JAVASCRIPT: PASS")


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
    """Validate real Qt semantic controls, search, and renderer updates."""
    try:
        from PySide6.QtCore import QCoreApplication, Qt
        from PySide6.QtWidgets import QApplication, QCheckBox
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
            "kanda_visualizer_v1c_qt_"
        ) as (project_root, support_root):
            evidence_path = write_semantic_complete_json(project_root)
            freeze_entry = write_semantic_freeze_entry(project_root)
            require(
                evidence_path.is_relative_to(support_root),
                "real Qt complete JSON fixture escaped the resolved support root",
            )
            require(
                not evidence_path.is_relative_to(project_root),
                "real Qt complete JSON fixture leaked into project source",
            )
            require(
                freeze_entry.is_relative_to(support_root),
                "real Qt Freeze fixture escaped the resolved support root",
            )
            widget = ProjectStructure3DWidget()
            widget.resize(1400, 820)
            widget.show()
            require(wait_until(app, lambda: bool(widget._renderer_ready), 45.0), "fixture renderer")
            widget.set_project_root(project_root)
            require(wait_until(app, lambda: bool(widget._renderer_ready), 45.0), "semantic renderer")
            require(not widget._build_result.is_fixture, "real Qt semantic fallback")
            require(
                widget._build_result.source_label
                == "second_prompt_files/" + evidence_path.name,
                "real Qt Project Support provenance label mismatch",
            )
            provenance = widget._source_snapshot.get("source_provenance", {})
            require(provenance.get("authoritative") is False, "real Qt evidence authority")
            require(
                provenance.get("support_owner") == "project_support.second_prompt_files",
                "real Qt Project Support owner missing",
            )
            require(any(node["kind"] == "class" for node in widget._snapshot["nodes"]), "classes hidden")
            require(any(edge["relationship"] == "calls" for edge in widget._snapshot["edges"]), "calls hidden")
            controls = {item.text(): item for item in widget.findChildren(QCheckBox)}
            require("Symbols" in controls and "Semantic" in controls, "semantic controls")
            controls["Symbols"].setChecked(False)
            require(
                all(node["kind"] not in {"class", "function"} for node in widget._snapshot["nodes"]),
                "real Qt Symbols filter",
            )
            controls["Symbols"].setChecked(True)
            controls["Semantic"].setChecked(False)
            require(
                all(edge["relationship"] not in SEMANTIC_RELATIONSHIPS for edge in widget._snapshot["edges"]),
                "real Qt Semantic filter",
            )
            controls["Semantic"].setChecked(True)
            require(
                bool(run_javascript(app, widget._web_view.page(), "window.kandaProjectGraph.focusByQuery('Child')")),
                "class search",
            )
            require(
                wait_until(app, lambda: "Child" in widget.details.toPlainText(), 8.0),
                "class details",
            )
            widget.close()
            widget.deleteLater()
            app.processEvents()
    require(
        environment_snapshot() == ambient,
        "real Qt show-project environment was not restored",
    )
    print("REAL_QT_V1C_FREEZE_FIXTURE_ENV_ISOLATION: PASS")
    print("REAL_QT_V1C_WINDOWS_SHOW_PROJECT_ROOT_ISOLATION: PASS")
    print("REAL_QT_PROJECT_STRUCTURE_3D_DYNAMIC_SUPPORT_EVIDENCE: PASS")
    print("VALIDATED_PYTHON_EXECUTABLE: " + str(Path(sys.executable).resolve()))
    print("RUNTIME_PROVENANCE: " + runtime_provenance())
    print("REAL_QT_PROJECT_STRUCTURE_3D_V1C: PASS")


def validate_static(root: Path) -> None:
    """Run source-only v1C validation gates."""
    validate_source_contract(root)
    validate_semantic_snapshot(root)
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
