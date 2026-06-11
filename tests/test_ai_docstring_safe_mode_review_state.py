
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    REVIEW_DECISION_ACCEPTED,
    REVIEW_DECISION_EDITED,
    REVIEW_DECISION_FALLBACK_REQUESTED,
    REVIEW_DECISION_REGENERATE_REQUESTED,
    REVIEW_DECISION_REJECTED,
    REVIEW_DECISION_SKIPPED,
    REVIEW_SOURCE_MANUAL_EDIT,
    accept_docstring,
    build_folder_review_state,
    clear_decision,
    edit_docstring,
    reject_docstring,
    request_fallback,
    request_regeneration,
    skip_docstring,
)


class SafeModeReviewStateTests(unittest.TestCase):
    """Validate per-docstring Safe Mode review state transitions."""

    def _build_state(self):
        rows = [
            {
                "file": "pkg/module.py",
                "target_kind": "function",
                "target_name": "alpha",
                "insert_line": 10,
                "generation_source": "ai",
                "review_status": "ready_for_review",
                "review_severity": "info",
                "review_action_hint": "review",
                "proposed_docstring": '"""Return alpha."""',
            },
            {
                "file": "pkg/module.py",
                "target_kind": "function",
                "target_name": "beta",
                "insert_line": 20,
                "generation_source": "heuristic",
                "review_status": "fallback_review_required",
                "review_severity": "warning",
                "failure_reason": "ai_call_failed",
                "proposed_docstring": '"""Return beta."""',
            },
        ]
        return build_folder_review_state("pkg", rows)

    def test_build_review_state_from_report_rows(self) -> None:
        state = self._build_state()

        self.assertEqual("pkg", state.folder_relative_path)
        self.assertEqual(2, len(state.rows))
        self.assertEqual(2, state.unresolved_count())
        self.assertFalse(state.is_resolved())
        self.assertEqual("alpha", state.rows[0].target_name)
        self.assertEqual('"""Return alpha."""', state.rows[0].proposed_docstring)

    def test_accept_and_edit_resolve_rows(self) -> None:
        state = self._build_state()
        first_id = state.rows[0].row_id
        second_id = state.rows[1].row_id

        state = accept_docstring(state, first_id)
        state = edit_docstring(state, second_id, '"""Return edited beta."""')

        self.assertTrue(state.is_resolved())
        accepted = state.accepted_docstrings()
        self.assertEqual(2, len(accepted))
        decisions = {item.row_id: item for item in accepted}
        self.assertEqual(REVIEW_DECISION_ACCEPTED, decisions[first_id].decision)
        self.assertEqual(REVIEW_DECISION_EDITED, decisions[second_id].decision)
        self.assertEqual(REVIEW_SOURCE_MANUAL_EDIT, decisions[second_id].source)

    def test_regenerate_and_fallback_requests_are_not_final(self) -> None:
        state = self._build_state()
        first_id = state.rows[0].row_id
        second_id = state.rows[1].row_id

        state = request_regeneration(state, first_id, "summary is weak")
        state = request_fallback(state, second_id, "local AI unavailable")

        self.assertFalse(state.is_resolved())
        self.assertEqual(2, state.unresolved_count())
        self.assertEqual(REVIEW_DECISION_REGENERATE_REQUESTED, state.decisions[first_id].decision)
        self.assertEqual(REVIEW_DECISION_FALLBACK_REQUESTED, state.decisions[second_id].decision)
        self.assertTrue(state.decisions[first_id].needs_ai_retry())
        self.assertTrue(state.decisions[second_id].needs_ai_retry())

    def test_skip_and_reject_resolve_rows_without_acceptance(self) -> None:
        state = self._build_state()
        first_id = state.rows[0].row_id
        second_id = state.rows[1].row_id

        state = skip_docstring(state, first_id, "not needed")
        state = reject_docstring(state, second_id, "unsupported claim")

        self.assertTrue(state.is_resolved())
        skipped = state.skipped_or_rejected()
        self.assertEqual(2, len(skipped))

        decisions = {item.row_id: item for item in skipped}
        self.assertEqual(REVIEW_DECISION_SKIPPED, decisions[first_id].decision)
        self.assertEqual(REVIEW_DECISION_REJECTED, decisions[second_id].decision)
        self.assertEqual((), state.accepted_docstrings())

    def test_clear_decision_reopens_row(self) -> None:
        state = self._build_state()
        first_id = state.rows[0].row_id

        state = accept_docstring(state, first_id)
        self.assertEqual(1, state.unresolved_count())

        state = clear_decision(state, first_id)
        self.assertEqual(2, state.unresolved_count())


if __name__ == "__main__":
    unittest.main()
