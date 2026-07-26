# project-path: kanda_reasoner_app/project_structure_visualizer/fixture_graph.py
"""Deterministic v1A fixture graph for Project Structure 3D."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from .graph_schema import validate_graph_snapshot

__all__ = ["build_fixture_graph"]


def _node(
    node_id: str,
    label: str,
    kind: str,
    category: str,
    position: tuple[int, int, int],
    *,
    relative_path: str = "",
    summary: str = "",
    frozen: bool = False,
    protected: bool = False,
    external: bool = False,
) -> dict[str, Any]:
    """Create one fixture node with the complete v1 schema."""
    return {
        "id": node_id,
        "label": label,
        "kind": kind,
        "relative_path": relative_path,
        "qualified_name": label,
        "package": relative_path.rpartition("/")[0],
        "parent_id": "",
        "category": category,
        "size_metric": 1,
        "complexity_metric": 0,
        "incoming_count": 0,
        "outgoing_count": 0,
        "frozen": frozen,
        "protected": protected,
        "external": external,
        "risk_level": "none",
        "summary": summary,
        "position": list(position),
        "metadata": {
            "fixture": True,
            "source_confidence": "confirmed",
        },
    }


def _edge(
    edge_id: str,
    source: str,
    target: str,
    relationship: str,
    *,
    confidence: str = "confirmed",
) -> dict[str, Any]:
    """Create one fixture relationship."""
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relationship": relationship,
        "directed": relationship != "contains",
        "weight": 1,
        "label": relationship.replace("_", " "),
        "evidence": "v1A deterministic fixture",
        "validation_status": "fixture_only",
        "confidence": confidence,
        "metadata": {"fixture": True},
    }


def _fixture_nodes() -> list[dict[str, Any]]:
    """Return stable nodes arranged into semantic spatial regions."""
    return [
        _node(
            "project:kanda_reasoner",
            "KANDA Reasoner",
            "project",
            "core",
            (0, 0, 0),
            summary="Selected Project boundary and visualization center.",
        ),
        _node(
            "package:gui",
            "GUI Shell",
            "package",
            "gui",
            (-230, -150, 40),
            relative_path="kanda_reasoner_app/reasoner_tools_gui_shell",
            summary="Owns the visible PySide6 tool tabs and navigation shell.",
        ),
        _node(
            "package:reasoner",
            "Reasoner Engine",
            "package",
            "ai",
            (230, -140, 20),
            relative_path="kanda_reasoner_app/reasoner_engine",
            summary="Owns Local AI and Project Web AI reasoning flows.",
        ),
        _node(
            "package:validation",
            "Validation",
            "package",
            "validation",
            (220, 180, -20),
            relative_path="tools",
            summary="Focused validators and regression protection.",
        ),
        _node(
            "package:evidence",
            "Evidence and Handoff",
            "package",
            "evidence",
            (-220, 170, -30),
            relative_path="kanda_reasoner_app/reasoner_context_collector",
            summary="Builds read-only project evidence and AI handoff artifacts.",
        ),
        _node(
            "module:tool_specs",
            "tool_specs.py",
            "module",
            "gui",
            (-330, -210, 80),
            relative_path="kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
            summary="Canonical visible-tool registry.",
            protected=True,
        ),
        _node(
            "module:main_window",
            "main_window.py",
            "module",
            "gui",
            (-205, -250, -30),
            relative_path="kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
            summary="Hosts lazy tabs and active Project synchronization.",
        ),
        _node(
            "class:reasoner_tools_window",
            "ReasonerToolsWindow",
            "class",
            "gui",
            (-110, -185, 95),
            relative_path="kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
            summary="Main application window and tab container.",
        ),
        _node(
            "module:project_web_ai",
            "project_web_ai_tab.py",
            "module",
            "ai",
            (315, -205, 80),
            relative_path="kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
            summary="Read-only and governed Web AI interface for the selected Project.",
            frozen=True,
        ),
        _node(
            "module:local_ai",
            "ai_reasoner_main_window.py",
            "module",
            "ai",
            (190, -250, -55),
            relative_path="kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py",
            summary="Local project question and evidence interface.",
        ),
        _node(
            "class:project_web_ai_tab",
            "ProjectWebAITab",
            "class",
            "ai",
            (105, -145, 105),
            relative_path="kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
            summary="Public Qt facade for Project Web AI.",
            frozen=True,
        ),
        _node(
            "module:collector_runner",
            "runner.py",
            "module",
            "evidence",
            (-310, 220, 55),
            relative_path="kanda_reasoner_app/reasoner_context_collector/runner.py",
            summary="Creates the external Show Project to AI handoff.",
        ),
        _node(
            "module:live_source",
            "live_source_fallback.py",
            "module",
            "evidence",
            (-145, 245, -65),
            relative_path=(
                "kanda_reasoner_app/reasoner_engine/"
                "reasoner_retriever_help/live_source_fallback.py"
            ),
            summary="Bounded live-source evidence fallback.",
            frozen=True,
        ),
        _node(
            "validator:architecture",
            "Architecture validator",
            "validator",
            "validation",
            (300, 230, 70),
            relative_path="tools/validate_box_architecture.py",
            summary="Checks box ownership and dependency boundaries.",
        ),
        _node(
            "validator:qt_lifecycle",
            "Qt lifecycle validator",
            "validator",
            "validation",
            (145, 255, -70),
            relative_path="tools/validate_architecture_review_ai_signal_lifecycle_recovery_v1.py",
            summary="Protects page-scoped widgets from late global callbacks.",
        ),
        _node(
            "external:qt_webengine",
            "Qt WebEngine",
            "external",
            "external",
            (0, -20, 330),
            summary="External embedded browser and WebChannel runtime.",
            external=True,
        ),
    ]


def _fixture_edges() -> list[dict[str, Any]]:
    """Return stable fixture relationships."""
    edge_specs = (
        ("contains:project:gui", "project:kanda_reasoner", "package:gui", "contains"),
        (
            "contains:project:reasoner",
            "project:kanda_reasoner",
            "package:reasoner",
            "contains",
        ),
        (
            "contains:project:validation",
            "project:kanda_reasoner",
            "package:validation",
            "contains",
        ),
        (
            "contains:project:evidence",
            "project:kanda_reasoner",
            "package:evidence",
            "contains",
        ),
        ("contains:gui:specs", "package:gui", "module:tool_specs", "contains"),
        ("contains:gui:window", "package:gui", "module:main_window", "contains"),
        (
            "contains:window:class",
            "module:main_window",
            "class:reasoner_tools_window",
            "contains",
        ),
        ("imports:window:specs", "module:main_window", "module:tool_specs", "imports"),
        (
            "contains:reasoner:web",
            "package:reasoner",
            "module:project_web_ai",
            "contains",
        ),
        (
            "contains:reasoner:local",
            "package:reasoner",
            "module:local_ai",
            "contains",
        ),
        (
            "contains:web:class",
            "module:project_web_ai",
            "class:project_web_ai_tab",
            "contains",
        ),
        (
            "contains:evidence:collector",
            "package:evidence",
            "module:collector_runner",
            "contains",
        ),
        (
            "contains:evidence:live",
            "package:evidence",
            "module:live_source",
            "contains",
        ),
        (
            "contains:validation:architecture",
            "package:validation",
            "validator:architecture",
            "contains",
        ),
        (
            "contains:validation:lifecycle",
            "package:validation",
            "validator:qt_lifecycle",
            "contains",
        ),
        (
            "validates:architecture:window",
            "validator:architecture",
            "module:main_window",
            "validates",
        ),
        (
            "validates:lifecycle:web",
            "validator:qt_lifecycle",
            "class:project_web_ai_tab",
            "validates",
        ),
        (
            "invokes:window:web",
            "class:reasoner_tools_window",
            "class:project_web_ai_tab",
            "invokes",
        ),
        (
            "depends:web:qt",
            "class:project_web_ai_tab",
            "external:qt_webengine",
            "depends_on",
        ),
        (
            "protects:project:web",
            "project:kanda_reasoner",
            "module:project_web_ai",
            "protects",
        ),
    )
    return [_edge(*spec) for spec in edge_specs]


def _apply_relationship_counts(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> None:
    """Populate deterministic incoming and outgoing counts."""
    by_id = {node["id"]: node for node in nodes}
    for edge in edges:
        by_id[edge["source"]]["outgoing_count"] += 1
        by_id[edge["target"]]["incoming_count"] += 1


def build_fixture_graph(project_root: Path | None = None) -> dict[str, Any]:
    """Build the immutable, renderer-ready v1A fixture snapshot."""
    nodes = _fixture_nodes()
    edges = _fixture_edges()
    _apply_relationship_counts(nodes, edges)
    project_slug = project_root.name if project_root is not None else "kanda_reasoner"
    snapshot: dict[str, Any] = {
        "schema_version": "1.0",
        "project_identity": {
            "slug": project_slug,
            "display_name": project_slug.replace("_", " ").title(),
            "fixture": True,
        },
        "generated_at": "fixture-v1a",
        "source_provenance": {
            "kind": "deterministic_fixture",
            "authoritative": False,
            "notice": "Prototype data only. Existing KANDA analysis remains canonical.",
        },
        "nodes": nodes,
        "edges": edges,
        "clusters": ["gui", "ai", "validation", "evidence", "external"],
        "legend": {
            "categories": ["core", "gui", "ai", "validation", "evidence", "external"],
            "relationships": [
                "contains",
                "imports",
                "invokes",
                "validates",
                "protects",
                "depends_on",
            ],
        },
        "layout": {
            "engine": "deterministic_canvas_3d_v1a",
            "stable": True,
            "coordinates_are_authoritative": False,
        },
        "statistics": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "fixture": True,
        },
    }
    validate_graph_snapshot(snapshot)
    return deepcopy(snapshot)
