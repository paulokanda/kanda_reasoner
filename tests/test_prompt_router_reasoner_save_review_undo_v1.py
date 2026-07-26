"""Validation tests for Prompt Router Reasoner Save Review and Undo v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    LABEL_BOTH_ACCEPTABLE_UNCLEAR,
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    PromptRouterReasonerReviewStore,
    PromptSnapshot,
    ROUTER_WITH_HELP_OF_ML,
    STATUS_PENDING,
    STATUS_REVIEWED,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "prompt_router_reasoner_gui"
    / "prompt_router_reasoner_tab.py"
)
PYSIDE_AVAILABLE = importlib.util.find_spec("PySide6") is not None


def _source_text() -> str:
    return TAB_SOURCE_PATH.read_text(encoding="utf-8")


def _snapshot(prompt_id: str, prompt_name: str) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/router/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="router",
        prompt_version="v1",
        score=0.88,
        explanation="Stored explanation for " + prompt_name,
        keywords=("router", "review", prompt_id),
        route="router_review_path",
    )


def _make_pending_review(root: Path) -> str:
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text="Validate prompt router review save and undo controls.",
        short_generator_text="Validate save and undo controls",
        generator_text_id="gen_20260622_777",
        heuristic_prompt=_snapshot("heuristic_save", "Heuristic Save Prompt"),
        ml_prompt=_snapshot("ml_save", "ML Save Prompt"),
    )


def test_save_review_undo_source_is_gui_review_store_only() -> None:
    source = _source_text()
    required_text = [
        "save_selected_review",
        "undo_selected_review",
        "_selected_human_label",
        "_update_review_control_state",
        "store.save_review",
        "store.undo_last_save",
        "Only pending review items can be saved",
    ]
    for text in required_text:
        assert text in source

    forbidden_runtime_wiring = [
        "SessionService(",
        "route_query_intent(",
        ".execute(",
        "ask_local_ai",
        "create_pending_review(",
        "router_with_ml_radio.setEnabled(True)",
        "project_freeze_ledger",
        "frozen_features_memory",
    ]
    for text in forbidden_runtime_wiring:
        assert text not in source


def test_pending_selection_enables_save_and_saves_ml_label_if_pyside_available() -> None:
    if not PYSIDE_AVAILABLE:
        assert TAB_SOURCE_PATH.exists()
        return

    from PySide6.QtWidgets import QApplication  # type: ignore[import-not-found]
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        PromptRouterReasonerTab,
    )

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()

        assert widget.get_selected_review_item_id() == review_id
        assert widget.get_review_action_state()["save_enabled"] is True
        assert widget.get_review_action_state()["undo_enabled"] is False
        assert widget.get_review_action_state()["ask_ai_enabled"] is True

        widget.ml_correct_radio.setChecked(True)
        widget.router_with_help_of_ml_radio.setChecked(True)
        widget.save_selected_review()

        saved = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert saved["review_status"] == STATUS_REVIEWED
        assert saved["human_label"] == LABEL_ML_CORRECT
        assert saved["router_mode_at_review"] == ROUTER_WITH_HELP_OF_ML
        assert saved["undo_available"] is True
        assert widget.get_selected_review_item_id() is None
        heuristic_text, ml_text = widget.get_current_review_detail_texts()
        assert "[pending selection]" in heuristic_text
        assert "[pending selection]" in ml_text


def test_reviewed_selection_enables_undo_and_restores_pending_if_pyside_available() -> None:
    if not PYSIDE_AVAILABLE:
        assert TAB_SOURCE_PATH.exists()
        return

    from PySide6.QtWidgets import QApplication  # type: ignore[import-not-found]
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        PromptRouterReasonerTab,
    )

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        store = PromptRouterReasonerReviewStore(root)
        store.save_review(review_id, LABEL_HEURISTICS_CORRECT)

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()
        assert widget.get_selected_review_item_id() == review_id
        assert widget.get_review_action_state()["save_enabled"] is False
        assert widget.get_review_action_state()["undo_enabled"] is True

        widget.undo_selected_review()
        undone = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert undone["review_status"] == STATUS_PENDING
        assert undone["human_label"] is None
        assert undone["undo_available"] is False
        assert widget.get_selected_review_item_id() is None


def test_both_acceptable_label_can_be_saved_if_pyside_available() -> None:
    if not PYSIDE_AVAILABLE:
        assert TAB_SOURCE_PATH.exists()
        return

    from PySide6.QtWidgets import QApplication  # type: ignore[import-not-found]
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        PromptRouterReasonerTab,
    )

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()
        widget.both_acceptable_radio.setChecked(True)
        widget.save_review_button.click()

        saved = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert saved["review_status"] == STATUS_REVIEWED
        assert saved["human_label"] == LABEL_BOTH_ACCEPTABLE_UNCLEAR


if __name__ == "__main__":
    test_save_review_undo_source_is_gui_review_store_only()
    test_pending_selection_enables_save_and_saves_ml_label_if_pyside_available()
    test_reviewed_selection_enables_undo_and_restores_pending_if_pyside_available()
    test_both_acceptable_label_can_be_saved_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner save review and undo")
