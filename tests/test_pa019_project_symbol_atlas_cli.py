"""Focused tests for PA019 Project Symbol Atlas CLI integration."""

from __future__ import annotations

import io
import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.safety_suite_cli.commands import (  # noqa: E402
    available_cli_commands,
    build_safety_suite_parser,
    run_cli,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _make_project() -> Path:
    root = Path(tempfile.mkdtemp(prefix="pa019_atlas_cli_"))
    _write(root / "sample_app" / "__init__.py", "")
    _write(
        root / "sample_app" / "panel.py",
        "from __future__ import annotations\n\n"
        "def build_panel():\n"
        "    return 'panel'\n",
    )
    _write(
        root / "tests" / "test_panel.py",
        "from sample_app.panel import build_panel\n\n"
        "def test_panel():\n"
        "    assert build_panel() == 'panel'\n",
    )
    return root


def test_pa019_command_catalog_includes_atlas_commands() -> None:
    commands = available_cli_commands()
    assert "atlas-report" in commands
    assert "evidence-freshness" in commands
    assert "find-symbol" in commands
    assert "pre-patch-gate" in commands
    parser = build_safety_suite_parser()
    assert parser.prog == "kanda-safety-suite"


def test_pa019_list_tools_outputs_atlas_commands() -> None:
    stdout = io.StringIO()
    status = run_cli(["list-tools"], stdout=stdout)
    assert status == 0
    output = stdout.getvalue()
    assert "find-symbol" in output
    assert "atlas-report" in output


def test_pa019_find_symbol_outputs_json_report() -> None:
    project_root = _make_project()
    stdout = io.StringIO()
    stderr = io.StringIO()
    status = run_cli(
        [
            "find-symbol",
            "--root",
            str(project_root),
            "--symbol",
            "build_panel",
            "--exact",
            "--format",
            "json",
        ],
        stdout=stdout,
        stderr=stderr,
    )
    assert status == 0, stderr.getvalue()
    data = json.loads(stdout.getvalue())
    assert data["report_type"] == "reasoner_symbol_atlas"
    assert "Existing code finder" in data["summary"]
    assert data["symbol_count"] >= 1


def test_pa019_evidence_freshness_outputs_missing_evidence_json() -> None:
    project_root = _make_project()
    stdout = io.StringIO()
    status = run_cli(
        [
            "evidence-freshness",
            "--root",
            str(project_root),
            "--format",
            "json",
        ],
        stdout=stdout,
    )
    assert status == 0
    data = json.loads(stdout.getvalue())
    assert data["report_type"] == "reasoner_symbol_atlas"
    assert "Evidence freshness" in data["summary"]


def test_pa019_atlas_report_writes_reports() -> None:
    project_root = _make_project()
    output_dir = project_root / "atlas_reports"
    stdout = io.StringIO()
    status = run_cli(
        [
            "atlas-report",
            "--root",
            str(project_root),
            "--symbol",
            "build_panel",
            "--output-dir",
            str(output_dir),
            "--format",
            "json",
        ],
        stdout=stdout,
    )
    assert status == 0
    data = json.loads(stdout.getvalue())
    assert data["status"] == "written"
    assert data["written_report_count"] >= 1
    assert list(output_dir.glob("*.json"))
    assert list(output_dir.glob("*.md"))


def main() -> int:
    test_pa019_command_catalog_includes_atlas_commands()
    test_pa019_list_tools_outputs_atlas_commands()
    test_pa019_find_symbol_outputs_json_report()
    test_pa019_evidence_freshness_outputs_missing_evidence_json()
    test_pa019_atlas_report_writes_reports()
    print("PA019 Project Symbol Atlas CLI integration tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
