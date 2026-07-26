# project-path: tests/test_architecture_warning_cleanup_batch20_runner_help_public_ownership.py
"""Static smoke coverage for Batch 20 runner-help public ownership repair."""

from __future__ import annotations

from scripts import repair_architecture_warning_cleanup_batch20_runner_help_public_ownership_v1 as repair
from scripts import validate_architecture_warning_cleanup_batch20_runner_help_public_ownership_v1 as validator


def test_batch20_public_entrypoints_are_available() -> None:
    assert repair.FEATURE_ID == "architecture-warning-cleanup-batch20-runner-help-public-ownership-repair-v1"
    assert validator.FEATURE_ID == "architecture-warning-cleanup-batch20-runner-help-public-ownership-repair-v1"
    assert repair.__all__ == ["main"]
    assert validator.__all__ == ["main"]


def test_batch20_static_target_evidence_is_complete() -> None:
    target_files = {
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_state_private_impl.py",
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_process_private_impl.py",
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py",
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_paths_private_impl.py",
    }
    duplicate_symbols = {
        "ALLOWED_ZIP_SIZE_MB_OPTIONS",
        "auto_zip_json_complete",
        "cleanup_loose_json_files_after_success",
        "cleanup_show_project_to_ai_root_after_success",
        "cleanup_transient_daily_refactor_folders",
        "clear_second_prompt_files_building_dir",
        "clear_second_prompt_files_dir",
        "DEFAULT_ZIP_SIZE_MB",
        "EXTENDED_ZIP_SIZE_MB_OPTIONS",
        "load_saved_part_size_mb",
        "publish_second_prompt_files_building_dir",
        "resolve_zip_dialog_start_folder",
        "run_zip_json_files",
        "save_selected_part_size_mb",
        "second_prompt_files_building_dir",
        "selected_part_size_mb",
        "write_second_prompt_status",
    }
    assert target_files == set(repair.IMPLEMENTATION_ONLY_MODULES)
    assert duplicate_symbols == set(validator.DUPLICATE_SYMBOLS)
