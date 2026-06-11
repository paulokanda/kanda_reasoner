"""Regression tests for T10P068 insert-missing-docstrings GUI migration."""

from __future__ import annotations

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OWNER_DIR = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui"
LEGACY_TOKEN = "_".join(("ask", "ai", "project", "reasoner"))
CANONICAL_TOKEN = "kanda_reasoner_app"


class InsertMissingDocstringsGuiCanonicalRefsTests(unittest.TestCase):
    """Verify that the owner box uses canonical package references."""

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        offenders = []
        for path in OWNER_DIR.rglob("*.py"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if LEGACY_TOKEN in text:
                offenders.append(str(path.relative_to(PROJECT_ROOT)))
        self.assertEqual([], offenders)

    def test_backend_payload_imports_use_canonical_package(self) -> None:
        files = [
            OWNER_DIR / "ai_docstring_generator.py",
            OWNER_DIR / "context_builder.py",
            OWNER_DIR / "docstring_validator.py",
            OWNER_DIR / "insert_missing_docstrings.py",
            OWNER_DIR / "insert_missing_docstrings_gui.py",
            OWNER_DIR / "module_summarizer.py",
        ]
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertIn(
                "from " + CANONICAL_TOKEN + ".backend_payloads.loader import load_payload",
                text,
            )

    def test_tab3_runtime_imports_use_canonical_package(self) -> None:
        support_path = OWNER_DIR / "insert_missing_docstrings_gui_help" / "manual_docstring_review_support.py"
        text = support_path.read_text(encoding="utf-8")
        self.assertIn(CANONICAL_TOKEN + ".tab3_manual_review_runtime.review_support", text)
        self.assertNotIn(LEGACY_TOKEN + ".tab3_manual_review_runtime", text)

    def test_tab1_audit_uses_canonical_architecture_entrypoint_path(self) -> None:
        path = OWNER_DIR / "insert_missing_docstrings_gui_help" / "tab1_audit_docstring_source.py"
        text = path.read_text(encoding="utf-8")
        self.assertIn('tool_root / "' + CANONICAL_TOKEN + '" / tool_dir / tool_name', text)
        self.assertNotIn('tool_root / "' + LEGACY_TOKEN + '" / tool_dir / tool_name', text)

    def test_worker_imports_canonical_worker_module(self) -> None:
        path = OWNER_DIR / "insert_missing_docstrings_gui_help" / "worker_thread.py"
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            '"' + CANONICAL_TOKEN + '.insert_missing_docstrings_gui.insert_missing_docstrings"',
            text,
        )


if __name__ == "__main__":
    unittest.main()
