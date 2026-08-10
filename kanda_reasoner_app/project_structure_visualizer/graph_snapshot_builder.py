# project-path: kanda_reasoner_app/project_structure_visualizer/graph_snapshot_builder.py
"""Build read-only Project Structure 3D snapshots from canonical evidence."""

from __future__ import annotations

import math
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_symbol_atlas.complete_json_adapter import (
    load_reasoner_symbol_atlas_complete_json,
)
from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
    is_active_atlas_path,
)

from .complete_json_zip_cache import resolve_complete_json_evidence
from .fixture_graph import build_fixture_graph
from .graph_schema import validate_graph_snapshot
from .graph_structure_analysis import analyze_graph_structure
from .graph_semantic_enrichment import enrich_graph_semantics
from .graph_snapshot_primitives import (
    apply_relationship_counts,
    category_for_path,
    external_name,
    make_edge,
    make_node,
    module_kind,
    module_name_from_path,
    module_position,
    normalize_relative_path,
    package_path,
    package_position,
    resolve_internal_target,
)

__all__ = ["GraphSnapshotBuild", "build_project_graph_snapshot"]

_MAX_MODULES = 450
_MAX_IMPORT_EDGES = 2400
_MAX_EXTERNAL_DEPENDENCIES = 60


@dataclass(frozen=True)
class GraphSnapshotBuild:
    """One immutable graph snapshot and its evidence status."""

    snapshot: dict[str, Any]
    source_status: str
    source_label: str
    fallback_reason: str = ""

    @property
    def is_fixture(self) -> bool:
        """Return whether the build uses the deterministic fallback fixture."""
        return bool(self.snapshot.get("statistics", {}).get("fixture"))


