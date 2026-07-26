"""Validation tests for Prompt Router Reasoner Import Loaded IDs Tuple Contract Repair v1."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "prompt_router_reasoner_gui"
    / "prompt_router_reasoner_tab.py"
)
IMPORT_TEST_PATH = PROJECT_ROOT / "tests" / "test_prompt_router_reasoner_import_review_dataset_v1.py"


def test_loaded_review_item_ids_contract_remains_tuple() -> None:
    source = TAB_SOURCE_PATH.read_text(encoding="utf-8")
    assert "def get_loaded_review_item_ids" in source
    assert 'return tuple(str(item.get("review_item_id", "")) for item in self._loaded_review_items)' in source


def test_import_gui_validation_matches_tuple_contract() -> None:
    source = IMPORT_TEST_PATH.read_text(encoding="utf-8")
    assert "assert widget.get_loaded_review_item_ids() == (review_id,)" in source
    assert "assert widget.get_loaded_review_item_ids() == [review_id]" not in source


if __name__ == "__main__":
    test_loaded_review_item_ids_contract_remains_tuple()
    test_import_gui_validation_matches_tuple_contract()
    print("VALIDATION OK: prompt router reasoner import loaded ids tuple contract repair")
