from pathlib import Path

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_FINAL_SAFETY_GATE_V1.md")
HANDOFF_READY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_COMPLETION_HANDOFF_READINESS_V1.md")
README = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/README.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md")
IMPL = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_ui.py")


def test_phase8_read_only_panel_ui_final_safety_gate_contract():
    text = DOC.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase8_read_only_advisory_panel_ui_final_safety_gate_v1" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Implementation Result Review Gate v1" in text
    assert "dormant renderer-neutral read-only panel view-model foundation" in text
    assert "Phase 7 read-only advisory surface envelope" in text
    assert "bounded typed panel sections only" in text
    assert "explicit no route authority label" in text
    assert "confidence/status not route correctness proof" in text
    assert "no runtime advisory panel activation" in text
    assert "no runtime UI mutation" in text
    assert "no runtime telemetry surface wiring" in text
    assert "no renderer activation" in text
    assert "no route influence" in text
    assert "no route authority" in text
    assert "no runtime Copilot decision behavior" in text
    assert "no MLRT-113" in text
    assert "critical boundary error budget zero" in text


def test_phase8_read_only_panel_ui_final_safety_handoff_readiness():
    text = HANDOFF_READY.read_text(encoding="utf-8")
    assert "Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Completion Handoff v1" in text
    assert "dormant renderer-neutral bounded in-memory read-only panel view-model" in text and "foundation" in text
    assert "no runtime panel has been activated" in text
    assert "no UI mutation has been wired" in text
    assert "no renderer has been mounted" in text
    assert "no telemetry surface has been wired into live runtime" in text
    assert "future governed runtime" in text and "panel activation contract" in text


def test_phase8_read_only_panel_ui_final_safety_readme_and_prior_artifacts_present():
    readme = README.read_text(encoding="utf-8")
    assert "Phase 8 read-only advisory panel UI final safety gate" in readme
    assert "does not render a real UI" in readme
    assert "does not" in readme and "runtime Copilot decision behavior" in readme
    assert PREV.exists()
    assert IMPL.exists()


if __name__ == "__main__":
    test_phase8_read_only_panel_ui_final_safety_gate_contract()
    test_phase8_read_only_panel_ui_final_safety_handoff_readiness()
    test_phase8_read_only_panel_ui_final_safety_readme_and_prior_artifacts_present()
    print("VALIDATION OK: phase8 read-only advisory panel UI final safety gate")
