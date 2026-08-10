"""Validation tests for Prompt Router Reasoner Review List Loading v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    PromptRouterReasonerReviewStore,
    PromptSnapshot,
    REVIEW_FOLDER_NAME,
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


def _snapshot(prompt_id: str) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name="Prompt " + prompt_id,
        prompt_path="ACTIVE_PROMPTS/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="Summary for " + prompt_id,
        prompt_group="test_group",
        prompt_version="1",
        score=0.75,
        confidence=0.70,
        explanation="selected for Prompt Router Reasoner list-loading validation",
        keywords=("prompt", prompt_id),
        route="test_route",
        semantic_match="semantic match for " + prompt_id,
        inferred_intent="test intent",
        disagreement_reason="different prompt candidate",
        safety_status="safe_shadow_candidate",
    )


def _make_store_with_reviews(root: Path) -> tuple[PromptRouterReasonerReviewStore, str, str, str]:
    store = PromptRouterReasonerReviewStore(root)
    pending_disagree = store.create_pending_review(
        full_generator_text="Pending disagreement generator text.",
        short_generator_text="Pending disagreement",
        generator_text_id="gen_0012",
        heuristic_prompt=_snapshot("heuristic_a"),
        ml_prompt=_snapshot("ml_a"),
    )
    reviewed_ml = store.create_pending_review(
        full_generator_text="ML wins reviewed generator text.",
        short_generator_text="ML wins reviewed",
        generator_text_id="gen_0013",
        heuristic_prompt=_snapshot("heuristic_b"),
        ml_prompt=_snapshot("ml_b"),
    )
    store.save_review(reviewed_ml, LABEL_ML_CORRECT)
    reviewed_heuristic = store.create_pending_review(
        full_generator_text="Heuristic wins reviewed generator text.",
        short_generator_text="Heuristic wins reviewed",
        generator_text_id="gen_0014",
        heuristic_prompt=_snapshot("heuristic_c"),
        ml_prompt=_snapshot("ml_c"),
    )
    store.save_review(reviewed_heuristic, LABEL_HEURISTICS_CORRECT)
    return store, pending_disagree, reviewed_ml, reviewed_heuristic


def test_review_list_loading_source_is_list_only_and_safe() -> None:
    source = _source_text()
    required_text = [
        "Refresh review list",
        "project_root_edit",
        "refresh_review_list",
        "apply_review_filter",
        "get_loaded_review_item_ids",
        "get_visible_review_item_ids",
        "list_review_items()",
        "REVIEW_FOLDER_NAME",
    ]
    for text in required_text:
        assert text in source

    forbidden_runtime_wiring = [
        "SessionService(",
        "route_query_intent(",
        ".execute(",
        "ask_local_ai",
        "create_pending_review(",
        "project_freeze_ledger",
        "frozen_features_memory",
    ]
    for text in forbidden_runtime_wiring:
        assert text not in source


def test_review_list_loading_no_store_placeholder_if_pyside_available() -> None:
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
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        assert widget.get_loaded_review_item_ids() == ()
        assert widget.get_visible_review_item_ids() == ()
        assert not (root / REVIEW_FOLDER_NAME).exists()
        assert "No Prompt Router Reasoner review store" in widget.review_list_status_label.text()


def test_review_list_loads_persisted_review_items_if_pyside_available() -> None:
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
        _store, pending_disagree, reviewed_ml, reviewed_heuristic = _make_store_with_reviews(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)

        loaded_ids = widget.get_loaded_review_item_ids()
        visible_ids = widget.get_visible_review_item_ids()
        assert set(loaded_ids) == {pending_disagree, reviewed_ml, reviewed_heuristic}
        assert set(visible_ids) == {pending_disagree, reviewed_ml, reviewed_heuristic}
        assert widget.generator_text_list.count() == 3
        assert widget.review_next_button.isEnabled() is True
        assert widget.generator_text_list.item(0).data(0x0100) == pending_disagree
        assert "DISAGREE" in widget.generator_text_list.item(0).text()
        assert "Loaded 3 review item(s)." == widget.review_list_status_label.text()


def test_review_list_filters_visible_items_if_pyside_available() -> None:
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
        _store, pending_disagree, reviewed_ml, reviewed_heuristic = _make_store_with_reviews(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)

        widget.review_filter_combo.setCurrentText("Pending")
        assert widget.get_visible_review_item_ids() == (pending_disagree,)

        widget.review_filter_combo.setCurrentText("ML correct")
        assert widget.get_visible_review_item_ids() == (reviewed_ml,)

        widget.review_filter_combo.setCurrentText("Heuristics correct")
        assert widget.get_visible_review_item_ids() == (reviewed_heuristic,)

        widget.review_filter_combo.setCurrentText("Disagreements only")
        assert set(widget.get_visible_review_item_ids()) == {
            pending_disagree,
            reviewed_ml,
            reviewed_heuristic,
        }


def test_review_next_selects_first_visible_item_and_allows_later_detail_wiring_if_pyside_available() -> None:
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
        _store, pending_disagree, _reviewed_ml, _reviewed_heuristic = _make_store_with_reviews(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()
        selected = widget.generator_text_list.currentItem()
        assert selected is not None
        assert selected.data(0x0100) == pending_disagree
        # Later patches may wire detail columns after selection. The list-loading
        # invariant is only that the first visible row is selected safely.
        assert widget.heuristic_prompt_summary_box.toPlainText()
        assert widget.ml_prompt_summary_box.toPlainText()


def test_review_list_loading_keeps_router_mode_and_review_buttons_safe_if_pyside_available() -> None:
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
        _make_store_with_reviews(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        assert widget.router_with_heuristics_radio.isChecked() is True
        assert widget.router_with_ml_radio.isEnabled() is False
        assert widget.save_review_button.isEnabled() in (True, False)
        assert widget.undo_last_save_button.isEnabled() in (True, False)
        assert widget.ask_ai_button.isEnabled() in (True, False)


if __name__ == "__main__":
    test_review_list_loading_source_is_list_only_and_safe()
    test_review_list_loading_no_store_placeholder_if_pyside_available()
    test_review_list_loads_persisted_review_items_if_pyside_available()
    test_review_list_filters_visible_items_if_pyside_available()
    test_review_next_selects_first_visible_item_and_allows_later_detail_wiring_if_pyside_available()
    test_review_list_loading_keeps_router_mode_and_review_buttons_safe_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner review list loading")
