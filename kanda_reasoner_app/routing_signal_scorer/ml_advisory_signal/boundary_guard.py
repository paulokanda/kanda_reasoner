# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/boundary_guard.py
"""Boundary guards for Phase 1a ML advisory signal scope."""

from __future__ import annotations

PHASE1A_ALLOWED_CAPABILITIES = frozenset(
    {
        "frozen_contracts",
        "advisor_protocol",
        "null_advisor",
        "deterministic_mock_advisor",
        "output_firewall",
        "boundary_docs",
        "in_memory_tests",
    }
)

PHASE1A_FORBIDDEN_CAPABILITIES = frozenset(
    {
        "real_ml_model",
        "runtime_shadow_mode",
        "provider_calls",
        "embeddings",
        "vector_store",
        "training",
        "calibration",
        "model_improvement",
        "prompt_loading",
        "freeze_memory_access",
        "router_canon_access",
        "prompt_library_access",
        "registry_mutation",
        "persistence",
        "report_persistence",
        "advisory_rankings",
        "free_text_explanations",
        "router_final_route_selection",
        "router_prompt_logic_modification",
    }
)


def assert_phase1a_environment_allowed(enabled_capabilities: set[str]) -> None:
    """Validate that an environment asks only for Phase 1a capabilities."""

    unexpected = set(enabled_capabilities) - PHASE1A_ALLOWED_CAPABILITIES
    forbidden = set(enabled_capabilities) & PHASE1A_FORBIDDEN_CAPABILITIES
    if unexpected or forbidden:
        details = sorted(unexpected | forbidden)
        raise ValueError("Phase 1a forbidden capabilities requested: " + ", ".join(details))
