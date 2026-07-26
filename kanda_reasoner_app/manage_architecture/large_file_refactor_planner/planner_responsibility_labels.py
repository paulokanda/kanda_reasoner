# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_responsibility_labels.py
"""Deterministic responsibility labels for heuristic helper clusters."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from .dependency_clusterer import DependencyCluster
from .models import ModuleAnalysisReport, RefactorSymbol

__all__ = [
    "ResponsibilityLabel",
    "label_cluster_responsibilities",
]

_TOKEN_RE = re.compile(r"[A-Za-z]+|\d+")
_CAMEL_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_STOP_TOKENS = {
    "a", "an", "and", "behavior", "for", "from", "function", "functions",
    "helper", "helpers", "is", "module", "modules", "of", "or", "support",
    "the", "to", "value", "values", "with",
}
_RESPONSIBILITY_LEXICON: dict[str, frozenset[str]] = {
    "path_resolution": frozenset({
        "path", "root", "normalize", "find", "compare", "resolve", "relative",
        "project",
    }),
    "helper_selection": frozenset({
        "helper", "select", "candidate", "score", "main", "target", "record",
        "private", "public", "suffix", "module", "role", "warning", "active",
        "imports", "stem",
    }),
    "decision_reporting": frozenset({
        "decision", "status", "format", "summary", "report", "evidence",
        "confidence", "test", "tests", "run", "result",
    }),
    "validation_policy": frozenset({
        "validate", "validation", "guard", "policy", "risk", "warning",
        "check", "status", "blocker",
    }),
    "serialization": frozenset({
        "dict", "json", "serialize", "normalize", "schema", "payload", "text",
    }),
    "configuration": frozenset({
        "option", "options", "config", "configuration", "setting", "settings",
        "policy", "include", "maximum", "minimum",
    }),
}


@dataclass(frozen=True)
class ResponsibilityLabel:
    """Explainable deterministic responsibility label for one helper cluster."""

    cluster_id: str
    primary_responsibility: str
    secondary_responsibilities: tuple[str, ...]
    confidence: str
    confidence_score: float
    evidence_tokens: tuple[str, ...]
    scores: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready label evidence."""
        return asdict(self)


def label_cluster_responsibilities(
    report: ModuleAnalysisReport,
    clusters: list[DependencyCluster],
) -> dict[str, ResponsibilityLabel]:
    """Return deterministic responsibility labels keyed by cluster id."""
    symbol_by_name = {symbol.name: symbol for symbol in report.symbols}
    return {
        cluster.cluster_id: _label_cluster(cluster, symbol_by_name)
        for cluster in clusters
    }


def _label_cluster(
    cluster: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> ResponsibilityLabel:
    symbols = [symbol_by_name[name] for name in cluster.symbols if name in symbol_by_name]
    tokens = _responsibility_tokens(symbols)
    raw_scores = {
        label: _weighted_overlap(tokens, vocabulary)
        for label, vocabulary in _RESPONSIBILITY_LEXICON.items()
    }
    ranked = sorted(raw_scores.items(), key=lambda item: (item[1], item[0]), reverse=True)
    primary, top_score = ranked[0] if ranked else ("cohesive_operations", 0.0)
    if top_score <= 0.0:
        primary = _fallback_label(tokens)
    secondaries = tuple(
        label
        for label, score in ranked[1:]
        if score >= max(0.18, top_score * 0.50) and score > 0.0
    )[:2]
    confidence_score = _confidence_score(ranked, len(tokens))
    confidence = (
        "high" if confidence_score >= 0.72 else
        "medium" if confidence_score >= 0.45 else
        "low"
    )
    evidence = tuple(_top_evidence_tokens(tokens, primary))
    return ResponsibilityLabel(
        cluster_id=cluster.cluster_id,
        primary_responsibility=primary,
        secondary_responsibilities=secondaries,
        confidence=confidence,
        confidence_score=round(confidence_score, 6),
        evidence_tokens=evidence,
        scores={name: round(score, 6) for name, score in ranked if score > 0.0},
    )


def _responsibility_tokens(symbols: list[RefactorSymbol]) -> dict[str, float]:
    weights: dict[str, float] = {}
    for symbol in symbols:
        _add_tokens(weights, symbol.name, 3.0)
        _add_tokens(weights, symbol.signature, 1.5)
        _add_tokens(weights, symbol.docstring_text, 1.0)
        for reference in symbol.references:
            _add_tokens(weights, reference, 0.35)
    return weights


def _add_tokens(weights: dict[str, float], text: str, weight: float) -> None:
    for token in _tokens(text):
        weights[token] = weights.get(token, 0.0) + weight


def _tokens(text: str) -> set[str]:
    expanded = _CAMEL_RE.sub(" ", str(text).replace("_", " "))
    return {
        token.lower()
        for token in _TOKEN_RE.findall(expanded)
        if len(token) > 1 and token.lower() not in _STOP_TOKENS
    }


def _weighted_overlap(tokens: dict[str, float], vocabulary: frozenset[str]) -> float:
    total = sum(tokens.values())
    if total <= 0.0:
        return 0.0
    matched = sum(weight for token, weight in tokens.items() if token in vocabulary)
    coverage = len(set(tokens) & set(vocabulary)) / max(1, len(vocabulary))
    return min(1.0, 0.75 * (matched / total) + 0.25 * coverage)


def _confidence_score(ranked: list[tuple[str, float]], token_count: int) -> float:
    if not ranked or ranked[0][1] <= 0.0:
        return 0.2 if token_count >= 3 else 0.0
    top = ranked[0][1]
    second = ranked[1][1] if len(ranked) > 1 else 0.0
    separation = max(0.0, top - second)
    token_support = min(1.0, token_count / 8.0)
    return min(1.0, 0.65 * min(1.0, top * 2.5) + 0.25 * min(1.0, separation * 5.0) + 0.10 * token_support)


def _fallback_label(tokens: dict[str, float]) -> str:
    ranked = sorted(tokens.items(), key=lambda item: (item[1], item[0]), reverse=True)
    names = [token for token, _weight in ranked[:2]]
    return "_".join(names) if names else "cohesive_operations"


def _top_evidence_tokens(tokens: dict[str, float], primary: str) -> list[str]:
    vocabulary = _RESPONSIBILITY_LEXICON.get(primary, frozenset())
    matched = [item for item in tokens.items() if item[0] in vocabulary]
    source = matched or list(tokens.items())
    return [token for token, _weight in sorted(source, key=lambda item: (item[1], item[0]), reverse=True)[:8]]
