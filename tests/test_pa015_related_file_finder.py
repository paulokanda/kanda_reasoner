"""Focused tests for PA015 Project Symbol Atlas related file finder."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_RELATED_STATUS_READY,
    ProjectSymbolAtlasRelatedFileOptions,
    build_reasoner_symbol_atlas_related_file_report,
    find_reasoner_symbol_atlas_related_files,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _normalize(values: tuple[str, ...]) -> list[str]:
    return [value.replace("\\", "/") for value in values]


def test_pa015_finds_main_helper_tests_and_manifest() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(
            root / "reasoner_tools_gui_engineering_safety_panel.py",
            "from reasoner_tools_gui_engineering_safety_panel_commands import build_args\n\n"
            "def build_engineering_safety_panel_command():\n"
            "    return build_args()\n",
        )
        _write(
            root / "reasoner_tools_gui_engineering_safety_panel_commands.py",
            "def build_args():\n"
            "    return ['risk-radar']\n",
        )
        _write(
            root / "tests" / "test_reasoner_tools_gui_engineering_safety_panel.py",
            "import reasoner_tools_gui_engineering_safety_panel\n",
        )
        _write(
            root / "workbench" / "_bundle_temp" / "BUNDLE_MANIFEST_reasoner_tools_gui_engineering_safety_panel.txt",
            "panel manifest\n",
        )
        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(root),
                target_path="reasoner_tools_gui_engineering_safety_panel_commands.py",
                include_workbench=True,
            )
        )
        assert decision.status == PROJECT_SYMBOL_ATLAS_RELATED_STATUS_READY
        assert "reasoner_tools_gui_engineering_safety_panel.py" in _normalize(decision.main_files)
        assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in _normalize(decision.helper_files)
        assert "tests/test_reasoner_tools_gui_engineering_safety_panel.py" in _normalize(decision.test_files)
        assert decision.manifest_files
        assert decision.tests_to_run


def test_pa015_finds_facade_and_real_owner() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(
            root / "reasoner_tools_gui.py",
            "from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS\n",
        )
        _write(
            root / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "tool_specs.py",
            "TOOLS = ()\n",
        )
        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(root),
                target_path="reasoner_tools_gui.py",
                symbol_name="TOOLS",
            )
        )
        assert "reasoner_tools_gui.py" in _normalize(decision.facade_files)
        assert any(
            value.endswith('ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/tool_specs.py')
            for value in _normalize(decision.real_owner_files)
        )
        assert "reasoner_tools_gui.py" in _normalize(decision.do_not_edit_files)


def test_pa015_builds_report_without_source_edits() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(root / "alpha.py", "def alpha():\n    return 1\n")
        _write(root / "tests" / "test_alpha.py", "from alpha import alpha\n")
        report = build_reasoner_symbol_atlas_related_file_report(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(root),
                target_path="alpha.py",
            )
        )
        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert "related_file_finder" in data["input_sources"]
        assert "Related help/support files" in data["summary"]


def main() -> int:
    test_pa015_finds_main_helper_tests_and_manifest()
    test_pa015_finds_facade_and_real_owner()
    test_pa015_builds_report_without_source_edits()
    print("PA015 Related help/support file finder tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
