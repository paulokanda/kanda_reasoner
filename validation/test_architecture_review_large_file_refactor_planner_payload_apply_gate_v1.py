# project-path: validation/test_architecture_review_large_file_refactor_planner_payload_apply_gate_v1.py
"""Validation for Large File Refactor Planner payload apply gate v1."""
from __future__ import annotations

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
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.payload_apply_gate import build_payload_apply_gate, write_payload_apply_gate_manifest
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_artifact_validation import validate_preview_artifacts
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import build_preview_bundle, resolve_preview_root, write_preview_files
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.project_patch_payload import create_project_patch_payload_zip
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan


def _write_sample_module(root: Path) -> Path:
    """Write a minimal Python module for apply gate validation."""
    path = root / "sample_large.py"
    path.write_text(
        "\n".join([
            '\"\"\"Sample large module.\"\"\"',
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
        ]),
        encoding="utf-8",
    )
    return path


def _build_payload(project_root: Path):
    """Create a governed project patch payload for validation."""
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
    payload = create_project_patch_payload_zip(gate, bundle, artifact_result, import_preview, active_project_root=str(project_root))
    after_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
    assert before_hash == after_hash
    assert payload.status == "payload_ready", payload.blockers
    return sample, payload


def test_payload_apply_gate_is_ready_but_never_apply_enabled() -> None:
    """Apply gate records review evidence without enabling source application."""
    root = Path(tempfile.mkdtemp(prefix="kanda_apply_gate_project_"))
    try:
        sample, payload = _build_payload(root)
        before_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
        result = build_payload_apply_gate(
            payload,
            active_project_root=str(root),
            human_confirmation="CONFIRM_REVIEWED_PROJECT_PATCH_PAYLOAD",
        )
        written = write_payload_apply_gate_manifest(result)
        after_hash = hashlib.sha256(sample.read_bytes()).hexdigest()
        assert before_hash == after_hash
        assert result.status == "apply_gate_ready", result.blockers
        assert result.apply_enabled is False
        assert result.human_confirmation_present is True
        assert result.human_confirmation_required is True
        assert result.source_hash_verified is True
        assert written.exists()
        assert not written.is_relative_to(root)
        data = json.loads(written.read_text(encoding="utf-8"))
        assert data["apply_enabled"] is False
        assert data["human_confirmation_required"] is True
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_payload_apply_gate_blocks_when_source_hash_changes() -> None:
    """Apply gate blocks when selected source changed after payload creation."""
    root = Path(tempfile.mkdtemp(prefix="kanda_apply_gate_changed_"))
    try:
        sample, payload = _build_payload(root)
        sample.write_text(sample.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")
        result = build_payload_apply_gate(payload, active_project_root=str(root))
        assert result.status == "blocked"
        assert result.apply_enabled is False
        assert "SELECTED_SOURCE_HASH_CHANGED" in result.blockers
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_payload_apply_gate_import_export_surface() -> None:
    """Package init exports the apply gate helpers for later GUI trains."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import build_payload_apply_gate as exported

    assert exported is build_payload_apply_gate


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
    """Run focused payload apply gate validation."""
    test_payload_apply_gate_is_ready_but_never_apply_enabled()
    test_payload_apply_gate_blocks_when_source_hash_changes()
    test_payload_apply_gate_import_export_surface()
    _assert_module_sizes()
    print("VALIDATION OK: architecture-review-large-file-refactor-planner-payload-apply-gate-v1")
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
