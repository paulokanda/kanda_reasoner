# project-path: tools/validate_project_structure_3d_import_structure_findings_v1.py
"""Validate import-only structural findings for Project Structure 3D."""

from __future__ import annotations

import argparse
from copy import deepcopy
import importlib.util
from pathlib import Path
import py_compile
from typing import Any

FEATURE_ID = "project-structure-3d-import-structure-findings-v1"

CHANGED_PYTHON = (
    "kanda_reasoner_app/project_structure_visualizer/graph_structure_analysis.py",
    "kanda_reasoner_app/project_structure_visualizer/graph_snapshot_builder.py",
    "kanda_reasoner_app/project_structure_visualizer/fixture_graph.py",
    "kanda_reasoner_app/project_structure_visualizer/graph_view_filters.py",
    "kanda_reasoner_app/project_structure_visualizer/details_presenter.py",
    "tools/validate_project_structure_3d_import_structure_findings_v1.py",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic assertion when a contract is not satisfied."""
    if not condition:
        raise AssertionError(message)


def _load_analysis(root: Path):
    """Load the isolated analysis module without importing GUI dependencies."""
    path = root / (
        "kanda_reasoner_app/project_structure_visualizer/"
        "graph_structure_analysis.py"
    )
    spec = importlib.util.spec_from_file_location(
        "kanda_project_structure_analysis_validation",
        path,
    )
    require(spec is not None and spec.loader is not None, "analysis spec missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _node(node_id: str, *, kind: str = "module", path: str = "") -> dict[str, Any]:
    """Return one minimal graph node for focused analysis fixtures."""
    return {
        "id": node_id,
        "kind": kind,
        "relative_path": path or node_id.replace(":", "/") + ".py",
        "metadata": {},
    }


def _edge(
    edge_id: str,
    source: str,
    target: str,
    relationship: str,
    confidence: str = "confirmed",
) -> dict[str, Any]:
    """Return one minimal graph edge for focused analysis fixtures."""
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relationship": relationship,
        "confidence": confidence,
        "metadata": {},
    }


def _validate_import_semantics(analysis_module: Any) -> None:
    """Prove import metrics do not reuse generic relationship degree."""
    nodes = [_node("module:a"), _node("module:b"), _node("validator:test")]
    edges = [
        _edge("contains:a", "module:b", "module:a", "contains"),
        _edge("protects:a", "module:b", "module:a", "protects"),
        _edge("validates:a", "validator:test", "module:a", "validates"),
        _edge("imports:a:b", "module:a", "module:b", "imports", "derived"),
    ]
    findings = analysis_module.analyze_graph_structure(nodes, edges)
    by_id = {node["id"]: node for node in nodes}
    require(by_id["module:a"]["metadata"]["import_fan_in"] == 0, "generic edges inflated import fan-in")
    require(by_id["module:b"]["metadata"]["import_fan_in"] == 1, "internal import fan-in missing")
    require(by_id["module:a"]["metadata"]["visible_validation_link_count"] == 1, "visible validation link missing")
    require(findings["low_confidence_edge_count"] == 0, "derived edge incorrectly low confidence")
    print("IMPORT_ONLY_FAN_IN_OUT: PASS")
    print("VISIBLE_VALIDATION_LINK_COUNT: PASS")


def _validate_cycles(analysis_module: Any) -> None:
    """Prove SCC semantics, call exclusion, and edge annotation."""
    nodes = [
        _node("module:a"),
        _node("module:b"),
        _node("module:c"),
        _node("module:d"),
    ]
    edges = [
        _edge("imports:a:b", "module:a", "module:b", "imports", "derived"),
        _edge("imports:b:a", "module:b", "module:a", "imports", "derived"),
        _edge("imports:a:c", "module:a", "module:c", "imports", "derived"),
        _edge("imports:c:a", "module:c", "module:a", "imports", "derived"),
        _edge("calls:c:d", "module:c", "module:d", "calls"),
        _edge("calls:d:c", "module:d", "module:c", "calls"),
    ]
    findings = analysis_module.analyze_graph_structure(nodes, edges)
    by_id = {node["id"]: node for node in nodes}
    require(findings["cyclic_component_count"] == 1, "one SCC was not reported as one component")
    require(findings["cyclic_node_count"] == 3, "SCC participant count incorrect")
    require(by_id["module:a"]["metadata"]["in_import_cycle"] is True, "cycle node A not marked")
    require(by_id["module:b"]["metadata"]["in_import_cycle"] is True, "cycle node B not marked")
    require(by_id["module:c"]["metadata"]["in_import_cycle"] is True, "cycle node C not marked")
    require(by_id["module:d"]["metadata"]["in_import_cycle"] is False, "call-only node marked as import cycle")
    cycle_edges = [edge for edge in edges if edge["metadata"].get("in_import_cycle")]
    require(len(cycle_edges) == 4, "cycle import edge annotation incorrect")
    require(all(edge["relationship"] == "imports" for edge in cycle_edges), "non-import edge marked as cycle")
    print("IMPORT_SCC_DETECTION: PASS")
    print("CALL_ONLY_CYCLE_EXCLUDED: PASS")
    print("IMPORT_CYCLE_EDGE_ANNOTATION: PASS")


def _validate_determinism_and_bounds(analysis_module: Any) -> None:
    """Prove stable ordering and bounded summary output."""
    nodes = [_node("module:source")]
    edges: list[dict[str, Any]] = []
    for index in range(15):
        node_id = f"module:target_{index:02d}"
        nodes.append(_node(node_id))
        edges.append(
            _edge(
                f"imports:source:{index:02d}",
                "module:source",
                node_id,
                "imports",
                "inferred" if index == 0 else "derived",
            )
        )
    nodes_a = deepcopy(nodes)
    edges_a = deepcopy(edges)
    nodes_b = deepcopy(nodes)
    edges_b = deepcopy(edges)
    result_a = analysis_module.analyze_graph_structure(nodes_a, edges_a)
    result_b = analysis_module.analyze_graph_structure(nodes_b, edges_b)
    require(result_a == result_b, "analysis result is not deterministic")
    require(nodes_a == nodes_b and edges_a == edges_b, "annotations are not deterministic")
    require(len(result_a["top_import_fan_in_nodes"]) == 10, "top list is not bounded")
    require(result_a["top_import_fan_in_truncated"] is True, "top-list truncation not reported")
    require(result_a["low_confidence_edge_count"] == 1, "low-confidence count incorrect")
    require(result_a["scope"] == "rendered_snapshot_only", "scope warning missing")
    require(result_a["whole_project_completeness_claimed"] is False, "whole-project claim leaked")
    require(result_a["quality_score"] is None, "single quality score was introduced")
    print("STRUCTURE_FINDINGS_DETERMINISTIC: PASS")
    print("STRUCTURE_FINDINGS_BOUNDED: PASS")
    print("RENDERED_SNAPSHOT_SCOPE_EXPLICIT: PASS")
    print("NO_SINGLE_QUALITY_SCORE: PASS")


def _validate_source_integration(root: Path) -> None:
    """Validate integration points and preserved visual category semantics."""
    builder = (root / "kanda_reasoner_app/project_structure_visualizer/graph_snapshot_builder.py").read_text(encoding="utf-8")
    fixture = (root / "kanda_reasoner_app/project_structure_visualizer/fixture_graph.py").read_text(encoding="utf-8")
    filters = (root / "kanda_reasoner_app/project_structure_visualizer/graph_view_filters.py").read_text(encoding="utf-8")
    presenter = (root / "kanda_reasoner_app/project_structure_visualizer/details_presenter.py").read_text(encoding="utf-8")
    painter = (root / "kanda_reasoner_app/project_structure_visualizer/web/graph_painter.js").read_text(encoding="utf-8")
    browser = (root / "kanda_reasoner_app/project_structure_visualizer/web/browser_details.js").read_text(encoding="utf-8")

    for source_name, text in (("builder", builder), ("fixture", fixture), ("filters", filters)):
        require("analyze_graph_structure" in text, source_name + " analysis integration missing")
        require('"structure_findings"' in text, source_name + " statistics integration missing")
    require('"structure_findings": structure_findings' not in fixture.split('"generated_at"', 1)[0], "fixture project identity polluted")
    require("rendered snapshot" in presenter.lower(), "embedded scope warning missing")
    require("Import fan-in" in presenter, "embedded import metric rows missing")
    require("return nodePalette[node.category]" in painter, "category node colors were replaced")
    require("import_fan_in_percentile" in painter, "fan-in node sizing missing")
    require("metadata(link).in_import_cycle" in painter, "cycle edge encoding missing")
    require("riskPalette" not in painter and "risk_level" not in painter, "generic risk color authority introduced")
    require("Structural findings" in browser, "standalone findings overview missing")
    require("whole-project completeness" in browser, "standalone scope warning missing")
    print("SNAPSHOT_BUILDER_INTEGRATION: PASS")
    print("FIXTURE_AND_FILTER_INTEGRATION: PASS")
    print("CATEGORY_COLOR_SEMANTICS_PRESERVED: PASS")
    print("IMPORT_CYCLE_EDGE_VISUAL_ENCODING: PASS")
    print("EMBEDDED_AND_BROWSER_DETAILS: PASS")


def _validate_python_quality(root: Path) -> None:
    """Compile changed Python and enforce the current module-size gate."""
    for relative in CHANGED_PYTHON:
        path = root / relative
        require(path.is_file(), "missing changed Python file: " + relative)
        py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(line_count <= 500, f"module exceeds 500 lines: {relative}: {line_count}")
    print("CHANGED_PYTHON_COMPILE: PASS")
    print("TOUCHED_PYTHON_MODULE_SIZE_MAX_500: PASS")


def main() -> int:
    """Run focused deterministic validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    require(root.is_dir(), "project root missing")
    analysis_module = _load_analysis(root)
    _validate_import_semantics(analysis_module)
    _validate_cycles(analysis_module)
    _validate_determinism_and_bounds(analysis_module)
    _validate_source_integration(root)
    _validate_python_quality(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
