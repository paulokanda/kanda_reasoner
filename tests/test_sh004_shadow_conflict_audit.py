from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.source_hygiene.shadow_audit as shadow_audit
from kanda_reasoner_app.source_hygiene.shadow_audit import (
    ShadowAuditFileSummary,
    audit_project_for_shadow_conflicts,
    audit_python_file_for_shadow_conflicts,
    iter_shadow_audit_files,
)


def test_shadow_audit_exports_public_contract() -> None:
    expected = {
        "ShadowAuditFileSummary",
        "audit_project_for_shadow_conflicts",
        "audit_python_file_for_shadow_conflicts",
        "iter_shadow_audit_files",
    }
    assert expected.issubset(set(shadow_audit.__all__))


def test_shadow_audit_reports_facade_and_symbol_risks(tmp_path: Path) -> None:
    package_dir = tmp_path / "sample_pkg"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text(
        "from .module_a import *\n"
        "__all__ = ['missing_name']\n"
        "print('runtime side effect')\n",
        encoding="utf-8",
    )
    (package_dir / "module_a.py").write_text(
        "def duplicate_symbol():\n"
        "    return 'a'\n",
        encoding="utf-8",
    )
    (package_dir / "module_b.py").write_text(
        "def duplicate_symbol():\n"
        "    return 'b'\n",
        encoding="utf-8",
    )
    ignored_dir = tmp_path / "__pycache__"
    ignored_dir.mkdir()
    (ignored_dir / "ignored.py").write_text("def hidden():\n    return 1\n", encoding="utf-8")

    files = iter_shadow_audit_files(tmp_path)
    assert all("__pycache__" not in str(path) for path in files)

    summary = audit_python_file_for_shadow_conflicts(package_dir / "__init__.py", tmp_path)
    assert isinstance(summary, ShadowAuditFileSummary)
    codes = {finding.code for finding in summary.findings}
    assert "WILDCARD_IMPORT_IN_FACADE" in codes
    assert "UNBOUND_ALL_EXPORT" in codes
    assert "RUNTIME_LOGIC_IN_FACADE" in codes

    report = audit_project_for_shadow_conflicts(tmp_path)
    assert report.report_type == "shadow_conflict_audit"
    report_codes = {finding.code for finding in report.findings}
    assert "DUPLICATE_PUBLIC_SYMBOL" in report_codes


def main() -> int:
    test_shadow_audit_exports_public_contract()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        test_shadow_audit_reports_facade_and_symbol_risks(Path(tmp))
    print("SH004 shadow conflict audit tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
