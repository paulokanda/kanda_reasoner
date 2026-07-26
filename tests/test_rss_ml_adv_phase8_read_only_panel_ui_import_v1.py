from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    ReadOnlyAdvisoryPanelUIContractDecision,
    ReadOnlyAdvisoryPanelUIContractPolicy,
    ReadOnlyPanelContractStatus,
    ReadOnlyPanelVisibilityMode,
    build_phase8_read_only_advisory_panel_ui_contract,
    evaluate_phase8_read_only_advisory_panel_ui_request,
)


def test_phase8_panel_ui_import_boundary():
    decision = build_phase8_read_only_advisory_panel_ui_contract()
    assert isinstance(decision, ReadOnlyAdvisoryPanelUIContractDecision)
    assert isinstance(ReadOnlyAdvisoryPanelUIContractPolicy(), ReadOnlyAdvisoryPanelUIContractPolicy)
    assert decision.status is ReadOnlyPanelContractStatus.ACCEPTED_CONTRACT_ONLY
    assert decision.visibility_mode is ReadOnlyPanelVisibilityMode.CONTRACT_ONLY
    blocked = evaluate_phase8_read_only_advisory_panel_ui_request(
        policy=ReadOnlyAdvisoryPanelUIContractPolicy(),
        requested_capabilities={"route_authority": True},
    )
    assert blocked.accepted is False
    assert blocked.route_authority_enabled is False


if __name__ == "__main__":
    test_phase8_panel_ui_import_boundary()
    print("VALIDATION OK: phase8 read-only advisory panel UI import boundary")
