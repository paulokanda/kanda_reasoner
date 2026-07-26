from __future__ import annotations

import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import (  # noqa: E402
    generate_ai_context_bundle,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (  # noqa: E402
    export_json_handoff_zip_parts,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter_support import (  # noqa: E402
    external_readme_text,
)
from kanda_reasoner_app.reasoner_context_bundle.source_archive_exporter import (  # noqa: E402
    write_source_archive_parts,
)


def _make_project(root: Path) -> None:
    (root / "app").mkdir(parents=True)
    (root / "assets" / "nested").mkdir(parents=True)
    (root / "app" / "main.py").write_text("print('hello')\n", encoding="utf-8")
    (root / "assets" / "icon.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"a" * 128)
    (root / "assets" / "nested" / "diagram.PNG").write_bytes(b"\x89PNG\r\n\x1a\n" + b"b" * 256)
    (root / "assets" / "note.txt").write_text("keep with source archive\n", encoding="utf-8")


def test_png_assets_are_exported_as_separate_stored_zip_family() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="png_asset_split_"))
    try:
        project_root = workspace / "demo_project"
        _make_project(project_root)
        destination = workspace / "demo_project_show_project_to_AI" / "second_prompt_files"
        temp_root = workspace / "zip_temp"
        destination.mkdir(parents=True)
        temp_root.mkdir(parents=True)

        result = write_source_archive_parts(
            project_root,
            destination,
            temp_root,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
        )

        assert result["ok"] is True, result
        assert len(result["source_zip_parts"]) == 1
        assert len(result["png_asset_zip_parts"]) == 1
        assert len(result["zip_parts"]) == 2

        source_zip = destination / result["source_zip_parts"][0]["filename"]
        png_zip = destination / result["png_asset_zip_parts"][0]["filename"]
        assert source_zip.name == "demo_project__source_archive_part01_of_01.zip"
        assert png_zip.name == "demo_project__png_assets_part01_of_01.zip"

        with zipfile.ZipFile(source_zip, "r") as archive:
            source_names = set(archive.namelist())
            assert "app/main.py" in source_names
            assert "assets/note.txt" in source_names
            assert "assets/icon.png" not in source_names
            assert "assets/nested/diagram.PNG" not in source_names
            assert all(info.compress_type == zipfile.ZIP_DEFLATED for info in archive.infolist())

        with zipfile.ZipFile(png_zip, "r") as archive:
            png_names = set(archive.namelist())
            assert png_names == {"assets/icon.png", "assets/nested/diagram.PNG"}
            assert all(info.compress_type == zipfile.ZIP_STORED for info in archive.infolist())

        manifest = json.loads(Path(str(result["manifest_path"])).read_text(encoding="utf-8"))
        assert manifest["png_asset_archive_contract"]["enabled"] is True
        assert manifest["png_asset_archive_contract"]["compression_method"] == "ZIP_STORED"
        assert manifest["counts"]["png_asset_files"] == 2
        assert manifest["counts"]["png_asset_archive_parts"] == 1
        assert manifest["parts"][0]["archive_family"] == "source_archive"
        assert manifest["png_asset_parts"][0]["archive_family"] == "png_assets"

        by_path = {item["path"]: item for item in manifest["included_files"]}
        assert by_path["app/main.py"]["archive_family"] == "source_archive"
        assert by_path["assets/icon.png"]["archive_family"] == "png_assets"
        assert by_path["assets/nested/diagram.PNG"]["archive_family"] == "png_assets"
        assert by_path["assets/icon.png"]["part_filename"] == png_zip.name
    finally:
        shutil.rmtree(workspace, ignore_errors=True)



def test_second_prompt_export_creates_png_asset_package_automatically() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="png_asset_export_"))
    try:
        project_root = workspace / "demo_project"
        _make_project(project_root)
        bundle = generate_ai_context_bundle(
            project_root,
            command_results={
                "architecture_validate": {
                    "ran": True,
                    "exit_code": 0,
                    "status": "pass",
                    "summary": "Architecture validation passed.",
                }
            },
            commands_run_by_bundle=True,
        )
        assert bundle["ok"] is True, bundle

        destination = workspace / "demo_project_show_project_to_AI" / "second_prompt_files"
        destination.mkdir(parents=True)
        result = export_json_handoff_zip_parts(
            project_root,
            destination,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
        )

        assert result["ok"] is True, result
        package_names = {item["name"] for item in result["packages"]}
        assert "source_archive" in package_names
        assert "png_assets" in package_names
        assert any(item["package"] == "png_assets" for item in result["zip_parts"])
        assert (destination / "demo_project__png_assets_part01_of_01.zip").exists()
        assert (destination / "demo_project__ai_handoff_upload.zip").exists()

        with zipfile.ZipFile(destination / "demo_project__ai_handoff_upload.zip", "r") as archive:
            names = archive.namelist()
        assert any(name.endswith("demo_project__source_archive_manifest.json") for name in names)
    finally:
        shutil.rmtree(workspace, ignore_errors=True)

