"""Validation tests for Prompt Router Reasoner GUI Polish and Review Ergonomics v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    PromptRouterReasonerReviewStore,
    PromptSnapshot,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "prompt_router_reasoner_gui"
    / "prompt_router_reasoner_tab.py"
)
PYSIDE_AVAILABLE = importlib.util.find_spec("PySide6") is not None
SESSION_RUNTIME_CAPTURE_FEATURE_ID = "prompt_router_reasoner_session_service_runtime_capture_wiring_v1"


def _source_text() -> str:
    return TAB_SOURCE_PATH.read_text(encoding="utf-8")


def _snapshot(prompt_id: str, prompt_name: str, *, route: str = "ergonomic_route") -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/ergonomics/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="ergonomics_group",
        prompt_version="v1",
        score=0.80,
        confidence=0.77,
        explanation="ergonomic validation explanation for " + prompt_name,
        keywords=("ergonomics", prompt_id),
        route=route,
        semantic_match="semantic match for " + prompt_name,
        inferred_intent="ergonomic review",
        disagreement_reason="different ergonomic candidate",
        safety_status="safe_shadow_candidate",
    )


def _make_review(root: Path, generator_id: str, text: str, prompt_token: str) -> str:
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text=text + " full generator text for copy validation",
        short_generator_text=text,
        generator_text_id=generator_id,
        heuristic_prompt=_snapshot("heuristic_" + prompt_token, "Heuristic " + prompt_token),
        ml_prompt=_snapshot("ml_" + prompt_token, "ML " + prompt_token),
        app_version=SESSION_RUNTIME_CAPTURE_FEATURE_ID,
    )


def test_gui_polish_source_is_gui_only() -> None:
    source = _source_text()
    required_text = [
        "prompt_router_reasoner_review_search_edit",
        "prompt_router_reasoner_selected_review_status_label",
        "prompt_router_reasoner_copy_selected_generator_text_button",
        "prompt_router_reasoner_copy_selected_detail_text_button",
        "prompt_router_reasoner_clear_review_selection_button",
        "clear_review_search",
        "copy_selected_generator_text",
        "copy_selected_detail_text",
        "get_gui_polish_state",
        "_review_item_matches_search",
    ]
    for text in required_text:
        assert text in source

    forbidden_runtime_wiring = [
        "route_query_intent(",
        "SessionService(",
        "capture_session_prompt_router_reasoner_review(",
        "router_with_ml_radio.setEnabled(True)",
        "ask_local_ai",
        "provider_call(",
        "write_freeze_memory(",
        "project_freeze_ledger",
        "frozen_features_memory",
    ]
    for text in forbidden_runtime_wiring:
        assert text not in source


def test_review_queue_search_and_clear_if_pyside_available() -> None:
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
        alpha_id = _make_review(root, "gen_alpha", "alpha clinical generator", "alpha")
        beta_id = _make_review(root, "gen_beta", "beta surgical generator", "beta")

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        assert set(widget.get_visible_review_item_ids()) == {alpha_id, beta_id}

        widget.review_search_edit.setText("surgical")
        state = widget.get_gui_polish_state()
        assert state["search_text"] == "surgical"
        assert state["visible_ids"] == (beta_id,)
        assert widget.is_ml_pilot_control_locked() is True

        widget.clear_review_search()
        state = widget.get_gui_polish_state()
        assert state["search_text"] == ""
        assert set(state["visible_ids"]) == {alpha_id, beta_id}


def test_selection_status_copy_helpers_and_clear_selection_if_pyside_available() -> None:
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
        review_id = _make_review(root, "gen_copy", "copyable generator", "copy")

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()
        polish = widget.get_gui_polish_state()
        assert polish["selected_id"] == review_id
        assert "Selected row:" in polish["selected_status_text"]
        assert "gen_copy" in polish["selected_status_text"]
        assert polish["copy_generator_enabled"] is True
        assert polish["copy_details_enabled"] is True
        assert polish["clear_selection_enabled"] is True

        widget.copy_selected_generator_text()
        assert "copyable generator" in QApplication.clipboard().text()
        widget.copy_selected_detail_text()
        clipboard_text = QApplication.clipboard().text()
        assert "HEURISTIC / DEFAULT DETAIL" in clipboard_text
        assert "ML SHADOW / ADVISORY DETAIL" in clipboard_text
        assert "Heuristic copy" in clipboard_text
        assert "ML copy" in clipboard_text

        widget.clear_review_selection()
        cleared = widget.get_gui_polish_state()
        assert cleared["selected_id"] is None
        assert cleared["selected_status_text"] == "Selected row: none."
        assert cleared["copy_generator_enabled"] is False
        assert cleared["copy_details_enabled"] is False
        assert widget.get_review_action_state()["save_enabled"] is False
        assert widget.is_ml_pilot_control_locked() is True


if __name__ == "__main__":
    test_gui_polish_source_is_gui_only()
    test_review_queue_search_and_clear_if_pyside_available()
    test_selection_status_copy_helpers_and_clear_selection_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner gui polish and review ergonomics")
