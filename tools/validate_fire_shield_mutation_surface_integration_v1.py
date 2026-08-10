# project-path: tools/validate_fire_shield_mutation_surface_integration_v1.py
"""Validate Fire Shield coverage across governed Project source mutation owners."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

FEATURE_ID = "kanda-reasoner-fire-shield-cross-project-immutability-v1"

CORE_OWNERS = (
    "kanda_reasoner_app/_project_fire_shield_types.py",
    "kanda_reasoner_app/_project_fire_shield_provenance.py",
    "kanda_reasoner_app/project_fire_shield.py",
    "kanda_reasoner_app/project_fire_shield_cli.py",
    "kanda_reasoner_app/archive_safety.py",
)

MUTATION_OWNERS = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py",
    "kanda_reasoner_app/source_hygiene/bom_fixer.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_apply.py",
    "kanda_reasoner_app/source_hygiene/shadow_fixer.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/batch_apply.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_apply.py",
    "kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/guarded_source_apply_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_source_mutation_primitives.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_rollback_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_rollback_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_rollback_recovery.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_transaction_rollback.py",
)


def gate(marker: str, condition: bool) -> None:
    """Print one stable PASS marker or fail closed."""
    if not condition:
        raise RuntimeError(marker + ": FAIL")
    print(marker + ": PASS")


def main() -> int:
    """Validate public Fire Shield integration and module-size constraints."""
    for relative in CORE_OWNERS:
        path = PROJECT_ROOT / relative
        text = path.read_text(encoding="utf-8")
        marker = relative.replace("/", "_").replace(".py", "").upper()
        gate("FIRE_SHIELD_CORE_ASCII_" + marker, all(ord(ch) < 128 for ch in text))
        gate("FIRE_SHIELD_CORE_MAX500_" + marker, len(text.splitlines()) <= 500)
    for relative in MUTATION_OWNERS:
        path = PROJECT_ROOT / relative
        text = path.read_text(encoding="utf-8")
        marker = relative.replace("/", "_").replace(".py", "").upper()
        gate("FIRE_SHIELD_MUTATION_OWNER_" + marker, "project_fire_shield" in text)
        gate("FIRE_SHIELD_MUTATION_OWNER_ASCII_" + marker, all(ord(ch) < 128 for ch in text))
        gate("FIRE_SHIELD_MUTATION_OWNER_MAX500_" + marker, len(text.splitlines()) <= 500)
    print("FIRE_SHIELD_GOVERNED_MUTATION_SURFACES_INTEGRATED: PASS")
    print("VALIDATION OK: " + FEATURE_ID + "-mutation-surface-integration")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
