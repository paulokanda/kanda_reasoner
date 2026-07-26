# project-path: kanda_reasoner_app/manage_architecture/_large_module_split_audit_analysis.py
"""AST analysis support for the large-module split audit runner."""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any, Iterable

from kanda_reasoner_app.manage_architecture._large_module_split_audit_symbol_analysis import (
    ARCHIVE_NAMES,
    DELETE_METHODS,
    GUI_IMPORT_PREFIXES,
    GUI_NAME_HINTS,
    SUBPROCESS_NAMES,
    WIDGET_ATTR_HINTS,
    WRITE_METHODS,
    _SymbolVisitor,
    _call_name,
    _candidate_label,
    _literal_write_mode,
    _looks_like_widget_attr,
    _risk_for,
    _root_name,
)

__all__: list[str] = []

@dataclass(slots=True)
class _SymbolAudit:
    """AST-derived evidence for one top-level function or class method."""

    kind: str
    name: str
    qualname: str
    line_start: int
    line_end: int
    line_count: int
    called_self_methods: list[str] = field(default_factory=list)
    self_attr_reads: list[str] = field(default_factory=list)
    self_attr_writes: list[str] = field(default_factory=list)
    imports_used: list[str] = field(default_factory=list)
    gui_touches: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    candidate_island: str = "general"
    risk: str = "low"

    def as_dict(self) -> dict[str, Any]:
        """Support as dict behavior.
        
        Returns
        -------
        dict[str, Any]
            The mapped values.
        """
        
        return {
            "kind": self.kind,
            "name": self.name,
            "qualname": self.qualname,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "line_count": self.line_count,
            "called_self_methods": self.called_self_methods,
            "self_attr_reads": self.self_attr_reads,
            "self_attr_writes": self.self_attr_writes,
            "imports_used": self.imports_used,
            "gui_touches": self.gui_touches,
            "side_effects": self.side_effects,
            "candidate_island": self.candidate_island,
            "risk": self.risk,
        }


@dataclass(slots=True)
class _IslandAudit:
    """Grouped responsibility-island evidence."""

    name: str
    symbols: list[_SymbolAudit]
    line_count: int
    self_attr_reads: list[str]
    self_attr_writes: list[str]
    gui_touches: list[str]
    side_effects: list[str]
    risk: str

    def as_dict(self) -> dict[str, Any]:
        """Support as dict behavior.
        
        Returns
        -------
        dict[str, Any]
            The mapped values.
        """
        
        return {
            "name": self.name,
            "symbols": [symbol.qualname for symbol in self.symbols],
            "line_count": self.line_count,
            "self_attr_reads": self.self_attr_reads,
            "self_attr_writes": self.self_attr_writes,
            "gui_touches": self.gui_touches,
            "side_effects": self.side_effects,
            "risk": self.risk,
        }


