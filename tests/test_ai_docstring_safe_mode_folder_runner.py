
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    FolderRunResult,
    FolderRunSettings,
    create_folder_run_plan,
    create_guided_session,
    preflight_folder,
    run_folder_with_backend,
)


class SafeModeFolderScopedRunnerTests(unittest.TestCase):
    """Validate Safe Mode folder-scoped runner primitives."""

    def test_preflight_counts_only_selected_folder_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "alpha").mkdir()
            (root / "beta").mkdir()

            (root / "alpha" / "module_a.py").write_text(
                "\n".join(
                    [
                        "from typing import overload",
                        "",
                        "",
                        "class Alpha:",
                        "    def method(self) -> int:",
                        "        return 1",
                        "",
                        "",
                        "def public_function(value: int) -> int:",
                        "    return value",
                        "",
                        "",
                        "def outer(func):",
                        "    def wrapper(*args, **kwargs):",
                        "        return func(*args, **kwargs)",
                        "    return wrapper",
                        "",
                        "",
                        "@overload",
                        "def parse_value(raw: int) -> int:",
                        "    ...",
                        "",
                        "",
                        "def parse_value(raw: int) -> int:",
                        "    return raw",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            (root / "beta" / "module_b.py").write_text(
                "def beta_function() -> None:\n    return None\n",
                encoding="utf-8",
            )

            session = create_guided_session(root)
            alpha_index = [
                item.relative_path for item in session.folder_queue
            ].index("alpha")
            item = session.folder_queue[alpha_index]

            preflight = preflight_folder(root, item, FolderRunSettings(include_init=True))

            self.assertEqual("alpha", preflight.folder_relative_path)
            self.assertEqual(1, preflight.files_parsed)
            self.assertEqual(0, len(preflight.files_with_syntax_errors))
            self.assertEqual(1, preflight.missing_module_docstrings)
            self.assertEqual(1, preflight.missing_class_docstrings)
            self.assertEqual(3, preflight.missing_function_docstrings)
            self.assertEqual(1, preflight.missing_method_docstrings)

    def test_run_plan_limits_backend_to_selected_folder_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "alpha").mkdir()
            (root / "beta").mkdir()
            (root / "alpha" / "module_a.py").write_text("def a() -> None:\n    pass\n", encoding="utf-8")
            (root / "beta" / "module_b.py").write_text("def b() -> None:\n    pass\n", encoding="utf-8")

            session = create_guided_session(root)
            alpha_index = [
                item.relative_path for item in session.folder_queue
            ].index("alpha")

            plan = create_folder_run_plan(session, index=alpha_index)

            def backend(active_plan):
                return FolderRunResult(
                    success=True,
                    folder_relative_path=active_plan.folder_relative_path,
                    processed_files=active_plan.python_files,
                    report_path=active_plan.report_path,
                    message="ok",
                    row_count=len(active_plan.python_files),
                )

            result = run_folder_with_backend(plan, backend)

            self.assertTrue(result.success)
            self.assertEqual(("alpha/module_a.py",), result.processed_files)
            self.assertIn(".docstring_safe_mode_alpha.jsonl", result.report_path)

    def test_backend_cannot_process_files_outside_selected_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "alpha").mkdir()
            (root / "beta").mkdir()
            (root / "alpha" / "module_a.py").write_text("def a() -> None:\n    pass\n", encoding="utf-8")
            (root / "beta" / "module_b.py").write_text("def b() -> None:\n    pass\n", encoding="utf-8")

            session = create_guided_session(root)
            alpha_index = [
                item.relative_path for item in session.folder_queue
            ].index("alpha")
            plan = create_folder_run_plan(session, index=alpha_index)

            def unsafe_backend(active_plan):
                return FolderRunResult(
                    success=True,
                    folder_relative_path=active_plan.folder_relative_path,
                    processed_files=("alpha/module_a.py", "beta/module_b.py"),
                    report_path=active_plan.report_path,
                )

            with self.assertRaises(ValueError):
                run_folder_with_backend(plan, unsafe_backend)


if __name__ == "__main__":
    unittest.main()
