"""Characterization tests for Batch 24 context-bundle facades."""

from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.reasoner_context_bundle.file_manifest_builder import (
    build_file_manifest_payload,
    is_ignored_project_archive,
    iter_active_project_files,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (
    export_json_handoff_zip_parts,
    is_destination_inside_project_root,
)
from kanda_reasoner_app.reasoner_context_bundle.project_context import resolve_project_context


def test_batch24_context_bundle_public_facades_still_run() -> None:
    """Exercise public imports without reaching into private helper modules."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        project_root = temp_root / "sample_project"
        project_root.mkdir()
        (project_root / "a.py").write_text('print("hello")\n', encoding="utf-8")
        (project_root / "data.bin").write_bytes(b"\x00\x01\x02")
        archive_path = project_root / "sample_project.zip"
        archive_path.write_bytes(b"fake zip placeholder")

        context = resolve_project_context(project_root)
        assert is_ignored_project_archive(archive_path, context) is True

        active_files = list(iter_active_project_files(context))
        active_names = {path.name for path in active_files}
        assert "a.py" in active_names
        assert "data.bin" in active_names

        payload = build_file_manifest_payload(context)
        assert payload["bundle_kind"] == "file_manifest"
        file_records = {item["path"]: item for item in payload["files"]}
        assert file_records["a.py"]["kind"] == "text"
        assert file_records["a.py"]["included_in_active_snapshot"] is True
        assert file_records["data.bin"]["kind"] == "binary"

        outside_destination = temp_root / "outside"
        outside_destination.mkdir()
        assert is_destination_inside_project_root(project_root, project_root / "child") is True
        assert is_destination_inside_project_root(project_root, outside_destination) is False

        destination_error = export_json_handoff_zip_parts(
            project_root,
            project_root,
            check_bundle=False,
        )
        assert destination_error["ok"] is False
        assert "Destination folder is inside" in destination_error["failures"][0]

        size_error = export_json_handoff_zip_parts(
            project_root,
            outside_destination,
            part_size_mb=123,
            check_bundle=False,
        )
        assert size_error["ok"] is False
        assert "part_size_mb must be one of" in size_error["failures"][0]
