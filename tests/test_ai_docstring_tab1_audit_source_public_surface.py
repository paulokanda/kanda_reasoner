
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
    tab1_audit_docstring_source,
)


class Tab1AuditDocstringSourcePublicSurfaceTests(unittest.TestCase):
    """Validate public surface control for the Tab 1 audit source helper."""

    def test_helper_defines_explicit_all(self) -> None:
        self.assertTrue(hasattr(tab1_audit_docstring_source, "__all__"))

        exported = set(tab1_audit_docstring_source.__all__)
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

        self.assertEqual(expected, exported)

    def test_all_symbols_exist(self) -> None:
        for name in tab1_audit_docstring_source.__all__:
            self.assertTrue(
                hasattr(tab1_audit_docstring_source, name),
                f"Missing exported symbol: {name}",
            )

    def test_regex_is_not_exported_as_public_surface(self) -> None:
        self.assertNotIn("MISSING_DOCSTRING_RE", tab1_audit_docstring_source.__all__)


if __name__ == "__main__":
    unittest.main()
