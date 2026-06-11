"""Regression tests for T10P060 reasoner tools shell migration."""

from __future__ import annotations

from pathlib import Path
import unittest


class ReasonerToolsShellCanonicalPythonRefsTests(unittest.TestCase):
    """Verify reasoner_tools_shell Python files do not hard-code legacy tokens."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.owner_root = cls.project_root / "kanda_reasoner_app" / "reasoner_tools_shell"
        cls.legacy_token = "_".join(("ask", "ai", "project", "reasoner"))
        cls.canonical_token = "kanda_reasoner_app"

    def _read(self, relative_path: str) -> str:
        return (self.owner_root / relative_path).read_text(encoding="utf-8")

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        for path in sorted(self.owner_root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            with self.subTest(path=str(path.relative_to(self.project_root))):
                self.assertNotIn(self.legacy_token, path.read_text(encoding="utf-8"))

    def test_runner_uses_canonical_payload_loader_import(self) -> None:
        text = self._read("runner.py")
        self.assertIn(
            "from kanda_reasoner_app.backend_payloads.loader import load_payload",
            text,
        )

    def test_child_module_commands_use_canonical_module_paths(self) -> None:
        process_text = self._read("runner_help/window_process_private_impl.py")
        zip_text = self._read("runner_help/zip_json_files_private_impl.py")
        self.assertIn(
            'CANONICAL_PACKAGE_NAME + ".reasoner_context_collector.complete_json_web_ai_enrichment"',
            process_text,
        )
        self.assertIn('CANONICAL_PACKAGE_NAME + ".reasoner_context_bundle"', process_text)
        self.assertIn(
            '"kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter"',
            zip_text,
        )

    def test_staged_physical_paths_are_dynamic_not_literal_legacy_paths(self) -> None:
        process_text = self._read("runner_help/window_process_private_impl.py")
        guard_text = self._read("tab4_scope_guard.py")
        validator_text = self._read("runner_validate_manifests.py")
        self.assertIn("_installed_package_dir(_tab4_tool_root())", process_text)
        self.assertIn("_installed_package_dir(root)", guard_text)
        self.assertIn("BASE = Path(__file__).resolve().parent", validator_text)

    def test_window_process_helper_remains_under_manifest_line_limit(self) -> None:
        text = self._read("runner_help/window_process_private_impl.py")
        line_count = len(text.splitlines())
        self.assertLessEqual(line_count, 499)


if __name__ == "__main__":
    unittest.main()
