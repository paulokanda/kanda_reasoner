"""Regression tests for Freeze tab project-local freeze-hint intake restore."""

from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from kanda_reasoner_app.freeze_hint_intake import (
    build_freeze_form_inputs_from_latest_hint,
    scan_and_save_latest_freeze_hint,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_SOURCE = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"


class FreezeTabFreezeHintIntakeRestoreTests(unittest.TestCase):
    def _source(self) -> str:
        return TAB_SOURCE.read_text(encoding="utf-8")

    def test_tab_uses_public_freeze_hint_intake_before_safe_starter_fallback(self) -> None:
        source = self._source()
        self.assertIn("from kanda_reasoner_app.freeze_hint_intake import", source)
        self.assertIn("build_freeze_form_inputs_from_latest_hint", source)
        self.assertIn("mark_latest_freeze_hint_used", source)
        self.assertIn("return build_freeze_form_inputs_from_latest_hint(project_root, fallback_inputs)", source)
        self.assertIn("project_freeze_after_update/freeze_hint_intake", source)
        self.assertIn("Freeze hint intake record marked as used for this freeze.", source)

    def test_safe_starter_is_still_available_and_not_writable_without_evidence(self) -> None:
        source = self._source()
        self.assertIn('"feature_title": "Current validated feature - replace with exact feature title"', source)
        self.assertIn('"validation_evidence_summary": ""', source)
        self.assertIn("No validation evidence has been inferred or invented.", source)
        self.assertNotIn('"feature_title": "Freeze Feature After Update Local Freeze Workflow v1"', source)
        self.assertNotIn("VALIDATION OK: startup_freeze_context_channel_v1", source)

    def test_project_local_freeze_hint_zip_fills_form_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo_project"
            project.mkdir()
            staging = Path(tmp) / "demo_project_delete_after_daily_work"
            staging.mkdir()
            patch_zip = staging / "demo_feature_patch.zip"
            hint = {
                "kind": "kanda_freeze_hint",
                "feature_id": "demo-feature-v1",
                "feature_title": "Demo Feature v1",
                "primary_box": "demo_box",
                "box_type": "Module Box",
                "validated_files": ["src/demo.py", "tests/test_demo.py"],
                "generated_files": ["workbench/bundle_manifest/BUNDLE_MANIFEST_demo.txt"],
                "protected_paths": ["src/demo.py"],
                "do_not_regress_rules": ["Keep demo behavior stable."],
                "validation_evidence_summary": "VALIDATION OK: demo_feature_v1\nCONTRACT_TEST_OK: demo feature validated",
                "known_warnings": "No known warnings.",
                "planned_next_step": "Freeze Demo Feature v1.",
                "notes": "Generated from root-level KANDA_FREEZE_HINT.json sidecar.",
            }
            with zipfile.ZipFile(patch_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, indent=2))
                archive.writestr("src/demo.py", "# demo\n")

            fallback = {
                "feature_title": "Current validated feature - replace with exact feature title",
                "primary_box": "Replace with the primary box for the current feature",
                "box_type": "Replace with the current box type",
                "validated_files": "",
                "generated_files": "",
                "protected_paths": "project_freeze_after_update/frozen_features_memory/",
                "do_not_regress_rules": "Do not freeze without current feature validation evidence.",
                "validation_evidence_summary": "",
                "known_warnings": "Starter draft only.",
                "planned_next_step": "Replace placeholders.",
                "notes": "Starter fallback.",
            }

            scan_result = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
            self.assertTrue(scan_result.get("ok"), scan_result)

            inputs = build_freeze_form_inputs_from_latest_hint(project, fallback)

            self.assertEqual(inputs["feature_title"], "Demo Feature v1")
            self.assertEqual(inputs["primary_box"], "demo_box")
            self.assertIn("src/demo.py", inputs["validated_files"])
            self.assertIn("VALIDATION OK: demo_feature_v1", inputs["validation_evidence_summary"])
            self.assertIn("project_freeze_after_update/frozen_features_memory/", inputs["protected_paths"])
            self.assertIn("Do not store project-specific frozen memory inside project_freeze_ledger.", inputs["do_not_regress_rules"])
            self.assertIn("Auto-filled from saved KANDA_FREEZE_HINT.json intake data", inputs["known_warnings"])
            self.assertTrue((project / "project_freeze_after_update" / "freeze_hint_intake" / "latest_freeze_hint.json").exists())


if __name__ == "__main__":
    unittest.main()
