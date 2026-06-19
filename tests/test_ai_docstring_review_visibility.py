"""Tests for generated-docstring review visibility report fields."""

from __future__ import annotations

import unittest
from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting import (
    build_report_row,
    result_review_action_hint,
    result_review_severity,
    result_review_status,
)


class ReviewVisibilityReportFieldTests(unittest.TestCase):
    def test_insert_report_row_marks_clean_ai_output_for_review(self) -> None:
        row = build_report_row(
            Path("<PROJECT_ROOT>"),
            Path("<PROJECT_ROOT>/pkg/sample.py"),
            target_kind="function",
            target_name="build_sample",
            line=10,
            action="inserted",
            generation_source="ai",
            failure_reason="none",
            issues=[],
        )

        self.assertEqual(row["review_status"], "ready_for_review")
        self.assertEqual(row["review_severity"], "info")
        self.assertIn("Review AI-generated docstring", row["review_action_hint"])

    def test_insert_report_row_marks_fallback_for_careful_review(self) -> None:
        row = build_report_row(
            Path("<PROJECT_ROOT>"),
            Path("<PROJECT_ROOT>/pkg/sample.py"),
            target_kind="function",
            target_name="build_sample",
            line=10,
            action="inserted",
            generation_source="heuristic_fallback",
            failure_reason="quality_rejected",
            issues=["contains TODO placeholder"],
        )

        self.assertEqual(row["review_status"], "fallback_review_required")
        self.assertEqual(row["review_severity"], "warning")
        self.assertIn("fallback", row["review_action_hint"].lower())

    def test_review_helpers_work_with_generation_result_objects(self) -> None:
        result = SimpleNamespace(
            generation_source="heuristic_fallback",
            failure_reason="ai_call_failed",
            issues=["local AI unavailable"],
        )

        self.assertEqual(result_review_status(result), "fallback_review_required")
        self.assertEqual(result_review_severity(result), "warning")
        self.assertIn("AI output failed", result_review_action_hint(result))


if __name__ == "__main__":
    unittest.main()
