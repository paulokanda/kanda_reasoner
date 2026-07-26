"""Validation for Project Intelligence Symbol Indexer v1."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_intelligence.models import ADVISORY_SOURCE_TRUTH_WARNING
from kanda_reasoner_app.project_intelligence.symbol_indexer import ProjectSymbolIndexer


SAMPLE_MODULE = 'import os\nimport sys as system_module\nfrom pathlib import Path\nfrom collections import defaultdict as dd\n\n\ndef documented_function(value):\n    """Return the input value."""\n    return value\n\n\ndef undocumented_function(flag):\n    def nested_helper(item):\n        return item\n    return nested_helper(flag)\n\n\nasync def async_worker():\n    """Run async work."""\n    return "ok"\n\n\nclass Example:\n    """Example class."""\n\n    def method_one(self):\n        return Path("x")\n\n    async def method_two(self):\n        return dd\n'


BAD_SYNTAX = "def broken(:\n    pass\n"
IGNORED_MODULE = "def ignored_symbol():\n    return 'ignore'\n"


def _write_fixture(root: Path) -> None:
    (root / "sample_module.py").write_text(SAMPLE_MODULE, encoding="utf-8")
    (root / "bad_syntax.py").write_text(BAD_SYNTAX, encoding="utf-8")
    (root / "__pycache__").mkdir()
    (root / "__pycache__" / "ignored.py").write_text(IGNORED_MODULE, encoding="utf-8")
    (root / ".venv").mkdir()
    (root / ".venv" / "ignored.py").write_text(IGNORED_MODULE, encoding="utf-8")


def _snapshot(root: Path) -> set[str]:
    return {item.relative_to(root).as_posix() for item in root.rglob("*")}


def _symbols_by_name(result):
    mapping = {}
    for symbol in result.symbols:
        mapping.setdefault(symbol.name, []).append(symbol)
    return mapping


def _assert_symbol(result, name: str, symbol_type: str) -> None:
    for symbol in result.symbols:
        if symbol.name == name and symbol.symbol_type == symbol_type:
            return
    raise AssertionError("Missing symbol: " + name + " type=" + symbol_type)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_symbol_indexer_") as temp_dir:
        fixture_root = Path(temp_dir)
        _write_fixture(fixture_root)
        before = _snapshot(fixture_root)

        indexer = ProjectSymbolIndexer()
        result = indexer.run_scan(fixture_root)
        after = _snapshot(fixture_root)

        if before != after:
            raise AssertionError("Symbol Indexer wrote files into the target project root.")

        _assert_symbol(result, "documented_function", "function")
        _assert_symbol(result, "undocumented_function", "function")
        _assert_symbol(result, "nested_helper", "nested_function")
        _assert_symbol(result, "async_worker", "async_function")
        _assert_symbol(result, "Example", "class")
        _assert_symbol(result, "method_one", "method")
        _assert_symbol(result, "method_two", "async_method")

        symbols = _symbols_by_name(result)
        if not symbols["documented_function"][0].has_docstring:
            raise AssertionError("Expected documented_function to have a docstring.")
        if symbols["undocumented_function"][0].has_docstring:
            raise AssertionError("Expected undocumented_function to have no docstring.")
        if "ignored_symbol" in symbols:
            raise AssertionError("Excluded folders were scanned unexpectedly.")

        import_pairs = {(item.module, item.imported_name, item.import_type) for item in result.imports}
        expected_imports = {
            ("os", "os", "import"),
            ("sys", "system_module", "import"),
            ("pathlib", "Path", "from_import"),
            ("collections", "dd", "from_import"),
        }
        missing_imports = expected_imports - import_pairs
        if missing_imports:
            raise AssertionError("Missing imports: " + repr(sorted(missing_imports)))

        syntax_files = [item for item in result.files if item.syntax_error]
        if len(syntax_files) != 1:
            raise AssertionError("Expected exactly one syntax-error file.")
        if not result.report.warnings:
            raise AssertionError("Expected syntax error to produce a warning.")

        json_text = json.dumps(result.to_dict(), ensure_ascii=True, sort_keys=True)
        if "sample_module.py" not in json_text:
            raise AssertionError("JSON serialization did not include expected file evidence.")

        markdown = indexer.to_markdown(result)
        if ADVISORY_SOURCE_TRUTH_WARNING not in markdown:
            raise AssertionError("Markdown report is missing advisory source-truth warning.")
        if "Project Intelligence Symbol Indexer" not in markdown:
            raise AssertionError("Markdown report is missing engine name.")

    print("VALIDATION OK: project-intelligence-symbol-indexer-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
