from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    AGREEMENT_AGREE,
    AGREEMENT_DISAGREE,
    LABEL_BOTH_ACCEPTABLE_UNCLEAR,
    LABEL_HEURISTICS_CORRECT,
    LABEL_ML_CORRECT,
    PromptRouterReasonerReviewStore,
    PromptRouterReasonerStoreError,
    PromptSnapshot,
    REVIEW_FOLDER_NAME,
    STATUS_PENDING,
    STATUS_REVIEWED,
)


def _snapshot(prompt_id: str, prompt_name: str | None = None) -> PromptSnapshot:
    return PromptSnapshot(
        prompt_id=prompt_id,
        prompt_name=prompt_name or prompt_id,
        prompt_path="prompts/" + prompt_id + ".md",
        prompt_hash="hash_" + prompt_id,
        prompt_summary="summary for " + prompt_id,
        prompt_group="test_group",
        prompt_version="1",
        score=0.9,
        explanation="selected for deterministic test reasons",
        keywords=("test", prompt_id),
        route="test_route",
    )


def test_store_creates_only_project_local_review_folder() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        store = PromptRouterReasonerReviewStore(root)
        assert store.review_dir == root / REVIEW_FOLDER_NAME
        assert store.log_file.exists()
        assert store.index_file.exists()
        assert store.stats_file.exists()
        assert store.ask_ai_requests_dir.exists()
        assert store.ask_ai_answers_dir.exists()
        assert not (root / "project_freeze_ledger" / REVIEW_FOLDER_NAME).exists()
        assert not (
            root / "project_freeze_after_update" / "frozen_features_memory" / REVIEW_FOLDER_NAME
        ).exists()
        for path in store.expected_storage_paths():
            relative = str(path.relative_to(root)).replace("\\", "/")
            assert relative.startswith(REVIEW_FOLDER_NAME)
            assert "project_freeze_ledger" not in relative
            assert "project_freeze_after_update" not in relative


def test_pending_review_persists_and_reloads() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        store = PromptRouterReasonerReviewStore(root)
        review_id = store.create_pending_review(
            full_generator_text="Create a patch for startup delivery.",
            heuristic_prompt=_snapshot("heuristic_prompt"),
            ml_prompt=_snapshot("ml_prompt"),
        )
        item = store.get_review_item(review_id)
        assert item["review_status"] == STATUS_PENDING
        assert item["agreement_status"] == AGREEMENT_DISAGREE
        assert item["human_label"] is None
        assert item["undo_available"] is False
        assert item["heuristic_prompt"]["prompt_id"] == "heuristic_prompt"
        assert item["ml_prompt"]["prompt_id"] == "ml_prompt"
        assert item["generator_text_hash"]

        reloaded = PromptRouterReasonerReviewStore(root)
        loaded = reloaded.get_review_item(review_id)
        assert loaded["review_item_id"] == review_id
        assert loaded["short_generator_text"] == "Create a patch for startup delivery."


def test_same_prompt_selection_is_agreement() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = PromptRouterReasonerReviewStore(Path(temp_dir))
        same = _snapshot("same_prompt")
        review_id = store.create_pending_review(
            full_generator_text="Use the same prompt.",
            heuristic_prompt=same,
            ml_prompt=same,
        )
        assert store.get_review_item(review_id)["agreement_status"] == AGREEMENT_AGREE


def test_save_and_undo_are_append_only_events() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = PromptRouterReasonerReviewStore(Path(temp_dir))
        review_id = store.create_pending_review(
            full_generator_text="Review one prompt choice.",
            heuristic_prompt=_snapshot("h"),
            ml_prompt=_snapshot("m"),
        )
        initial_events = store.iter_events()
        assert len(initial_events) == 1

        saved = store.save_review(review_id, LABEL_ML_CORRECT)
        assert saved["review_status"] == STATUS_REVIEWED
        assert saved["human_label"] == LABEL_ML_CORRECT
        assert saved["undo_available"] is True
        after_save_events = store.iter_events()
        assert len(after_save_events) == 2
        assert after_save_events[-1]["event_type"] == "review_saved"

        undone = store.undo_last_save(review_id)
        assert undone["review_status"] == STATUS_PENDING
        assert undone["human_label"] is None
        assert undone["undo_available"] is False
        after_undo_events = store.iter_events()
        assert len(after_undo_events) == 3
        assert after_undo_events[-1]["event_type"] == "review_undone"

        rebuilt = store.rebuild_index_from_log()
        assert rebuilt["items"][review_id]["review_status"] == STATUS_PENDING
        assert rebuilt["items"][review_id]["human_label"] is None


def test_filters_and_labels() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = PromptRouterReasonerReviewStore(Path(temp_dir))
        first = store.create_pending_review(
            full_generator_text="Heuristic wins.",
            heuristic_prompt=_snapshot("h1"),
            ml_prompt=_snapshot("m1"),
        )
        second = store.create_pending_review(
            full_generator_text="ML wins.",
            heuristic_prompt=_snapshot("h2"),
            ml_prompt=_snapshot("m2"),
        )
        third = store.create_pending_review(
            full_generator_text="Both ok.",
            heuristic_prompt=_snapshot("h3"),
            ml_prompt=_snapshot("m3"),
        )
        store.save_review(first, LABEL_HEURISTICS_CORRECT)
        store.save_review(second, LABEL_ML_CORRECT)
        store.save_review(third, LABEL_BOTH_ACCEPTABLE_UNCLEAR)

        assert len(store.list_review_items(review_status=STATUS_REVIEWED)) == 3
        assert len(store.list_review_items(human_label=LABEL_HEURISTICS_CORRECT)) == 1
        assert len(store.list_review_items(human_label=LABEL_ML_CORRECT)) == 1
        assert len(store.list_review_items(human_label=LABEL_BOTH_ACCEPTABLE_UNCLEAR)) == 1
        assert len(store.list_review_items(agreement_status=AGREEMENT_DISAGREE)) == 3


def test_store_refuses_forbidden_review_directory() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        forbidden_root = Path(temp_dir) / "project_freeze_after_update"
        try:
            PromptRouterReasonerReviewStore(forbidden_root)
        except PromptRouterReasonerStoreError as exc:
            assert "must not be stored" in str(exc)
        else:
            raise AssertionError("store should reject freeze-memory-like review path")


if __name__ == "__main__":
    test_store_creates_only_project_local_review_folder()
    test_pending_review_persists_and_reloads()
    test_same_prompt_selection_is_agreement()
    test_save_and_undo_are_append_only_events()
    test_filters_and_labels()
    test_store_refuses_forbidden_review_directory()
    print("VALIDATION OK: prompt router reasoner persistent review store")
