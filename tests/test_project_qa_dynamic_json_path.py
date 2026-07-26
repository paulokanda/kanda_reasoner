"""Project Q&A dynamic JSON-path resolution tests."""

from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.json_track import (
    classify_loaded_json_track,
)
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.project_json_path_resolver import (
    is_deprecated_project_json_path,
    resolve_project_json_path,
    should_replace_project_json_path,
)


DEPRECATED_JSON_PATH = (
    "E:/developer_tools/dev_tools_docs/json_complete/"
    "developer_tools__complete_local_AI.json"
)


def _unique_project_root(name: str) -> Path:
    return Path.cwd() / ("_qa_dynamic_json_" + uuid4().hex) / name


def test_deprecated_developer_tools_path_resolves_to_selected_project() -> None:
    resolution = resolve_project_json_path(_unique_project_root("ClientApp"))
    resolved_text = str(resolution.selected_json).replace("\\", "/")

    assert is_deprecated_project_json_path(DEPRECATED_JSON_PATH)
    assert should_replace_project_json_path(DEPRECATED_JSON_PATH, resolution)
    assert "developer_tools" not in resolved_text
    assert "_show_project_to_AI/second_prompt_files/" in resolved_text
    assert resolved_text.lower().endswith("__complete_local_ai.json")


def test_project_change_replaces_previous_project_json_path() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        old_hint = Path(tmp_dir) / "OldProject_show_project_to_AI"
        new_hint = Path(tmp_dir) / "NewProject_show_project_to_AI"
        old_resolution = resolve_project_json_path(old_hint)
        new_resolution = resolve_project_json_path(new_hint)

        old_resolution.local_ai_json.parent.mkdir(parents=True, exist_ok=True)
        old_resolution.local_ai_json.write_text("{}", encoding="utf-8")

        assert should_replace_project_json_path(
            str(old_resolution.local_ai_json),
            new_resolution,
        )


def test_existing_local_ai_json_is_kept_for_selected_project() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        project_hint = Path(tmp_dir) / "DemoProject_show_project_to_AI"
        initial_resolution = resolve_project_json_path(project_hint)
        initial_resolution.local_ai_json.parent.mkdir(parents=True, exist_ok=True)
        initial_resolution.local_ai_json.write_text("{}", encoding="utf-8")

        resolution = resolve_project_json_path(project_hint)

        assert resolution.selected_json == resolution.local_ai_json
        assert resolution.selected_kind == "local-ai"
        assert not should_replace_project_json_path(
            str(resolution.local_ai_json),
            resolution,
        )


def test_json_track_accepts_dynamic_second_prompt_filenames() -> None:
    assert (
        classify_loaded_json_track(
            "E:/sample_show_project_to_AI/second_prompt_files/"
            "sample__complete_local_AI.json"
        )
        == "Local-AI working JSON"
    )
    assert (
        classify_loaded_json_track(
            "E:/sample_show_project_to_AI/second_prompt_files/"
            "sample__complete.json"
        )
        == "Canonical web-AI JSON"
    )


def test_runtime_controller_does_not_use_tool_project_root() -> None:
    source = Path(
        "kanda_reasoner_app/reasoner_engine/"
        "ai_reasoner_main_window_help/runtime_controller.py"
    ).read_text(encoding="utf-8")
    assert "_tool_project_root" not in source
    assert "ensure_local_ai_copy(project_root)" in source
    assert "refresh_local_ai_copy(project_root)" in source


if __name__ == "__main__":
    test_deprecated_developer_tools_path_resolves_to_selected_project()
    test_project_change_replaces_previous_project_json_path()
    test_existing_local_ai_json_is_kept_for_selected_project()
    test_json_track_accepts_dynamic_second_prompt_filenames()
    test_runtime_controller_does_not_use_tool_project_root()
    print("Project Q&A dynamic JSON path tests passed.")
