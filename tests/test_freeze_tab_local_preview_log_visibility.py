"""Regression tests for visible local-freeze preview logging."""

from __future__ import annotations

from pathlib import Path
import importlib.util
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GUI_SOURCE = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"
RENDERER_SOURCE = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "local_freeze_preview_log.py"

spec = importlib.util.spec_from_file_location("local_freeze_preview_log_under_test", RENDERER_SOURCE)
assert spec is not None and spec.loader is not None
renderer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer_module)

LOCAL_FREEZE_PREVIEW_LOG_BEGIN = renderer_module.LOCAL_FREEZE_PREVIEW_LOG_BEGIN
LOCAL_FREEZE_PREVIEW_LOG_END = renderer_module.LOCAL_FREEZE_PREVIEW_LOG_END
build_local_freeze_preview_log_text = renderer_module.build_local_freeze_preview_log_text


class FreezeTabLocalPreviewLogVisibilityTests(unittest.TestCase):
    def test_renderer_includes_the_real_preview_markdown_and_write_targets(self) -> None:
        preview = {
            "ok": True,
            "is_writable": True,
            "freeze_id": "freeze-20260617-demo-v1",
            "feature_title": "Demo v1",
            "primary_box": "kanda_reasoner_app/demo",
            "box_type": "Module Box",
            "write_targets": [
                r"E:\\kanda_reasoner\\project_freeze_after_update\\frozen_features_memory\\entries\\freeze-20260617-demo-v1.md",
                r"E:\\kanda_reasoner\\project_freeze_after_update\\frozen_features_memory\\freeze_index.json",
            ],
            "errors": [],
            "warnings": [],
            "markdown": "---\nfreeze_id: demo\n---\n\n# Demo v1\n\n## validated files\n\n- src/demo.py\n",
        }
        validation = {"ok": True, "errors": [], "warnings": []}

        rendered = build_local_freeze_preview_log_text(preview, validation)

        self.assertIn(LOCAL_FREEZE_PREVIEW_LOG_BEGIN, rendered)
        self.assertIn("Freeze ID: freeze-20260617-demo-v1", rendered)
        self.assertIn("Feature title: Demo v1", rendered)
        self.assertIn("Primary box: kanda_reasoner_app/demo", rendered)
        self.assertIn("Writable: YES", rendered)
        self.assertIn("Validation: OK", rendered)
        self.assertIn("Will write after Confirm and Write:", rendered)
        self.assertIn("freeze_index.json", rendered)
        self.assertIn("Preview Markdown:", rendered)
        self.assertIn("# Demo v1", rendered)
        self.assertIn("- src/demo.py", rendered)
        self.assertIn(LOCAL_FREEZE_PREVIEW_LOG_END, rendered)

    def test_renderer_surfaces_errors_when_preview_is_not_writable(self) -> None:
        preview = {
            "ok": False,
            "is_writable": False,
            "freeze_id": "freeze-20260617-bad-v1",
            "feature_title": "Bad v1",
            "primary_box": "Replace with the primary box",
            "box_type": "Module Box",
            "errors": ["Missing mandatory field: validated_files"],
            "warnings": ["Starter fallback used."],
            "markdown": "# Bad v1\n",
        }

        rendered = build_local_freeze_preview_log_text(preview)

        self.assertIn("Writable: NO", rendered)
        self.assertIn("Validation: NOT RUN", rendered)
        self.assertIn("Preview errors:", rendered)
        self.assertIn("Missing mandatory field: validated_files", rendered)
        self.assertIn("Starter fallback used.", rendered)
        self.assertIn("# Bad v1", rendered)

    def test_gui_preview_button_mirrors_preview_to_visible_log(self) -> None:
        source = GUI_SOURCE.read_text(encoding="utf-8")

        self.assertIn("build_local_freeze_preview_log_text", source)
        self.assertIn("def _append_log_block", source)
        self.assertIn("preview_text_edit.setPlainText", source)
        self.assertIn("self._append_log_block(build_local_freeze_preview_log_text(result, validation_result))", source)
        self.assertIn("Local freeze entry preview is ready and writable. No files were written.", source)

    def test_renderer_remains_qt_free_for_static_contract_tests(self) -> None:
        renderer = RENDERER_SOURCE.read_text(encoding="utf-8")

        self.assertNotIn("PySide6", renderer)
        self.assertNotIn("QTextEdit", renderer)
        self.assertIn("never writes freeze memory", renderer)


if __name__ == "__main__":
    unittest.main()
