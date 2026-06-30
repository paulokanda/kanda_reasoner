# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/normalization.py
"""Internal normalization helpers for widget UI action bridge records."""

from __future__ import annotations

from typing import Any

__all__: list[str] = []


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


def _normalize_qt_signal_records(qt_signal_map: Any) -> list[dict[str, Any]]:
    """Support normalize qt signal records behavior.
    
    Parameters
    ----------
    qt_signal_map : Any
        The qt signal map value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    records: list[dict[str, Any]] = []

    if isinstance(qt_signal_map, list):
        raw_records = qt_signal_map
    elif isinstance(qt_signal_map, dict):
        raw_records = []
        for value in qt_signal_map.values():
            if isinstance(value, list):
                raw_records.extend(value)
    else:
        raw_records = []

    for raw_record in raw_records:
        if not isinstance(raw_record, dict):
            continue

        records.append(
            {
                "source_file": _safe_str(raw_record.get("source_file", "")),
                "source_symbol": _safe_str(raw_record.get("source_symbol", "")),
                "signal_name": _safe_str(
                    raw_record.get("signal_name", "") or raw_record.get("signal", "")
                ),
                "target": _safe_str(
                    raw_record.get("target", "") or raw_record.get("handler", "")
                ),
                "target_kind": _safe_str(raw_record.get("target_kind", "")),
                "widget": _safe_str(raw_record.get("widget", "")),
                "line": raw_record.get("line"),
            }
        )

    return records
