"""Repair tests for Prompt Router Reasoner auto ML pilot readiness state."""

from __future__ import annotations

from pathlib import Path


def test_readiness_bar_state_exposes_ml_pilot_activation_state() -> None:
    source_path = Path(
        "kanda_reasoner_app/prompt_router_reasoner_gui/prompt_router_reasoner_tab.py"
    )
    source = source_path.read_text(encoding="utf-8")

    assert "def get_readiness_bar_state" in source
    assert '"ml_pilot_activation_state": activation_state' in source
    assert '"activation_applied": False' in source
    assert '"router_with_ml_locked": True' in source
    assert "conservative_wilson_lcb_auto_ml_pilot_v1" in source


if __name__ == "__main__":
    test_readiness_bar_state_exposes_ml_pilot_activation_state()
    print("VALIDATION OK: prompt router reasoner auto ml pilot activation repair")
