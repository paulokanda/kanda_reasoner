"""Build stable evidence IDs for Project Reasoner web AI.

This module creates a compact cross-reference index of deterministic evidence IDs
for files, symbols, snippets, and primary definitions.

It is additive over existing collector output. It does not replace files,
symbol_index, web_ai_symbol_index, edit_ready_symbol_index, snippet_index,
duplicate_symbols, or primary_definition_index.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

__all__ = [
    "build_stable_evidence_id_index",
    "build_stable_evidence_id_summary",
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
    """Normalize file paths to forward slashes."""
    text = _safe_text(value).replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text.strip("/")


def _slug(value: Any, *, fallback: str = "item") -> str:
    """Return a compact deterministic ASCII slug."""
    text = _safe_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or fallback


def _hash12(value: str) -> str:
    """Return a deterministic 12-character SHA-256 prefix."""
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()[:12]


def _file_evidence_id(file_path: str) -> str:
    """Build deterministic file evidence ID."""
    normalized = _normalize_path(file_path)
    base = normalized.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return "file_" + _slug(base, fallback="file") + "_" + _hash12(normalized)


def _snippet_evidence_id(file_path: str, line_start: int, anchor: str) -> str:
    """Build deterministic snippet evidence ID."""
    normalized = _normalize_path(file_path)
    key = normalized + "::" + str(line_start) + "::" + _safe_text(anchor)
    return "snip_" + _slug(anchor, fallback="snippet") + "_" + str(line_start) + "_" + _hash12(key)


def _primary_evidence_id(symbol: str, primary_evidence_id: str) -> str:
    """Build deterministic primary-definition group evidence ID."""
    key = _safe_text(symbol) + "::" + _safe_text(primary_evidence_id)
    return "primary_" + _slug(symbol, fallback="symbol") + "_" + _hash12(key)


def _add_record(
    output: dict[str, dict[str, Any]],
    record: dict[str, Any],
) -> None:
    """Add an evidence record if its evidence_id is not empty."""
    evidence_id = _safe_text(record.get("evidence_id", ""))
    if not evidence_id:
        return

    output[evidence_id] = record


def _build_file_records(files_payload: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build stable evidence records for files."""
    records: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        if not isinstance(file_record, dict):
            continue

        file_path = _normalize_path(file_record.get("path", ""))
        if not file_path:
            continue

        evidence_id = _file_evidence_id(file_path)
        record = {
            "evidence_id": evidence_id,
            "evidence_kind": "file",
            "stable_key": file_path,
            "file": file_path,
            "symbol": "",
            "line_start": 0,
            "line_end": 0,
            "source_index": "files",
            "confidence": "high",
        }
        _add_record(records, record)

    return records


