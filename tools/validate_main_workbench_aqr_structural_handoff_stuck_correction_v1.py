"""Validate the Workbench AQR structural-handoff stuck-state correction."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
from tempfile import TemporaryDirectory

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_aqr_retry import (
    AQR_RETRY_READY,
    AQR_RETRY_TIMEOUT,
    AQR_RETRY_WAIT,
    AqrStartSettlementGate,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_formatting import (
    format_preflight_gate_reason,
)
from kanda_reasoner_app.freeze_hint_intake import (
    load_latest_freeze_hint_record,
    merge_validation_evidence_into_latest_hint,
)
from kanda_reasoner_app.freeze_hint_intake.records import save_freeze_hint_record

FEATURE_ID = "main-workbench-aqr-structural-handoff-stuck-correction-v1"
PLANNER = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
)
TOUCHED_SOURCE = (
    PLANNER / "advanced_quality_review_gui.py",
    PLANNER / "main_workbench_aqr_retry.py",
    PLANNER / "main_workbench_pipeline.py",
    PLANNER / "main_workbench_stage_adapters.py",
    PLANNER / "workbench_preflight_backup_formatting.py",
    Path("kanda_reasoner_app/freeze_hint_intake/records.py"),
    Path("tools/validate_architecture_review_large_file_refactor_preflight_backup_readiness_v1.py"),
    Path("tools/validate_advanced_quality_review_gui_contract_v1.py"),
    Path("tools/validate_main_workbench_aqr_structural_handoff_stuck_correction_v1.py"),
)


def require(condition: bool, marker: str) -> None:
    """Fail closed with one deterministic marker."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _validate_source_contract(project_root: Path) -> None:
    """Validate compile, ASCII, line law, and exact integration contracts."""
    for relative in TOUCHED_SOURCE:
        path = project_root / relative
        require(path.is_file(), "TOUCHED_FILE_PRESENT:" + relative.as_posix())
        data = path.read_bytes()
        require(not data.startswith(b"\xef\xbb\xbf"), "UTF8_NO_BOM:" + relative.as_posix())
        require(all(value < 128 for value in data), "ASCII_SOURCE:" + relative.as_posix())
        text = data.decode("utf-8")
        compile(text, str(path), "exec")
        ast.parse(text, filename=str(path))
        require(
            len(text.splitlines()) <= 500,
            "MODULE_SIZE_MAX_500:" + relative.as_posix(),
        )

    gui = _read(project_root, PLANNER / "advanced_quality_review_gui.py")
    adapters = _read(project_root, PLANNER / "main_workbench_stage_adapters.py")
    pipeline = _read(project_root, PLANNER / "main_workbench_pipeline.py")
    formatter = _read(
        project_root,
        PLANNER / "workbench_preflight_backup_formatting.py",
    )
    freeze_records = _read(
        project_root,
        Path("kanda_reasoner_app/freeze_hint_intake/records.py"),
    )
    broad_validator = _read(
        project_root,
        Path("tools/validate_architecture_review_large_file_refactor_preflight_backup_readiness_v1.py"),
    )
    gui_validator = _read(
        project_root,
        Path("tools/validate_advanced_quality_review_gui_contract_v1.py"),
    )

    require(
        "def advanced_quality_review_runtime_running" in gui
        and "return _start_review(window)" in gui,
        "AQR_START_REPORTS_EXACT_FRESH_GENERATION_ACCEPTANCE",
    )
    require(
        "def _start_review(window: object) -> bool" in gui
        and "return False" in gui
        and "return True" in gui,
        "AQR_GUI_START_HAS_EXPLICIT_BOOLEAN_RESULT",
    )
    require(
        "def mark_advanced_quality_review_ready_for_run" in gui
        and "ADVANCED QUALITY REVIEW READY" in gui,
        "POST_STRUCTURAL_AQR_READY_STATE_VISIBLE",
    )
    require(
        "mark_advanced_quality_review_ready_for_run(window, status)" in adapters,
        "STRUCTURAL_PASS_PROJECTS_FRESH_AQR_HANDOFF",
    )
    require(
        'reason = "AQR_REQUIRED"' in formatter
        and 'reason = "PREFLIGHT_AVAILABLE"' not in formatter,
        "STRUCTURAL_PASS_DOES_NOT_FALSELY_AUTHORIZE_PREFLIGHT",
    )
    require(
        "AqrStartSettlementGate" in pipeline
        and "advanced_quality_review_runtime_running(self._window)" in pipeline
        and "AQR_PREVIOUS_GENERATION_SETTLEMENT_TIMEOUT" in pipeline,
        "MAIN_WORKBENCH_RETRIES_SETTLING_AQR_WITH_BOUNDED_TIMEOUT",
    )
    require(
        'assert "AQR_REQUIRED" in ready' in broad_validator
        and 'assert "PREFLIGHT_AVAILABLE" not in ready' in broad_validator,
        "PREVIOUS_PREFLIGHT_VALIDATOR_UPDATED_TO_CANONICAL_GATE",
    )
    require(
        'stage_adapters = (PACKAGE / "main_workbench_stage_adapters.py")' in gui_validator
        and 'mark_advanced_quality_review_ready_for_run(window, status)' in gui_validator,
        "AQR_GUI_VALIDATOR_FOLLOWS_CURRENT_STAGE_OWNER",
    )
    require(
        "cleaned_hint = dict(hint)" in freeze_records
        and "cleaned_hint.update(" in freeze_records,
        "FREEZE_HINT_MERGE_PRESERVES_NON_FORM_METADATA",
    )


