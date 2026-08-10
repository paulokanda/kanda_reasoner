# project-path: tests/test_engineering_diagnostics_wave2u_gui_scale.py
"""GUI-source and high-volume policy contracts for Wave 2U."""

from __future__ import annotations

from pathlib import Path
import time
import unittest

from kanda_reasoner_app.engineering_diagnostics_patch_preview import (
    patch_preview_approval_token,
)


class EngineeringDiagnosticsWave2UGuiScaleTests(unittest.TestCase):
    """Keep Patch Preview separate, observable, and cheap to project."""

    def test_gui_declares_separate_patch_preview_control(self) -> None:
        root = Path(__file__).resolve().parents[1]
        ui = (root / "kanda_reasoner_app/engineering_diagnostics_gui/patch_preview_ui.py").read_text()
        tab = (root / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py").read_text()
        self.assertIn("engineeringDiagnosticsPatchPreviewButton", ui)
        self.assertIn("Create Patch Preview", ui)
        self.assertIn("create_patch_preview_button", tab)
        self.assertNotIn("Authorize Project Update", ui)
        self.assertNotIn("apply_ruff_correction_preview", ui)

    def test_gui_requires_patch_prepared_safe_unfrozen_ready_state(self) -> None:
        root = Path(__file__).resolve().parents[1]
        ui = (root / "kanda_reasoner_app/engineering_diagnostics_gui/patch_preview_ui.py").read_text()
        for fragment in (
            'view.decision_state == "PATCH_PREPARED"',
            'view.owner_status == "READY"',
            'view.frozen_status == "UNFROZEN"',
            'intent.action_class == "SAFE_MECHANICAL_FIX_AVAILABLE"',
        ):
            self.assertIn(fragment, ui)

    def test_preview_policy_projection_scales_to_25000_issue_tokens(self) -> None:
        started = time.perf_counter()
        values = tuple(patch_preview_approval_token(f"{index:064x}") for index in range(25000))
        elapsed = time.perf_counter() - started
        self.assertEqual(len(values), 25000)
        self.assertLess(elapsed, 1.5)

    def test_patch_preview_box_has_no_sqlite_or_source_apply_surface(self) -> None:
        root = Path(__file__).resolve().parents[1] / "kanda_reasoner_app/engineering_diagnostics_patch_preview"
        text = "\n".join(path.read_text() for path in root.glob("*.py"))
        self.assertNotIn("sqlite3", text)
        self.assertNotIn("os.replace(source", text)
        self.assertNotIn("apply_ruff_correction_preview", text)
        self.assertIn("source_mutation_allowed", text)


if __name__ == "__main__":
    unittest.main()
