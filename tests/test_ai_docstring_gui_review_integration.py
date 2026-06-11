"""Tests for Tab 3 GUI review-field integration."""

from __future__ import annotations

import sys
import types
import unittest


def _install_pyside_stubs_if_needed() -> None:
    """Install minimal PySide stubs when PySide6 is unavailable."""
    try:
        import PySide6  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    pyside = types.ModuleType("PySide6")
    qt_core = types.ModuleType("PySide6.QtCore")
    qt_widgets = types.ModuleType("PySide6.QtWidgets")

    class _ItemDataRole:
        UserRole = "UserRole"

    class _Qt:
        ItemDataRole = _ItemDataRole

    class _QListWidgetItem:
        def __init__(self, text: str = "") -> None:
            self.text = text
            self.data_by_role = {}

        def setData(self, role: object, value: object) -> None:
            self.data_by_role[role] = value

        def data(self, role: object) -> object:
            return self.data_by_role.get(role)

    qt_core.Qt = _Qt
    qt_widgets.QListWidgetItem = _QListWidgetItem
    sys.modules.setdefault("PySide6", pyside)
    sys.modules.setdefault("PySide6.QtCore", qt_core)
    sys.modules.setdefault("PySide6.QtWidgets", qt_widgets)


_install_pyside_stubs_if_needed()

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel import (  # noqa: E501
    matches_review_filter,
    refresh_review_summary,
    review_action_hint_for_row,
    review_severity_for_row,
    review_status_for_row,
    row_needs_review,
)


class _FakeCombo:
    def __init__(self, text: str) -> None:
        self._text = text

    def currentText(self) -> str:
        return self._text


class _FakeLabel:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, text: str) -> None:
        self.text = text


class _FakeView:
    def __init__(self, mode: str = "Needs review") -> None:
        self._review_filter_combo = _FakeCombo(mode)
        self._review_summary = _FakeLabel()
        self._report_rows = []

    def _row_needs_review(self, row: dict) -> bool:
        return row_needs_review(self, row)


class GuiReviewVisibilityIntegrationTests(unittest.TestCase):
    def test_review_status_helpers_use_explicit_report_fields(self) -> None:
        row = {
            "review_status": "fallback_review_required",
            "review_severity": "warning",
            "review_action_hint": "Review fallback output before insertion.",
        }

        self.assertEqual(review_status_for_row(row), "fallback_review_required")
        self.assertEqual(review_severity_for_row(row), "warning")
        self.assertIn("fallback", review_action_hint_for_row(row).lower())

    def test_row_needs_review_uses_new_review_status_and_severity(self) -> None:
        view = _FakeView()
        fallback_row = {
            "action": "inserted",
            "review_status": "fallback_review_required",
            "review_severity": "warning",
        }
        clean_row = {
            "action": "inserted",
            "review_status": "ready_for_review",
            "review_severity": "info",
        }

        self.assertTrue(row_needs_review(view, fallback_row))
        self.assertFalse(row_needs_review(view, clean_row))

    def test_review_filter_modes_use_new_review_statuses(self) -> None:
        fallback_view = _FakeView("Fallback review")
        blocked_view = _FakeView("Blocked/rejected")
        ready_view = _FakeView("Ready for review")

        fallback_row = {"review_status": "fallback_review_required"}
        blocked_row = {"review_status": "blocked_or_rejected"}
        ready_row = {"review_status": "ready_for_review"}

        self.assertTrue(matches_review_filter(fallback_view, fallback_row))
        self.assertFalse(matches_review_filter(fallback_view, ready_row))
        self.assertTrue(matches_review_filter(blocked_view, blocked_row))
        self.assertTrue(matches_review_filter(ready_view, ready_row))

    def test_review_summary_surfaces_status_and_severity_counts(self) -> None:
        view = _FakeView()
        view._report_rows = [
            {"action": "inserted", "target_kind": "function", "review_status": "ready_for_review"},
            {"action": "inserted", "target_kind": "function", "review_status": "fallback_review_required"},
            {"action": "failed", "target_kind": "method", "review_status": "blocked_or_rejected"},
        ]

        refresh_review_summary(view)

        self.assertIn("Review status:", view._review_summary.text)
        self.assertIn("fallback_review_required=1", view._review_summary.text)
        self.assertIn("Severity:", view._review_summary.text)


if __name__ == "__main__":
    unittest.main()
