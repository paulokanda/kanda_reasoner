# project-path: kanda_reasoner_app/reasoner_context_collector/collector_web_ai_symbol_index.py
"""Build a compact web-AI symbol index for Project Reasoner.

This module is additive over the existing Step 4 collector payload. It does not
replace symbol_index, edit_ready_symbol_index, snippet_index, or source_file_index.

The purpose is to help web AI answer exact symbol questions such as:
- What is the responsibility of PromptBuilder?
- Where is PromptBuilder defined?
- Which file defines ProjectRetriever?

All records are derived from already-collected source data.
"""

from __future__ import annotations

import re
from typing import Any

__all__ = [
    "build_web_ai_symbol_index",
    "build_web_ai_symbol_summary",
]


def _safe_text(value: Any) -> str:
    """Return a safe stripped string."""
    return str(value or "").strip()


def _safe_int(value: Any) -> int:
    """Return int(value), or zero if conversion fails."""
    try:
        return int(value)
    except Exception:
        return 0


def _normalize_path(value: Any) -> str:
    """Normalize a project-relative path to forward slashes."""
    text = _safe_text(value).replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text


def _first_line(value: Any) -> str:
    """Return the first non-empty line from text."""
    for line in _safe_text(value).splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _stable_slug(value: str) -> str:
    """Return a deterministic ASCII slug for evidence IDs."""
    text = _safe_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "symbol"


def _definition_line_from_excerpt(source_excerpt: str) -> str:
    """Return the first class/function definition line in an excerpt."""
    for line in _safe_text(source_excerpt).splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if (
            lowered.startswith("class ")
            or lowered.startswith("def ")
            or lowered.startswith("async def ")
        ):
            return stripped
    return ""


def _signature_from_definition_line(definition_line: str) -> str:
    """Return a compact signature-like string from a definition line."""
    text = _safe_text(definition_line)
    if not text:
        return ""

    if text.endswith(":"):
        text = text[:-1].rstrip()

    return text


def _source_truth_for_docstring(docstring: str) -> str:
    """Return source truth class for docstring evidence."""
    return "ast_docstring" if _safe_text(docstring) else "source_span"


def _confidence_for_record(
    *,
    has_docstring: bool,
    has_complete_span: bool,
    span_fallback_used: bool,
) -> str:
    """Return confidence label for a web-AI symbol record."""
    if has_docstring and has_complete_span and not span_fallback_used:
        return "high"
    if has_complete_span:
        return "medium"
    return "low"


def _iter_file_symbols(file_record: dict[str, Any]) -> list[dict[str, Any]]:
    """Return top-level function, class, and method records from a file."""
    symbols: list[dict[str, Any]] = []

    for function_record in file_record.get("functions", []):
        if isinstance(function_record, dict):
            record = dict(function_record)
            record["_web_ai_kind"] = record.get("symbol_kind") or "function"
            symbols.append(record)

    for class_record in file_record.get("classes", []):
        if not isinstance(class_record, dict):
            continue

        cls = dict(class_record)
        cls["_web_ai_kind"] = cls.get("symbol_kind") or "class"
        symbols.append(cls)

        parent = _safe_text(class_record.get("qualname") or class_record.get("name"))
        for method_record in class_record.get("methods", []):
            if isinstance(method_record, dict):
                method = dict(method_record)
                method["_web_ai_kind"] = method.get("symbol_kind") or "method"
                if not _safe_text(method.get("parent_symbol")) and parent:
                    method["parent_symbol"] = parent
                symbols.append(method)

    return symbols


