"""PA048B focused tests for canonical bulk draft owner naming."""

from __future__ import annotations

import importlib
from pathlib import Path


def test_bulk_draft_canonical_owner_module_exports_public_contract() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.tab3_manual_review_runtime.review_bulk_drafts_runtime"
    )

    assert hasattr(module, "BulkDraftSummary")
    assert hasattr(module, "generate_bulk_drafts")
    assert "BulkDraftSummary" in module.__all__
    assert "generate_bulk_drafts" in module.__all__

    summary = module.BulkDraftSummary(scope="visible", generated=2, fallback=1, skipped=3, failed=4)
    output = summary.output_line()
    assert "scope=visible" in output
    assert "generated=2" in output
    assert "fallback=1" in output
    assert "skipped=3" in output
    assert "failed=4" in output


def test_stale_bulk_draft_generation_module_is_absent_from_project_tree() -> None:
    project_root = Path(__file__).resolve().parents[1]
    stale_path = (
        project_root
        / 'ask_' 'ai_project_reasoner'
        / "tab3_manual_review_runtime"
        / "bulk_draft_generation.py"
    )
    assert not stale_path.exists()


if __name__ == "__main__":
    test_bulk_draft_canonical_owner_module_exports_public_contract()
    test_stale_bulk_draft_generation_module_is_absent_from_project_tree()
    print("PA048B bulk draft canonical owner tests passed.")
