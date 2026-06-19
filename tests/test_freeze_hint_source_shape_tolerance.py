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
from kanda_reasoner_app.freeze_hint_intake.contract import build_freeze_hint_intake_paths


class FreezeHintSourceShapeToleranceTests(unittest.TestCase):
    def _write_patch_zip(self, path: Path, *, evidence: str = "LOCAL VALIDATION PENDING: source shape") -> None:
        hint = {
            "schema_version": "1.0",
            "kind": "kanda_freeze_hint",
            "feature_id": "freeze_hint_source_shape_tolerance_v1",
            "feature_title": "Freeze Hint Source Shape Tolerance v1",
            "primary_box": "kanda_reasoner_app/freeze_hint_intake",
            "box_type": "Intake / Contract / Legacy Record Tolerance",
            "validated_files": ["kanda_reasoner_app/freeze_hint_intake/contract.py"],
            "generated_files": ["workbench/bundle_manifest/BUNDLE_MANIFEST_freeze_hint_source_shape_tolerance_v1.txt"],
            "protected_paths": [
                "kanda_reasoner_app/freeze_hint_intake/",
                "project_freeze_after_update/freeze_hint_intake/",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "Freeze hint intake must tolerate legacy scalar source metadata without crashing.",
                "Do not store project-specific frozen memory inside project_freeze_ledger.",
            ],
            "validation_evidence_summary": evidence,
            "known_warnings": "Source metadata shape compatibility repair.",
            "planned_next_step": "Use New Local Freeze Entry after validation.",
            "notes": "Regression repair for legacy source field shapes in latest_freeze_hint.json.",
        }
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, indent=2))
            archive.writestr("dummy.txt", "dummy")

    def test_scalar_source_in_latest_hint_does_not_crash_staged_rescan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir(parents=True)
            staging = Path(tmp) / "staging"
            staging.mkdir(parents=True)
            paths = build_freeze_hint_intake_paths(root)
            paths.intake_root.mkdir(parents=True)

            latest = {
                "kind": "kanda_saved_freeze_hint",
                "schema_version": "1.0",
                "project_root": str(root.resolve()),
                "saved_at_utc": "2026-06-16T15:05:00Z",
                "used_at_utc": None,
                "source": "formulary_data_zip",
                "source_zip": "legacy_data.zip",
                "hint": {
                    "schema_version": "1.0",
                    "kind": "kanda_freeze_hint",
                    "feature_id": "freeze-hint-source-shape-tolerance-v1",
                    "feature_title": "Freeze Hint Source Shape Tolerance v1",
                    "primary_box": "kanda_reasoner_app/freeze_hint_intake",
                    "box_type": "Intake / Contract / Legacy Record Tolerance",
                    "validated_files": "kanda_reasoner_app/freeze_hint_intake/contract.py",
                    "generated_files": "workbench/bundle_manifest/BUNDLE_MANIFEST_freeze_hint_source_shape_tolerance_v1.txt",
                    "protected_paths": "project_freeze_after_update/frozen_features_memory/",
                    "do_not_regress_rules": "Do not store project-specific frozen memory inside project_freeze_ledger.",
                    "validation_evidence_summary": "VALIDATION OK: freeze_hint_source_shape_tolerance_v1",
                    "known_warnings": "Legacy scalar source metadata.",
                    "planned_next_step": "Validate formulary read.",
                    "notes": "Saved from data ZIP.",
                },
                "form_inputs": {
                    "feature_title": "Freeze Hint Source Shape Tolerance v1",
                    "primary_box": "kanda_reasoner_app/freeze_hint_intake",
                    "box_type": "Intake / Contract / Legacy Record Tolerance",
                    "validated_files": "kanda_reasoner_app/freeze_hint_intake/contract.py",
                    "generated_files": "workbench/bundle_manifest/BUNDLE_MANIFEST_freeze_hint_source_shape_tolerance_v1.txt",
                    "protected_paths": "project_freeze_after_update/frozen_features_memory/",
                    "do_not_regress_rules": "Do not store project-specific frozen memory inside project_freeze_ledger.",
                    "validation_evidence_summary": "VALIDATION OK: freeze_hint_source_shape_tolerance_v1",
                    "known_warnings": "Legacy scalar source metadata.",
                    "planned_next_step": "Validate formulary read.",
                    "notes": "Saved from data ZIP.",
                },
            }
            paths.latest_hint.write_text(json.dumps(latest, indent=2), encoding="utf-8")

            self._write_patch_zip(staging / "newer_same_feature.zip")
            result = scan_and_save_latest_freeze_hint(root, staging_dir=staging)
            self.assertTrue(result.get("ok"), result)

            fallback = {key: "" for key in (
                "feature_title", "primary_box", "box_type", "validated_files", "generated_files",
                "protected_paths", "do_not_regress_rules", "validation_evidence_summary",
                "known_warnings", "planned_next_step", "notes",
            )}
            inputs = build_freeze_form_inputs_from_latest_hint(root, fallback)
            self.assertEqual(inputs["feature_title"], "Freeze Hint Source Shape Tolerance v1")
            self.assertIn("VALIDATION OK: freeze_hint_source_shape_tolerance_v1", inputs["validation_evidence_summary"])


if __name__ == "__main__":
    unittest.main()
