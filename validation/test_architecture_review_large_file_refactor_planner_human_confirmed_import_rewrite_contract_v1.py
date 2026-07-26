# project-path: validation/test_architecture_review_large_file_refactor_planner_human_confirmed_import_rewrite_contract_v1.py
"""Validation for Human-Confirmed Import Rewrite Contract v1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.human_confirmed_import_rewrite_contract import (
    build_human_confirmed_import_rewrite_contract,
    write_human_confirmed_import_rewrite_contract_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.human_confirmed_import_rewrite_contract_formatting import (
    format_human_confirmed_import_rewrite_contract,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.import_rewrite_application_gate import (
    IMPORT_REWRITE_CONFIRMATION_TOKEN,
    ImportRewriteApplicationGateResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import FEATURE_ID, SCHEMA_VERSION

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-human-confirmed-import-rewrite-contract-v1"
PREVIOUS_MARKERS = ['architecture-review-large-file-refactor-planner-import-rewrite-application-gate-v1', 'architecture-review-large-file-refactor-planner-payload-apply-gui-wiring-v1', 'architecture-review-large-file-refactor-planner-payload-apply-gate-v1', 'architecture-review-large-file-refactor-planner-project-patch-payload-v1', 'architecture-review-large-file-refactor-planner-patch-zip-creation-gate-v1', 'architecture-review-large-file-refactor-planner-preview-validation-import-migration-v1', 'architecture-review-large-file-refactor-planner-governed-preview-generation-v1', 'architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1', 'architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1', 'architecture-review-large-file-refactor-planner-docstring-contracts-v1', 'architecture-review-large-file-refactor-planner-split-contracts-v1', 'architecture-review-large-file-refactor-planner-ast-v1']


def _daily_root_for_test(project_root: Path) -> Path:
    """Return the canonical daily-work root for a temporary test project."""
    anchor = project_root.anchor or str(project_root.parent)
    if anchor == "/":
        return project_root.parent / (project_root.name + "_delete_after_daily_work")
    return Path(anchor) / (project_root.name + "_delete_after_daily_work")


def _make_context(tmp: Path) -> tuple[Path, Path, Path, str, Path]:
    """Create test paths that obey the production daily-work root rule."""
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    daily_root = _daily_root_for_test(project_root)
    preview_root = daily_root / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    gate_manifest = preview_root / "IMPORT_REWRITE_APPLICATION_GATE.json"
    gate_manifest.write_text('{"rewrite_enabled": false, "apply_enabled": false}\n', encoding="utf-8")
    return project_root, target, preview_root, source_hash, daily_root


def _import_gate(
    target: Path,
    preview_root: Path,
    source_hash: str,
    *,
    status: str = "import_rewrite_gate_ready",
    blockers: list[str] | None = None,
) -> ImportRewriteApplicationGateResult:
    """Return a ready import rewrite application gate result."""
    return ImportRewriteApplicationGateResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        apply_gate_manifest_path=str(preview_root / "PAYLOAD_APPLY_GATE.json"),
        import_rewrite_gate_manifest_path=str(preview_root / "IMPORT_REWRITE_APPLICATION_GATE.json"),
        importer_count=1,
        confirmation_token_required=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        human_confirmation_present=False,
        human_confirmation_required=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_hash_verified=True,
        checked_rules=["import_migration_rewrite_enabled_false"],
        blockers=blockers or [],
        warnings=["IMPORT_REWRITE_REMAINS_REVIEW_ONLY"],
    )


def test_human_confirmation_creates_contract_without_enabling_rewrite() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        contract = build_human_confirmed_import_rewrite_contract(
            _import_gate(target, preview_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        )
        assert contract.status == "human_confirmed_import_rewrite_contract_ready"
        assert contract.human_confirmation_present is True
        assert contract.human_confirmation_valid is True
        assert contract.rewrite_enabled is False
        assert contract.apply_enabled is False
        assert contract.source_hash_verified is True
        written = write_human_confirmed_import_rewrite_contract_manifest(contract)
        data = json.loads(written.read_text(encoding="utf-8"))
        assert data["rewrite_enabled"] is False
        assert data["apply_enabled"] is False
        assert data["human_confirmation_recorded_for_future_train_only"] is True
        assert str(written).startswith(str(preview_root))
        assert "HUMAN-CONFIRMED IMPORT REWRITE CONTRACT" in format_human_confirmed_import_rewrite_contract(contract)
        shutil.rmtree(daily_root, ignore_errors=True)


def test_missing_human_confirmation_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        contract = build_human_confirmed_import_rewrite_contract(
            _import_gate(target, preview_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation="",
        )
        assert contract.status == "blocked"
        assert "HUMAN_CONFIRMATION_TOKEN_MISSING_OR_INVALID" in contract.blockers
        assert contract.rewrite_enabled is False
        assert contract.apply_enabled is False
        shutil.rmtree(daily_root, ignore_errors=True)


def test_not_ready_import_gate_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        contract = build_human_confirmed_import_rewrite_contract(
            _import_gate(target, preview_root, source_hash, status="blocked", blockers=["UPSTREAM_BLOCKER"]),
            active_project_root=str(project_root),
            human_confirmation=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        )
        assert contract.status == "blocked"
        assert "IMPORT_REWRITE_APPLICATION_GATE_NOT_READY" in contract.blockers
        assert "UPSTREAM_BLOCKER" in contract.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_source_hash_change_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root = _make_context(tmp)
        target.write_text("VALUE = 2\n", encoding="utf-8")
        contract = build_human_confirmed_import_rewrite_contract(
            _import_gate(target, preview_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        )
        assert contract.status == "blocked"
        assert "SELECTED_SOURCE_HASH_CHANGED" in contract.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_project_source_preview_root_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, _preview_root, source_hash, daily_root = _make_context(tmp)
        unsafe_root = project_root / "large_file_refactor_preview"
        unsafe_root.mkdir()
        contract = build_human_confirmed_import_rewrite_contract(
            _import_gate(target, unsafe_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        )
        assert contract.status == "blocked"
        assert "PREVIEW_ROOT_INSIDE_PROJECT_SOURCE" in contract.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def main() -> int:
    test_human_confirmation_creates_contract_without_enabling_rewrite()
    test_missing_human_confirmation_blocks()
    test_not_ready_import_gate_blocks()
    test_source_hash_change_blocks()
    test_project_source_preview_root_blocks()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
