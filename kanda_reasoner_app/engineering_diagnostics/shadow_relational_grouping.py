# project-path: kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py
"""Deterministic Shadow relational graph and connected-component grouping."""

from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from .collectors.shadow_collector import SHADOW_PRODUCER_ID
from .fingerprinting import canonical_json, normalize_relative_path
from .grouping_models import DiagnosticGroupRecord
from .models import DiagnosticFindingRecord, DiagnosticRunRecord
from .shadow_relational_models import (
    DiagnosticRelationEdge,
    DiagnosticRelationNode,
    DiagnosticRelationalGraph,
)

__all__ = [
    "build_shadow_relational_diagnostic_groups",
    "build_shadow_relational_graph",
]


def _digest(label: str, payload: object) -> str:
    return hashlib.sha256((label + "|" + canonical_json(payload)).encode("utf-8")).hexdigest()


def _node_id(kind: str, label: str) -> str:
    return _digest("engineering-diagnostics-shadow-node-v1", {"kind": kind, "label": label})


def _edge_id(kind: str, source: str, target: str, evidence: Mapping[str, Any]) -> str:
    return _digest(
        "engineering-diagnostics-shadow-edge-v1",
        {"kind": kind, "source": source, "target": target, "evidence": evidence},
    )


def _tuple_text(value: object) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple, set, frozenset)):
        return ()
    return tuple(sorted({str(item).strip().replace("\\", "/") for item in value if str(item).strip()}))


class _GraphBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, DiagnosticRelationNode] = {}
        self._edge_rows: dict[tuple[str, str, str, str], dict[str, Any]] = {}

    def node(self, kind: str, label: str, **attributes: Any) -> str:
        identity = _node_id(kind, label)
        self.nodes.setdefault(
            identity,
            DiagnosticRelationNode(identity, kind, label, MappingProxyType(dict(attributes))),
        )
        return identity

    def edge(
        self,
        kind: str,
        source: str,
        target: str,
        issue_fingerprint: str,
        **evidence: Any,
    ) -> None:
        payload = {"deterministic": True, "source_contract": "shadow_audit.v1"}
        payload.update(evidence)
        evidence_key = canonical_json(payload)
        key = (kind, source, target, evidence_key)
        row = self._edge_rows.setdefault(
            key,
            {"evidence": payload, "supports": set()},
        )
        supports = row["supports"]
        if not isinstance(supports, set):
            raise RuntimeError("SHADOW_RELATIONAL_SUPPORT_SET_INVALID")
        supports.add(issue_fingerprint)

    def finalized_edges(self) -> tuple[DiagnosticRelationEdge, ...]:
        values: list[DiagnosticRelationEdge] = []
        for (kind, source, target, _evidence_key), row in self._edge_rows.items():
            evidence = dict(row["evidence"])
            supports = tuple(sorted(row["supports"]))
            values.append(
                DiagnosticRelationEdge(
                    _edge_id(kind, source, target, evidence),
                    kind,
                    source,
                    target,
                    supports,
                    MappingProxyType(evidence),
                )
            )
        return tuple(
            sorted(
                values,
                key=lambda item: (
                    item.kind,
                    item.source_node_id,
                    item.target_node_id,
                    item.edge_id,
                ),
            )
        )


def _file_node(builder: _GraphBuilder, relative_path: str) -> str:
    path = normalize_relative_path(relative_path)
    return builder.node("file", path, relative_path=path)


def _facade_node(builder: _GraphBuilder, relative_path: str) -> str:
    path = normalize_relative_path(relative_path)
    return builder.node("facade", path, relative_path=path)


def _add_facade_role(builder: _GraphBuilder, finding: DiagnosticFindingRecord) -> tuple[str, str]:
    file_node = _file_node(builder, finding.relative_path)
    facade_node = _facade_node(builder, finding.relative_path)
    builder.edge(
        "facade_of",
        facade_node,
        file_node,
        finding.issue_fingerprint,
        relative_path=finding.relative_path,
    )
    return file_node, facade_node


def _add_duplicate_symbol(builder: _GraphBuilder, finding: DiagnosticFindingRecord) -> None:
    symbol = str(finding.evidence.get("symbol") or finding.symbol_id or "").strip()
    owners = _tuple_text(finding.evidence.get("owners"))
    if not symbol or len(owners) < 2:
        return
    symbol_node = builder.node("symbol", symbol, symbol=symbol)
    surface_node = builder.node("public_surface", "public:" + symbol, symbol=symbol)
    builder.edge("implements", surface_node, symbol_node, finding.issue_fingerprint, symbol=symbol)
    owner_nodes: list[str] = []
    for owner in owners:
        owner_node = builder.node("implementation_owner", owner, owner=owner)
        file_node = _file_node(builder, owner)
        builder.edge("implements", owner_node, symbol_node, finding.issue_fingerprint, owner=owner, symbol=symbol)
        builder.edge("implements", file_node, owner_node, finding.issue_fingerprint, owner=owner)
        if PurePosixPath(owner).name == "__init__.py":
            facade_node = _facade_node(builder, owner)
            builder.edge("reexports", facade_node, surface_node, finding.issue_fingerprint, symbol=symbol)
        owner_nodes.append(owner_node)
    anchor = owner_nodes[0]
    for other in owner_nodes[1:]:
        builder.edge("duplicate_of", other, anchor, finding.issue_fingerprint, symbol=symbol)