def _build_raw_symbol_lookup(
    files_payload: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build symbol-name to collected source record lookup."""
    lookup: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        path = _normalize_path(file_record.get("path", ""))
        module_name = _safe_text(file_record.get("module_name", ""))

        for symbol_record in _iter_file_symbols(file_record):
            symbol_name = _safe_text(
                symbol_record.get("qualname")
                or symbol_record.get("name")
            )
            if not symbol_name:
                continue

            record = dict(symbol_record)
            record["_web_ai_file"] = path
            record["_web_ai_module_name"] = module_name
            lookup[symbol_name] = record

    return lookup


def _build_evidence_id(
    *,
    symbol: str,
    kind: str,
    file_path: str,
    line_start: int,
) -> str:
    """Build a deterministic evidence ID for a symbol definition."""
    path_part = _stable_slug(file_path.rsplit("/", 1)[-1].rsplit(".", 1)[0])
    symbol_part = _stable_slug(symbol.split(".")[-1])
    kind_part = _stable_slug(kind)
    return "sym_" + path_part + "_" + symbol_part + "_" + kind_part + "_" + str(line_start)


def build_web_ai_symbol_summary(
    web_ai_symbol_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a compact summary for web_ai_symbol_index."""
    kind_frequency: dict[str, int] = {}
    confidence_frequency: dict[str, int] = {}
    source_truth_frequency: dict[str, int] = {}
    docstring_count = 0

    for record in web_ai_symbol_index.values():
        kind = _safe_text(record.get("kind", "unknown")) or "unknown"
        confidence = _safe_text(record.get("confidence", "unknown")) or "unknown"
        source_truth = _safe_text(record.get("source_truth", "unknown")) or "unknown"

        kind_frequency[kind] = kind_frequency.get(kind, 0) + 1
        confidence_frequency[confidence] = confidence_frequency.get(confidence, 0) + 1
        source_truth_frequency[source_truth] = source_truth_frequency.get(source_truth, 0) + 1

        if _safe_text(record.get("docstring_first_line", "")):
            docstring_count += 1

    return {
        "symbol_count": len(web_ai_symbol_index),
        "docstring_symbol_count": docstring_count,
        "kind_frequency": dict(sorted(kind_frequency.items())),
        "confidence_frequency": dict(sorted(confidence_frequency.items())),
        "source_truth_frequency": dict(sorted(source_truth_frequency.items())),
    }


def build_web_ai_symbol_index(
    files_payload: list[dict[str, Any]],
    edit_ready_symbol_index: dict[str, dict[str, Any]],
    legacy_symbol_index: dict[str, dict[str, Any]] | None = None,
    *,
    enabled: bool = True,
) -> dict[str, dict[str, Any]]:
    """Build a compact additive symbol index for web AI.

    Parameters
    ----------
    files_payload:
        Existing collector files payload.
    edit_ready_symbol_index:
        Existing source-span-backed symbol index.
    legacy_symbol_index:
        Existing symbol_index payload, used only as fallback metadata.
    enabled:
        When False, return an empty index.
    """
    if not enabled:
        return {}

    legacy_symbol_index = legacy_symbol_index or {}
    raw_lookup = _build_raw_symbol_lookup(files_payload)

    output: dict[str, dict[str, Any]] = {}

    for symbol_name, edit_record in sorted(edit_ready_symbol_index.items()):
        raw_record = raw_lookup.get(symbol_name, {})
        legacy_record = legacy_symbol_index.get(symbol_name, {})

        file_path = _normalize_path(
            edit_record.get("file")
            or raw_record.get("_web_ai_file")
            or legacy_record.get("file")
        )
        kind = (
            _safe_text(edit_record.get("kind"))
            or _safe_text(raw_record.get("_web_ai_kind"))
            or _safe_text(legacy_record.get("kind"))
            or "unknown"
        )
        line_start = _safe_int(
            edit_record.get("line_start")
            or raw_record.get("lineno")
            or legacy_record.get("line")
        )
        line_end = _safe_int(edit_record.get("line_end") or line_start)
        parent_symbol = _safe_text(
            edit_record.get("parent_symbol")
            or raw_record.get("parent_symbol")
        )
        module_name = _safe_text(raw_record.get("_web_ai_module_name", ""))
        source_excerpt = _safe_text(edit_record.get("source_excerpt", ""))
        definition_line = _definition_line_from_excerpt(source_excerpt)
        docstring_first_line = _first_line(raw_record.get("docstring", ""))

        has_complete_span = bool(edit_record.get("has_complete_span", False))
        span_fallback_used = bool(edit_record.get("span_fallback_used", False))
        confidence = _confidence_for_record(
            has_docstring=bool(docstring_first_line),
            has_complete_span=has_complete_span,
            span_fallback_used=span_fallback_used,
        )

        evidence_id = _build_evidence_id(
            symbol=symbol_name,
            kind=kind,
            file_path=file_path,
            line_start=line_start,
        )

        output[symbol_name] = {
            "evidence_id": evidence_id,
            "symbol": symbol_name,
            "qualified_name": symbol_name,
            "kind": kind,
            "file": file_path,
            "module_name": module_name,
            "line_start": line_start,
            "line_end": line_end,
            "parent_symbol": parent_symbol,
            "definition_line": definition_line,
            "signature": _signature_from_definition_line(definition_line),
            "docstring_first_line": docstring_first_line,
            "definition_excerpt_id": evidence_id,
            "source_truth": _source_truth_for_docstring(docstring_first_line),
            "confidence": confidence,
            "has_complete_span": has_complete_span,
            "span_fallback_used": span_fallback_used,
            "symbol_sha12": _safe_text(edit_record.get("symbol_sha12", "")),
            "source_sha12": _safe_text(edit_record.get("source_sha12", "")),
        }

    return output
