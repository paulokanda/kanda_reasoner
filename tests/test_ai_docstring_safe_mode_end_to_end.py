
from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    FOLDER_STATE_APPLIED_CLEAN,
    FolderQueueItem,
    GuidedFolderSession,
    accept_docstring,
    apply_correction_result,
    apply_heuristic_fallback_result,
    apply_plan_with_validation,
    build_folder_apply_gate,
    build_folder_review_state,
    build_safe_mode_gui_snapshot,
    create_correction_request,
    create_guided_session,
    create_heuristic_fallback_request,
    preflight_folder,
    request_fallback,
    request_regeneration,
    run_heuristic_fallback,
    run_local_ai_correction,
)


class SafeModeEndToEndStressTests(unittest.TestCase):
    """Validate Safe Mode behavior over a fake multi-folder project."""

    def test_multi_folder_accept_ai_fallback_apply_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_function(root, "alpha", "module_a.py", "alpha")
            self._write_function(root, "beta", "module_b.py", "beta")
            self._write_function(root, "gamma", "module_c.py", "gamma")

            session = create_guided_session(root)
            self.assertEqual(3, len(session.folder_queue))
            self.assertFalse(session.can_continue_to_next_folder())

            session = replace(session, current_index=self._index_for(session, "alpha"))
            alpha_item = session.current_folder()
            alpha_preflight = preflight_folder(root, alpha_item)
            self.assertGreaterEqual(alpha_preflight.total_missing_docstrings, 1)

            alpha_state = build_folder_review_state(
                "alpha",
                [
                    self._row("alpha/module_a.py", "function", "alpha", 2, '"""Return alpha."""')
                ],
            )
            alpha_state = accept_docstring(alpha_state, alpha_state.rows[0].row_id)
            alpha_gate = build_folder_apply_gate(alpha_state)
            alpha_result = apply_plan_with_validation(root, alpha_gate.plan)
            self.assertTrue(alpha_result.success)
            self.assertEqual(
                "Return alpha.",
                self._function_docstring(root / "alpha" / "module_a.py", "alpha"),
            )
            session = self._mark_folder_applied(session, "alpha")

            session = replace(session, current_index=self._index_for(session, "beta"))
            beta_state = build_folder_review_state(
                "beta",
                [
                    self._row("beta/module_b.py", "function", "beta", 2, '"""Beta."""')
                ],
            )
            beta_row = beta_state.rows[0]
            beta_state = request_regeneration(beta_state, beta_row.row_id, "summary is weak")
            beta_request = create_correction_request(
                beta_row,
                source_context="def beta(value):\n    return value",
                allowed_parameters=("value",),
                allowed_returns=("value",),
            )

            def beta_corrector(_request):
                return '"""Return beta.\n\nParameters:\n    value: Value passed to beta.\n\nReturns:\n    Value passed to beta.\n"""'

            beta_correction = run_local_ai_correction(beta_request, beta_corrector)
            beta_state = apply_correction_result(beta_state, beta_correction)
            beta_gate = build_folder_apply_gate(beta_state)
            beta_result = apply_plan_with_validation(root, beta_gate.plan)
            self.assertTrue(beta_result.success)
            self.assertIn(
                "Return beta.",
                self._function_docstring(root / "beta" / "module_b.py", "beta"),
            )
            session = self._mark_folder_applied(session, "beta")

            session = replace(session, current_index=self._index_for(session, "gamma"))
            gamma_state = build_folder_review_state(
                "gamma",
                [
                    self._row("gamma/module_c.py", "function", "gamma", 2, '"""Gamma."""')
                ],
            )
            gamma_row = gamma_state.rows[0]
            gamma_state = request_fallback(gamma_state, gamma_row.row_id, "local AI unavailable")
            gamma_request = create_heuristic_fallback_request(
                gamma_row,
                allowed_parameters=("value",),
                allowed_returns=("value",),
            )
            gamma_fallback = run_heuristic_fallback(gamma_request)
            gamma_state = apply_heuristic_fallback_result(gamma_state, gamma_fallback)
            gamma_gate = build_folder_apply_gate(gamma_state)
            gamma_result = apply_plan_with_validation(root, gamma_gate.plan)
            self.assertTrue(gamma_result.success)
            self.assertIn(
                "Run the gamma function.",
                self._function_docstring(root / "gamma" / "module_c.py", "gamma"),
            )
            session = self._mark_folder_applied(session, "gamma")

            self.assertTrue(all(item.is_resolved() for item in session.folder_queue))

    def test_failed_folder_apply_rolls_back_without_touching_later_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_function(root, "alpha", "module_a.py", "alpha")
            self._write_function(root, "beta", "module_b.py", "beta")

            alpha_path = root / "alpha" / "module_a.py"
            beta_path = root / "beta" / "module_b.py"
            alpha_original = alpha_path.read_text(encoding="utf-8")
            beta_original = beta_path.read_text(encoding="utf-8")

            state = build_folder_review_state(
                "alpha",
                [
                    self._row("alpha/module_a.py", "function", "alpha", 1, '"""Return alpha."""')
                ],
            )
            state = accept_docstring(state, state.rows[0].row_id)
            gate = build_folder_apply_gate(state)

            result = apply_plan_with_validation(root, gate.plan)

            self.assertFalse(result.success)
            self.assertTrue(result.rollback_performed)
            self.assertEqual(alpha_original, alpha_path.read_text(encoding="utf-8"))
            self.assertEqual(beta_original, beta_path.read_text(encoding="utf-8"))

    def test_gui_snapshot_tracks_pending_and_apply_ready_states(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            self._write_function(root, "alpha", "module_a.py", "alpha")
            session = create_guided_session(root)

            state = build_folder_review_state(
                "alpha",
                [
                    self._row("alpha/module_a.py", "function", "alpha", 2, '"""Return alpha."""')
                ],
            )

            pending_snapshot = build_safe_mode_gui_snapshot(session, state)
            self.assertEqual(1, pending_snapshot.pending_count)
            self.assertFalse(pending_snapshot.can_apply_folder)

            state = accept_docstring(state, state.rows[0].row_id)
            ready_snapshot = build_safe_mode_gui_snapshot(session, state)
            self.assertEqual(0, ready_snapshot.pending_count)
            self.assertTrue(ready_snapshot.can_apply_folder)

            gate = build_folder_apply_gate(state)
            result = apply_plan_with_validation(root, gate.plan)
            self.assertTrue(result.success)

            session = self._mark_folder_applied(session, "alpha")
            resolved_snapshot = build_safe_mode_gui_snapshot(session, state)
            self.assertTrue(resolved_snapshot.can_continue_to_next_folder)

    def _write_function(
        self,
        root: Path,
        folder_name: str,
        file_name: str,
        function_name: str,
    ) -> None:
        folder = root / folder_name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / file_name).write_text(
            f"def {function_name}(value):\n"
            "    return value\n",
            encoding="utf-8",
        )

    def _row(
        self,
        file_path: str,
        target_kind: str,
        target_name: str,
        insert_line: int,
        proposed_docstring: str,
    ) -> dict[str, object]:
        return {
            "file": file_path,
            "target_kind": target_kind,
            "target_name": target_name,
            "insert_line": insert_line,
            "generation_source": "ai",
            "review_status": "ready_for_review",
            "review_severity": "info",
            "proposed_docstring": proposed_docstring,
        }

    def _index_for(self, session: GuidedFolderSession, folder_name: str) -> int:
        for index, item in enumerate(session.folder_queue):
            if item.relative_path == folder_name:
                return index
        raise AssertionError(f"Folder was not discovered: {folder_name}")

    def _mark_folder_applied(
        self,
        session: GuidedFolderSession,
        folder_name: str,
    ) -> GuidedFolderSession:
        index = self._index_for(session, folder_name)
        items = list(session.folder_queue)
        old_item = items[index]
        items[index] = FolderQueueItem(
            relative_path=old_item.relative_path,
            python_files=old_item.python_files,
            state=FOLDER_STATE_APPLIED_CLEAN,
            error="",
        )
        return GuidedFolderSession(
            project_root=session.project_root,
            folder_queue=tuple(items),
            current_index=index,
            settings=session.settings,
            last_report_path=session.last_report_path,
        )

    def _function_docstring(self, path: Path, function_name: str) -> str:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                value = ast.get_docstring(node)
                if value is None:
                    raise AssertionError(f"Function has no docstring: {function_name}")
                return value
        raise AssertionError(f"Function not found: {function_name}")


if __name__ == "__main__":
    unittest.main()
