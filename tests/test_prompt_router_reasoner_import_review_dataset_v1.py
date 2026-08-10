"""Validation tests for Prompt Router Reasoner Import Review Dataset v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    EVENT_REVIEW_DATASET_IMPORTED,
    IMPORT_DATASETS_FOLDER_NAME,
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    PromptRouterReasonerReviewStore,
    PromptSnapshot,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STORE_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_engine"
    / "prompt_router_reasoner_review_store.py"
)
TAB_SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "prompt_router_reasoner_gui"
    / "prompt_router_reasoner_tab.py"
)
PYSIDE_AVAILABLE = importlib.util.find_spec("PySide6") is not None


def _source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _snapshot(prompt_id: str, prompt_name: str, *, route: str = "import_route") -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/import/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="import_group",
        prompt_version="v1",
        score=0.83,
        confidence=0.74,
        explanation="import dataset explanation for " + prompt_name,
        keywords=("import", prompt_id),
        route=route,
        semantic_match="import semantic match",
        inferred_intent="import_review_dataset",
        disagreement_reason="candidate differs for import validation",
        safety_status="safe_shadow_candidate",
    )


def _make_review(root: Path, token: str, *, reviewed: bool = False, label: str = LABEL_HEURISTICS_CORRECT) -> str:
    store = PromptRouterReasonerReviewStore(root)
    review_id = store.create_pending_review(
        full_generator_text="Import dataset generator text " + token,
        short_generator_text="Import dataset " + token,
        generator_text_id="gen_import_" + token,
        heuristic_prompt=_snapshot("heuristic_" + token, "Heuristic " + token),
        ml_prompt=_snapshot("ml_" + token, "ML " + token),
        app_version="prompt_router_reasoner_import_review_dataset_v1_test",
        router_version="router_import_test",
        retriever_version="retriever_import_test",
        ml_version="ml_import_test",
        prompt_library_version="prompt_library_import_test",
    )
    if reviewed:
        store.save_review(review_id, label)
    return review_id


def _copy_export_jsonl_to_import_folder(source_root: Path, target_root: Path) -> Path:
    exported = PromptRouterReasonerReviewStore(source_root).export_review_dataset()
    source_jsonl = Path(exported["jsonl_path"])
    target_store = PromptRouterReasonerReviewStore(target_root)
    target_path = target_store.import_datasets_dir / source_jsonl.name
    shutil.copyfile(source_jsonl, target_path)
    return target_path


def test_import_review_dataset_source_is_import_only_and_safe() -> None:
    store_source = _source_text(STORE_SOURCE_PATH)
    tab_source = _source_text(TAB_SOURCE_PATH)

    for text in [
        "IMPORT_DATASETS_FOLDER_NAME",
        "EVENT_REVIEW_DATASET_IMPORTED",
        "preview_import_review_dataset",
        "import_review_dataset",
        "_review_export_row_to_import_item",
        "_resolve_import_dataset_path",
    ]:
        assert text in store_source

    for text in [
        "prompt_router_reasoner_preview_import_review_dataset_button",
        "prompt_router_reasoner_import_review_dataset_button",
        "get_import_review_dataset_state",
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


def test_store_dry_run_imports_no_events_then_imports_missing_rows_only() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as source_dir, tempfile.TemporaryDirectory(
        ignore_cleanup_errors=True
    ) as target_dir:
        source_root = Path(source_dir)
        target_root = Path(target_dir)
        first_id = _make_review(source_root, "alpha", reviewed=True)
        second_id = _make_review(source_root, "beta", reviewed=False)
        target_jsonl = _copy_export_jsonl_to_import_folder(source_root, target_root)

        target_store = PromptRouterReasonerReviewStore(target_root)
        before_events = target_store.iter_events()
        preview = target_store.preview_import_review_dataset(target_jsonl)
        after_preview_events = target_store.iter_events()

        assert before_events == after_preview_events
        assert preview["ok"] is True
        assert preview["dry_run"] is True
        assert preview["rows_seen"] == 2
        assert preview["would_import_count"] == 2
        assert preview["imported_count"] == 0
        assert preview["metadata"]["labels_overwritten"] is False
        assert preview["source_file"].startswith(IMPORT_DATASETS_FOLDER_NAME + "/")

        imported = target_store.import_review_dataset(target_jsonl, dry_run=False)
        assert imported["ok"] is True
        assert imported["dry_run"] is False
        assert imported["imported_count"] == 2
        events = target_store.iter_events()
        assert len(events) == 2
        assert all(event["event_type"] == EVENT_REVIEW_DATASET_IMPORTED for event in events)

        first = target_store.get_review_item(first_id)
        second = target_store.get_review_item(second_id)
        assert first["human_label"] == LABEL_HEURISTICS_CORRECT
        assert first["review_status"] == "reviewed"
        assert first["undo_available"] is False
        assert second["human_label"] is None
        assert second["review_status"] == "pending"

        reimport = target_store.import_review_dataset(target_jsonl, dry_run=False)
        assert reimport["imported_count"] == 0
        assert len(reimport["skipped_existing_ids"]) == 2
        assert target_store.get_review_item(first_id)["human_label"] == LABEL_HEURISTICS_CORRECT


def test_import_skips_existing_review_id_without_overwriting_label() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as source_dir, tempfile.TemporaryDirectory(
        ignore_cleanup_errors=True
    ) as target_dir:
        source_root = Path(source_dir)
        target_root = Path(target_dir)
        review_id = _make_review(source_root, "same", reviewed=True, label=LABEL_HEURISTICS_CORRECT)
        target_jsonl = _copy_export_jsonl_to_import_folder(source_root, target_root)

        target_store = PromptRouterReasonerReviewStore(target_root)
        local_id = target_store.create_pending_review(
            full_generator_text="Local row with same id placeholder",
            short_generator_text="Local same id",
            generator_text_id="gen_local_same",
            heuristic_prompt=_snapshot("local_h", "Local H"),
            ml_prompt=_snapshot("local_m", "Local M"),
        )
        target_store.save_review(local_id, LABEL_ML_CORRECT)

        index = target_store._index  # validation-only controlled setup
        existing = dict(index["items"].pop(local_id))
        existing["review_item_id"] = review_id
        existing["human_label"] = LABEL_ML_CORRECT
        existing["review_status"] = "reviewed"
        index["items"][review_id] = existing
        target_store._write_index()

        result = target_store.import_review_dataset(target_jsonl, dry_run=False)
        assert result["imported_count"] == 0
        assert result["skipped_existing_ids"] == [review_id]
        assert target_store.get_review_item(review_id)["human_label"] == LABEL_ML_CORRECT


def test_gui_import_buttons_preview_and_import_latest_dataset_if_pyside_available() -> None:
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
    ) as target_dir:
        source_root = Path(source_dir)
        target_root = Path(target_dir)
        review_id = _make_review(source_root, "gui", reviewed=True)
        _copy_export_jsonl_to_import_folder(source_root, target_root)

        widget = PromptRouterReasonerTab()
        widget.set_project_root(target_root)
        state = widget.get_import_review_dataset_state()
        assert state["preview_import_enabled"] is True
        assert state["import_enabled"] is True
        assert state["latest_dataset_file"].startswith(IMPORT_DATASETS_FOLDER_NAME + "/")

        preview = widget.preview_import_review_dataset()
        assert preview["ok"] is True
        assert preview["would_import_count"] == 1
        assert widget.get_selected_review_item_id() is None

        imported = widget.import_review_dataset()
        assert imported["ok"] is True
        assert imported["imported_count"] == 1
        assert widget.get_loaded_review_item_ids() == (review_id,)
        state = widget.get_import_review_dataset_state()
        assert state["latest_import"]["imported_count"] == 1
        assert state["router_with_ml_locked"] is True


if __name__ == "__main__":
    test_import_review_dataset_source_is_import_only_and_safe()
    test_store_dry_run_imports_no_events_then_imports_missing_rows_only()
    test_import_skips_existing_review_id_without_overwriting_label()
    test_gui_import_buttons_preview_and_import_latest_dataset_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner import review dataset")
