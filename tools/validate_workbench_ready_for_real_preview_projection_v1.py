# project-path: tools/validate_workbench_ready_for_real_preview_projection_v1.py
"""Validate canonical button projection for READY_FOR_REAL_PREVIEW."""
from __future__ import annotations

from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui_progression import (
    build_workbench_gui_progression,
)

FEATURE_ID = "workbench-patch5-executor-proof-status-projection-v1"


def main() -> int:
    intake = SimpleNamespace(
        status="plan_intake_ready",
        ready_for_real_preview=True,
        source_hash_fresh=True,
    )
    progression = build_workbench_gui_progression(intake=intake)

    assert progression.current_stage == "DEPENDENCY_READINESS"
    assert progression.next_action == "Analyze Dependency Readiness"
    assert progression.dependency_analysis_enabled
    print("READY_FOR_REAL_PREVIEW_DEPENDENCY_ACTION_ENABLED: PASS")

    downstream = (
        progression.real_preview_enabled,
        progression.structural_validation_enabled,
        progression.advanced_quality_review_enabled,
        progression.preflight_enabled,
        progression.source_payload_enabled,
        progression.completion_evidence_enabled,
        progression.transaction_summary_enabled,
        progression.transaction_confirmation_enabled,
        progression.refactor_large_module_enabled,
    )
    assert not any(downstream)
    print("READY_FOR_REAL_PREVIEW_DOWNSTREAM_STAGES_REMAIN_SEQUENTIAL: PASS")

    print("WORKBENCH_READY_FOR_REAL_PREVIEW_PROJECTION: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
