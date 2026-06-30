# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge.py
"""Support static evidence collection for Project Reasoner."""

# =====================================================
# collector_widget_ui_action_bridge - Bridge widgets to UI actions
# =====================================================

from __future__ import annotations

from typing import Any
from .collector_widget_ui_action_bridge_help import (
    _append_action_widget_index,
    _append_widget_action_index,
    _build_bridge_summary,
    _find_matching_signal_record,
    _list_or_empty,
    _match_confidence,
    _match_widget_by_hint,
    _match_widget_by_signal_name,
    _match_widget_for_action,
    _normalize_qt_signal_records,
    _prefer_interactive_widget,
    _safe_str,
)

__all__ = [
    "build_widget_ui_action_bridge",
    "build_widget_ui_action_hotspots",
]


def build_widget_ui_action_bridge(
    widget_registry: dict[str, dict[str, Any]],
    ui_action_index: dict[str, dict[str, Any]],
    qt_signal_map: Any,
) -> dict[str, Any]:
    """
    Build an additive bridge between the parallel widget registry and the
    existing UI action collectors.

    This module does not replace or mutate:
    - collector_qt.extract_qt_signal_map
    - collector_ui_actions.build_ui_action_index

    It consumes their current outputs and adds a widget-oriented mapping
    that answers questions like:
    - which widget likely owns a signal connection
    - which handler is associated with a widget
    - which widgets have actions but no matched signal records
    """

    bridge_records: list[dict[str, Any]] = []
    widget_action_index: dict[str, dict[str, Any]] = {}
    action_widget_index: dict[str, dict[str, Any]] = {}

    normalized_signal_records = _normalize_qt_signal_records(qt_signal_map)

    for action_key, action_payload in ui_action_index.items():
        if not isinstance(action_payload, dict):
            continue

        source_symbol = _safe_str(action_payload.get("source_symbol", ""))
        signal_name = _safe_str(
            action_payload.get("signal_name", "") or action_payload.get("signal", "")
        )
        target = _safe_str(
            action_payload.get("target", "") or action_payload.get("handler", "")
        )
        action_records = _list_or_empty(action_payload.get("records", []))

        for action_record in action_records:
            if not isinstance(action_record, dict):
                continue

            action_source_file = _safe_str(action_record.get("source_file", ""))
            action_source_symbol = _safe_str(
                action_record.get("source_symbol", "") or source_symbol
            )
            action_signal_name = _safe_str(
                action_record.get("signal_name", "") or signal_name
            )
            action_handler = _safe_str(action_record.get("handler", "") or target)

            matched_signal_record = _find_matching_signal_record(
                normalized_signal_records=normalized_signal_records,
                source_file=action_source_file,
                source_symbol=action_source_symbol,
                signal_name=action_signal_name,
                target=action_handler,
                line=action_record.get("line"),
            )

            matched_widget = _match_widget_for_action(
                widget_registry=widget_registry,
                source_file=action_source_file,
                source_symbol=action_source_symbol,
                signal_name=action_signal_name,
                signal_record=matched_signal_record,
            )

            bridge_record = {
                "action_key": action_key,
                "widget_id": _safe_str(matched_widget.get("widget_id", "")),
                "widget_type": _safe_str(matched_widget.get("widget_type", "")),
                "widget_variable_name": _safe_str(matched_widget.get("variable_name", "")),
                "widget_display_text": _safe_str(matched_widget.get("display_text", "")),
                "widget_source_file": _safe_str(matched_widget.get("source_file", "")),
                "widget_source_symbol": _safe_str(matched_widget.get("source_symbol", "")),
                "action_source_file": action_source_file,
                "action_source_symbol": action_source_symbol,
                "signal_name": action_signal_name,
                "handler": action_handler,
                "target_file": _safe_str(action_record.get("target_file", "")),
                "target_line": action_record.get("target_line"),
                "target_kind": _safe_str(action_record.get("target_kind", "")),
                "target_bucket": _safe_str(action_record.get("target_bucket", "")),
                "resolved_target": bool(action_record.get("resolved_target", False)),
                "qt_signal_line": matched_signal_record.get("line"),
                "qt_signal_widget_hint": _safe_str(matched_signal_record.get("widget", "")),
                "qt_signal_target_kind": _safe_str(
                    matched_signal_record.get("target_kind", "")
                ),
                "match_confidence": _match_confidence(
                    matched_widget=matched_widget,
                    matched_signal_record=matched_signal_record,
                ),
            }

            bridge_records.append(bridge_record)
            _append_widget_action_index(widget_action_index, bridge_record)
            _append_action_widget_index(action_widget_index, bridge_record)

    summary = _build_bridge_summary(
        bridge_records=bridge_records,
        widget_action_index=widget_action_index,
        action_widget_index=action_widget_index,
    )

    return {
        "bridge_records": bridge_records,
        "widget_action_index": dict(sorted(widget_action_index.items())),
        "action_widget_index": dict(sorted(action_widget_index.items())),
        "summary": summary,
    }


