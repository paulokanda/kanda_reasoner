"""Ensure Tab 3 runtime code does not target the old reasoner_tools_gui package path."""

from __future__ import annotations

from pathlib import Path


RUNTIME_ROOTS = [
    Path('ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help'),
    Path('ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime'),
]


def test_tab3_runtime_sources_do_not_reference_stale_runtime_package() -> None:
    stale = "reasoner_tools_gui.tab3_manual_review_runtime"
    offenders: list[str] = []
    for root in RUNTIME_ROOTS:
        for path in root.glob("*.py"):
            if stale in path.read_text(encoding="utf-8"):
                offenders.append(str(path))

    assert offenders == []


if __name__ == "__main__":
    test_tab3_runtime_sources_do_not_reference_stale_runtime_package()
    print("Tab 3 stale runtime path tests passed.")
