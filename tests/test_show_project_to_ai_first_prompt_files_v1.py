from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (  # noqa: E402
    analysis_first_prompt_files_dir,
    analysis_json_complete_dir,
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help import (  # noqa: E402
    first_prompt_files_private_impl,
)


def test_first_and_second_prompt_folders_are_siblings() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        project_root = Path(temp_name) / "demo_project"
        project_root.mkdir()
        show_root = project_analysis_evidence_root(project_root)

        assert analysis_first_prompt_files_dir(project_root) == show_root / "first_prompt_files"
        assert analysis_json_complete_dir(project_root) == show_root / "second_prompt_files"


def test_clear_first_prompt_files_deletes_only_child_contents() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        show_root = Path(temp_name) / "demo_project_show_project_to_AI"
        first_prompt = show_root / "first_prompt_files"
        nested = first_prompt / "old_nested"
        nested.mkdir(parents=True)
        (first_prompt / "old.md").write_text("old", encoding="utf-8")
        (nested / "old.zip").write_text("zip", encoding="utf-8")

        removed = first_prompt_files_private_impl.clear_first_prompt_files_dir(first_prompt)

        assert removed == 2
        assert first_prompt.exists()
        assert list(first_prompt.iterdir()) == []
        assert show_root.exists()


def test_clear_first_prompt_files_rejects_unsafe_folder() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        unsafe = Path(temp_name) / "not_first_prompt_files"
        unsafe.mkdir()
        try:
            first_prompt_files_private_impl.clear_first_prompt_files_dir(unsafe)
        except ValueError as exc:
            assert "first_prompt_files" in str(exc)
        else:
            raise AssertionError("unsafe first_prompt_files clear should fail")


def test_startup_sync_script_writes_to_first_prompt_files_output_dir() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        selected_project = Path(temp_name) / ("demo_project_" + Path(temp_name).name.replace("-", "_"))
        selected_project.mkdir()
        output_dir = analysis_first_prompt_files_dir(selected_project)
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)
        (output_dir / "stale.txt").write_text("stale", encoding="utf-8")
        stale_dir = output_dir / "stale_dir"
        stale_dir.mkdir()
        (stale_dir / "old.txt").write_text("old", encoding="utf-8")

        workspace_root = PROJECT_ROOT / "kanda_prompt_workspace"
        script = workspace_root / "prompt_tools" / "sync_startup_routing_kernel_pack.py"

        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--sync",
                "--yes",
                "--workspace",
                str(workspace_root),
                "--output-dir",
                str(output_dir),
                "--project-root",
                str(selected_project),
            ],
            cwd=str(workspace_root),
            text=True,
            capture_output=True,
        )

        assert completed.returncode == 0, completed.stdout + completed.stderr
        for name in first_prompt_files_private_impl.REQUIRED_FIRST_PROMPT_FILENAMES:
            assert (output_dir / name).is_file(), name
        assert not (output_dir / "stale.txt").exists()
        assert not stale_dir.exists()


def test_show_project_to_ai_ui_has_two_column_labels_and_button() -> None:
    ui_text = (
        PROJECT_ROOT
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_methods_private_impl.py"
    ).read_text(encoding="utf-8")

    assert "Show Project to AI First Prompt Files" in ui_text
    assert "Show Project to AI Second Prompt Files" in ui_text
    assert "Create First Prompt Files" in ui_text
    assert "QSplitter(Qt.Horizontal)" in ui_text


def main() -> int:
    test_first_and_second_prompt_folders_are_siblings()
    test_clear_first_prompt_files_deletes_only_child_contents()
    test_clear_first_prompt_files_rejects_unsafe_folder()
    test_startup_sync_script_writes_to_first_prompt_files_output_dir()
    test_show_project_to_ai_ui_has_two_column_labels_and_button()
    print("VALIDATION OK: show_project_to_ai_first_prompt_files_v1")
    print("VALIDATION OK: show project to AI first prompt files")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