def _build_symbol_records(
    web_ai_symbol_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build stable evidence records from web_ai_symbol_index."""
    records: dict[str, dict[str, Any]] = {}

    for symbol, payload in web_ai_symbol_index.items():
        if not isinstance(payload, dict):
            continue

        evidence_id = _safe_text(payload.get("evidence_id", ""))
        if not evidence_id:
            continue

        file_path = _normalize_path(payload.get("file", ""))
        symbol_name = _safe_text(payload.get("symbol", symbol))
        kind = _safe_text(payload.get("kind", "symbol")) or "symbol"
        line_start = _safe_int(payload.get("line_start", 0))
        line_end = _safe_int(payload.get("line_end", 0))
        stable_key = file_path + "::" + symbol_name + "::" + kind + "::" + str(line_start)

        record = {
            "evidence_id": evidence_id,
            "evidence_kind": "symbol_definition",
            "stable_key": stable_key,
            "file": file_path,
            "symbol": symbol_name,
            "qualified_name": _safe_text(payload.get("qualified_name", symbol_name)),
            "kind": kind,
            "line_start": line_start,
            "line_end": line_end,
            "parent_symbol": _safe_text(payload.get("parent_symbol", "")),
            "source_index": "web_ai_symbol_index",
            "confidence": _safe_text(payload.get("confidence", "")) or "unknown",
            "source_truth": _safe_text(payload.get("source_truth", "")),
        }
        _add_record(records, record)

    return records


def _build_snippet_records(snippet_index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Build stable evidence records for snippet_index entries."""
    records: dict[str, dict[str, Any]] = {}

    for key, payload in snippet_index.items():
        if not isinstance(payload, dict):
            continue

        file_path = _normalize_path(payload.get("path") or payload.get("file") or "")
        if not file_path:
            continue

        line_start = _safe_int(
            payload.get("line")
            or payload.get("line_start")
            or payload.get("start_line")
        )
        line_end = _safe_int(
            payload.get("line_end")
            or payload.get("end_line")
            or line_start
        )
        anchor = _safe_text(payload.get("anchor") or payload.get("symbol") or key)
        evidence_id = _safe_text(payload.get("snippet_id", ""))
        if not evidence_id:
            evidence_id = _snippet_evidence_id(file_path, line_start, anchor)

        stable_key = file_path + "::snippet::" + str(line_start) + "::" + anchor
        record = {
            "evidence_id": evidence_id,
            "evidence_kind": "snippet",
            "stable_key": stable_key,
            "file": file_path,
            "symbol": _safe_text(payload.get("symbol", "")),
            "anchor": anchor,
            "line_start": line_start,
            "line_end": line_end,
            "source_index": "snippet_index",
            "confidence": "medium",
        }
        _add_record(records, record)

    return records


def _build_primary_records(
    primary_definition_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build stable evidence records for primary-definition groups."""
    records: dict[str, dict[str, Any]] = {}

    for symbol, payload in primary_definition_index.items():
        if not isinstance(payload, dict):
            continue

        primary = payload.get("primary", {})
        if not isinstance(primary, dict):
            continue

        primary_evidence_id = _safe_text(primary.get("evidence_id", ""))
        evidence_id = _primary_evidence_id(symbol, primary_evidence_id)
        file_path = _normalize_path(primary.get("file", ""))
        line_start = _safe_int(primary.get("line_start", 0))
        line_end = _safe_int(primary.get("line_end", line_start))

        record = {
            "evidence_id": evidence_id,
            "evidence_kind": "primary_definition",
            "stable_key": _safe_text(symbol) + "::primary_definition",
            "file": file_path,
            "symbol": _safe_text(symbol),
            "primary_evidence_id": primary_evidence_id,
            "line_start": line_start,
            "line_end": line_end,
            "source_index": "primary_definition_index",
            "confidence": _safe_text(primary.get("confidence", "")) or "unknown",
            "alternate_count": _safe_int(payload.get("alternate_count", 0)),
            "candidate_count": _safe_int(payload.get("candidate_count", 0)),
        }
        _add_record(records, record)

    return records


def build_stable_evidence_id_summary(
    stable_evidence_id_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build compact summary for stable_evidence_id_index."""
    kind_frequency: dict[str, int] = {}
    source_index_frequency: dict[str, int] = {}
    confidence_frequency: dict[str, int] = {}

    for record in stable_evidence_id_index.values():
        kind = _safe_text(record.get("evidence_kind", "")) or "unknown"
        source_index = _safe_text(record.get("source_index", "")) or "unknown"
        confidence = _safe_text(record.get("confidence", "")) or "unknown"

        kind_frequency[kind] = kind_frequency.get(kind, 0) + 1
        source_index_frequency[source_index] = source_index_frequency.get(source_index, 0) + 1
        confidence_frequency[confidence] = confidence_frequency.get(confidence, 0) + 1

    return {
        "evidence_record_count": len(stable_evidence_id_index),
        "kind_frequency": dict(sorted(kind_frequency.items())),
        "source_index_frequency": dict(sorted(source_index_frequency.items())),
        "confidence_frequency": dict(sorted(confidence_frequency.items())),
    }


def build_stable_evidence_id_index(
    files_payload: list[dict[str, Any]],
    web_ai_symbol_index: dict[str, dict[str, Any]],
    snippet_index: dict[str, Any],
    primary_definition_index: dict[str, dict[str, Any]],
    *,
    enabled: bool = True,
) -> dict[str, dict[str, Any]]:
    """Build a compact stable evidence ID cross-reference index."""
    if not enabled:
        return {}

    output: dict[str, dict[str, Any]] = {}

    for source in (
        _build_file_records(files_payload),
        _build_symbol_records(web_ai_symbol_index),
        _build_snippet_records(snippet_index),
        _build_primary_records(primary_definition_index),
    ):
        for evidence_id, record in source.items():
            if evidence_id not in output:
                output[evidence_id] = record

    return dict(sorted(output.items()))
