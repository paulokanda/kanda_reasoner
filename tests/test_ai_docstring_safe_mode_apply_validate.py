
from __future__ import annotations

import ast
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    APPLY_VALIDATION_STATUS_APPLIED,
    APPLY_VALIDATION_STATUS_EMPTY,
    APPLY_VALIDATION_STATUS_FAILED_ROLLED_BACK,
    accept_docstring,
    apply_plan_with_validation,
    build_folder_apply_gate,
    build_folder_review_state,
    skip_docstring,
    validate_changed_files,
)


class SafeModeApplyAndPostWriteValidationTests(unittest.TestCase):
    """Validate Safe Mode apply and post-write validation behavior."""

    def test_apply_plan_writes_function_docstring_and_validates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            pkg = root / "pkg"
            pkg.mkdir()
            target = pkg / "module.py"
            target.write_text(
                "def alpha(value):\n"
                "    return value\n",
                encoding="utf-8",
            )

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
            state = accept_docstring(state, state.rows[0].row_id)
            gate = build_folder_apply_gate(state)

            result = apply_plan_with_validation(root, gate.plan)

            self.assertTrue(result.success)
            self.assertEqual(APPLY_VALIDATION_STATUS_APPLIED, result.status)
            self.assertEqual(("pkg/module.py",), result.changed_files)

            tree = ast.parse(target.read_text(encoding="utf-8"))
            function_node = tree.body[0]
            self.assertEqual("Return alpha.", ast.get_docstring(function_node))

    def test_failed_post_write_validation_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            pkg = root / "pkg"
            pkg.mkdir()
            target = pkg / "module.py"
            original = (
                "def alpha(value):\n"
                "    return value\n"
            )
            target.write_text(original, encoding="utf-8")

            state = build_folder_review_state(
                "pkg",
                [
                    {
                        "file": "pkg/module.py",
                        "target_kind": "function",
                        "target_name": "alpha",
                        "insert_line": 1,
                        "generation_source": "ai",
                        "review_status": "ready_for_review",
                        "review_severity": "info",
                        "proposed_docstring": '"""Return alpha."""',
                    }
                ],
            )
            state = accept_docstring(state, state.rows[0].row_id)
            gate = build_folder_apply_gate(state)

            result = apply_plan_with_validation(root, gate.plan)

            self.assertFalse(result.success)
            self.assertEqual(APPLY_VALIDATION_STATUS_FAILED_ROLLED_BACK, result.status)
            self.assertTrue(result.rollback_performed)
            self.assertEqual(original, target.read_text(encoding="utf-8"))

    def test_empty_plan_validates_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            pkg = root / "pkg"
            pkg.mkdir()
            target = pkg / "module.py"
            original = "def alpha(value):\n    return value\n"
            target.write_text(original, encoding="utf-8")

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
            state = skip_docstring(state, state.rows[0].row_id)
            gate = build_folder_apply_gate(state)

            result = apply_plan_with_validation(root, gate.plan)

            self.assertTrue(result.success)
            self.assertEqual(APPLY_VALIDATION_STATUS_EMPTY, result.status)
            self.assertEqual(original, target.read_text(encoding="utf-8"))

    def test_validate_changed_files_detects_missing_applied_docstring(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            pkg = root / "pkg"
            pkg.mkdir()
            target = pkg / "module.py"
            target.write_text(
                "def alpha(value):\n"
                "    return value\n",
                encoding="utf-8",
            )

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
            state = accept_docstring(state, state.rows[0].row_id)
            gate = build_folder_apply_gate(state)

            result = validate_changed_files(root, gate.plan)

            self.assertFalse(result.success)
            self.assertIn("Docstring missing after apply", result.error)


if __name__ == "__main__":
    unittest.main()
