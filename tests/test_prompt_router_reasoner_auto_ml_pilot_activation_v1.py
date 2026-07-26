"""Tests for readiness-gated automatic ML pilot activation."""

from __future__ import annotations

from pathlib import Path
import tempfile

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_stats import (
    compute_prompt_router_reasoner_stats,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    AGREEMENT_DISAGREE,
    LABEL_ML_CORRECT,
    REVIEW_FOLDER_NAME,
    ROUTER_WITH_ML,
    STATUS_REVIEWED,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_router_mode_state import (
    MODE_CHANGE_STATUS_APPLIED,
    PromptRouterReasonerRouterModeState,
)

try:
    from PySide6.QtWidgets import QApplication  # type: ignore[import-not-found]

    PYSIDE_AVAILABLE = True
except ImportError:
    QApplication = None  # type: ignore[assignment]
    PYSIDE_AVAILABLE = False


def _clean_ml_win_item(index: int) -> dict[str, object]:
    return {
        "review_item_id": "prr_auto_" + str(index),
        "review_status": STATUS_REVIEWED,
        "human_label": LABEL_ML_CORRECT,
        "agreement_status": AGREEMENT_DISAGREE,
        "safety_violation": False,
    }


def _passing_review_items(count: int = 500) -> list[dict[str, object]]:
    return [_clean_ml_win_item(index) for index in range(count)]


def test_default_policy_requires_conservative_clean_evidence() -> None:
    stats = compute_prompt_router_reasoner_stats(_passing_review_items())

    assert stats["pilot_activation_policy"] == "conservative_wilson_lcb_auto_ml_pilot_v1"
    assert stats["pilot_activation_thresholds"]["minimum_reviewed_total"] == 500
    assert stats["pilot_activation_thresholds"]["minimum_non_ambiguous_disagreements"] == 100
    assert stats["pilot_activation_thresholds"]["minimum_ml_strict_lower_bound"] == 0.95
    assert stats["pilot_activation_thresholds"]["minimum_ml_disagreement_lower_bound"] == 0.55
    assert stats["auto_ml_pilot_activation_eligible"] is True
    assert stats["pilot_threshold_met"] is True
    assert stats["pilot_readiness_percent"] == 100.0


def test_router_mode_state_auto_activates_ml_when_policy_passes() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        stats = compute_prompt_router_reasoner_stats(_passing_review_items())
        state = PromptRouterReasonerRouterModeState(root)

        result = state.activate_ml_pilot_if_ready(stats)

        assert result.status == MODE_CHANGE_STATUS_APPLIED
        assert result.effective_mode == ROUTER_WITH_ML
        assert result.ml_pilot_locked is False
        assert state.get_effective_mode() == ROUTER_WITH_ML
        assert state.load_state()["ml_pilot_locked"] is False
        assert (root / REVIEW_FOLDER_NAME).exists()
        assert not (root / "project_freeze_ledger").exists()
        assert not (root / "project_freeze_after_update").exists()


def test_gui_auto_removes_lock_when_policy_passes_if_pyside_available() -> None:
    if not PYSIDE_AVAILABLE:
        assert True
        return

    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (  # type: ignore[import-not-found]
        PromptRouterReasonerTab,
    )

    app = QApplication.instance()  # type: ignore[union-attr]
    if app is None:
        app = QApplication([])  # type: ignore[operator]

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        (root / REVIEW_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
        widget = PromptRouterReasonerTab()
        widget.set_project_root(root)
        widget._loaded_review_items = _passing_review_items()  # noqa: SLF001

        widget.refresh_stats_panel()
        readiness_state = widget.get_readiness_bar_state()
        mode_state = PromptRouterReasonerRouterModeState(root).load_state()

        assert readiness_state["pilot_value"] == 100
        assert readiness_state["router_with_ml_locked"] is False
        assert readiness_state["ml_pilot_activation_state"]["activation_applied"] is True
        assert widget.router_with_ml_radio.isChecked() is True
        assert mode_state["effective_mode"] == ROUTER_WITH_ML
        assert mode_state["ml_pilot_locked"] is False


if __name__ == "__main__":
    test_default_policy_requires_conservative_clean_evidence()
    test_router_mode_state_auto_activates_ml_when_policy_passes()
    test_gui_auto_removes_lock_when_policy_passes_if_pyside_available()
    print("VALIDATION OK: prompt router reasoner auto ml pilot activation")
