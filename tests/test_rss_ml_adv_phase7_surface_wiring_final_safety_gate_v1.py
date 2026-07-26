from pathlib import Path


DOC = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_FINAL_SAFETY_GATE_V1.md"
)
HANDOFF_READY = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_COMPLETION_HANDOFF_READINESS_V1.md"
)
README = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/README.md")
PREV = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
)
IMPL = Path(
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/"
    "read_only_advisory_surface_wiring.py"
)


def test_phase7_read_only_surface_wiring_final_safety_gate_contract():
    text = DOC.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase7_read_only_advisory_surface_wiring_final_safety_gate_v1" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Implementation Result Review Gate v1" in text
    assert "safe only" in text and "non-authoritative telemetry surface envelope" in text
    assert "uses a copied canonical dispatch snapshot unchanged" in text
    assert "consumes already-built guarded advisory display payloads only" in text
    assert "final-selection-invisible" in text
    assert "route-invariant" in text
    assert "no runtime advisory panel activation" in text
    assert "no runtime UI mutation" in text
    assert "no runtime telemetry surface wiring" in text
    assert "no route influence" in text
    assert "no route authority" in text
    assert "no router prompt logic modification" in text
    assert "no router final selection modification" in text
    assert "no runtime Copilot decision behavior" in text
    assert "no MLRT-113" in text
    assert "critical boundary error budget zero" in text


def test_phase7_read_only_surface_wiring_final_safety_handoff_readiness():
    text = HANDOFF_READY.read_text(encoding="utf-8")
    assert "Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Completion Handoff v1" in text
    assert "bounded in-memory read-only telemetry envelope logic" in text
    assert "no runtime panel has been activated" in text
    assert "no UI mutation has been wired" in text
    assert "no route authority or route influence exists" in text
    assert "separate advisory panel UI contract" in text


def test_phase7_read_only_surface_wiring_final_safety_readme_and_prior_artifacts_present():
    readme = README.read_text(encoding="utf-8")
    assert "Phase 7 read-only advisory surface wiring final safety gate" in readme
    assert "does not activate a runtime advisory" in readme and "panel" in readme
    assert PREV.exists()
    assert IMPL.exists()


if __name__ == "__main__":
    test_phase7_read_only_surface_wiring_final_safety_gate_contract()
    test_phase7_read_only_surface_wiring_final_safety_handoff_readiness()
    test_phase7_read_only_surface_wiring_final_safety_readme_and_prior_artifacts_present()
    print("VALIDATION OK: phase7 read-only advisory surface wiring final safety gate")