def _add_unbound_export(builder: _GraphBuilder, finding: DiagnosticFindingRecord) -> None:
    exported = str(finding.evidence.get("exported_name") or finding.symbol_id or "").strip()
    if not exported:
        return
    _file, facade = _add_facade_role(builder, finding)
    export = builder.node(
        "export",
        finding.relative_path + "::__all__::" + exported,
        exported_name=exported,
        relative_path=finding.relative_path,
    )
    symbol = builder.node("symbol", exported, symbol=exported)
    builder.edge("unbound_export", facade, export, finding.issue_fingerprint, exported_name=exported)
    builder.edge("reexports", export, symbol, finding.issue_fingerprint, exported_name=exported)


def _add_facade_behavior(builder: _GraphBuilder, finding: DiagnosticFindingRecord) -> None:
    _file, facade = _add_facade_role(builder, finding)
    symbol = str(finding.evidence.get("symbol") or finding.symbol_id or "").strip()
    if not symbol:
        return
    symbol_node = builder.node("symbol", symbol, symbol=symbol)
    surface = builder.node(
        "public_surface",
        finding.relative_path + "::" + symbol,
        relative_path=finding.relative_path,
        symbol=symbol,
    )
    builder.edge("implements", facade, symbol_node, finding.issue_fingerprint, symbol=symbol)
    builder.edge("facade_of", facade, surface, finding.issue_fingerprint, symbol=symbol)


def _add_facade_surface(builder: _GraphBuilder, finding: DiagnosticFindingRecord) -> None:
    _file, facade = _add_facade_role(builder, finding)
    surface = builder.node(
        "public_surface",
        finding.relative_path + "::__all__",
        relative_path=finding.relative_path,
    )
    builder.edge("reexports", facade, surface, finding.issue_fingerprint, code=finding.code)


def build_shadow_relational_graph(
    run: DiagnosticRunRecord,
    findings: tuple[DiagnosticFindingRecord, ...],
) -> DiagnosticRelationalGraph:
    """Build a deterministic graph using only copied Shadow evidence."""
    if run.producer_id != SHADOW_PRODUCER_ID:
        raise ValueError("SHADOW_RELATIONAL_RUN_PRODUCER_MISMATCH")
    builder = _GraphBuilder()
    for finding in findings:
        if finding.run_id != run.run_id:
            raise ValueError("SHADOW_RELATIONAL_FINDING_RUN_MISMATCH")
        if finding.code == "DUPLICATE_PUBLIC_SYMBOL":
            _add_duplicate_symbol(builder, finding)
        elif finding.code == "UNBOUND_ALL_EXPORT":
            _add_unbound_export(builder, finding)
        elif finding.code == "BEHAVIOR_DEFINED_IN_FACADE":
            _add_facade_behavior(builder, finding)
        elif finding.code in {
            "RUNTIME_LOGIC_IN_FACADE",
            "FACADE_WITHOUT_ALL",
            "WILDCARD_IMPORT_IN_FACADE",
            "DYNAMIC_ALL_EXPORT",
        }:
            _add_facade_surface(builder, finding)
    return DiagnosticRelationalGraph(
        project_id=run.project_id,
        producer_id=run.producer_id,
        scope_fingerprint=run.scope_fingerprint,
        nodes=tuple(sorted(builder.nodes.values(), key=lambda item: (item.kind, item.label, item.node_id))),
        edges=builder.finalized_edges(),
    )


def _components(graph: DiagnosticRelationalGraph) -> tuple[tuple[str, ...], ...]:
    adjacency: dict[str, set[str]] = {node.node_id: set() for node in graph.nodes}
    for edge in graph.edges:
        adjacency[edge.source_node_id].add(edge.target_node_id)
        adjacency[edge.target_node_id].add(edge.source_node_id)
    visited: set[str] = set()
    components: list[tuple[str, ...]] = []
    for node_id in sorted(adjacency):
        if node_id in visited:
            continue
        stack = [node_id]
        member_ids: list[str] = []
        visited.add(node_id)
        while stack:
            current = stack.pop()
            member_ids.append(current)
            for neighbor in sorted(adjacency[current], reverse=True):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        components.append(tuple(sorted(member_ids)))
    return tuple(components)


_CANONICAL_JSON_SEQUENCE_LIMIT = 10000
_LARGE_COMPONENT_SAMPLE_SIZE = 32


