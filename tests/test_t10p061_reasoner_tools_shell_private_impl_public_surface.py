"""Regression tests for T10P061 reasoner tools shell public surface."""

from __future__ import annotations

from pathlib import Path
import ast
import unittest


class ReasonerToolsShellPrivateImplPublicSurfaceTests(unittest.TestCase):
    """Verify private helper implementation declares an explicit public surface."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.target = (
            cls.project_root
            / 'ask_' 'ai_project_reasoner'
            / "reasoner_tools_shell"
            / "runner_help"
            / "window_process_private_impl.py"
        )

    def test_private_impl_declares_empty_all(self) -> None:
        module = ast.parse(self.target.read_text(encoding="utf-8"))
        assignments = [
            node
            for node in module.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "__all__"
                for target in node.targets
            )
        ]
        self.assertEqual(len(assignments), 1)
        value = assignments[0].value
        self.assertIsInstance(value, ast.Tuple)
        self.assertEqual(len(value.elts), 0)

    def test_window_process_helper_remains_under_manifest_line_limit(self) -> None:
        text = self.target.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 499)


if __name__ == "__main__":
    unittest.main()
