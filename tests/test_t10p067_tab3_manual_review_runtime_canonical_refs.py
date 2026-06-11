"""Regression tests for T10P067 Tab 3 runtime canonical package references."""

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime"
LEGACY_TOKEN = 'ask_' 'ai_project_reasoner'
CANONICAL_TOKEN = "kanda_reasoner_app"


class Tab3ManualReviewRuntimeCanonicalRefsTests(unittest.TestCase):
    """Verify that the Tab 3 runtime owner box no longer pins the legacy package token."""

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        offenders = []
        for path in sorted(OWNER_ROOT.rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            if LEGACY_TOKEN in text:
                offenders.append(str(path.relative_to(PROJECT_ROOT)))
        self.assertEqual([], offenders)

    def test_runtime_imports_use_canonical_package_token(self) -> None:
        checked_files = [
            OWNER_ROOT / "ai_docstring_provider_runtime.py",
            OWNER_ROOT / "ai_docstring_row_bridge_runtime.py",
            OWNER_ROOT / "inline_corrector_runtime.py",
            OWNER_ROOT / "layout_runtime.py",
            OWNER_ROOT / "review_bulk_drafts_runtime.py",
            OWNER_ROOT / "scan_only_workflow.py",
        ]
        for path in checked_files:
            text = path.read_text(encoding="utf-8")
            self.assertIn(CANONICAL_TOKEN + ".tab3_manual_review_runtime", text)
            self.assertNotIn(LEGACY_TOKEN + ".tab3_manual_review_runtime", text)

    def test_insert_docstring_gui_cross_imports_are_canonical(self) -> None:
        checked_files = [
            OWNER_ROOT / "layout_runtime.py",
            OWNER_ROOT / "report_panel_runtime.py",
            OWNER_ROOT / "review_support.py",
        ]
        for path in checked_files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(LEGACY_TOKEN + ".insert_missing_docstrings_gui", text)
            self.assertIn(CANONICAL_TOKEN, text)


if __name__ == "__main__":
    unittest.main()
