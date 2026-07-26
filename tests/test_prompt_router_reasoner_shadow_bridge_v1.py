from __future__ import annotations

from pathlib import Path
import tempfile

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    AGREEMENT_AGREE,
    AGREEMENT_DISAGREE,
    PromptRouterReasonerReviewStore,
    ROUTER_WITH_HEURISTICS,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_shadow_bridge import (
    SHADOW_REASON_DISABLED,
    SHADOW_REASON_NO_ML_PROMPT,
    SHADOW_STATUS_CAPTURED,
    SHADOW_STATUS_SKIPPED,
    bridge_result_keeps_authoritative_output,
    build_prompt_snapshot_from_candidate,
    capture_shadow_prompt_selection,
)


def _candidate(prompt_id: str, prompt_hash: str | None = None) -> dict:
    return {
        "prompt_id": prompt_id,
        "prompt_name": "Prompt " + prompt_id,
        "prompt_path": "ACTIVE_PROMPTS/" + prompt_id + ".md",
        "prompt_hash": prompt_hash or ("hash_" + prompt_id),
        "prompt_summary": "Summary for " + prompt_id,
        "prompt_group": "test_group",
        "prompt_version": "1.0",
        "score": 0.75,
        "confidence": 0.70,
        "explanation": "Selected for test coverage.",
        "keywords": ["test", prompt_id],
        "route": "test_route",
        "semantic_match": "test semantic match",
        "inferred_intent": "test intent",
        "disagreement_reason": "test disagreement",
        "safety_status": "safe_shadow_candidate",
    }


def test_shadow_bridge_captures_disagreement_without_changing_authoritative_output() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = PromptRouterReasonerReviewStore(Path(temp_dir))
        final_output = {"route": "deterministic", "prompt": "heuristic_prompt"}

        result = capture_shadow_prompt_selection(
            full_generator_text="Create a patch for the prompt router reasoner.",
            heuristic_prompt=_candidate("heuristic_prompt"),
            ml_prompt=_candidate("ml_prompt"),
            final_router_output=final_output,
            review_store=store,
            router_mode_at_capture=ROUTER_WITH_HEURISTICS,
            router_version="router-test",
            ml_version="ml-shadow-test",
        )

        assert result.shadow_status == SHADOW_STATUS_CAPTURED
        assert result.final_router_output is final_output
        assert bridge_result_keeps_authoritative_output(result, final_output) is True
        item = store.get_review_item(result.review_item_id)
        assert item["agreement_status"] == AGREEMENT_DISAGREE
        assert item["review_status"] == "pending"
        assert item["heuristic_prompt"]["prompt_id"] == "heuristic_prompt"
        assert item["ml_prompt"]["prompt_id"] == "ml_prompt"
        assert item["router_version"] == "router-test"
        assert item["ml_version"] == "ml-shadow-test"


def test_shadow_bridge_captures_agreement_when_prompt_ids_match() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = PromptRouterReasonerReviewStore(Path(temp_dir))
        final_output = object()
        same = _candidate("same_prompt")

        result = capture_shadow_prompt_selection(
            full_generator_text="Use the same prompt.",
            heuristic_prompt=same,
            ml_prompt=same,
            final_router_output=final_output,
            review_store=store,
        )

        assert result.shadow_status == SHADOW_STATUS_CAPTURED
        assert result.final_router_output is final_output
        assert store.get_review_item(result.review_item_id)["agreement_status"] == AGREEMENT_AGREE


def test_shadow_bridge_fails_open_when_disabled() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = PromptRouterReasonerReviewStore(Path(temp_dir))
        final_output = {"route": "ranked"}

        result = capture_shadow_prompt_selection(
            full_generator_text="Disabled bridge should not capture.",
            heuristic_prompt=_candidate("heuristic_prompt"),
            ml_prompt=_candidate("ml_prompt"),
            final_router_output=final_output,
            review_store=store,
            enabled=False,
        )

        assert result.shadow_status == SHADOW_STATUS_SKIPPED
        assert result.reason == SHADOW_REASON_DISABLED
        assert result.final_router_output is final_output
        assert len(store.list_review_items()) == 0


def test_shadow_bridge_fails_open_when_ml_prompt_missing() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = PromptRouterReasonerReviewStore(Path(temp_dir))
        final_output = {"route": "generative"}

        result = capture_shadow_prompt_selection(
            full_generator_text="Missing ML prompt should not break routing.",
            heuristic_prompt=_candidate("heuristic_prompt"),
            ml_prompt=None,
            final_router_output=final_output,
            review_store=store,
        )

        assert result.shadow_status == SHADOW_STATUS_SKIPPED
        assert result.reason == SHADOW_REASON_NO_ML_PROMPT
        assert result.final_router_output is final_output
        assert len(store.list_review_items()) == 0


def test_shadow_bridge_can_create_store_from_project_root() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        final_output = {"prompt": "unchanged"}

        result = capture_shadow_prompt_selection(
            full_generator_text="Create store from project root.",
            heuristic_prompt=_candidate("heuristic_prompt"),
            ml_prompt=_candidate("ml_prompt"),
            final_router_output=final_output,
            project_root=root,
        )

        assert result.shadow_status == SHADOW_STATUS_CAPTURED
        assert (root / "prompt_router_reasoner_reviews").exists()
        store = PromptRouterReasonerReviewStore(root)
        assert len(store.list_review_items()) == 1


def test_candidate_normalization_is_pure_and_requires_snapshot_fields() -> None:
    snapshot = build_prompt_snapshot_from_candidate(_candidate("candidate_prompt"), role="heuristic")
    assert snapshot.prompt_id == "candidate_prompt"
    assert snapshot.prompt_hash == "hash_candidate_prompt"


def test_shadow_bridge_does_not_write_to_freeze_memory_or_ledger() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        capture_shadow_prompt_selection(
            full_generator_text="Capture outside freeze memory.",
            heuristic_prompt=_candidate("heuristic_prompt"),
            ml_prompt=_candidate("ml_prompt"),
            project_root=root,
        )
        assert (root / "prompt_router_reasoner_reviews").exists()
        assert not (root / "project_freeze_after_update").exists()
        assert not (root / "project_freeze_ledger").exists()


if __name__ == "__main__":
    test_shadow_bridge_captures_disagreement_without_changing_authoritative_output()
    test_shadow_bridge_captures_agreement_when_prompt_ids_match()
    test_shadow_bridge_fails_open_when_disabled()
    test_shadow_bridge_fails_open_when_ml_prompt_missing()
    test_shadow_bridge_can_create_store_from_project_root()
    test_candidate_normalization_is_pure_and_requires_snapshot_fields()
    test_shadow_bridge_does_not_write_to_freeze_memory_or_ledger()
    print("VALIDATION OK: prompt router reasoner shadow ml bridge")
