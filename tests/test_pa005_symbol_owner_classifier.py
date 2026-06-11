"""Focused tests for PA005 Project Symbol Atlas owner classification."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.owner_classifier import (  # noqa: E402
    ProjectSymbolAtlasOwnerClassifyOptions,
    build_reasoner_symbol_atlas_owner_report,
    classify_reasoner_symbol_atlas_owners,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _records_by_path(records):
    return {record.path.replace("\\", "/"): record for record in records}


def test_owner_classifier_marks_facades_helpers_tests_and_owners() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(
            root / "pkg" / "__init__.py",
            "from .core import public_api\n__all__ = ['public_api']\n",
        )
        _write(
            root / "pkg" / "core.py",
            "VALUE = 1\n\ndef public_api():\n    return VALUE\n",
        )
        _write(
            root / "pkg" / "helpers.py",
            "def make_helper():\n    return 'helper'\n",
        )
        _write(
            root / "pkg" / "compat_layer.py",
            "def __getattr__(name):\n    raise AttributeError(name)\n",
        )
        _write(
            root / "tests" / "test_core.py",
            "from pkg.core import public_api\n\ndef test_public_api():\n    assert public_api() == 1\n",
        )

        records = classify_reasoner_symbol_atlas_owners(
            root,
            ProjectSymbolAtlasOwnerClassifyOptions(include_tests=True),
        )
        by_path = _records_by_path(records)

        assert by_path["pkg/__init__.py"].owner_role == "facade"
        assert by_path["pkg/core.py"].owner_role == "canonical_owner"
        assert by_path["pkg/helpers.py"].owner_role == "private_helper"
        assert by_path["pkg/compat_layer.py"].owner_role == "compatibility_facade"
        assert by_path["tests/test_core.py"].owner_role == "test_only"

        core_symbols = {symbol.name: symbol for symbol in by_path["pkg/core.py"].symbols}
        assert core_symbols["public_api"].owner_role == "canonical_owner"
        assert core_symbols["VALUE"].owner_role == "canonical_owner"

        init_symbols = {symbol.name: symbol for symbol in by_path["pkg/__init__.py"].symbols}
        assert init_symbols["public_api"].kind == "import"
        assert init_symbols["public_api"].owner_role == "facade"


def test_owner_classifier_builds_owner_map_report() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(root / "app.py", "def run_app():\n    return True\n")

        report = build_reasoner_symbol_atlas_owner_report(root)
        payload = report.to_dict()

        assert payload["report_type"] == "owner_map"
        assert payload["module_count"] == 1
        assert payload["symbol_count"] == 1
        assert "reasoner_symbol_atlas.owner_classifier" in payload["input_sources"]
        assert "canonical_owner=1" in payload["summary"]


if __name__ == "__main__":
    test_owner_classifier_marks_facades_helpers_tests_and_owners()
    test_owner_classifier_builds_owner_map_report()
    print("PA005 Project Symbol Atlas owner classifier tests passed.")
