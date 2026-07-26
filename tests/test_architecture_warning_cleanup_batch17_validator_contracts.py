"""Smoke coverage for Batch 15 and Batch 16 validator public contracts."""

from __future__ import annotations

import scripts.validate_architecture_warning_cleanup_batch15_remaining_side_effects_v1 as batch15_validator
import scripts.validate_architecture_warning_cleanup_batch16_test_protection_smoke_v1 as batch16_validator


_VALIDATOR_MODULES = (
    batch15_validator,
    batch16_validator,
)


def test_batch17_previous_cleanup_validators_expose_main_only() -> None:
    """Verify previous cleanup validators keep narrow public entry points."""

    for module in _VALIDATOR_MODULES:
        assert module.__all__ == ["main"]
        assert callable(module.main)
