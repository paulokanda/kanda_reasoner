# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_symbol_affinity.py
"""Deterministic multi-signal affinity evidence for split-plan clusters."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from .dependency_clusterer import DependencyCluster
from .models import ModuleAnalysisReport, RefactorSymbol

if TYPE_CHECKING:
    from .planner_git_cochange import GitCochangeEvidence

__all__ = ["ClusterAffinity", "cluster_affinity"]

_TOKEN_RE = re.compile(r"[A-Za-z]+|\d+")
_CAMEL_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_STOP_TOKENS = {
    "a",
    "an",
    "and",
    "behavior",
    "for",
    "from",
    "function",
    "functions",
    "helper",
    "helpers",
    "is",
    "module",
    "modules",
    "of",
    "or",
    "support",
    "the",
    "to",
    "value",
    "values",
    "with",
}


@dataclass(frozen=True)
class ClusterAffinity:
    """Explainable affinity score between two existing atomic clusters."""

    left_cluster_id: str
    right_cluster_id: str
    total_score: float
    structural_score: float
    semantic_score: float
    source_proximity_score: float
    role_compatibility_score: float
    historical_cochange_score: float
    historical_cochange_raw_score: float
    history_confidence_weight: float
    shared_history_commit_count: int
    history_available: bool
    shared_callers: tuple[str, ...]
    shared_reference_tokens: tuple[str, ...]
    shared_semantic_tokens: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready affinity evidence record."""
        return asdict(self)


def cluster_affinity(
    report: ModuleAnalysisReport,
    left: DependencyCluster,
    right: DependencyCluster,
    git_history: "GitCochangeEvidence | None" = None,
) -> ClusterAffinity:
    """Return deterministic multi-signal affinity between two clusters."""
    symbol_by_name = {symbol.name: symbol for symbol in report.symbols}
    left_symbols = _cluster_symbols(left, symbol_by_name)
    right_symbols = _cluster_symbols(right, symbol_by_name)
    shared_callers = _shared_callers(report, left, right)
    left_refs = _reference_tokens(left_symbols, set(left.symbols))
    right_refs = _reference_tokens(right_symbols, set(right.symbols))
    shared_refs = sorted(left_refs & right_refs)
    reference_jaccard = _jaccard(left_refs, right_refs)
    caller_score = 1.0 if shared_callers else 0.0
    structural = max(caller_score, reference_jaccard)

    left_semantic = _semantic_tokens(left_symbols)
    right_semantic = _semantic_tokens(right_symbols)
    shared_semantic = sorted(left_semantic & right_semantic)
    semantic = _jaccard(left_semantic, right_semantic)
    proximity = _source_proximity(left_symbols, right_symbols)
    role_score = _role_compatibility(left.role, right.role)
    history = (
        git_history.affinity_for_symbols(left.symbols, right.symbols)
        if git_history is not None
        else None
    )
    if history is not None and history.available:
        historical_raw_score = history.score
        historical_score = history.effective_score
        total = (
            0.30 * structural
            + 0.30 * semantic
            + 0.15 * proximity
            + 0.10 * role_score
            + 0.15 * historical_score
        )
    else:
        historical_raw_score = 0.0
        historical_score = 0.0
        total = (
            0.35 * structural
            + 0.35 * semantic
            + 0.20 * proximity
            + 0.10 * role_score
        )
    return ClusterAffinity(
        left_cluster_id=left.cluster_id,
        right_cluster_id=right.cluster_id,
        total_score=round(total, 6),
        structural_score=round(structural, 6),
        semantic_score=round(semantic, 6),
        source_proximity_score=round(proximity, 6),
        role_compatibility_score=round(role_score, 6),
        historical_cochange_score=round(historical_score, 6),
        historical_cochange_raw_score=round(historical_raw_score, 6),
        history_confidence_weight=(history.confidence_weight if history is not None else 0.0),
        shared_history_commit_count=(history.shared_commit_count if history is not None else 0),
        history_available=bool(history is not None and history.available),
        shared_callers=tuple(sorted(shared_callers)),
        shared_reference_tokens=tuple(shared_refs),
        shared_semantic_tokens=tuple(shared_semantic),
    )


def _cluster_symbols(
    cluster: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> list[RefactorSymbol]:
    """Return known symbols owned by a cluster."""
    return [symbol_by_name[name] for name in cluster.symbols if name in symbol_by_name]


def _shared_callers(
    report: ModuleAnalysisReport,
    left: DependencyCluster,
    right: DependencyCluster,
) -> set[str]:
    """Return top-level symbols that reference both cluster symbol sets."""
    left_names = set(left.symbols)
    right_names = set(right.symbols)
    result: set[str] = set()
    for caller in report.symbols:
        references = set(caller.references)
        if references & left_names and references & right_names:
            result.add(caller.name)
    return result


def _reference_tokens(symbols: list[RefactorSymbol], owned: set[str]) -> set[str]:
    """Return normalized non-owned reference vocabulary for symbols."""
    tokens: set[str] = set()
    for symbol in symbols:
        for reference in symbol.references:
            if reference not in owned:
                tokens.update(_tokens(reference))
        for reference in symbol.imports_used:
            tokens.update(_tokens(reference))
        for reference in symbol.globals_used:
            tokens.update(_tokens(reference))
    return tokens


def _semantic_tokens(symbols: list[RefactorSymbol]) -> set[str]:
    """Return responsibility vocabulary from symbol names and docstrings."""
    tokens: set[str] = set()
    for symbol in symbols:
        tokens.update(_tokens(symbol.name))
        tokens.update(_tokens(symbol.docstring_text))
        tokens.update(_tokens(symbol.signature))
    return tokens


def _tokens(text: str) -> set[str]:
    """Return normalized lexical tokens suitable for deterministic affinity."""
    expanded = _CAMEL_RE.sub(" ", str(text).replace("_", " "))
    return {
        token.lower()
        for token in _TOKEN_RE.findall(expanded)
        if len(token) > 1 and token.lower() not in _STOP_TOKENS
    }


def _jaccard(left: set[str], right: set[str]) -> float:
    """Return Jaccard similarity for two token sets."""
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _source_proximity(
    left_symbols: list[RefactorSymbol],
    right_symbols: list[RefactorSymbol],
) -> float:
    """Return a bounded score favoring nearby source responsibilities."""
    if not left_symbols or not right_symbols:
        return 0.0
    left_start = min(symbol.start_line for symbol in left_symbols)
    left_end = max(symbol.end_line for symbol in left_symbols)
    right_start = min(symbol.start_line for symbol in right_symbols)
    right_end = max(symbol.end_line for symbol in right_symbols)
    if left_end < right_start:
        gap = right_start - left_end
    elif right_end < left_start:
        gap = left_start - right_end
    else:
        gap = 0
    return 1.0 / (1.0 + gap / 50.0)


def _role_compatibility(left_role: str, right_role: str) -> float:
    """Return a coarse deterministic compatibility score for helper roles."""
    if left_role == right_role:
        return 1.0
    if left_role.endswith("_helper") and right_role.endswith("_helper"):
        return 0.7
    return 0.4
