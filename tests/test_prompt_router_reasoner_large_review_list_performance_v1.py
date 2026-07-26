"""Validation tests for Prompt Router Reasoner Performance Large Review List v1."""

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


def _source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _snapshot(prompt_id: str, prompt_name: str, *, token: str) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/large_review_list/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name + " " + token,
        prompt_group="large_review_list_group",
        prompt_version="v1",
        score=0.82,
        confidence=0.71,
        explanation="large review list explanation " + token,
        keywords=("large_review_list", token),
        route="large_review_list_route",
        semantic_match="large review list semantic match " + token,
        inferred_intent="large_review_list_performance",
        disagreement_reason="candidate differs for large review list validation",
        safety_status="safe_shadow_candidate",
    )


def _make_review(root: Path, token: str, *, long_text: bool = False) -> str:
    text = "Large review list generator text " + token
    if long_text:
        text += " " + ("long_generator_payload_" + token + " ") * 220
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text=text,
        short_generator_text="Large list " + token,
        generator_text_id="gen_large_review_list_" + token,
        heuristic_prompt=_snapshot("heuristic_" + token, "Heuristic " + token, token=token),
        ml_prompt=_snapshot("ml_" + token, "ML " + token, token=token),
        app_version="prompt_router_reasoner_large_review_list_performance_v1_test",
        router_version="router_large_review_list_test",
        retriever_version="retriever_large_review_list_test",
        ml_version="ml_large_review_list_test",
        prompt_library_version="prompt_library_large_review_list_test",
    )


def test_large_review_list_source_uses_gui_only_caches_and_blocks_bulk_updates() -> None:
    tab_source = _source_text(TAB_SOURCE_PATH)

    for text in [
        "LARGE_REVIEW_LIST_SEARCH_CACHE_FIELD",
        "LARGE_REVIEW_LIST_ROW_TEXT_FIELD",
        "LARGE_REVIEW_LIST_TOOLTIP_FIELD",
        "_prepare_review_items_for_large_list",
        "_build_review_item_search_blob",
        "setUpdatesEnabled(False)",
        "blockSignals(True)",
        "get_large_review_list_performance_state",
    ]:
        assert text in tab_source

    forbidden_tab_wiring = [
        "router_with_ml_radio.setEnabled(True)",
        "SessionService(",
        "route_query_intent(",
        ".execute(",
        "ask_local_ai",
        "provider_call(",
        "write_freeze_memory(",
        "project_freeze_ledger",
        "frozen_features_memory",
    ]
    for text in forbidden_tab_wiring:
        assert text not in tab_source


def test_gui_large_review_list_search_uses_cached_blobs_without_contract_changes_if_pyside_available() -> None:
    if not PYSIDE_AVAILABLE:
        assert TAB_SOURCE_PATH.exists()
        return

    from PySide6.QtWidgets import QApplication  # type: ignore[import-not-found]
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        LARGE_REVIEW_LIST_TOOLTIP_LIMIT,
        PromptRouterReasonerTab,
    )

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        target_id = ""
        for index in range(140):
            token = f"large_token_{index:03d}"
            review_id = _make_review(root, token, long_text=index == 99)
            if index == 99:
                target_id = review_id

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)

        loaded_ids = widget.get_loaded_review_item_ids()
        visible_ids = widget.get_visible_review_item_ids()
        perf_state = widget.get_large_review_list_performance_state()

        assert isinstance(loaded_ids, tuple)
        assert isinstance(visible_ids, tuple)
        assert len(loaded_ids) == 140
        assert len(visible_ids) == 140
        assert perf_state["loaded_total"] == 140
        assert perf_state["visible_total"] == 140
        assert perf_state["rendered_total"] == 140
        assert perf_state["search_cache_ready"] == 140
        assert perf_state["render_updates_blocked"] is True
        assert perf_state["tooltip_limit"] == LARGE_REVIEW_LIST_TOOLTIP_LIMIT
        assert perf_state["loaded_ids_contract"] == "tuple"
        assert perf_state["visible_ids_contract"] == "tuple"
        assert perf_state["router_with_ml_locked"] is True

        widget.review_search_edit.setText("large_token_099")
        filtered_ids = widget.get_visible_review_item_ids()
        filtered_state = widget.get_large_review_list_performance_state()

        assert filtered_ids == (target_id,)
        assert filtered_state["visible_total"] == 1
        assert filtered_state["search_cache_ready"] == 140
        assert filtered_state["search_text"] == "large_token_099"
        assert filtered_state["router_with_ml_locked"] is True

        row = widget.generator_text_list.item(0)
        assert row is not None
        assert len(row.toolTip()) <= LARGE_REVIEW_LIST_TOOLTIP_LIMIT + 64
        assert "tooltip truncated" in row.toolTip()


if __name__ == "__main__":
    test_large_review_list_source_uses_gui_only_caches_and_blocks_bulk_updates()
    test_gui_large_review_list_search_uses_cached_blobs_without_contract_changes_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner performance large review list")
