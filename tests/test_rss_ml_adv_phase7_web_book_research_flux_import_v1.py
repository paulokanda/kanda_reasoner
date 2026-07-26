def test_phase7_web_book_research_contract_import_boundary():
    import kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal as pkg

    contract = pkg.build_phase7_web_book_informed_surface_wiring_contract()
    assert contract.direct_route_authority_allowed is False
    assert contract.runtime_panel_wired is False
    assert contract.provider_calls_allowed is False
    assert contract.persistence_allowed is False
    assert contract.source_counts() == (7, 5)
    assert "modular_typed_interface_no_hidden_registry_or_global_state_coupling" in contract.gain_codes()

    decision = pkg.evaluate_phase7_web_book_advisory_surface_wiring_request(
        auto_use_after_router=False,
        visible_panel=False,
        affect_route_choice=False,
    )
    assert decision.required_next_contract == "no_runtime_wiring_requested"


if __name__ == "__main__":
    test_phase7_web_book_research_contract_import_boundary()
    print("VALIDATION OK: phase7 web-and-book-informed advisory surface wiring import boundary")
