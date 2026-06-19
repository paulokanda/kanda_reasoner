from __future__ import annotations

import json
import tempfile
from pathlib import Path
from uuid import uuid4
import unittest
import zipfile

from kanda_reasoner_app.freeze_hint_intake.contract import (
    build_freeze_form_inputs_from_latest_hint,
    build_freeze_hint_intake_paths,
    merge_validation_evidence_into_latest_hint,
    save_freeze_hint_record,
)


class FreezeHintSkipEntryFileFrozenTests(unittest.TestCase):
    def _project(self) -> Path:
        tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        project = Path(tmp.name) / ("active_project_" + uuid4().hex)
        project.mkdir(parents=True)
        staging = Path(project.anchor) / (project.name + "_delete_after_daily_work")
        if staging.exists():
            import shutil
            shutil.rmtree(staging)
        self.addCleanup(lambda: __import__("shutil").rmtree(staging, ignore_errors=True))
        return project

    def _hint(self) -> dict[str, object]:
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
                "project_freeze_after_update/freeze_hint_intake",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "New Local Freeze Entry must fill from project-local freeze hint intake.",
                "Do not store project-specific frozen memory inside project_freeze_ledger.",
            ],
            "validation_evidence_summary": "LOCAL VALIDATION PENDING: freeze_tab_freeze_hint_intake_restore_v1",
            "known_warnings": "Human review is still required.",
            "planned_next_step": "Install locally, validate, then freeze this feature through the tab.",
            "notes": "Saved from freeze hint sidecar.",
        }

    def _save_validated_hint(self, project: Path) -> None:
        save_freeze_hint_record(project, self._hint())
        merged = merge_validation_evidence_into_latest_hint(
            project,
            "\n".join(
                [
                    "VALIDATION OK: freeze_tab_freeze_hint_intake_restore_v1",
                    "CONTRACT_TEST_OK: Freeze tab reads project-local KANDA_FREEZE_HINT.json intake data before safe starter fallback",
                    "STATUS: FREEZE_TAB_FREEZE_HINT_INTAKE_RESTORED",
                ]
            ),
            feature_id="freeze_tab_freeze_hint_intake_restore_v1",
            feature_title="Freeze Tab Freeze Hint Intake Restore v1",
        )
        self.assertTrue(merged.get("ok"), merged)

    def _fallback(self) -> dict[str, str]:
        return {
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

    def _write_entry_file_only(self, project: Path) -> None:
        memory = project / "project_freeze_after_update" / "frozen_features_memory"
        entries = memory / "entries"
        entries.mkdir(parents=True, exist_ok=True)
        entry = entries / "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1.md"
        entry.write_text(
            '---\n'
            'freeze_id: "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1"\n'
            'feature_title: "Freeze Tab Freeze Hint Intake Restore v1"\n'
            'status: "frozen"\n'
            '---\n'
            '# freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1\n',
            encoding="utf-8",
        )
        # Deliberately leave the index stale/missing the entry, reproducing the
        # real-project failure mode from the user's validation.
        (memory / "freeze_index.json").write_text(
            json.dumps({"schema_version": "1.0", "freezes": []}, indent=2),
            encoding="utf-8",
        )

    def test_entry_file_only_frozen_hint_is_marked_used_and_not_refilled(self) -> None:
        project = self._project()
        self._save_validated_hint(project)
        self._write_entry_file_only(project)

        inputs = build_freeze_form_inputs_from_latest_hint(project, self._fallback())

        self.assertNotEqual(inputs["feature_title"], "Freeze Tab Freeze Hint Intake Restore v1")
        paths = build_freeze_hint_intake_paths(project)
        latest = json.loads(paths.latest_hint.read_text(encoding="utf-8-sig"))
        self.assertTrue(latest.get("used_at_utc"))
        self.assertEqual(latest.get("used_freeze_id"), "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1")

    def test_staged_zip_for_entry_file_frozen_feature_is_skipped(self) -> None:
        project = self._project()
        self._write_entry_file_only(project)
        staging = Path(project.anchor) / (project.name + "_delete_after_daily_work")
        staging.mkdir(parents=True)
        zip_path = staging / "freeze_tab_freeze_hint_intake_restore_v1_patch.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(self._hint(), indent=2))
            archive.writestr("dummy.txt", "dummy")

        inputs = build_freeze_form_inputs_from_latest_hint(project, self._fallback())

        self.assertNotEqual(inputs["feature_title"], "Freeze Tab Freeze Hint Intake Restore v1")
        paths = build_freeze_hint_intake_paths(project)
        consumed = json.loads(paths.consumed_hints.read_text(encoding="utf-8-sig"))
        self.assertEqual(len(consumed.get("items", [])), 1)
        self.assertEqual(
            consumed["items"][0]["used_freeze_id"],
            "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1",
        )


if __name__ == "__main__":
    unittest.main()
