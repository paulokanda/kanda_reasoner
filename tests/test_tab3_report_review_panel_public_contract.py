"""Public-contract test for Tab 3 report review panel facade."""

from __future__ import annotations

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel import (
    __all__ as REPORT_REVIEW_PANEL_PUBLIC_API,
    load_report_rows,
    matches_review_filter,
    open_docstring_review_window,
    populate_review_list,
    refresh_review_summary,
    review_action_hint_for_row,
    review_severity_for_row,
    review_status_for_row,
    row_needs_review,
    show_review_item_details,
)


def test_report_review_panel_public_contract_imports() -> None:
    """Verify Tab 3 report review facade public symbols remain importable."""
    imported = {
        "load_report_rows": load_report_rows,
        "matches_review_filter": matches_review_filter,
        "open_docstring_review_window": open_docstring_review_window,
        "populate_review_list": populate_review_list,
        "refresh_review_summary": refresh_review_summary,
        "review_action_hint_for_row": review_action_hint_for_row,
        "review_severity_for_row": review_severity_for_row,
        "review_status_for_row": review_status_for_row,
        "row_needs_review": row_needs_review,
        "show_review_item_details": show_review_item_details,
    }
    assert sorted(imported) == sorted(REPORT_REVIEW_PANEL_PUBLIC_API)
    for value in imported.values():
        assert callable(value)


def main() -> int:
    """Run Tab 3 report review panel public-contract test without pytest."""
    test_report_review_panel_public_contract_imports()
    print("Tab 3 report review panel public contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
