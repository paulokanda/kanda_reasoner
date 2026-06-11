"""PA021 patch script contract tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCRIPT_PATH = (
    ROOT
    / "workbench"
    / "_bundle_temp"
    / "PA021_APPLY_PROJECT_SYMBOL_ATLAS_GUI_INTEGRATION.py"
)


def test_pa021_patch_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_pa021_patch_script_contains_markers() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "PA021_PROJECT_SYMBOL_ATLAS_GUI_TOOLS" in text
    assert "PA021_PROJECT_SYMBOL_ATLAS_GUI_COMMANDS" in text
    assert "from __future__ import annotations" in text


def main() -> int:
    test_pa021_patch_script_exists()
    test_pa021_patch_script_contains_markers()
    print("PA021 Project Symbol Atlas GUI patch script contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
