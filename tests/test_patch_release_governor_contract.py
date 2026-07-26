from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from kanda_reasoner_app.patch_governance.installer_template import render_installer_template
from kanda_reasoner_app.patch_governance.models import (
    FREEZE_HINT_FILENAME,
    build_freeze_payload,
    freeze_form_json_text,
)
from kanda_reasoner_app.patch_governance.validator import (
    PatchZipContractError,
    validate_install_script_text,
    validate_patch_zip,
)


class PatchReleaseGovernorContractTests(unittest.TestCase):
    def _payload(self) -> dict[str, object]:
        return build_freeze_payload(
            patch_name="release_guard_zip_contract_v1_patch",
            feature_id="release_guard_zip_delivery_contract_v1",
            feature_title="Release Guard ZIP Delivery Contract v1",
            primary_box="kanda_reasoner_app/patch_governance",
            box_type="Patch Delivery Governance / Release Gate",
            validated_files=[
                "kanda_reasoner_app/patch_governance/models.py",
                "kanda_reasoner_app/patch_governance/validator.py",
                "kanda_reasoner_app/patch_governance/installer_template.ps1",
                "tests/test_patch_release_governor_contract.py",
            ],
            generated_files=[
                "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip",
                "kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md",
            ],
            protected_paths=[
                "kanda_reasoner_app/patch_governance/",
                "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
                "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            do_not_regress_rules=[
                "Patch ZIP delivery must fail closed when root-level KANDA_FREEZE_HINT.json is missing or incomplete.",
                "Installer logic must stage from the project drive root into <project>_delete_after_daily_work before extraction.",
                "Root-level delivery metadata must not be duplicated inside the install payload folder.",
            ],
            validation_evidence_summary="LOCAL VALIDATION PENDING: release_guard_zip_delivery_contract_v1",
            known_warnings="User-local validation remains required before Confirm and Write.",
            planned_next_step="Run local install and validation, then merge validation evidence into freeze intake before Confirm and Write.",
            notes="Single-source freeze payload feeds both root sidecar and form JSON.",
        )

    def _zip_with_hint(self, hint: dict[str, object]) -> Path:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "release_guard_zip_contract_v1_patch.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(FREEZE_HINT_FILENAME, json.dumps(hint, indent=2))
            archive.writestr("release_guard_zip_contract_v1_patch/dummy.txt", "dummy")
        return path

    def test_valid_zip_with_root_hint_passes_contract(self) -> None:
        path = self._zip_with_hint(self._payload())
        report = validate_patch_zip(path)
        self.assertTrue(report["ok"])
        self.assertEqual(report["feature_id"], "release_guard_zip_delivery_contract_v1")

    def test_missing_root_hint_fails_closed(self) -> None:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "bad_patch.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("bad_patch/dummy.txt", "dummy")
        with self.assertRaisesRegex(PatchZipContractError, "Missing root-level"):
            validate_patch_zip(path)

    def test_empty_validated_files_fails_closed(self) -> None:
        hint = self._payload()
        hint["validated_files"] = []
        path = self._zip_with_hint(hint)
        with self.assertRaisesRegex(PatchZipContractError, "validated_files"):
            validate_patch_zip(path)

    def test_placeholder_title_fails_closed(self) -> None:
        hint = self._payload()
        hint["feature_title"] = "Current validated feature - replace with exact feature title"
        path = self._zip_with_hint(hint)
        with self.assertRaisesRegex(PatchZipContractError, "placeholder"):
            validate_patch_zip(path)

    def test_invalid_kind_fails_closed_for_app_compatibility(self) -> None:
        hint = self._payload()
        hint["kind"] = "kanda_patch_freeze_hint"
        path = self._zip_with_hint(hint)
        with self.assertRaisesRegex(PatchZipContractError, "kind must be kanda_freeze_hint"):
            validate_patch_zip(path)

    def test_duplicate_hint_inside_payload_fails_closed(self) -> None:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "bad_duplicate_patch.zip"
        hint_text = json.dumps(self._payload(), indent=2)
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(FREEZE_HINT_FILENAME, hint_text)
            archive.writestr("bad_duplicate_patch/KANDA_FREEZE_HINT.json", hint_text)
        with self.assertRaisesRegex(PatchZipContractError, "must not be duplicated"):
            validate_patch_zip(path)

    def test_form_json_and_sidecar_share_one_payload_source(self) -> None:
        hint = self._payload()
        text = freeze_form_json_text(hint)
        self.assertTrue(text.startswith("KANDA_FREEZE_FORM_JSON_BEGIN\n"))
        body = text.split("\n", 1)[1].rsplit("\n", 1)[0]
        parsed = json.loads(body)
        self.assertEqual(parsed["feature_title"], hint["feature_title"])
        self.assertEqual(parsed["validated_files"], hint["validated_files"])
        self.assertEqual(parsed["validation_evidence_summary"], hint["validation_evidence_summary"])

    def test_canonical_installer_template_uses_staging_without_generic_paths(self) -> None:
        script = render_installer_template(
            project_root_placeholder="C:\\PATH\\TO\\PROJECT",
            patch_name="release_guard_zip_contract_v1_patch",
            payload_folder="release_guard_zip_contract_v1_patch",
        )
        report = validate_install_script_text(script)
        self.assertTrue(report["ok"])
        lowered = script.lower()
        self.assertIn("_delete_after_daily_work", lowered)
        self.assertIn("[system.io.path]::getpathroot", lowered)
        self.assertNotIn("downloads", lowered)
        self.assertNotIn("desktop", lowered)


if __name__ == "__main__":
    unittest.main()
