"""Focused tests for PA004 Project Symbol Atlas import/facade analysis."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.import_analyzer import (  # noqa: E402
    ProjectSymbolAtlasImportAnalysisOptions,
    analyze_reasoner_symbol_atlas_imports,
    build_reasoner_symbol_atlas_import_report,
    collect_reasoner_symbol_atlas_imports,
)


def _write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_pa004_detects_imports_reexports_and_facade_evidence() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_file(
            root / "pkg" / "__init__.py",
            '\n'.join(
                [
                    'from .core import Widget as Widget',
                    'from .helpers import *',
                    '__all__ = ["Widget", "helper_func"]',
                    'def __getattr__(name):',
                    '    raise AttributeError(name)',
                    '',
                ]
            ),
        )
        _write_file(
            root / "pkg" / "core.py",
            '\n'.join(
                [
                    'class Widget:',
                    '    pass',
                    '',
                    'def make_widget():',
                    '    return Widget()',
                    '',
                ]
            ),
        )
        _write_file(
            root / "pkg" / "helpers.py", 'def helper_func():\n    return "ok"\n')
        _write_file(
            root / "pkg" / "compat_facade.py",
            '\n'.join(
                [
                    'from pkg.core import Widget',
                    '__all__ = ["Widget"]',
                    '',
                ]
            ),
        )

        modules = analyze_reasoner_symbol_atlas_imports(
            root,
            options=ProjectSymbolAtlasImportAnalysisOptions(),
        )
        by_module = {record.module: record for record in modules}

        package_record = by_module["pkg"]
        assert "from .core import Widget as Widget" in package_record.imports
        assert "from .helpers import *" in package_record.imports
        assert package_record.owner_role == "compatibility_facade"
        assert any("wildcard_import_detected: true" == item for item in package_record.evidence)
        assert any(symbol.name == "Widget" for symbol in package_record.symbols)

        facade_record = by_module["pkg.compat_facade"]
        assert facade_record.owner_role == "compatibility_facade"
        assert any(symbol.name == "Widget" for symbol in facade_record.symbols)

        imports = collect_reasoner_symbol_atlas_imports(root)
        assert "from pkg.core import Widget" in imports

        report = build_reasoner_symbol_atlas_import_report(root)
        payload = report.to_dict()
        assert payload["module_count"] == 4
        assert "import/facade analysis" in payload["summary"]


def main() -> None:
    test_pa004_detects_imports_reexports_and_facade_evidence()
    print("PA004 Project Symbol Atlas import/facade analyzer tests passed.")


if __name__ == "__main__":
    main()
