"""Validate Source Tree Exporter Refactor Completion Guard v1."""

from __future__ import annotations

import ast
import json
import sys
import tempfile
import zipfile
from pathlib import Path

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

TARGET_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle"

EXPECTED_MODULES = {
    "source_tree_exporter.py",
    "source_tree_exporter_shared.py",
    "source_tree_exporter_inventory.py",
    "source_tree_exporter_archive_io.py",
    "source_tree_exporter_planning.py",
    "source_tree_exporter_writer.py",
}
MAX_LINES = 500
FACADE_MAX_LINES = 80
HELPER_MIN_LINES = 80


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _function_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


def _assert_completion_shape() -> None:
    actual = {path.name for path in TARGET_DIR.glob("source_tree_exporter*.py")}
    unexpected = actual - EXPECTED_MODULES
    missing = EXPECTED_MODULES - actual
    assert not missing, ("missing source-tree-exporter modules", sorted(missing))
    assert not unexpected, ("unexpected source-tree-exporter refactor helper sprawl", sorted(unexpected))

    counts = {name: _line_count(TARGET_DIR / name) for name in sorted(EXPECTED_MODULES)}
    assert counts["source_tree_exporter.py"] < FACADE_MAX_LINES, counts
    for name, count in counts.items():
        assert count <= MAX_LINES, (name, count)
    for name in sorted(EXPECTED_MODULES - {"source_tree_exporter.py"}):
        assert counts[name] >= HELPER_MIN_LINES, (name, counts[name])


def _assert_facade_contract() -> None:
    facade = (TARGET_DIR / "source_tree_exporter.py").read_text(encoding="utf-8")
    assert "write_source_archive_parts" in facade
    assert "gather_source_archive_inventory" in facade
    assert "build_source_archive_manifest_path" in facade
    assert "source_tree_exporter_writer" in facade
    assert "source_tree_exporter_inventory" in facade
    assert "source_tree_exporter_shared" in facade
    assert "def write_source_archive_parts" not in facade
    assert "def gather_source_archive_inventory" not in facade
    assert "__all__" in facade


def _assert_ownership() -> None:
    ownership = {
        "source_tree_exporter_shared.py": {
            "_context",
            "build_source_archive_manifest_path",
            "_posix_rel",
            "_exclusion_record",
            "_is_path_same_or_inside",
            "_is_generated_output_path",
            "_is_generated_project_archive",
            "_excluded_by_project_rules",
            "_is_png_asset_record",
            "_split_png_asset_records",
        },
        "source_tree_exporter_inventory.py": {
            "_excluded_by_builtin_policy",
            "_file_record",
            "_iter_sorted_entries",
            "_load_previous_source_archive_manifest",
            "_previous_png_record_map",
            "_current_png_signature",
            "_previous_png_signature",
            "_can_reuse_previous_png_assets",
            "gather_source_archive_inventory",
        },
        "source_tree_exporter_archive_io.py": {
            "_write_zip",
            "_reuse_previous_png_asset_parts",
            "_write_archive_groups",
        },
        "source_tree_exporter_planning.py": {
            "_estimate_record_size",
            "_candidate_zip_size",
            "_single_record_fits",
            "_initial_groups",
            "_enforce_group_caps",
            "_rebalance_tiny_final_group",
            "_part_filename",
            "_png_asset_part_filename",
        },
        "source_tree_exporter_writer.py": {"_write_manifest", "write_source_archive_parts"},
    }
    for filename, expected in ownership.items():
        names = _function_names(TARGET_DIR / filename)
        missing = expected - names
        assert not missing, (filename, sorted(missing))


def _assert_manifest_contract(payload: dict) -> None:
    assert payload["bundle_kind"] == "source_archive_manifest"
    assert payload["archive_contract"]["parts_are_standalone_zip_files"] is True
    assert payload["archive_contract"]["byte_chunking_allowed"] is False
    assert payload["archive_contract"]["chunk_manifest_allowed"] is False
    assert payload["archive_contract"]["chunks_folder_allowed"] is False
    assert payload["png_asset_archive_contract"]["enabled"] is True
    assert payload["png_asset_archive_contract"]["compression_method"] == "ZIP_STORED"
    assert payload["png_asset_archive_contract"]["signature_fields"] == [
        "path",
        "size_bytes",
        "mtime_ns",
        "sha256",
    ]
    for key in [
        "counts",
        "parts",
        "png_asset_parts",
        "included_files",
        "excluded_paths",
        "reconstruction_instructions",
    ]:
        assert key in payload, key


