"""Public-contract tests for the Freeze Tool cleanup boundary."""

from __future__ import annotations

import importlib
import unittest

from kanda_reasoner_app.freeze_hint_intake import (
    clean_stale_pending_text_after_local_validation,
)


class FreezeHintPublicCleanupContractTests(unittest.TestCase):
    def test_public_cleanup_removes_stale_pending_text_after_validation(self) -> None:
        cleaned = clean_stale_pending_text_after_local_validation(
            {
                "validation_evidence_summary": (
                    "VALIDATION OK: example-feature\nSTATUS: IN_SYNC\n"
                    "Local validation pending."
                ),
                "planned_next_step": "Local validation pending. Freeze next.",
            }
        )
        self.assertIn(
            "VALIDATION OK: example-feature",
            cleaned["validation_evidence_summary"],
        )
        self.assertNotIn("pending", cleaned["validation_evidence_summary"].lower())
        self.assertNotIn("pending", cleaned["planned_next_step"].lower())

    def test_public_cleanup_preserves_pending_text_without_completion(self) -> None:
        cleaned = clean_stale_pending_text_after_local_validation(
            {
                "validation_evidence_summary": "Local validation pending.",
                "planned_next_step": "Run local validation.",
            }
        )
        self.assertIn("pending", cleaned["validation_evidence_summary"].lower())

    def test_complete_public_intake_import_graph_is_importable(self) -> None:
        modules = (
            "kanda_reasoner_app.freeze_hint_intake",
            "kanda_reasoner_app.freeze_hint_intake.contract",
            "kanda_reasoner_app.freeze_hint_intake.records",
            "kanda_reasoner_app.freeze_hint_intake.scanner",
            "kanda_reasoner_app.freeze_hint_intake.autofill",
        )
        for module_name in modules:
            with self.subTest(module=module_name):
                self.assertIsNotNone(importlib.import_module(module_name))


if __name__ == "__main__":
    unittest.main()
