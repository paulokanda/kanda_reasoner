# project-path: kanda_reasoner_app/project_structure_visualizer/details_presenter.py
"""Escaped HTML presenters for Project Structure 3D details."""

from __future__ import annotations

import html
from typing import Any

from .graph_snapshot_builder import GraphSnapshotBuild

__all__ = ["node_details_html", "overview_details_html"]


def overview_details_html(build: GraphSnapshotBuild) -> str:
    """Return an overview describing current evidence and limitations."""
    statistics = build.snapshot.get("statistics", {})
    if build.is_fixture:
        source_text = (
            "The canonical complete JSON was unavailable, so the deterministic "
            "fixture is displayed. " + html.escape(build.fallback_reason)
        )
    else:
        source_text = (
            "This graph consumes project-specific KANDA evidence from Project Support: "
            "<code>" + html.escape(build.source_label) + "</code>."
        )
    semantic_summary = (
        html.escape(str(statistics.get("class_count", 0)))
        + " classes, "
        + html.escape(str(statistics.get("function_count", 0)))
        + " important functions, "
        + html.escape(str(statistics.get("call_edge_count", 0)))
        + " calls, and "
        + html.escape(str(statistics.get("inheritance_edge_count", 0)))
        + " inheritance links."
    )
    return (
        "<h2>Project Structure 3D</h2>"
        "<p><b>v1D stable layout and focus-path view</b></p>"
        "<p>" + source_text + "</p>"
        "<p>Packages, modules, selected symbols, imports, calls, inheritance, "
        "validator coverage, and existing Freeze protection are displayed "
        "without rescanning or modifying the Project.</p>"
        "<p><b>Current graph:</b> "
        + html.escape(str(statistics.get("node_count", 0)))
        + " nodes and "
        + html.escape(str(statistics.get("edge_count", 0)))
        + " edges.</p><p><b>Semantic evidence:</b> "
        + semantic_summary
        + "</p><p><b>Layout cache:</b> "
        + html.escape(str(build.snapshot.get("layout", {}).get(
            "position_cache", {}
        ).get("status", "disabled")))
        + " under Project Support.</p><p>Select a node to inspect its evidence-backed metadata. "
        "Project source remains authoritative; Project Support evidence is read-only visualization input.</p>"
    )


def _metadata_text(metadata: dict[str, Any], key: str, fallback: str) -> str:
    """Return compact display text for scalar or list metadata."""
    value = metadata.get(key)
    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(cleaned[:8]) if cleaned else fallback
    text = str(value or "").strip()
    return text or fallback


def node_details_html(
    node: dict[str, Any],
    build: GraphSnapshotBuild,
) -> str:
    """Return escaped details for one current-snapshot node."""
    statuses = [
        label
        for condition, label in (
            (bool(node.get("frozen")), "Frozen"),
            (bool(node.get("protected")), "Protected"),
            (bool(node.get("external")), "External"),
        )
        if condition
    ]
    status_text = ", ".join(statuses) if statuses else "Normal"
    metadata = node.get("metadata") if isinstance(node.get("metadata"), dict) else {}
    rows = [
        ("Type", node.get("kind", "")),
        ("Qualified name", node.get("qualified_name", "") or "Not applicable"),
        ("Category", node.get("category", "")),
        ("Semantic zone", _metadata_text(metadata, "semantic_zone", "core")),
        ("Relative path", node.get("relative_path", "") or "Not applicable"),
        ("Package", node.get("package", "") or "Not applicable"),
        ("Parent", node.get("parent_id", "") or "Not applicable"),
        ("Incoming", node.get("incoming_count", 0)),
        ("Outgoing", node.get("outgoing_count", 0)),
        ("Line", metadata.get("line", "Not available")),
        ("Lines", metadata.get("line_count", "Not available")),
        ("Symbols", metadata.get("symbol_count", "Not available")),
        ("Bases", _metadata_text(metadata, "bases", "Not applicable")),
        ("Linked tests", _metadata_text(metadata, "linked_tests", "Not available")),
        ("Freeze IDs", _metadata_text(metadata, "freeze_ids", "Not applicable")),
        ("Status", status_text),
    ]
    table = "".join(
        "<tr><td style='color:#819ab3;padding:4px 10px 4px 0'>"
        + html.escape(str(label))
        + "</td><td>"
        + html.escape(str(value))
        + "</td></tr>"
        for label, value in rows
    )
    provenance = "Fixture fallback" if build.is_fixture else build.source_label
    return (
        "<h2>" + html.escape(str(node.get("label", ""))) + "</h2>"
        "<table>" + table + "</table>"
        "<p>" + html.escape(str(node.get("summary", ""))) + "</p>"
        "<hr><p style='color:#819ab3'>Source provenance: "
        + html.escape(provenance)
        + ". Project source remains authoritative; Project Support evidence is read-only visualization input.</p>"
    )
