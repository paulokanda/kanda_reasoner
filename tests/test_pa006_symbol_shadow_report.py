"""Focused tests for PA006 Project Symbol Atlas shadow report."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.shadow_report import (  # noqa: E402
    ProjectSymbolAtlasShadowReportOptions,
    build_reasoner_symbol_atlas_shadow_report,
    collect_reasoner_symbol_atlas_shadow_findings,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_pa006_detects_duplicate_public_definitions() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(root / "pkg" / "__init__.py", "")
        _write(
            root / "pkg" / "alpha.py",
            "def shared_name():\n"
            "    return 'alpha'\n",
        )
        _write(
            root / "pkg" / "beta.py",
            "def shared_name():\n"
            "    return 'beta'\n",
        )
        findings = collect_reasoner_symbol_atlas_shadow_findings(root)
        names = {finding.name for finding in findings}
        assert "shared_name" in names
        shared = next(finding for finding in findings if finding.name == "shared_name")
        assert shared.owner_role == "ambiguous_owner"
        assert any("duplicate_public_symbol_count: 2" in item for item in shared.evidence)


def test_pa006_report_is_read_only_and_dynamic_root() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(root / "app" / "__init__.py", "")
        _write(root / "app" / "owner.py", "class ExistingCodeFinder:\n    pass\n")
        _write(root / "app" / "other.py", "class ExistingCodeFinder:\n    pass\n")
        report = build_reasoner_symbol_atlas_shadow_report(
            root,
            options=ProjectSymbolAtlasShadowReportOptions(include_tests=False),
        )
        payload = report.to_dict()
        assert payload["project_root"] == str(root.resolve())
        assert payload["report_type"] == "reasoner_symbol_atlas"
        assert payload["symbol_count"] == 1
        assert payload["module_count"] == 2
        assert "findings=1" in payload["summary"]
        assert "E:\\developer_tools" not in str(payload)


def main() -> None:
    test_pa006_detects_duplicate_public_definitions()
    test_pa006_report_is_read_only_and_dynamic_root()
    print("PA006 Project Symbol Atlas shadow report tests passed.")


if __name__ == "__main__":
    main()
