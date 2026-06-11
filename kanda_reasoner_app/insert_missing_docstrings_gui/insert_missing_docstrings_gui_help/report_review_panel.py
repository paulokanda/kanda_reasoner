"""Compatibility facade for Tab 3 report review helpers."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "review_status_for_row",
    "review_severity_for_row",
    "review_action_hint_for_row",
    "load_report_rows",
    "refresh_review_summary",
    "row_needs_review",
    "matches_review_filter",
    "populate_review_list",
    "show_review_item_details",
    "open_docstring_review_window",
]


def _report_panel_runtime() -> Any:
    """Load the Tab 3 report review runtime lazily."""
    module_name = "kanda_reasoner_app.tab3_manual_review_runtime.report_panel_runtime"
    return import_module(module_name)


def review_status_for_row(*args: Any, **kwargs: Any) -> Any:
    """Return the review status for a report row."""
    return _report_panel_runtime()._review_status_for_row(*args, **kwargs)


def review_severity_for_row(*args: Any, **kwargs: Any) -> Any:
    """Return the review severity for a report row."""
    return _report_panel_runtime()._review_severity_for_row(*args, **kwargs)


def review_action_hint_for_row(*args: Any, **kwargs: Any) -> Any:
    """Return the recommended review action for a report row."""
    return _report_panel_runtime()._review_action_hint_for_row(*args, **kwargs)


def load_report_rows(*args: Any, **kwargs: Any) -> Any:
    """Load report rows through the runtime boundary."""
    return _report_panel_runtime()._load_report_rows(*args, **kwargs)


def refresh_review_summary(*args: Any, **kwargs: Any) -> Any:
    """Refresh the Tab 3 review summary."""
    return _report_panel_runtime()._refresh_review_summary(*args, **kwargs)


def row_needs_review(*args: Any, **kwargs: Any) -> Any:
    """Return whether a report row needs manual review."""
    return _report_panel_runtime()._row_needs_review(*args, **kwargs)


def matches_review_filter(*args: Any, **kwargs: Any) -> Any:
    """Return whether a report row matches the active review filter."""
    return _report_panel_runtime()._matches_review_filter(*args, **kwargs)


def populate_review_list(*args: Any, **kwargs: Any) -> Any:
    """Populate the Tab 3 review list."""
    return _report_panel_runtime()._populate_review_list(*args, **kwargs)


def show_review_item_details(*args: Any, **kwargs: Any) -> Any:
    """Show details for the selected review item."""
    return _report_panel_runtime()._show_review_item_details(*args, **kwargs)


def open_docstring_review_window(*args: Any, **kwargs: Any) -> Any:
    """Open the manual docstring review window."""
    return _report_panel_runtime()._open_docstring_review_window(*args, **kwargs)
