"""Focused tests for the reasoner_context_bundle canonical package rename."""

from __future__ import annotations

import importlib
from pathlib import Path
import unittest


class ReasonerContextBundleCanonicalRenameTests(unittest.TestCase):
    """Validate the staged project_context_bundle to reasoner_context_bundle rename."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.app_root = cls.project_root / "kanda_reasoner_app"

    def test_canonical_package_exists_and_old_package_is_compatibility_only(self) -> None:
        canonical_dir = self.app_root / "reasoner_context_bundle"
        legacy_dir = self.app_root / "project_context_bundle"
        self.assertTrue(canonical_dir.is_dir())
        self.assertTrue(legacy_dir.is_dir())
        canonical_source = (canonical_dir / "output_paths.py").read_text(encoding="utf-8")
        legacy_source = (legacy_dir / "__init__.py").read_text(encoding="utf-8")
        self.assertIn("def bundle_artifact_paths", canonical_source)
        self.assertIn("_COMPAT_SUBMODULES", legacy_source)
        self.assertIn("kanda_reasoner_app.reasoner_context_bundle", legacy_source)
        self.assertFalse((legacy_dir / "output_paths.py").exists())

    def test_canonical_imports_work_and_legacy_imports_resolve_same_api(self) -> None:
        canonical = importlib.import_module(
            "kanda_reasoner_app.reasoner_context_bundle.output_paths"
        )
        legacy = importlib.import_module(
            "kanda_reasoner_app.project_context_bundle.output_paths"
        )
        self.assertIs(canonical.bundle_artifact_paths, legacy.bundle_artifact_paths)

    def test_module_runners_use_reasoner_context_bundle(self) -> None:
        process_text = (
            self.app_root
            / "reasoner_tools_shell"
            / "runner_help"
            / "window_process_private_impl.py"
        ).read_text(encoding="utf-8")
        zip_text = (
            self.app_root
            / "reasoner_tools_shell"
            / "runner_help"
            / "zip_json_files_private_impl.py"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'CANONICAL_PACKAGE_NAME + ".reasoner_context_bundle"',
            process_text,
        )
        self.assertNotIn(
            'CANONICAL_PACKAGE_NAME + ".project_context_bundle"',
            process_text,
        )
        self.assertIn(
            '"kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter"',
            zip_text,
        )
        self.assertNotIn(
            '"kanda_reasoner_app.project_context_bundle.handoff_zip_exporter"',
            zip_text,
        )

    def test_canonical_package_exports_new_cli_name_and_legacy_alias(self) -> None:
        package = importlib.import_module("kanda_reasoner_app.reasoner_context_bundle")
        self.assertTrue(callable(package.run_reasoner_context_bundle_cli))
        self.assertTrue(callable(package.run_project_context_bundle_cli))
        self.assertIs(
            package.run_reasoner_context_bundle_cli,
            package.run_project_context_bundle_cli,
        )


if __name__ == "__main__":
    unittest.main()
