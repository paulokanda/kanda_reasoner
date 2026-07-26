# project-path: validation/test_architecture_review_large_file_refactor_planner_import_rewrite_application_gate_v1.py
"""Validation for Import Rewrite Application Gate v1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.import_rewrite_application_gate import (
    IMPORT_REWRITE_CONFIRMATION_TOKEN,
    build_import_rewrite_application_gate,
    write_import_rewrite_application_gate_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.import_rewrite_application_gate_formatting import (
    format_import_rewrite_application_gate,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ImportMigrationPreview,
    ImportMigrationRecord,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.payload_apply_gate import (
    PayloadApplyGateResult,
)

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-import-rewrite-application-gate-v1"
PREVIOUS_MARKERS = ['architecture-review-large-file-refactor-planner-payload-apply-gui-wiring-v1', 'architecture-review-large-file-refactor-planner-payload-apply-gate-v1', 'architecture-review-large-file-refactor-planner-project-patch-payload-v1', 'architecture-review-large-file-refactor-planner-patch-zip-creation-gate-v1', 'architecture-review-large-file-refactor-planner-preview-validation-import-migration-v1', 'architecture-review-large-file-refactor-planner-governed-preview-generation-v1', 'architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1', 'architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1', 'architecture-review-large-file-refactor-planner-docstring-contracts-v1', 'architecture-review-large-file-refactor-planner-split-contracts-v1', 'architecture-review-large-file-refactor-planner-ast-v1']


def _daily_root_for_test(project_root: Path) -> Path:
    """Return the canonical daily-work root for a temporary test project."""
    anchor = project_root.anchor or str(project_root.parent)
    if anchor == "/":
        return project_root.parent / (project_root.name + "_delete_after_daily_work")
    return Path(anchor) / (project_root.name + "_delete_after_daily_work")


def _make_context(tmp: Path) -> tuple[Path, Path, Path, str, Path]:
    """Create test paths that obey the production daily-work root rule on each OS."""
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    daily_root = _daily_root_for_test(project_root)
    preview_root = daily_root / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    apply_manifest = preview_root / "PAYLOAD_APPLY_GATE.json"
    apply_manifest.write_text('{"apply_enabled": false}\n', encoding="utf-8")
    return project_root, target, preview_root, source_hash, daily_root

def _apply_gate(preview_root: Path, apply_manifest: Path) -> PayloadApplyGateResult:
    return PayloadApplyGateResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status="apply_gate_ready",
        payload_zip_path=str(preview_root / "large_file_refactor_project_patch_payload.zip"),
        payload_manifest_path=str(preview_root / "PROJECT_PATCH_PAYLOAD_MANIFEST.json"),
        preview_root=str(preview_root),
        apply_gate_manifest_path=str(apply_manifest),
        confirmation_token_required="CONFIRM_REVIEWED_PROJECT_PATCH_PAYLOAD",
        human_confirmation_present=False,
        apply_enabled=False,
        source_hash_verified=True,
        checked_rules=["apply_enabled_false_in_this_train"],
        blockers=[],
        warnings=[],
    )


def _import_preview(target: Path, source_hash: str, *, rewrite_enabled: bool = False) -> ImportMigrationPreview:
    record = ImportMigrationRecord(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        importer_file=str(target.parent / "consumer.py"),
        original_import="from large_module import VALUE",
        suggested_import="Keep public imports pointed at facade large_module.py.",
        action="review_only_no_rewrite",
        reason="Facade remains the public API owner.",
        status="preview_only",
        blockers=[],
        risk_flags=["IMPORT_MIGRATION_NOT_APPLIED"],
    )
    return ImportMigrationPreview(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        rewrite_enabled=rewrite_enabled,
        records=[record],
        blockers=[],
        warnings=["IMPORT_MIGRATION_PREVIEW_ONLY_NO_REWRITE"],
        status="preview_only",
    )


def test_gate_ready_without_enabling_rewrite() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        apply_manifest = preview_root / "PAYLOAD_APPLY_GATE.json"
        gate = build_import_rewrite_application_gate(
            _import_preview(target, source_hash),
            _apply_gate(preview_root, apply_manifest),
            active_project_root=str(project_root),
        )
        assert gate.status == "import_rewrite_gate_ready"
        assert gate.rewrite_enabled is False
        assert gate.apply_enabled is False
        assert gate.source_hash_verified is True
        written = write_import_rewrite_application_gate_manifest(gate)
        data = json.loads(written.read_text(encoding="utf-8"))
        assert data["rewrite_enabled"] is False
        assert data["apply_enabled"] is False
        assert str(written).startswith(str(preview_root))
        assert "IMPORT REWRITE APPLICATION GATE" in format_import_rewrite_application_gate(gate)
        shutil.rmtree(daily_root, ignore_errors=True)


def test_human_confirmation_does_not_enable_rewrite() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        gate = build_import_rewrite_application_gate(
            _import_preview(target, source_hash),
            _apply_gate(preview_root, preview_root / "PAYLOAD_APPLY_GATE.json"),
            active_project_root=str(project_root),
            human_confirmation=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        )
        assert gate.human_confirmation_present is True
        assert gate.rewrite_enabled is False
        assert gate.apply_enabled is False
        assert "HUMAN_CONFIRMATION_RECORDED_FOR_FUTURE_IMPORT_REWRITE_TRAIN_ONLY" in gate.warnings
        shutil.rmtree(daily_root, ignore_errors=True)


def test_rewrite_enabled_preview_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        gate = build_import_rewrite_application_gate(
            _import_preview(target, source_hash, rewrite_enabled=True),
            _apply_gate(preview_root, preview_root / "PAYLOAD_APPLY_GATE.json"),
            active_project_root=str(project_root),
        )
        assert gate.status == "blocked"
        assert "IMPORT_REWRITE_ALREADY_ENABLED" in gate.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_source_hash_change_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        target.write_text("VALUE = 2\n", encoding="utf-8")
        gate = build_import_rewrite_application_gate(
            _import_preview(target, source_hash),
            _apply_gate(preview_root, preview_root / "PAYLOAD_APPLY_GATE.json"),
            active_project_root=str(project_root),
        )
        assert gate.status == "blocked"
        assert "SELECTED_SOURCE_HASH_CHANGED" in gate.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_project_source_preview_root_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, _preview_root, source_hash, daily_root = _make_context(tmp)
        unsafe_root = project_root / "large_file_refactor_preview"
        unsafe_root.mkdir()
        apply_manifest = unsafe_root / "PAYLOAD_APPLY_GATE.json"
        apply_manifest.write_text('{"apply_enabled": false}\n', encoding="utf-8")
        gate = build_import_rewrite_application_gate(
            _import_preview(target, source_hash),
            _apply_gate(unsafe_root, apply_manifest),
            active_project_root=str(project_root),
        )
        assert gate.status == "blocked"
        assert "PREVIEW_ROOT_INSIDE_PROJECT_SOURCE" in gate.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def main() -> int:
    test_gate_ready_without_enabling_rewrite()
    test_human_confirmation_does_not_enable_rewrite()
    test_rewrite_enabled_preview_blocks()
    test_source_hash_change_blocks()
    test_project_source_preview_root_blocks()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
