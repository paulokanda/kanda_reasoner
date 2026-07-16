"""Focused checks for canonical package import probes in workflow_manifest.json."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_MANIFEST = PROJECT_ROOT / "workflow_manifest.json"
CANONICAL_PACKAGE = "kanda_reasoner_app"
LEGACY_PACKAGE = 'ask_' 'ai_project_reasoner'


class WorkflowManifestCanonicalImportProbeTests(unittest.TestCase):
    """Validate workflow import probes prefer the canonical package."""

    def _manifest(self) -> dict:
        return json.loads(WORKFLOW_MANIFEST.read_text(encoding="utf-8"))

    def _include_modules(self) -> list[str]:
        manifest = self._manifest()
        return list(
            manifest.get("workflows", {})
            .get("imports", {})
            .get("include_modules", [])
        )

    def test_import_probe_prefers_canonical_package(self) -> None:
        modules = self._include_modules()

        self.assertIn(CANONICAL_PACKAGE, modules)
        self.assertNotIn(LEGACY_PACKAGE, modules)

    def test_import_probe_keeps_gui_and_support_modules(self) -> None:
        modules = self._include_modules()

        self.assertIn("reasoner_tools_gui", modules)
        self.assertIn("_inject_missing_module_docstrings", modules)

    def test_import_probe_has_no_duplicate_modules(self) -> None:
        modules = self._include_modules()

        self.assertEqual(len(modules), len(set(modules)))


if __name__ == "__main__":
    unittest.main()
