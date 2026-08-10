# project-path: kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py
"""Immutable deterministic relational graph contracts for Shadow diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

__all__ = [
    "RELATIONAL_EDGE_KINDS",
    "RELATIONAL_NODE_KINDS",
    "DiagnosticRelationEdge",
    "DiagnosticRelationNode",
    "DiagnosticRelationalGraph",
]

RELATIONAL_NODE_KINDS = frozenset(
    {"file", "symbol", "public_surface", "facade", "implementation_owner", "export"}
)
RELATIONAL_EDGE_KINDS = frozenset(
    {"duplicate_of", "reexports", "facade_of", "implements", "unbound_export"}
)


def _required(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(field_name + " is required.")
    return text


def _mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise ValueError("attributes/evidence must be a mapping.")
    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class DiagnosticRelationNode:
    """One deterministic node in a Shadow relational graph."""

    node_id: str
    kind: str
    label: str
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "node_id", _required(self.node_id, "node_id"))
        kind = _required(self.kind, "node kind").lower()
        if kind not in RELATIONAL_NODE_KINDS:
            raise ValueError("Unsupported relational node kind: " + kind)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "label", _required(self.label, "node label"))
        object.__setattr__(self, "attributes", _mapping(self.attributes))


@dataclass(frozen=True, slots=True)
class DiagnosticRelationEdge:
    """One deterministic evidence-backed edge in a Shadow relational graph."""

    edge_id: str
    kind: str
    source_node_id: str
    target_node_id: str
    supporting_issue_fingerprints: tuple[str, ...]
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "edge_id", _required(self.edge_id, "edge_id"))
        kind = _required(self.kind, "edge kind").lower()
        if kind not in RELATIONAL_EDGE_KINDS:
            raise ValueError("Unsupported relational edge kind: " + kind)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(
            self, "source_node_id", _required(self.source_node_id, "source_node_id")
        )
        object.__setattr__(
            self, "target_node_id", _required(self.target_node_id, "target_node_id")
        )
        supports = tuple(
            sorted(
                {
                    str(value).strip()
                    for value in self.supporting_issue_fingerprints
                    if str(value).strip()
                }
            )
        )
        if not supports:
            raise ValueError("Relational edges require deterministic issue evidence.")
        object.__setattr__(self, "supporting_issue_fingerprints", supports)
        object.__setattr__(self, "evidence", _mapping(self.evidence))
        if self.evidence.get("deterministic") is not True:
            raise ValueError("Relational edges must declare deterministic evidence.")


@dataclass(frozen=True, slots=True)
class DiagnosticRelationalGraph:
    """One immutable Shadow relation graph derived from a completed run."""

    project_id: str
    producer_id: str
    scope_fingerprint: str
    nodes: tuple[DiagnosticRelationNode, ...]
    edges: tuple[DiagnosticRelationEdge, ...]

    def __post_init__(self) -> None:
        for field_name in ("project_id", "producer_id", "scope_fingerprint"):
            object.__setattr__(self, field_name, _required(getattr(self, field_name), field_name))
        nodes = tuple(self.nodes)
        edges = tuple(self.edges)
        node_ids = {node.node_id for node in nodes}
        if len(node_ids) != len(nodes):
            raise ValueError("Relational node IDs must be unique.")
        edge_ids = {edge.edge_id for edge in edges}
        if len(edge_ids) != len(edges):
            raise ValueError("Relational edge IDs must be unique.")
        for edge in edges:
            if edge.source_node_id not in node_ids or edge.target_node_id not in node_ids:
                raise ValueError("Relational edge references an unknown node.")
        object.__setattr__(self, "nodes", nodes)
        object.__setattr__(self, "edges", edges)
