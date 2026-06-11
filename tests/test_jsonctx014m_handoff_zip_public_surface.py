"""JSONCTX014M tests for handoff ZIP helper public-surface contracts."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle import handoff_zip_exporter as facade
from kanda_reasoner_app.reasoner_context_bundle import handoff_zip_exporter_support as support
from kanda_reasoner_app.reasoner_context_bundle import handoff_zip_exporter_writer as writer
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext


def test_support_public_surface_is_explicit_and_stable() -> None:
    expected = {
        "context_from_project",
        "ordered_export_paths",
        "package_specs",
        "timestamp_value",
        "artifact_record",
        "safe_zip_member_name",
    }
    assert expected.issubset(set(support.__all__))
    assert "DEFAULT_PART_SIZE_MB" not in support.__all__
    assert "CONSERVATIVE_PART_SIZE_MB" not in support.__all__
    assert "is_destination_inside_project_root" not in support.__all__
    assert facade.DEFAULT_PART_SIZE_MB == 40
    assert facade.CONSERVATIVE_PART_SIZE_MB == 25
    assert facade.is_destination_inside_project_root(Path("C:/project"), Path("C:/project/subdir"))


def test_writer_public_surface_is_explicit_and_writes_valid_zip() -> None:
    expected = {
        "candidate_zip_size",
        "split_artifacts_into_parts",
        "write_external_readme",
        "write_package_parts",
        "write_zip",
        "zip_record",
    }
    assert expected == set(writer.__all__)

    with TemporaryDirectory() as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "project"
        destination = temp_root / "outside"
        project_root.mkdir()
        destination.mkdir()
        artifact = project_root / "example.json"
        artifact.write_text(json.dumps({"ok": True}), encoding="utf-8")

        context = ProjectContext(
            root=project_root,
            project_slug="demo_project",
            evidence_root=project_root / "project_analysis_evidence",
            json_complete_dir=project_root / "project_analysis_evidence" / "json_complete",
        )
        zip_path = destination / "demo.zip"
        writer.write_zip(
            zip_path,
            [artifact],
            context,
            "demo_project__ai_handoff_upload",
            readme_text="readme",
            readme_name="UPLOAD_README.txt",
        )

        assert zip_path.exists()
        with zipfile.ZipFile(zip_path, "r") as archive:
            names = set(archive.namelist())
        assert "demo_project__ai_handoff_upload/UPLOAD_README.txt" in names
        assert "demo_project__ai_handoff_upload/example.json" in names


def test_writer_zip_record_reports_artifact_metadata() -> None:
    with TemporaryDirectory() as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "project"
        destination = temp_root / "outside"
        project_root.mkdir()
        destination.mkdir()
        artifact = project_root / "example.json"
        artifact.write_text("{}", encoding="utf-8")
        zip_path = destination / "demo.zip"
        zip_path.write_bytes(b"zip-bytes")
        context = ProjectContext(
            root=project_root,
            project_slug="demo_project",
            evidence_root=project_root / "project_analysis_evidence",
            json_complete_dir=project_root / "project_analysis_evidence" / "json_complete",
        )

        record = writer.zip_record(zip_path, [artifact], context, "upload")
        assert record["package"] == "upload"
        assert record["filename"] == "demo.zip"
        assert record["artifact_count"] == 1
        assert record["artifacts"][0]["path"] == "example.json"


if __name__ == "__main__":
    test_support_public_surface_is_explicit_and_stable()
    test_writer_public_surface_is_explicit_and_writes_valid_zip()
    test_writer_zip_record_reports_artifact_metadata()
    print("JSONCTX014M handoff ZIP public surface tests passed.")
