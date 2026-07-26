from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_ui_contract import (
    FORBIDDEN_PANEL_CAPABILITIES,
    ALLOWED_PANEL_SECTIONS,
    ReadOnlyAdvisoryPanelUIContractPolicy,
    ReadOnlyPanelContractStatus,
    build_phase8_read_only_advisory_panel_ui_contract,
    evaluate_phase8_read_only_advisory_panel_ui_request,
)

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_CONTRACT_V1.md")
BOUNDARY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_BOUNDARY_MODEL_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_CONTRACT_RESULT_REVIEW_READINESS_V1.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_COMPLETION_HANDOFF_V1.md")


def test_phase8_panel_ui_contract_default_decision():
    decision = build_phase8_read_only_advisory_panel_ui_contract()
    assert decision.feature_id == "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_v1"
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelContractStatus.ACCEPTED_CONTRACT_ONLY
    assert decision.panel_contract_only is True
    assert decision.runtime_panel_activation_enabled is False
    assert decision.runtime_ui_mutation_enabled is False
    assert decision.runtime_telemetry_surface_wiring_enabled is False
    assert decision.route_authority_enabled is False
    assert decision.route_influence_enabled is False
    assert decision.router_calls_enabled is False
    assert decision.advisor_calls_enabled is False
    assert decision.adapter_execution_enabled is False
    assert decision.provider_calls_enabled is False
    assert decision.persistence_enabled is False
    assert decision.final_router_remains_authoritative is True
    assert decision.canonical_route_unchanged_label_required is True
    assert decision.advisory_role_label_required is True
    assert decision.non_training_feedback_slot_required is True
    assert "canonical_route_unchanged_label" in decision.allowed_sections
    assert "route_override_button" in decision.forbidden_capabilities


def test_phase8_panel_ui_contract_blocks_unsafe_capabilities():
    checks = [
        ("runtime_ui_mutation", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_UI_MUTATION),
        ("runtime_panel_activation", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_UI_MUTATION),
        ("runtime_telemetry_surface_wiring", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_UI_MUTATION),
        ("route_authority", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("route_influence", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("router_call", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE),
        ("advisor_call", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE),
        ("adapter_execution", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE),
        ("provider_call", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE),
        ("persistence", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE),
        ("free_text_route_advice", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_TEXT_OR_RANKING),
        ("free_text_explanations", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_TEXT_OR_RANKING),
        ("advisory_rankings", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_TEXT_OR_RANKING),
        ("route_override", ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_AUTHORITY),
    ]
    for capability, expected_status in checks:
        decision = evaluate_phase8_read_only_advisory_panel_ui_request(
            policy=ReadOnlyAdvisoryPanelUIContractPolicy(),
            requested_capabilities={capability: True},
        )
        assert decision.accepted is False
        assert decision.status is expected_status
        assert decision.route_authority_enabled is False
        assert decision.runtime_panel_activation_enabled is False


def test_phase8_panel_ui_docs_and_boundary():
    text = DOC.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_v1" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Completion Handoff v1" in text
    assert "UI contract" in text
    assert "does not render a panel" in text
    assert "does not activate" in text
    assert "canonical route unchanged label" in text
    assert "advisory data is telemetry only" in text
    assert "governed router remains the final selector" in text
    assert "route override button" in text
    assert "free-text route advice" in text
    assert "runtime UI mutation" in text
    assert "route authority" in text
    assert "not the visible panel implementation" in boundary
    assert "must not perform direct reads" in boundary
    assert "no runtime panel activation" in readiness
    assert PREV.exists()


def test_phase8_allowed_and_forbidden_constant_sets():
    assert "advisory_role_label" in ALLOWED_PANEL_SECTIONS
    assert "canonical_route_unchanged_label" in ALLOWED_PANEL_SECTIONS
    assert "non_training_feedback_slot" in ALLOWED_PANEL_SECTIONS
    assert "route_override_button" in FORBIDDEN_PANEL_CAPABILITIES
    assert "use_ml_route_button" in FORBIDDEN_PANEL_CAPABILITIES
    assert "prompt_ranking" in FORBIDDEN_PANEL_CAPABILITIES
    assert "router_call" in FORBIDDEN_PANEL_CAPABILITIES
    assert "runtime_panel_activation" in FORBIDDEN_PANEL_CAPABILITIES


if __name__ == "__main__":
    test_phase8_panel_ui_contract_default_decision()
    test_phase8_panel_ui_contract_blocks_unsafe_capabilities()
    test_phase8_panel_ui_docs_and_boundary()
    test_phase8_allowed_and_forbidden_constant_sets()
    print("VALIDATION OK: phase8 read-only advisory panel UI contract")
