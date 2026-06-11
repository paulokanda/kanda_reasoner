"""Focused tests for canonical v10 static context evidence formatter migration."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class V10StaticContextEvidenceFormatterCanonicalMigrationTests(unittest.TestCase):
    def test_canonical_evidence_formatter_file_exists(self):
        path = Path(
            "kanda_reasoner_app/reasoner_engine/"
            "v10_static_context_evidence_formatter.py"
        )
        self.assertTrue(path.exists(), str(path))

    def test_canonical_evidence_formatter_source_prefers_reasoner_engine(self):
        path = Path(
            "kanda_reasoner_app/reasoner_engine/"
            "v10_static_context_evidence_formatter.py"
        )
        text = path.read_text(encoding="utf-8", errors="replace")
        self.assertNotIn("ask_ai_project_reasoner.project_reasoner_v10", text)
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10", text)

    def test_canonical_evidence_formatter_imports(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine."
            "v10_static_context_evidence_formatter"
        )
        self.assertIsNotNone(module)

    def test_canonical_inspector_widget_imports_after_formatter(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine."
            "v10_static_context_inspector_widget"
        )
        self.assertIsNotNone(module)


if __name__ == "__main__":
    unittest.main()
