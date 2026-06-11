"""Internal matching helpers for widget UI action bridge records."""

from __future__ import annotations

from typing import Any

from .normalization import _list_or_empty, _safe_str

__all__: list[str] = []


def _find_matching_signal_record(
    normalized_signal_records: list[dict[str, Any]],
    source_file: str,
    source_symbol: str,
    signal_name: str,
    target: str,
    line: Any,
) -> dict[str, Any]:
    exact_matches: list[dict[str, Any]] = []
    relaxed_matches: list[dict[str, Any]] = []

    for signal_record in normalized_signal_records:
        if _safe_str(signal_record.get("source_file", "")) != source_file:
            continue
        if _safe_str(signal_record.get("source_symbol", "")) != source_symbol:
            continue
        if _safe_str(signal_record.get("signal_name", "")) != signal_name:
            continue

        signal_target = _safe_str(signal_record.get("target", ""))
        signal_line = signal_record.get("line")

        if signal_target == target and signal_line == line:
            exact_matches.append(signal_record)
        elif signal_target == target:
            relaxed_matches.append(signal_record)

    if exact_matches:
        return exact_matches[0]
    if relaxed_matches:
        return relaxed_matches[0]
    return {}


def _match_widget_for_action(
    widget_registry: dict[str, dict[str, Any]],
    source_file: str,
    source_symbol: str,
    signal_name: str,
    signal_record: dict[str, Any],
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []

    for widget_record in widget_registry.values():
        if not isinstance(widget_record, dict):
            continue

        if _safe_str(widget_record.get("source_file", "")) != source_file:
            continue
        if _safe_str(widget_record.get("source_symbol", "")) != source_symbol:
            continue

        candidates.append(widget_record)

    if not candidates:
        return {}

    widget_hint = _safe_str(signal_record.get("widget", ""))
    if widget_hint:
        matched_by_hint = _match_widget_by_hint(candidates, widget_hint)
        if matched_by_hint:
            return matched_by_hint

    matched_by_signal = _match_widget_by_signal_name(candidates, signal_name)
    if matched_by_signal:
        return matched_by_signal

    return _prefer_interactive_widget(candidates)


def _match_widget_by_hint(
    candidates: list[dict[str, Any]],
    widget_hint: str,
) -> dict[str, Any]:
    hint = _safe_str(widget_hint).lower()

    for candidate in candidates:
        variable_name = _safe_str(candidate.get("variable_name", "")).lower()
        widget_ref = _safe_str(candidate.get("widget_ref", "")).lower()
        object_name = _safe_str(candidate.get("object_name", "")).lower()

        if hint and hint in {variable_name, widget_ref, object_name}:
            return candidate

        if hint and variable_name and hint.endswith(variable_name):
            return candidate

    return {}


def _match_widget_by_signal_name(
    candidates: list[dict[str, Any]],
    signal_name: str,
) -> dict[str, Any]:
    signal = _safe_str(signal_name)

    if "clicked" in signal:
        for candidate in candidates:
            if _safe_str(candidate.get("widget_type", "")) == "QPushButton":
                return candidate

    if "toggled" in signal:
        for candidate in candidates:
            if _safe_str(candidate.get("widget_type", "")) in {"QCheckBox", "QRadioButton"}:
                return candidate

    if "textChanged" in signal or "editingFinished" in signal:
        for candidate in candidates:
            if _safe_str(candidate.get("widget_type", "")) == "QLineEdit":
                return candidate

    if "currentIndexChanged" in signal:
        for candidate in candidates:
            if _safe_str(candidate.get("widget_type", "")) == "QComboBox":
                return candidate

    return {}


def _prefer_interactive_widget(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    interactive_types = {
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

    for candidate in candidates:
        if _safe_str(candidate.get("widget_type", "")) in interactive_types:
            return candidate

    return candidates[0] if candidates else {}


def _match_confidence(
    matched_widget: dict[str, Any],
    matched_signal_record: dict[str, Any],
) -> float:
    if matched_widget and matched_signal_record:
        if _safe_str(matched_signal_record.get("widget", "")):
            return 0.95
        return 0.80
    if matched_widget:
        return 0.60
    return 0.0
