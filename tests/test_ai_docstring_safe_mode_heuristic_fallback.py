
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    FALLBACK_STATUS_GENERATED,
    REVIEW_DECISION_EDITED,
    REVIEW_DECISION_FALLBACK_REQUESTED,
    REVIEW_SOURCE_HEURISTIC,
    apply_heuristic_fallback_result,
    build_folder_review_state,
    create_heuristic_fallback_request,
    generate_heuristic_fallback_docstring,
    request_fallback,
    request_rows_for_fallback_retry,
    run_heuristic_fallback,
)


class SafeModeHeuristicFallbackLoopTests(unittest.TestCase):
    """Validate Safe Mode heuristic fallback correction loop primitives."""

    def _state(self):
        rows = [
            {
                "file": "pkg/module.py",
                "target_kind": "function",
                "target_name": "normalize_payload",
                "insert_line": 12,
                "generation_source": "ai",
                "review_status": "fallback_review_required",
                "review_severity": "warning",
                "failure_reason": "local AI unavailable",
                "proposed_docstring": '"""Normalize data."""',
            }
        ]
        return build_folder_review_state("pkg", rows)

    def test_fallback_request_generates_evidence_limited_docstring(self) -> None:
        state = self._state()
        row = state.rows[0]

        request = create_heuristic_fallback_request(
            row,
            source_context="def normalize_payload(value: int) -> int:\n    return value",
            allowed_parameters=("value",),
            allowed_returns=("int",),
            allowed_raises=("ValueError",),
        )

        docstring = generate_heuristic_fallback_docstring(request)

        self.assertTrue(docstring.startswith(chr(34) * 3))
        self.assertIn("Run the normalize payload function.", docstring)
        self.assertIn("value: Parameter used by this function.", docstring)
        self.assertIn("int: Return value evidenced", docstring)
        self.assertIn("ValueError: Raised when", docstring)
        self.assertNotIn("TODO", docstring)

    def test_successful_fallback_becomes_heuristic_edited_decision(self) -> None:
        state = self._state()
        row = state.rows[0]
        request = create_heuristic_fallback_request(
            row,
            allowed_parameters=("value",),
            allowed_returns=("int",),
        )

        result = run_heuristic_fallback(request)
        updated = apply_heuristic_fallback_result(state, result)

        self.assertTrue(result.success)
        self.assertEqual(FALLBACK_STATUS_GENERATED, result.status)
        self.assertEqual(REVIEW_DECISION_EDITED, updated.decisions[row.row_id].decision)
        self.assertEqual(REVIEW_SOURCE_HEURISTIC, updated.decisions[row.row_id].source)
        self.assertTrue(updated.is_resolved())

    def test_requested_rows_for_fallback_retry_uses_fallback_decisions(self) -> None:
        state = self._state()
        row = state.rows[0]

        state = request_fallback(state, row.row_id, "local AI unavailable")
        rows = request_rows_for_fallback_retry(state)

        self.assertEqual(1, len(rows))
        self.assertEqual(row.row_id, rows[0].row_id)
        self.assertEqual(
            REVIEW_DECISION_FALLBACK_REQUESTED,
            state.decisions[row.row_id].decision,
        )


if __name__ == "__main__":
    unittest.main()
