"""Compatibility facade for Tab 3 review support helpers."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _apply_saved_manual_review_state as apply_saved_manual_review_state
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _backup_source_file as backup_source_file
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _classify_location_after_tab1_refresh as classify_location_after_tab1_refresh
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _docstring_text_from_row as docstring_text_from_row
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _docstring_text_or_placeholder as docstring_text_or_placeholder
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _format_review_row_context as format_review_row_context
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _format_tab1_findings_for_editor as format_tab1_findings_for_editor
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _format_tab1_snippets as format_tab1_snippets
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _manual_review_is_inside_project_root as manual_review_is_inside_project_root
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _project_root_for_owner as project_root_for_window
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _refresh_tab1_findings_for_owner as refresh_tab1_findings_for_window
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _manual_review_safe_int as manual_review_safe_int
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _manual_review_state_summary_text as manual_review_state_summary_text
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _next_filtered_location_index as next_filtered_location_index
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _review_location_matches_state_filter as review_location_matches_state_filter
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import _save_manual_review_state as save_manual_review_state

__all__ = [
    "apply_saved_manual_review_state",
    "backup_source_file",
    "classify_location_after_tab1_refresh",
    "docstring_text_from_row",
    "docstring_text_or_placeholder",
    "format_review_row_context",
    "format_tab1_findings_for_editor",
    "format_tab1_snippets",
    "manual_review_is_inside_project_root",
    "project_root_for_window",
    "refresh_tab1_findings_for_window",
    "manual_review_safe_int",
    "manual_review_state_summary_text",
    "next_filtered_location_index",
    "review_location_matches_state_filter",
    "save_manual_review_state",
]
