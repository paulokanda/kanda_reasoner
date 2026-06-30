# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/__init__.py
"""Helper functions for widget UI-action bridge collection."""

from __future__ import annotations

__all__: list[str] = []

from .indexing import (
    _append_action_widget_index,
    _append_widget_action_index,
    _build_bridge_summary,
)
from .matching import (
    _find_matching_signal_record,
    _match_confidence,
    _match_widget_by_hint,
    _match_widget_by_signal_name,
    _match_widget_for_action,
    _prefer_interactive_widget,
)
from .normalization import (
    _list_or_empty,
    _normalize_qt_signal_records,
    _safe_str,
)