def _validate_preflight_gate() -> None:
    """Prove Structural Validation alone does not authorize Preflight."""
    text = format_preflight_gate_reason("passed_with_warnings")
    require("Reason: AQR_REQUIRED" in text, "AQR_REQUIRED_GATE_RENDERED")
    require("PREFLIGHT_AVAILABLE" not in text, "FALSE_PREFLIGHT_AVAILABLE_REMOVED")
    require(
        "Run Advanced Quality Review" in text,
        "AQR_NEXT_ACTION_RENDERED",
    )


def _validate_retry_gate() -> None:
    """Prove wait, fresh-start readiness, reset, and timeout behavior."""
    gate = AqrStartSettlementGate(max_polls=3)
    require(gate.observe(False) == AQR_RETRY_READY, "AQR_RETRY_IDLE_IS_READY")
    gate.begin()
    require(gate.observe(True) == AQR_RETRY_WAIT, "AQR_RETRY_FIRST_POLL_WAITS")
    require(gate.observe(False) == AQR_RETRY_READY, "AQR_RETRY_SETTLED_BECOMES_READY")
    require(not gate.pending and gate.polls == 0, "AQR_RETRY_READY_RESETS_STATE")

    gate.begin()
    require(gate.observe(True) == AQR_RETRY_WAIT, "AQR_RETRY_TIMEOUT_POLL_ONE_WAITS")
    require(gate.observe(True) == AQR_RETRY_WAIT, "AQR_RETRY_TIMEOUT_POLL_TWO_WAITS")
    require(gate.observe(True) == AQR_RETRY_TIMEOUT, "AQR_RETRY_TIMEOUT_IS_BOUNDED")
    require(not gate.pending and gate.polls == 0, "AQR_RETRY_TIMEOUT_RESETS_STATE")


def _validate_freeze_hint_identity_preservation() -> None:
    """Prove validation cleanup preserves feature identity and source metadata."""
    with TemporaryDirectory(prefix="kanda_freeze_hint_merge_") as temporary:
        project_root = Path(temporary) / "sample_project"
        project_root.mkdir()
        feature_id = FEATURE_ID
        hint = {
            "schema_version": "1.0",
            "kind": "kanda_freeze_hint",
            "patch_name": "fixture-patch",
            "source_patch_zip": "fixture-patch.zip",
            "feature_id": feature_id,
            "feature_title": "Fixture Feature",
            "primary_box": "fixture/box",
            "box_type": "fixture",
            "validated_files": ["fixture.py"],
            "generated_files": ["fixture_validator.py"],
            "protected_paths": ["fixture.py"],
            "do_not_regress_rules": ["Preserve feature identity."],
            "validation_evidence_summary": "Local validation remains required.",
            "known_warnings": "Fixture warning.",
            "planned_next_step": "Run local validation.",
            "notes": "Fixture metadata.",
        }
        save_freeze_hint_record(project_root, hint)
        marker = "VALIDATION OK: " + feature_id
        merged = merge_validation_evidence_into_latest_hint(
            project_root,
            marker + "\nSTATUS: IN_SYNC",
            feature_id=feature_id,
            feature_title="Fixture Feature",
        )
        require(bool(merged.get("ok")), "FREEZE_HINT_VALIDATION_EVIDENCE_MERGED")
        loaded = load_latest_freeze_hint_record(project_root)
        require(bool(loaded.get("ok")), "FREEZE_HINT_LATEST_RECORD_RELOADS")
        record = dict(loaded.get("record") or {})
        saved_hint = dict(record.get("hint") or {})
        require(
            saved_hint.get("feature_id") == feature_id,
            "FREEZE_HINT_FEATURE_ID_PRESERVED_AFTER_MERGE",
        )
        require(
            saved_hint.get("kind") == "kanda_freeze_hint"
            and saved_hint.get("source_patch_zip") == "fixture-patch.zip",
            "FREEZE_HINT_SOURCE_METADATA_PRESERVED_AFTER_MERGE",
        )
        require(
            marker in str(saved_hint.get("validation_evidence_summary") or ""),
            "FREEZE_HINT_LOCAL_MARKER_PRESERVED_AFTER_MERGE",
        )


def _read(project_root: Path, relative: Path) -> str:
    """Read one UTF-8 project source file."""
    return (project_root / relative).read_text(encoding="utf-8")


def main() -> int:
    """Run the focused correction validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve(strict=True)

    _validate_source_contract(project_root)
    _validate_preflight_gate()
    _validate_retry_gate()
    _validate_freeze_hint_identity_preservation()

    print("MAIN_WORKBENCH_AQR_STRUCTURAL_HANDOFF_STUCK_CORRECTION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
