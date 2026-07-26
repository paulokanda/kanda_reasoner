"""Validation tests for Prompt Router Reasoner Review Dataset Export Polish v1."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    EXPORT_DATASETS_FOLDER_NAME,
    LABEL_HEURISTICS_CORRECT,
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


def _snapshot(prompt_id: str, prompt_name: str) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/export_polish/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="export_polish_group",
        prompt_version="v1",
        score=0.88,
        confidence=0.77,
        explanation="export polish explanation for " + prompt_name,
        keywords=("export_polish", prompt_id),
        route="export_polish_route",
        semantic_match="export polish semantic match",
        inferred_intent="export_review_dataset_polish",
        disagreement_reason="candidate differs for export polish validation",
        safety_status="safe_shadow_candidate",
    )


def _make_review(root: Path, token: str, *, reviewed: bool = False) -> str:
    store = PromptRouterReasonerReviewStore(root)
    review_id = store.create_pending_review(
        full_generator_text="Export polish generator text " + token,
        short_generator_text="Export polish " + token,
        generator_text_id="gen_export_polish_" + token,
        heuristic_prompt=_snapshot("heuristic_" + token, "Heuristic " + token),
        ml_prompt=_snapshot("ml_" + token, "ML " + token),
        app_version="prompt_router_reasoner_export_polish_v1_test",
        router_version="router_export_polish_test",
        retriever_version="retriever_export_polish_test",
        ml_version="ml_export_polish_test",
        prompt_library_version="prompt_library_export_polish_test",
    )
    if reviewed:
        store.save_review(review_id, LABEL_HEURISTICS_CORRECT)
    return review_id


def test_export_polish_source_is_export_only() -> None:
    store_source = _source_text(STORE_SOURCE_PATH)
    tab_source = _source_text(TAB_SOURCE_PATH)

    for text in [
        "latest_prompt_router_reasoner_review_dataset.json",
        "list_exported_review_datasets",
        "label_counts",
        "agreement_counts",
        "summary_text",
    ]:
        assert text in store_source

    for text in [
        "prompt_router_reasoner_export_dataset_summary_label",
        "prompt_router_reasoner_copy_latest_export_paths_button",
        "prompt_router_reasoner_copy_export_folder_path_button",
        "copy_latest_export_paths",
        "copy_export_folder_path",
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


def test_store_export_polish_writes_latest_metadata_and_recent_list_without_events() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        first_id = _make_review(root, "alpha", reviewed=True)
        _make_review(root, "beta", reviewed=False)
        store = PromptRouterReasonerReviewStore(root)
        before_events = store.iter_events()

        exported = store.export_review_dataset()
        after_events = store.iter_events()

        assert before_events == after_events
        metadata = exported["metadata"]
        assert metadata["row_count"] == 2
        assert metadata["reviewed_count"] == 1
        assert metadata["pending_count"] == 1
        assert metadata["training_ready_count"] == 1
        assert metadata["label_counts"][LABEL_HEURISTICS_CORRECT] == 1
        assert metadata["label_counts"]["unlabeled"] == 1
        assert metadata["history_unchanged"] is True
        assert metadata["labels_overwritten"] is False
        assert metadata["router_changed"] is False
        assert "training-ready" in metadata["summary_text"]
        assert exported["export_folder"] == EXPORT_DATASETS_FOLDER_NAME
        assert exported["latest_metadata_file"].endswith("latest_prompt_router_reasoner_review_dataset.json")

        latest_metadata_path = Path(exported["latest_metadata_path"])
        assert latest_metadata_path.exists()
        latest_metadata = json.loads(latest_metadata_path.read_text(encoding="utf-8-sig"))
        assert latest_metadata["jsonl_file"] == exported["jsonl_file"]
        assert latest_metadata["artifact_files"] == list(exported["artifact_files"])

        records = store.list_exported_review_datasets(limit=5)
        assert len(records) == 1
        assert records[0]["jsonl_file"] == exported["jsonl_file"]
        assert records[0]["training_ready_count"] == 1
        assert first_id in Path(exported["jsonl_path"]).read_text(encoding="utf-8-sig")


def test_gui_export_polish_copy_helpers_if_pyside_available() -> None:
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
        _make_review(root, "gui", reviewed=True)

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        before_state = widget.get_export_review_dataset_state()
        assert before_state["export_enabled"] is True
        assert before_state["copy_export_paths_enabled"] is False
        assert before_state["copy_export_folder_enabled"] is False

        exported = widget.export_review_dataset()
        assert exported["ok"] is True
        assert exported["latest_metadata_file"].endswith("latest_prompt_router_reasoner_review_dataset.json")
        assert Path(exported["latest_metadata_path"]).exists()
        assert Path(exported["export_folder_path"]).exists()

        state = widget.get_export_review_dataset_state()
        assert state["copy_export_paths_enabled"] is True
        assert state["copy_export_folder_enabled"] is True
        assert "training-ready" in state["export_summary_text"]
        assert state["latest_export"]["recent_exports"]
        assert state["router_with_ml_locked"] is True

        widget.copy_latest_export_paths()
        clipboard_text = QApplication.clipboard().text()
        assert exported["jsonl_path"] in clipboard_text
        assert exported["csv_path"] in clipboard_text
        assert exported["metadata_path"] in clipboard_text
        assert exported["export_folder_path"] in clipboard_text

        widget.copy_export_folder_path()
        assert QApplication.clipboard().text() == exported["export_folder_path"]


if __name__ == "__main__":
    test_export_polish_source_is_export_only()
    test_store_export_polish_writes_latest_metadata_and_recent_list_without_events()
    test_gui_export_polish_copy_helpers_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner review dataset export polish")