def _source_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Return bounded active source records from complete JSON."""
    source_index = payload.get("source_file_index")
    if not isinstance(source_index, dict):
        return []
    records: list[dict[str, Any]] = []
    for key in sorted(source_index):
        item = source_index.get(key)
        if not isinstance(item, dict):
            continue
        relative_path = normalize_relative_path(item.get("file") or key)
        if not relative_path or not relative_path.endswith(".py"):
            continue
        if not is_active_atlas_path(relative_path):
            continue
        records.append(
            {
                "relative_path": relative_path,
                "module_name": str(
                    item.get("module_name") or module_name_from_path(relative_path)
                ).strip(),
                "line_count": _safe_int(item.get("line_count")),
                "symbol_count": _safe_int(item.get("symbol_count")),
            }
        )
        if len(records) >= _MAX_MODULES:
            break
    return records


def _safe_int(value: object) -> int:
    """Return one non-negative integer without leaking conversion errors."""
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _responsibility_summary(payload: dict[str, Any], relative_path: str) -> str:
    """Read an optional responsibility description without inventing one."""
    index = payload.get("web_ai_file_responsibility_index")
    if isinstance(index, dict):
        item = index.get(relative_path)
        if isinstance(item, dict):
            responsibility = str(item.get("primary_responsibility") or "").strip()
            if responsibility:
                return responsibility
    semantic = payload.get("semantic_roles")
    if isinstance(semantic, dict):
        item = semantic.get(relative_path)
        if isinstance(item, dict):
            for key in ("summary", "responsibility", "role"):
                text = str(item.get(key) or "").strip()
                if text:
                    return text
    return "Project module from canonical complete JSON evidence."


def _create_structure_nodes(
    project_root: Path,
    payload: dict[str, Any],
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, str], list[str]]:
    """Create project, package, module, and containment records."""
    project_slug = project_root.name
    project_id = "project:" + project_slug
    package_records: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        package_records.setdefault(package_path(record["relative_path"]), []).append(record)

    nodes: list[dict[str, Any]] = [
        make_node(
            project_id,
            project_slug.replace("_", " ").title(),
            "project",
            "core",
            (0.0, 0.0, 0.0),
            summary="Selected Project represented from canonical complete JSON evidence.",
            metadata={"source": "complete_json", "fixture": False},
        )
    ]
    edges: list[dict[str, Any]] = []
    module_to_node: dict[str, str] = {}
    package_names = sorted(package_records)

    for package_index, package_name in enumerate(package_names):
        package_id = "package:" + package_name
        center = package_position(package_index, len(package_names))
        modules = package_records[package_name]
        nodes.append(
            make_node(
                package_id,
                package_name,
                "package",
                category_for_path(package_name),
                center,
                relative_path=package_name,
                package=package_name,
                parent_id=project_id,
                summary=f"Contains {len(modules)} visualized modules.",
                size_metric=len(modules),
                metadata={"source": "source_file_index", "fixture": False},
            )
        )
        edges.append(
            make_edge(
                "contains:" + project_id + ":" + package_id,
                project_id,
                package_id,
                "contains",
                evidence="source_file_index",
            )
        )
        for module_index, record in enumerate(modules):
            relative_path = record["relative_path"]
            node_id = "module:" + relative_path
            module_name = record["module_name"] or module_name_from_path(relative_path)
            module_to_node[module_name] = node_id
            module_to_node[module_name_from_path(relative_path)] = node_id
            nodes.append(
                make_node(
                    node_id,
                    PurePosixPath(relative_path).name,
                    module_kind(relative_path),
                    category_for_path(relative_path),
                    module_position(center, module_index, len(modules)),
                    relative_path=relative_path,
                    package=package_name,
                    parent_id=package_id,
                    summary=_responsibility_summary(payload, relative_path),
                    size_metric=record["line_count"],
                    metadata={
                        "source": "source_file_index",
                        "module_name": module_name,
                        "line_count": record["line_count"],
                        "symbol_count": record["symbol_count"],
                        "fixture": False,
                    },
                )
            )
            edges.append(
                make_edge(
                    "contains:" + package_id + ":" + node_id,
                    package_id,
                    node_id,
                    "contains",
                    evidence="source_file_index",
                )
            )
    return nodes, edges, module_to_node, package_names


def _collect_imports(
    payload: dict[str, Any],
    module_to_node: dict[str, str],
) -> tuple[list[tuple[str, str, str]], Counter[str]]:
    """Collect internal import edges and external dependency frequencies."""
    import_graph = payload.get("import_graph")
    if not isinstance(import_graph, dict):
        return [], Counter()
    internal: list[tuple[str, str, str]] = []
    external_counts: Counter[str] = Counter()
    for source_module in sorted(import_graph):
        source_id = resolve_internal_target(source_module, module_to_node)
        targets = import_graph.get(source_module)
        if not source_id or not isinstance(targets, list):
            continue
        for raw_target in targets:
            target_text = str(raw_target or "").strip()
            target_id = resolve_internal_target(target_text, module_to_node)
            if target_id and target_id != source_id:
                internal.append((source_id, target_id, target_text))
                continue
            external = external_name(target_text)
            if external and external not in sys.stdlib_module_names:
                external_counts[external] += 1
    return internal, external_counts


def _add_external_nodes(
    nodes: list[dict[str, Any]],
    external_counts: Counter[str],
) -> set[str]:
    """Add bounded high-frequency external dependencies."""
    allowed = {
        name for name, _count in external_counts.most_common(_MAX_EXTERNAL_DEPENDENCIES)
    }
    for index, external in enumerate(sorted(allowed)):
        angle = (2.0 * math.pi * index) / max(1, len(allowed))
        position = (610.0 * math.cos(angle), 610.0 * math.sin(angle), 180.0)
        nodes.append(
            make_node(
                "external:" + external,
                external,
                "external",
                "external",
                position,
                summary="External dependency referenced by canonical import evidence.",
                size_metric=external_counts[external],
                metadata={"source": "import_graph", "fixture": False},
                external=True,
            )
        )
    return allowed


def _add_import_edges(
    edges: list[dict[str, Any]],
    internal_imports: list[tuple[str, str, str]],
    payload: dict[str, Any],
    module_to_node: dict[str, str],
    external_allowed: set[str],
) -> None:
    """Add deduplicated internal and external import relationships."""
    seen: set[tuple[str, str]] = set()
    for source_id, target_id, target_text in internal_imports:
        if len(seen) >= _MAX_IMPORT_EDGES:
            break
        key = (source_id, target_id)
        if key in seen:
            continue
        seen.add(key)
        edges.append(
            make_edge(
                "imports:" + source_id + ":" + target_id,
                source_id,
                target_id,
                "imports",
                evidence="import_graph: " + target_text,
                confidence="derived",
            )
        )

    import_graph = payload.get("import_graph")
    if not isinstance(import_graph, dict):
        return
    for source_module in sorted(import_graph):
        source_id = resolve_internal_target(source_module, module_to_node)
        targets = import_graph.get(source_module)
        if not source_id or not isinstance(targets, list):
            continue
        for raw_target in targets:
            if len(seen) >= _MAX_IMPORT_EDGES:
                return
            target_text = str(raw_target or "").strip()
            external = external_name(target_text)
            if external not in external_allowed:
                continue
            target_id = "external:" + external
            key = (source_id, target_id)
            if key in seen:
                continue
            seen.add(key)
            edges.append(
                make_edge(
                    "imports:" + source_id + ":" + target_id,
                    source_id,
                    target_id,
                    "imports",
                    evidence="import_graph: " + target_text,
                    confidence="derived",
                )
            )


def _build_from_complete_json(
    project_root: Path,
    json_path: Path,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Build a package/module/import snapshot from existing complete JSON."""
    records = _source_records(payload)
    if not records:
        raise ValueError("complete JSON contains no active Python source records")
    nodes, edges, module_to_node, package_names = _create_structure_nodes(
        project_root,
        payload,
        records,
    )
    internal_imports, external_counts = _collect_imports(payload, module_to_node)
    external_allowed = _add_external_nodes(nodes, external_counts)
    _add_import_edges(edges, internal_imports, payload, module_to_node, external_allowed)
    semantic_statistics = enrich_graph_semantics(
        project_root,
        payload,
        nodes,
        edges,
    )
    apply_relationship_counts(nodes, edges)
    structure_findings = analyze_graph_structure(nodes, edges)
    module_count = sum(node["kind"] in {"module", "validator"} for node in nodes)
    snapshot: dict[str, Any] = {
        "schema_version": "1.0",
        "project_identity": {
            "slug": project_root.name,
            "display_name": project_root.name.replace("_", " ").title(),
            "fixture": False,
        },
        "generated_at": "complete-json-runtime",
        "source_provenance": {
            "kind": "complete_json",
            "authoritative": False,
            "authority_scope": "read_only_visualization_input",
            "project_source_authority": "selected_project_source",
            "support_owner": "project_support.project_structure_3d_json",
            "filename": json_path.name,
            "notice": (
                "Project source remains authoritative; this graph is derived "
                "from project-specific KANDA evidence in Project Support."
            ),
            "semantic_sources": [
                "files",
                "call_edges",
                "web_ai_test_protection_index",
                "freeze_after_update.frozen_features_memory",
            ],
        },
        "nodes": nodes,
        "edges": edges,
        "clusters": package_names + (["external"] if external_allowed else []),
        "legend": {
            "categories": ["core", "gui", "ai", "validation", "evidence", "external"],
            "relationships": [
                "contains",
                "imports",
                "calls",
                "inherits",
                "validates",
                "protects",
            ],
        },
        "layout": {
            "engine": "deterministic_evidence_layout_v1c",
            "stable": True,
            "coordinates_are_authoritative": False,
        },
        "statistics": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "package_count": len(package_names),
            "module_count": module_count,
            "external_dependency_count": len(external_allowed),
            "fixture": False,
            "source_file_count_available": len(records),
            "source_file_limit": _MAX_MODULES,
            "structure_findings": structure_findings,
            **semantic_statistics,
        },
    }
    validate_graph_snapshot(snapshot)
    return snapshot


