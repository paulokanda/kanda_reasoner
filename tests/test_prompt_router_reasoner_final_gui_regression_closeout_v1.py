"""Final regression closeout for the Prompt Router Reasoner GUI workflow.

This test intentionally exercises the frozen GUI review loop without granting ML
routing authority or mutating prompt-library/source files. It is a closeout
regression harness, not a new runtime feature.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
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
STORE_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_engine"
    / "prompt_router_reasoner_review_store.py"
)
PYSIDE_AVAILABLE = importlib.util.find_spec("PySide6") is not None


FINAL_FEATURE_ID = "prompt_router_reasoner_final_gui_regression_closeout_v1"


def _source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _prompt_file(root: Path, relative_path: str, text: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _snapshot(prompt_id: str, prompt_name: str, prompt_path: str, *, token: str) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path=prompt_path,
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary " + token,
        prompt_group="final_closeout_group",
        prompt_version="v1",
        score=0.91,
        confidence=0.84,
        explanation="final closeout explanation " + token,
        keywords=("final_closeout", token),
        route="final_closeout_route",
        semantic_match="final closeout semantic match " + token,
        inferred_intent="final_gui_regression_closeout",
        disagreement_reason="heuristic and ml differ for regression coverage",
        safety_status="safe_shadow_candidate",
    )


def _make_review(root: Path, token: str, *, app_version: str = FINAL_FEATURE_ID) -> str:
    heuristic_path = f"ACTIVE_PROMPTS/final_closeout/heuristic_{token}.md"
    ml_path = f"ACTIVE_PROMPTS/final_closeout/ml_{token}.md"
    _prompt_file(root, heuristic_path, "HEURISTIC FULL PROMPT FINAL CLOSEOUT " + token)
    _prompt_file(root, ml_path, "ML FULL PROMPT FINAL CLOSEOUT " + token)
    store = PromptRouterReasonerReviewStore(root)
    return store.create_pending_review(
        full_generator_text="Final GUI closeout generator text " + token,
        short_generator_text="Final closeout " + token,
        generator_text_id="gen_final_closeout_" + token,
        heuristic_prompt=_snapshot("heuristic_" + token, "Heuristic " + token, heuristic_path, token=token),
        ml_prompt=_snapshot("ml_" + token, "ML " + token, ml_path, token=token),
        app_version=app_version,
        router_version="router_final_closeout_test",
        retriever_version="retriever_final_closeout_test",
        ml_version="ml_final_closeout_test",
        prompt_library_version="prompt_library_final_closeout_test",
    )


def test_final_gui_closeout_source_contracts_present_and_forbidden_authority_absent() -> None:
    tab_source = _source_text(TAB_SOURCE_PATH)
    store_source = _source_text(STORE_SOURCE_PATH)

    required_tab_markers = [
        "PromptRouterReasonerTabContract",
        "Router with heuristics",
        "Router with ML",
        "self.router_with_ml_radio.setEnabled(False)",
        "Refresh review list",
        "Show newest capture",
        "Export review dataset",
        "Dry-run import dataset",
        "Review import conflicts",
        "Import dataset",
        "Show full heuristic prompt",
        "Show full ML prompt",
        "Ask AI",
        "Paste AI answer",
        "Save review",
        "Undo last save",
        "get_runtime_capture_visibility_state",
        "get_gui_polish_state",
        "get_large_review_list_performance_state",
        "get_export_review_dataset_state",
        "get_import_review_dataset_state",
        "get_import_conflict_review_state",
        "get_full_prompt_lazy_display_state",
    ]
    for marker in required_tab_markers:
        assert marker in tab_source

    required_store_markers = [
        "def export_review_dataset",
        "def import_review_dataset",
        "def list_exported_review_datasets",
        "conflict_records",
        "latest_prompt_router_reasoner_review_dataset.json",
        "labels_overwritten",
        "router_changed",
    ]
    for marker in required_store_markers:
        assert marker in store_source

    forbidden_authority_changes = [
        "self.router_with_ml_radio.setEnabled(True)",
        "route_query_intent(",
        "SessionService(",
        "provider_call(",
        "ask_local_ai(",
        "create_embedding(",
        "write_freeze_memory(",
        "project_freeze_ledger",
        "frozen_features_memory",
    ]
    for marker in forbidden_authority_changes:
        assert marker not in tab_source



def test_final_gui_closeout_end_to_end_review_export_import_conflict_cycle_if_pyside_available() -> None:
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

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as source_dir, tempfile.TemporaryDirectory(
        ignore_cleanup_errors=True
    ) as import_dir:
        source_root = Path(source_dir)
        import_root = Path(import_dir)

        review_id = _make_review(source_root, "alpha")
        source_tab = PromptRouterReasonerTab()
        source_tab.set_project_root(source_root)

        assert source_tab.contract().to_dict()["ml_mode_locked"] is True
        assert source_tab.is_ml_pilot_control_locked() is True
        assert source_tab.get_loaded_review_item_ids() == (review_id,)
        assert source_tab.get_visible_review_item_ids() == (review_id,)
        assert source_tab.get_runtime_capture_visibility_state()["loaded_total"] == 1
        assert source_tab.get_readiness_bar_state()["router_with_ml_locked"] is True

        source_tab.select_next_review_item()
        assert source_tab.get_selected_review_item_id() == review_id
        action_state = source_tab.get_review_action_state()
        assert action_state["save_enabled"] is True
        assert action_state["ask_ai_enabled"] is True
        assert action_state["paste_ai_answer_enabled"] is True
        assert action_state["copy_generator_enabled"] is True

        heuristic_text = source_tab.load_full_prompt_text_for_selected("heuristic")
        ml_text = source_tab.load_full_prompt_text_for_selected("ml")
        assert "HEURISTIC FULL PROMPT FINAL CLOSEOUT alpha" in heuristic_text
        assert "ML FULL PROMPT FINAL CLOSEOUT alpha" in ml_text
        full_prompt_state = source_tab.get_full_prompt_lazy_display_state()
        assert full_prompt_state["ok"] is True
        assert full_prompt_state["router_with_ml_locked"] is True

        source_tab.review_search_edit.setText("alpha")
        assert source_tab.get_visible_review_item_ids() == (review_id,)
        perf_state = source_tab.get_large_review_list_performance_state()
        assert perf_state["search_cache_ready"] == 1
        assert perf_state["loaded_ids_contract"] == "tuple"
        assert perf_state["visible_ids_contract"] == "tuple"

        source_tab.heuristics_correct_radio.setChecked(True)
        source_tab.save_selected_review()
        saved_items = PromptRouterReasonerReviewStore(source_root).list_review_items()
        assert saved_items[0]["review_status"] == "reviewed"
        assert saved_items[0]["human_label"] == LABEL_HEURISTICS_CORRECT

        source_tab.set_project_root(source_root)
        source_tab.select_next_review_item()
        source_tab.undo_selected_review()
        undone_items = PromptRouterReasonerReviewStore(source_root).list_review_items()
        assert undone_items[0]["review_status"] == "pending"
        assert undone_items[0]["human_label"] is None

        source_tab.set_project_root(source_root)
        source_tab.select_next_review_item()
        ask_prompt = source_tab.build_ask_ai_prompt_for_selected_review()
        assert "senior prompt engineer" in ask_prompt.lower()
        assert "heuristic" in ask_prompt.lower()
        assert "ml" in ask_prompt.lower()

        export_result = source_tab.export_review_dataset()
        assert export_result["ok"] is True
        assert export_result["row_count"] == 1
        export_state = source_tab.get_export_review_dataset_state()
        assert export_state["copy_export_paths_enabled"] is True
        assert export_state["copy_export_folder_enabled"] is True
        assert export_state["latest_export"]["metadata"]["router_changed"] is False
        assert export_state["latest_export"]["metadata"]["labels_overwritten"] is False

        jsonl_path = Path(export_result["jsonl_path"])
        target_import_dir = import_root / "prompt_router_reasoner_reviews" / "import_review_datasets"
        target_import_dir.mkdir(parents=True, exist_ok=True)
        copied_jsonl = target_import_dir / jsonl_path.name
        shutil.copyfile(jsonl_path, copied_jsonl)

        import_tab = PromptRouterReasonerTab()
        import_tab.set_project_root(import_root)
        import_state_before = import_tab.get_import_review_dataset_state()
        assert import_state_before["preview_import_enabled"] is True
        assert import_state_before["import_enabled"] is True

        preview = import_tab.preview_import_review_dataset()
        assert preview["dry_run"] is True
        assert preview["would_import_count"] == 1
        assert import_tab.get_loaded_review_item_ids() == ()

        imported = import_tab.import_review_dataset()
        assert imported["dry_run"] is False
        assert imported["imported_count"] == 1
        assert import_tab.get_loaded_review_item_ids() == (review_id,)
        assert import_tab.get_import_review_dataset_state()["router_with_ml_locked"] is True

        conflict = import_tab.review_import_conflicts()
        assert conflict["conflict_review"] is True
        assert conflict["conflict_count"] >= 1
        conflict_state = import_tab.get_import_conflict_review_state()
        assert conflict_state["review_conflicts_enabled"] is True
        assert conflict_state["router_with_ml_locked"] is True
        assert any(
            record.get("reason") == "existing_review_item_id"
            for record in conflict_state["conflict_records"]
        )

        import_tab.clear_review_selection()
        assert import_tab.get_selected_review_item_id() is None
        assert import_tab.get_gui_polish_state()["clear_selection_enabled"] is False

        assert source_tab.is_ml_pilot_control_locked() is True
        assert import_tab.is_ml_pilot_control_locked() is True

    print("VALIDATION OK: prompt router reasoner final gui regression and closeout")


if __name__ == "__main__":
    test_final_gui_closeout_source_contracts_present_and_forbidden_authority_absent()
    test_final_gui_closeout_end_to_end_review_export_import_conflict_cycle_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner final gui regression and closeout")
