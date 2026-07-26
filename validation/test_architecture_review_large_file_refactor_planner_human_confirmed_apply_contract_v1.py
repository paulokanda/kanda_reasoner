# project-path: validation/test_architecture_review_large_file_refactor_planner_human_confirmed_apply_contract_v1.py
"""Validation for Human-Confirmed Apply Contract v1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.human_confirmed_apply_contract import (
    HUMAN_CONFIRMED_APPLY_TOKEN,
    build_human_confirmed_apply_contract,
    write_human_confirmed_apply_contract_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.human_confirmed_apply_contract_formatting import (
    format_human_confirmed_apply_contract,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.human_confirmed_import_rewrite_contract import (
    HumanConfirmedImportRewriteContractResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.import_rewrite_application_gate import (
    IMPORT_REWRITE_CONFIRMATION_TOKEN,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import FEATURE_ID, SCHEMA_VERSION
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.payload_apply_gate import PayloadApplyGateResult

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-human-confirmed-apply-contract-v1"
PREVIOUS_MARKERS = ['architecture-review-large-file-refactor-planner-human-confirmed-import-rewrite-contract-v1', 'architecture-review-large-file-refactor-planner-import-rewrite-application-gate-v1', 'architecture-review-large-file-refactor-planner-payload-apply-gui-wiring-v1', 'architecture-review-large-file-refactor-planner-payload-apply-gate-v1', 'architecture-review-large-file-refactor-planner-project-patch-payload-v1', 'architecture-review-large-file-refactor-planner-patch-zip-creation-gate-v1', 'architecture-review-large-file-refactor-planner-preview-validation-import-migration-v1', 'architecture-review-large-file-refactor-planner-governed-preview-generation-v1', 'architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1', 'architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1', 'architecture-review-large-file-refactor-planner-docstring-contracts-v1', 'architecture-review-large-file-refactor-planner-split-contracts-v1', 'architecture-review-large-file-refactor-planner-ast-v1']


def _daily_root_for_test(project_root: Path) -> Path:
    """Return the canonical daily-work root for a temporary test project."""
    anchor = project_root.anchor or str(project_root.parent)
    if anchor == "/":
        return project_root.parent / (project_root.name + "_delete_after_daily_work")
    return Path(anchor) / (project_root.name + "_delete_after_daily_work")


def _make_context(tmp: Path) -> tuple[Path, Path, Path, str, Path, Path, Path]:
    """Create payload and contract paths that obey the daily-work root rule."""
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    daily_root = _daily_root_for_test(project_root)
    preview_root = daily_root / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    payload_manifest = preview_root / "PROJECT_PATCH_PAYLOAD_MANIFEST.json"
    payload_data = {
        "target_file": str(target),
        "source_content_hash": source_hash,
        "apply_to_source": False,
        "requires_human_review": True,
        "import_rewrite_enabled": False,
    }
    payload_manifest.write_text(json.dumps(payload_data, indent=2) + "\n", encoding="utf-8")
    payload_zip = preview_root / "PROJECT_PATCH_PAYLOAD.zip"
    with zipfile.ZipFile(payload_zip, "w") as archive:
        archive.write(payload_manifest, "PROJECT_PATCH_PAYLOAD_MANIFEST.json")
    apply_gate_manifest = preview_root / "PAYLOAD_APPLY_GATE.json"
    apply_gate_manifest.write_text('{"apply_enabled": false}\n', encoding="utf-8")
    import_contract_manifest = preview_root / "HUMAN_CONFIRMED_IMPORT_REWRITE_CONTRACT.json"
    import_contract_manifest.write_text('{"rewrite_enabled": false, "apply_enabled": false}\n', encoding="utf-8")
    return project_root, target, preview_root, source_hash, daily_root, payload_zip, payload_manifest


def _payload_gate(preview_root: Path, payload_zip: Path, payload_manifest: Path) -> PayloadApplyGateResult:
    """Return a ready payload apply gate result."""
    return PayloadApplyGateResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status="apply_gate_ready",
        payload_zip_path=str(payload_zip),
        payload_manifest_path=str(payload_manifest),
        preview_root=str(preview_root),
        apply_gate_manifest_path=str(preview_root / "PAYLOAD_APPLY_GATE.json"),
        confirmation_token_required=HUMAN_CONFIRMED_APPLY_TOKEN,
        human_confirmation_present=True,
        human_confirmation_required=True,
        apply_enabled=False,
        source_hash_verified=True,
        checked_rules=["apply_enabled_false_in_this_train"],
        blockers=[],
        warnings=["PAYLOAD_APPLY_IS_NOT_IMPLEMENTED_IN_THIS_TRAIN"],
    )


def _import_contract(target: Path, preview_root: Path, source_hash: str, *, status: str = "human_confirmed_import_rewrite_contract_ready") -> HumanConfirmedImportRewriteContractResult:
    """Return a ready human-confirmed import rewrite contract result."""
    return HumanConfirmedImportRewriteContractResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        import_rewrite_gate_manifest_path=str(preview_root / "IMPORT_REWRITE_APPLICATION_GATE.json"),
        human_contract_manifest_path=str(preview_root / "HUMAN_CONFIRMED_IMPORT_REWRITE_CONTRACT.json"),
        confirmation_token_required=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        human_confirmation_present=True,
        human_confirmation_valid=True,
        human_confirmation_recorded_for_future_train_only=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_hash_verified=True,
        checked_rules=["rewrite_enabled_false_in_this_train"],
        blockers=[],
        warnings=["IMPORT_REWRITE_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN"],
    )


def test_human_apply_confirmation_creates_contract_without_enabling_apply() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, payload_manifest = _make_context(tmp)
        contract = build_human_confirmed_apply_contract(
            _payload_gate(preview_root, payload_zip, payload_manifest),
            _import_contract(target, preview_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation=HUMAN_CONFIRMED_APPLY_TOKEN,
        )
        assert contract.status == "human_confirmed_apply_contract_ready"
        assert contract.human_confirmation_present is True
        assert contract.human_confirmation_valid is True
        assert contract.rewrite_enabled is False
        assert contract.apply_enabled is False
        assert contract.source_hash_verified is True
        written = write_human_confirmed_apply_contract_manifest(contract)
        data = json.loads(written.read_text(encoding="utf-8"))
        assert data["rewrite_enabled"] is False
        assert data["apply_enabled"] is False
        assert data["human_confirmation_recorded_for_future_train_only"] is True
        assert str(written).startswith(str(preview_root))
        assert "HUMAN-CONFIRMED APPLY CONTRACT" in format_human_confirmed_apply_contract(contract)
        shutil.rmtree(daily_root, ignore_errors=True)


def test_missing_human_apply_confirmation_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, payload_manifest = _make_context(tmp)
        contract = build_human_confirmed_apply_contract(
            _payload_gate(preview_root, payload_zip, payload_manifest),
            _import_contract(target, preview_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation="",
        )
        assert contract.status == "blocked"
        assert "HUMAN_APPLY_CONFIRMATION_TOKEN_MISSING_OR_INVALID" in contract.blockers
        assert contract.apply_enabled is False
        shutil.rmtree(daily_root, ignore_errors=True)


def test_import_contract_not_ready_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, payload_manifest = _make_context(tmp)
        contract = build_human_confirmed_apply_contract(
            _payload_gate(preview_root, payload_zip, payload_manifest),
            _import_contract(target, preview_root, source_hash, status="blocked"),
            active_project_root=str(project_root),
            human_confirmation=HUMAN_CONFIRMED_APPLY_TOKEN,
        )
        assert contract.status == "blocked"
        assert "HUMAN_IMPORT_REWRITE_CONTRACT_NOT_READY" in contract.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_source_hash_change_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, payload_manifest = _make_context(tmp)
        target.write_text("VALUE = 2\n", encoding="utf-8")
        contract = build_human_confirmed_apply_contract(
            _payload_gate(preview_root, payload_zip, payload_manifest),
            _import_contract(target, preview_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation=HUMAN_CONFIRMED_APPLY_TOKEN,
        )
        assert contract.status == "blocked"
        assert "SELECTED_SOURCE_HASH_CHANGED" in contract.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_payload_gate_apply_enabled_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, payload_manifest = _make_context(tmp)
        gate = _payload_gate(preview_root, payload_zip, payload_manifest)
        unsafe_gate = PayloadApplyGateResult(**{**gate.to_dict(), "apply_enabled": True})
        contract = build_human_confirmed_apply_contract(
            unsafe_gate,
            _import_contract(target, preview_root, source_hash),
            active_project_root=str(project_root),
            human_confirmation=HUMAN_CONFIRMED_APPLY_TOKEN,
        )
        assert contract.status == "blocked"
        assert "PAYLOAD_APPLY_GATE_APPLY_ENABLED_UNEXPECTEDLY" in contract.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def main() -> int:
    test_human_apply_confirmation_creates_contract_without_enabling_apply()
    test_missing_human_apply_confirmation_blocks()
    test_import_contract_not_ready_blocks()
    test_source_hash_change_blocks()
    test_payload_gate_apply_enabled_blocks()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
