
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    SAFE_MODE_ACTION_ACCEPT,
    SAFE_MODE_ACTION_CLEAR,
    SAFE_MODE_ACTION_EDIT,
    SAFE_MODE_ACTION_FALLBACK,
    SAFE_MODE_ACTION_REGENERATE,
    SAFE_MODE_ACTION_REJECT,
    SAFE_MODE_ACTION_SKIP,
    build_folder_review_state,
    build_safe_mode_button_state,
    build_safe_mode_gui_snapshot,
    create_guided_session,
    perform_safe_mode_review_action,
)


class SafeModeGuiBridgeIntegrationTests(unittest.TestCase):
    """Validate Safe Mode GUI bridge behavior without PySide coupling."""

    def _session_and_state(self):
        tmp_dir = tempfile.TemporaryDirectory()
        root = Path(tmp_dir.name)
        pkg = root / "pkg"
        pkg.mkdir()
        (pkg / "module.py").write_text("def alpha():\n    pass\n", encoding="utf-8")

        session = create_guided_session(root)
        state = build_folder_review_state(
            "pkg",
            [
                {
                    "file": "pkg/module.py",
                    "target_kind": "function",
                    "target_name": "alpha",
                    "insert_line": 2,
                    "generation_source": "ai",
                    "review_status": "ready_for_review",
                    "review_severity": "info",
                    "proposed_docstring": '"""Return alpha."""',
                }
            ],
        )
        return tmp_dir, session, state

    def test_snapshot_surfaces_current_folder_and_pending_count(self) -> None:
        tmp_dir, session, state = self._session_and_state()
        with tmp_dir:
            snapshot = build_safe_mode_gui_snapshot(session, state)

            self.assertEqual("pkg", snapshot.folder_relative_path)
            self.assertEqual(1, snapshot.total_folders)
            self.assertEqual(1, snapshot.python_file_count)
            self.assertEqual(1, snapshot.pending_count)
            self.assertFalse(snapshot.can_apply_folder)
            self.assertIn("pending", snapshot.status_message)

    def test_accept_action_updates_state_and_enables_apply(self) -> None:
        tmp_dir, session, state = self._session_and_state()
        with tmp_dir:
            row_id = state.rows[0].row_id

            action_result = perform_safe_mode_review_action(
                state,
                row_id,
                SAFE_MODE_ACTION_ACCEPT,
            )
            self.assertTrue(action_result.success)

            snapshot = build_safe_mode_gui_snapshot(session, action_result.state)
            buttons = build_safe_mode_button_state(session, action_result.state)

            self.assertEqual(0, snapshot.pending_count)
            self.assertEqual(1, snapshot.accepted_count)
            self.assertTrue(snapshot.can_apply_folder)
            self.assertTrue(buttons.can_apply_folder)

    def test_edit_skip_reject_clear_actions_are_gui_safe(self) -> None:
        tmp_dir, _session, state = self._session_and_state()
        with tmp_dir:
            row_id = state.rows[0].row_id

            edited = perform_safe_mode_review_action(
                state,
                row_id,
                SAFE_MODE_ACTION_EDIT,
                final_docstring='"""Return edited alpha."""',
            )
            self.assertTrue(edited.success)
            self.assertTrue(edited.state.is_resolved())

            cleared = perform_safe_mode_review_action(
                edited.state,
                row_id,
                SAFE_MODE_ACTION_CLEAR,
            )
            self.assertTrue(cleared.success)
            self.assertFalse(cleared.state.is_resolved())

            skipped = perform_safe_mode_review_action(
                cleared.state,
                row_id,
                SAFE_MODE_ACTION_SKIP,
                reason="not needed",
            )
            self.assertTrue(skipped.success)
            self.assertTrue(skipped.state.is_resolved())

            rejected = perform_safe_mode_review_action(
                cleared.state,
                row_id,
                SAFE_MODE_ACTION_REJECT,
                reason="unsupported",
            )
            self.assertTrue(rejected.success)
            self.assertTrue(rejected.state.is_resolved())

    def test_retry_actions_leave_rows_unresolved_for_followup_loops(self) -> None:
        tmp_dir, _session, state = self._session_and_state()
        with tmp_dir:
            row_id = state.rows[0].row_id

            regen = perform_safe_mode_review_action(
                state,
                row_id,
                SAFE_MODE_ACTION_REGENERATE,
                reason="summary is weak",
            )
            self.assertTrue(regen.success)
            self.assertFalse(regen.state.is_resolved())

            fallback = perform_safe_mode_review_action(
                state,
                row_id,
                SAFE_MODE_ACTION_FALLBACK,
                reason="local AI unavailable",
            )
            self.assertTrue(fallback.success)
            self.assertFalse(fallback.state.is_resolved())

    def test_unknown_action_returns_error_without_modifying_state(self) -> None:
        tmp_dir, _session, state = self._session_and_state()
        with tmp_dir:
            row_id = state.rows[0].row_id

            result = perform_safe_mode_review_action(state, row_id, "unknown-action")

            self.assertFalse(result.success)
            self.assertEqual(state, result.state)
            self.assertIn("Unknown Safe Mode action", result.error)


if __name__ == "__main__":
    unittest.main()
