from __future__ import annotations

import importlib
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_symbol_atlas.symbol_indexer as symbol_indexer
from kanda_reasoner_app.reasoner_symbol_atlas import (
    ProjectSymbolAtlasSymbolIndexOptions,
    build_reasoner_symbol_atlas_symbol_report,
    collect_reasoner_symbol_atlas_symbols,
    index_reasoner_symbol_atlas_modules,
)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _symbol_names(symbols: tuple[object, ...]) -> list[str]:
    return sorted(getattr(symbol, "name") for symbol in symbols)


def test_symbol_indexer_public_contract() -> None:
    assert "ProjectSymbolAtlasSymbolIndexOptions" in symbol_indexer.__all__
    assert "collect_reasoner_symbol_atlas_symbols" in symbol_indexer.__all__
    assert "index_reasoner_symbol_atlas_modules" in symbol_indexer.__all__
    assert "build_reasoner_symbol_atlas_symbol_report" in symbol_indexer.__all__
    assert not hasattr(symbol_indexer, "DEFAULT_PROJECT_ROOT")
    assert not hasattr(symbol_indexer, "VALID_REPORT_TYPES")


def test_collects_public_symbols_without_importing_project_code() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_text(root / "pkg" / "__init__.py", "\n")
        _write_text(
            root / "pkg" / "service.py",
            "from dataclasses import dataclass\n"
            "__all__ = ['PUBLIC_CONSTANT', 'EXPORTED_ALIAS', 'DataModel']\n"
            "PUBLIC_CONSTANT = 1\n"
            "EXPORTED_ALIAS = object()\n"
            "local_value = 2\n"
            "def public_function():\n"
            "    return PUBLIC_CONSTANT\n"
            "def _private_function():\n"
            "    return local_value\n"
            "class Service:\n"
            "    pass\n"
            "@dataclass\n"
            "class DataModel:\n"
            "    value: int\n"
            "raise RuntimeError('must not import during atlas scan')\n",
        )

        symbols = collect_reasoner_symbol_atlas_symbols(root)
        names = _symbol_names(symbols)

        assert names == [
            "DataModel",
            "EXPORTED_ALIAS",
            "PUBLIC_CONSTANT",
            "Service",
            "public_function",
        ]
        assert all(str(root) not in symbol.path for symbol in symbols)
        exported = {symbol.name: symbol.exported_by_all for symbol in symbols}
        assert exported["PUBLIC_CONSTANT"] is True
        assert exported["EXPORTED_ALIAS"] is True
        assert exported["DataModel"] is True
        kinds = {symbol.name: symbol.kind for symbol in symbols}
        assert kinds["DataModel"] == "dataclass"
        assert kinds["Service"] == "class"
        assert kinds["public_function"] == "function"
        assert kinds["PUBLIC_CONSTANT"] == "constant"
        assert "_private_function" not in names
        assert "local_value" not in names


def test_include_private_option_collects_private_definitions() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_text(
            root / "pkg" / "service.py",
            "def _private_function():\n"
            "    return 1\n"
            "class _PrivateClass:\n"
            "    pass\n",
        )

        symbols = collect_reasoner_symbol_atlas_symbols(
            root,
            options=ProjectSymbolAtlasSymbolIndexOptions(include_private=True),
        )
        names = _symbol_names(symbols)

        assert names == ["_PrivateClass", "_private_function"]
        assert all(symbol.is_public is False for symbol in symbols)


def test_indexed_modules_preserve_module_records_and_parse_errors() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_text(root / "pkg" / "good.py", "VALUE = 1\n")
        _write_text(root / "pkg" / "bad.py", "def broken(:\n    pass\n")

        modules = index_reasoner_symbol_atlas_modules(root)
        by_module = {module.module: module for module in modules}

        assert by_module["pkg.good"].symbols[0].name == "VALUE"
        assert by_module["pkg.bad"].symbols == tuple()
        assert any(
            "syntax_error_line" in evidence for evidence in by_module["pkg.bad"].evidence
        )


def test_builds_symbol_report_with_dynamic_project_root() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_text(root / "pkg" / "service.py", "def public_function():\n    return 1\n")

        report = build_reasoner_symbol_atlas_symbol_report(root)
        payload = report.to_dict()

        assert payload["report_type"] == "reasoner_symbol_atlas"
        assert payload["module_count"] == 1
        assert payload["symbol_count"] == 1
        assert payload["symbols"][0]["name"] == "public_function"
        assert str(root) == payload["project_root"]
        assert "reasoner_symbol_atlas.symbol_indexer" in payload["input_sources"]
        assert "symbols=1" in payload["summary"]


def test_public_contract_exports_are_directly_importable() -> None:
    package = importlib.import_module("kanda_reasoner_app.reasoner_symbol_atlas")

    for name in symbol_indexer.__all__:
        assert hasattr(symbol_indexer, name), name
        assert hasattr(package, name), name


if __name__ == "__main__":
    test_symbol_indexer_public_contract()
    test_collects_public_symbols_without_importing_project_code()
    test_include_private_option_collects_private_definitions()
    test_indexed_modules_preserve_module_records_and_parse_errors()
    test_builds_symbol_report_with_dynamic_project_root()
    test_public_contract_exports_are_directly_importable()
    print("PA003 Project Symbol Atlas public symbol indexer tests passed.")
