"""Validate canonical import usage in the static context smoke assertion."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class StaticContextSmokeCanonicalImportTests(unittest.TestCase):
    """Check that the static context smoke assertion uses canonical imports."""

    def test_static_context_smoke_imports_project_root_resolver_canonically(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.assert_real_project_static_context_smoke"
        )

        self.assertTrue(hasattr(module, "default_smoke_output_json_path"))
        self.assertEqual(
            module.default_smoke_output_json_path.__module__,
            "kanda_reasoner_app.project_root_resolver",
        )

    def test_static_context_smoke_source_has_no_legacy_project_root_import(self) -> None:
        source = Path(
            'ask_' 'ai_project_reasoner' '/assert_real_project_static_context_smoke.py'
        ).read_text(encoding="utf-8")
        legacy_import = (
            "from ask_ai"
            "_project_reasoner.project_root_resolver import "
            "default_smoke_output_json_path"
        )

        self.assertNotIn(legacy_import, source)
        self.assertIn(
            "from kanda_reasoner_app.project_root_resolver import "
            "default_smoke_output_json_path",
            source,
        )


if __name__ == "__main__":
    unittest.main()
