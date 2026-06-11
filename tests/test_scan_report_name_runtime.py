"""Public-contract tests for Tab 3 scan report naming helpers."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.scan_report_name_runtime import (
    REPORT_DATE_FORMAT,
    build_project_missing_docstrings_report_name,
)


def test_build_project_missing_docstrings_report_name_uses_safe_slug() -> None:
    """Project names should become safe timestamped JSONL report names."""
    report_name = build_project_missing_docstrings_report_name(
        Path("My Fake Project"),
        "20260606_160405",
    )

    assert report_name == "my_fake_project_missing_docstrings_20260606_160405.jsonl"


def test_report_date_format_matches_expected_filename_timestamp() -> None:
    """Timestamp format should remain compact and Windows filename safe."""
    assert REPORT_DATE_FORMAT == "%Y%m%d_%H%M%S"


if __name__ == "__main__":
    test_build_project_missing_docstrings_report_name_uses_safe_slug()
    test_report_date_format_matches_expected_filename_timestamp()
    print("scan_report_name_runtime public contract tests passed.")
