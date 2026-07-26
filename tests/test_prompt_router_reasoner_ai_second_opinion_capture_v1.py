"""Validation tests for Prompt Router Reasoner AI Second Opinion Capture v1."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    ASK_AI_ANSWERS_FOLDER_NAME,
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    PromptRouterReasonerReviewStore,
    PromptSnapshot,
    STATUS_PENDING,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "prompt_router_reasoner_gui"
    / "prompt_router_reasoner_tab.py"
)
STORE_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_engine"
    / "prompt_router_reasoner_review_store.py"
)
PYSIDE_AVAILABLE = importlib.util.find_spec("PySide6") is not None


def _source_text() -> str:
    return TAB_SOURCE_PATH.read_text(encoding="utf-8")


def _store_source_text() -> str:
    return STORE_SOURCE_PATH.read_text(encoding="utf-8")


def _snapshot(prompt_id: str, prompt_name: str, *, is_ml: bool = False) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/router/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="router",
        prompt_version="v1",
        score=0.91,
        confidence=0.88 if is_ml else None,
        explanation="Stored explanation for " + prompt_name,
        keywords=("router", "second-opinion", prompt_id),
        route="router_review_path",
        semantic_match="semantic match text" if is_ml else "",
        inferred_intent="second_opinion_review" if is_ml else "",
        disagreement_reason="ML chose a neighboring semantic prompt" if is_ml else "",
        safety_status="shadow_only_safe" if is_ml else "not_evaluated",
    )


def _make_pending_review(root: Path) -> str:
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text="Create a patch for prompt router reasoner AI second opinion capture.",
        short_generator_text="Create AI second opinion capture patch",
        generator_text_id="gen_20260622_999",
        heuristic_prompt=_snapshot("heuristic_second_opinion", "Heuristic Second Opinion Prompt"),
        ml_prompt=_snapshot("ml_second_opinion", "ML Second Opinion Prompt", is_ml=True),
    )


def test_second_opinion_source_is_advisory_and_project_local() -> None:
    source = _source_text()
    store_source = _store_source_text()
    required_tab_text = [
        "PromptRouterReasonerPasteAIAnswerDialog",
        "Paste AI answer",
        "open_paste_ai_answer_window",
        "_save_ai_second_opinion",
        "Human label unchanged.",
        "advisory external AI answer",
    ]
    for text in required_tab_text:
        assert text in source

    required_store_text = [
        "EVENT_AI_SECOND_OPINION_SAVED",
        "save_ai_second_opinion",
        "prompt_router_reasoner_ai_second_opinion",
        ASK_AI_ANSWERS_FOLDER_NAME,
        "ai_answer_label_detected",
        "ai_agrees_with_human",
        "advisory_only",
        "detect_ai_second_opinion_label",
    ]
    for text in required_store_text:
        assert text in store_source

    forbidden_runtime_wiring = [
        "SessionService(",
        "route_query_intent(",
        "ask_local_ai",
        "router_with_ml_radio.setEnabled(True)",
        "provider_call(",
        "write_freeze_memory(",
        "openai",
    ]
    combined = source + "\n" + store_source
    for text in forbidden_runtime_wiring:
        assert text not in combined


def test_store_saves_second_opinion_without_changing_human_label() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        store = PromptRouterReasonerReviewStore(root)
        before = store.get_review_item(review_id)
        assert before["review_status"] == STATUS_PENDING
        assert before["human_label"] is None

        saved = store.save_ai_second_opinion(
            review_id,
            "After comparing both selections, the ML correct answer is better because it matches intent.",
        )

        text_path = root / "prompt_router_reasoner_reviews" / saved["text_file"]
        metadata_path = root / "prompt_router_reasoner_reviews" / saved["metadata_file"]
        assert text_path.exists()
        assert metadata_path.exists()
        assert ASK_AI_ANSWERS_FOLDER_NAME in saved["text_file"]
        assert "ML correct" in text_path.read_text(encoding="utf-8")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert metadata["kind"] == "prompt_router_reasoner_ai_second_opinion"
        assert metadata["review_item_id"] == review_id
        assert metadata["ai_answer_label_detected"] == LABEL_ML_CORRECT
        assert metadata["human_final_label"] is None
        assert metadata["ai_agrees_with_human"] == "unknown"
        assert metadata["advisory_only"] is True

        after = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert after["review_status"] == STATUS_PENDING
        assert after["human_label"] is None
        assert saved["text_file"] in after["ai_second_opinion_files"]
        assert after["latest_ai_second_opinion_label"] == LABEL_ML_CORRECT


def test_second_opinion_agreement_metadata_after_human_review() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        store = PromptRouterReasonerReviewStore(root)
        store.save_review(review_id, LABEL_HEURISTICS_CORRECT)
        saved = store.save_ai_second_opinion(
            review_id,
            "Best answer: heuristic. The heuristic selection is better for this governed prompt.",
        )
        metadata = saved["metadata"]
        assert metadata["ai_answer_label_detected"] == LABEL_HEURISTICS_CORRECT
        assert metadata["human_final_label"] == LABEL_HEURISTICS_CORRECT
        assert metadata["ai_agrees_with_human"] == "yes"


def test_second_opinion_survives_index_rebuild() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        store = PromptRouterReasonerReviewStore(root)
        saved = store.save_ai_second_opinion(review_id, "ML correct is the better selection.")
        rebuilt = store.rebuild_index_from_log()
        item = rebuilt["items"][review_id]
        assert saved["text_file"] in item["ai_second_opinion_files"]
        assert item["human_label"] is None
        assert item["latest_ai_second_opinion_label"] == LABEL_ML_CORRECT


def test_gui_paste_ai_answer_saves_advisory_answer_if_pyside_available() -> None:
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
        assert widget.get_review_action_state()["paste_ai_answer_enabled"] is True

        widget._save_ai_second_opinion(review_id, "The ML correct option is better as an advisory answer.")
        refreshed = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert refreshed["human_label"] is None
        assert refreshed["ai_second_opinion_files"]
        assert refreshed["latest_ai_second_opinion_label"] == LABEL_ML_CORRECT
        assert widget.get_review_action_state()["paste_ai_answer_enabled"] is True


def test_ask_ai_pending_answer_filter_turns_off_after_answer_if_pyside_available() -> None:
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
        store.save_ask_ai_request(review_id, "request")

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.review_filter_combo.setCurrentText("Ask AI pending answer")
        assert widget.get_visible_review_item_ids() == (review_id,)

        widget.select_next_review_item()
        widget._save_ai_second_opinion(review_id, "Both acceptable / unclear is my advisory answer.")
        widget.review_filter_combo.setCurrentText("Ask AI pending answer")
        assert widget.get_visible_review_item_ids() == ()


if __name__ == "__main__":
    test_second_opinion_source_is_advisory_and_project_local()
    test_store_saves_second_opinion_without_changing_human_label()
    test_second_opinion_agreement_metadata_after_human_review()
    test_second_opinion_survives_index_rebuild()
    test_gui_paste_ai_answer_saves_advisory_answer_if_pyside_available()
    test_ask_ai_pending_answer_filter_turns_off_after_answer_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner ai second opinion capture")
