"""Focused regression test for PA015G public API expectation repair."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_pa015g_related_file_finder_public_api_name() -> None:
    """The public API uses the Project Symbol Atlas naming convention."""

    from kanda_reasoner_app.reasoner_symbol_atlas import related_file_finder

    assert hasattr(related_file_finder, "find_reasoner_symbol_atlas_related_files")
    assert hasattr(related_file_finder, "build_reasoner_symbol_atlas_related_file_report")
    assert not hasattr(related_file_finder, "find_related_files")


def main() -> int:
    test_pa015g_related_file_finder_public_api_name()
    print("PA015G Related file finder public API test repair passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
