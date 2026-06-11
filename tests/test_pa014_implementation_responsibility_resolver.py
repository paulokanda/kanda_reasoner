"""Focused tests for PA014 Project Symbol Atlas implementation responsibility resolver."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.implementation_responsibility_resolver import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW,
    PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY,
    ProjectSymbolAtlasImplementationResponsibilityOptions,
    build_reasoner_symbol_atlas_implementation_responsibility_report,
    resolve_reasoner_symbol_atlas_implementation_responsibility,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_pa014_resolves_gui_helper_back_to_main_owner() -> None:
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
        decision = resolve_reasoner_symbol_atlas_implementation_responsibility(
            ProjectSymbolAtlasImplementationResponsibilityOptions(
                project_root=str(root),
                task_description="repair GUI panel command map",
                target_path="reasoner_tools_gui_engineering_safety_panel_commands.py",
            )
        )
        assert decision.status in {
            PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY,
            PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW,
        }
        assert decision.recommended_owner_box == "gui_shell"
        assert decision.primary_edit_target.replace("\\", "/") == "reasoner_tools_gui_engineering_safety_panel.py"
        assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in [
            item.replace("\\", "/") for item in decision.secondary_helper_targets
        ]
        assert decision.tests_to_run


def test_pa014_warns_when_target_is_facade() -> None:
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
        decision = resolve_reasoner_symbol_atlas_implementation_responsibility(
            ProjectSymbolAtlasImplementationResponsibilityOptions(
                project_root=str(root),
                task_description="add GUI tab registration",
                target_path="reasoner_tools_gui.py",
                symbol_name="TOOLS",
            )
        )
        assert decision.status == PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW
        assert decision.facade_patch_risk
        assert decision.primary_edit_target.replace("\\", "/").endswith(
            'ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/tool_specs.py'
        )
        assert "reasoner_tools_gui.py" in [item.replace("\\", "/") for item in decision.files_not_to_touch]


def test_pa014_builds_report_without_source_edits() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(root / "project_analysis_evidence_paths.py", "def complete_json_file_path():\n    return 'ok'\n")
        report = build_reasoner_symbol_atlas_implementation_responsibility_report(
            ProjectSymbolAtlasImplementationResponsibilityOptions(
                project_root=str(root),
                task_description="fix Tab 4 complete JSON output path",
                target_path="project_analysis_evidence_paths.py",
            )
        )
        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert "implementation_responsibility_resolver" in data["input_sources"]
        assert "Implementation responsibility" in data["summary"]


def main() -> int:
    test_pa014_resolves_gui_helper_back_to_main_owner()
    test_pa014_warns_when_target_is_facade()
    test_pa014_builds_report_without_source_edits()
    print("PA014 Implementation responsibility resolver tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
