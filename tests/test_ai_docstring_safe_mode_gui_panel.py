
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    SAFE_MODE_ACTION_ACCEPT,
    SAFE_MODE_ACTION_EDIT,
    SAFE_MODE_ACTION_FALLBACK,
    SAFE_MODE_ACTION_REGENERATE,
    SAFE_MODE_ACTION_REJECT,
    SAFE_MODE_ACTION_SKIP,
    accept_docstring,
    build_folder_review_state,
    build_safe_mode_button_state,
    build_safe_mode_gui_snapshot,
    build_safe_mode_panel_model,
    create_guided_session,
)


class SafeModeGuiVisualPanelTests(unittest.TestCase):
    """Validate the Safe Mode GUI panel model without requiring PySide."""

    def _snapshot_and_buttons(self, accepted: bool = False):
        tmp_dir = tempfile.TemporaryDirectory()
        root = Path(tmp_dir.name)
        pkg = root / "pkg"
        pkg.mkdir()
        (pkg / "module.py").write_text("def alpha():\n    pass\n", encoding="utf-8")

        session = create_guided_session(root)
        state = build_folder_review_state(
            "pkg",
            [
                {
                    "file": "pkg/module.py",
                    "target_kind": "function",
                    "target_name": "alpha",
                    "insert_line": 2,
                    "generation_source": "ai",
                    "review_status": "ready_for_review",
                    "review_severity": "info",
                    "proposed_docstring": '"""Return alpha."""',
                }
            ],
        )
        if accepted:
            state = accept_docstring(state, state.rows[0].row_id)

        snapshot = build_safe_mode_gui_snapshot(session, state)
        buttons = build_safe_mode_button_state(session, state)
        return tmp_dir, snapshot, buttons

    def test_panel_model_surfaces_folder_progress_and_review_counts(self) -> None:
        tmp_dir, snapshot, buttons = self._snapshot_and_buttons()
        with tmp_dir:
            model = build_safe_mode_panel_model(snapshot, buttons)

            self.assertEqual("Safe Mode", model.title)
            self.assertEqual("pkg", model.folder_label)
            self.assertEqual("Folder 1 of 1", model.progress_label)
            self.assertEqual("Pending rows: 1", model.pending_label)
            self.assertIn("Accepted: 0", model.review_label)
            self.assertIn("pending", model.status_message)

    def test_panel_model_disables_apply_until_folder_ready(self) -> None:
        tmp_dir, snapshot, buttons = self._snapshot_and_buttons()
        with tmp_dir:
            model = build_safe_mode_panel_model(snapshot, buttons)

            self.assertFalse(model.button_enabled["apply_folder"])
            self.assertTrue(model.button_enabled[SAFE_MODE_ACTION_ACCEPT])
            self.assertTrue(model.button_enabled[SAFE_MODE_ACTION_EDIT])
            self.assertTrue(model.button_enabled[SAFE_MODE_ACTION_REGENERATE])
            self.assertTrue(model.button_enabled[SAFE_MODE_ACTION_FALLBACK])
            self.assertTrue(model.button_enabled[SAFE_MODE_ACTION_SKIP])
            self.assertTrue(model.button_enabled[SAFE_MODE_ACTION_REJECT])

    def test_panel_model_enables_apply_after_accept(self) -> None:
        tmp_dir, snapshot, buttons = self._snapshot_and_buttons(accepted=True)
        with tmp_dir:
            model = build_safe_mode_panel_model(snapshot, buttons)

            self.assertTrue(model.button_enabled["apply_folder"])
            self.assertEqual("Apply folder", model.button_text["apply_folder"])
            self.assertEqual("Next folder", model.button_text["next_folder"])
            self.assertEqual("Accepted: 1 | Skipped: 0 | Rejected: 0", model.review_label)

    def test_panel_widget_factory_is_lazy_imported(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode.gui_panel as panel_module

        self.assertTrue(hasattr(panel_module, "create_safe_mode_panel_widget"))
        self.assertTrue(hasattr(panel_module, "apply_safe_mode_panel_model"))
        self.assertTrue(hasattr(panel_module, "connect_safe_mode_panel_callbacks"))


if __name__ == "__main__":
    unittest.main()
