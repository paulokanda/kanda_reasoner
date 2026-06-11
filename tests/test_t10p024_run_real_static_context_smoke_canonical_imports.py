"""Regression tests for T10P024 run real static-context smoke imports."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SMOKE_SOURCE = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "run_real_project_static_context_smoke.py"


class RunRealStaticContextSmokeCanonicalImportTests(unittest.TestCase):
    """Validate canonical imports in the real-project static context smoke script."""

    def _source_text(self) -> str:
        return SMOKE_SOURCE.read_text(encoding="utf-8")

    def test_smoke_script_uses_canonical_imports(self) -> None:
        """The smoke script should import dependencies through kanda_reasoner_app."""
        source = self._source_text()

        self.assertIn(
            "from kanda_reasoner_app.reasoner_context_collector.collector_main import",
            source,
        )
        self.assertIn(
            "from kanda_reasoner_app.project_root_resolver import",
            source,
        )

    def test_smoke_script_does_not_use_legacy_from_imports(self) -> None:
        """The smoke script should not use legacy package from-imports."""
        source = self._source_text()

        self.assertNotIn(
            "from kanda_reasoner_app.reasoner_context_collector.collector_main import",
            source,
        )
        self.assertNotIn(
            "from kanda_reasoner_app.project_root_resolver import",
            source,
        )

    def test_smoke_script_remains_ast_parseable(self) -> None:
        """The changed smoke script should remain syntactically valid Python."""
        ast.parse(self._source_text(), filename=str(SMOKE_SOURCE))


if __name__ == "__main__":
    unittest.main()
