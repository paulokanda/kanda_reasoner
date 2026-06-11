"""Tests for PA007B Project Analysis Evidence migration helper."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_migration import (  # noqa: E402
    ProjectAnalysisEvidenceMigrationFile,
    ProjectAnalysisEvidenceMigrationReport,
    migrate_project_analysis_evidence,
    plan_project_analysis_evidence_migration,
    write_project_analysis_evidence_migration_report,
)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def test_pa007b_dry_run_does_not_create_canonical_folder() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        legacy = project_root / "_project_reference" / "project_analysis_evidence"
        _write_json(legacy / "demo__complete.json", {"ok": True})

        report = plan_project_analysis_evidence_migration(project_root)

        assert isinstance(report, ProjectAnalysisEvidenceMigrationReport)
        assert report.status == "migration_available"
        assert report.dry_run is True
        assert report.planned_copy_count == 1
        assert report.copied_count == 0
        assert not (project_root / "project_analysis_evidence").exists()
        assert isinstance(report.files[0], ProjectAnalysisEvidenceMigrationFile)
        assert report.files[0].action == "copy"


def test_pa007b_apply_copies_legacy_json_without_deleting_source() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        legacy = project_root / "_project_reference" / "project_analysis_evidence"
        source_file = legacy / "demo__complete.json"
        _write_json(source_file, {"value": 1})

        report = migrate_project_analysis_evidence(project_root, apply_changes=True)

        target_file = project_root / "project_analysis_evidence" / "demo__complete.json"
        assert report.status == "migrated"
        assert report.dry_run is False
        assert report.copied_count == 1
        assert source_file.exists()
        assert target_file.exists()
        assert json.loads(target_file.read_text(encoding="utf-8"))["value"] == 1


def test_pa007b_apply_backs_up_changed_canonical_file() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        legacy = project_root / "_project_reference" / "project_analysis_evidence"
        canonical = project_root / "project_analysis_evidence"
        _write_json(legacy / "demo__complete.json", {"value": "legacy"})
        _write_json(canonical / "demo__complete.json", {"value": "canonical"})

        report = migrate_project_analysis_evidence(project_root, apply_changes=True)

        assert report.status == "migrated"
        item = report.files[0]
        assert item.action == "backup_and_copy"
        assert item.copied is True
        assert item.backup_path
        assert Path(item.backup_path).exists()
        target = canonical / "demo__complete.json"
        assert json.loads(target.read_text(encoding="utf-8"))["value"] == "legacy"


def test_pa007b_report_writer_outputs_json() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        legacy = project_root / "_project_reference" / "project_analysis_evidence"
        _write_json(legacy / "demo__complete_runtime_trace.json", {"trace": []})
        report = plan_project_analysis_evidence_migration(project_root)
        output_path = project_root / "workbench" / "migration_report.json"

        written = write_project_analysis_evidence_migration_report(report, output_path)

        assert written == output_path
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert payload["status"] == "migration_available"
        assert payload["planned_copy_count"] == 1


def main() -> int:
    test_pa007b_dry_run_does_not_create_canonical_folder()
    test_pa007b_apply_copies_legacy_json_without_deleting_source()
    test_pa007b_apply_backs_up_changed_canonical_file()
    test_pa007b_report_writer_outputs_json()
    print("PA007B Project Analysis Evidence migration helper tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
