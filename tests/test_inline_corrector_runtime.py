"""Focused public-contract tests for inline_corrector_runtime."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.tab3_manual_review_runtime.inline_corrector_runtime import (
    approve_current_row,
    approve_visible_rows,
    refresh_inline_corrector_for_selection,
    reject_current_row,
    reset_filtered_review_selection,
    save_all_approved_corrections,
    save_current_correction,
    select_next_filtered_review_item,
    undo_current_correction,
    wire_inline_corrector_events,
)


def test_inline_corrector_runtime_public_contract_imports() -> None:
    """Verify public inline corrector runtime functions import directly."""
    public_functions = [
        approve_current_row,
        approve_visible_rows,
        refresh_inline_corrector_for_selection,
        reject_current_row,
        reset_filtered_review_selection,
        save_all_approved_corrections,
        save_current_correction,
        select_next_filtered_review_item,
        undo_current_correction,
        wire_inline_corrector_events,
    ]

    for function in public_functions:
        assert callable(function)


if __name__ == "__main__":
    test_inline_corrector_runtime_public_contract_imports()
    print("inline_corrector_runtime public contract tests passed.")
