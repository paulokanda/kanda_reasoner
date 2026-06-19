from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from uuid import uuid4

from kanda_reasoner_app.freeze_hint_intake.contract import (
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


class FreezeHintNestedPatchBoundaryFormularyAutofillTests(unittest.TestCase):
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

    def _kbsc_nested_hint(self) -> dict[str, object]:
        return {
            "kind": "kanda_freeze_hint",
            "schema_version": "1.0",
            "feature_id": "kanda_box_shielding_canon_routing_registration_v1",
            "feature_title": "KANDA Box Shielding Canon Routing Registration v1",
            "feature_type": "prompt_library_routing_canonization",
            "owning_box": "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries + prompt routing indexes",
            "summary": "Registers KBSC as an on-request routable context asset and routing canon.",
            "validation_evidence_summary": "\n".join(
                [
                    "VALIDATION OK: kanda_box_shielding_canon_routing_registration_v1",
                    "CONTRACT_TEST_OK: KBSC routing registration validated",
                    "SANDBOX_KANDA_BOX_SHIELDING_CANON_ROUTING_REGISTRATION_V1_VALIDATION_OK",
                ]
            ),
            "protected_architecture_characteristics": [
                "prompt_registered_as_routable_context_asset",
                "on_request_not_always_startup_loaded",
                "shield_before_stronger_ml",
            ],
            "patch_boundary": {
                "allowed_paths": [
                    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md",
                    "kanda_prompt_workspace/prompt_library/METADATA/kanda_box_shielding_canon.meta.json",
                    "kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json",
                    "tests/test_kbsc_routing_registration.py",
                ],
                "forbidden_paths": [
                    "kanda_reasoner_app/freeze_hint_intake",
                    "kanda_reasoner_app/freeze_after_update",
                    "kanda_reasoner_app/freeze_after_update_gui",
                    "project_freeze_ledger",
                ],
            },
            "freeze_warning": "Freeze only after local validation passes. Do not freeze placeholder titles.",
            "expected_freeze_title": "KANDA Box Shielding Canon Routing Registration v1",
        }

    def _write_zip(self, staging: Path, hint: dict[str, object]) -> Path:
        zip_path = staging / "kanda_box_shielding_canon_routing_registration_v1_patch.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, indent=2))
            archive.writestr("dummy.txt", "dummy")
        return zip_path

    def test_nested_patch_boundary_allowed_paths_populate_mandatory_formulary_fields(self) -> None:
        project_root = self._project_root()
        staging = self._staging_dir()
        self._write_zip(staging, self._kbsc_nested_hint())

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            staging_dir=staging,
        )
        form = state["form_inputs"]

        self.assertEqual(form["feature_title"], "KANDA Box Shielding Canon Routing Registration v1")
        self.assertIn("04_box_architecture_and_boundaries", form["primary_box"])
        self.assertEqual(form["box_type"], "prompt library routing canonization")
        self.assertIn("kanda_box_shielding_canon.md", form["validated_files"])
        self.assertIn("tests/test_kbsc_routing_registration.py", form["validated_files"])
        self.assertIn("kanda_box_shielding_canon.md", form["protected_paths"])
        self.assertIn("project_freeze_after_update/frozen_features_memory/", form["protected_paths"])
        self.assertIn("Preserve on request not always startup loaded.", form["do_not_regress_rules"])
        self.assertIn("Registers KBSC as an on-request", form["notes"])
        self.assertIn("Freeze only after local validation passes", form["known_warnings"])
        self.assertIn("Preview Freeze Entry", form["planned_next_step"])
        self.assertEqual(state["mandatory_fields_status"], "complete")
        self.assertTrue(state["confirm_write_enabled"])

        for value in form.values():
            self.assertNotIn("Replace with", str(value))
            self.assertNotIn("Starter draft only", str(value))
            self.assertNotIn("None recorded", str(value))

    def test_saved_legacy_record_is_repaired_from_raw_nested_hint_when_form_inputs_are_blank(self) -> None:
        project_root = self._project_root()
        hint = self._kbsc_nested_hint()
        record = save_freeze_hint_record(
            project_root,
            hint,
            source_signature={"source_path": "kanda_box_shielding_canon_routing_registration_v1_patch.zip"},
        )
        # Simulate a legacy bad saved record produced before the nested sidecar repair.
        record["form_inputs"].update(
            {
                "primary_box": "Replace with the primary box for the current feature",
                "box_type": "Replace with the current box type",
                "validated_files": "",
                "known_warnings": "Starter draft only.",
                "planned_next_step": "Replace placeholders.",
                "notes": "Starter fallback.",
            }
        )
        latest = project_root / "project_freeze_after_update" / "freeze_hint_intake" / "latest_freeze_hint.json"
        latest.write_text(json.dumps(record, indent=2), encoding="utf-8")

        state = resolve_freeze_hint_autofill_state(project_root, self._fallback(), staging_dir=self._staging_dir())
        form = state["form_inputs"]

        self.assertIn("04_box_architecture_and_boundaries", form["primary_box"])
        self.assertIn("kanda_box_shielding_canon.md", form["validated_files"])
        self.assertNotIn("Replace with", form["primary_box"])
        self.assertNotIn("Starter draft only", form["known_warnings"])
        self.assertEqual(state["mandatory_fields_status"], "complete")
        self.assertTrue(state["confirm_write_enabled"])

    def test_confirm_write_signal_is_disabled_when_mandatory_validated_files_are_missing(self) -> None:
        project_root = self._project_root()
        form = self._fallback() | {
            "feature_title": "Current Validated Feature v1",
            "primary_box": "kanda_reasoner_app/example_box",
            "box_type": "Module Box",
            "validated_files": "",
            "validation_evidence_summary": "VALIDATION OK: current_validated_feature_v1",
        }

        state = resolve_freeze_hint_autofill_state(
            project_root,
            self._fallback(),
            preview_form_inputs=form,
        )

        self.assertEqual(state["mandatory_fields_status"], "missing_or_placeholder")
        self.assertFalse(state["confirm_write_enabled"])


if __name__ == "__main__":
    unittest.main()
