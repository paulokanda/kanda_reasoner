"""Build a primary definition index for Project Reasoner web AI.

This module is additive over duplicate_symbols and web_ai_symbol_index. It helps
web AI decide which definition is the likely active/canonical implementation when
several symbols share the same short name.

It does not replace duplicate_symbols, symbol_index, edit_ready_symbol_index, or
web_ai_symbol_index.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "build_primary_definition_index",
    "build_primary_definition_summary",
]


LEGACY_PATH_MARKERS = (
    "/archive/",
    "/archives/",
    "/backup/",
    "/backups/",
    "/deprecated/",
    "/legacy/",
    "/old/",
    "/scratch/",
    "/tmp/",
    "/temp/",
    "/_old/",
)

TEST_PATH_MARKERS = (
    "/test/",
    "/tests/",
)

TEST_NAME_MARKERS = (
    "test_",
    "_test.py",
)


def _safe_text(value: Any) -> str:
    """Return a safe stripped string."""
    return str(value or "").strip()


def _safe_int(value: Any) -> int:
    """Return an integer, or zero if conversion fails."""
    try:
        return int(value)
    except Exception:
        return 0


def _safe_float(value: Any) -> float:
    """Return a float, or zero if conversion fails."""
    try:
        return float(value)
    except Exception:
        return 0.0


def _normalize_path(value: Any) -> str:
    """Normalize file paths to forward slashes."""
    text = _safe_text(value).replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text


def _short_symbol_name(symbol: str) -> str:
    """Return the final dotted component for a symbol name."""
    text = _safe_text(symbol)
    if not text:
        return ""
    return text.split(".")[-1]


def _is_test_path(file_path: str) -> bool:
    """Return True when a file path appears to be a test file."""
    normalized = "/" + _normalize_path(file_path).lower().lstrip("/")
    basename = normalized.rsplit("/", 1)[-1]
    if any(marker in normalized for marker in TEST_PATH_MARKERS):
        return True
    return basename.startswith("test_") or basename.endswith("_test.py")


def _is_legacy_path(file_path: str) -> bool:
    """Return True when a file path appears deprecated or non-active."""
    normalized = "/" + _normalize_path(file_path).lower().lstrip("/")
    return any(marker in normalized for marker in LEGACY_PATH_MARKERS)


def _is_init_file(file_path: str) -> bool:
    """Return True when a file is an __init__.py module."""
    return _normalize_path(file_path).lower().endswith("/__init__.py")


def _candidate_reason_parts(record: dict[str, Any]) -> list[str]:
    """Build concise score reason labels for one candidate."""
    parts: list[str] = []

    if _safe_text(record.get("docstring_first_line", "")):
        parts.append("has_docstring")

    if _safe_text(record.get("confidence", "")) == "high":
        parts.append("high_confidence")

    if bool(record.get("has_complete_span", False)):
        parts.append("complete_source_span")

    if not bool(record.get("span_fallback_used", False)):
        parts.append("no_span_fallback")

    file_path = _safe_text(record.get("file", ""))
    if file_path and not _is_test_path(file_path):
        parts.append("non_test_source")
    if file_path and not _is_legacy_path(file_path):
        parts.append("non_legacy_path")

    kind = _safe_text(record.get("kind", ""))
    if kind in {"class", "function", "method"}:
        parts.append(kind + "_definition")

    return parts


def _score_candidate(record: dict[str, Any], requested_symbol: str) -> float:
    """Return deterministic primary-definition candidate score."""
    score = 0.0

    symbol = _safe_text(record.get("symbol", ""))
    kind = _safe_text(record.get("kind", ""))
    file_path = _safe_text(record.get("file", ""))
    confidence = _safe_text(record.get("confidence", ""))

    if symbol == requested_symbol:
        score += 12.0
    elif _short_symbol_name(symbol) == requested_symbol:
        score += 8.0

    if kind == "class":
        score += 4.0
    elif kind == "function":
        score += 3.0
    elif kind == "method":
        score += 2.5

    if _safe_text(record.get("docstring_first_line", "")):
        score += 5.0

    if confidence == "high":
        score += 4.0
    elif confidence == "medium":
        score += 2.0
    elif confidence == "low":
        score += 0.5

    if bool(record.get("has_complete_span", False)):
        score += 2.0

    if not bool(record.get("span_fallback_used", False)):
        score += 1.0

    if _safe_text(record.get("definition_line", "")):
        score += 1.0

    if file_path:
        if not _is_test_path(file_path):
            score += 6.0
        else:
            score -= 6.0

        if not _is_legacy_path(file_path):
            score += 3.0
        else:
            score -= 5.0

        if _is_init_file(file_path):
            score -= 1.0

    line_start = _safe_int(record.get("line_start", 0))
    if line_start > 0:
        score += max(0.0, 1.0 - min(float(line_start), 1000.0) / 1000.0)

    return round(score, 3)


def _candidate_from_symbol_record(
    record: dict[str, Any],
    requested_symbol: str,
) -> dict[str, Any]:
    """Convert web_ai_symbol_index record into primary-definition candidate."""
    score = _score_candidate(record, requested_symbol)
    reason_parts = _candidate_reason_parts(record)

    return {
        "evidence_id": _safe_text(record.get("evidence_id", "")),
        "symbol": _safe_text(record.get("symbol", "")),
        "qualified_name": _safe_text(record.get("qualified_name", "")),
        "kind": _safe_text(record.get("kind", "")),
        "file": _normalize_path(record.get("file", "")),
        "line_start": _safe_int(record.get("line_start", 0)),
        "line_end": _safe_int(record.get("line_end", 0)),
        "parent_symbol": _safe_text(record.get("parent_symbol", "")),
        "docstring_first_line": _safe_text(record.get("docstring_first_line", "")),
        "confidence": _safe_text(record.get("confidence", "")),
        "source_truth": _safe_text(record.get("source_truth", "")),
        "score": score,
        "reason": "_and_".join(reason_parts) if reason_parts else "fallback_candidate",
        "reason_parts": reason_parts,
    }


def _duplicate_symbol_names(duplicate_symbols: list[dict[str, Any]]) -> set[str]:
    """Return short duplicate names from duplicate_symbols payload."""
    names: set[str] = set()
    for item in duplicate_symbols:
        if not isinstance(item, dict):
            continue
        name = _safe_text(item.get("symbol_name", ""))
        if name:
            names.add(name)
    return names


def _candidate_groups(
    web_ai_symbol_index: dict[str, dict[str, Any]],
    duplicate_symbols: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Group candidates by exact symbol and duplicate short symbol names."""
    groups: dict[str, list[dict[str, Any]]] = {}
    duplicate_names = _duplicate_symbol_names(duplicate_symbols)

    for symbol, record in web_ai_symbol_index.items():
        if not isinstance(record, dict):
            continue

        exact_symbol = _safe_text(symbol) or _safe_text(record.get("symbol", ""))
        if not exact_symbol:
            continue

        exact_candidate = _candidate_from_symbol_record(record, exact_symbol)
        groups.setdefault(exact_symbol, []).append(exact_candidate)

        short = _short_symbol_name(exact_symbol)
        if short and short in duplicate_names:
            short_candidate = _candidate_from_symbol_record(record, short)
            groups.setdefault(short, []).append(short_candidate)

    return groups


