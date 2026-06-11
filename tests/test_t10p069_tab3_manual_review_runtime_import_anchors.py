"""Import anchors for tab3 manual review runtime helper modules."""

from __future__ import annotations

import unittest

import kanda_reasoner_app.tab3_manual_review_runtime.export_summary as export_summary
import kanda_reasoner_app.tab3_manual_review_runtime.heuristic_suggestion as heuristic_suggestion
import kanda_reasoner_app.tab3_manual_review_runtime.preview_summary as preview_summary


class Tab3ManualReviewRuntimeImportAnchorsTests(unittest.TestCase):
    """Verify tab3 helper modules remain importable by direct module path."""

    def test_tab3_manual_review_runtime_import_anchors(self) -> None:
        self.assertTrue(hasattr(export_summary, "_export_manual_review_summary"))
        self.assertTrue(hasattr(heuristic_suggestion, "_suggest_manual_review_heuristic"))
        self.assertTrue(hasattr(preview_summary, "_build_approved_review_preview"))


if __name__ == "__main__":
    unittest.main()