def _fixture_fallback(root: Path, reason: str) -> GraphSnapshotBuild:
    """Return the v1A fixture with an explicit evidence failure reason."""
    snapshot = build_fixture_graph(root)
    snapshot["source_provenance"]["fallback_reason"] = reason
    return GraphSnapshotBuild(
        snapshot=snapshot,
        source_status="fixture_fallback",
        source_label="Fixture fallback",
        fallback_reason=reason,
    )


def build_project_graph_snapshot(project_root: Path | str) -> GraphSnapshotBuild:
    """Build from verified Project Support complete JSON or fixture fallback."""
    root = Path(project_root).expanduser().resolve()
    support_root = project_analysis_evidence_root(root).resolve(strict=False)
    try:
        selected, source_kind, cache_status = resolve_complete_json_evidence(root)
    except (OSError, ValueError, TypeError) as exc:
        return _fixture_fallback(
            root,
            "Project Support complete JSON ZIP evidence was unusable: " + str(exc),
        )
    if selected is None:
        return _fixture_fallback(
            root,
            "No complete JSON ZIP family or legacy loose evidence file was "
            "found in Project Support.",
        )
    try:
        selected.resolve(strict=False).relative_to(support_root)
        payload = load_reasoner_symbol_atlas_complete_json(selected)
        snapshot = _build_from_complete_json(root, selected, payload)
    except (OSError, ValueError, TypeError) as exc:
        return _fixture_fallback(
            root,
            "Project Support evidence was unusable: " + str(exc),
        )
    return GraphSnapshotBuild(
        snapshot=snapshot,
        source_status="complete_json_ready",
        source_label=source_kind + " (" + cache_status + ")",
    )
