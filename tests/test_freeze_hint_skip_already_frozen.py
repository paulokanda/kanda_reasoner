from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from kanda_reasoner_app.freeze_hint_intake.contract import (
    build_freeze_form_inputs_from_latest_hint,
    build_freeze_hint_intake_paths,
    merge_validation_evidence_into_latest_hint,
    save_freeze_hint_record,
)


class FreezeHintSkipAlreadyFrozenTests(unittest.TestCase):
    def _project(self) -> Path:
        tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name) / "active_project"

    def _save_hint(self, project: Path) -> None:
        project.mkdir(parents=True)
        hint = {
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
        save_freeze_hint_record(project, hint)
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

    def _write_freeze_index(self, project: Path) -> None:
        memory = project / "project_freeze_after_update" / "frozen_features_memory"
        entries = memory / "entries"
        entries.mkdir(parents=True, exist_ok=True)
        entry = entries / "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1.md"
        entry.write_text("# frozen\n", encoding="utf-8")
        index = {
            "schema_version": "1.0",
            "freezes": [
                {
                    "freeze_id": "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1",
                    "box": "kanda_reasoner_app/freeze_after_update_gui",
                    "status": "frozen",
                    "date": "2026-06-16",
                    "entry": "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1.md",
                    "protected_paths": ["kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py"],
                    "do_not_touch_summary": ["New Local Freeze Entry must fill from project-local freeze hint intake."],
                    "superseded_by": None,
                }
            ],
        }
        (memory / "freeze_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

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

    def test_already_frozen_latest_hint_is_marked_used_and_not_refilled(self) -> None:
        project = self._project()
        self._save_hint(project)
        self._write_freeze_index(project)

        inputs = build_freeze_form_inputs_from_latest_hint(project, self._fallback())

        self.assertEqual(inputs["feature_title"], "Current validated feature - replace with exact feature title")
        self.assertNotIn("Freeze Tab Freeze Hint Intake Restore v1", inputs["feature_title"])

        paths = build_freeze_hint_intake_paths(project)
        latest = json.loads(paths.latest_hint.read_text(encoding="utf-8-sig"))
        self.assertTrue(latest.get("used_at_utc"))
        self.assertEqual(latest.get("used_freeze_id"), "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1")

        consumed = json.loads(paths.consumed_hints.read_text(encoding="utf-8-sig"))
        self.assertEqual(len(consumed.get("items", [])), 1)
        self.assertEqual(
            consumed["items"][0]["used_freeze_id"],
            "freeze-20260616-freeze-tab-freeze-hint-intake-restore-v1",
        )

    def test_unfrozen_latest_hint_still_fills_the_form(self) -> None:
        project = self._project()
        self._save_hint(project)

        inputs = build_freeze_form_inputs_from_latest_hint(project, self._fallback())

        self.assertEqual(inputs["feature_title"], "Freeze Tab Freeze Hint Intake Restore v1")
        self.assertIn(
            "VALIDATION OK: freeze_tab_freeze_hint_intake_restore_v1",
            inputs["validation_evidence_summary"],
        )

    def test_unrelated_freeze_index_entry_does_not_consume_latest_hint(self) -> None:
        project = self._project()
        self._save_hint(project)
        memory = project / "project_freeze_after_update" / "frozen_features_memory"
        memory.mkdir(parents=True, exist_ok=True)
        index = {
            "schema_version": "1.0",
            "freezes": [
                {
                    "freeze_id": "freeze-20260616-unrelated-feature-v1",
                    "box": "some_box",
                    "status": "frozen",
                    "entry": "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-unrelated-feature-v1.md",
                    "protected_paths": [],
                    "do_not_touch_summary": [],
                    "superseded_by": None,
                }
            ],
        }
        (memory / "freeze_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

        inputs = build_freeze_form_inputs_from_latest_hint(project, self._fallback())

        self.assertEqual(inputs["feature_title"], "Freeze Tab Freeze Hint Intake Restore v1")
        paths = build_freeze_hint_intake_paths(project)
        latest = json.loads(paths.latest_hint.read_text(encoding="utf-8-sig"))
        self.assertIsNone(latest.get("used_at_utc"))


if __name__ == "__main__":
    unittest.main()
