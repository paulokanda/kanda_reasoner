from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from kanda_reasoner_app.freeze_hint_intake.contract import (
    build_freeze_form_inputs_from_latest_hint,
    build_freeze_hint_intake_paths,
    merge_validation_evidence_into_latest_hint,
    read_freeze_hint_from_patch_zip,
    save_freeze_hint_record,
    scan_and_save_latest_freeze_hint,
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


class FreezeHintStaleZipSelectionRepairTests(unittest.TestCase):
    def _project_root(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name) / "active_project"
        root.mkdir(parents=True)
        return root

    def _staging_dir(self, project_root: Path) -> Path:
        anchor = project_root.anchor
        if anchor:
            staging = Path(anchor) / (project_root.name + "_delete_after_daily_work")
        else:
            staging = project_root.parent / (project_root.name + "_delete_after_daily_work")
        staging.mkdir(parents=True, exist_ok=True)
        self.addCleanup(lambda: shutil.rmtree(staging, ignore_errors=True))
        return staging

    def _hint(self, feature_id: str, feature_title: str, evidence: str) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "kind": "kanda_freeze_hint",
            "feature_id": feature_id,
            "feature_title": feature_title,
            "primary_box": "kanda_reasoner_app/freeze_hint_intake",
            "box_type": "Freeze Hint Intake / GUI Autofill",
            "validated_files": [
                "kanda_reasoner_app/freeze_hint_intake/contract.py",
                "tests/test_freeze_hint_stale_zip_selection_repair.py",
            ],
            "generated_files": [],
            "protected_paths": [
                "kanda_reasoner_app/freeze_hint_intake/",
                "project_freeze_after_update/freeze_hint_intake/",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "New Local Freeze Entry must not overwrite the current validated hint with stale older sidecars.",
                "Do not store project-specific frozen memory inside project_freeze_ledger.",
            ],
            "validation_evidence_summary": evidence,
            "known_warnings": "Human review remains required before Confirm and Write.",
            "planned_next_step": "Preview Freeze Entry, then Confirm and Write after human review.",
            "notes": "Test hint.",
        }

    def _write_zip(self, path: Path, hint: dict[str, object]) -> Path:
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, indent=2))
            archive.writestr("dummy.txt", "dummy")
        return path

    def _fallback(self) -> dict[str, str]:
        return {
            key: "" for key in FORM_KEYS
        } | {
            "feature_title": "Current validated feature - replace with exact feature title",
            "primary_box": "Replace with the primary box for the current feature",
            "box_type": "Replace with the current box type",
            "protected_paths": "project_freeze_after_update/frozen_features_memory/",
            "do_not_regress_rules": "Do not freeze without current feature validation evidence.",
            "known_warnings": "Starter draft only.",
            "planned_next_step": "Replace placeholders.",
            "notes": "Starter fallback.",
        }

    def test_consumed_newest_hint_does_not_fall_through_to_older_stale_sidecar(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir(project_root)

        current_hint = self._hint(
            "routing_signal_scorer_v2_similarity_test_corpus",
            "Routing Signal Scorer v2 Similarity Test Corpus",
            "LOCAL VALIDATION PENDING: routing_signal_scorer_v2_similarity_test_corpus",
        )
        current_zip = self._write_zip(
            staging / "routing_signal_scorer_v2_similarity_test_corpus_patch.zip",
            current_hint,
        )

        saved_hint = read_freeze_hint_from_patch_zip(current_zip)
        save_freeze_hint_record(project_root, saved_hint, source_signature=saved_hint.get("source"))
        merge = merge_validation_evidence_into_latest_hint(
            project_root,
            "\n".join(
                [
                    "VALIDATION OK: routing_signal_scorer_v2_similarity_test_corpus",
                    "CONTRACT_TEST_OK: corpus-only similarity scenarios validated",
                    "SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_TEST_CORPUS_VALIDATION_OK",
                ]
            ),
            feature_id="routing_signal_scorer_v2_similarity_test_corpus",
            feature_title="Routing Signal Scorer v2 Similarity Test Corpus",
        )
        self.assertTrue(merge.get("ok"), merge)

        paths = build_freeze_hint_intake_paths(project_root)
        consumed = {
            "schema_version": "1.0",
            "kind": "kanda_consumed_freeze_hints",
            "items": [
                {
                    "source": saved_hint.get("source"),
                    "feature_id": saved_hint.get("feature_id"),
                    "feature_title": saved_hint.get("feature_title"),
                    "used_freeze_id": "manual-retry-not-written-yet",
                }
            ],
        }
        paths.consumed_hints.parent.mkdir(parents=True, exist_ok=True)
        paths.consumed_hints.write_text(json.dumps(consumed, indent=2), encoding="utf-8")

        stale_hint = self._hint(
            "freeze_hint_source_shape_tolerance_v1",
            "Freeze Hint Source Shape Tolerance v1",
            "LOCAL VALIDATION PENDING: freeze_hint_source_shape_tolerance_v1",
        )
        stale_zip = self._write_zip(staging / "freeze_hint_source_shape_tolerance_v1_patch.zip", stale_hint)
        stale_time = current_zip.stat().st_mtime - 60
        os.utime(stale_zip, (stale_time, stale_time))

        scan = scan_and_save_latest_freeze_hint(project_root, staging_dir=staging)
        self.assertFalse(scan.get("ok"), scan)
        self.assertIn("routing_signal_scorer_v2_similarity_test_corpus_patch.zip", scan.get("skipped_consumed", []))
        self.assertIn(
            "Stopped at the newest consumed or already-frozen freeze hint sidecar instead of falling through to older stale sidecars.",
            scan.get("warnings", []),
        )

        inputs = build_freeze_form_inputs_from_latest_hint(project_root, self._fallback())
        self.assertEqual(inputs["feature_title"], "Routing Signal Scorer v2 Similarity Test Corpus")
        self.assertNotEqual(inputs["feature_title"], "Freeze Hint Source Shape Tolerance v1")
        self.assertIn(
            "VALIDATION OK: routing_signal_scorer_v2_similarity_test_corpus",
            inputs["validation_evidence_summary"],
        )

    def test_newer_unconsumed_sidecar_can_still_replace_older_validated_latest(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir(project_root)

        older_hint = self._hint(
            "old_validated_feature_v1",
            "Old Validated Feature v1",
            "LOCAL VALIDATION PENDING: old_validated_feature_v1",
        )
        older_zip = self._write_zip(staging / "old_validated_feature_v1_patch.zip", older_hint)
        saved_hint = read_freeze_hint_from_patch_zip(older_zip)
        save_freeze_hint_record(project_root, saved_hint, source_signature=saved_hint.get("source"))
        merge = merge_validation_evidence_into_latest_hint(
            project_root,
            "VALIDATION OK: old_validated_feature_v1",
            feature_id="old_validated_feature_v1",
            feature_title="Old Validated Feature v1",
        )
        self.assertTrue(merge.get("ok"), merge)

        newer_hint = self._hint(
            "new_current_feature_v1",
            "New Current Feature v1",
            "LOCAL VALIDATION PENDING: new_current_feature_v1",
        )
        newer_zip = self._write_zip(staging / "new_current_feature_v1_patch.zip", newer_hint)
        newer_time = older_zip.stat().st_mtime + 60
        os.utime(newer_zip, (newer_time, newer_time))

        inputs = build_freeze_form_inputs_from_latest_hint(project_root, self._fallback())
        self.assertEqual(inputs["feature_title"], "New Current Feature v1")
        self.assertIn("LOCAL VALIDATION PENDING: new_current_feature_v1", inputs["validation_evidence_summary"])

    def test_used_latest_and_consumed_newest_hint_falls_back_instead_of_reopening_old_stale_hint(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir(project_root)

        current_hint = self._hint(
            "routing_signal_scorer_v2_similarity_test_corpus",
            "Routing Signal Scorer v2 Similarity Test Corpus",
            "VALIDATION OK: routing_signal_scorer_v2_similarity_test_corpus",
        )
        current_zip = self._write_zip(
            staging / "routing_signal_scorer_v2_similarity_test_corpus_patch.zip",
            current_hint,
        )
        saved_hint = read_freeze_hint_from_patch_zip(current_zip)
        save_freeze_hint_record(project_root, saved_hint, source_signature=saved_hint.get("source"))

        paths = build_freeze_hint_intake_paths(project_root)
        latest = json.loads(paths.latest_hint.read_text(encoding="utf-8-sig"))
        latest["used_at_utc"] = "2026-06-16T23:45:44Z"
        latest["used_freeze_id"] = "freeze-20260616-routing-signal-scorer-v2-similarity-test-corpus"
        paths.latest_hint.write_text(json.dumps(latest, indent=2), encoding="utf-8")
        paths.consumed_hints.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "kind": "kanda_consumed_freeze_hints",
                    "items": [
                        {
                            "source": saved_hint.get("source"),
                            "feature_id": saved_hint.get("feature_id"),
                            "feature_title": saved_hint.get("feature_title"),
                            "used_freeze_id": latest["used_freeze_id"],
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        stale_hint = self._hint(
            "freeze_hint_source_shape_tolerance_v1",
            "Freeze Hint Source Shape Tolerance v1",
            "LOCAL VALIDATION PENDING: freeze_hint_source_shape_tolerance_v1",
        )
        stale_zip = self._write_zip(staging / "freeze_hint_source_shape_tolerance_v1_patch.zip", stale_hint)
        stale_time = current_zip.stat().st_mtime - 60
        os.utime(stale_zip, (stale_time, stale_time))

        fallback = self._fallback()
        inputs = build_freeze_form_inputs_from_latest_hint(project_root, fallback)
        self.assertEqual(inputs["feature_title"], fallback["feature_title"])
        self.assertNotEqual(inputs["feature_title"], "Freeze Hint Source Shape Tolerance v1")
        self.assertIn(
            "Stopped at the newest consumed or already-frozen freeze hint sidecar instead of falling through to older stale sidecars.",
            inputs["known_warnings"],
        )


if __name__ == "__main__":
    unittest.main()
