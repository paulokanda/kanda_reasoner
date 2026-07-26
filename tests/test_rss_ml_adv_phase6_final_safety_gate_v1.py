from pathlib import Path


DOC = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_FINAL_SAFETY_GATE_V1.md"
)
HANDOFF = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_COMPLETION_HANDOFF_V1.md"
)
README = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/README.md")
PREV = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
)


def test_phase6_final_safety_gate_contract():
    text = DOC.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase6_guarded_runtime_advisory_display_final_safety_gate_v1" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Implementation Result Review Gate v1" in text
    assert "safe only" in text and "non-authoritative telemetry payload construction" in text
    assert "final-selection-invisible" in text
    assert "route-invariant" in text
    assert "no router prompt logic modification" in text
    assert "no router final selection modification" in text
    assert "no route authority" in text
    assert "no runtime advisory panel" in text
    assert "no runtime UI mutation" in text
    assert "no runtime Copilot decision behavior" in text
    assert "no MLRT-113" in text
    assert "critical boundary error budget zero" in text


def test_phase6_completion_handoff_boundaries():
    text = HANDOFF.read_text(encoding="utf-8")
    assert "bounded in-memory" in text and "read-only telemetry payload builder" in text
    assert "cannot influence routing" in text
    assert "router final selection modification" in text
    assert "real ML/provider calls" in text
    assert "do not call the next feature a Copilot decision feature" in text
    assert "governed router must remain the final selector" in text


def test_phase6_final_safety_readme_registered_and_prior_review_present():
    readme = README.read_text(encoding="utf-8")
    assert "Phase 6 guarded runtime advisory display final safety gate" in readme
    assert "does not wire a runtime advisory panel" in readme
    assert PREV.exists()


if __name__ == "__main__":
    test_phase6_final_safety_gate_contract()
    test_phase6_completion_handoff_boundaries()
    test_phase6_final_safety_readme_registered_and_prior_review_present()
    print("VALIDATION OK: phase6 guarded runtime advisory display final safety gate")
