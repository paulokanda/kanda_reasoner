from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from kanda_reasoner_app.freeze_hint_intake import (
    build_freeze_form_inputs_from_latest_hint,
    merge_validation_evidence_into_latest_hint,
)
from kanda_reasoner_app.freeze_hint_intake.contract import save_freeze_hint_record


FORM_KEYS = [
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
]


class FreezeHintValidatedLatestPreserveTests(unittest.TestCase):
    def _project_root(self) -> Path:
        return Path(tempfile.mkdtemp(prefix="kanda_freeze_hint_preserve_"))

    def _default_staging_dir(self, project_root: Path) -> Path:
        anchor = project_root.anchor
        if anchor:
            return Path(anchor) / (project_root.name + "_delete_after_daily_work")
        return project_root.parent / (project_root.name + "_delete_after_daily_work")

    def _hint(self, feature_id: str, title: str) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "kind": "kanda_freeze_hint",
            "feature_id": feature_id,
            "feature_title": title,
            "primary_box": "kanda_reasoner_app/freeze_hint_intake",
            "box_type": "Intake / Contract",
            "validated_files": [
                "kanda_reasoner_app/freeze_hint_intake/contract.py",
            ],
            "generated_files": [
                "workbench/bundle_manifest/BUNDLE_MANIFEST_" + feature_id + ".txt",
            ],
            "protected_paths": [
                "kanda_reasoner_app/freeze_hint_intake/",
                "project_freeze_after_update/freeze_hint_intake/",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "Freeze hint intake must preserve validation evidence for the same staged hint and prefer the newest staged hint for new work.",
                "Do not store project-specific frozen memory inside project_freeze_ledger.",
            ],
            "validation_evidence_summary": "LOCAL VALIDATION PENDING: run the provided validation block before freezing",
            "known_warnings": "Human review remains required before Confirm and Write.",
            "planned_next_step": "Validate locally, then freeze.",
            "notes": "Test hint.",
        }

    def _write_staged_hint_zip(self, project_root: Path, hint: dict[str, object], name: str) -> Path:
        staging = self._default_staging_dir(project_root)
        staging.mkdir(parents=True, exist_ok=True)
        zip_path = staging / name
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, indent=2))
            archive.writestr("dummy.txt", "dummy")
        return zip_path

    def test_newer_staged_hint_replaces_older_validated_latest_hint(self) -> None:
        project_root = self._project_root()
        current_hint = self._hint(
            "freeze_tab_freeze_hint_intake_restore_v1",
            "Freeze Tab Freeze Hint Intake Restore v1",
        )
        save_result = save_freeze_hint_record(project_root, current_hint)
        self.assertEqual(save_result["hint"]["feature_id"], "freeze-tab-freeze-hint-intake-restore-v1")

        evidence = "\n".join(
            [
                "VALIDATION OK: freeze_tab_freeze_hint_intake_restore_v1",
                "CONTRACT_TEST_OK: Freeze tab reads project-local KANDA_FREEZE_HINT.json intake data before safe starter fallback",
                "STATUS: FREEZE_TAB_FREEZE_HINT_INTAKE_RESTORED",
            ]
        )
        merge_result = merge_validation_evidence_into_latest_hint(
            project_root,
            evidence,
            feature_id="freeze_tab_freeze_hint_intake_restore_v1",
            feature_title="Freeze Tab Freeze Hint Intake Restore v1",
        )
        self.assertTrue(merge_result["ok"], merge_result)

        unrelated_hint = self._hint(
            "freeze_hint_feature_id_alias_merge_v1",
            "Freeze Hint Feature ID Alias Merge v1",
        )
        self._write_staged_hint_zip(project_root, unrelated_hint, "zz_newer_unrelated_patch.zip")

        fallback = {key: "" for key in FORM_KEYS}
        inputs = build_freeze_form_inputs_from_latest_hint(project_root, fallback)

        self.assertEqual(inputs["feature_title"], "Freeze Hint Feature ID Alias Merge v1")
        self.assertNotIn("Freeze Tab Freeze Hint Intake Restore v1", inputs["feature_title"])
        self.assertIn("LOCAL VALIDATION PENDING", inputs["validation_evidence_summary"])
        self.assertIn("project_freeze_after_update/frozen_features_memory/", inputs["protected_paths"])

    def test_same_staged_hint_preserves_merged_validation_evidence(self) -> None:
        project_root = self._project_root()
        current_hint = self._hint(
            "freeze_tab_freeze_hint_intake_restore_v1",
            "Freeze Tab Freeze Hint Intake Restore v1",
        )
        zip_path = self._write_staged_hint_zip(project_root, current_hint, "freeze_tab_restore_patch.zip")
        first = build_freeze_form_inputs_from_latest_hint(project_root, {key: "" for key in FORM_KEYS})
        self.assertEqual(first["feature_title"], "Freeze Tab Freeze Hint Intake Restore v1")

        evidence = "\n".join(
            [
                "VALIDATION OK: freeze_tab_freeze_hint_intake_restore_v1",
                "CONTRACT_TEST_OK: Freeze tab reads project-local KANDA_FREEZE_HINT.json intake data before safe starter fallback",
                "STATUS: FREEZE_TAB_FREEZE_HINT_INTAKE_RESTORED",
            ]
        )
        merge_result = merge_validation_evidence_into_latest_hint(
            project_root,
            evidence,
            feature_id="freeze_tab_freeze_hint_intake_restore_v1",
            feature_title="Freeze Tab Freeze Hint Intake Restore v1",
        )
        self.assertTrue(merge_result["ok"], merge_result)

        # The same staged ZIP may be scanned again, but the saved local
        # validation evidence must not be downgraded back to the pending sidecar.
        inputs = build_freeze_form_inputs_from_latest_hint(project_root, {key: "" for key in FORM_KEYS})
        self.assertEqual(inputs["feature_title"], "Freeze Tab Freeze Hint Intake Restore v1")
        self.assertIn("VALIDATION OK: freeze_tab_freeze_hint_intake_restore_v1", inputs["validation_evidence_summary"])
        self.assertNotIn("LOCAL VALIDATION PENDING", inputs["validation_evidence_summary"])


if __name__ == "__main__":
    unittest.main()
