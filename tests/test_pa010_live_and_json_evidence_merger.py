"""Focused tests for PA010 live AST plus complete JSON evidence merger."""

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

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_merger import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ADVISORY,
    PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ENRICHED,
    PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_REJECTED,
    PROJECT_SYMBOL_ATLAS_MERGE_STATUS_LIVE_ONLY,
    ProjectSymbolAtlasEvidenceMergeOptions,
    build_reasoner_symbol_atlas_merged_evidence_report,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)


def _write_file(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def _set_mtime(path: Path, moment: datetime) -> None:
    timestamp = moment.timestamp()
    os.utime(path, (timestamp, timestamp))


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
            item: {
                "file": item,
                "module_name": item.replace("/", ".").removesuffix(".py"),
                "line_count": 10,
            }
            for item in source_files
        },
        "symbol_index": {
            "run_app": {
                "file": "pkg/main.py",
                "kind": "function",
                "line": 1,
            }
        },
        "primary_definition_index": {
            "run_app": {
                "primary": {
                    "file": "pkg/main.py",
                    "kind": "function",
                    "line_start": 1,
                }
            }
        },
        "web_ai_symbol_index": {
            "run_app": {
                "file": "pkg/main.py",
                "kind": "function",
                "line_start": 1,
                "module_name": "pkg.main",
                "qualified_name": "run_app",
            }
        },
        "web_ai_file_responsibility_index": {
            "pkg/main.py": {
                "owner_box": "runtime",
                "primary_responsibility": "Application entry logic",
            }
        },
    }
    path = evidence_dir / "sample_project__complete.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n")
    return path


def test_pa010_uses_live_only_when_json_is_missing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        _write_file(root / "pkg" / "main.py", "def run_app():\n    return 1\n")
        report, summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
            ProjectSymbolAtlasEvidenceMergeOptions(project_root=str(root))
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_MERGE_STATUS_LIVE_ONLY
        assert summary.live_module_count == 1
        assert summary.merged_module_count == 1
        assert any(symbol.name == "run_app" for symbol in report.symbols)
        assert not (root / "project_analysis_evidence").exists()


def test_pa010_enriches_live_ast_with_fresh_json() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        generated_at = datetime.now(timezone.utc)
        source_path = _write_file(root / "pkg" / "main.py", "def run_app():\n    return 1\n")
        _set_mtime(source_path, generated_at - timedelta(minutes=5))
        json_path = _write_complete_json(root, generated_at, ["pkg/main.py"])
        report, summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
            ProjectSymbolAtlasEvidenceMergeOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ENRICHED
        assert summary.json_module_count == 1
        assert summary.merged_module_count == 1
        module = report.modules[0]
        assert any("fresh_json_enrichment" in item for item in module.evidence)
        run_symbols = [symbol for symbol in report.symbols if symbol.name == "run_app"]
        assert run_symbols
        assert any("fresh_json_symbol_enrichment" in item for item in run_symbols[0].evidence)


def test_pa010_marks_stale_json_as_advisory() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        generated_at = datetime.now(timezone.utc) - timedelta(hours=1)
        source_path = _write_file(root / "pkg" / "main.py", "def run_app():\n    return 2\n")
        _set_mtime(source_path, generated_at + timedelta(minutes=5))
        json_path = _write_complete_json(root, generated_at, ["pkg/main.py"])
        report, summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
            ProjectSymbolAtlasEvidenceMergeOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ADVISORY
        assert "complete_json_advisory" in report.input_sources
        assert any("json_advisory" in item for item in report.modules[0].evidence)


def test_pa010_rejects_wrong_project_json() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        other_root = Path(tmp) / "other_project"
        root.mkdir()
        other_root.mkdir()
        generated_at = datetime.now(timezone.utc)
        source_path = _write_file(root / "pkg" / "main.py", "def run_app():\n    return 1\n")
        _set_mtime(source_path, generated_at - timedelta(minutes=5))
        json_path = _write_complete_json(
            root,
            generated_at,
            ["pkg/main.py"],
            evidence_project_root=other_root,
        )
        report, summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
            ProjectSymbolAtlasEvidenceMergeOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert summary.status == PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_REJECTED
        assert "complete_json_rejected" in report.input_sources


def test_pa010_builds_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        _write_file(root / "pkg" / "main.py", "def run_app():\n    return 1\n")
        report = build_reasoner_symbol_atlas_merged_evidence_report(
            ProjectSymbolAtlasEvidenceMergeOptions(project_root=str(root))
        )
        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert "Evidence merge status=" in data["summary"]
        assert data["module_count"] == 1


def main() -> int:
    test_pa010_uses_live_only_when_json_is_missing()
    test_pa010_enriches_live_ast_with_fresh_json()
    test_pa010_marks_stale_json_as_advisory()
    test_pa010_rejects_wrong_project_json()
    test_pa010_builds_report()
    print("PA010 Live AST plus JSON evidence merger tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
