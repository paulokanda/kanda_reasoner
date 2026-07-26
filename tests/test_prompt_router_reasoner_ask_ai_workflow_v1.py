"""Validation tests for Prompt Router Reasoner Ask AI Workflow v1."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    ASK_AI_REQUESTS_FOLDER_NAME,
    LABEL_HEURISTICS_CORRECT,
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
        confidence=0.83 if is_ml else None,
        explanation="Stored explanation for " + prompt_name,
        keywords=("router", "ask-ai", prompt_id),
        route="router_review_path",
        semantic_match="semantic match text" if is_ml else "",
        inferred_intent="ask_ai_review" if is_ml else "",
        disagreement_reason="ML chose a neighboring semantic prompt" if is_ml else "",
        safety_status="shadow_only_safe" if is_ml else "not_evaluated",
    )


def _make_pending_review(root: Path) -> str:
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text="Create a patch for prompt router reasoner ask AI workflow.",
        short_generator_text="Create Ask AI workflow patch",
        generator_text_id="gen_20260622_888",
        heuristic_prompt=_snapshot("heuristic_ask_ai", "Heuristic Ask AI Prompt"),
        ml_prompt=_snapshot("ml_ask_ai", "ML Ask AI Prompt", is_ml=True),
    )


def test_ask_ai_source_is_advisory_and_project_local() -> None:
    source = _source_text()
    store_source = _store_source_text()
    required_tab_text = [
        "PromptRouterReasonerAskAIReviewDialog",
        "build_ask_ai_prompt_for_selected_review",
        "open_ask_ai_window",
        "_save_ask_ai_request",
        "_copy_ask_ai_request_text",
        "You are a senior prompt engineer and machine learning specialist with 20 years of experience.",
        "Human review remains final.",
        "Do not suggest making ML authoritative now.",
        "Select a review row to open an editable advisory AI prompt.",
    ]
    for text in required_tab_text:
        assert text in source

    required_store_text = [
        "EVENT_ASK_AI_REQUEST_SAVED",
        "save_ask_ai_request",
        "prompt_router_reasoner_ask_ai_request",
        ASK_AI_REQUESTS_FOLDER_NAME,
        "current_human_label",
        "related_ai_answer_file",
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


def test_store_saves_ask_ai_request_without_changing_human_label() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        store = PromptRouterReasonerReviewStore(root)
        before = store.get_review_item(review_id)
        assert before["review_status"] == STATUS_PENDING
        assert before["human_label"] is None
        saved = store.save_ask_ai_request(review_id, "editable senior review prompt")

        text_path = root / "prompt_router_reasoner_reviews" / saved["text_file"]
        metadata_path = root / "prompt_router_reasoner_reviews" / saved["metadata_file"]
        assert text_path.exists()
        assert metadata_path.exists()
        assert ASK_AI_REQUESTS_FOLDER_NAME in saved["text_file"]
        assert text_path.read_text(encoding="utf-8").strip() == "editable senior review prompt"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        assert metadata["kind"] == "prompt_router_reasoner_ask_ai_request"
        assert metadata["review_item_id"] == review_id
        assert metadata["saved_by_user"] is True
        assert metadata["copied_by_user"] is False
        assert metadata["related_ai_answer_file"] is None

        after = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert after["review_status"] == STATUS_PENDING
        assert after["human_label"] is None
        assert saved["text_file"] in after["ask_ai_request_files"]


def test_gui_builds_prompt_and_saves_request_if_pyside_available() -> None:
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
        assert widget.get_review_action_state()["ask_ai_enabled"] is True
        ask_text = widget.build_ask_ai_prompt_for_selected_review()
        assert "20 years of experience" in ask_text
        assert "Create a patch for prompt router reasoner ask AI workflow." in ask_text
        assert "Heuristic Ask AI Prompt" in ask_text
        assert "ML Ask AI Prompt" in ask_text
        assert "Decide which selection is better" in ask_text
        assert "Human review remains final" in ask_text

        widget._save_ask_ai_request(review_id, ask_text)
        refreshed = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert refreshed["human_label"] is None
        assert refreshed["ask_ai_request_files"]
        assert widget.get_review_action_state()["ask_ai_enabled"] is True


def test_copy_ask_ai_request_does_not_save_file_if_pyside_available() -> None:
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
        widget._copy_ask_ai_request_text("copy only prompt")
        assert QApplication.clipboard().text() == "copy only prompt"
        unchanged = PromptRouterReasonerReviewStore(root).get_review_item(review_id)
        assert unchanged["ask_ai_request_files"] == []
        assert unchanged["human_label"] is None


def test_ask_ai_request_survives_index_rebuild() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        review_id = _make_pending_review(root)
        store = PromptRouterReasonerReviewStore(root)
        saved = store.save_ask_ai_request(review_id, "rebuild me")
        rebuilt = store.rebuild_index_from_log()
        item = rebuilt["items"][review_id]
        assert saved["text_file"] in item["ask_ai_request_files"]
        assert item["human_label"] is None


if __name__ == "__main__":
    test_ask_ai_source_is_advisory_and_project_local()
    test_store_saves_ask_ai_request_without_changing_human_label()
    test_gui_builds_prompt_and_saves_request_if_pyside_available()
    test_copy_ask_ai_request_does_not_save_file_if_pyside_available()
    test_ask_ai_request_survives_index_rebuild()
    print("VALIDATION OK: prompt router reasoner ask ai workflow")
