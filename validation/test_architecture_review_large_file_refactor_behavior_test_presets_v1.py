# project-path: validation/test_architecture_review_large_file_refactor_behavior_test_presets_v1.py
"""Tests for behavior-test preset discovery."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.behavior_test_presets import (
    build_behavior_test_presets,
    write_behavior_test_presets,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    build_behavior_test_presets as exported_build_behavior_test_presets,
    write_behavior_test_presets as exported_write_behavior_test_presets,
)


class BehaviorTestPresetDiscoveryTests(unittest.TestCase):
    """Behavior-test preset discovery is read-only and daily-work-contained."""

    def test_discovers_pytest_and_unittest_presets_without_running_tests(self) -> None:
        """Detected test files create allow-listed presets and no behavior claim."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            tests = root / "tests"
            tests.mkdir(parents=True)
            (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
            (tests / "test_alpha.py").write_text("def test_alpha():\n    assert True\n", encoding="utf-8")

            report = build_behavior_test_presets(active_project_root=str(root))
            written = write_behavior_test_presets(report)

            self.assertEqual(written.status, "behavior_test_presets_ready")
            self.assertFalse(written.source_mutation_enabled)
            self.assertFalse(written.test_execution_enabled)
            self.assertFalse(written.behavior_validation_claimed)
            commands = {preset.command for preset in written.presets}
            self.assertIn("python -m pytest", commands)
            self.assertIn("python -m pytest tests", commands)
            self.assertIn("python -m unittest discover -s tests", commands)
            payload = json.loads(Path(written.report_path).read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "behavior_test_presets_ready")
            self.assertTrue(Path(written.view_path).exists())

    def test_preview_root_inside_project_source_is_blocked(self) -> None:
        """Preset artifacts cannot be written inside project source."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            bad_preview = root / "large_file_refactor_preview"
            report = build_behavior_test_presets(
                active_project_root=str(root),
                preview_root=str(bad_preview),
            )
            self.assertEqual(report.status, "blocked")
            self.assertIn("PREVIEW_ROOT_INSIDE_PROJECT_SOURCE", report.blockers)
            self.assertIn("PREVIEW_ROOT_OUTSIDE_DAILY_WORK", report.blockers)

    def test_no_tests_is_visible_without_claiming_behavior_validation(self) -> None:
        """Projects without test signals produce explicit no-preset evidence."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            report = build_behavior_test_presets(active_project_root=str(root))
            self.assertEqual(report.status, "no_behavior_test_presets_discovered")
            self.assertEqual(report.presets, [])
            self.assertFalse(report.behavior_validation_claimed)
            self.assertIn("NO_PROJECT_TEST_PRESETS_DISCOVERED", report.warnings)

    def test_package_exports_presets_helpers(self) -> None:
        """Package facade exports the preset discovery helpers."""
        self.assertIs(exported_build_behavior_test_presets, build_behavior_test_presets)
        self.assertIs(exported_write_behavior_test_presets, write_behavior_test_presets)


if __name__ == "__main__":
    unittest.main()
