# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/indexing.py
"""Internal indexing helpers for widget UI action bridge records."""

from __future__ import annotations

from typing import Any

from .normalization import _safe_str

__all__: list[str] = []


def _append_widget_action_index(
    widget_action_index: dict[str, dict[str, Any]],
    bridge_record: dict[str, Any],
) -> None:
    """Support append widget action index behavior.
    
    Parameters
    ----------
    widget_action_index : dict[str, dict[str, Any]]
        The widget action index value.
    bridge_record : dict[str, Any]
        The bridge record value.
    """
    
    widget_id = _safe_str(bridge_record.get("widget_id", "")) or "<unmatched_widget>"

    if widget_id not in widget_action_index:
        widget_action_index[widget_id] = {
            "widget_id": widget_id,
            "widget_type": _safe_str(bridge_record.get("widget_type", "")),
            "widget_variable_name": _safe_str(
                bridge_record.get("widget_variable_name", "")
            ),
            "widget_display_text": _safe_str(
                bridge_record.get("widget_display_text", "")
            ),
            "widget_source_file": _safe_str(
                bridge_record.get("widget_source_file", "")
            ),
            "widget_source_symbol": _safe_str(
                bridge_record.get("widget_source_symbol", "")
            ),
            "action_count": 0,
            "resolved_action_count": 0,
            "signals": [],
            "handlers": [],
            "records": [],
        }

    entry = widget_action_index[widget_id]
    entry["action_count"] += 1

    if bool(bridge_record.get("resolved_target", False)):
        entry["resolved_action_count"] += 1

    signal_name = _safe_str(bridge_record.get("signal_name", ""))
    handler = _safe_str(bridge_record.get("handler", ""))

    if signal_name and signal_name not in entry["signals"]:
        entry["signals"].append(signal_name)

    if handler and handler not in entry["handlers"]:
        entry["handlers"].append(handler)

    entry["records"].append(bridge_record)


def _append_action_widget_index(
    action_widget_index: dict[str, dict[str, Any]],
    bridge_record: dict[str, Any],
) -> None:
    """Support append action widget index behavior.
    
    Parameters
    ----------
    action_widget_index : dict[str, dict[str, Any]]
        The action widget index value.
    bridge_record : dict[str, Any]
        The bridge record value.
    """
    
    action_key = _safe_str(bridge_record.get("action_key", ""))
    if not action_key:
        return

    if action_key not in action_widget_index:
        action_widget_index[action_key] = {
            "action_key": action_key,
            "signal_name": _safe_str(bridge_record.get("signal_name", "")),
            "handler": _safe_str(bridge_record.get("handler", "")),
            "matched_widget_count": 0,
            "widget_ids": [],
            "records": [],
        }

    entry = action_widget_index[action_key]
    widget_id = _safe_str(bridge_record.get("widget_id", ""))

    if widget_id:
        if widget_id not in entry["widget_ids"]:
            entry["widget_ids"].append(widget_id)
        entry["matched_widget_count"] = len(entry["widget_ids"])

    entry["records"].append(bridge_record)


def _build_bridge_summary(
    bridge_records: list[dict[str, Any]],
    widget_action_index: dict[str, dict[str, Any]],
    action_widget_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Support build bridge summary behavior.
    
    Parameters
    ----------
    bridge_records : list[dict[str, Any]]
        The bridge records value.
    widget_action_index : dict[str, dict[str, Any]]
        The widget action index value.
    action_widget_index : dict[str, dict[str, Any]]
        The action widget index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    matched_widget_record_count = sum(
        1 for record in bridge_records
        if _safe_str(record.get("widget_id", ""))
    )

    unresolved_target_count = sum(
        1 for record in bridge_records
        if not bool(record.get("resolved_target", False))
    )

    unmatched_action_count = sum(
        1 for payload in action_widget_index.values()
        if isinstance(payload, dict) and not bool(payload.get("matched_widget_count", 0))
    )

    widget_with_actions_count = sum(
        1 for widget_id in widget_action_index
        if widget_id and widget_id != "<unmatched_widget>"
    )

    return {
        "bridge_record_count": len(bridge_records),
        "matched_widget_record_count": matched_widget_record_count,
        "unmatched_widget_record_count": len(bridge_records) - matched_widget_record_count,
        "unresolved_target_count": unresolved_target_count,
        "widget_with_actions_count": widget_with_actions_count,
        "action_key_count": len(action_widget_index),
        "unmatched_action_count": unmatched_action_count,
    }
