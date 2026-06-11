
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    CORRECTION_STATUS_REJECTED,
    CORRECTION_STATUS_REPAIRED,
    REVIEW_DECISION_EDITED,
    REVIEW_DECISION_REGENERATE_REQUESTED,
    REVIEW_SOURCE_AI,
    apply_correction_result,
    build_folder_review_state,
    create_correction_request,
    request_regeneration,
    request_rows_for_ai_retry,
    run_local_ai_correction,
)


class SafeModeLocalAiCorrectionLoopTests(unittest.TestCase):
    """Validate Safe Mode local-AI correction loop primitives."""

    def _state(self):
        rows = [
            {
                "file": "pkg/module.py",
                "target_kind": "function",
                "target_name": "normalize_payload",
                "insert_line": 12,
                "generation_source": "ai",
                "review_status": "quality_rejected",
                "review_severity": "warning",
                "failure_reason": "missing parameter description",
                "proposed_docstring": '"""Normalize data."""',
            }
        ]
        return build_folder_review_state("pkg", rows)

    def test_prompt_contains_evidence_and_anti_hallucination_rules(self) -> None:
        state = self._state()
        row = state.rows[0]

        request = create_correction_request(
            row,
            source_context="def normalize_payload(value: int) -> int:\n    return value",
            allowed_parameters=("value",),
            allowed_returns=("int",),
            allowed_raises=(),
        )

        self.assertIn("Use only evidence", request.prompt)
        self.assertIn("Do not invent", request.prompt)
        self.assertIn("normalize_payload", request.prompt)
        self.assertIn("- value", request.prompt)
        self.assertIn("- int", request.prompt)
        self.assertIn("Return only the corrected docstring.", request.prompt)

    def test_successful_ai_correction_becomes_edited_decision(self) -> None:
        state = self._state()
        row = state.rows[0]
        request = create_correction_request(
            row,
            source_context="def normalize_payload(value: int) -> int:\n    return value",
            allowed_parameters=("value",),
            allowed_returns=("int",),
        )

        def corrector(active_request):
            self.assertEqual(row.row_id, active_request.row.row_id)
            return '"""Return the normalized integer value.\n\nParameters:\n    value: Integer value to normalize.\n\nReturns:\n    Integer value after normalization.\n"""'

        result = run_local_ai_correction(request, corrector)
        state = apply_correction_result(state, result)

        self.assertTrue(result.success)
        self.assertEqual(CORRECTION_STATUS_REPAIRED, result.status)
        self.assertEqual(REVIEW_DECISION_EDITED, state.decisions[row.row_id].decision)
        self.assertEqual(REVIEW_SOURCE_AI, state.decisions[row.row_id].source)
        self.assertTrue(state.is_resolved())

    def test_rejected_ai_output_does_not_modify_review_state(self) -> None:
        state = self._state()
        row = state.rows[0]
        request = create_correction_request(row, source_context="def f():\n    pass")

        def corrector(_active_request):
            return '"""TODO: describe this later."""'

        result = run_local_ai_correction(request, corrector)
        updated = apply_correction_result(state, result)

        self.assertFalse(result.success)
        self.assertEqual(CORRECTION_STATUS_REJECTED, result.status)
        self.assertEqual({}, updated.decisions)
        self.assertFalse(updated.is_resolved())

    def test_requested_rows_for_ai_retry_uses_regenerate_decisions(self) -> None:
        state = self._state()
        row = state.rows[0]

        state = request_regeneration(state, row.row_id, "summary is weak")
        rows = request_rows_for_ai_retry(state)

        self.assertEqual(1, len(rows))
        self.assertEqual(row.row_id, rows[0].row_id)
        self.assertEqual(
            REVIEW_DECISION_REGENERATE_REQUESTED,
            state.decisions[row.row_id].decision,
        )


if __name__ == "__main__":
    unittest.main()
