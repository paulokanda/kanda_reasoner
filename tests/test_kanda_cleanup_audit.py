"""Focused tests for the read-only cleanup audit."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import tools.kanda_cleanup_audit as cleanup_audit
from tools.kanda_cleanup_audit import build_report


class KandaCleanupAuditTests(unittest.TestCase):
    """Protect the cleanup audit behavior."""

    def test_public_surface_is_declared(self) -> None:
        exported_names = getattr(cleanup_audit, "__all__", None)

        self.assertIsInstance(exported_names, list)
        self.assertIn("CleanupCandidate", exported_names)
        self.assertIn("build_report", exported_names)
        self.assertIn("iter_cleanup_candidates", exported_names)
        self.assertIn("iter_canonical_status", exported_names)

        missing_names = [
            name
            for name in exported_names
            if not hasattr(cleanup_audit, name)
        ]
        self.assertEqual([], missing_names)

    def test_report_detects_safe_cache_and_patch_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "kanda_reasoner_app").mkdir()
            (root / "kanda_reasoner_app" / "reasoner_engine").mkdir()
            (root / "kanda_reasoner_app" / "reasoner_context_collector").mkdir()
            (root / "kanda_reasoner_app" / "reasoner_runtime_collector").mkdir()
            (root / "kanda_reasoner_app" / "reasoner_symbol_atlas").mkdir()
            (root / "__pycache__").mkdir()
            (root / "module.pyc").write_bytes(b"")
            (root / "kanda_reasoner_example_patch.zip").write_bytes(b"")

            report = build_report(root)
            categories = {
                item["category"]
                for item in report["cleanup_candidates"]
            }

            self.assertIn("safe_cache_directory", categories)
            self.assertIn("safe_compiled_python_file", categories)
            self.assertIn("patch_archive_in_project_root", categories)

    def test_report_detects_legacy_leftovers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            legacy = root / "kanda_reasoner_app" / "project_reasoner_v10"
            legacy.mkdir(parents=True)

            report = build_report(root)
            leftovers = [
                item
                for item in report["cleanup_candidates"]
                if item["category"] == "legacy_leftover"
            ]

            self.assertEqual(1, len(leftovers))
            self.assertEqual(
                "kanda_reasoner_app/project_reasoner_v10",
                leftovers[0]["relative_path"],
            )


if __name__ == "__main__":
    unittest.main()
