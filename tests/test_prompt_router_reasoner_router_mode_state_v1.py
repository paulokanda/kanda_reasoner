"""Tests for Prompt Router Reasoner Router Mode State v1."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    REVIEW_FOLDER_NAME,
    ROUTER_WITH_HEURISTICS,
    ROUTER_WITH_HELP_OF_ML,
    ROUTER_WITH_ML,
    PromptRouterReasonerStoreError,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_router_mode_state import (
    BLOCK_REASON_ML_PILOT_LOCKED,
    MODE_CHANGE_STATUS_APPLIED,
    MODE_CHANGE_STATUS_BLOCKED,
    MODE_CHANGE_STATUS_UNCHANGED,
    ROUTER_MODE_STATE_FILENAME,
    PromptRouterReasonerRouterModeState,
)


def test_router_mode_state_defaults_to_heuristics(tmp_path: Path) -> None:
    state = PromptRouterReasonerRouterModeState(tmp_path)
    loaded = state.load_state()

    assert loaded["effective_mode"] == ROUTER_WITH_HEURISTICS
    assert loaded["requested_mode"] == ROUTER_WITH_HEURISTICS
    assert loaded["ml_pilot_locked"] is True
    assert loaded["router_authority"] == "heuristics_authoritative_until_validated_ml_pilot"
    assert loaded["ml_authority"] == "validated_pilot_only_after_readiness_gate"
    assert (tmp_path / REVIEW_FOLDER_NAME / ROUTER_MODE_STATE_FILENAME).exists()


def test_router_mode_state_allows_help_of_ml_without_route_authority(tmp_path: Path) -> None:
    state = PromptRouterReasonerRouterModeState(tmp_path)
    result = state.set_mode(ROUTER_WITH_HELP_OF_ML)

    assert result.status == MODE_CHANGE_STATUS_APPLIED
    assert result.effective_mode == ROUTER_WITH_HELP_OF_ML
    assert result.requested_mode == ROUTER_WITH_HELP_OF_ML
    assert result.ml_pilot_locked is True
    assert state.get_effective_mode() == ROUTER_WITH_HELP_OF_ML

    reloaded = PromptRouterReasonerRouterModeState(tmp_path)
    assert reloaded.get_effective_mode() == ROUTER_WITH_HELP_OF_ML


def test_router_mode_state_ml_mode_blocks_without_readiness_stats(tmp_path: Path) -> None:
    state = PromptRouterReasonerRouterModeState(tmp_path)
    state.set_mode(ROUTER_WITH_HELP_OF_ML)

    result = state.set_mode(ROUTER_WITH_ML)

    assert result.status == MODE_CHANGE_STATUS_BLOCKED
    assert result.requested_mode == ROUTER_WITH_ML
    assert result.effective_mode == ROUTER_WITH_HELP_OF_ML
    assert result.ml_pilot_locked is True
    assert "ml_pilot_readiness_gate_not_met" in result.blocking_reasons
    assert state.get_effective_mode() == ROUTER_WITH_HELP_OF_ML


def test_router_mode_state_auto_activates_ml_when_readiness_passes(tmp_path: Path) -> None:
    state = PromptRouterReasonerRouterModeState(tmp_path)
    state.set_mode(ROUTER_WITH_HELP_OF_ML)

    result = state.set_mode(
        ROUTER_WITH_ML,
        readiness_stats={
            "pilot_threshold_met": True,
            "pilot_blocking_reasons": [],
        },
    )

    assert result.status == MODE_CHANGE_STATUS_APPLIED
    assert result.requested_mode == ROUTER_WITH_ML
    assert result.effective_mode == ROUTER_WITH_ML
    assert result.ml_pilot_locked is False
    assert result.blocking_reasons == ()
    assert state.get_effective_mode() == ROUTER_WITH_ML
    assert state.load_state()["ml_pilot_locked"] is False


def test_router_mode_state_ml_mode_blocks_failed_readiness(tmp_path: Path) -> None:
    state = PromptRouterReasonerRouterModeState(tmp_path)
    result = state.set_mode(
        ROUTER_WITH_ML,
        governed_pilot_unlock=True,
        readiness_stats={
            "pilot_threshold_met": False,
            "pilot_blocking_reasons": ["reviewed_total_below_minimum"],
        },
    )

    assert result.status == MODE_CHANGE_STATUS_BLOCKED
    assert result.effective_mode == ROUTER_WITH_HEURISTICS
    assert "ml_pilot_readiness_gate_not_met" in result.blocking_reasons
    assert "ml_pilot_readiness_has_blocking_reasons" in result.blocking_reasons


def test_router_mode_state_reset_and_unchanged_status(tmp_path: Path) -> None:
    state = PromptRouterReasonerRouterModeState(tmp_path)
    unchanged = state.set_mode("heuristics")
    assert unchanged.status == MODE_CHANGE_STATUS_UNCHANGED

    state.set_mode(ROUTER_WITH_HELP_OF_ML)
    reset = state.reset_to_heuristics()
    assert reset.status == MODE_CHANGE_STATUS_APPLIED
    assert reset.effective_mode == ROUTER_WITH_HEURISTICS


def test_router_mode_state_does_not_write_to_freeze_memory(tmp_path: Path) -> None:
    state = PromptRouterReasonerRouterModeState(tmp_path)
    state.set_mode(ROUTER_WITH_HELP_OF_ML)

    assert not (tmp_path / "project_freeze_after_update").exists()
    assert not (tmp_path / "project_freeze_ledger").exists()
    assert (tmp_path / REVIEW_FOLDER_NAME / ROUTER_MODE_STATE_FILENAME).exists()


def test_router_mode_state_rejects_freeze_memory_project_root(tmp_path: Path) -> None:
    unsafe_root = tmp_path / "project_freeze_after_update" / "frozen_features_memory"
    unsafe_root.mkdir(parents=True)

    try:
        PromptRouterReasonerRouterModeState(unsafe_root)
    except PromptRouterReasonerStoreError as exc:
        assert "router_mode_state_path_must_not_use_freeze_memory" in str(exc)
    else:
        raise AssertionError("unsafe freeze-memory root should have been rejected")

if __name__ == "__main__":
    import tempfile

    tests = [
        test_router_mode_state_defaults_to_heuristics,
        test_router_mode_state_allows_help_of_ml_without_route_authority,
        test_router_mode_state_ml_mode_blocks_without_readiness_stats,
        test_router_mode_state_auto_activates_ml_when_readiness_passes,
        test_router_mode_state_ml_mode_blocks_failed_readiness,
        test_router_mode_state_reset_and_unchanged_status,
        test_router_mode_state_does_not_write_to_freeze_memory,
        test_router_mode_state_rejects_freeze_memory_project_root,
    ]
    for test in tests:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            test(Path(temp_dir))
    print("VALIDATION OK: prompt router reasoner router mode state")
