"""Validation tests for Prompt Router Reasoner Full Prompt Lazy Display v1."""

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


def _source_text() -> str:
    return TAB_SOURCE_PATH.read_text(encoding="utf-8")


def _snapshot(
    prompt_id: str,
    prompt_name: str,
    prompt_path: str,
    *,
    is_ml: bool = False,
) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path=prompt_path,
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="lazy_display_group",
        prompt_version="v1",
        score=0.90,
        confidence=0.84 if is_ml else None,
        explanation="lazy display explanation for " + prompt_name,
        keywords=("full_prompt", "lazy_display", prompt_id),
        route="lazy_display_route",
        semantic_match="semantic lazy display match" if is_ml else "authoritative lazy display route",
        inferred_intent="full_prompt_lazy_display",
        disagreement_reason="advisory prompt differs" if is_ml else "authoritative baseline",
        safety_status="safe_shadow_candidate" if is_ml else "authoritative_default",
    )


def _make_review(root: Path, heuristic_path: str, ml_path: str) -> str:
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text="Need full prompt lazy display for selected review candidates.",
        short_generator_text="Need full prompt lazy display",
        generator_text_id="gen_lazy_001",
        heuristic_prompt=_snapshot("heuristic_lazy", "Heuristic Lazy", heuristic_path),
        ml_prompt=_snapshot("ml_lazy", "ML Lazy", ml_path, is_ml=True),
    )


def test_full_prompt_lazy_display_source_is_gui_only() -> None:
    source = _source_text()
    required_text = [
        "PromptRouterReasonerFullPromptDialog",
        "load_full_prompt_text_for_selected",
        "get_full_prompt_lazy_display_state",
        "_resolve_prompt_file",
        "_read_prompt_file_for_display",
        "show_full_heuristic_prompt",
        "show_full_ml_prompt",
    ]
    for text in required_text:
        assert text in source

    forbidden_runtime_wiring = [
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
    for text in forbidden_runtime_wiring:
        assert text not in source


def test_existing_project_local_prompt_files_enable_buttons_and_load_text_if_pyside_available() -> None:
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
        heuristic_file = root / "ACTIVE_PROMPTS" / "lazy" / "heuristic_lazy.md"
        ml_file = root / "ACTIVE_PROMPTS" / "lazy" / "ml_lazy.md"
        heuristic_file.parent.mkdir(parents=True, exist_ok=True)
        heuristic_file.write_text("# Heuristic Lazy Prompt\n\nUse safe default selection.", encoding="utf-8")
        ml_file.write_text("# ML Lazy Prompt\n\nAdvisory only; no route authority.", encoding="utf-8")

        review_id = _make_review(
            root,
            "ACTIVE_PROMPTS/lazy/heuristic_lazy.md",
            "ACTIVE_PROMPTS/lazy/ml_lazy.md",
        )

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()
        assert widget.get_selected_review_item_id() == review_id
        assert widget.heuristic_full_prompt_button.isEnabled() is True
        assert widget.ml_full_prompt_button.isEnabled() is True

        heuristic_text = widget.load_full_prompt_text_for_selected("heuristic")
        assert "# Heuristic Lazy Prompt" in heuristic_text
        assert "Use safe default selection" in heuristic_text
        state = widget.get_full_prompt_lazy_display_state()
        assert state["ok"] is True
        assert state["prompt_kind"] == "heuristic"
        assert state["prompt_id"] == "heuristic_lazy"
        assert state["router_with_ml_locked"] is True

        ml_text = widget.load_full_prompt_text_for_selected("ml")
        assert "# ML Lazy Prompt" in ml_text
        assert "Advisory only; no route authority" in ml_text
        state = widget.get_full_prompt_lazy_display_state()
        assert state["ok"] is True
        assert state["prompt_kind"] == "ML advisory"
        assert state["prompt_id"] == "ml_lazy"
        assert widget.is_ml_pilot_control_locked() is True


def test_missing_and_unsafe_prompt_paths_stay_disabled_if_pyside_available() -> None:
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
        outside = root.parent / "outside_prompt.md"
        outside.write_text("outside prompt must not be loaded", encoding="utf-8")
        review_id = _make_review(root, "../outside_prompt.md", "missing/ml_prompt.md")

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget.select_next_review_item()
        assert widget.get_selected_review_item_id() == review_id
        assert widget.heuristic_full_prompt_button.isEnabled() is False
        assert widget.ml_full_prompt_button.isEnabled() is False

        assert widget.load_full_prompt_text_for_selected("heuristic") == ""
        state = widget.get_full_prompt_lazy_display_state()
        assert state["ok"] is False
        assert "missing or outside" in state["error"]
        assert widget.is_ml_pilot_control_locked() is True


if __name__ == "__main__":
    test_full_prompt_lazy_display_source_is_gui_only()
    test_existing_project_local_prompt_files_enable_buttons_and_load_text_if_pyside_available()
    test_missing_and_unsafe_prompt_paths_stay_disabled_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner full prompt lazy display")
