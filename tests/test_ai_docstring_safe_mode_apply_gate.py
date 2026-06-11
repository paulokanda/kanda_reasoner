
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    APPLY_GATE_STATUS_BLOCKED,
    APPLY_GATE_STATUS_EMPTY,
    APPLY_GATE_STATUS_READY,
    accept_docstring,
    approved_file_paths,
    build_folder_apply_gate,
    build_folder_review_state,
    edit_docstring,
    reject_docstring,
    skip_docstring,
    summarize_folder_apply_plan,
)


class SafeModeFolderApplyGateTests(unittest.TestCase):
    """Validate Safe Mode folder apply-gate behavior."""

    def _state(self):
        rows = [
            {
                "file": "pkg/module.py",
                "target_kind": "function",
                "target_name": "alpha",
                "insert_line": 10,
                "generation_source": "ai",
                "review_status": "ready_for_review",
                "review_severity": "info",
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
                "proposed_docstring": '"""Return beta."""',
            },
            {
                "file": "pkg/skip_me.py",
                "target_kind": "function",
                "target_name": "skip_me",
                "insert_line": 30,
                "generation_source": "ai",
                "review_status": "ready_for_review",
                "review_severity": "info",
                "proposed_docstring": '"""Skip me."""',
            },
        ]
        return build_folder_review_state("pkg", rows)

    def test_unresolved_rows_block_apply_gate(self) -> None:
        state = self._state()

        result = build_folder_apply_gate(state)

        self.assertFalse(result.success)
        self.assertEqual(APPLY_GATE_STATUS_BLOCKED, result.status)
        self.assertEqual(3, len(result.blocked_row_ids))

    def test_accepted_and_edited_rows_create_apply_plan(self) -> None:
        state = self._state()
        first_id = state.rows[0].row_id
        second_id = state.rows[1].row_id
        third_id = state.rows[2].row_id

        state = accept_docstring(state, first_id)
        state = edit_docstring(state, second_id, '"""Return edited beta."""')
        state = skip_docstring(state, third_id, "not needed")

        result = build_folder_apply_gate(state)

        self.assertTrue(result.success)
        self.assertEqual(APPLY_GATE_STATUS_READY, result.status)
        self.assertIsNotNone(result.plan)
        self.assertEqual(2, len(result.plan.patches))
        self.assertEqual((third_id,), result.plan.skipped_row_ids)
        self.assertEqual(("pkg/module.py",), approved_file_paths(result.plan))

        summary = summarize_folder_apply_plan(result.plan)
        self.assertEqual(2, summary["approved_patch_count"])
        self.assertEqual(1, summary["skipped_count"])

    def test_invalid_approved_docstring_blocks_gate(self) -> None:
        state = self._state()
        first_id = state.rows[0].row_id
        second_id = state.rows[1].row_id
        third_id = state.rows[2].row_id

        state = edit_docstring(state, first_id, '"""TODO: fill later."""')
        state = skip_docstring(state, second_id)
        state = skip_docstring(state, third_id)

        result = build_folder_apply_gate(state)

        self.assertFalse(result.success)
        self.assertEqual(APPLY_GATE_STATUS_BLOCKED, result.status)
        self.assertEqual((first_id,), result.blocked_row_ids)
        self.assertIn("forbidden marker", result.error)

    def test_rejected_and_skipped_only_rows_create_empty_plan(self) -> None:
        state = self._state()
        first_id = state.rows[0].row_id
        second_id = state.rows[1].row_id
        third_id = state.rows[2].row_id

        state = reject_docstring(state, first_id, "unsupported")
        state = skip_docstring(state, second_id)
        state = skip_docstring(state, third_id)

        result = build_folder_apply_gate(state)

        self.assertTrue(result.success)
        self.assertEqual(APPLY_GATE_STATUS_EMPTY, result.status)
        self.assertIsNotNone(result.plan)
        self.assertEqual(0, len(result.plan.patches))
        self.assertEqual((second_id, third_id), result.plan.skipped_row_ids)
        self.assertEqual((first_id,), result.plan.rejected_row_ids)

    def test_row_outside_folder_blocks_gate(self) -> None:
        rows = [
            {
                "file": "other/module.py",
                "target_kind": "function",
                "target_name": "alpha",
                "insert_line": 10,
                "generation_source": "ai",
                "review_status": "ready_for_review",
                "review_severity": "info",
                "proposed_docstring": '"""Return alpha."""',
            }
        ]
        state = build_folder_review_state("pkg", rows)
        state = accept_docstring(state, state.rows[0].row_id)

        result = build_folder_apply_gate(state)

        self.assertFalse(result.success)
        self.assertEqual(APPLY_GATE_STATUS_BLOCKED, result.status)
        self.assertIn("outside selected folder", result.error)


if __name__ == "__main__":
    unittest.main()
