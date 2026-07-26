from pathlib import Path


DOC = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
)
READINESS = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_FINAL_SAFETY_GATE_READINESS_V1.md"
)
README = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/README.md")


def test_phase6_display_implementation_review_gate_contract():
    text = DOC.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase6_guarded_runtime_advisory_display_implementation_result_review_gate_v1" in text
    assert "rss_ml_adv_phase6_guarded_runtime_advisory_display_implementation_v1" not in text  # reviewed by title in prose, not opaque-only evidence
    assert "bounded in-memory read-only telemetry payload builder" in text
    assert "actual validation output" in text
    assert "no router prompt logic modification" in text
    assert "no router final selection modification" in text
    assert "no route authority" in text
    assert "no runtime Copilot decision behavior" in text
    assert "no MLRT-113" in text
    assert "critical boundary error budget zero" in text


def test_phase6_display_final_safety_gate_readiness_doc():
    text = READINESS.read_text(encoding="utf-8")
    assert "Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Final Safety Gate v1" in text
    assert "Phase 6 display implementation is frozen with actual validation evidence" in text
    assert "Router prompt logic and router final selection remain unchanged" in text
    assert "bounded, read-only, in-memory, fail-open, removable" in text
    assert "must not implement an advisory panel" in text


def test_phase6_display_review_gate_readme_registered():
    text = README.read_text(encoding="utf-8")
    assert "Phase 6 guarded runtime advisory display implementation result review gate" in text
    assert "not runtime UI integration" in text


if __name__ == "__main__":
    test_phase6_display_implementation_review_gate_contract()
    test_phase6_display_final_safety_gate_readiness_doc()
    test_phase6_display_review_gate_readme_registered()
    print("VALIDATION OK: phase6 display implementation result review gate")
