from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from uuid import uuid4

from kanda_reasoner_app.freeze_hint_intake.contract import (
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


class FreezeHintMetadataAliasAutofillTests(unittest.TestCase):
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

    def _write_zip(self, staging: Path, name: str, hint: dict[str, object]) -> Path:
        zip_path = staging / name
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, indent=2))
            archive.writestr("dummy.txt", "dummy")
        return zip_path

    def test_box_paths_alias_populates_mandatory_validated_files(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        hint = {
            "kind": "kanda_freeze_hint",
            "feature_id": "routing_signal_scorer_v2_similarity_runtime_lite_calibration_tests_v1",
            "feature_title": "Routing Signal Scorer v2 Similarity Runtime Lite Calibration Tests v1",
            "box_paths": [
                "tests/test_routing_signal_scorer_v2_similarity_runtime_lite_calibration.py"
            ],
            "validation_evidence_summary": "\n".join(
                [
                    "VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite_calibration_tests_v1",
                    "CONTRACT_TEST_OK: calibration metadata alias autofill validated",
                    "SANDBOX_CALIBRATION_METADATA_ALIAS_AUTOFILL_OK",
                ]
            ),
            "freeze_summary": "Tests-only calibration coverage for the runtime-lite advisor.",
            "do_not_regress": [
                "Runtime-lite remains advisory only.",
                "Do not introduce embeddings, TF-IDF dependency, vector store, or self-learning.",
            ],
            "validation_tests": [
                "tests/test_routing_signal_scorer_v2_similarity_runtime_lite_calibration.py",
                "tests/test_routing_signal_scorer_v2_similarity_runtime_lite.py",
            ],
        }
        self._write_zip(
            staging,
            "routing_signal_scorer_v2_similarity_runtime_lite_calibration_tests_v1_patch.zip",
            hint,
        )

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
        )
        form = state["form_inputs"]

        self.assertEqual(
            form["feature_title"],
            "Routing Signal Scorer v2 Similarity Runtime Lite Calibration Tests v1",
        )
        self.assertEqual(form["primary_box"], "tests")
        self.assertEqual(form["box_type"], "tests-only validation shielding")
        self.assertIn(
            "tests/test_routing_signal_scorer_v2_similarity_runtime_lite_calibration.py",
            form["validated_files"],
        )
        self.assertNotIn("None recorded", form["validated_files"])
        self.assertIn(
            "tests/test_routing_signal_scorer_v2_similarity_runtime_lite_calibration.py",
            form["protected_paths"],
        )
        self.assertIn("Runtime-lite remains advisory only.", form["do_not_regress_rules"])
        self.assertIn("Tests-only calibration coverage", form["notes"])
        self.assertTrue(state["confirm_write_enabled"])

    def test_saved_alias_record_does_not_fall_back_to_starter_placeholders(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        hint = {
            "kind": "kanda_freeze_hint",
            "feature_id": "current_alias_feature_v1",
            "feature_title": "Current Alias Feature v1",
            "box_paths": ["tests/test_current_alias_feature.py"],
            "validation_evidence_summary": "VALIDATION OK: current_alias_feature_v1",
            "do_not_regress": ["Alias metadata must populate freeze form fields."],
        }
        zip_path = self._write_zip(staging, "current_alias_feature_v1_patch.zip", hint)
        normalized_hint = read_freeze_hint_from_patch_zip(zip_path)
        save_freeze_hint_record(project_root, normalized_hint, source_signature=normalized_hint.get("source"))

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
        )
        form = state["form_inputs"]

        self.assertEqual(form["feature_title"], "Current Alias Feature v1")
        self.assertEqual(form["primary_box"], "tests")
        self.assertIn("tests/test_current_alias_feature.py", form["validated_files"])
        self.assertNotEqual(
            form["primary_box"],
            "Replace with the primary box for the current feature",
        )
        self.assertNotEqual(form["box_type"], "Replace with the current box type")
        self.assertTrue(state["confirm_write_enabled"])


if __name__ == "__main__":
    unittest.main()
