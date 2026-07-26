"""Validation tests for Prompt Router Reasoner Export Review Dataset v1."""

from __future__ import annotations

import csv
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


def _snapshot(prompt_id: str, prompt_name: str, *, route: str = "export_route") -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        prompt_path="ACTIVE_PROMPTS/export/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_name,
        prompt_group="export_group",
        prompt_version="v1",
        score=0.81,
        confidence=0.72,
        explanation="export dataset explanation for " + prompt_name,
        keywords=("export", prompt_id),
        route=route,
        semantic_match="export semantic match",
        inferred_intent="export_review_dataset",
        disagreement_reason="candidate differs for export validation",
        safety_status="safe_shadow_candidate",
    )


def _make_review(root: Path, token: str, *, reviewed: bool = False) -> str:
    store = PromptRouterReasonerReviewStore(root)
    review_id = store.create_pending_review(
        full_generator_text="Export dataset generator text " + token,
        short_generator_text="Export dataset " + token,
        generator_text_id="gen_export_" + token,
        heuristic_prompt=_snapshot("heuristic_" + token, "Heuristic " + token),
        ml_prompt=_snapshot("ml_" + token, "ML " + token),
        app_version="prompt_router_reasoner_export_review_dataset_v1_test",
        router_version="router_export_test",
        retriever_version="retriever_export_test",
        ml_version="ml_export_test",
        prompt_library_version="prompt_library_export_test",
    )
    if reviewed:
        store.save_review(review_id, LABEL_HEURISTICS_CORRECT)
    return review_id


def test_export_review_dataset_source_is_export_only() -> None:
    store_source = _source_text(STORE_SOURCE_PATH)
    tab_source = _source_text(TAB_SOURCE_PATH)

    for text in [
        "EXPORT_DATASETS_FOLDER_NAME",
        "export_review_dataset",
        "prompt_router_reasoner_export_review_dataset",
        "_review_item_to_export_row",
        "_export_fieldnames",
    ]:
        assert text in store_source

    for text in [
        "prompt_router_reasoner_export_review_dataset_button",
        "export_review_dataset",
        "get_export_review_dataset_state",
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


def test_store_exports_jsonl_csv_and_metadata_without_review_events() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        first_id = _make_review(root, "alpha", reviewed=True)
        second_id = _make_review(root, "beta", reviewed=False)
        store = PromptRouterReasonerReviewStore(root)
        before_events = store.iter_events()

        exported = store.export_review_dataset()
        after_events = store.iter_events()

        assert before_events == after_events
        metadata = exported["metadata"]
        assert metadata["kind"] == "prompt_router_reasoner_export_review_dataset"
        assert metadata["row_count"] == 2
        assert metadata["reviewed_count"] == 1
        assert metadata["pending_count"] == 1
        assert metadata["training_ready_count"] == 1
        assert metadata["advisory_only"] is True
        assert metadata["history_unchanged"] is True
        assert exported["jsonl_file"].startswith(EXPORT_DATASETS_FOLDER_NAME + "/")
        assert exported["csv_file"].startswith(EXPORT_DATASETS_FOLDER_NAME + "/")
        assert exported["metadata_file"].startswith(EXPORT_DATASETS_FOLDER_NAME + "/")

        jsonl_path = Path(exported["jsonl_path"])
        csv_path = Path(exported["csv_path"])
        metadata_path = Path(exported["metadata_path"])
        assert jsonl_path.exists()
        assert csv_path.exists()
        assert metadata_path.exists()
        for path in (jsonl_path, csv_path, metadata_path):
            relative = path.relative_to(root).as_posix()
            assert relative.startswith("prompt_router_reasoner_reviews/" + EXPORT_DATASETS_FOLDER_NAME + "/")

        rows = [json.loads(line) for line in jsonl_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        assert {row["review_item_id"] for row in rows} == {first_id, second_id}
        reviewed_rows = [row for row in rows if row["review_item_id"] == first_id]
        assert reviewed_rows[0]["training_label"] == LABEL_HEURISTICS_CORRECT
        assert reviewed_rows[0]["is_training_ready"] is True
        assert reviewed_rows[0]["heuristic_prompt_id"] == "heuristic_alpha"
        assert reviewed_rows[0]["ml_prompt_id"] == "ml_alpha"

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            csv_rows = list(csv.DictReader(handle))
        assert len(csv_rows) == 2
        assert {row["review_item_id"] for row in csv_rows} == {first_id, second_id}
        assert "full_generator_text" in csv_rows[0]
        assert "ml_prompt_hash" in csv_rows[0]


def test_gui_export_button_writes_dataset_if_pyside_available() -> None:
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
        review_id = _make_review(root, "gui", reviewed=True)

        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        state = widget.get_export_review_dataset_state()
        assert state["export_enabled"] is True
        assert state["loaded_total"] == 1

        exported = widget.export_review_dataset()
        assert exported["ok"] is True
        assert exported["row_count"] == 1
        assert exported["training_ready_count"] == 1
        assert Path(exported["jsonl_path"]).exists()
        assert Path(exported["csv_path"]).exists()
        assert Path(exported["metadata_path"]).exists()
        state = widget.get_export_review_dataset_state()
        assert state["latest_export"]["jsonl_file"] == exported["jsonl_file"]
        assert state["router_with_ml_locked"] is True
        assert widget.get_selected_review_item_id() is None
        jsonl_text = Path(exported["jsonl_path"]).read_text(encoding="utf-8-sig")
        assert review_id in jsonl_text


if __name__ == "__main__":
    test_export_review_dataset_source_is_export_only()
    test_store_exports_jsonl_csv_and_metadata_without_review_events()
    test_gui_export_button_writes_dataset_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner export review dataset")
