"""PA032 tests for hiding private compatibility files from Tab 8 related output."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from kanda_reasoner_app.reasoner_symbol_atlas.pre_patch_gate import (
    ProjectSymbolAtlasPrePatchGateOptions,
    run_reasoner_symbol_atlas_pre_patch_gate,
)
from kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder import (
    ProjectSymbolAtlasRelatedFileOptions,
    find_reasoner_symbol_atlas_related_files,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_project(root: Path) -> None:
    _write(
        root / "reasoner_tools_gui_engineering_safety_panel.py",
        "from reasoner_tools_gui_engineering_safety_panel_commands import "
        "build_engineering_safety_panel_command\n"
        "__all__ = [\"create_engineering_safety_panel\"]\n"
        "def create_engineering_safety_panel():\n"
        "    return None\n",
    )
    _write(
        root / "reasoner_tools_gui_engineering_safety_panel_commands.py",
        "def build_engineering_safety_panel_command():\n"
        "    return []\n",
    )
    _write(
        root / "_reasoner_tools_gui_engineering_safety_panel_commands.py",
        "from reasoner_tools_gui_engineering_safety_panel_commands import *\n",
    )


def test_related_files_hide_private_compatibility_file() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _build_project(root)

        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(root),
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
            )
        )

    assert "reasoner_tools_gui_engineering_safety_panel.py" in decision.related_files
    assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.related_files
    assert "_reasoner_tools_gui_engineering_safety_panel_commands.py" not in decision.related_files


def test_pre_patch_gate_hide_private_compatibility_related_file() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _build_project(root)

        decision = run_reasoner_symbol_atlas_pre_patch_gate(
            ProjectSymbolAtlasPrePatchGateOptions(
                project_root=str(root),
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
                task_description="Review Project Symbol Atlas GUI button wiring before patching.",
            )
        )

    assert decision.primary_edit_target == "reasoner_tools_gui_engineering_safety_panel.py"
    assert "reasoner_tools_gui_engineering_safety_panel.py" in decision.related_files
    assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.related_files
    assert "_reasoner_tools_gui_engineering_safety_panel_commands.py" not in decision.related_files


def test_private_file_remains_related_when_it_is_the_direct_target() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _build_project(root)

        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(root),
                target_path="_reasoner_tools_gui_engineering_safety_panel_commands.py",
                symbol_name="",
            )
        )

    assert "_reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.related_files


if __name__ == "__main__":
    test_related_files_hide_private_compatibility_file()
    test_pre_patch_gate_hide_private_compatibility_related_file()
    test_private_file_remains_related_when_it_is_the_direct_target()
    print("PA032 Tab 8 private compatibility related-file cleanup tests passed.")