def _ordered_id_stream_digest(label: str, values: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    digest.update(label.encode("ascii", errors="strict"))
    digest.update(b"\0")
    for value in values:
        encoded = str(value).encode("ascii", errors="strict")
        digest.update(str(len(encoded)).encode("ascii"))
        digest.update(b":")
        digest.update(encoded)
        digest.update(b"\n")
    return digest.hexdigest()


def _group_id(run: DiagnosticRunRecord, node_ids: tuple[str, ...]) -> str:
    if len(node_ids) <= _CANONICAL_JSON_SEQUENCE_LIMIT:
        payload: dict[str, object] = {
            "project_id": run.project_id,
            "producer_id": run.producer_id,
            "scope_fingerprint": run.scope_fingerprint,
            "producer_version": run.producer_version,
            "configuration_fingerprint": run.configuration_fingerprint,
            "node_ids": node_ids,
        }
    else:
        payload = {
            "project_id": run.project_id,
            "producer_id": run.producer_id,
            "scope_fingerprint": run.scope_fingerprint,
            "producer_version": run.producer_version,
            "configuration_fingerprint": run.configuration_fingerprint,
            "large_component_identity_contract": (
                "engineering-diagnostics-shadow-relational-group-stream-v1"
            ),
            "node_count": len(node_ids),
            "node_ids_digest": _ordered_id_stream_digest(
                "engineering-diagnostics-shadow-relational-node-ids-v1",
                node_ids,
            ),
        }
    return _digest(
        "engineering-diagnostics-shadow-relational-group-v1",
        payload,
    )


def _id_sequence_evidence(
    key: str,
    values: tuple[str, ...],
) -> dict[str, object]:
    if len(values) <= _CANONICAL_JSON_SEQUENCE_LIMIT:
        return {key: values}
    return {
        key + "_complete": False,
        key + "_count": len(values),
        key + "_digest": _ordered_id_stream_digest(
            "engineering-diagnostics-shadow-relational-" + key + "-v1",
            values,
        ),
        key + "_digest_contract": (
            "engineering-diagnostics-shadow-relational-ordered-id-stream-v1"
        ),
        key + "_sample_head": values[:_LARGE_COMPONENT_SAMPLE_SIZE],
        key + "_sample_tail": values[-_LARGE_COMPONENT_SAMPLE_SIZE:],
    }


def build_shadow_relational_diagnostic_groups(
    run: DiagnosticRunRecord,
    findings: tuple[DiagnosticFindingRecord, ...],
) -> tuple[DiagnosticGroupRecord, ...]:
    """Convert evidence-complete connected components into Diagnostic groups."""
    graph = build_shadow_relational_graph(run, findings)
    node_map = {node.node_id: node for node in graph.nodes}
    groups: list[DiagnosticGroupRecord] = []
    for component in _components(graph):
        component_set = set(component)
        edges = tuple(
            edge
            for edge in graph.edges
            if edge.source_node_id in component_set and edge.target_node_id in component_set
        )
        if not edges or any(edge.evidence.get("deterministic") is not True for edge in edges):
            continue
        issue_ids = tuple(
            sorted(
                {
                    issue
                    for edge in edges
                    for issue in edge.supporting_issue_fingerprints
                }
            )
        )
        if len(issue_ids) < 2:
            continue
        nodes = tuple(node_map[node_id] for node_id in component)
        confidence = "high"
        finding_confidence = {
            finding.issue_fingerprint: finding.confidence for finding in findings
        }
        if any(finding_confidence.get(issue) != "high" for issue in issue_ids):
            confidence = "medium"
        labels = sorted(
            node.label for node in nodes if node.kind in {"symbol", "facade", "implementation_owner"}
        )
        label = "Shadow relation: " + (", ".join(labels[:3]) or str(len(nodes)) + " nodes")
        groups.append(
            DiagnosticGroupRecord(
                group_id=_group_id(run, component),
                project_id=run.project_id,
                producer_id=run.producer_id,
                scope_fingerprint=run.scope_fingerprint,
                kind="DETERMINISTIC",
                recipe_id="shadow.relational_component.v1",
                label=label,
                confidence=confidence,
                member_issue_fingerprints=issue_ids,
                evidence=MappingProxyType(
                    {
                        "grouping_mode": "deterministic_relational_component",
                        "root_cause_claimed": False,
                        "ai_grouping_used": False,
                        "node_count": len(nodes),
                        "edge_count": len(edges),
                        "node_kinds": tuple(sorted({node.kind for node in nodes})),
                        "edge_kinds": tuple(sorted({edge.kind for edge in edges})),
                        **_id_sequence_evidence("node_ids", component),
                        **_id_sequence_evidence(
                            "edge_ids",
                            tuple(edge.edge_id for edge in edges),
                        ),
                        "all_edges_deterministic": True,
                    }
                ),
            )
        )
    return tuple(sorted(groups, key=lambda group: (group.label, group.group_id)))