def _assert_synthetic_export_and_png_reuse_guard() -> None:
    from kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter import (
        gather_source_archive_inventory,
        write_source_archive_parts,
    )

    with tempfile.TemporaryDirectory(prefix="kanda_source_tree_completion_guard_") as tmp_text:
        tmp = Path(tmp_text)
        project = tmp / "sample_project"
        output = tmp / "sample_project_show_project_to_AI" / "second_prompt_files"
        temp_root = tmp / "working_temp"
        (project / "pkg").mkdir(parents=True)
        (project / "show_project_to_AI").mkdir()
        (project / "second_prompt_files").mkdir()
        (project / "__pycache__").mkdir()
        (project / "pkg" / "a.py").write_text("print('hello')\n", encoding="utf-8")
        (project / "pkg" / "readme.txt").write_text("readme\n", encoding="utf-8")
        (project / "pkg" / "image.png").write_bytes(b"pngbytes")
        (project / "show_project_to_AI" / "generated.txt").write_text("ignore\n", encoding="utf-8")
        (project / "second_prompt_files" / "generated.txt").write_text("ignore\n", encoding="utf-8")
        (project / "__pycache__" / "x.pyc").write_bytes(b"cache")

        inventory = gather_source_archive_inventory(project, output)
        included = [item["path"] for item in inventory["included_files"]]
        assert included == ["pkg/a.py", "pkg/image.png", "pkg/readme.txt"], included
        excluded_codes = {item["reason_code"] for item in inventory["excluded_paths"]}
        assert "recursive_output_guard" in excluded_codes, excluded_codes
        assert "standard_noise_directory" in excluded_codes, excluded_codes

        result = write_source_archive_parts(
            project,
            output,
            temp_root,
            part_size_mb=1,
            part_size_bytes=1024 * 1024,
        )
        assert result["ok"] is True
        assert result["png_assets_reused"] is False
        manifest = Path(result["manifest_path"])
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        _assert_manifest_contract(payload)
        manifest_records = payload["included_files"]
        assert [item["path"] for item in manifest_records] == included
        assert any(item.get("archive_family") == "png_assets" for item in manifest_records)
        for part in result["created_paths"]:
            part_path = Path(part)
            assert part_path.exists(), part_path
            if part_path.suffix == ".zip":
                with zipfile.ZipFile(part_path, "r") as archive:
                    assert archive.testzip() is None

        second_output = tmp / "sample_project_show_project_to_AI_second" / "second_prompt_files"
        second_temp = tmp / "working_temp_second"
        second = write_source_archive_parts(
            project,
            second_output,
            second_temp,
            part_size_mb=1,
            part_size_bytes=1024 * 1024,
            reuse_png_assets_from=output,
        )
        assert second["ok"] is True
        assert second["png_assets_reused"] is True

        png_part_names = [part["filename"] for part in payload["png_asset_parts"]]
        assert png_part_names, payload
        corrupt_part = output / png_part_names[0]
        corrupt_part.write_bytes(b"not a valid previous png asset zip")

        third_output = tmp / "sample_project_show_project_to_AI_third" / "second_prompt_files"
        third_temp = tmp / "working_temp_third"
        third = write_source_archive_parts(
            project,
            third_output,
            third_temp,
            part_size_mb=1,
            part_size_bytes=1024 * 1024,
            reuse_png_assets_from=output,
        )
        assert third["ok"] is True
        assert third["png_assets_reused"] is False


def main() -> None:
    _ensure_project_root_on_path()
    _assert_completion_shape()
    _assert_facade_contract()
    _assert_ownership()
    _assert_synthetic_export_and_png_reuse_guard()
    print("VALIDATION OK: source-tree-exporter-refactor-completion-guard-v1")


if __name__ == "__main__":
    main()
