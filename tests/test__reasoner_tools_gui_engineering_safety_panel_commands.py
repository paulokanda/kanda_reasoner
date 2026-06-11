"""Direct protection test for the private Engineering Safety panel command helper."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import _reasoner_tools_gui_engineering_safety_panel_commands as helper  # noqa: E402


def test_private_helper_imports_directly() -> None:
    """The private helper must remain import-safe."""
    assert hasattr(helper, "_build_cli_args")
    assert hasattr(helper, "_run_command")


def test_private_helper_exports_no_public_symbols() -> None:
    """The helper must not create public architecture ownership collisions."""
    public_names = [
        name
        for name in dir(helper)
        if not name.startswith("_") and name not in {"annotations"}
    ]
    assert public_names == []


def main() -> None:
    """Run tests without pytest."""
    test_private_helper_imports_directly()
    test_private_helper_exports_no_public_symbols()
    print("Direct private Engineering Safety panel helper tests passed.")


if __name__ == "__main__":
    main()
