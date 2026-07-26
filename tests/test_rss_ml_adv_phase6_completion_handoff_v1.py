from pathlib import Path


HANDOFF = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_COMPLETION_HANDOFF_V1.md"
)
STATUS = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_COMPLETION_STATUS_V1.md"
)
README = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/README.md")
PREV = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_FINAL_SAFETY_GATE_V1.md"
)


def test_phase6_completion_handoff_contract():
    text = HANDOFF.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase6_guarded_runtime_advisory_display_completion_handoff_v1" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Final Safety Gate v1" in text
    assert "bounded in-memory read-only telemetry payload" in text
    assert "already computed AdvisoryOutput" in text
    assert "governed router remains the final selector" in text
    assert "ML Advisory Signal remains telemetry only" in text
    assert "Governed Prompt Intake remains the only safe door" in text
    assert "Manual Prompt Code Hint remains classification help only" in text
    assert "no route authority" in text
    assert "no runtime advisory panel" in text
    assert "no runtime UI mutation" in text
    assert "no runtime Copilot decision behavior" in text
    assert "no MLRT-113" in text
    assert "critical boundary error budget zero" in text


def test_phase6_completion_status_contract():
    text = STATUS.read_text(encoding="utf-8")
    assert "Completion handoff only" in text
    assert "bounded in-memory read-only telemetry payload construction" in text
    assert "There is no automatic next implementation step" in text
    assert "new governed boundary contract" in text
    assert "governed router final selector" in text


def test_phase6_completion_readme_registered_and_final_safety_present():
    readme = README.read_text(encoding="utf-8")
    assert "Phase 6 guarded runtime advisory display completion handoff" in readme
    assert "not a runtime Copilot decision system" in readme
    assert "must start as a separately" in readme
    assert PREV.exists()


if __name__ == "__main__":
    test_phase6_completion_handoff_contract()
    test_phase6_completion_status_contract()
    test_phase6_completion_readme_registered_and_final_safety_present()
    print("VALIDATION OK: phase6 guarded runtime advisory display completion handoff")
