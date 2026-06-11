
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
    tab1_audit_docstring_source,
)


HELPER_PATH = Path(
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
    "insert_missing_docstrings_gui_help/tab1_audit_docstring_source.py"
)


class Tab1AuditDocstringSourceFutureImportTests(unittest.TestCase):
    """Validate future-import placement and public surface control."""

    def test_future_import_remains_before_all_assignment(self) -> None:
        source = HELPER_PATH.read_text(encoding="utf-8")
        lines = source.splitlines()

        future_line = None
        all_line = None
        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped == "from __future__ import annotations":
                future_line = index
            if stripped.startswith("__all__ ="):
                all_line = index

        self.assertIsNotNone(future_line)
        self.assertIsNotNone(all_line)
        self.assertLess(future_line, all_line)

    def test_module_parses_and_defines_expected_all(self) -> None:
        source = HELPER_PATH.read_text(encoding="utf-8")
        ast.parse(source)

        expected = {
            "MISSING_DOCSTRING_CODE",
            "TAB1_AUDIT_SOURCE_LABEL",
            "Tab1AuditDocstringSourceResult",
            "Tab1MissingDocstringFinding",
            "extract_missing_docstring_findings",
            "read_missing_docstrings_from_tab1_audit",
            "refresh_tab1_audit_docstring_source",
            "tab1_audit_source_is_enabled",
        }

        self.assertEqual(expected, set(tab1_audit_docstring_source.__all__))

    def test_internal_regex_is_not_exported(self) -> None:
        self.assertNotIn("MISSING_DOCSTRING_RE", tab1_audit_docstring_source.__all__)


if __name__ == "__main__":
    unittest.main()
