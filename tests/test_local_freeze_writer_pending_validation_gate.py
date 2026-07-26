from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from project_freeze_ledger.freeze_tools.local_freeze_writer import (
    preview_freeze_entry,
    write_confirmed_freeze_entry,
)


class LocalFreezeWriterPendingValidationGateTests(unittest.TestCase):
    def _project_root(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name) / "active_project"
        root.mkdir(parents=True)
        return root

    def _inputs(self, evidence: str) -> dict[str, object]:
        return {
            "feature_title": "Freeze Form Pending Validation Gate v1",
            "primary_box": "project_freeze_ledger/freeze_tools/local_freeze_writer.py",
            "box_type": "Freeze Writer Validation Gate",
            "validated_files": [
                "project_freeze_ledger/freeze_tools/local_freeze_writer.py",
                "tests/test_local_freeze_writer_pending_validation_gate.py",
            ],
            "generated_files": [],
            "protected_paths": [
                "project_freeze_ledger/freeze_tools/",
                "project_freeze_after_update/frozen_features_memory/",
            ],
            "do_not_regress_rules": [
                "Do not write frozen memory while local validation remains unresolved.",
                "Remove stale sidecar wording when real local validation markers exist.",
            ],
            "validation_evidence_summary": evidence,
            "known_warnings": "Pre-validation sidecar only. User-local validation must be run before Confirm and Write.",
            "planned_next_step": "Run the delivered validation block before Confirm and Write.",
            "notes": "User-local validation remains required before freeze confirmation.",
        }

    def test_sandbox_pending_evidence_blocks_preview_and_write(self) -> None:
        project_root = self._project_root()
        evidence = (
            "SANDBOX VALIDATION OK: python -m unittest tests.test_example\n"
            "LOCAL VALIDATION PENDING: run the delivered validation block before Confirm and Write."
        )
        preview = preview_freeze_entry(project_root, self._inputs(evidence))

        self.assertFalse(preview["is_writable"])
        combined_errors = "\n".join(preview.get("errors") or [])
        self.assertIn("local validation is still pending", combined_errors)

        with self.assertRaises(Exception):
            write_confirmed_freeze_entry(project_root, preview, confirmation=True)

    def test_local_validation_marker_cleans_stale_pending_text_before_render(self) -> None:
        project_root = self._project_root()
        evidence = (
            "VALIDATION OK: freeze_form_pending_validation_gate_v1\n"
            "STATUS: IN_SYNC\n"
            "LOCAL VALIDATION PENDING: stale sidecar wording should be removed."
        )
        preview = preview_freeze_entry(project_root, self._inputs(evidence))

        self.assertTrue(preview["is_writable"], preview.get("errors"))
        combined = "\n".join(
            [
                str(preview.get("validation_evidence_summary") or ""),
                str(preview.get("known_warnings") or ""),
                str(preview.get("planned_next_step") or ""),
                str(preview.get("notes") or ""),
                str(preview.get("markdown") or ""),
            ]
        )
        self.assertIn("VALIDATION OK: freeze_form_pending_validation_gate_v1", combined)
        self.assertNotIn("LOCAL VALIDATION PENDING", combined)
        self.assertNotIn("Pre-validation sidecar only", combined)
        self.assertNotIn("User-local validation must be run", combined)
        self.assertNotIn("before Confirm and Write", combined)


if __name__ == "__main__":
    unittest.main()
