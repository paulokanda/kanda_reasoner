"""Support static evidence collection for Project Reasoner."""

# =====================================================
# collector_widget_text_index - Widget text indexing
# =====================================================

from __future__ import annotations

from collections import Counter
from typing import Any


def build_widget_text_index(
    widget_registry: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Build a searchable text index from the parallel widget registry.

    This module is additive only. It does not modify or replace any
    existing collector output. It indexes user-visible widget text and
    related text-bearing properties so downstream tools can answer
    questions like:
    - where is the "Close" button
    - which widgets use the text "Project root:"
    - which files contain duplicated visible widget text

    Output structure
    ----------------
    {
        "text_entries": {
            "<text>": {
                "text": "<text>",
                "normalized_text": "<normalized>",
                "entry_count": <int>,
                "widget_ids": [...],
                "widget_types": [...],
                "source_files": [...],
                "source_symbols": [...],
                "property_types": [...],
                "records": [...],
            },
            ...
        },
        "property_type_counts": {...},
        "duplicate_texts": [...],
        "summary": {...},
    }
    """
    text_entries: dict[str, dict[str, Any]] = {}
    property_type_counter: Counter[str] = Counter()

    for widget_id, record in widget_registry.items():
        for property_type, text_value in _iter_widget_text_values(record):
            clean_text = _safe_str(text_value)
            if not clean_text:
                continue

            normalized_text = _normalize_text(clean_text)

            if clean_text not in text_entries:
                text_entries[clean_text] = {
                    "text": clean_text,
                    "normalized_text": normalized_text,
                    "entry_count": 0,
                    "widget_ids": [],
                    "widget_types": [],
                    "source_files": [],
                    "source_symbols": [],
                    "property_types": [],
                    "records": [],
                }

            entry = text_entries[clean_text]
            entry["entry_count"] += 1

            widget_type = _safe_str(record.get("widget_type", ""))
            source_file = _safe_str(record.get("source_file", ""))
            source_symbol = _safe_str(record.get("source_symbol", ""))

            if widget_id not in entry["widget_ids"]:
                entry["widget_ids"].append(widget_id)

            if widget_type and widget_type not in entry["widget_types"]:
                entry["widget_types"].append(widget_type)

            if source_file and source_file not in entry["source_files"]:
                entry["source_files"].append(source_file)

            if source_symbol and source_symbol not in entry["source_symbols"]:
                entry["source_symbols"].append(source_symbol)

            if property_type and property_type not in entry["property_types"]:
                entry["property_types"].append(property_type)

            entry["records"].append(
                {
                    "widget_id": widget_id,
                    "widget_type": widget_type,
                    "variable_name": _safe_str(record.get("variable_name", "")),
                    "source_file": source_file,
                    "source_symbol": source_symbol,
                    "line": record.get("line"),
                    "property_type": property_type,
                    "text": clean_text,
                }
            )

            property_type_counter[property_type] += 1

    duplicate_texts = _build_duplicate_texts(text_entries)

    summary = {
        "unique_text_count": len(text_entries),
        "duplicate_text_count": len(duplicate_texts),
        "property_type_counts": dict(sorted(property_type_counter.items())),
        "top_texts": _build_top_text_rows(text_entries, limit=25),
    }

    return {
        "text_entries": dict(sorted(text_entries.items())),
        "property_type_counts": dict(sorted(property_type_counter.items())),
        "duplicate_texts": duplicate_texts,
        "summary": summary,
    }


def build_widget_text_hotspots(
    widget_text_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """
    Build hotspot rows for suspicious or high-value text patterns.

    Hotspots prioritize:
    - duplicated visible text
    - texts reused across many files
    - texts reused across many widgets
    """
    text_entries = widget_text_index.get("text_entries", {})
    if not isinstance(text_entries, dict):
        return []

    hotspots: list[dict[str, Any]] = []

    for text_value, payload in text_entries.items():
        if not isinstance(payload, dict):
            continue

        widget_count = len(payload.get("widget_ids", []))
        file_count = len(payload.get("source_files", []))
        property_count = len(payload.get("property_types", []))
        entry_count = int(payload.get("entry_count", 0))

        risk_score = 0
        if widget_count > 1:
            risk_score += 3
        if file_count > 1:
            risk_score += 2
        if property_count > 1:
            risk_score += 1
        if entry_count > 3:
            risk_score += 1

        hotspots.append(
            {
                "text": text_value,
                "normalized_text": _safe_str(payload.get("normalized_text", "")),
                "entry_count": entry_count,
                "widget_count": widget_count,
                "file_count": file_count,
                "property_count": property_count,
                "widget_types": sorted(payload.get("widget_types", [])),
                "source_files": sorted(payload.get("source_files", [])),
                "property_types": sorted(payload.get("property_types", [])),
                "risk_score": risk_score,
            }
        )

    hotspots.sort(
        key=lambda item: (
            -int(item.get("risk_score", 0)),
            -int(item.get("widget_count", 0)),
            -int(item.get("file_count", 0)),
            item.get("text", ""),
        )
    )

    return hotspots[:limit]


def _iter_widget_text_values(record: dict[str, Any]) -> list[tuple[str, str]]:
    """
    Yield text-bearing fields from a widget record as
    (property_type, text_value) pairs.
    """
    values: list[tuple[str, str]] = []

    display_text = _safe_str(record.get("display_text", ""))
    if display_text:
        values.append(("display_text", display_text))

    placeholder_text = _safe_str(record.get("placeholder_text", ""))
    if placeholder_text:
        values.append(("placeholder_text", placeholder_text))

    tooltip_text = _safe_str(record.get("tooltip_text", ""))
    if tooltip_text:
        values.append(("tooltip_text", tooltip_text))

    object_name = _safe_str(record.get("object_name", ""))
    if object_name:
        values.append(("object_name", object_name))

    for item_value in _string_list(record.get("items", [])):
        values.append(("items", item_value))

    for header_value in _string_list(record.get("header_labels", [])):
        values.append(("header_labels", header_value))

    for tab_text in _iter_tab_text_values(record.get("tab_texts", [])):
        values.append(("tab_texts", tab_text))

    return values


def _iter_tab_text_values(tab_texts: Any) -> list[str]:
    results: list[str] = []

    if not isinstance(tab_texts, list):
        return results

    for item in tab_texts:
        if isinstance(item, dict):
            text_value = _safe_str(item.get("text", ""))
            if text_value:
                results.append(text_value)
        else:
            text_value = _safe_str(item)
            if text_value:
                results.append(text_value)

    return results


def _string_list(values: Any) -> list[str]:
    results: list[str] = []

    if not isinstance(values, list):
        return results

    for value in values:
        text_value = _safe_str(value)
        if text_value:
            results.append(text_value)

    return results


def _build_duplicate_texts(
    text_entries: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    duplicates: list[dict[str, Any]] = []

    for text_value, payload in text_entries.items():
        if not isinstance(payload, dict):
            continue

        widget_count = len(payload.get("widget_ids", []))
        if widget_count <= 1:
            continue

        duplicates.append(
            {
                "text": text_value,
                "normalized_text": _safe_str(payload.get("normalized_text", "")),
                "entry_count": int(payload.get("entry_count", 0)),
                "widget_count": widget_count,
                "file_count": len(payload.get("source_files", [])),
                "property_types": sorted(payload.get("property_types", [])),
                "widget_ids": list(payload.get("widget_ids", [])),
            }
        )

    duplicates.sort(
        key=lambda item: (
            -int(item.get("widget_count", 0)),
            -int(item.get("file_count", 0)),
            item.get("text", ""),
        )
    )

    return duplicates


def _build_top_text_rows(
    text_entries: dict[str, dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for text_value, payload in text_entries.items():
        if not isinstance(payload, dict):
            continue

        rows.append(
            {
                "text": text_value,
                "entry_count": int(payload.get("entry_count", 0)),
                "widget_count": len(payload.get("widget_ids", [])),
                "file_count": len(payload.get("source_files", [])),
                "property_types": sorted(payload.get("property_types", [])),
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("entry_count", 0)),
            -int(item.get("widget_count", 0)),
            -int(item.get("file_count", 0)),
            item.get("text", ""),
        )
    )

    return rows[:limit]


def _normalize_text(text_value: str) -> str:
    return " ".join(_safe_str(text_value).lower().split())


def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    try:
        return str(value).strip()
    except Exception:
        return ""