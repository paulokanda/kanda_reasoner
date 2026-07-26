from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path

from kanda_reasoner_app.reasoner_context_bundle.bundle_manifest_builder import BUNDLE_ARTIFACT_ORDER
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter_support import package_specs
from kanda_reasoner_app.reasoner_context_bundle.source_archive_exporter import write_source_archive_parts
from kanda_reasoner_app.reasoner_context_bundle.project_context import resolve_project_context


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _make_project(base: Path, name: str) -> Path:
    root = base / name
    (root / "app").mkdir(parents=True)
    (root / "app" / "main.py").write_text("print('hello from ' + __name__)\n", encoding="utf-8")
    (root / "README.md").write_text("# " + name + "\n", encoding="utf-8")
    (root / ".git").mkdir()
    (root / ".git" / "config").write_text("ignored", encoding="utf-8")
    (root / "__pycache__").mkdir()
    (root / "__pycache__" / "main.cpython-312.pyc").write_bytes(b"ignored")
    return root


def test_source_archive_uses_selected_project_root_not_tool_root() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="hybrid_source_archive_dynamic_root_"))
    try:
        tool_root = _make_project(workspace, "kanda_reasoner")
        (tool_root / "tool_only.py").write_text("tool", encoding="utf-8")
        selected_root = _make_project(workspace, "other_project")
        (selected_root / "selected_only.py").write_text("selected", encoding="utf-8")

        destination = workspace / "other_project_show_project_to_AI" / "second_prompt_files"
        temp_root = destination / "_tmp"
        destination.mkdir(parents=True)
        temp_root.mkdir()

        result = write_source_archive_parts(
            selected_root,
            destination,
            temp_root,
            part_size_mb=40,
            part_size_bytes=40 * 1024 * 1024,
        )
        assert result["ok"] is True
        assert result["project_slug"] == "other_project"

        manifest_path = Path(str(result["manifest_path"]))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["project"]["project_slug"] == "other_project"
        assert manifest["project"]["dynamic_output_contract"] == "<project_drive>:\\<project_slug>_show_project_to_AI\\second_prompt_files"
        assert manifest["archive_contract"]["selected_size_cap_bytes"] == 40 * 1024 * 1024
        assert manifest["archive_contract"]["planning_target_bytes"] == int(40 * 1024 * 1024 * 0.90)
        assert manifest["archive_contract"]["byte_chunking_allowed"] is False
        assert manifest["archive_contract"]["chunk_manifest_allowed"] is False
        assert manifest["archive_contract"]["chunks_folder_allowed"] is False

        included_paths = {item["path"] for item in manifest["included_files"]}
        assert "selected_only.py" in included_paths
        assert "app/main.py" in included_paths
        assert "tool_only.py" not in included_paths
        assert all("kanda_reasoner" not in item["path"] for item in manifest["included_files"])

        excluded_paths = {item["path"] for item in manifest["excluded_paths"]}
        assert ".git" in excluded_paths or any(path.startswith(".git/") for path in excluded_paths)
        assert "__pycache__" in excluded_paths or any(path.startswith("__pycache__/") for path in excluded_paths)

        zip_parts = [Path(item["path"]) for item in manifest["parts"]]
        assert zip_parts
        assert all(path.name.startswith("other_project__source_archive_part") for path in zip_parts)
        assert all(path.stat().st_size <= 40 * 1024 * 1024 for path in zip_parts)

        extract_dir = workspace / "roundtrip"
        extract_dir.mkdir()
        for archive_path in zip_parts:
            with zipfile.ZipFile(archive_path, "r") as archive:
                names = archive.namelist()
                assert "CHUNK_MANIFEST.json" not in names
                assert not any(name.startswith("chunks/") or "/chunks/" in name for name in names)
                archive.extractall(extract_dir)
        for item in manifest["included_files"]:
            extracted = extract_dir / item["path"]
            assert extracted.is_file(), item["path"]
            assert _sha256(extracted) == item["sha256"]
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_small_cap_uses_file_level_parts_without_byte_chunks() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="hybrid_source_archive_small_cap_"))
    try:
        selected_root = workspace / "small_project"
        selected_root.mkdir()
        for index in range(5):
            (selected_root / f"data_{index}.bin").write_bytes(os.urandom(6000))
        destination = workspace / "small_project_show_project_to_AI" / "second_prompt_files"
        temp_root = destination / "_tmp"
        destination.mkdir(parents=True)
        temp_root.mkdir()

        result = write_source_archive_parts(
            selected_root,
            destination,
            temp_root,
            part_size_mb=1,
            part_size_bytes=16000,
        )
        manifest = json.loads(Path(str(result["manifest_path"])).read_text(encoding="utf-8"))
        assert len(manifest["parts"]) >= 2
        assert all(part["actual_size_bytes"] <= 16000 for part in manifest["parts"])
        for part in manifest["parts"]:
            with zipfile.ZipFile(part["path"], "r") as archive:
                names = archive.namelist()
                assert "CHUNK_MANIFEST.json" not in names
                assert not any(name.startswith("chunks/") or "/chunks/" in name for name in names)
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def test_reconstruction_payload_is_not_required_or_packaged() -> None:
    assert "reconstruction_payload_json" not in BUNDLE_ARTIFACT_ORDER
    context = resolve_project_context(Path(tempfile.mkdtemp(prefix="hybrid_specs_project_")))
    specs = package_specs(context, [])
    names = [spec["name"] for spec in specs]
    assert names == ["upload", "all_in_one"]
    assert all("reconstruction" not in spec["stem"] for spec in specs)


def test_legacy_byte_chunk_warning_strings_are_not_active() -> None:
    writer = Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_writer.py").read_text(encoding="utf-8")
    assert "Single artifact requires byte-chunk ZIP splitting" not in writer
    assert "Oversized artifact split into" not in writer
    assert "CHUNK_MANIFEST.json" not in writer
    assert "/chunks/" not in writer


def main() -> int:
    test_source_archive_uses_selected_project_root_not_tool_root()
    test_small_cap_uses_file_level_parts_without_byte_chunks()
    test_reconstruction_payload_is_not_required_or_packaged()
    test_legacy_byte_chunk_warning_strings_are_not_active()
    print("VALIDATION OK: show_project_to_ai_hybrid_source_archive_export_v1")
    print("VALIDATION OK: show project to AI hybrid source archive export")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
