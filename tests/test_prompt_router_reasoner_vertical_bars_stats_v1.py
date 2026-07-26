"""Validation tests for Prompt Router Reasoner Vertical Bars and Stats Panel v1."""

from __future__ import annotations

import importlib.util
import json
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
    REVIEW_FOLDER_NAME,
    REVIEW_STATS_FILENAME,
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


def _snapshot(prompt_id: str, prompt_name: str, *, hash_suffix: str | None = None) -> PromptSnapshot:
    suffix = hash_suffix or prompt_id
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/router/" + prompt_id + ".md",
        prompt_hash="hash_" + suffix,
        prompt_summary="summary for " + prompt_name,
        prompt_group="router",
        prompt_version="v1",
        score=0.91,
        confidence=0.89,
        explanation="Stored explanation for " + prompt_name,
        keywords=("router", "stats", prompt_id),
        route="router_review_path",
        semantic_match="semantic match for " + prompt_name,
        inferred_intent="stats_panel_validation",
        disagreement_reason="different prompt hash" if hash_suffix is None else "same prompt hash",
        safety_status="safe_shadow_only",
    )


def _make_review(root: Path, label: str, *, agree: bool, index: int) -> str:
    store = PromptRouterReasonerReviewStore(root)
    heuristic = _snapshot("heuristic_" + str(index), "Heuristic Prompt " + str(index), hash_suffix="same_" + str(index) if agree else None)
    ml = _snapshot("ml_" + str(index), "ML Prompt " + str(index), hash_suffix="same_" + str(index) if agree else None)
    review_id = store.create_pending_review(
        full_generator_text="Validate stats panel review " + str(index),
        short_generator_text="Stats panel review " + str(index),
        generator_text_id="gen_20260622_" + str(index),
        heuristic_prompt=heuristic,
        ml_prompt=ml,
    )
    store.save_review(review_id, label)
    return review_id


def test_vertical_bars_stats_source_is_display_only() -> None:
    source = _source_text()
    required_text = [
        "compute_prompt_router_reasoner_stats",
        "refresh_stats_panel",
        "get_readiness_bar_state",
        "write_stats_cache",
        "friendly_heuristic_score",
        "friendly_ml_score",
        "pilot_readiness_percent",
        "ML Pilot Readiness: LOCKED",
        "router_with_ml_radio.setEnabled(False)",
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


def test_vertical_bars_update_from_review_stats_if_pyside_available() -> None:
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
        _make_review(root, LABEL_HEURISTICS_CORRECT, agree=False, index=1)
        _make_review(root, LABEL_ML_CORRECT, agree=False, index=2)
        _make_review(root, LABEL_BOTH_ACCEPTABLE_UNCLEAR, agree=False, index=3)

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        state = widget.get_readiness_bar_state()

        assert state["heuristics_value"] == 67
        assert state["ml_value"] == 67
        assert state["pilot_value"] < 100
        assert state["router_with_ml_locked"] is True
        assert "LOCKED" in state["status_text"]
        assert "Reviewed: 3" in state["status_text"]

        stats_cache = root / REVIEW_FOLDER_NAME / REVIEW_STATS_FILENAME
        assert stats_cache.exists()
        cached = json.loads(stats_cache.read_text(encoding="utf-8-sig"))
        assert cached["kind"] == "prompt_router_reasoner_stats_cache"
        assert cached["stats"]["reviewed_total"] == 3
        assert cached["stats"]["pilot_threshold_met"] is False


def test_vertical_bars_refresh_after_save_and_undo_if_pyside_available() -> None:
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
        store = PromptRouterReasonerReviewStore(root)
        review_id = store.create_pending_review(
            full_generator_text="Validate stats refresh after save and undo.",
            short_generator_text="Stats refresh save undo",
            generator_text_id="gen_20260622_991",
            heuristic_prompt=_snapshot("heuristic_refresh", "Heuristic Refresh"),
            ml_prompt=_snapshot("ml_refresh", "ML Refresh"),
        )

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        initial = widget.get_readiness_bar_state()
        assert initial["heuristics_value"] == 0
        assert initial["ml_value"] == 0

        widget.select_next_review_item()
        assert widget.get_selected_review_item_id() == review_id
        widget.ml_correct_radio.setChecked(True)
        widget.save_selected_review()
        after_save = widget.get_readiness_bar_state()
        assert after_save["heuristics_value"] == 0
        assert after_save["ml_value"] == 100
        assert after_save["router_with_ml_locked"] is True

        widget.review_filter_combo.setCurrentText("Reviewed")
        widget.select_next_review_item()
        widget.undo_selected_review()
        after_undo = widget.get_readiness_bar_state()
        assert after_undo["heuristics_value"] == 0
        assert after_undo["ml_value"] == 0
        assert after_undo["router_with_ml_locked"] is True


if __name__ == "__main__":
    test_vertical_bars_stats_source_is_display_only()
    test_vertical_bars_update_from_review_stats_if_pyside_available()
    test_vertical_bars_refresh_after_save_and_undo_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner vertical bars and stats panel")
