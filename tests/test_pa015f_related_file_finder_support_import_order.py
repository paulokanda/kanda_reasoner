"""Focused test for PA015F support import-order repair."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SUPPORT_IMPORTS = {
    "import kanda_reasoner_app.reasoner_symbol_atlas._related_file_finder_support as _related_file_finder_support",
    "from . import _related_file_finder_support as _related_support",
}

PUBLIC_RELATED_FILE_FINDER_NAME = "find_reasoner_symbol_atlas_related_files"


def test_pa015f_support_import_order_is_valid() -> None:
    """Ensure support imports never appear before __future__."""

    target = (
        PROJECT_ROOT
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_symbol_atlas"
        / "related_file_finder.py"
    )
    text = target.read_text(encoding="utf-8")
    lines = text.splitlines()

    future_indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip() == "from __future__ import annotations"
    ]
    support_indexes = [
        index for index, line in enumerate(lines) if line.strip() in SUPPORT_IMPORTS
    ]

    assert len(future_indexes) == 1
    assert support_indexes
    assert all(future_indexes[0] < index for index in support_indexes)


def test_pa015f_modules_import_cleanly() -> None:
    """Ensure private support and public related finder import cleanly."""

    import kanda_reasoner_app.reasoner_symbol_atlas._related_file_finder_support as support
    import kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder as finder

    assert getattr(support, "__all__", None) == []
    assert hasattr(finder, PUBLIC_RELATED_FILE_FINDER_NAME)
    assert not hasattr(finder, "find_related_files")


def main() -> int:
    test_pa015f_support_import_order_is_valid()
    test_pa015f_modules_import_cleanly()
    print("PA015F Related file finder support import-order tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
