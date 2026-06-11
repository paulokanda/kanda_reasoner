"""PA031 tests for keeping tests out of Tab 8 active project output."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
    ProjectSymbolAtlasExistingCodeFinderOptions,
    find_reasoner_symbol_atlas_existing_code,
)
from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
    is_active_project_source_path,
    is_active_test_command,
)
from kanda_reasoner_app.reasoner_symbol_atlas.pre_patch_gate import (
    ProjectSymbolAtlasPrePatchGateOptions,
    run_reasoner_symbol_atlas_pre_patch_gate,
)
from kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder import (
    ProjectSymbolAtlasRelatedFileOptions,
    find_reasoner_symbol_atlas_related_files,
)


def _make_project() -> TemporaryDirectory[str]:
    temp_dir = TemporaryDirectory()
    root = Path(temp_dir.name)
    (root / "reasoner_tools_gui_engineering_safety_panel.py").write_text(
        "def create_engineering_safety_panel():\n"
        "    return None\n",
        encoding="utf-8",
    )
    (root / "reasoner_tools_gui_engineering_safety_panel_commands.py").write_text(
        "def run_engineering_safety_panel_cli_command():\n"
        "    return None\n",
        encoding="utf-8",
    )
    tests_root = root / "tests"
    tests_root.mkdir()
    (tests_root / "test_reasoner_tools_gui_engineering_safety_panel.py").write_text(
        "def test_panel():\n"
        "    assert True\n",
        encoding="utf-8",
    )
    return temp_dir


def _assert_no_direct_test_outputs(values: tuple[str, ...]) -> None:
    for value in values:
        normalized = value.replace("\\", "/").lower()
        assert not normalized.startswith("tests/"), value
        assert "/tests/" not in normalized, value
        assert "python tests/" not in normalized, value
        assert "python ./tests/" not in normalized, value


def test_policy_rejects_tests_as_active_project_source() -> None:
    assert not is_active_project_source_path("tests/test_example.py")
    assert not is_active_project_source_path("pkg/tests/test_example.py")
    assert is_active_project_source_path("reasoner_tools_gui_engineering_safety_panel.py")


def test_policy_rejects_direct_test_commands_but_keeps_gates() -> None:
    assert not is_active_test_command("python tests/test_example.py")
    assert is_active_test_command("python -m py_compile reasoner_tools_gui_engineering_safety_panel.py")
    assert is_active_test_command(
        'python ask_' 'ai_project_reasoner' '\\manage_architecture\\manage_architecture.py --root <PROJECT_ROOT> --validate'
    )


def test_pre_patch_gate_default_output_excludes_tests() -> None:
    with _make_project() as project_root:
        decision = run_reasoner_symbol_atlas_pre_patch_gate(
            ProjectSymbolAtlasPrePatchGateOptions(
                project_root=project_root,
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
                task_description="Review Project Symbol Atlas GUI button wiring before patching.",
            )
        )

    assert decision.primary_edit_target == "reasoner_tools_gui_engineering_safety_panel.py"
    assert "reasoner_tools_gui_engineering_safety_panel.py" in decision.related_files
    assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.related_files
    _assert_no_direct_test_outputs(decision.related_files)
    _assert_no_direct_test_outputs(decision.tests_to_run)


def test_related_files_default_output_excludes_tests() -> None:
    with _make_project() as project_root:
        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=project_root,
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
            )
        )

    assert decision.test_files == tuple()
    assert "reasoner_tools_gui_engineering_safety_panel.py" in decision.related_files
    _assert_no_direct_test_outputs(decision.related_files)
    _assert_no_direct_test_outputs(decision.tests_to_run)


def test_existing_code_pre_patch_default_output_excludes_tests() -> None:
    with _make_project() as project_root:
        result = find_reasoner_symbol_atlas_existing_code(
            ProjectSymbolAtlasExistingCodeFinderOptions(
                project_root=project_root,
                query_type="pre_patch_gate",
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
                symbol_name="create_engineering_safety_panel",
                task_description="Review Project Symbol Atlas GUI button wiring before patching.",
                exact=True,
            )
        )

    assert result.primary_edit_target == "reasoner_tools_gui_engineering_safety_panel.py"
    _assert_no_direct_test_outputs(result.related_files)
    _assert_no_direct_test_outputs(result.tests_to_run)


if __name__ == "__main__":
    test_policy_rejects_tests_as_active_project_source()
    test_policy_rejects_direct_test_commands_but_keeps_gates()
    test_pre_patch_gate_default_output_excludes_tests()
    test_related_files_default_output_excludes_tests()
    test_existing_code_pre_patch_default_output_excludes_tests()
    print("PA031 Tab 8 tests-out-of-active-project tests passed.")