def _sort_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort candidates by primary-definition preference."""
    deduped: dict[tuple[str, str, int, str], dict[str, Any]] = {}
    for item in candidates:
        key = (
            _safe_text(item.get("symbol", "")),
            _safe_text(item.get("file", "")),
            _safe_int(item.get("line_start", 0)),
            _safe_text(item.get("kind", "")),
        )
        existing = deduped.get(key)
        if existing is None or _safe_float(item.get("score", 0)) > _safe_float(existing.get("score", 0)):
            deduped[key] = item

    return sorted(
        deduped.values(),
        key=lambda item: (
            -_safe_float(item.get("score", 0.0)),
            _safe_text(item.get("file", "")),
            _safe_int(item.get("line_start", 0)),
            _safe_text(item.get("symbol", "")),
        ),
    )


def build_primary_definition_summary(
    primary_definition_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build compact summary for primary_definition_index."""
    duplicate_group_count = 0
    confidence_frequency: dict[str, int] = {}

    for payload in primary_definition_index.values():
        if bool(payload.get("is_duplicate_group", False)):
            duplicate_group_count += 1

        primary = payload.get("primary", {})
        if isinstance(primary, dict):
            confidence = _safe_text(primary.get("confidence", "")) or "unknown"
            confidence_frequency[confidence] = confidence_frequency.get(confidence, 0) + 1

    return {
        "symbol_group_count": len(primary_definition_index),
        "duplicate_group_count": duplicate_group_count,
        "confidence_frequency": dict(sorted(confidence_frequency.items())),
    }


def build_primary_definition_index(
    web_ai_symbol_index: dict[str, dict[str, Any]],
    duplicate_symbols: list[dict[str, Any]],
    *,
    enabled: bool = True,
) -> dict[str, dict[str, Any]]:
    """Build primary-definition records from web_ai_symbol_index.

    The index is additive and deterministic. It does not remove or alter
    duplicate_symbols; it only gives web AI a ranked primary candidate.
    """
    if not enabled:
        return {}

    groups = _candidate_groups(web_ai_symbol_index, duplicate_symbols)
    duplicate_names = _duplicate_symbol_names(duplicate_symbols)
    output: dict[str, dict[str, Any]] = {}

    for symbol, candidates in sorted(groups.items()):
        ordered = _sort_candidates(candidates)
        if not ordered:
            continue

        primary = ordered[0]
        alternates = ordered[1:]

        output[symbol] = {
            "symbol": symbol,
            "primary": primary,
            "alternates": alternates,
            "alternate_count": len(alternates),
            "candidate_count": len(ordered),
            "is_duplicate_group": bool(symbol in duplicate_names or len(ordered) > 1),
            "selection_rule": (
                "Prefer exact symbol, non-test source, non-legacy path, "
                "docstring, high confidence, complete span, and stable line order."
            ),
            "source_index": "web_ai_symbol_index",
        }

    return output
