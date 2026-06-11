"""Regression tests for T10P018 source hygiene canonical commands."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from kanda_reasoner_app.source_hygiene.schemas import SourceHygieneFinding
from kanda_reasoner_app.source_hygiene.shadow_planner import finding_to_plan_item


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SHADOW_PLANNER = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "source_hygiene" / "shadow_planner.py"


class SourceHygieneCanonicalCommandTests(unittest.TestCase):
    """Validate canonical command text in source hygiene planning."""

    def test_shadow_planner_source_remains_ast_parseable(self) -> None:
        """The changed planner module should remain syntactically valid."""
        source = SHADOW_PLANNER.read_text(encoding="utf-8")
        ast.parse(source)

    def test_shadow_planner_does_not_hardcode_legacy_validation_commands(self) -> None:
        """Required validation commands should not point to legacy CLI paths."""
        source = SHADOW_PLANNER.read_text(encoding="utf-8")
        self.assertNotIn('python ask_' 'ai_project_reasoner' '\\\\manage_architecture', source)
        self.assertNotIn('python ask_' 'ai_project_reasoner' '\\\\manage_workflows', source)
        self.assertIn("python kanda_reasoner_app\\\\manage_architecture", source)
        self.assertIn("python kanda_reasoner_app\\\\manage_workflows", source)

    def test_plan_items_emit_canonical_required_validation_commands(self) -> None:
        """Observable plan output should recommend canonical validation commands."""
        finding = SourceHygieneFinding(
            code="FACADE_WITHOUT_ALL",
            path="demo/__init__.py",
            line=1,
            severity="warning",
            confidence="high",
            message="Facade lacks explicit public surface.",
            evidence={},
            suggested_action="Add __all__.",
        )
        item = finding_to_plan_item(finding)
        joined = "\n".join(item.required_tests)
        self.assertIn("kanda_reasoner_app\\manage_architecture", joined)
        self.assertIn("kanda_reasoner_app\\manage_workflows", joined)
        self.assertNotIn('ask_' 'ai_project_reasoner' '\\manage_architecture', joined)
        self.assertNotIn('ask_' 'ai_project_reasoner' '\\manage_workflows', joined)


if __name__ == "__main__":
    unittest.main()
