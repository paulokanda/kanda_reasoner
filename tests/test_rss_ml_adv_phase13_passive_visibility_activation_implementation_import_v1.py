import inspect

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import _passive_visibility_activation_invariants as invariants
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import _passive_visibility_activation_models as models
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import read_only_advisory_panel_passive_visibility_activation as module
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_passive_visibility_activation import (
    build_phase13_read_only_panel_passive_visibility_activation_implementation_probe,
)


def test_phase13_passive_visibility_activation_implementation_import_boundary_has_no_forbidden_dependencies():
    source = inspect.getsource(module).lower()
    forbidden_fragments = (
        "requests",
        "urllib",
        "socket",
        "subprocess",
        "openai",
        "chromadb",
        "faiss",
        "sqlite3",
        "pickle",
        "pathlib",
        "open(",
        "actual_passive_visibility_activation_enabled = true",
        "passive_visibility_slot_registration_enabled = true",
        "passive_visibility_slot_mutation_enabled = true",
        "host_event_subscription_enabled = true",
        "host_callback_registration_enabled = true",
        "runtime_ui_mutation_enabled = true",
        "runtime_telemetry_surface_wiring_enabled = true",
    )
    sources = (
        source,
        inspect.getsource(invariants).lower(),
        inspect.getsource(models).lower(),
    )
    for checked_source in sources:
        for fragment in forbidden_fragments:
            assert fragment not in checked_source


def test_phase13_passive_visibility_activation_probe_is_pure_descriptor():
    descriptor = build_phase13_read_only_panel_passive_visibility_activation_implementation_probe()
    assert descriptor.read_only_passive_visibility_activation_descriptor_ready is True
    assert descriptor.passive_visibility_slot_descriptor_ready is True
    assert descriptor.actual_passive_visibility_activation_enabled is False
    assert descriptor.passive_visibility_slot_registration_enabled is False
    assert descriptor.passive_visibility_slot_mutation_enabled is False
    assert descriptor.actual_runtime_app_host_visibility_enabled is False
    assert descriptor.visibility_activation_enabled is False
    assert descriptor.runtime_ui_mutation_enabled is False
    assert descriptor.runtime_telemetry_surface_wiring_enabled is False
    assert descriptor.host_event_subscription_enabled is False
    assert descriptor.host_callback_registration_enabled is False
    assert descriptor.route_authority_enabled is False
    assert descriptor.runtime_copilot_decision_behavior_enabled is False
    assert descriptor.autonomous_ml_router_enabled is False
    assert descriptor.visible_ml_integration_complete is False


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_implementation_import_boundary_has_no_forbidden_dependencies()
    test_phase13_passive_visibility_activation_probe_is_pure_descriptor()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation implementation import boundary")
