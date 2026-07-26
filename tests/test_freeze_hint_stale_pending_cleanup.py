from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.freeze_hint_intake.contract import (
    build_freeze_form_inputs_from_latest_hint,
    merge_validation_evidence_into_latest_hint,
    resolve_freeze_hint_autofill_state,
    save_freeze_hint_record,
)


FORM_KEYS = (
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
)


class FreezeHintStalePendingCleanupTests(unittest.TestCase):
    def _project_root(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name) / "active_project"
        root.mkdir(parents=True)
        return root

    def _fallback(self) -> dict[str, str]:
        return {key: "" for key in FORM_KEYS} | {
            "feature_title": "Current validated feature - replace with exact feature title",
            "primary_box": "Replace with the primary box for the current feature",
            "box_type": "Replace with the current box type",
            "protected_paths": "project_freeze_after_update/frozen_features_memory/",
            "do_not_regress_rules": "Do not freeze without current feature validation evidence.",
            "known_warnings": "Starter draft only.",
            "planned_next_step": "Replace placeholders.",
            "notes": "Starter fallback.",
        }

    def _hint(self, evidence: str) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "kind": "kanda_freeze_hint",
            "feature_id": "stale_pending_cleanup_v1",
            "feature_title": "Stale Pending Cleanup v1",
            "primary_box": "kanda_reasoner_app/freeze_hint_intake",
            "box_type": "Freeze Hint Intake / Evidence Hygiene",
            "validated_files": [
                "kanda_reasoner_app/freeze_hint_intake/contract.py",
                "tests/test_freeze_hint_stale_pending_cleanup.py",
            ],
            "generated_files": [],
            "protected_paths": [
                "kanda_reasoner_app/freeze_hint_intake/",
                "project_freeze_after_update/freeze_hint_intake/",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "Do not preserve LOCAL VALIDATION PENDING text after real local validation passes.",
                "Do not remove LOCAL VALIDATION PENDING text when only sandbox validation exists.",
            ],
            "validation_evidence_summary": evidence,
            "known_warnings": "Pre-validation sidecar only. User-local validation must be run before Confirm and Write. Human review remains required.",
            "planned_next_step": "Run the delivered validation block before Confirm and Write. Then preview freeze entry.",
            "notes": "User-local validation remains required before freeze confirmation. Keep this feature governed.",
        }

    def test_sandbox_only_evidence_keeps_pending_warning_and_blocks_confirm(self) -> None:
        project_root = self._project_root()
        hint = self._hint(
            "SANDBOX VALIDATION OK: python -m unittest tests.test_example\n"
            "LOCAL VALIDATION PENDING: run local validation before Confirm and Write."
        )
        save_freeze_hint_record(project_root, hint)

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=project_root / "empty_staging",
        )

        self.assertFalse(state["confirm_write_enabled"])
        self.assertEqual(state["validation_evidence_status"], "missing_or_unrecognized")
        self.assertIn("LOCAL VALIDATION PENDING", state["form_inputs"]["validation_evidence_summary"])
        self.assertIn("User-local validation must be run", state["form_inputs"]["known_warnings"])

    def test_merge_local_validation_cleans_stale_pending_text_from_form_fields(self) -> None:
        project_root = self._project_root()
        save_freeze_hint_record(project_root, self._hint("LOCAL VALIDATION PENDING: stale_pending_cleanup_v1"))

        evidence = "\n".join(
            [
                "VALIDATION OK: stale_pending_cleanup_v1",
                "STATUS: IN_SYNC",
                "ZIP CONTRACT: PASS",
            ]
        )
        result = merge_validation_evidence_into_latest_hint(
            project_root,
            evidence,
            feature_id="stale_pending_cleanup_v1",
            feature_title="Stale Pending Cleanup v1",
        )
        self.assertTrue(result["ok"], result)

        inputs = build_freeze_form_inputs_from_latest_hint(project_root, self._fallback())

        combined = "\n".join(
            [
                inputs["validation_evidence_summary"],
                inputs["known_warnings"],
                inputs["planned_next_step"],
                inputs["notes"],
            ]
        )
        self.assertIn("VALIDATION OK: stale_pending_cleanup_v1", inputs["validation_evidence_summary"])
        self.assertNotIn("LOCAL VALIDATION PENDING", combined)
        self.assertNotIn("Pre-validation sidecar only", combined)
        self.assertNotIn("User-local validation must be run", combined)
        self.assertNotIn("before Confirm and Write", combined)

    def test_legacy_mixed_local_evidence_is_cleaned_during_autofill(self) -> None:
        project_root = self._project_root()
        hint = self._hint(
            "VALIDATION OK: stale_pending_cleanup_v1\n"
            "STATUS: IN_SYNC\n"
            "LOCAL VALIDATION PENDING: stale text from old sidecar."
        )
        save_freeze_hint_record(project_root, hint)

        inputs = build_freeze_form_inputs_from_latest_hint(project_root, self._fallback())
        combined = "\n".join(
            [
                inputs["validation_evidence_summary"],
                inputs["known_warnings"],
                inputs["planned_next_step"],
                inputs["notes"],
            ]
        )

        self.assertIn("VALIDATION OK: stale_pending_cleanup_v1", inputs["validation_evidence_summary"])
        self.assertNotIn("LOCAL VALIDATION PENDING", combined)
        self.assertNotIn("User-local validation remains required", combined)


if __name__ == "__main__":
    unittest.main()
