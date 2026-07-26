"""Validation tests for Prompt Router Reasoner Heuristic ML Detail Panels v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    LABEL_HEURISTICS_CORRECT,
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


def _source_text() -> str:
    return TAB_SOURCE_PATH.read_text(encoding="utf-8")


def _heuristic_snapshot() -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id="heuristic_prompt_alpha",
        prompt_name="Heuristic Prompt Alpha",
        prompt_path="ACTIVE_PROMPTS/router/heuristic_alpha.md",
        prompt_hash="hash_heuristic_alpha",
        prompt_summary="Heuristic alpha summary.",
        prompt_group="router",
        prompt_version="h1",
        score=0.91,
        confidence=0.90,
        explanation="Heuristics selected alpha because the route and keywords matched.",
        keywords=("router", "heuristic", "alpha"),
        route="governed_router_path",
        safety_status="authoritative_default",
    )


def _ml_snapshot() -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id="ml_prompt_beta",
        prompt_name="ML Prompt Beta",
        prompt_path="ACTIVE_PROMPTS/router/ml_beta.md",
        prompt_hash="hash_ml_beta",
        prompt_summary="ML beta summary.",
        prompt_group="router",
        prompt_version="m1",
        score=0.83,
        confidence=0.82,
        explanation="ML selected beta because semantic similarity favored the ML candidate.",
        keywords=("semantic", "ml", "beta"),
        route="ml_shadow_path",
        semantic_match="semantic overlap with beta prompt",
        inferred_intent="compare router prompt candidates",
        disagreement_reason="ML preferred semantic similarity over exact heuristic route.",
        safety_status="safe_shadow_candidate",
    )


def _make_review(root: Path) -> str:
    store = PromptRouterReasonerReviewStore(root)
    review_id = store.create_pending_review(
        full_generator_text="Create a router prompt comparison tab with heuristic and ML candidates.",
        short_generator_text="Create router prompt comparison tab",
        generator_text_id="gen_20260622_001",
        heuristic_prompt=_heuristic_snapshot(),
        ml_prompt=_ml_snapshot(),
    )
    return review_id


def test_detail_panel_source_declares_safe_detail_loading() -> None:
    source = _source_text()
    required_text = [
        "_on_review_row_selected",
        "_render_prompt_detail_panels",
        "_format_prompt_detail",
        "Heuristics selected this prompt because",
        "ML selected this prompt because",
        "_update_full_prompt_buttons",
        "get_current_review_detail_texts",
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


def test_clicking_review_row_loads_heuristic_and_ml_details_if_pyside_available() -> None:
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
        review_id = _make_review(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)

        assert widget.get_visible_review_item_ids() == (review_id,)
        widget.select_next_review_item()
        heuristic_text, ml_text = widget.get_current_review_detail_texts()

        assert "Review item: " + review_id in heuristic_text
        assert "Full generator text: Create a router prompt comparison tab" in heuristic_text
        assert "Heuristic/default selected prompt" in heuristic_text
        assert "Heuristic Prompt Alpha" in heuristic_text
        assert "hash_heuristic_alpha" in heuristic_text
        assert "governed_router_path" in heuristic_text
        assert "Heuristics selected alpha because" in heuristic_text

        assert "Review item: " + review_id in ml_text
        assert "ML selected prompt" in ml_text
        assert "ML Prompt Beta" in ml_text
        assert "hash_ml_beta" in ml_text
        assert "Confidence: 0.82" in ml_text
        assert "semantic overlap with beta prompt" in ml_text
        assert "ML selected beta because" in ml_text
        assert "safe_shadow_candidate" in ml_text


def test_detail_loading_keeps_review_actions_and_ml_pilot_locked_if_pyside_available() -> None:
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
        review_id = _make_review(root)
        store = PromptRouterReasonerReviewStore(root)
        store.save_review(review_id, LABEL_HEURISTICS_CORRECT)

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()

        assert widget.router_with_heuristics_radio.isChecked() is True
        assert widget.router_with_ml_radio.isEnabled() is False
        assert widget.save_review_button.isEnabled() is False
        assert widget.undo_last_save_button.isEnabled() is True
        assert widget.ask_ai_button.isEnabled() is True
        assert widget.heuristic_full_prompt_button.isEnabled() is False
        assert widget.ml_full_prompt_button.isEnabled() is False


def test_clearing_filter_resets_detail_placeholders_if_pyside_available() -> None:
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
        _make_review(root)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()
        assert "Heuristic Prompt Alpha" in widget.heuristic_prompt_summary_box.toPlainText()

        widget.review_filter_combo.setCurrentText("ML correct")
        heuristic_text, ml_text = widget.get_current_review_detail_texts()
        assert "[pending selection]" in heuristic_text
        assert "[pending selection]" in ml_text


if __name__ == "__main__":
    test_detail_panel_source_declares_safe_detail_loading()
    test_clicking_review_row_loads_heuristic_and_ml_details_if_pyside_available()
    test_detail_loading_keeps_review_actions_and_ml_pilot_locked_if_pyside_available()
    test_clearing_filter_resets_detail_placeholders_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner heuristic ml detail panels")
