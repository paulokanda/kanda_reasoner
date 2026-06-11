"""Focused PA015E test for related file finder helper reachability."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_symbol_atlas._related_file_finder_support as support
import kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder as finder


IMPORT_LINE = (
    "import kanda_reasoner_app.reasoner_symbol_atlas."
    "_related_file_finder_support as _related_file_finder_support"
)


def test_pa015e_support_module_has_private_contract() -> None:
    assert getattr(support, "__all__", []) == []


def test_pa015e_related_file_finder_has_static_production_import() -> None:
    target = (
        PROJECT_ROOT
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_symbol_atlas"
        / "related_file_finder.py"
    )
    text = target.read_text(encoding="utf-8")
    assert IMPORT_LINE in text


def test_pa015e_public_module_still_imports() -> None:
    assert finder.__name__.endswith("related_file_finder")


def main() -> int:
    test_pa015e_support_module_has_private_contract()
    test_pa015e_related_file_finder_has_static_production_import()
    test_pa015e_public_module_still_imports()
    print("PA015E Related file finder support production import tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