def test_png_asset_readme_mentions_png_asset_parts() -> None:
    from kanda_reasoner_app.reasoner_context_bundle.project_context import resolve_project_context

    workspace = Path(tempfile.mkdtemp(prefix="png_asset_readme_"))
    try:
        project_root = workspace / "demo_project"
        project_root.mkdir(parents=True)
        context = resolve_project_context(project_root)
        text = external_readme_text(context, 500)
        assert "__png_assets_partXX_of_YY.zip" in text
        assert "ZIP_STORED" in text
        assert "Source archive and PNG asset parts" in text
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_png_assets_zip_is_reused_when_signature_is_unchanged() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="png_asset_reuse_"))
    try:
        project_root = workspace / "demo_project"
        _make_project(project_root)
        first_destination = workspace / "demo_project_show_project_to_AI" / "second_prompt_files"
        second_destination = workspace / "stage_second_prompt_files"
        temp_root = workspace / "zip_temp"
        first_destination.mkdir(parents=True)
        second_destination.mkdir(parents=True)
        temp_root.mkdir(parents=True)

        first = write_source_archive_parts(
            project_root,
            first_destination,
            temp_root,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
        )
        assert first["ok"] is True, first
        assert first["png_assets_reused"] is False
        first_png = first_destination / first["png_asset_zip_parts"][0]["filename"]
        first_sha = first["png_asset_zip_parts"][0]["sha256"]

        second = write_source_archive_parts(
            project_root,
            second_destination,
            temp_root,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
            reuse_png_assets_from=first_destination,
        )
        assert second["ok"] is True, second
        assert second["png_assets_reused"] is True
        assert second["png_asset_zip_parts"][0]["sha256"] == first_sha
        second_png = second_destination / second["png_asset_zip_parts"][0]["filename"]
        assert second_png.exists()
        assert second_png.read_bytes() == first_png.read_bytes()

        (project_root / "assets" / "new_image.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"c" * 64)
        third_destination = workspace / "stage_after_new_png"
        third_destination.mkdir(parents=True)
        third = write_source_archive_parts(
            project_root,
            third_destination,
            temp_root,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
            reuse_png_assets_from=first_destination,
        )
        assert third["ok"] is True, third
        assert third["png_assets_reused"] is False
        with zipfile.ZipFile(third_destination / third["png_asset_zip_parts"][0]["filename"], "r") as archive:
            assert "assets/new_image.png" in set(archive.namelist())
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_png_assets_reuse_can_read_previous_manifest_from_handoff_zip() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="png_asset_reuse_handoff_"))
    try:
        project_root = workspace / "demo_project"
        _make_project(project_root)
        previous_destination = workspace / "demo_project_show_project_to_AI" / "second_prompt_files"
        next_destination = workspace / "next_stage"
        temp_root = workspace / "zip_temp"
        previous_destination.mkdir(parents=True)
        next_destination.mkdir(parents=True)
        temp_root.mkdir(parents=True)

        first = write_source_archive_parts(
            project_root,
            previous_destination,
            temp_root,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
        )
        manifest_path = Path(str(first["manifest_path"]))
        handoff_zip = previous_destination / "demo_project__ai_handoff_upload.zip"
        with zipfile.ZipFile(handoff_zip, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
            archive.write(
                manifest_path,
                arcname="demo_project__ai_handoff_upload/show_project_to_AI/second_prompt_files/demo_project__source_archive_manifest.json",
            )
        manifest_path.unlink()

        second = write_source_archive_parts(
            project_root,
            next_destination,
            temp_root,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
            reuse_png_assets_from=previous_destination,
        )
        assert second["ok"] is True, second
        assert second["png_assets_reused"] is True
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def _make_python_only_project(root: Path) -> None:
    (root / "pkg").mkdir(parents=True)
    (root / "tests").mkdir(parents=True)
    (root / "pkg" / "__init__.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "tests" / "test_pkg.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")


def test_python_only_project_creates_no_png_asset_zip() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="python_only_project_"))
    try:
        project_root = workspace / "pure_python_modules"
        _make_python_only_project(project_root)
        destination = workspace / "pure_python_modules_show_project_to_AI" / "second_prompt_files"
        temp_root = workspace / "zip_temp"
        destination.mkdir(parents=True)
        temp_root.mkdir(parents=True)

        result = write_source_archive_parts(
            project_root,
            destination,
            temp_root,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
        )

        assert result["ok"] is True, result
        assert result["project_slug"] == "pure_python_modules"
        assert len(result["source_zip_parts"]) == 1
        assert result["png_asset_zip_parts"] == []
        assert not list(destination.glob("*__png_assets_part*.zip"))
        assert (destination / "pure_python_modules__source_archive_part01_of_01.zip").exists()
        assert not any("kanda_reasoner" in item.name for item in destination.iterdir())

        manifest = json.loads(Path(str(result["manifest_path"])).read_text(encoding="utf-8"))
        assert manifest["project"]["project_slug"] == "pure_python_modules"
        assert manifest["counts"]["png_asset_files"] == 0
        assert manifest["counts"]["png_asset_archive_parts"] == 0
        assert manifest["png_asset_parts"] == []
        assert manifest["png_asset_archive_contract"]["no_png_files_creates_no_png_zip"] is True
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_png_reuse_uses_selected_project_final_second_prompt_files_when_building() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="selected_project_png_reuse_"))
    try:
        selected_project = workspace / "client_project"
        _make_project(selected_project)
        show_root = workspace / "client_project_show_project_to_AI"
        final_destination = show_root / "second_prompt_files"
        building_destination = show_root / "second_prompt_files_building"
        final_destination.mkdir(parents=True)
        building_destination.mkdir(parents=True)

        bundle = generate_ai_context_bundle(
            selected_project,
            command_results={
                "architecture_validate": {
                    "ran": True,
                    "exit_code": 0,
                    "status": "pass",
                    "summary": "Architecture validation passed.",
                }
            },
            commands_run_by_bundle=True,
        )
        assert bundle["ok"] is True, bundle

        first = export_json_handoff_zip_parts(
            selected_project,
            final_destination,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
        )
        assert first["ok"] is True, first
        final_png = final_destination / "client_project__png_assets_part01_of_01.zip"
        assert final_png.exists()
        first_png_bytes = final_png.read_bytes()

        second = export_json_handoff_zip_parts(
            selected_project,
            building_destination,
            part_size_mb=500,
            part_size_bytes=500 * 1024 * 1024,
        )
        assert second["ok"] is True, second
        building_png = building_destination / "client_project__png_assets_part01_of_01.zip"
        assert building_png.exists()
        assert building_png.read_bytes() == first_png_bytes
        assert not (building_destination / "kanda_reasoner__png_assets_part01_of_01.zip").exists()
        assert not (final_destination / "kanda_reasoner__png_assets_part01_of_01.zip").exists()

        with zipfile.ZipFile(building_destination / "client_project__ai_handoff_upload.zip", "r") as archive:
            names = archive.namelist()
            manifest_names = [name for name in names if name.endswith("client_project__source_archive_manifest.json")]
            assert manifest_names, names
            manifest = json.loads(archive.read(manifest_names[0]).decode("utf-8"))
        assert manifest["project"]["project_slug"] == "client_project"
        assert manifest["counts"]["png_asset_files"] == 2
        assert manifest["counts"]["png_asset_archive_parts"] == 1
        assert all("kanda_reasoner" not in str(item) for item in manifest["png_asset_parts"])
    finally:
        shutil.rmtree(workspace, ignore_errors=True)

def main() -> int:
    test_png_assets_are_exported_as_separate_stored_zip_family()
    test_second_prompt_export_creates_png_asset_package_automatically()
    test_png_asset_readme_mentions_png_asset_parts()
    test_png_assets_zip_is_reused_when_signature_is_unchanged()
    test_png_assets_reuse_can_read_previous_manifest_from_handoff_zip()
    test_python_only_project_creates_no_png_asset_zip()
    test_png_reuse_uses_selected_project_final_second_prompt_files_when_building()
    print("VALIDATION OK: show_project_to_ai_png_assets_archive_v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
