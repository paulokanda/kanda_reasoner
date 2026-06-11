"""PA046D tests for architecture-clean review status helper contracts."""

from __future__ import annotations

from pathlib import Path

import kanda_reasoner_app.tab3_manual_review_runtime.review_status_visibility as review_status_visibility
import kanda_reasoner_app.tab3_manual_review_runtime.review_engine_status_runtime as review_engine_status_runtime


def test_stale_review_draft_status_variants_are_not_present() -> None:
    folder = Path('ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime')
    assert not (folder / "review_draft_status_runtime.py").exists()
    assert not (folder / "review_draft_status_box.py").exists()
    assert (folder / "review_status_visibility.py").exists()


def test_review_status_helpers_have_direct_public_contracts() -> None:
    assert "draft_status_text_for_row" in review_status_visibility.__all__
    assert "apply_review_draft_status" in review_status_visibility.__all__
    assert "append_draft_generation_output" in review_status_visibility.__all__
    assert "correction_mode_from_owner" in review_engine_status_runtime.__all__
    assert "apply_correction_engine_status" in review_engine_status_runtime.__all__
    assert "local_ai_enabled_from_owner" in review_engine_status_runtime.__all__


def test_reviewable_heuristic_row_reports_heuristic_draft_generated() -> None:
    row = {
        "file": "app/main.py",
        "action": "inserted",
        "target_kind": "function",
        "target_name": "build_runner",
        "line": 10,
        "draft_docstring": "Build a runner.",
        "selected_draft_source": "heuristic",
    }
    assert review_status_visibility.draft_status_text_for_row(row) == "HEURISTIC DRAFT GENERATED"


if __name__ == "__main__":
    test_stale_review_draft_status_variants_are_not_present()
    test_review_status_helpers_have_direct_public_contracts()
    test_reviewable_heuristic_row_reports_heuristic_draft_generated()
    print("PA046D review status architecture contract tests passed.")
