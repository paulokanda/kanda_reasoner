"""Focused tests for PA011 Project Symbol Atlas logic placement advisor."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.logic_placement_advisor import (
    PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW,
    PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY,
    ProjectSymbolAtlasLogicPlacementOptions,
    advise_reasoner_symbol_atlas_logic_placement,
    build_reasoner_symbol_atlas_logic_placement_report,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _make_project() -> tempfile.TemporaryDirectory[str]:
    temp = tempfile.TemporaryDirectory()
    root = Path(temp.name)
    _write(root / 'ask_' 'ai_project_reasoner' / "__init__.py", "\"\"\"Package.\"\"\"\n")
    _write(
        root / 'ask_' 'ai_project_reasoner' / "reasoner_symbol_atlas" / "logic_placement_advisor.py",
        "\"\"\"Atlas advisor.\"\"\"\n\n"
        "def advise_reasoner_symbol_atlas_logic_placement():\n"
        "    return None\n",
    )
    _write(
        root / 'ask_' 'ai_project_reasoner' / "project_analysis_evidence_paths.py",
        "\"\"\"Evidence paths.\"\"\"\n\n"
        "def complete_analysis_json_file_path(project_root):\n"
        "    return project_root\n",
    )
    _write(
        root / "reasoner_tools_gui_engineering_safety_panel.py",
        "\"\"\"GUI panel.\"\"\"\n\n"
        "def build_engineering_safety_panel_command(command_name):\n"
        "    return [command_name]\n",
    )
    _write(
        root / "reasoner_tools_gui.py",
        "\"\"\"Facade.\"\"\"\n\n"
        "from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS\n",
    )
    _write(
        root / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "tool_specs.py",
        "\"\"\"Tool specs owner.\"\"\"\n\nTOOLS = ()\n",
    )
    return temp


def test_pa011_recommends_project_analysis_evidence_owner_for_tab4_task() -> None:
    temp = _make_project()
    try:
        root = Path(temp.name)
        decision = advise_reasoner_symbol_atlas_logic_placement(
            ProjectSymbolAtlasLogicPlacementOptions(
                project_root=str(root),
                task_description="fix Tab 4 complete JSON output path",
                target_path='ask_' 'ai_project_reasoner' '/project_analysis_evidence_paths.py',
            )
        )
        assert decision.recommended_owner_box == "project_analysis_evidence"
        assert decision.status == PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY
        assert "project_analysis_evidence_paths.py" in decision.primary_target_path
    finally:
        temp.cleanup()


def test_pa011_flags_facade_target_for_owner_review() -> None:
    temp = _make_project()
    try:
        root = Path(temp.name)
        decision = advise_reasoner_symbol_atlas_logic_placement(
            ProjectSymbolAtlasLogicPlacementOptions(
                project_root=str(root),
                task_description="add GUI tab registration",
                target_path="reasoner_tools_gui.py",
            )
        )
        assert decision.recommended_owner_box == "gui_shell"
        assert decision.status == PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW
        assert decision.target_owner_role in {"facade", "compatibility_facade", "ambiguous_owner"}
    finally:
        temp.cleanup()


def test_pa011_finds_existing_symbol_and_builds_report() -> None:
    temp = _make_project()
    try:
        root = Path(temp.name)
        decision = advise_reasoner_symbol_atlas_logic_placement(
            ProjectSymbolAtlasLogicPlacementOptions(
                project_root=str(root),
                task_description="update Engineering Safety GUI button command map",
                symbol_name="build_engineering_safety_panel_command",
            )
        )
        assert decision.recommended_owner_box == "gui_shell"
        assert "reasoner_tools_gui_engineering_safety_panel.py" in decision.primary_target_path
        assert decision.confidence in {"high", "medium"}
        report = build_reasoner_symbol_atlas_logic_placement_report(
            ProjectSymbolAtlasLogicPlacementOptions(
                project_root=str(root),
                task_description="update Engineering Safety GUI button command map",
                symbol_name="build_engineering_safety_panel_command",
            )
        )
        payload = report.to_dict()
        assert payload["report_type"] == "reasoner_symbol_atlas"
        assert "owner_box=gui_shell" in payload["summary"]
    finally:
        temp.cleanup()


def main() -> int:
    test_pa011_recommends_project_analysis_evidence_owner_for_tab4_task()
    test_pa011_flags_facade_target_for_owner_review()
    test_pa011_finds_existing_symbol_and_builds_report()
    print("PA011 Logic placement advisor tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
