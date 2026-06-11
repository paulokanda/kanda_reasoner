"""PA015D reachability contract for the related-file private support module."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas import (  # noqa: E402
    _related_file_finder_support as support,
)


def test_pa015d_support_module_has_private_contract() -> None:
    """The private support module is intentionally reachable and tested."""
    assert support.__name__.endswith("._related_file_finder_support")
    assert getattr(support, "__all__", []) == []


def main() -> int:
    test_pa015d_support_module_has_private_contract()
    print("PA015D Related file finder support static import tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
