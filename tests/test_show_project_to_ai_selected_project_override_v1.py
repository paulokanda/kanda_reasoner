"""Regression tests for selected-project Show Project to AI child-process overrides."""
from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV,
    SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV,
    SECOND_PROMPT_FILES_BUILDING_DIR,
    analysis_json_complete_dir,
    primary_evidence_json_path,
    project_analysis_evidence_root,
    secondary_evidence_json_path,
)


def _clear_env() -> None:
    os.environ.pop(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV, None)
    os.environ.pop(SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV, None)


def test_override_uses_selected_project_root_even_if_child_project_root_is_stale() -> None:
    with TemporaryDirectory() as tmp:
        base = Path(tmp)
        selected_root = base / "kanda_reasoner"
        stale_root = base / "stale_runtime_root"
        selected_root.mkdir()
        stale_root.mkdir()
        override_dir = project_analysis_evidence_root(selected_root) / SECOND_PROMPT_FILES_BUILDING_DIR
        override_dir.mkdir(parents=True, exist_ok=True)

        _clear_env()
        try:
            os.environ[SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV] = str(selected_root)
            os.environ[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = str(override_dir)

            assert analysis_json_complete_dir(stale_root) == override_dir.resolve(strict=False)
            assert primary_evidence_json_path(stale_root) == override_dir.resolve(strict=False) / "kanda_reasoner__complete.json"
            assert secondary_evidence_json_path(stale_root) == override_dir.resolve(strict=False) / "kanda_reasoner__complete_runtime_trace.json"
        finally:
            _clear_env()


def test_override_rejects_folder_from_a_different_selected_project() -> None:
    with TemporaryDirectory() as tmp:
        base = Path(tmp)
        selected_root = base / "kanda_reasoner"
        other_root = base / "other_project_root"
        selected_root.mkdir()
        other_root.mkdir()
        wrong_override = project_analysis_evidence_root(other_root) / SECOND_PROMPT_FILES_BUILDING_DIR
        wrong_override.mkdir(parents=True, exist_ok=True)

        _clear_env()
        try:
            os.environ[SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV] = str(selected_root)
            os.environ[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = str(wrong_override)
            try:
                analysis_json_complete_dir(other_root)
            except ValueError as exc:
                message = str(exc)
                assert "selected project's show_project_to_AI folder" in message
                assert "kanda_reasoner_show_project_to_AI" in message
            else:
                raise AssertionError("cross-project override was accepted")
        finally:
            _clear_env()


def test_child_environment_carries_selected_project_root_for_override_validation() -> None:
    source = Path(
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py"
    ).read_text(encoding="utf-8")
    assert "KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT" in source
    assert "env[\"KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT\"] = str(project_root)" in source


def main() -> int:
    test_override_uses_selected_project_root_even_if_child_project_root_is_stale()
    test_override_rejects_folder_from_a_different_selected_project()
    test_child_environment_carries_selected_project_root_for_override_validation()
    print("VALIDATION OK: show_project_to_ai_selected_project_override_v1")
    print("VALIDATION OK: show project to AI selected project override")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
