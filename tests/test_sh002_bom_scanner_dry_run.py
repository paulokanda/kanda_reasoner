from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.source_hygiene.bom_scanner import (  # noqa: E402
    UTF8_BOM_BYTES,
    iter_bom_scan_files,
    scan_file_for_bom,
    scan_project_for_bom,
)


def test_scan_file_for_bom_reports_utf8_bom() -> None:
    temp_dir = Path(tempfile.mkdtemp(prefix="sh002_bom_file_"))
    try:
        target = temp_dir / "module.py"
        target.write_bytes(UTF8_BOM_BYTES + b'print("hello")\n')

        findings = scan_file_for_bom(target, project_root=temp_dir)
        codes = {finding.code for finding in findings}

        assert "UTF8_BOM_DETECTED" in codes
        assert all(finding.path == "module.py" for finding in findings)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_scan_project_for_bom_is_dry_run_and_structured() -> None:
    temp_dir = Path(tempfile.mkdtemp(prefix="sh002_bom_project_"))
    try:
        clean_file = temp_dir / "clean.py"
        bom_file = temp_dir / "with_bom.json"
        ignored_file = temp_dir / "binary.bin"
        cache_dir = temp_dir / "__pycache__"
        skipped_file = cache_dir / "cached.py"

        cache_dir.mkdir()
        clean_file.write_text('print("clean")\n', encoding="utf-8")
        bom_file.write_bytes(UTF8_BOM_BYTES + b'{"value": 1}\n')
        ignored_file.write_bytes(b"\x00\x01\x02")
        skipped_file.write_bytes(UTF8_BOM_BYTES + b'print("skip")\n')

        files = iter_bom_scan_files(temp_dir)
        assert clean_file in files
        assert bom_file in files
        assert ignored_file not in files
        assert skipped_file not in files

        report = scan_project_for_bom(temp_dir)
        data = report.to_dict()
        findings = data["findings"]

        assert data["report_type"] == "bom_scan"
        assert data["finding_count"] == 1
        assert findings[0]["code"] == "UTF8_BOM_DETECTED"
        assert findings[0]["path"] == "with_bom.json"
        json.dumps(data, sort_keys=True)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_scan_project_for_bom_reports_utf8_decode_error() -> None:
    temp_dir = Path(tempfile.mkdtemp(prefix="sh002_decode_"))
    try:
        target = temp_dir / "latin.txt"
        target.write_bytes(b"caf\xe9\n")

        report = scan_project_for_bom(temp_dir)
        codes = {finding.code for finding in report.findings}

        assert "UTF8_DECODE_ERROR" in codes
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    test_scan_file_for_bom_reports_utf8_bom()
    test_scan_project_for_bom_is_dry_run_and_structured()
    test_scan_project_for_bom_reports_utf8_decode_error()
    print("SH002 BOM scanner dry-run tests passed.")
