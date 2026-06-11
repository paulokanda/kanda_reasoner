"""PA030 tests for Project Symbol Atlas target ranking."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
    ProjectSymbolAtlasExistingCodeFinderOptions,
    find_reasoner_symbol_atlas_existing_code,
)
from kanda_reasoner_app.reasoner_symbol_atlas.implementation_responsibility_resolver import (
    ProjectSymbolAtlasImplementationResponsibilityOptions,
    resolve_reasoner_symbol_atlas_implementation_responsibility,
)
from kanda_reasoner_app.reasoner_symbol_atlas.main_helper_mapper import (
    ProjectSymbolAtlasMainHelperOptions,
    map_reasoner_symbol_atlas_main_helpers,
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
        root / 'ask_' 'ai_project_reasoner' / "assert_real_project_static_context_smoke.py",
        "import reasoner_tools_gui_engineering_safety_panel\n"
        "def run_smoke():\n"
        "    return True\n",
    )
    _write(
        root / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "gui_scope_helpers.py",
        "def unrelated_gui_scope_helper():\n"
        "    return True\n",
    )
    _write(
        root / "project_analysis_evidence" / "json_complete" / "developer_tools__complete.json",
        "{}\n",
    )
    _write(
        root / "tests" / "test_gui003_engineering_safety_panel_actions.py",
        "from reasoner_tools_gui_engineering_safety_panel import "
        "create_engineering_safety_panel\n"
        "def test_panel():\n"
        "    assert create_engineering_safety_panel() is None\n",
    )


def test_pa030_main_helper_prefers_exact_active_target_over_smoke_file() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _build_project(root)

        decision = map_reasoner_symbol_atlas_main_helpers(
            ProjectSymbolAtlasMainHelperOptions(
                project_root=str(root),
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
            )
        )

        assert decision.main_path == "reasoner_tools_gui_engineering_safety_panel.py"
        assert "assert_real_project_static_context_smoke.py" not in decision.main_path
        assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.helper_paths


def test_pa030_related_files_exclude_evidence_json_and_unrelated_smoke_files() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _build_project(root)

        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(root),
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
                include_evidence_files=True,
            )
        )

        assert "reasoner_tools_gui_engineering_safety_panel.py" in decision.related_files
        assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.related_files
        assert all(not path.startswith("tests/") for path in decision.related_files)
        assert all("project_analysis_evidence" not in path for path in decision.related_files)
        assert all("assert_real_project_static_context_smoke" not in path for path in decision.related_files)
        assert all("gui_scope_helpers" not in path for path in decision.related_files)


def test_pa030_implementation_responsibility_keeps_exact_target_as_primary() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _build_project(root)

        decision = resolve_reasoner_symbol_atlas_implementation_responsibility(
            ProjectSymbolAtlasImplementationResponsibilityOptions(
                project_root=str(root),
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
                task_description="Review Project Symbol Atlas GUI button wiring before patching.",
            )
        )

        assert decision.primary_edit_target == "reasoner_tools_gui_engineering_safety_panel.py"
        assert "reasoner_tools_gui_engineering_safety_panel.py" not in decision.files_not_to_touch
        assert all("assert_real_project_static_context_smoke" not in path for path in decision.secondary_helper_targets)


def test_pa030_existing_code_pre_patch_result_does_not_invent_unrelated_target() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _build_project(root)

        result = find_reasoner_symbol_atlas_existing_code(
            ProjectSymbolAtlasExistingCodeFinderOptions(
                project_root=str(root),
                query_type="pre_patch_gate",
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
                task_description="Review Project Symbol Atlas GUI button wiring before patching.",
                exact=True,
            )
        )

        assert result.primary_edit_target == "reasoner_tools_gui_engineering_safety_panel.py"
        assert result.main_path == "reasoner_tools_gui_engineering_safety_panel.py"
        assert all("project_analysis_evidence" not in path for path in result.related_files)
        assert all("assert_real_project_static_context_smoke" not in path for path in result.related_files)


def main() -> int:
    test_pa030_main_helper_prefers_exact_active_target_over_smoke_file()
    test_pa030_related_files_exclude_evidence_json_and_unrelated_smoke_files()
    test_pa030_implementation_responsibility_keeps_exact_target_as_primary()
    test_pa030_existing_code_pre_patch_result_does_not_invent_unrelated_target()
    print("PA030 Atlas target ranking tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
