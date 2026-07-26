"""Reachability coverage for validation-only Brick Wall Q23-Q29 and Q37-Q40 modules."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
for path in (str(ROOT), str(TOOLS)):
    if path not in sys.path:
        sys.path.insert(0, path)

import tools.brick_wall_q23_mcard_transition_contract as q23
import tools.brick_wall_q24_property_based_mcard_pilot_contract as q24
import tools.brick_wall_q25_mutation_testing_pilot_contract as q25
import tools.brick_wall_q26_zip_containment_collision_contract as q26
import tools.brick_wall_q27_control_byte_encoding_contract as q27
import tools.brick_wall_q28_structured_exception_provenance_contract as q28
import tools.brick_wall_q29_no_leak_runtime_trace_pilot_contract as q29_contract
import tools.brick_wall_q29_runtime_trace_probe as q29_probe
import tools.brick_wall_q37_delivery_provenance as q37_provenance
import tools.brick_wall_q38_delivery_provenance as q38_provenance
import tools.brick_wall_q39_delivery_provenance as q39_provenance
import tools.brick_wall_q40_delivery_provenance as q40_provenance


VALIDATION_ONLY_MODULES = (
    q23,
    q24,
    q25,
    q26,
    q27,
    q28,
    q29_contract,
    q29_probe,
    q37_provenance,
    q38_provenance,
    q39_provenance,
    q40_provenance,
)


def test_brick_wall_q23_q40_validation_only_modules_are_reachable() -> None:
    """Keep validation-only modules in the scanned project graph."""

    for module in VALIDATION_ONLY_MODULES:
        assert module.__all__ == []
        assert module.__name__


def test_brick_wall_q23_q29_contracts_expose_internal_validators() -> None:
    """Document validation-only contract internals without promoting public exports."""

    for module in (q23, q24, q25, q26, q27, q28, q29_contract):
        assert hasattr(module, "validate_record")
        assert hasattr(module, "valid_not_applicable_record")

    assert hasattr(q29_probe, "main")


def test_brick_wall_q37_q40_provenance_helpers_are_importable() -> None:
    """Document delivery provenance helpers as validation-only implementation details."""

    for module in (q37_provenance, q38_provenance, q39_provenance, q40_provenance):
        assert hasattr(module, "build_provenance_payload")
        assert hasattr(module, "write_durable_evidence")
