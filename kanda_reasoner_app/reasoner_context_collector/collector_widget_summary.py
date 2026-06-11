"""Support static evidence collection for Project Reasoner."""

# =====================================================
# collector_widget_summary - Widget summary and hotspots
# =====================================================

from __future__ import annotations

from collections import Counter
from typing import Any


def build_widget_summary(
    widget_registry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Build additive summary metrics for the parallel widget registry.

    This module does not modify or replace any existing collector output.
    It summarizes only the new widget_registry structure.
    """
    records = list(widget_registry.values())

    type_counter: Counter[str] = Counter()
    source_file_counter: Counter[str] = Counter()
    source_symbol_counter: Counter[str] = Counter()
    display_text_counter: Counter[str] = Counter()

    widgets_with_display_text = 0
    widgets_with_placeholder_text = 0
    widgets_with_tooltip_text = 0
    widgets_with_object_name = 0
    widgets_with_layout = 0
    widgets_with_connections = 0
    widgets_with_container = 0
    widgets_without_variable_name = 0
    widgets_without_text = 0

    for record in records:
        widget_type = _safe_str(record.get("widget_type", "unknown")) or "unknown"
        source_file = _safe_str(record.get("source_file", ""))
        source_symbol = _safe_str(record.get("source_symbol", ""))
        display_text = _safe_str(record.get("display_text", ""))
        placeholder_text = _safe_str(record.get("placeholder_text", ""))
        tooltip_text = _safe_str(record.get("tooltip_text", ""))
        object_name = _safe_str(record.get("object_name", ""))
        variable_name = _safe_str(record.get("variable_name", ""))
        parent_layout = _safe_str(record.get("parent_layout", ""))
        container_widget = _safe_str(record.get("container_widget", ""))

        type_counter[widget_type] += 1

        if source_file:
            source_file_counter[source_file] += 1

        if source_symbol:
            source_symbol_counter[source_symbol] += 1

        if display_text:
            widgets_with_display_text += 1
            display_text_counter[display_text] += 1

        if placeholder_text:
            widgets_with_placeholder_text += 1

        if tooltip_text:
            widgets_with_tooltip_text += 1

        if object_name:
            widgets_with_object_name += 1

        if parent_layout:
            widgets_with_layout += 1

        if container_widget:
            widgets_with_container += 1

        if _has_connections(record):
            widgets_with_connections += 1

        if not variable_name:
            widgets_without_variable_name += 1

        if not _has_any_user_visible_text(record):
            widgets_without_text += 1

    duplicate_display_text_count = sum(
        1 for _text, count in display_text_counter.items()
        if count > 1
    )

    return {
        "widget_count": len(records),
        "widget_type_count": len(type_counter),
        "widget_file_count": len(source_file_counter),
        "widget_scope_count": len(source_symbol_counter),
        "widgets_with_display_text": widgets_with_display_text,
        "widgets_with_placeholder_text": widgets_with_placeholder_text,
        "widgets_with_tooltip_text": widgets_with_tooltip_text,
        "widgets_with_object_name": widgets_with_object_name,
        "widgets_with_layout": widgets_with_layout,
        "widgets_with_connections": widgets_with_connections,
        "widgets_with_container": widgets_with_container,
        "widgets_without_variable_name": widgets_without_variable_name,
        "widgets_without_text": widgets_without_text,
        "duplicate_display_text_count": duplicate_display_text_count,
        "widget_type_breakdown": dict(sorted(type_counter.items())),
        "top_widget_files": _top_counter_rows(source_file_counter, limit=25),
        "top_widget_scopes": _top_counter_rows(source_symbol_counter, limit=25),
        "top_display_texts": _top_counter_rows(display_text_counter, limit=25),
    }


def build_widget_hotspots(
    widget_registry: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """
    Build prioritized widget hotspot rows.

    Hotspots are meant to surface potentially important or suspicious widgets,
    such as widgets without text, layout, variable name, or connections.
    """
    text_counter = _display_text_counter(widget_registry)
    hotspots: list[dict[str, Any]] = []

    for widget_id, record in widget_registry.items():
        display_text = _safe_str(record.get("display_text", ""))
        placeholder_text = _safe_str(record.get("placeholder_text", ""))
        tooltip_text = _safe_str(record.get("tooltip_text", ""))
        variable_name = _safe_str(record.get("variable_name", ""))
        widget_type = _safe_str(record.get("widget_type", "unknown")) or "unknown"
        source_file = _safe_str(record.get("source_file", ""))
        source_symbol = _safe_str(record.get("source_symbol", ""))
        parent_layout = _safe_str(record.get("parent_layout", ""))
        object_name = _safe_str(record.get("object_name", ""))

        duplicate_text = bool(display_text and text_counter.get(display_text, 0) > 1)
        has_any_text = _has_any_user_visible_text(record)
        has_connections = _has_connections(record)
        has_layout = bool(parent_layout)
        has_variable_name = bool(variable_name)

        risk_score = 0

        if duplicate_text:
            risk_score += 3
        if not has_any_text:
            risk_score += 2
        if not has_connections and widget_type in _interactive_widget_types():
            risk_score += 2
        if not has_layout:
            risk_score += 1
        if not has_variable_name:
            risk_score += 1
        if not object_name:
            risk_score += 1

        hotspots.append(
            {
                "widget_id": widget_id,
                "widget_type": widget_type,
                "variable_name": variable_name,
                "display_text": display_text,
                "placeholder_text": placeholder_text,
                "tooltip_text": tooltip_text,
                "source_file": source_file,
                "source_symbol": source_symbol,
                "line": record.get("line"),
                "parent_layout": parent_layout,
                "layout_kind": _safe_str(record.get("layout_kind", "")),
                "object_name": object_name,
                "has_connections": has_connections,
                "has_layout": has_layout,
                "duplicate_display_text": duplicate_text,
                "risk_score": risk_score,
            }
        )

    hotspots.sort(
        key=lambda item: (
            -int(item.get("risk_score", 0)),
            item.get("source_file", ""),
            item.get("source_symbol", ""),
            item.get("line") if item.get("line") is not None else -1,
            item.get("widget_id", ""),
        )
    )

    return hotspots[:limit]


def _display_text_counter(
    widget_registry: dict[str, dict[str, Any]],
) -> dict[str, int]:
    counter: Counter[str] = Counter()

    for record in widget_registry.values():
        display_text = _safe_str(record.get("display_text", ""))
        if display_text:
            counter[display_text] += 1

    return dict(counter)


def _top_counter_rows(counter: Counter[str], limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for value, count in counter.most_common(limit):
        rows.append(
            {
                "value": value,
                "count": int(count),
            }
        )

    return rows


def _interactive_widget_types() -> set[str]:
    return {
        "QPushButton",
        "QCheckBox",
        "QRadioButton",
        "QComboBox",
        "QLineEdit",
        "QListWidget",
        "QTableWidget",
        "QSpinBox",
        "QDoubleSpinBox",
        "QSlider",
        "QTabWidget",
    }


def _has_connections(record: dict[str, Any]) -> bool:
    connections = record.get("connections", [])
    return isinstance(connections, list) and len(connections) > 0


def _has_any_user_visible_text(record: dict[str, Any]) -> bool:
    display_text = _safe_str(record.get("display_text", ""))
    placeholder_text = _safe_str(record.get("placeholder_text", ""))
    tooltip_text = _safe_str(record.get("tooltip_text", ""))
    items = record.get("items", [])
    header_labels = record.get("header_labels", [])
    tab_texts = record.get("tab_texts", [])

    if display_text or placeholder_text or tooltip_text:
        return True

    if isinstance(items, list) and len(items) > 0:
        return True

    if isinstance(header_labels, list) and len(header_labels) > 0:
        return True

    if isinstance(tab_texts, list) and len(tab_texts) > 0:
        return True

    return False


def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    try:
        return str(value).strip()
    except Exception:
        return ""