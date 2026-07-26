"""Private public-surface coverage for validation-only Brick Wall contract modules."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
for path in (str(ROOT), str(TOOLS)):
    if path not in sys.path:
        sys.path.insert(0, path)

import tools.brick_wall_q22_public_facade_contract as q22
import tools.brick_wall_q30_human_confirmation_freeze_protection_contract as q30
import tools.brick_wall_q31_changed_file_validator_coverage_contract as q31
import tools.brick_wall_q32_validation_evidence_provenance_contract as q32
import tools.brick_wall_q33_pinned_local_model_provenance_contract as q33
import tools.brick_wall_q34_profile_before_optimization_contract as q34
import tools.brick_wall_q35_focused_performance_baseline_contract as q35
import tools.brick_wall_q36_module_size_cohesion_contract as q36
import tools.brick_wall_q37_canonical_ownership_reconciliation_contract as q37
import tools.brick_wall_q38_handoff_freshness_provenance_contract as q38
import tools.brick_wall_q39_task_specific_context_admission_contract as q39
import tools.brick_wall_q40_one_primary_box_governed_release_contract as q40


VALIDATION_CONTRACTS = (q22, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40)


def test_brick_wall_q22_q40_contracts_do_not_claim_duplicate_public_symbols() -> None:
    """Keep shared fixture helper names out of project-wide public-symbol ownership."""

    for module in VALIDATION_CONTRACTS:
        assert module.__all__ == []
        assert hasattr(module, "validate_record")
        assert hasattr(module, "valid_not_applicable_record")
