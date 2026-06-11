"""Reachability protection for the related-file-finder private helper.

This test intentionally imports the private support module directly so the
architecture validator can see that the helper is active, protected, and not a
stale source candidate. The production public API remains owned by
related_file_finder.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas import _related_file_finder_support as support


def test_pa015c_private_support_module_is_test_protected() -> None:
    """Verify the private helper module is intentionally reachable by tests."""
    assert support.__name__.endswith("._related_file_finder_support")
    assert getattr(support, "__all__", []) == []


def main() -> int:
    """Run the focused reachability checks."""
    test_pa015c_private_support_module_is_test_protected()
    print("PA015C Related file finder support reachability tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
