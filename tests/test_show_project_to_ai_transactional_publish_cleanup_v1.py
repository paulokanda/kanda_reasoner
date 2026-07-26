from __future__ import annotations

import json
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from kanda_reasoner_app import project_analysis_evidence_paths as paths
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext
from kanda_reasoner_app.reasoner_context_bundle.source_archive_exporter import gather_source_archive_inventory
from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_private_impl as impl


def test_ensure_dirs_does_not_create_legacy_or_building_folders() -> None:
    with TemporaryDirectory() as td:
        tmp = Path(td)
        project_root = tmp / "other_project"
        project_root.mkdir()
        show_root = tmp / "other_project_show_project_to_AI"
        original_root = paths.project_analysis_evidence_root
        try:
            paths.project_analysis_evidence_root = lambda _root: show_root  # type: ignore[assignment]
            paths.ensure_project_analysis_evidence_dirs(project_root)
        finally:
            paths.project_analysis_evidence_root = original_root  # type: ignore[assignment]

        assert (show_root / "first_prompt_files").is_dir()
        assert (show_root / "second_prompt_files").is_dir()
        assert not (show_root / "json_splitted").exists()
        assert not (show_root / "second_prompt_files_building").exists()


def test_publish_is_atomic_and_cleans_show_project_root() -> None:
    with TemporaryDirectory() as td:
        tmp = Path(td)
        project_root = tmp / "other_project"
        project_root.mkdir()
        show_root = tmp / "other_project_show_project_to_AI"
        first = show_root / "first_prompt_files"
        final = show_root / "second_prompt_files"
        build = show_root / "second_prompt_files_building"
        first.mkdir(parents=True)
        final.mkdir(parents=True)
        build.mkdir(parents=True)
        (final / "old_delivery.txt").write_text("old", encoding="utf-8")
        (build / "other_project__ai_briefing.json").write_text(json.dumps({"ok": True}), encoding="utf-8")
        (build / "other_project__source_archive_manifest.json").write_text(json.dumps({"ok": True}), encoding="utf-8")
        with zipfile.ZipFile(build / "other_project__source_archive_part01_of_01.zip", "w") as archive:
            archive.writestr("hello.txt", "hello")

        stale_split = show_root / "json_splitted"
        stale_split.mkdir(parents=True)
        (stale_split / "old.json").write_text("{}", encoding="utf-8")
        (show_root / "other_project__complete.json").write_text("{}", encoding="utf-8")
        (show_root / "other_project__source_archive_part01_of_01.zip").write_bytes(b"old")

        original_root = impl.project_analysis_evidence_root
        original_refresh = impl._refresh_bundle_manifest_after_publish_rewrite
        try:
            impl.project_analysis_evidence_root = lambda _root: show_root  # type: ignore[assignment]
            impl._refresh_bundle_manifest_after_publish_rewrite = lambda *_args, **_kwargs: None  # type: ignore[assignment]
            result = impl.publish_second_prompt_files_building_dir(build, final, project_root=project_root)
        finally:
            impl.project_analysis_evidence_root = original_root  # type: ignore[assignment]
            impl._refresh_bundle_manifest_after_publish_rewrite = original_refresh  # type: ignore[assignment]

        assert result["moved_items"] >= 3
        assert not build.exists()
        assert not stale_split.exists()
        assert not (show_root / "other_project__complete.json").exists()
        assert not (show_root / "other_project__source_archive_part01_of_01.zip").exists()
        assert not (final / "other_project__complete.json").exists()
        assert (final / "other_project__ai_briefing.json").is_file()
        assert (final / "other_project__source_archive_part01_of_01.zip").is_file()
        assert sorted(child.name for child in show_root.iterdir()) == ["first_prompt_files", "second_prompt_files"]


def test_source_archive_excludes_legacy_heavy_output_dirs() -> None:
    with TemporaryDirectory() as td:
        root = Path(td) / "other_project"
        out = Path(td) / "other_project_show_project_to_AI" / "second_prompt_files"
        root.mkdir()
        out.mkdir(parents=True)
        (root / "app.py").write_text("print('ok')\n", encoding="utf-8")
        for folder in (".project_reference", "workbench", "runtime_scenarios", "json_splitted"):
            d = root / folder
            d.mkdir()
            (d / "noise.txt").write_text("noise", encoding="utf-8")
        context = ProjectContext(root=root, project_slug="other_project", evidence_root=out.parent, json_complete_dir=out)
        inventory = gather_source_archive_inventory(context, out)
        included = {item["path"] for item in inventory["included_files"]}
        excluded = {item["path"]: item["reason_code"] for item in inventory["excluded_paths"]}

        assert "app.py" in included
        assert ".project_reference" in excluded
        assert "workbench" in excluded
        assert "runtime_scenarios" in excluded
        assert "json_splitted" in excluded
        assert excluded["json_splitted"] == "recursive_output_guard"


if __name__ == "__main__":
    test_ensure_dirs_does_not_create_legacy_or_building_folders()
    test_publish_is_atomic_and_cleans_show_project_root()
    test_source_archive_excludes_legacy_heavy_output_dirs()
    print("VALIDATION OK: show_project_to_ai_transactional_publish_cleanup_v1")
    print("VALIDATION OK: show project to AI transactional publish cleanup")
