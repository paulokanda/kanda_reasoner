from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.source_hygiene.bom_fixer import (  # noqa: E402
    BomFixResult,
    fix_project_utf8_bom,
    remove_utf8_bom_from_file,
    validate_text_file_after_bom_fix,
)


def test_remove_utf8_bom_from_python_file_with_backup(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    package_dir = project_root / "pkg"
    package_dir.mkdir(parents=True)
    target = package_dir / "module.py"
    target.write_bytes(b"\xef\xbb\xbfVALUE = 1\n")
    backup_root = tmp_path / "backups"

    result = remove_utf8_bom_from_file(
        target,
        project_root=project_root,
        backup_root=backup_root,
        validate=True,
    )

    assert isinstance(result, BomFixResult)
    assert result.success is True
    assert result.changed is True
    assert target.read_bytes() == b"VALUE = 1\n"
    assert Path(result.backup_path).read_bytes().startswith(b"\xef\xbb\xbf")


def test_bom_fix_rolls_back_invalid_json(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    target = project_root / "broken.json"
    original_payload = b"\xef\xbb\xbf{bad json}\n"
    target.write_bytes(original_payload)

    result = remove_utf8_bom_from_file(
        target,
        project_root=project_root,
        backup_root=tmp_path / "backups",
        validate=True,
    )

    assert result.success is False
    assert result.changed is True
    assert target.read_bytes() == original_payload
    assert Path(result.backup_path).exists()


def test_fix_project_utf8_bom_report(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    target = project_root / "data.json"
    target.write_bytes(b"\xef\xbb\xbf{\"ok\": true}\n")

    report = fix_project_utf8_bom(
        project_root,
        backup_root=tmp_path / "backups",
        validate=True,
    )

    data = report.to_dict()
    assert data["report_type"] == "bom_fix"
    assert data["finding_count"] == 1
    assert data["findings"][0]["code"] == "UTF8_BOM_REMOVED"
    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}


def test_validate_text_file_after_bom_fix_public_contract(tmp_path: Path) -> None:
    target = tmp_path / "module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    validate_text_file_after_bom_fix(target)


if __name__ == "__main__":
    import shutil

    for name, test_func in (
        ("test_tmp_sh003_one", test_remove_utf8_bom_from_python_file_with_backup),
        ("test_tmp_sh003_two", test_bom_fix_rolls_back_invalid_json),
        ("test_tmp_sh003_three", test_fix_project_utf8_bom_report),
        ("test_tmp_sh003_four", test_validate_text_file_after_bom_fix_public_contract),
    ):
        base = Path(name)
        shutil.rmtree(base, ignore_errors=True)
        base.mkdir(parents=True, exist_ok=True)
        test_func(base)
        shutil.rmtree(base, ignore_errors=True)
    print("SH003 BOM fixer with backup tests passed.")
