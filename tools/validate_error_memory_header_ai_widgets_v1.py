# project-path: tools/validate_error_memory_header_ai_widgets_v1.py
"""Validate that Error Memory uses in-tab modes, not header AI configuration."""

from __future__ import annotations

import ast
from pathlib import Path

FEATURE_ID = "error-memory-header-ai-widgets-v1-centralized"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAZY_TABS = PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"
ERROR_MEMORY_TAB = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
MODE_RUNTIME = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/_ai_mode_runtime.py"
MAX_MODULE_LINES = 500


def _read(path: Path) -> str:
    if not path.exists():
        raise AssertionError("Missing expected file: " + str(path))
    return path.read_text(encoding="utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    for path in (LAZY_TABS, ERROR_MEMORY_TAB, MODE_RUNTIME, Path(__file__).resolve()):
        text = _read(path)
        ast.parse(text, filename=str(path))
        _require(len(text.splitlines()) <= MAX_MODULE_LINES, str(path) + " exceeds 500 lines")
    lazy = _read(LAZY_TABS)
    ai_sources = lazy.split("if spec.source_hint in {", 1)[1].split("}:", 1)[0]
    _require(
        "_ERROR_MEMORY_GUI_SOURCE" not in ai_sources,
        "Error Memory still receives the standard header model configuration.",
    )
    tab = _read(ERROR_MEMORY_TAB)
    mode = _read(MODE_RUNTIME)
    _require("preview_layout.addWidget(_ai_mode_runtime.build_mode_group(self))" in tab, "Mode group is not in the Error Memory body.")
    for marker in ("Heuristic", "Local AI", "Web AI"):
        _require(marker in mode, "Missing Error Memory mode: " + marker)
    _require("Open Config Web AI" not in tab, "Error Memory should expose only modes, not another configuration panel.")
    print("ERROR_MEMORY_HEADER_MODEL_CONFIG_REMOVED: PASS")
    print("ERROR_MEMORY_BODY_MODE_SELECTOR_PRESENT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
