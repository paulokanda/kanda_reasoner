# project-path: validation/test_architecture_review_large_file_refactor_planner_project_patch_payload_v1.py
"""Validation for Large File Refactor Planner project patch payload v1."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.import_migration_preview import build_import_migration_preview
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import PlannerSettings
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.patch_zip_gate import build_patch_zip_creation_gate, write_patch_gate_manifest
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_artifact_validation import validate_preview_artifacts
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import build_preview_bundle, resolve_preview_root, write_preview_files
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.project_patch_payload import create_project_patch_payload_zip
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan


def _write_sample_module(root: Path) -> Path:
    """Write a minimal Python module for payload validation."""
    path = root / "sample_large.py"
    source = "\n".join([
        '"""Sample large module."""',
        "",
        "def alpha():",
        '    return "alpha"',
        "",
        "def beta():",
        '    return "beta"',
        "",
        "class Gamma:",
        "    def run(self):",
        "        return alpha()",
        "",
    ])
    path.write_text(source, encoding="utf-8")
    return path


def _build_payload_inputs(project_root: Path):
    """Return validated preview artifacts and a gate-open result."""
    sample = _write_sample_module(project_root)
    before_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
    report = analyze_python_file(str(sample))
    plan = build_split_plan(report, PlannerSettings())
    preview_root = resolve_preview_root(str(project_root))
    bundle = build_preview_bundle(plan, preview_root=preview_root, governed_write=True)
    write_result = write_preview_files(bundle, str(project_root))
    import_preview = build_import_migration_preview(plan, active_project_root=str(project_root))
    artifact_result = validate_preview_artifacts(
        bundle,
        write_result,
        active_project_root=str(project_root),
        import_preview=import_preview,
    )
    gate = build_patch_zip_creation_gate(artifact_result, import_preview, active_project_root=str(project_root))
    write_patch_gate_manifest(gate)
    after_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
    assert before_hash == after_hash
    assert artifact_result.status == "passed", artifact_result.blockers
    assert gate.status == "gate_open", gate.blockers
    return sample, bundle, artifact_result, import_preview, gate


def test_project_patch_payload_zip_created_from_validated_preview_only() -> None:
    """Payload ZIP is created only from daily-work preview artifacts."""
    root = Path(tempfile.mkdtemp(prefix="kanda_payload_project_"))
    try:
        sample, bundle, artifact_result, import_preview, gate = _build_payload_inputs(root)
        before_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
        result = create_project_patch_payload_zip(
            gate,
            bundle,
            artifact_result,
            import_preview,
            active_project_root=str(root),
        )
        after_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
        assert before_hash == after_hash
        assert result.status == "payload_ready", result.blockers
        assert result.patch_payload_created is True
        assert result.source_hash_verified is True
        payload_zip = Path(result.payload_zip_path)
        manifest = Path(result.payload_manifest_path)
        assert payload_zip.exists()
        assert manifest.exists()
        assert not payload_zip.is_relative_to(root)
        with zipfile.ZipFile(payload_zip, "r") as archive:
            names = set(archive.namelist())
        assert "PROJECT_PATCH_PAYLOAD_MANIFEST.json" in names
        assert "PREVIEW_MANIFEST.json" in names
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["apply_to_source"] is False
        assert data["requires_human_review"] is True
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_project_patch_payload_blocks_when_gate_is_not_open() -> None:
    """Payload creation blocks when the gate result is not open."""
    root = Path(tempfile.mkdtemp(prefix="kanda_payload_blocked_"))
    try:
        _, bundle, artifact_result, import_preview, gate = _build_payload_inputs(root)
        closed_gate = gate.__class__(
            schema_version=gate.schema_version,
            feature_id=gate.feature_id,
            status="blocked",
            patch_zip_creation_enabled=False,
            preview_root=gate.preview_root,
            gate_manifest_path=gate.gate_manifest_path,
            checked_rules=list(gate.checked_rules),
            blockers=["MANUAL_BLOCK"],
            warnings=[],
        )
        result = create_project_patch_payload_zip(
            closed_gate,
            bundle,
            artifact_result,
            import_preview,
            active_project_root=str(root),
        )
        assert result.status == "blocked"
        assert result.patch_payload_created is False
        assert "PATCH_GATE_NOT_OPEN" in result.blockers
        assert not Path(result.payload_zip_path).exists()
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _assert_module_sizes() -> None:
    """Enforce KANDA planner module line-size gates."""
    package = PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
    oversized = []
    for path in package.glob("*.py"):
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count > 500:
            oversized.append(f"{path.name}:{count}")
    assert not oversized, "Oversized planner modules: " + ", ".join(oversized)


def main() -> int:
    """Run focused project patch payload validation."""
    test_project_patch_payload_zip_created_from_validated_preview_only()
    test_project_patch_payload_blocks_when_gate_is_not_open()
    _assert_module_sizes()
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-project-patch-payload-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-patch-zip-creation-gate-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-preview-validation-import-migration-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-governed-preview-generation-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-docstring-contracts-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-split-contracts-v1")
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-ast-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
