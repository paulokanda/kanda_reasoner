from __future__ import annotations

import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from kanda_reasoner_app.freeze_after_update.send_pack_builder import generate_freeze_after_update_ai_files
from kanda_reasoner_app.generated_artifact_hygiene import (
    cleanup_project_generated_zip_noise,
    project_delete_after_daily_work_dir,
)
from kanda_reasoner_app.reasoner_context_bundle.source_archive_exporter import write_source_archive_parts


def _write_zip(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("payload.txt", "generated noise")


def _make_project_with_generated_zip_noise(base: Path) -> Path:
    root = base / "kanda_reasoner"
    root.mkdir()
    (root / "app.py").write_text("print('source')\n", encoding="utf-8")
    _write_zip(root / "kanda_prompt_workspace" / "first_AI_deliver" / "first_prompts_to_ai.zip")
    _write_zip(root / "kanda_prompt_workspace" / "first_AI_deliver" / "prompt_library.zip")
    _write_zip(root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS.zip")
    _write_zip(root / "kanda_prompt_workspace" / "prompt_library" / "prompt_library.zip")
    _write_zip(root / "kanda_prompt_workspace" / "prompt_audit_zips" / "prompt_audit_chunk.zip")
    _write_zip(root / "project_freeze_after_update" / "files_to_send_ai" / "freeze_feature_ai_send_pack_20260624_103319.zip")
    (root / "project_freeze_after_update" / "frozen_features_memory" / "entries").mkdir(parents=True)
    (root / "project_freeze_after_update" / "frozen_features_memory" / "entries" / "freeze-ok.md").write_text("# ok\n", encoding="utf-8")
    return root


def test_cleanup_deletes_known_generated_zip_noise_without_removing_source_memory() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="project_zip_noise_cleanup_"))
    try:
        root = _make_project_with_generated_zip_noise(workspace)
        result = cleanup_project_generated_zip_noise(root)
        assert result["ok"] is True
        removed = {item["path"] for item in result["removed"]}
        assert "kanda_prompt_workspace/first_AI_deliver" in removed
        assert "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS.zip" in removed
        assert "kanda_prompt_workspace/prompt_library/prompt_library.zip" in removed
        assert "kanda_prompt_workspace/prompt_audit_zips" in removed
        assert "project_freeze_after_update/files_to_send_ai" in removed

        assert not (root / "kanda_prompt_workspace" / "first_AI_deliver").exists()
        assert not (root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS.zip").exists()
        assert not (root / "kanda_prompt_workspace" / "prompt_library" / "prompt_library.zip").exists()
        assert not (root / "kanda_prompt_workspace" / "prompt_audit_zips").exists()
        assert not (root / "project_freeze_after_update" / "files_to_send_ai").exists()
        assert (root / "project_freeze_after_update" / "frozen_features_memory" / "entries" / "freeze-ok.md").is_file()
        assert "_delete_after_daily_work" in result["delete_after_daily_work_dir"]
        assert Path(result["delete_after_daily_work_dir"]).name == "kanda_reasoner_delete_after_daily_work"
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_source_archive_cleans_generated_zip_noise_instead_of_packaging_it() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="project_zip_noise_archive_"))
    try:
        root = _make_project_with_generated_zip_noise(workspace)
        destination = workspace / "kanda_reasoner_show_project_to_AI" / "second_prompt_files"
        temp_root = destination / "_tmp"
        destination.mkdir(parents=True)
        temp_root.mkdir(parents=True)

        result = write_source_archive_parts(root, destination, temp_root, part_size_mb=40, part_size_bytes=40 * 1024 * 1024)
        assert result["ok"] is True
        manifest = json.loads(Path(str(result["manifest_path"])).read_text(encoding="utf-8"))
        included_paths = {item["path"] for item in manifest["included_files"]}

        assert "app.py" in included_paths
        assert not any(path.endswith(".zip") for path in included_paths)
        assert not (root / "kanda_prompt_workspace" / "first_AI_deliver").exists()
        assert not (root / "kanda_prompt_workspace" / "prompt_audit_zips").exists()
        assert not (root / "project_freeze_after_update" / "files_to_send_ai").exists()
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_deprecated_ai_send_generation_no_longer_creates_project_local_files_to_send_ai() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="project_zip_noise_ai_send_"))
    try:
        root = _make_project_with_generated_zip_noise(workspace)
        result = generate_freeze_after_update_ai_files(root)
        assert result.ok is True
        assert result.output_zip is None
        assert result.output_instruction is None
        assert "Deprecated project-local files_to_send_ai ZIP generation skipped" in result.message
        assert not (root / "project_freeze_after_update" / "files_to_send_ai").exists()
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_prompt_audit_zip_destination_policy_is_outside_project_source() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="project_zip_noise_workdir_"))
    try:
        root = workspace / "kanda_reasoner"
        root.mkdir()
        work_dir = project_delete_after_daily_work_dir(root)
        assert work_dir.name == "kanda_reasoner_delete_after_daily_work"
        try:
            work_dir.resolve(strict=False).relative_to(root.resolve(strict=False))
            inside_project = True
        except ValueError:
            inside_project = False
        assert inside_project is False
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def main() -> int:
    test_cleanup_deletes_known_generated_zip_noise_without_removing_source_memory()
    test_source_archive_cleans_generated_zip_noise_instead_of_packaging_it()
    test_deprecated_ai_send_generation_no_longer_creates_project_local_files_to_send_ai()
    test_prompt_audit_zip_destination_policy_is_outside_project_source()
    print("VALIDATION OK: show_project_to_ai_project_zip_noise_cleanup_v1")
    print("VALIDATION OK: show project to AI project ZIP noise cleanup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