def _iter_auditable_symbols(tree: ast.Module) -> Iterable[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Support iter auditable symbols behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    
    Returns
    -------
    Iterable[ast.FunctionDef | ast.AsyncFunctionDef]
        The sequence of values.
    """
    
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    child._audit_class_name = node.name  # type: ignore[attr-defined]
                    yield child

def _audit_symbol(node: ast.FunctionDef | ast.AsyncFunctionDef, imports: dict[str, str]) -> _SymbolAudit:
    """Return AST-derived evidence for one auditable symbol."""
    visitor = _SymbolVisitor(imports)
    visitor.visit(node)
    try:
        class_name = node._audit_class_name  # type: ignore[attr-defined]
    except AttributeError:
        class_name = ""
    kind = "method" if class_name else "function"
    qualname = f"{class_name}.{node.name}" if class_name else node.name
    try:
        line_start = int(node.lineno or 0)
    except AttributeError:
        line_start = 0
    try:
        line_end = int(node.end_lineno or line_start)
    except AttributeError:
        line_end = line_start
    side_effects = sorted(visitor.side_effects)
    gui_touches = sorted(visitor.gui_touches)
    candidate = _candidate_label(node.name, side_effects, gui_touches)
    risk = _risk_for(side_effects, gui_touches, visitor.self_attr_writes)
    return _SymbolAudit(
        kind=kind,
        name=node.name,
        qualname=qualname,
        line_start=line_start,
        line_end=line_end,
        line_count=max(1, line_end - line_start + 1),
        called_self_methods=sorted(visitor.called_self_methods),
        self_attr_reads=sorted(visitor.self_attr_reads),
        self_attr_writes=sorted(visitor.self_attr_writes),
        imports_used=sorted(visitor.imports_used),
        gui_touches=gui_touches,
        side_effects=side_effects,
        candidate_island=candidate,
        risk=risk,
    )


def _group_islands(symbols: list[_SymbolAudit]) -> list[_IslandAudit]:
    """Support group islands behavior.
    
    Parameters
    ----------
    symbols : list[_SymbolAudit]
        The symbols value.
    
    Returns
    -------
    list[_IslandAudit]
        The list of values.
    """
    
    groups: dict[str, list[_SymbolAudit]] = {}
    for symbol in symbols:
        groups.setdefault(symbol.candidate_island, []).append(symbol)
    islands: list[_IslandAudit] = []
    for name, items in groups.items():
        risk = _combined_risk(item.risk for item in items)
        islands.append(
            _IslandAudit(
                name=name,
                symbols=items,
                line_count=sum(item.line_count for item in items),
                self_attr_reads=sorted({value for item in items for value in item.self_attr_reads}),
                self_attr_writes=sorted({value for item in items for value in item.self_attr_writes}),
                gui_touches=sorted({value for item in items for value in item.gui_touches}),
                side_effects=sorted({value for item in items for value in item.side_effects}),
                risk=risk,
            )
        )
    islands.sort(key=lambda item: (-item.line_count, item.risk, item.name))
    return islands


def _combined_risk(risks: Iterable[str]) -> str:
    """Support combined risk behavior.
    
    Parameters
    ----------
    risks : Iterable[str]
        The risks value.
    
    Returns
    -------
    str
        The string result.
    """
    
    values = set(risks)
    if "high" in values:
        return "high"
    if "medium" in values:
        return "medium"
    return "low"


def _independence_matrix(islands: list[_IslandAudit]) -> list[dict[str, Any]]:
    """Support independence matrix behavior.
    
    Parameters
    ----------
    islands : list[_IslandAudit]
        The islands value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []
    for i, left in enumerate(islands):
        for right in islands[i + 1:]:
            reasons: list[str] = []
            shared_writes = set(left.self_attr_writes).intersection(right.self_attr_writes)
            if shared_writes:
                reasons.append("conflicting self writes: " + ", ".join(sorted(shared_writes)))
            left_methods = {symbol.name for symbol in left.symbols}
            right_methods = {symbol.name for symbol in right.symbols}
            left_calls_right = {call for symbol in left.symbols for call in symbol.called_self_methods if call in right_methods}
            right_calls_left = {call for symbol in right.symbols for call in symbol.called_self_methods if call in left_methods}
            if left_calls_right or right_calls_left:
                called = sorted(left_calls_right.union(right_calls_left))
                reasons.append("cross-island self calls: " + ", ".join(called))
            shared_gui = set(left.gui_touches).intersection(right.gui_touches)
            if shared_gui and ("signal_wiring" in left.side_effects or "signal_wiring" in right.side_effects):
                reasons.append("shared GUI signal/widget scope: " + ", ".join(sorted(shared_gui)))
            risky_overlap = {"file_delete", "subprocess", "archive", "thread_or_timer"}.intersection(left.side_effects).intersection(right.side_effects)
            if risky_overlap:
                reasons.append("shared high-risk side effect category: " + ", ".join(sorted(risky_overlap)))
            relation = "independent" if not reasons else "dependent"
            rows.append({"left": left.name, "right": right.name, "relation": relation, "reasons": reasons})
    return rows


def _recommend_patch_shape(islands: list[_IslandAudit], matrix: list[dict[str, Any]]) -> dict[str, Any]:
    """Support recommend patch shape behavior.
    
    Parameters
    ----------
    islands : list[_IslandAudit]
        The islands value.
    matrix : list[dict[str, Any]]
        The matrix value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    if not islands:
        return {"mode": "manual_audit_required", "reason": "No auditable symbols found."}
    safe_pairs = [row for row in matrix if row["relation"] == "independent"]
    island_by_name = {island.name: island for island in islands}
    candidates: list[tuple[int, str, str]] = []
    for row in safe_pairs:
        left = island_by_name[row["left"]]
        right = island_by_name[row["right"]]
        if "high" in {left.risk, right.risk}:
            continue
        candidates.append((left.line_count + right.line_count, left.name, right.name))
    if candidates:
        candidates.sort(reverse=True)
        _, left, right = candidates[0]
        return {"mode": "two_island_batch_candidate", "islands": [left, right], "reason": "Largest independent non-high-risk pair."}
    best = islands[0]
    return {"mode": "single_island", "islands": [best.name], "reason": "No clean non-high-risk pair found; use strongest single island."}
