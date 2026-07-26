"""Validation tests for Prompt Router Reasoner runtime newest selection tie repair v1."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    PromptRouterReasonerReviewStore,
    PromptSnapshot,
    REVIEW_FOLDER_NAME,
    REVIEW_INDEX_FILENAME,
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
SESSION_RUNTIME_CAPTURE_FEATURE_ID = "prompt_router_reasoner_session_service_runtime_capture_wiring_v1"


def _snapshot(prompt_id: str, prompt_name: str, *, is_ml: bool = False) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path=(
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/"
            "session_service.py::SessionService.execute"
            if not is_ml
            else "kanda_reasoner_app/routing_signal_scorer/contract.py::preview"
        ),
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="reasoner_engine" if not is_ml else "routing_signal_scorer",
        prompt_version="v1",
        score=0.91,
        confidence=0.88 if is_ml else None,
        explanation="Stored explanation for " + prompt_name,
        keywords=("runtime", "tie_repair", prompt_id),
        route="runtime_capture_route",
        semantic_match="semantic match text" if is_ml else "authoritative flow",
        inferred_intent="runtime_capture_visibility" if is_ml else "authoritative intent",
        disagreement_reason="advisory no route authority" if is_ml else "authoritative baseline",
        safety_status="advisory_only_no_router_authority" if is_ml else "authoritative_heuristic_baseline",
    )


def _make_runtime_review(root: Path, generator_id: str, text: str) -> str:
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text=text,
        short_generator_text=text[:64],
        generator_text_id=generator_id,
        heuristic_prompt=_snapshot("heuristic_" + generator_id, "Heuristic " + generator_id),
        ml_prompt=_snapshot("ml_" + generator_id, "ML " + generator_id, is_ml=True),
        app_version=SESSION_RUNTIME_CAPTURE_FEATURE_ID,
        router_version="runtime_route:runtime_intent",
        retriever_version="session_service_retrieval_bundle_snapshot_v1",
        ml_version="routing_signal_scorer_similarity_prompt_context_preview_shadow_v1",
        prompt_library_version="prompt_builder_final_prompt_hash",
    )


def test_sources_have_timestamp_and_sequence_tie_repair() -> None:
    store_source = STORE_SOURCE_PATH.read_text(encoding="utf-8")
    tab_source = TAB_SOURCE_PATH.read_text(encoding="utf-8")
    assert 'timespec="microseconds"' in store_source
    assert '"review_sequence": review_sequence' in store_source
    assert "_next_review_sequence" in store_source
    assert "review_sequence is used as the deterministic tie-breaker" in tab_source

    forbidden_text = [
        "router_with_ml_radio.setEnabled(True)",
        "provider_call(",
        "openai",
        "write_freeze_memory(",
        "project_freeze_ledger.write",
    ]
    combined = store_source + "\n" + tab_source
    for text in forbidden_text:
        assert text not in combined


def test_newest_runtime_capture_prefers_review_sequence_when_timestamp_ties_if_pyside_available() -> None:
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
        older_id = _make_runtime_review(root, "gen_100", "older runtime capture row")
        newest_id = _make_runtime_review(root, "gen_999", "newest runtime capture row")

        # Force the historical Windows failure condition: two runtime rows share
        # one visible timestamp. The newer row must still win by review_sequence,
        # never by random UUID string order.
        index_path = root / REVIEW_FOLDER_NAME / REVIEW_INDEX_FILENAME
        index = json.loads(index_path.read_text(encoding="utf-8-sig"))
        shared_time = "2026-06-22T13:00:00Z"
        index["items"][older_id]["created_at"] = shared_time
        index["items"][newest_id]["created_at"] = shared_time
        assert index["items"][older_id]["review_sequence"] < index["items"][newest_id]["review_sequence"]
        index_path.write_text(json.dumps(index, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_newest_runtime_capture()
        assert widget.get_selected_review_item_id() == newest_id
        heuristic_text, ml_text = widget.get_current_review_detail_texts()
        assert "newest runtime capture row" in heuristic_text
        assert "ML gen_999" in ml_text
        assert widget.is_ml_pilot_control_locked() is True


if __name__ == "__main__":
    test_sources_have_timestamp_and_sequence_tie_repair()
    test_newest_runtime_capture_prefers_review_sequence_when_timestamp_ties_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner runtime newest selection tie repair")
