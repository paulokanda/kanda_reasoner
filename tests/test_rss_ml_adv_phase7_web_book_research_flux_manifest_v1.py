import json
from pathlib import Path


FEATURE_ID = "rss_ml_adv_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1"
PREFIX = "ml_advisory_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1_"


def test_phase7_web_book_research_manifest_gates():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == FEATURE_ID
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase6_guarded_runtime_advisory_display_completion_handoff_v1"
    assert manifest[PREFIX + "web_research_integrated"] is True
    assert manifest[PREFIX + "book_research_integrated"] is True
    assert manifest[PREFIX + "web_source_count"] == 7
    assert manifest[PREFIX + "book_source_count"] == 5
    assert manifest[PREFIX + "real_gain_count"] == 14
    assert "AI Engineering: Building Applications with Foundation Models — Chip Huyen" in manifest[PREFIX + "book_sources_used"]
    assert "Human-Centered AI — Ben Shneiderman" in manifest[PREFIX + "book_sources_used"]
    assert "NIST AI Risk Management Framework and Generative AI Profile" in manifest[PREFIX + "web_sources_used"]
    assert "OWASP Top 10 for LLM and GenAI Applications" in manifest[PREFIX + "web_sources_used"]
    assert "direct_ml_route_override" in manifest[PREFIX + "rejected_or_deferred_from_audit"]
    assert manifest[PREFIX + "automatic_use_allowed_next"] == "only_after_canonical_router_final_selection_and_without_route_mutation"
    assert manifest[PREFIX + "visible_panel_allowed_next"] == "only_as_read_only_bounded_telemetry_with_uncertainty_scope_and_authority_disclaimer"
    assert manifest[PREFIX + "route_effect_allowed_next"] == "blocked_directly_only_deterministic_recheck_request_contract_may_be_studied_later"
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "runtime_advisory_panel_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wired"] is False
    assert manifest[PREFIX + "router_prompt_logic_modified"] is False
    assert manifest[PREFIX + "router_final_selection_modified"] is False
    assert manifest[PREFIX + "route_authority_enabled"] is False
    assert manifest[PREFIX + "provider_calls_enabled"] is False
    assert manifest[PREFIX + "persistence_enabled"] is False
    assert manifest[PREFIX + "free_text_explanations_enabled"] is False
    assert manifest[PREFIX + "mlrt_113_created"] is False
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0


if __name__ == "__main__":
    test_phase7_web_book_research_manifest_gates()
    print("VALIDATION OK: phase7 web-and-book-informed advisory surface wiring manifest gates")
