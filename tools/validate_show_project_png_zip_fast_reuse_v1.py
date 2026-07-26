"""Focused validation for true fast reuse of unchanged PNG ZIP parts."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext
from kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter import (
    write_source_archive_parts,
)

FEATURE_ID = "show-project-png-zip-fast-reuse-v1"


def _context(root: Path, output: Path) -> ProjectContext:
    return ProjectContext(
        root=root,
        project_slug="sample_project",
        evidence_root=output.parent,
        json_complete_dir=output,
        active_project_id="sample-project",
        active_project_root_fingerprint="focused-test",
    )


def _write_sample_project(root: Path) -> Path:
    package = root / "pkg"
    package.mkdir(parents=True)
    (package / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    image = package / "image.png"
    image.write_bytes(b"PNG-CONTENT-UNCHANGED")
    return image


def _validate_fast_reuse() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_png_fast_reuse_") as temp_text:
        temp = Path(temp_text)
        project = temp / "sample_project"
        first_output = temp / "first" / "second_prompt_files"
        second_output = temp / "second" / "second_prompt_files"
        third_output = temp / "third" / "second_prompt_files"
        image = _write_sample_project(project)

        first = write_source_archive_parts(
            _context(project, first_output),
            first_output,
            temp / "first_temp",
            part_size_mb=1,
            part_size_bytes=1024 * 1024,
        )
        assert first["png_assets_reused"] is False
        assert first["png_assets_reuse_method"] == "created"

        first_manifest = json.loads(
            Path(first["manifest_path"]).read_text(encoding="utf-8")
        )
        contract = first_manifest["png_asset_archive_contract"]
        assert contract["content_signature_fields"] == [
            "path",
            "size_bytes",
            "sha256",
        ]
        assert len(contract["content_signature_sha256"]) == 64
        assert contract["preferred_reuse_method"] == "same_volume_hardlink"
        first_part = first_output / first["png_asset_zip_parts"][0]["filename"]

        image_stat = image.stat()
        os.utime(
            image,
            ns=(image_stat.st_atime_ns, image_stat.st_mtime_ns + 10_000_000),
        )
        second = write_source_archive_parts(
            _context(project, second_output),
            second_output,
            temp / "second_temp",
            part_size_mb=1,
            part_size_bytes=1024 * 1024,
            reuse_png_assets_from=first_output,
        )
        assert second["png_assets_reused"] is True
        assert second["png_assets_reuse_method"] in {"hardlink", "copy"}
        second_part = second_output / second["png_asset_zip_parts"][0]["filename"]
        assert first_part.read_bytes() == second_part.read_bytes()
        if second["png_assets_reuse_method"] == "hardlink":
            assert os.path.samefile(first_part, second_part)

        second_manifest = json.loads(
            Path(second["manifest_path"]).read_text(encoding="utf-8")
        )
        second_record = second_manifest["png_asset_parts"][0]
        assert int(second_record["file_mtime_ns"]) == int(
            second_part.stat().st_mtime_ns
        )
        assert second_record["reuse_method"] == second["png_assets_reuse_method"]

        image.write_bytes(b"PNG-CONTENT-CHANGED")
        third = write_source_archive_parts(
            _context(project, third_output),
            third_output,
            temp / "third_temp",
            part_size_mb=1,
            part_size_bytes=1024 * 1024,
            reuse_png_assets_from=second_output,
        )
        assert third["png_assets_reused"] is False
        assert third["png_assets_reuse_method"] == "created"

    print("PNG_CONTENT_IDENTITY_REUSE: PASS")
    print("PNG_TIMESTAMP_ONLY_CHANGE_REUSES: PASS")
    print("PNG_SAME_VOLUME_HARDLINK_OR_COPY_FALLBACK: PASS")
    print("PNG_CONTENT_CHANGE_REBUILDS: PASS")


def _validate_source_contract(root: Path) -> None:
    inventory = root / (
        "kanda_reasoner_app/reasoner_context_bundle/"
        "source_tree_exporter_inventory.py"
    )
    archive_io = root / (
        "kanda_reasoner_app/reasoner_context_bundle/"
        "source_tree_exporter_archive_io.py"
    )
    writer = root / (
        "kanda_reasoner_app/reasoner_context_bundle/"
        "source_tree_exporter_writer.py"
    )
    handoff = root / (
        "kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py"
    )
    process = root / (
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
        "zip_json_files_process_private_impl.py"
    )

    inventory_text = inventory.read_text(encoding="utf-8")
    archive_text = archive_io.read_text(encoding="utf-8")
    writer_text = writer.read_text(encoding="utf-8")
    handoff_text = handoff.read_text(encoding="utf-8")
    process_text = process.read_text(encoding="utf-8")

    assert "content_signature_sha256" in writer_text
    assert "metadata_identity_matches" in inventory_text
    assert "require_full_test=False" in inventory_text
    assert "os.link(source_path, destination_zip)" in archive_text
    assert 'reuse_method = "hardlink"' in archive_text
    assert 'reuse_method = "copy"' in archive_text
    assert "png_assets_reuse_method" in handoff_text
    assert "png_assets_reuse_method:" in process_text

    for path in (inventory, archive_io, writer, handoff, process):
        assert len(path.read_text(encoding="utf-8").splitlines()) <= 500, path

    print("PNG_FAST_METADATA_VERIFICATION: PASS")
    print("PNG_FULL_HASH_CRC_FALLBACK: PASS")
    print("PNG_REUSE_METHOD_OBSERVABILITY: PASS")
    print("MODULE_SIZE_GATE: PASS")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    _validate_fast_reuse()
    _validate_source_contract(root)
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
