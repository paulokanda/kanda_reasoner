"""PA023B Atlas output policy active-scope tests."""

from __future__ import annotations

from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
    is_active_atlas_path,
    is_active_test_command,
    sanitize_atlas_markdown_text,
)


def test_pa023b_active_path_policy() -> None:
    assert is_active_atlas_path("reasoner_tools_gui_engineering_safety_panel.py")
    assert is_active_atlas_path('ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/existing_code_finder.py')
    assert not is_active_atlas_path("_project_reference/tests_archive/old.py")
    assert not is_active_atlas_path("snippets/example.py")
    assert not is_active_atlas_path("workbench/_bundle_temp/temp.py")


def test_pa023b_test_command_policy() -> None:
    assert is_active_test_command("python tests/test_pa021_reasoner_symbol_atlas_gui_integration.py")
    assert not is_active_test_command("python _project_reference/tests_archive/old/test_x.py")
    assert not is_active_test_command("python tests/__init__.py")


def test_pa023b_sanitizes_wrong_project_owner_recommendations() -> None:
    raw = "\n".join(
        [
            "# Project Symbol Atlas Report",
            "## Summary",
            "Existing code finder query completed; status=ready; primary_edit_target=_project_reference/ACTIVE_PROJECT_ GOVERNANCE/check_reasoner_project_canon.py; pre_patch_status=wrong_target_file.",
            "## Decision Details",
            "- query_type=pre_patch_gate",
            "- main_path=_project_reference/ACTIVE_PROJECT_ GOVERNANCE/check_reasoner_project_canon.py",
            "- related_file=_project_reference/tests_archive/old/test_x.py",
            "- related_file=reasoner_tools_gui_engineering_safety_panel.py",
            "- test_to_run=python _project_reference/tests_archive/old/test_y.py",
            "- test_to_run=python tests/test_pa021_reasoner_symbol_atlas_gui_integration.py",
            "## Symbols",
            "- existing_code_finder_decision (unknown) in  -> reasoner_tools_gui_engineering_safety_panel.py",
        ]
    )
    cleaned = sanitize_atlas_markdown_text(raw)
    assert "_project_reference" not in cleaned
    assert "primary_edit_target=reasoner_tools_gui_engineering_safety_panel.py" in cleaned
    assert "main_path=reasoner_tools_gui_engineering_safety_panel.py" in cleaned
    assert "pre_patch_status=needs_owner_review" in cleaned
    assert "tests/test_pa021_reasoner_symbol_atlas_gui_integration.py" in cleaned
    assert "existing_code_finder_decision (decision)" in cleaned


def main() -> int:
    test_pa023b_active_path_policy()
    test_pa023b_test_command_policy()
    test_pa023b_sanitizes_wrong_project_owner_recommendations()
    print("PA023B Atlas output policy active-scope tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
