"""Regression tests for T10P069 manifest and runtime public contracts."""

from __future__ import annotations

import ast
import subprocess
import sys
import unittest
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import export_summary
from kanda_reasoner_app.tab3_manual_review_runtime import heuristic_suggestion
from kanda_reasoner_app.tab3_manual_review_runtime import preview_summary

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui"
TAB3_ROOT = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime"
LEGACY_TOKEN = "_".join(("ask", "ai", "project", "reasoner"))


class InsertDocstringsManifestRuntimeContractsTests(unittest.TestCase):
    """Verify repaired manifest validators and explicit runtime contracts."""

    def _literal_all(self, path: Path) -> list[str] | None:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        return list(ast.literal_eval(node.value))
        return None

    def test_manifest_validators_accept_mixed_manifest_schemas(self) -> None:
        for script_name in (
            "insert_missing_docstrings_validate_manifests.py",
            "insert_missing_docstrings_gui_validate_manifests.py",
        ):
            result = subprocess.run(
                [sys.executable, str(OWNER_ROOT / script_name)],
                cwd=str(PROJECT_ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("PASS", result.stdout)

    def test_validators_do_not_pin_literal_legacy_package_token(self) -> None:
        for script_name in (
            "insert_missing_docstrings_validate_manifests.py",
            "insert_missing_docstrings_gui_validate_manifests.py",
        ):
            text = (OWNER_ROOT / script_name).read_text(encoding="utf-8")
            self.assertNotIn(LEGACY_TOKEN, text)
            self.assertIn("helper_folder", text)

    def test_tab3_helpers_have_direct_test_imports(self) -> None:
        self.assertTrue(hasattr(export_summary, "_export_manual_review_summary"))
        self.assertTrue(hasattr(heuristic_suggestion, "_suggest_manual_review_heuristic"))
        self.assertTrue(hasattr(preview_summary, "_build_approved_review_preview"))


if __name__ == "__main__":
    unittest.main()
