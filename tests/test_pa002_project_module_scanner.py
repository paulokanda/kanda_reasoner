from __future__ import annotations

import importlib
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_symbol_atlas.module_scanner as module_scanner
from kanda_reasoner_app.reasoner_symbol_atlas import (
    ProjectSymbolAtlasModuleScanOptions,
    build_reasoner_symbol_atlas_module_report,
    collect_reasoner_symbol_atlas_modules,
    reasoner_symbol_atlas_module_name_for_path,
)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _module_names(records: tuple[object, ...]) -> list[str]:
    return sorted(getattr(record, "module") for record in records)


def test_module_scanner_public_contract() -> None:
    assert "ProjectSymbolAtlasModuleScanOptions" in module_scanner.__all__
    assert "collect_reasoner_symbol_atlas_modules" in module_scanner.__all__
    assert "build_reasoner_symbol_atlas_module_report" in module_scanner.__all__
    assert not hasattr(module_scanner, "DEFAULT_PROJECT_ROOT")
    assert not hasattr(module_scanner, "VALID_REPORT_TYPES")


def test_collects_modules_without_hardcoded_project_root() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_text(root / "pkg" / "__init__.py", "\n")
        _write_text(root / "pkg" / "service.py", "VALUE = 1\n\n")
        _write_text(root / "tests" / "test_service.py", "def test_smoke():\n    assert True\n")
        _write_text(root / "workbench" / "_bundle_temp" / "stale.py", "VALUE = 2\n")
        _write_text(root / "_tmp_sh006_a" / "tmp.py", "VALUE = 3\n")

        records = collect_reasoner_symbol_atlas_modules(root)
        names = _module_names(records)

        assert names == ["pkg", "pkg.service", "tests.test_service"]
        assert all(str(root) not in record.path for record in records)
        service = next(record for record in records if record.module == "pkg.service")
        assert service.line_count == 2
        assert service.owner_role == "unknown"
        test_record = next(record for record in records if record.module == "tests.test_service")
        assert test_record.is_test_file is True
        assert test_record.owner_role == "test_only"
        assert "workbench._bundle_temp.stale" not in names
        assert "_tmp_sh006_a.tmp" not in names


def test_scanner_options_can_exclude_tests_and_include_workbench() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_text(root / "pkg" / "service.py", "VALUE = 1\n")
        _write_text(root / "tests" / "test_service.py", "def test_smoke():\n    assert True\n")
        _write_text(root / "workbench" / "report_tool.py", "VALUE = 2\n")

        no_tests = collect_reasoner_symbol_atlas_modules(
            root,
            options=ProjectSymbolAtlasModuleScanOptions(include_tests=False),
        )
        assert _module_names(no_tests) == ["pkg.service"]

        with_workbench = collect_reasoner_symbol_atlas_modules(
            root,
            options=ProjectSymbolAtlasModuleScanOptions(include_workbench=True),
        )
        assert _module_names(with_workbench) == [
            "pkg.service",
            "tests.test_service",
            "workbench.report_tool",
        ]


def test_module_name_for_path_handles_init_files() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        init_path = root / "pkg" / "__init__.py"
        service_path = root / "pkg" / "service.py"
        _write_text(init_path, "\n")
        _write_text(service_path, "VALUE = 1\n")

        assert reasoner_symbol_atlas_module_name_for_path(root, init_path) == "pkg"
        assert reasoner_symbol_atlas_module_name_for_path(root, service_path) == "pkg.service"


def test_builds_module_report() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_text(root / "pkg" / "service.py", "VALUE = 1\n")

        report = build_reasoner_symbol_atlas_module_report(root)
        payload = report.to_dict()

        assert payload["report_type"] == "reasoner_symbol_atlas"
        assert payload["module_count"] == 1
        assert payload["modules"][0]["module"] == "pkg.service"
        assert "modules=1" in payload["summary"]
        assert payload["input_sources"] == ["reasoner_symbol_atlas.module_scanner"]


def test_public_contract_exports_are_directly_importable() -> None:
    package = importlib.import_module("kanda_reasoner_app.reasoner_symbol_atlas")

    for name in package.__all__:
        assert hasattr(package, name), name

    for name in module_scanner.__all__:
        assert hasattr(module_scanner, name), name


if __name__ == "__main__":
    test_module_scanner_public_contract()
    test_collects_modules_without_hardcoded_project_root()
    test_scanner_options_can_exclude_tests_and_include_workbench()
    test_module_name_for_path_handles_init_files()
    test_builds_module_report()
    test_public_contract_exports_are_directly_importable()
    print("PA002 Project Symbol Atlas module scanner tests passed.")
