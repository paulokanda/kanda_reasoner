"""Tests for T10P021 Project Symbol Atlas canonical validation commands."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILES = (
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_symbol_atlas" / "_related_file_finder_support.py",
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_symbol_atlas" / "implementation_responsibility_resolver.py",
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_symbol_atlas" / "logic_placement_advisor.py",
)
LEGACY_ARCHITECTURE_COMMAND = 'python ask_' 'ai_project_reasoner' '\\manage_architecture\\manage_architecture.py'
LEGACY_WORKFLOW_COMMAND = 'python ask_' 'ai_project_reasoner' '\\manage_workflows\\manage_workflows.py'
CANONICAL_ARCHITECTURE_COMMAND = "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py"
CANONICAL_WORKFLOW_COMMAND = "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py"


def _source_runtime_text(path: Path) -> str:
    """Return source text with escaped path separators normalized for string checks."""

    return path.read_text(encoding="utf-8").replace("\\\\", "\\")


class ProjectSymbolAtlasCanonicalValidationCommandTests(unittest.TestCase):
    """Verify Project Symbol Atlas recommends canonical validation commands."""

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed atlas files should remain syntactically valid Python."""

        for path in CHANGED_FILES:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_changed_files_do_not_emit_legacy_validation_commands(self) -> None:
        """Changed atlas files should not recommend legacy validation CLI paths."""

        for path in CHANGED_FILES:
            source = _source_runtime_text(path)
            self.assertNotIn(LEGACY_ARCHITECTURE_COMMAND, source, path.as_posix())
            self.assertNotIn(LEGACY_WORKFLOW_COMMAND, source, path.as_posix())

    def test_changed_files_emit_canonical_validation_commands(self) -> None:
        """Changed atlas files should recommend canonical validation CLI paths."""

        combined = "\n".join(_source_runtime_text(path) for path in CHANGED_FILES)
        self.assertIn(CANONICAL_ARCHITECTURE_COMMAND, combined)
        self.assertIn(CANONICAL_WORKFLOW_COMMAND, combined)


if __name__ == "__main__":
    unittest.main()
