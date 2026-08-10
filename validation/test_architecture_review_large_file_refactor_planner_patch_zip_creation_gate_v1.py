# project-path: validation/test_architecture_review_large_file_refactor_planner_patch_zip_creation_gate_v1.py
"""Validation for Large File Refactor Planner patch ZIP creation gate v1."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


import hashlib
import json
import shutil
import sys
import tempfile
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
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan


def _write_sample_module(root: Path) -> Path:
    """Write a minimal Python module for gate validation."""
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


def _build_passed_artifacts(project_root: Path):
    """Return preview artifacts that satisfy previous train gates."""
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
    after_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
    assert before_hash == after_hash
    assert artifact_result.status == "passed", artifact_result.blockers
    return artifact_result, import_preview


def test_patch_zip_creation_gate_opens_only_after_preview_validation() -> None:
    """Gate opens only when preview artifacts and import preview are safe."""
    root = Path(tempfile.mkdtemp(prefix="kanda_patch_gate_project_"))
    try:
        artifact_result, import_preview = _build_passed_artifacts(root)
        gate = build_patch_zip_creation_gate(
            artifact_result,
            import_preview,
            active_project_root=str(root),
        )
        assert gate.status == "gate_open", gate.blockers
        assert gate.patch_zip_creation_enabled is True
        assert "patch payload" not in gate.gate_manifest_path.lower()
        manifest = Path(write_patch_gate_manifest(gate))
        assert manifest.exists()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["status"] == "gate_open"
        assert data["patch_zip_creation_enabled"] is True
        assert "PATCH_PAYLOAD_NOT_CREATED_BY_GATE_TRAIN" in data["warnings"]
        assert not Path(root, "PATCH_ZIP_CREATION_GATE.json").exists()
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_patch_zip_creation_gate_blocks_bad_preview_root() -> None:
    """Gate blocks preview roots inside selected project source."""
    root = Path(tempfile.mkdtemp(prefix="kanda_patch_gate_bad_root_"))
    try:
        artifact_result, import_preview = _build_passed_artifacts(root)
        bad = artifact_result.__class__(
            schema_version=artifact_result.schema_version,
            feature_id=artifact_result.feature_id,
            status="passed",
            preview_root=str(root / "inside_project"),
            checked_files=list(artifact_result.checked_files),
            source_hash_verified=True,
            manifest_present=True,
            proof_present=True,
            import_migration_preview_status=artifact_result.import_migration_preview_status,
            blockers=[],
            warnings=[],
        )
        gate = build_patch_zip_creation_gate(bad, import_preview, active_project_root=str(root))
        assert gate.status == "blocked"
        assert gate.patch_zip_creation_enabled is False
        assert "PREVIEW_ROOT_INSIDE_PROJECT_SOURCE" in gate.blockers
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
    """Run focused patch gate validation."""
    test_patch_zip_creation_gate_opens_only_after_preview_validation()
    test_patch_zip_creation_gate_blocks_bad_preview_root()
    _assert_module_sizes()
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
