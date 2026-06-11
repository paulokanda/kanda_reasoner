"""Direct tests for handoff_zip_exporter_writer public contract."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter_writer import (  # noqa: E402
    __all__ as WRITER_ALL,
    write_zip,
    zip_record,
)
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext  # noqa: E402


def _context(project_root: Path) -> ProjectContext:
    return ProjectContext(
        root=project_root,
        project_slug="demo_project",
        evidence_root=project_root / "project_analysis_evidence",
        json_complete_dir=project_root / "project_analysis_evidence" / "json_complete",
    )


def test_writer_contract_exports_expected_surface() -> None:
    assert set(WRITER_ALL) == {
        "candidate_zip_size",
        "split_artifacts_into_parts",
        "write_external_readme",
        "write_package_parts",
        "write_zip",
        "zip_record",
    }


def test_writer_writes_zip_and_reports_record() -> None:
    with TemporaryDirectory() as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "project"
        destination = temp_root / "outside"
        project_root.mkdir()
        destination.mkdir()
        artifact = project_root / "example.json"
        artifact.write_text(json.dumps({"ok": True}), encoding="utf-8")
        zip_path = destination / "demo.zip"
        context = _context(project_root)

        write_zip(
            zip_path,
            [artifact],
            context,
            "demo_project__ai_handoff_upload",
            readme_text="readme",
            readme_name="UPLOAD_README.txt",
        )

        with zipfile.ZipFile(zip_path, "r") as archive:
            names = set(archive.namelist())
        assert "demo_project__ai_handoff_upload/UPLOAD_README.txt" in names
        assert "demo_project__ai_handoff_upload/example.json" in names

        record = zip_record(zip_path, [artifact], context, "upload")
        assert record["package"] == "upload"
        assert record["artifact_count"] == 1
        assert record["artifacts"][0]["path"] == "example.json"


if __name__ == "__main__":
    test_writer_contract_exports_expected_surface()
    test_writer_writes_zip_and_reports_record()
    print("handoff_zip_exporter_writer direct tests passed.")
