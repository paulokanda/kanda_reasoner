from pathlib import Path

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE13_READ_ONLY_ADVISORY_PANEL_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT_RESULT_REVIEW_GATE_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE13_READ_ONLY_ADVISORY_PANEL_PASSIVE_VISIBILITY_ACTIVATION_IMPLEMENTATION_READINESS_V1.md")


def test_phase13_passive_visibility_activation_contract_result_review_gate_doc():
    text = DOC.read_text(encoding="utf-8")
    assert "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract Result Review Gate v1" in text
    assert "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_contract_v1" in text
    assert "Accepted for later governed implementation: yes." in text
    assert "Accepted as actual passive visibility activation: no." in text
    assert "Accepted as passive visibility slot registration: no." in text
    assert "Accepted as passive visibility slot mutation: no." in text
    assert "Accepted as actual runtime app-host visibility: no." in text
    assert "Accepted as visibility activation: no." in text
    assert "Accepted as mounted runtime panel: no." in text
    assert "Accepted as runtime UI mutation: no." in text
    assert "Accepted as runtime telemetry surface wiring: no." in text
    assert "Accepted as route influence or route authority: no." in text
    assert "Accepted as visible ML integration completion: no." in text
    assert "Phase 12 runtime app-host visibility descriptor lineage" in text
    assert "feature-flagged and default-off" in text
    assert "route-invariant" in text
    assert "final-selection-invisible" in text
    assert "non-authoritative" in text
    assert "Passive visibility slot registration" in text
    assert "Passive visibility slot mutation" in text
    assert "Runtime UI mutation" in text
    assert "Runtime telemetry surface wiring" in text
    assert "Host event subscription" in text
    assert "Host callback registration" in text
    assert "autonomous ML" in text
    assert "visible ML integration completion" in text
    assert "MLRT-113" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation v1" in text


def test_phase13_passive_visibility_activation_implementation_readiness_doc():
    text = READINESS.read_text(encoding="utf-8")
    assert "passive visibility activation implementation readiness" in text
    assert "Phase 12 runtime app-host visibility descriptor" in text
    assert "read-only" in text
    assert "feature-flagged" in text
    assert "default-off" in text
    assert "removable/no-op" in text
    assert "route-invariant" in text
    assert "final-selection-invisible" in text
    assert "fail-open" in text
    assert "non-authoritative" in text
    assert "must not add route authority" in text
    assert "runtime Copilot decision behavior" in text
    assert "visible ML integration completion" in text
    assert "MLRT-113" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation v1" in text


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_contract_result_review_gate_doc()
    test_phase13_passive_visibility_activation_implementation_readiness_doc()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation contract result review gate")
