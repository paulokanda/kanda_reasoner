from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
    primary_evidence_json_path,
    project_analysis_evidence_root,
    secondary_evidence_json_path,
)
from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS
from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_private_impl


def test_second_prompt_files_is_the_run_collector_output_folder() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        project_root = Path(temp_name) / "demo_project"
        project_root.mkdir()

        show_root = project_analysis_evidence_root(project_root)
        second_prompt = analysis_json_complete_dir(project_root)

        assert show_root.name == "demo_project_show_project_to_AI"
        assert second_prompt == show_root / "second_prompt_files"
        assert primary_evidence_json_path(project_root) == second_prompt / "demo_project__complete.json"
        assert secondary_evidence_json_path(project_root) == second_prompt / "demo_project__complete_runtime_trace.json"


def test_clear_second_prompt_files_deletes_only_child_contents() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        show_root = Path(temp_name) / "demo_project_show_project_to_AI"
        second_prompt = show_root / "second_prompt_files"
        nested = second_prompt / "old_nested"
        nested.mkdir(parents=True)
        (second_prompt / "old.json").write_text("{}", encoding="utf-8")
        (nested / "old.zip").write_text("zip", encoding="utf-8")

        removed = zip_json_files_private_impl.clear_second_prompt_files_dir(second_prompt)

        assert removed == 2
        assert second_prompt.exists()
        assert list(second_prompt.iterdir()) == []
        assert show_root.exists()


def test_clear_second_prompt_files_rejects_unsafe_folder() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        unsafe = Path(temp_name) / "not_second_prompt_files"
        unsafe.mkdir()
        try:
            zip_json_files_private_impl.clear_second_prompt_files_dir(unsafe)
        except ValueError as exc:
            assert "second_prompt_files" in str(exc)
        else:
            raise AssertionError("unsafe folder clear should fail")


def test_lazy_tab_title_is_show_project_to_ai() -> None:
    labels = [spec.step_title for spec in TOOLS]
    assert "Show Project to AI" in labels
    assert "Project Structure Map" not in labels


def main() -> int:
    test_second_prompt_files_is_the_run_collector_output_folder()
    test_clear_second_prompt_files_deletes_only_child_contents()
    test_clear_second_prompt_files_rejects_unsafe_folder()
    test_lazy_tab_title_is_show_project_to_ai()
    print("VALIDATION OK: show_project_to_ai_second_prompt_files_v1")
    print("VALIDATION OK: show project to AI second prompt files")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
