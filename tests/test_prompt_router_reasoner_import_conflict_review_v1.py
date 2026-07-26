"""Validation tests for Prompt Router Reasoner Import Conflict Review v1."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
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


def _snapshot(prompt_id: str, prompt_name: str, *, route: str = "conflict_route") -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/import_conflict/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="import_conflict_group",
        prompt_version="v1",
        score=0.84,
        confidence=0.76,
        explanation="import conflict explanation for " + prompt_name,
        keywords=("import", "conflict", prompt_id),
        route=route,
        semantic_match="import conflict semantic match",
        inferred_intent="import_conflict_review",
        disagreement_reason="candidate differs for import conflict validation",
        safety_status="safe_shadow_candidate",
    )


def _make_review(
    root: Path,
    token: str,
    *,
    reviewed: bool = False,
    label: str = LABEL_HEURISTICS_CORRECT,
) -> str:
    store = PromptRouterReasonerReviewStore(root)
    review_id = store.create_pending_review(
        full_generator_text="Import conflict generator text " + token,
        short_generator_text="Import conflict " + token,
        generator_text_id="gen_import_conflict_" + token,
        heuristic_prompt=_snapshot("heuristic_" + token, "Heuristic " + token),
        ml_prompt=_snapshot("ml_" + token, "ML " + token),
        app_version="prompt_router_reasoner_import_conflict_review_v1_test",
        router_version="router_import_conflict_test",
        retriever_version="retriever_import_conflict_test",
        ml_version="ml_import_conflict_test",
        prompt_library_version="prompt_library_import_conflict_test",
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


def _force_review_id(store: PromptRouterReasonerReviewStore, old_id: str, new_id: str) -> None:
    index = store._index  # validation-only controlled setup
    item = dict(index["items"].pop(old_id))
    item["review_item_id"] = new_id
    index["items"][new_id] = item
    store._write_index()


def test_import_conflict_review_source_is_read_only_and_safe() -> None:
    store_source = _source_text(STORE_SOURCE_PATH)
    tab_source = _source_text(TAB_SOURCE_PATH)

    for text in [
        "skipped_existing_conflicts",
        "skipped_duplicate_conflicts",
        "conflict_records",
        "_import_conflict_record",
        "_existing_review_fingerprint_map",
        "missing_rows_only_skip_conflicts_never_overwrite",
    ]:
        assert text in store_source

    for text in [
        "prompt_router_reasoner_review_import_conflicts_button",
        "review_import_conflicts",
        "get_import_conflict_review_state",
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


def test_store_import_conflict_review_reports_existing_duplicate_and_invalid_without_writes() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as source_dir, tempfile.TemporaryDirectory(
        ignore_cleanup_errors=True
    ) as target_dir:
        source_root = Path(source_dir)
        target_root = Path(target_dir)
        existing_source_id = _make_review(source_root, "same_id", reviewed=True, label=LABEL_HEURISTICS_CORRECT)
        _make_review(source_root, "duplicate", reviewed=True, label=LABEL_HEURISTICS_CORRECT)
        import_jsonl = _copy_export_jsonl_to_import_folder(source_root, target_root)
        with import_jsonl.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write('{"review_item_id":"invalid_missing_full_text"}\n')

        local_existing_id = _make_review(target_root, "local_same_id", reviewed=True, label=LABEL_ML_CORRECT)
        target_store = PromptRouterReasonerReviewStore(target_root)
        _force_review_id(target_store, local_existing_id, existing_source_id)
        _make_review(target_root, "duplicate", reviewed=False)
        target_store = PromptRouterReasonerReviewStore(target_root)
        before_events = target_store.iter_events()

        preview = target_store.preview_import_review_dataset(import_jsonl)
        after_events = target_store.iter_events()

        assert before_events == after_events
        assert preview["dry_run"] is True
        assert preview["ok"] is False
        assert preview["imported_count"] == 0
        assert preview["would_import_count"] == 0
        assert preview["conflict_count"] == 3
        assert len(preview["skipped_existing_conflicts"]) == 1
        assert len(preview["skipped_duplicate_conflicts"]) == 1
        assert len(preview["invalid_conflicts"]) == 1
        assert preview["metadata"]["conflict_count"] == 3
        assert preview["metadata"]["labels_overwritten"] is False
        reasons = {record["reason"] for record in preview["conflict_records"]}
        assert reasons == {
            "existing_review_item_id",
            "duplicate_generator_prompt_fingerprint",
            "invalid_row",
        }
        existing_conflict = preview["skipped_existing_conflicts"][0]
        assert existing_conflict["existing_human_label"] == LABEL_ML_CORRECT
        assert existing_conflict["incoming_human_label"] == LABEL_HEURISTICS_CORRECT
        assert target_store.get_review_item(existing_source_id)["human_label"] == LABEL_ML_CORRECT


def test_gui_import_conflict_review_button_summarizes_conflicts_if_pyside_available() -> None:
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
        review_id = _make_review(source_root, "gui_conflict", reviewed=True)
        _copy_export_jsonl_to_import_folder(source_root, target_root)

        local_id = _make_review(target_root, "local_gui_conflict", reviewed=True, label=LABEL_ML_CORRECT)
        target_store = PromptRouterReasonerReviewStore(target_root)
        _force_review_id(target_store, local_id, review_id)

        widget = PromptRouterReasonerTab()
        widget.set_project_root(target_root)
        state = widget.get_import_review_dataset_state()
        assert state["review_conflicts_enabled"] is True
        assert state["latest_dataset_file"].startswith(IMPORT_DATASETS_FOLDER_NAME + "/")

        result = widget.review_import_conflicts()
        conflict_state = widget.get_import_conflict_review_state()
        assert result["dry_run"] is True
        assert result["conflict_review"] is True
        assert result["conflict_count"] == 1
        assert conflict_state["conflict_count"] == 1
        assert conflict_state["conflict_records"][0]["reason"] == "existing_review_item_id"
        assert "Import conflict review" in conflict_state["status_text"]
        assert conflict_state["router_with_ml_locked"] is True
        assert widget.get_loaded_review_item_ids() == (review_id,)


if __name__ == "__main__":
    test_import_conflict_review_source_is_read_only_and_safe()
    test_store_import_conflict_review_reports_existing_duplicate_and_invalid_without_writes()
    test_gui_import_conflict_review_button_summarizes_conflicts_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner import conflict review")
