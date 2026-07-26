"""Validate Source Tree Exporter Refactor Train Car 1 v1."""

from __future__ import annotations

import ast
import json
import shutil
import tempfile
import sys
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
MODULES = [
    "source_tree_exporter.py",
    "source_tree_exporter_shared.py",
    "source_tree_exporter_inventory.py",
    "source_tree_exporter_archive_io.py",
    "source_tree_exporter_planning.py",
    "source_tree_exporter_writer.py",
]
MAX_LINES = 500
MIN_SUBSTANTIVE_LINES = 80


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _function_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


def _assert_line_contracts() -> None:
    counts = {name: _line_count(TARGET_DIR / name) for name in MODULES}
    assert counts["source_tree_exporter.py"] < MIN_SUBSTANTIVE_LINES, counts
    for name, count in counts.items():
        assert count <= MAX_LINES, (name, count)
    for name in MODULES[1:]:
        assert counts[name] >= MIN_SUBSTANTIVE_LINES, (name, counts[name])


def _assert_facade_contract() -> None:
    facade = (TARGET_DIR / "source_tree_exporter.py").read_text(encoding="utf-8")
    assert "write_source_archive_parts" in facade
    assert "gather_source_archive_inventory" in facade
    assert "build_source_archive_manifest_path" in facade
    assert "source_tree_exporter_writer" in facade
    assert "source_tree_exporter_inventory" in facade
    assert "def write_source_archive_parts" not in facade
    assert "def gather_source_archive_inventory" not in facade
    assert "SOURCE_ARCHIVE_MANIFEST_SUFFIX" in facade


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


def _assert_synthetic_export() -> None:
    from kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter import (
        gather_source_archive_inventory,
        write_source_archive_parts,
    )

    with tempfile.TemporaryDirectory(prefix="kanda_source_tree_exporter_test_") as tmp_text:
        tmp = Path(tmp_text)
        project = tmp / "sample_project"
        output = tmp / "sample_project_show_project_to_AI" / "second_prompt_files"
        temp_root = tmp / "working_temp"
        (project / "pkg").mkdir(parents=True)
        (project / "show_project_to_AI").mkdir()
        (project / "__pycache__").mkdir()
        (project / "pkg" / "a.py").write_text("print('hello')\n", encoding="utf-8")
        (project / "pkg" / "readme.txt").write_text("readme\n", encoding="utf-8")
        (project / "pkg" / "image.png").write_bytes(b"pngbytes")
        (project / "show_project_to_AI" / "generated.txt").write_text("ignore\n", encoding="utf-8")
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
        assert manifest.exists()
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        manifest_records = payload["included_files"]
        assert [item["path"] for item in manifest_records] == included
        assert any(item.get("archive_family") == "png_assets" for item in manifest_records)
        assert payload["archive_contract"]["parts_are_standalone_zip_files"] is True
        assert payload["png_asset_archive_contract"]["compression_method"] == "ZIP_STORED"
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


def main() -> None:
    _ensure_project_root_on_path()
    _assert_line_contracts()
    _assert_facade_contract()
    _assert_ownership()
    _assert_synthetic_export()
    print("VALIDATION OK: source-tree-exporter-refactor-train-car-1-v1")


if __name__ == "__main__":
    main()
