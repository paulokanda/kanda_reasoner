from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.freeze_hint_intake import (
    build_freeze_form_inputs_from_latest_hint,
    merge_validation_evidence_into_latest_hint,
)
from kanda_reasoner_app.freeze_hint_intake.contract import save_freeze_hint_record


class FreezeHintFeatureIdAliasMergeTests(unittest.TestCase):
    def _project_root(self) -> Path:
        return Path(tempfile.mkdtemp(prefix="kanda_freeze_hint_alias_"))

    def _base_hint(self) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "kind": "kanda_freeze_hint",
            "feature_id": "freeze_tab_freeze_hint_intake_restore_v1",
            "feature_title": "Freeze Tab Freeze Hint Intake Restore v1",
            "primary_box": "kanda_reasoner_app/freeze_after_update_gui",
            "box_type": "GUI / Workflow / Freeze Hint Intake Bridge",
            "validated_files": [
                "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
                "tests/test_freeze_tab_freeze_hint_intake_restore.py",
            ],
            "generated_files": [
                "workbench/bundle_manifest/BUNDLE_MANIFEST_freeze_tab_freeze_hint_intake_restore_v1.txt"
            ],
            "protected_paths": [
                "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "New Local Freeze Entry must fill from project-local freeze hint intake when a current KANDA_FREEZE_HINT.json sidecar exists.",
            ],
            "validation_evidence_summary": "LOCAL VALIDATION PENDING: run the provided validation block before freezing",
            "known_warnings": "Human review remains required before Confirm and Write.",
            "planned_next_step": "Install locally, run validation, then freeze this feature through the tab.",
            "notes": "Regression restore patch.",
        }

    def test_merge_accepts_underscore_feature_id_for_hyphenated_saved_hint(self) -> None:
        project_root = self._project_root()
        save_result = save_freeze_hint_record(project_root, self._base_hint())
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
        self.assertEqual(merge_result["feature_id"], "freeze-tab-freeze-hint-intake-restore-v1")

        fallback = {key: "" for key in [
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
        ]}
        form_inputs = build_freeze_form_inputs_from_latest_hint(project_root, fallback)
        self.assertIn("VALIDATION OK: freeze_tab_freeze_hint_intake_restore_v1", form_inputs["validation_evidence_summary"])
        self.assertIn("kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py", form_inputs["validated_files"])

    def test_merge_still_rejects_unrelated_feature_id(self) -> None:
        project_root = self._project_root()
        save_freeze_hint_record(project_root, self._base_hint())

        merge_result = merge_validation_evidence_into_latest_hint(
            project_root,
            "VALIDATION OK: some_other_feature",
            feature_id="some_other_feature",
            feature_title="Freeze Tab Freeze Hint Intake Restore v1",
        )

        self.assertFalse(merge_result["ok"])
        self.assertIn("feature_id mismatch", "\n".join(merge_result["errors"]))


if __name__ == "__main__":
    unittest.main()
