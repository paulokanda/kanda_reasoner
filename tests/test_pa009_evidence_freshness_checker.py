"""Focused tests for PA009 evidence freshness checker."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_freshness import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT,
    ProjectSymbolAtlasEvidenceFreshnessOptions,
    build_reasoner_symbol_atlas_evidence_freshness_report,
    check_reasoner_symbol_atlas_evidence_freshness,
)


def _write_complete_json(
    project_root: Path,
    generated_at: datetime,
    source_files: list[str],
    evidence_project_root: Path | None = None,
) -> Path:
    evidence_dir = project_root / "project_analysis_evidence" / "json_complete"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "project_root": str(evidence_project_root or project_root),
        "generated_at": generated_at.replace(microsecond=0).isoformat(),
        "source_file_index": {
            item: {"file": item, "line_count": 1} for item in source_files
        },
        "symbol_index": {},
        "primary_definition_index": {},
    }
    path = evidence_dir / "sample_project__complete.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n")
    return path


def _write_py(project_root: Path, relative_path: str, content: str = "x = 1\n") -> Path:
    path = project_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def _set_mtime(path: Path, moment: datetime) -> None:
    timestamp = moment.timestamp()
    os.utime(path, (timestamp, timestamp))


def test_pa009_missing_evidence_is_reported_without_writes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        summary = check_reasoner_symbol_atlas_evidence_freshness(
            ProjectSymbolAtlasEvidenceFreshnessOptions(project_root=str(root))
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE
        assert not (root / "project_analysis_evidence").exists()


def test_pa009_reports_fresh_evidence_when_live_tree_matches() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        generated_at = datetime.now(timezone.utc)
        file_path = _write_py(root, "pkg/main.py")
        _set_mtime(file_path, generated_at - timedelta(minutes=5))
        json_path = _write_complete_json(root, generated_at, ["pkg/main.py"])
        summary = check_reasoner_symbol_atlas_evidence_freshness(
            ProjectSymbolAtlasEvidenceFreshnessOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH
        assert not summary.missing_source_files
        assert not summary.new_source_files
        assert not summary.modified_after_generation


def test_pa009_reports_stale_when_source_file_changed_after_generation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        generated_at = datetime.now(timezone.utc) - timedelta(hours=1)
        file_path = _write_py(root, "pkg/main.py")
        _set_mtime(file_path, generated_at + timedelta(minutes=5))
        json_path = _write_complete_json(root, generated_at, ["pkg/main.py"])
        summary = check_reasoner_symbol_atlas_evidence_freshness(
            ProjectSymbolAtlasEvidenceFreshnessOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE
        assert "pkg/main.py" in summary.modified_after_generation


def test_pa009_keeps_json_canonical_when_new_file_exists() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        generated_at = datetime.now(timezone.utc)
        old_file = _write_py(root, "pkg/main.py")
        new_file = _write_py(root, "pkg/new_module.py")
        _set_mtime(old_file, generated_at - timedelta(minutes=5))
        _set_mtime(new_file, generated_at - timedelta(minutes=4))
        json_path = _write_complete_json(root, generated_at, ["pkg/main.py"])
        summary = check_reasoner_symbol_atlas_evidence_freshness(
            ProjectSymbolAtlasEvidenceFreshnessOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL
        assert "pkg/new_module.py" in summary.new_source_files


def test_pa009_reports_wrong_project_evidence() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        other_root = Path(tmp) / "other_project"
        root.mkdir()
        other_root.mkdir()
        generated_at = datetime.now(timezone.utc)
        _write_py(root, "pkg/main.py")
        json_path = _write_complete_json(
            root,
            generated_at,
            ["pkg/main.py"],
            evidence_project_root=other_root,
        )
        summary = check_reasoner_symbol_atlas_evidence_freshness(
            ProjectSymbolAtlasEvidenceFreshnessOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT


def test_pa009_builds_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        generated_at = datetime.now(timezone.utc)
        file_path = _write_py(root, "pkg/main.py")
        _set_mtime(file_path, generated_at - timedelta(minutes=5))
        json_path = _write_complete_json(root, generated_at, ["pkg/main.py"])
        report = build_reasoner_symbol_atlas_evidence_freshness_report(
            ProjectSymbolAtlasEvidenceFreshnessOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert "status=fresh" in data["summary"]


def main() -> int:
    test_pa009_missing_evidence_is_reported_without_writes()
    test_pa009_reports_fresh_evidence_when_live_tree_matches()
    test_pa009_reports_stale_when_source_file_changed_after_generation()
    test_pa009_keeps_json_canonical_when_new_file_exists()
    test_pa009_reports_wrong_project_evidence()
    test_pa009_builds_report()
    print("PA009 Evidence freshness checker tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
