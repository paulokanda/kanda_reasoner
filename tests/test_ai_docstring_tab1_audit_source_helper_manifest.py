
from __future__ import annotations

import json
from pathlib import Path
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
    tab1_audit_docstring_source,
)


MANIFEST_PATH = Path(
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
    "insert_missing_docstrings_gui_help.json"
)
HELPER_NAME = "tab1_audit_docstring_source.py"


class Tab1AuditDocstringSourceHelperManifestTests(unittest.TestCase):
    """Validate helper-manifest alignment for the Tab 1 audit source helper."""

    def test_manifest_lists_tab1_audit_helper(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertIn("helpers", manifest)
        self.assertIn(HELPER_NAME, manifest["helpers"])

    def test_manifest_exports_match_helper_all(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        helper = manifest["helpers"][HELPER_NAME]

        self.assertEqual(list(tab1_audit_docstring_source.__all__), helper["exports"])

    def test_manifest_dependency_graph_has_helper(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertIn("dependency_graph", manifest)
        self.assertIn(HELPER_NAME, manifest["dependency_graph"])
        self.assertEqual([], manifest["dependency_graph"][HELPER_NAME])

    def test_manifest_purpose_mentions_tab1_audit(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        helper = manifest["helpers"][HELPER_NAME]

        self.assertIn("Tab 1", helper["purpose"])
        self.assertIn("MISSING_DOCSTRING", helper["purpose"])


if __name__ == "__main__":
    unittest.main()
