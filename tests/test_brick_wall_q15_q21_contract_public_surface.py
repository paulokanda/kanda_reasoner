"""Public-surface coverage for Brick Wall Q15-Q21 contract modules."""

from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(ROOT)
if ROOT_TEXT not in sys.path:
    sys.path.insert(0, ROOT_TEXT)

import tools.brick_wall_q15_path_authority_contract as q15
import tools.brick_wall_q16_resolved_path_containment_contract as q16
import tools.brick_wall_q17_preview_shadow_source_contract as q17
import tools.brick_wall_q18_stale_async_result_contract as q18
import tools.brick_wall_q19_real_qt_decision_contract as q19
import tools.brick_wall_q20_isolated_filesystem_fixture_contract as q20
import tools.brick_wall_q21_negative_boundary_matrix_contract as q21


CONTRACT_MODULES = (q15, q16, q17, q18, q19, q20, q21)


def test_brick_wall_q15_q21_contracts_declare_private_public_api() -> None:
    """Keep validation-only Brick Wall contracts reachable without duplicate exports."""

    for module in CONTRACT_MODULES:
        assert module.__all__ == []
        assert hasattr(module, "validate_record")
        assert hasattr(module, "valid_required_record")
        assert hasattr(module, "valid_not_applicable_record")


def test_brick_wall_q15_q21_exported_fixtures_validate() -> None:
    """Exercise the exported fixture/validator pair for each public contract."""

    for module in CONTRACT_MODULES:
        _validate_exported_records(module)


def _validate_exported_records(module: ModuleType) -> None:
    module.validate_record(module.valid_required_record())
    module.validate_record(module.valid_not_applicable_record())
