from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from uuid import uuid4

from kanda_reasoner_app.freeze_hint_intake.contract import (
    build_freeze_hint_intake_paths,
    merge_validation_evidence_into_latest_hint,
    read_freeze_hint_from_patch_zip,
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


class FreezeHintAutofillStateMachineTests(unittest.TestCase):
    def _project_root(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name) / ("active_project_" + uuid4().hex)
        root.mkdir(parents=True)
        return root

    def _staging_dir(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        staging = Path(temp_dir.name) / ("staging_" + uuid4().hex)
        staging.mkdir(parents=True)
        return staging

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

    def _hint(self, feature_id: str, feature_title: str, evidence: str) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "kind": "kanda_freeze_hint",
            "feature_id": feature_id,
            "feature_title": feature_title,
            "primary_box": "kanda_reasoner_app/freeze_hint_intake",
            "box_type": "Freeze Hint Intake / State Machine",
            "validated_files": [
                "kanda_reasoner_app/freeze_hint_intake/contract.py",
                "tests/test_freeze_hint_autofill_state_machine.py",
            ],
            "generated_files": [],
            "protected_paths": [
                "kanda_reasoner_app/freeze_hint_intake/",
                "project_freeze_after_update/freeze_hint_intake/",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "Autofill source arbitration must preserve the current validated feature.",
                "Do not store project-specific frozen memory inside project_freeze_ledger.",
            ],
            "validation_evidence_summary": evidence,
            "known_warnings": "Human review remains required before Confirm and Write.",
            "planned_next_step": "Preview Freeze Entry, then Confirm and Write after human review.",
            "notes": "State-machine test hint.",
        }

    def _write_zip(self, staging: Path, name: str, hint: dict[str, object]) -> Path:
        zip_path = staging / name
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, indent=2))
            archive.writestr("dummy.txt", "dummy")
        return zip_path

    def _save_latest_from_zip(self, project_root: Path, zip_path: Path) -> dict[str, object]:
        hint = read_freeze_hint_from_patch_zip(zip_path)
        return save_freeze_hint_record(project_root, hint, source_signature=hint.get("source"))

    def _merge_validation(self, project_root: Path, feature_id: str, feature_title: str) -> None:
        evidence = "\n".join(
            [
                "VALIDATION OK: " + feature_id,
                "CONTRACT_TEST_OK: state-machine autofill scenario validated",
                "SANDBOX_STATE_MACHINE_VALIDATION_OK",
            ]
        )
        result = merge_validation_evidence_into_latest_hint(
            project_root,
            evidence,
            feature_id=feature_id,
            feature_title=feature_title,
        )
        self.assertTrue(result.get("ok"), result)

    def _write_freeze_index(self, project_root: Path, feature_slug: str, title: str) -> None:
        memory = project_root / "project_freeze_after_update" / "frozen_features_memory"
        entries = memory / "entries"
        entries.mkdir(parents=True, exist_ok=True)
        freeze_id = "freeze-20260616-" + feature_slug.replace("_", "-")
        entry = entries / (freeze_id + ".md")
        entry.write_text(
            "---\n"
            + "freeze_id: \"" + freeze_id + "\"\n"
            + "feature_title: \"" + title + "\"\n"
            + "status: \"frozen\"\n"
            + "---\n",
            encoding="utf-8",
        )
        index = {
            "schema_version": "1.0",
            "freezes": [
                {
                    "freeze_id": freeze_id,
                    "feature_title": title,
                    "box": "kanda_reasoner_app/freeze_hint_intake",
                    "status": "frozen",
                    "entry": "project_freeze_after_update/frozen_features_memory/entries/" + freeze_id + ".md",
                    "superseded_by": None,
                }
            ],
        }
        (memory / "freeze_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

    def test_preview_snapshot_wins_over_disk_sources(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        stale = self._hint(
            "freeze_hint_source_shape_tolerance_v1",
            "Freeze Hint Source Shape Tolerance v1",
            "VALIDATION OK: freeze_hint_source_shape_tolerance_v1",
        )
        self._write_zip(staging, "freeze_hint_source_shape_tolerance_v1_patch.zip", stale)

        preview = self._hint(
            "routing_signal_scorer_v2_similarity_test_corpus",
            "Routing Signal Scorer v2 Similarity Test Corpus",
            "VALIDATION OK: routing_signal_scorer_v2_similarity_test_corpus",
        )
        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
            preview_form_inputs=preview,
        )

        self.assertEqual(state["source_kind"], "preview_session_snapshot")
        self.assertEqual(state["form_inputs"]["feature_title"], "Routing Signal Scorer v2 Similarity Test Corpus")
        self.assertTrue(state["confirm_write_enabled"])
        self.assertTrue(state["preview_read_only"])

    def test_manual_review_mismatch_is_rejected_and_latest_is_preserved(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        current = self._hint(
            "current_feature_v1",
            "Current Feature v1",
            "LOCAL VALIDATION PENDING: current_feature_v1",
        )
        current_zip = self._write_zip(staging, "current_feature_v1_patch.zip", current)
        self._save_latest_from_zip(project_root, current_zip)
        self._merge_validation(project_root, "current_feature_v1", "Current Feature v1")

        manual = self._hint(
            "other_feature_v1",
            "Other Feature v1",
            "VALIDATION OK: other_feature_v1",
        )
        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
            manual_form_inputs=manual,
        )

        self.assertEqual(state["form_inputs"]["feature_title"], "Current Feature v1")
        self.assertNotEqual(state["form_inputs"]["feature_title"], "Other Feature v1")
        self.assertIn("VALIDATION OK: current_feature_v1", state["form_inputs"]["validation_evidence_summary"])

    def test_manual_review_match_with_validation_can_fill_current_feature(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        current = self._hint(
            "current_feature_v1",
            "Current Feature v1",
            "LOCAL VALIDATION PENDING: current_feature_v1",
        )
        current_zip = self._write_zip(staging, "current_feature_v1_patch.zip", current)
        self._save_latest_from_zip(project_root, current_zip)
        self._merge_validation(project_root, "current_feature_v1", "Current Feature v1")

        manual = self._hint(
            "current_feature_v1",
            "Current Feature v1",
            "VALIDATION OK: current_feature_v1",
        )
        manual["notes"] = "Manual AI review was accepted for the current feature."
        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
            manual_form_inputs=manual,
        )

        self.assertEqual(state["source_kind"], "manual_ai_review_json")
        self.assertEqual(state["form_inputs"]["feature_title"], "Current Feature v1")
        self.assertIn("Manual AI review", state["form_inputs"]["notes"])
        self.assertTrue(state["confirm_write_enabled"])

    def test_valid_latest_without_staged_sidecar_does_not_fall_back_to_starter(self) -> None:
        project_root = self._project_root()
        hint = self._hint(
            "latest_feature_v1",
            "Latest Feature v1",
            "VALIDATION OK: latest_feature_v1",
        )
        save_freeze_hint_record(project_root, hint)

        state = resolve_freeze_hint_autofill_state(project_root, self._fallback(), staging_dir=self._staging_dir())

        self.assertEqual(state["form_inputs"]["feature_title"], "Latest Feature v1")
        self.assertTrue(state["confirm_write_enabled"])
        self.assertIn("VALIDATION OK: latest_feature_v1", state["form_inputs"]["validation_evidence_summary"])

    def test_no_valid_evidence_uses_starter_fallback_and_disables_confirm(self) -> None:
        project_root = self._project_root()
        state = resolve_freeze_hint_autofill_state(project_root, self._fallback(), staging_dir=self._staging_dir())

        self.assertEqual(state["source_kind"], "starter_fallback")
        self.assertEqual(state["form_inputs"]["feature_title"], "Current validated feature - replace with exact feature title")
        self.assertFalse(state["confirm_write_enabled"])
        self.assertTrue(state["preview_read_only"])

    def test_latest_without_recognizer_marker_disables_confirm_write(self) -> None:
        project_root = self._project_root()
        hint = self._hint(
            "pending_feature_v1",
            "Pending Feature v1",
            "LOCAL VALIDATION PENDING: pending_feature_v1",
        )
        save_freeze_hint_record(project_root, hint)

        state = resolve_freeze_hint_autofill_state(project_root, self._fallback(), staging_dir=self._staging_dir())

        self.assertEqual(state["form_inputs"]["feature_title"], "Pending Feature v1")
        self.assertFalse(state["confirm_write_enabled"])
        self.assertEqual(state["validation_evidence_status"], "missing_or_unrecognized")

    def test_consumed_current_sidecar_blocks_older_stale_sidecar_and_preserves_latest(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        current = self._hint(
            "routing_signal_scorer_v2_similarity_test_corpus",
            "Routing Signal Scorer v2 Similarity Test Corpus",
            "LOCAL VALIDATION PENDING: routing_signal_scorer_v2_similarity_test_corpus",
        )
        current_zip = self._write_zip(staging, "routing_signal_scorer_v2_similarity_test_corpus_patch.zip", current)
        saved_hint = read_freeze_hint_from_patch_zip(current_zip)
        save_freeze_hint_record(project_root, saved_hint, source_signature=saved_hint.get("source"))
        self._merge_validation(
            project_root,
            "routing_signal_scorer_v2_similarity_test_corpus",
            "Routing Signal Scorer v2 Similarity Test Corpus",
        )

        paths = build_freeze_hint_intake_paths(project_root)
        paths.consumed_hints.parent.mkdir(parents=True, exist_ok=True)
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
                            "used_freeze_id": "manual-retry-not-written-yet",
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        stale = self._hint(
            "freeze_hint_source_shape_tolerance_v1",
            "Freeze Hint Source Shape Tolerance v1",
            "VALIDATION OK: freeze_hint_source_shape_tolerance_v1",
        )
        stale_zip = self._write_zip(staging, "freeze_hint_source_shape_tolerance_v1_patch.zip", stale)
        stale_time = current_zip.stat().st_mtime - 60
        os.utime(stale_zip, (stale_time, stale_time))

        state = resolve_freeze_hint_autofill_state(project_root, self._fallback(), staging_dir=staging)

        self.assertEqual(state["form_inputs"]["feature_title"], "Routing Signal Scorer v2 Similarity Test Corpus")
        self.assertNotEqual(state["form_inputs"]["feature_title"], "Freeze Hint Source Shape Tolerance v1")
        self.assertIn("VALIDATION OK: routing_signal_scorer_v2_similarity_test_corpus", state["form_inputs"]["validation_evidence_summary"])

    def test_newer_unconsumed_sidecar_replaces_older_validated_latest(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        older = self._hint("older_feature_v1", "Older Feature v1", "VALIDATION OK: older_feature_v1")
        older_zip = self._write_zip(staging, "older_feature_v1_patch.zip", older)
        self._save_latest_from_zip(project_root, older_zip)
        self._merge_validation(project_root, "older_feature_v1", "Older Feature v1")

        newer = self._hint("newer_feature_v1", "Newer Feature v1", "LOCAL VALIDATION PENDING: newer_feature_v1")
        newer_zip = self._write_zip(staging, "newer_feature_v1_patch.zip", newer)
        new_time = older_zip.stat().st_mtime + 60
        os.utime(newer_zip, (new_time, new_time))

        state = resolve_freeze_hint_autofill_state(project_root, self._fallback(), staging_dir=staging)

        self.assertEqual(state["form_inputs"]["feature_title"], "Newer Feature v1")
        self.assertIn("LOCAL VALIDATION PENDING: newer_feature_v1", state["form_inputs"]["validation_evidence_summary"])
        self.assertFalse(state["confirm_write_enabled"])

    def test_already_frozen_latest_feature_is_not_presented_as_pending(self) -> None:
        project_root = self._project_root()
        hint = self._hint(
            "frozen_feature_v1",
            "Frozen Feature v1",
            "VALIDATION OK: frozen_feature_v1",
        )
        save_freeze_hint_record(project_root, hint)
        self._write_freeze_index(project_root, "frozen_feature_v1", "Frozen Feature v1")

        state = resolve_freeze_hint_autofill_state(project_root, self._fallback(), staging_dir=self._staging_dir())

        self.assertEqual(state["source_kind"], "starter_fallback")
        self.assertNotEqual(state["form_inputs"]["feature_title"], "Frozen Feature v1")
        self.assertFalse(state["confirm_write_enabled"])

    def test_cross_project_staging_data_is_not_used_when_scanning_selected_project(self) -> None:
        project_a = self._project_root()
        project_b = self._project_root()
        staging_a = self._staging_dir()
        staging_b = self._staging_dir()
        hint_a = self._hint(
            "project_a_feature_v1",
            "Project A Feature v1",
            "VALIDATION OK: project_a_feature_v1",
        )
        self._write_zip(staging_a, "project_a_feature_v1_patch.zip", hint_a)

        state_b = resolve_freeze_hint_autofill_state(project_b, self._fallback(), staging_dir=staging_b)

        self.assertEqual(state_b["source_kind"], "starter_fallback")
        self.assertNotEqual(state_b["form_inputs"]["feature_title"], "Project A Feature v1")
        shutil.rmtree(project_a, ignore_errors=True)

    def test_consumed_newer_unrelated_sidecar_does_not_hide_current_unconsumed_patch(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()

        consumed_feature = self._hint(
            "freeze_hint_autofill_state_machine_tests_v1",
            "Freeze Hint Autofill State Machine Tests v1",
            "VALIDATION OK: freeze_hint_autofill_state_machine_tests_v1",
        )
        consumed_zip = self._write_zip(
            staging,
            "freeze_hint_autofill_state_machine_tests_v1_patch.zip",
            consumed_feature,
        )
        consumed_hint = read_freeze_hint_from_patch_zip(consumed_zip)
        paths = build_freeze_hint_intake_paths(project_root)
        paths.consumed_hints.parent.mkdir(parents=True, exist_ok=True)
        paths.consumed_hints.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "kind": "kanda_consumed_freeze_hints",
                    "items": [
                        {
                            "source": consumed_hint.get("source"),
                            "feature_id": consumed_hint.get("feature_id"),
                            "feature_title": consumed_hint.get("feature_title"),
                            "used_freeze_id": "freeze-20260617-freeze-hint-autofill-state-machine-tests-v1",
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        current_feature = self._hint(
            "routing_signal_scorer_v2_similarity_runtime_lite",
            "Routing Signal Scorer v2 Similarity Runtime Lite",
            "VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite",
        )
        current_zip = self._write_zip(
            staging,
            "routing_signal_scorer_v2_similarity_runtime_lite_patch.zip",
            current_feature,
        )

        older_time = consumed_zip.stat().st_mtime - 60
        os.utime(current_zip, (older_time, older_time))

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
        )

        self.assertEqual(
            state["form_inputs"]["feature_title"],
            "Routing Signal Scorer v2 Similarity Runtime Lite",
        )
        self.assertTrue(state["confirm_write_enabled"])
        self.assertIn(
            "freeze_hint_autofill_state_machine_tests_v1_patch.zip",
            state.get("scan_result", {}).get("skipped_consumed", []),
        )
        self.assertIn(
            "VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite",
            state["form_inputs"]["validation_evidence_summary"],
        )

    def test_unrelated_frozen_repair_entry_body_mention_does_not_hide_current_patch(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()

        memory = project_root / "project_freeze_after_update" / "frozen_features_memory"
        entries = memory / "entries"
        entries.mkdir(parents=True, exist_ok=True)
        repair_entry = entries / "freeze-20260617-freeze-hint-consumed-newer-scan-continuation-v1.md"
        repair_entry.write_text(
            "---\n"
            + "freeze_id: \"freeze-20260617-freeze-hint-consumed-newer-scan-continuation-v1\"\n"
            + "feature_title: \"Freeze Hint Consumed Newer Scan Continuation v1\"\n"
            + "status: \"frozen\"\n"
            + "---\n"
            + "# Freeze Hint Consumed Newer Scan Continuation v1\n"
            + "CONTRACT_TEST_OK: consumed/frozen newer sidecars skipped and "
            + "routing_signal_scorer_v2_similarity_runtime_lite validation preserved.\n",
            encoding="utf-8",
        )
        (memory / "freeze_index.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "freezes": [
                        {
                            "freeze_id": "freeze-20260617-freeze-hint-consumed-newer-scan-continuation-v1",
                            "feature_title": "Freeze Hint Consumed Newer Scan Continuation v1",
                            "status": "frozen",
                            "entry": "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-freeze-hint-consumed-newer-scan-continuation-v1.md",
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        current_feature = self._hint(
            "routing_signal_scorer_v2_similarity_runtime_lite",
            "Routing Signal Scorer v2 Similarity Runtime Lite",
            "VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite",
        )
        self._write_zip(
            staging,
            "routing_signal_scorer_v2_similarity_runtime_lite_patch.zip",
            current_feature,
        )

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
        )

        self.assertEqual(
            state["form_inputs"]["feature_title"],
            "Routing Signal Scorer v2 Similarity Runtime Lite",
        )
        self.assertTrue(state["confirm_write_enabled"])
        self.assertIn(
            "VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite",
            state["form_inputs"]["validation_evidence_summary"],
        )

    def test_false_consumed_record_with_unrelated_freeze_id_does_not_hide_current_patch(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()

        current_feature = self._hint(
            "routing_signal_scorer_v2_similarity_runtime_lite",
            "Routing Signal Scorer v2 Similarity Runtime Lite",
            "VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite",
        )
        current_zip = self._write_zip(
            staging,
            "routing_signal_scorer_v2_similarity_runtime_lite_patch.zip",
            current_feature,
        )
        current_hint = read_freeze_hint_from_patch_zip(current_zip)

        paths = build_freeze_hint_intake_paths(project_root)
        paths.consumed_hints.parent.mkdir(parents=True, exist_ok=True)
        paths.consumed_hints.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "kind": "kanda_consumed_freeze_hints",
                    "items": [
                        {
                            "source": current_hint.get("source"),
                            "feature_id": current_hint.get("feature_id"),
                            "feature_title": current_hint.get("feature_title"),
                            "used_freeze_id": "freeze-20260617-freeze-hint-consumed-newer-scan-continuation-v1",
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
        )

        self.assertEqual(
            state["form_inputs"]["feature_title"],
            "Routing Signal Scorer v2 Similarity Runtime Lite",
        )
        self.assertTrue(state["confirm_write_enabled"])
        self.assertIn(
            "VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite",
            state["form_inputs"]["validation_evidence_summary"],
        )




if __name__ == "__main__":
    unittest.main()
