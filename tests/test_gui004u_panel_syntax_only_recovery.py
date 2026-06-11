"""GUI004U syntax-only recovery smoke test."""

from __future__ import annotations

import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"


def test_gui004u_panel_py_compile() -> None:
    py_compile.compile(str(PANEL), doraise=True)


def main() -> None:
    test_gui004u_panel_py_compile()
    print("GUI004U panel syntax-only recovery test passed.")


if __name__ == "__main__":
    main()
