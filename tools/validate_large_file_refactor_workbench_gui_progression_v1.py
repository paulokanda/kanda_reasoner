# project-path: tools/validate_large_file_refactor_workbench_gui_progression_v1.py
"""Validate sequential GUI progression from Real Preview through final authorization."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui_progression import (
    build_workbench_gui_progression,
    preview_validation_guidance,
)

FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-"
    "gui-sequential-progression-preview-to-final-v1"
)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
)


def run_validation() -> None:
    """Run pure progression, GUI wiring, messaging, and size-policy checks."""
    stages = _build_stage_objects()
    _validate_initial_and_intake(stages)
    _validate_preview_to_structural(stages)
    _validate_structural_to_payload(stages)
    _validate_completion_to_final(stages)
    _validate_blocked_preview_guidance(stages)
    _validate_gui_wiring_source()
    _validate_visible_sequence_source()
    _validate_tutorial_source()
    _validate_changed_python_sizes()
    print("GUI_PROGRESSION_SINGLE_SOURCE_OF_TRUTH: PASS")
    print("REAL_PREVIEW_ACTIVATES_STRUCTURAL_VALIDATION: PASS")
    print("BLOCKED_PREVIEW_EXPLAINS_STRUCTURAL_GATE: PASS")
    print("STRUCTURAL_TO_AQR_TO_PREFLIGHT_TO_PAYLOAD_CHAIN: PASS")
    print("PAYLOAD_ACTIVATES_COMPLETION_EVIDENCE: PASS")
    print("COMPLETION_REVIEW_TO_TRANSACTION_TO_FINAL_GATE: PASS")
    print("LEGACY_BEHAVIOR_PANEL_REMOVED: PASS")
    print("WORKBENCH_VISIBLE_SEQUENCE_1_TO_7: PASS")
    print("PATCH_CORRECTION_SOURCE_SIZE_POLICY_101_499: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")


def _build_stage_objects() -> dict[str, object]:
    gate = SimpleNamespace(enabled=True)
    return {
        "intake": SimpleNamespace(
            status="plan_intake_ready",
            ready_for_real_preview=True,
            source_hash_fresh=True,
        ),
        "dependency": SimpleNamespace(
            status="dependency_readiness_ready",
            ready_for_real_preview_writer=True,
        ),
        "preview": SimpleNamespace(
            status="real_preview_written",
            files=(SimpleNamespace(relative_path="helper.py"),),
            written_files=("preview/helper.py", "preview/REAL_PREVIEW_MANIFEST.json"),
            blockers=(),
        ),
        "structural": SimpleNamespace(
            status="passed_with_warnings",
            structural_status="STRUCTURAL_PASS_WITH_WARNINGS",
            blockers=(),
        ),
        "aqr": SimpleNamespace(
            cross_check_report=SimpleNamespace(quality_decision=SimpleNamespace(value="PASS")),
            run_record=SimpleNamespace(execution_status=SimpleNamespace(value="SUCCEEDED")),
        ),
        "preflight": SimpleNamespace(status="preflight_backup_ready"),
        "payload": SimpleNamespace(status="source_apply_payload_ready"),
        "evidence": SimpleNamespace(shadow_validation=SimpleNamespace(status="SHADOW_VALIDATED")),
        "transaction": SimpleNamespace(gate=gate),
        "outcome": SimpleNamespace(final_transaction_state="COMPLETED_VALIDATED"),
    }


def _progress(stages: dict[str, object], *names: str):
    values = {name: stages[name] for name in names}
    return build_workbench_gui_progression(
        intake=values.get("intake"),
        dependency_readiness=values.get("dependency"),
        preview=values.get("preview"),
        structural_validation=values.get("structural"),
        advanced_quality_review=values.get("aqr"),
        preflight=values.get("preflight"),
        source_payload=values.get("payload"),
        completion_evidence=values.get("evidence"),
        completion_transaction=values.get("transaction"),
        completion_outcome=values.get("outcome"),
    )


def _validate_initial_and_intake(stages: dict[str, object]) -> None:
    initial = _progress(stages)
    assert not initial.dependency_analysis_enabled
    assert initial.current_stage == "PLAN_INTAKE"
    intake = _progress(stages, "intake")
    assert intake.dependency_analysis_enabled
    assert not intake.real_preview_enabled
    assert intake.next_action == "Analyze Dependency Readiness"
    dependency = _progress(stages, "intake", "dependency")
    assert dependency.real_preview_enabled
    assert not dependency.structural_validation_enabled


def _validate_preview_to_structural(stages: dict[str, object]) -> None:
    state = _progress(stages, "intake", "dependency", "preview")
    assert state.real_preview_ready
    assert state.structural_validation_enabled
    assert state.current_stage == "STRUCTURAL_VALIDATION"
    assert state.next_action == "Validate Real Preview"
    guidance = preview_validation_guidance(stages["preview"])
    assert "Click Validate Real Preview" in guidance


def _validate_structural_to_payload(stages: dict[str, object]) -> None:
    structural = _progress(stages, "intake", "dependency", "preview", "structural")
    assert structural.advanced_quality_review_enabled
    assert not structural.preflight_enabled
    aqr = _progress(stages, "intake", "dependency", "preview", "structural", "aqr")
    assert aqr.advanced_quality_review_ready
    assert aqr.preflight_enabled
    preflight = _progress(
        stages, "intake", "dependency", "preview", "structural", "aqr", "preflight"
    )
    assert preflight.source_payload_enabled
    assert not preflight.completion_evidence_enabled
    payload = _progress(
        stages,
        "intake",
        "dependency",
        "preview",
        "structural",
        "aqr",
        "preflight",
        "payload",
    )
    assert payload.completion_evidence_enabled
    assert payload.current_stage == "COMPLETION_EVIDENCE"


def _validate_completion_to_final(stages: dict[str, object]) -> None:
    names = ("intake", "dependency", "preview", "structural", "aqr", "preflight", "payload")
    evidence = _progress(stages, *names, "evidence")
    assert evidence.transaction_summary_enabled
    assert evidence.human_review_enabled
    assert not evidence.transaction_confirmation_enabled
    transaction = _progress(stages, *names, "evidence", "transaction")
    assert transaction.transaction_confirmation_enabled
    assert transaction.refactor_large_module_enabled
    assert transaction.current_stage == "READY_TO_REFACTOR"


def _validate_blocked_preview_guidance(stages: dict[str, object]) -> None:
    blocked = SimpleNamespace(
        status="blocked",
        files=(),
        written_files=(),
        blockers=("STALE_SOURCE", "DESTINATION_COLLISION:helper.py"),
    )
    state = build_workbench_gui_progression(
        intake=stages["intake"],
        dependency_readiness=stages["dependency"],
        preview=blocked,
    )
    assert not state.structural_validation_enabled
    guidance = preview_validation_guidance(blocked)
    assert "STALE_SOURCE" in guidance
    assert "DESTINATION_COLLISION:helper.py" in guidance
    assert "run Generate Real Preview again" in guidance


def _validate_gui_wiring_source() -> None:
    source = (PACKAGE / "workbench_gui.py").read_text(encoding="utf-8")
    adapters = (PACKAGE / "main_workbench_stage_adapters.py").read_text(
        encoding="utf-8"
    )
    required = (
        "build_workbench_gui_progression(",
        '"_large_file_refactor_workbench_validate_button", progression.structural_validation_enabled',
        '"_large_file_refactor_workbench_preflight_button", progression.preflight_enabled',
        '"_large_file_refactor_workbench_source_payload_button", progression.source_payload_enabled',
        '"_large_file_refactor_workbench_completion_prepare_button", progression.completion_evidence_enabled',
    )
    for marker in required:
        assert marker in source, marker
    assert "preview_validation_guidance(result)" in adapters
    assert "build_behavior_validation_section" not in source
    assert "sync_behavior_validation_buttons" not in source


def _validate_visible_sequence_source() -> None:
    gui = (PACKAGE / "workbench_gui.py").read_text(encoding="utf-8")
    completion = (PACKAGE / "workbench_completion_gui.py").read_text(encoding="utf-8")
    for marker in (
        'QGroupBox("1. Plan Intake from Large File Refactor Planner")',
        'QGroupBox("2. Dependency and Scope Readiness")',
        'QGroupBox("3. Real Moved-Code Preview Generation")',
        'QGroupBox("4. Structural Validation")',
        'QGroupBox("6. Preflight Backup and Source Payload")',
    ):
        assert marker in gui, marker
    assert 'QGroupBox("7. Completion Review and Refactor Authorization")' in completion
    aqr_gui = (PACKAGE / "advanced_quality_review_gui.py").read_text(encoding="utf-8")
    assert 'QGroupBox("5. Advanced Quality Review")' in aqr_gui
    assert "Legacy Compatibility \u2014 Optional Behavior Validation (Non-sequential)" not in gui
    assert 'prepare_btn.setEnabled(False)' in completion


def _validate_tutorial_source() -> None:
    tutorial = (PACKAGE / "LARGE_FILE_REFACTOR_WORKBENCH_TUTORIAL.md").read_text(
        encoding="utf-8"
    )
    assert "## Exact visible tab sequence" in tutorial
    assert "When Preview succeeds with status `real_preview_written`" in tutorial
    assert "legacy optional behavior-validation panel" not in tutorial.lower()
    assert "6. Completion Review and Refactor Authorization" in tutorial or "7. Completion Review and Refactor Authorization" in tutorial


def _validate_changed_python_sizes() -> None:
    paths = (
        PACKAGE / "workbench_gui_progression.py",
        PACKAGE / "workbench_gui.py",
        PACKAGE / "workbench_completion_gui.py",
        Path(__file__).resolve(),
    )
    for path in paths:
        lines = len(path.read_text(encoding="utf-8").splitlines())
        assert 100 < lines < 500, f"SIZE_POLICY:{path}:{lines}"


if __name__ == "__main__":
    run_validation()
