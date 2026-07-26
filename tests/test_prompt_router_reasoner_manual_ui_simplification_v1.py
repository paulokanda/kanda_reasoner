"""Regression tests for Prompt Router Reasoner Manual UI Simplification v1.

These tests intentionally inspect source text and compile the module so they do
not require a running Qt display in CI. Local GUI smoke testing happens by
opening the tab and checking the visible widgets.
"""

from __future__ import annotations

from pathlib import Path
import py_compile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "prompt_router_reasoner_gui" / "prompt_router_reasoner_tab.py"


def read_tab_source() -> str:
    return TAB_PATH.read_text(encoding="utf-8")


def test_manual_ui_simplification_removed_old_visible_groups() -> None:
    source = read_tab_source()
    removed_visible_titles = [
        'QGroupBox("Global router mode")',
        'QGroupBox("Generator text review queue")',
        'QGroupBox("Heuristic default selected prompt")',
        'QGroupBox("ML selected prompt',
    ]
    for text in removed_visible_titles:
        assert text not in source
    assert "has_three_columns=False" in source
    assert "has_review_controls=False" in source
    assert "has_ask_ai_button=False" in source
    assert "has_readiness_bars=False" in source


def test_manual_ui_has_two_editor_workflow_and_buttons() -> None:
    source = read_tab_source()
    required = [
        "manual_router_choice_code_editor",
        "manual_router_final_prompt_editor",
        "paste_router_choice_code_button",
        "clear_router_choice_code_button",
        "undo_router_choice_code_button",
        "edit_final_prompt_button",
        "save_final_prompt_edit_button",
        "clear_final_prompt_button",
        "undo_final_prompt_edit_button",
        "copy_manual_router_final_prompt_button",
        "_auto_load_manual_router_choice_from_editor",
        "capture_manual_router_choice",
    ]
    for token in required:
        assert token in source


def test_manual_ui_keeps_ml_sleeping_and_metric_excluded() -> None:
    source = read_tab_source()
    assert "ML remains sleeping" in source
    assert "metric_excluded" in source
    assert "MANUAL_ROUTER_CHOICE_MODE" in source
    assert "manual_router_choice_capture" in source


def test_prompt_router_reasoner_tab_compiles() -> None:
    py_compile.compile(str(TAB_PATH), doraise=True)

if __name__ == "__main__":
    test_manual_ui_simplification_removed_old_visible_groups()
    test_manual_ui_has_two_editor_workflow_and_buttons()
    test_manual_ui_keeps_ml_sleeping_and_metric_excluded()
    test_prompt_router_reasoner_tab_compiles()
    print("VALIDATION OK: prompt_router_reasoner_manual_ui_simplification_v1")
