# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_layout_index.py
"""Support static evidence collection for Project Reasoner."""

# =====================================================
# collector_widget_layout_index - Widget layout indexing
# =====================================================

from __future__ import annotations

from collections import Counter
from typing import Any


def build_widget_layout_index(
    widget_registry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Build a parallel layout index from the additive widget registry.

    This module is additive only. It does not modify or replace any
    existing collector output. It groups widgets by parent layout and
    preserves per-widget layout records so downstream tools can answer
    questions like:
    - which widgets are inside a given layout
    - which layouts contain the most widgets
    - which widgets have no layout localization
    - which widgets have grid row and column positions
    """
    layout_entries: dict[str, dict[str, Any]] = {}
    layout_kind_counter: Counter[str] = Counter()
    source_file_counter: Counter[str] = Counter()

    widgets_with_layout = 0
    widgets_without_layout = 0
    widgets_with_grid_position = 0

    orphan_widgets: list[dict[str, Any]] = []

    for widget_id, record in widget_registry.items():
        source_file = _safe_str(record.get("source_file", ""))
        source_symbol = _safe_str(record.get("source_symbol", ""))
        widget_type = _safe_str(record.get("widget_type", "unknown")) or "unknown"
        variable_name = _safe_str(record.get("variable_name", ""))
        parent_layout = _safe_str(record.get("parent_layout", ""))
        layout_kind = _safe_str(record.get("layout_kind", ""))
        container_widget = _safe_str(record.get("container_widget", ""))
        layout_position = _dict_or_empty(record.get("layout_position", {}))
        layout_records = _list_or_empty(record.get("layout_records", []))

        if parent_layout:
            widgets_with_layout += 1
        else:
            widgets_without_layout += 1
            orphan_widgets.append(
                {
                    "widget_id": widget_id,
                    "widget_type": widget_type,
                    "variable_name": variable_name,
                    "source_file": source_file,
                    "source_symbol": source_symbol,
                    "line": record.get("line"),
                    "container_widget": container_widget,
                }
            )

        if _has_grid_position(layout_position):
            widgets_with_grid_position += 1

        if layout_kind:
            layout_kind_counter[layout_kind] += 1

        if source_file:
            source_file_counter[source_file] += 1

        normalized_layout_records = _normalize_layout_records(
            widget_id=widget_id,
            widget_type=widget_type,
            variable_name=variable_name,
            source_file=source_file,
            source_symbol=source_symbol,
            fallback_parent_layout=parent_layout,
            fallback_layout_kind=layout_kind,
            fallback_layout_position=layout_position,
            fallback_line=record.get("line"),
            raw_layout_records=layout_records,
        )

        for layout_record in normalized_layout_records:
            layout_key = _build_layout_key(
                source_file=source_file,
                source_symbol=source_symbol,
                parent_layout=_safe_str(layout_record.get("parent_layout", "")),
                layout_kind=_safe_str(layout_record.get("layout_kind", "")),
            )

            if layout_key not in layout_entries:
                layout_entries[layout_key] = {
                    "layout_key": layout_key,
                    "source_file": source_file,
                    "source_symbol": source_symbol,
                    "parent_layout": _safe_str(layout_record.get("parent_layout", "")),
                    "layout_kind": _safe_str(layout_record.get("layout_kind", "")),
                    "widget_count": 0,
                    "widget_ids": [],
                    "widget_types": [],
                    "variable_names": [],
                    "container_widgets": [],
                    "records": [],
                }

            entry = layout_entries[layout_key]
            entry["widget_count"] += 1

            if widget_id not in entry["widget_ids"]:
                entry["widget_ids"].append(widget_id)

            if widget_type and widget_type not in entry["widget_types"]:
                entry["widget_types"].append(widget_type)

            if variable_name and variable_name not in entry["variable_names"]:
                entry["variable_names"].append(variable_name)

            if container_widget and container_widget not in entry["container_widgets"]:
                entry["container_widgets"].append(container_widget)

            entry["records"].append(layout_record)

    summary = {
        "layout_count": len(layout_entries),
        "widgets_with_layout": widgets_with_layout,
        "widgets_without_layout": widgets_without_layout,
        "widgets_with_grid_position": widgets_with_grid_position,
        "orphan_widget_count": len(orphan_widgets),
        "layout_kind_counts": dict(sorted(layout_kind_counter.items())),
        "top_layouts": _build_top_layout_rows(layout_entries, limit=25),
        "top_layout_files": _build_top_counter_rows(source_file_counter, limit=25),
    }

    return {
        "layout_entries": dict(sorted(layout_entries.items())),
        "orphan_widgets": orphan_widgets,
        "summary": summary,
    }


def build_widget_layout_hotspots(
    widget_layout_index: dict[str, Any],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """
    Build hotspot rows for the layout index.

    Hotspots prioritize:
    - layouts with many widgets
    - layouts with mixed layout positions
    - layouts with many records missing explicit position data
    """
    layout_entries = widget_layout_index.get("layout_entries", {})
    if not isinstance(layout_entries, dict):
        return []

    hotspots: list[dict[str, Any]] = []

    for layout_key, payload in layout_entries.items():
        if not isinstance(payload, dict):
            continue

        records = _list_or_empty(payload.get("records", []))
        widget_count = int(payload.get("widget_count", 0))
        positioned_count = 0
        missing_position_count = 0
        grid_count = 0
        tab_count = 0
        form_count = 0

        for record in records:
            if not isinstance(record, dict):
                continue

            layout_kind = _safe_str(record.get("layout_kind", ""))
            layout_position = _dict_or_empty(record.get("layout_position", {}))

            if layout_position:
                positioned_count += 1
            else:
                missing_position_count += 1

            if _has_grid_position(layout_position):
                grid_count += 1

            if layout_kind == "tab_page":
                tab_count += 1

            if layout_kind in {"form_row_label", "form_row_field"}:
                form_count += 1

        risk_score = 0

        if widget_count >= 5:
            risk_score += 3
        elif widget_count >= 3:
            risk_score += 2

        if missing_position_count > 0:
            risk_score += 1

        if grid_count > 0 and missing_position_count > 0:
            risk_score += 1

        if tab_count > 0:
            risk_score += 1

        if form_count > 0:
            risk_score += 1

        hotspots.append(
            {
                "layout_key": layout_key,
                "source_file": _safe_str(payload.get("source_file", "")),
                "source_symbol": _safe_str(payload.get("source_symbol", "")),
                "parent_layout": _safe_str(payload.get("parent_layout", "")),
                "layout_kind": _safe_str(payload.get("layout_kind", "")),
                "widget_count": widget_count,
                "positioned_count": positioned_count,
                "missing_position_count": missing_position_count,
                "grid_count": grid_count,
                "tab_count": tab_count,
                "form_count": form_count,
                "widget_types": sorted(payload.get("widget_types", [])),
                "risk_score": risk_score,
            }
        )

    hotspots.sort(
        key=lambda item: (
            -int(item.get("risk_score", 0)),
            -int(item.get("widget_count", 0)),
            item.get("source_file", ""),
            item.get("parent_layout", ""),
        )
    )

    return hotspots[:limit]


def _normalize_layout_records(
    widget_id: str,
    widget_type: str,
    variable_name: str,
    source_file: str,
    source_symbol: str,
    fallback_parent_layout: str,
    fallback_layout_kind: str,
    fallback_layout_position: dict[str, Any],
    fallback_line: Any,
    raw_layout_records: list[Any],
) -> list[dict[str, Any]]:
    """Support normalize layout records behavior.
    
    Parameters
    ----------
    widget_id : str
        The widget id value.
    widget_type : str
        The widget type value.
    variable_name : str
        The variable name value.
    source_file : str
        The source file value.
    source_symbol : str
        The source symbol value.
    fallback_parent_layout : str
        The fallback parent layout value.
    fallback_layout_kind : str
        The fallback layout kind value.
    fallback_layout_position : dict[str, Any]
        The fallback layout position value.
    fallback_line : Any
        The fallback line value.
    raw_layout_records : list[Any]
        The raw layout records value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    records: list[dict[str, Any]] = []

    if not raw_layout_records and fallback_parent_layout:
        return [
            {
                "widget_id": widget_id,
                "widget_type": widget_type,
                "variable_name": variable_name,
                "source_file": source_file,
                "source_symbol": source_symbol,
                "parent_layout": fallback_parent_layout,
                "layout_kind": fallback_layout_kind,
                "layout_position": fallback_layout_position,
                "line": fallback_line,
            }
        ]

    for raw_record in raw_layout_records:
        if not isinstance(raw_record, dict):
            continue

        records.append(
            {
                "widget_id": widget_id,
                "widget_type": widget_type,
                "variable_name": variable_name,
                "source_file": source_file,
                "source_symbol": source_symbol,
                "parent_layout": _safe_str(raw_record.get("parent_layout", fallback_parent_layout)),
                "layout_kind": _safe_str(raw_record.get("layout_kind", fallback_layout_kind)),
                "layout_position": _dict_or_empty(raw_record.get("layout_position", fallback_layout_position)),
                "line": raw_record.get("line", fallback_line),
            }
        )

    return records


def _build_layout_key(
    source_file: str,
    source_symbol: str,
    parent_layout: str,
    layout_kind: str,
) -> str:
    """Support build layout key behavior.
    
    Parameters
    ----------
    source_file : str
        The source file value.
    source_symbol : str
        The source symbol value.
    parent_layout : str
        The parent layout value.
    layout_kind : str
        The layout kind value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return "::".join(
        [
            _safe_str(source_file),
            _safe_str(source_symbol),
            _safe_str(parent_layout) or "<unknown_layout>",
            _safe_str(layout_kind) or "<unknown_kind>",
        ]
    )


def _build_top_layout_rows(
    layout_entries: dict[str, dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    """Support build top layout rows behavior.
    
    Parameters
    ----------
    layout_entries : dict[str, dict[str, Any]]
        The layout entries value.
    limit : int
        The limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for layout_key, payload in layout_entries.items():
        if not isinstance(payload, dict):
            continue

        rows.append(
            {
                "layout_key": layout_key,
                "source_file": _safe_str(payload.get("source_file", "")),
                "source_symbol": _safe_str(payload.get("source_symbol", "")),
                "parent_layout": _safe_str(payload.get("parent_layout", "")),
                "layout_kind": _safe_str(payload.get("layout_kind", "")),
                "widget_count": int(payload.get("widget_count", 0)),
                "widget_types": sorted(payload.get("widget_types", [])),
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("widget_count", 0)),
            item.get("source_file", ""),
            item.get("parent_layout", ""),
        )
    )

    return rows[:limit]


def _build_top_counter_rows(counter: Counter[str], limit: int) -> list[dict[str, Any]]:
    """Support build top counter rows behavior.
    
    Parameters
    ----------
    counter : Counter[str]
        The counter value.
    limit : int
        The limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for value, count in counter.most_common(limit):
        rows.append(
            {
                "value": value,
                "count": int(count),
            }
        )

    return rows


def _has_grid_position(layout_position: dict[str, Any]) -> bool:
    """Support has grid position behavior.
    
    Parameters
    ----------
    layout_position : dict[str, Any]
        The layout position value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not isinstance(layout_position, dict):
        return False
    return "row" in layout_position and "col" in layout_position


def _dict_or_empty(value: Any) -> dict[str, Any]:
    """Support dict or empty behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    if isinstance(value, dict):
        return value
    return {}


def _list_or_empty(value: Any) -> list[Any]:
    """Support list or empty behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    list[Any]
        The list of values.
    """
    
    if isinstance(value, list):
        return value
    return []


def _safe_str(value: Any) -> str:
    """Support safe str behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if value is None:
        return ""
    try:
        return str(value).strip()
    except Exception:
        return ""
