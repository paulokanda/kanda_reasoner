from pathlib import Path

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE13_READ_ONLY_ADVISORY_PANEL_PASSIVE_VISIBILITY_ACTIVATION_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE13_READ_ONLY_ADVISORY_PANEL_PASSIVE_VISIBILITY_ACTIVATION_FINAL_SAFETY_GATE_READINESS_V1.md")


def test_phase13_passive_visibility_activation_implementation_result_review_gate_doc():
    text = DOC.read_text(encoding="utf-8")
    assert "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation Result Review Gate v1" in text
    assert "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_result_review_gate_v1" in text
    assert "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_v1" in text
    assert "safe for a later final safety gate" in text
    assert "feature-flagged" in text
    assert "default-off" in text
    assert "in-memory" in text
    assert "read-only passive visibility activation descriptor" in text
    assert "Phase 12 runtime app-host visibility descriptor lineage" in text
    assert "bounded passive visibility slot descriptors" in text
    assert "Accepted as actual passive visibility activation: no" in text
    assert "Accepted as passive visibility slot registration: no" in text
    assert "Accepted as passive visibility slot mutation: no" in text
    assert "Accepted as route influence or route authority: no" in text
    assert "Runtime UI mutation" in text
    assert "Runtime telemetry surface wiring" in text
    assert "Host event subscription" in text
    assert "Host callback registration" in text
    assert "visible ML integration completion" in text
    assert "MLRT-113" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Final Safety Gate v1" in text


def test_phase13_passive_visibility_activation_final_safety_gate_readiness_doc():
    text = READINESS.read_text(encoding="utf-8")
    assert "final safety gate readiness" in text
    assert "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_result_review_gate_v1" in text
    assert "completion handoff" in text
    assert "must not add actual passive visibility" in text
    assert "passive slot registration" in text
    assert "runtime UI mutation" in text
    assert "runtime telemetry surface wiring" in text
    assert "route authority" in text
    assert "runtime Copilot decision" in text
    assert "visible ML integration completion" in text
    assert "MLRT-113" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Final Safety Gate v1" in text


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_implementation_result_review_gate_doc()
    test_phase13_passive_visibility_activation_final_safety_gate_readiness_doc()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation implementation result review gate")
