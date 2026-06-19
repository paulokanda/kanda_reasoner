"""Regression tests for current-feature freeze formulary auto-fill."""

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"


class FreezeFormularyCurrentFeatureAutofillRegressionTests(unittest.TestCase):
    def _source(self) -> str:
        return SOURCE_PATH.read_text(encoding="utf-8")

    def test_heuristic_autofill_no_longer_uses_stale_local_workflow_title(self) -> None:
        source = self._source()
        self.assertNotIn('"feature_title": "Freeze Feature After Update Local Freeze Workflow v1"', source)
        self.assertIn('"feature_title": "Current validated feature - replace with exact feature title"', source)

    def test_heuristic_autofill_no_longer_injects_legacy_workflow_evidence_or_paths(self) -> None:
        source = self._source()
        self.assertNotIn("VALIDATION OK: startup_freeze_context_channel_v1", source)
        self.assertNotIn("VALIDATION OK: freeze_after_update_tab_local_ai_thread_crash_guard_v1_12", source)
        self.assertNotIn("project_freeze_ledger/freeze_tools/local_freeze_writer.py", source)
        self.assertNotIn("project_freeze_ledger/freeze_tools/expose_freeze_memory.py", source)
        self.assertIn("No validation evidence has been inferred or invented.", source)

    def test_copy_formulary_prompt_tells_ai_to_replace_stale_or_placeholder_data(self) -> None:
        source = self._source()
        self.assertIn("current validated feature only", source)
        self.assertIn("If the current form contains placeholders", source)
        self.assertIn("stale legacy data from another feature", source)
        self.assertIn("replace it using only evidence already present in this chat", source)
        self.assertIn("Current form JSON to review and correct for the current feature only", source)

    def test_project_freeze_memory_rules_remain_protected(self) -> None:
        source = self._source()
        self.assertIn("project_freeze_after_update/frozen_features_memory/", source)
        self.assertIn("Do not store project-specific frozen memory inside project_freeze_ledger.", source)


if __name__ == "__main__":
    unittest.main()
