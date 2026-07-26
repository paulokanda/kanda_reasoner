from pathlib import Path

HANDOFF = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_COMPLETION_HANDOFF_V1.md"
)
STATUS = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_COMPLETION_STATUS_V1.md"
)
README = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/README.md")
PREV = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_FINAL_SAFETY_GATE_V1.md"
)


def test_phase8_panel_ui_completion_handoff_contract():
    text = HANDOFF.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase8_read_only_advisory_panel_ui_completion_handoff_v1" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Final Safety Gate v1" in text
    assert "dormant renderer-neutral bounded in-memory read-only panel" in text
    assert "Phase 7 read-only advisory surface envelope" in text
    assert "bounded typed panel sections" in text
    assert "governed router remains the final selector" in text
    assert "ML Advisory Signal remains telemetry only" in text
    assert "Governed Prompt Intake remains the only safe door" in text
    assert "Manual Prompt Code Hint remains classification help only" in text
    assert "no runtime advisory panel activation" in text
    assert "no runtime UI mutation" in text
    assert "no runtime telemetry surface wiring" in text
    assert "no renderer activation" in text
    assert "no mounted panel" in text
    assert "no route influence" in text
    assert "no route authority" in text
    assert "no runtime Copilot decision behavior" in text
    assert "no MLRT-113" in text
    assert "critical boundary error budget zero" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Contract v1" in text


def test_phase8_panel_ui_completion_status_contract():
    text = STATUS.read_text(encoding="utf-8")
    assert "Completion handoff only" in text
    assert "dormant" in text
    assert "renderer-neutral bounded in-memory read-only panel view-model foundation" in text
    assert "There is no mounted visible panel" in text
    assert "governed router final selector remains unchanged" in text
    assert "There is no automatic next implementation step" in text
    assert "new governed activation" in text
    assert "not a UI activation file" in text
    assert "not a mounted-panel registration file" in text


def test_phase8_panel_ui_completion_readme_registered_and_final_safety_present():
    readme = README.read_text(encoding="utf-8")
    assert "Phase 8 read-only advisory panel UI completion handoff" in readme
    assert "not a mounted visible panel" in readme
    assert "not runtime panel activation" in readme
    assert "not route authority" in readme
    assert "Phase 9 Read-Only Advisory Panel Runtime Activation Contract" in readme
    assert PREV.exists()


if __name__ == "__main__":
    test_phase8_panel_ui_completion_handoff_contract()
    test_phase8_panel_ui_completion_status_contract()
    test_phase8_panel_ui_completion_readme_registered_and_final_safety_present()
    print("VALIDATION OK: phase8 read-only advisory panel UI completion handoff")