def build_widget_ui_action_hotspots(
    widget_ui_action_bridge: dict[str, Any],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """
    Build hotspot rows from the widget-action bridge.

    Priority is given to:
    - action records without a matched widget
    - widgets with many actions
    - unresolved handler targets
    """
    widget_action_index = widget_ui_action_bridge.get("widget_action_index", {})
    action_widget_index = widget_ui_action_bridge.get("action_widget_index", {})
    bridge_records = _list_or_empty(widget_ui_action_bridge.get("bridge_records", []))

    hotspots: list[dict[str, Any]] = []

    for widget_id, payload in widget_action_index.items():
        if not isinstance(payload, dict):
            continue

        action_count = int(payload.get("action_count", 0))
        resolved_action_count = int(payload.get("resolved_action_count", 0))
        unresolved_action_count = action_count - resolved_action_count

        risk_score = 0
        if not widget_id or widget_id == "<unmatched_widget>":
            risk_score += 4
        if action_count >= 3:
            risk_score += 2
        elif action_count >= 2:
            risk_score += 1
        if unresolved_action_count > 0:
            risk_score += 2

        hotspots.append(
            {
                "widget_id": widget_id,
                "widget_type": _safe_str(payload.get("widget_type", "")),
                "widget_variable_name": _safe_str(payload.get("widget_variable_name", "")),
                "widget_display_text": _safe_str(payload.get("widget_display_text", "")),
                "widget_source_file": _safe_str(payload.get("widget_source_file", "")),
                "widget_source_symbol": _safe_str(payload.get("widget_source_symbol", "")),
                "action_count": action_count,
                "resolved_action_count": resolved_action_count,
                "unresolved_action_count": unresolved_action_count,
                "signals": sorted(payload.get("signals", [])),
                "handlers": sorted(payload.get("handlers", [])),
                "risk_score": risk_score,
            }
        )

    unmatched_action_count = sum(
        1 for action_key, payload in action_widget_index.items()
        if isinstance(payload, dict)
        and not bool(payload.get("matched_widget_count", 0))
    )

    if unmatched_action_count > 0:
        hotspots.append(
            {
                "widget_id": "<unmatched_widget>",
                "widget_type": "",
                "widget_variable_name": "",
                "widget_display_text": "",
                "widget_source_file": "",
                "widget_source_symbol": "",
                "action_count": unmatched_action_count,
                "resolved_action_count": 0,
                "unresolved_action_count": unmatched_action_count,
                "signals": [],
                "handlers": [],
                "risk_score": 5,
            }
        )

    hotspots.sort(
        key=lambda item: (
            -int(item.get("risk_score", 0)),
            -int(item.get("action_count", 0)),
            item.get("widget_source_file", ""),
            item.get("widget_id", ""),
        )
    )

    return hotspots[:limit]
