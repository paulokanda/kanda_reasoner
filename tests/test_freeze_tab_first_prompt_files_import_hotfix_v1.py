from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    FIRST_PROMPT_FILES_DIR,
    SECOND_PROMPT_FILES_BUILDING_DIR,
    SECOND_PROMPT_FILES_DIR,
    analysis_first_prompt_files_dir,
    analysis_json_building_dir,
    analysis_json_complete_dir,
    project_analysis_evidence_root,
)


def test_first_prompt_files_helper_is_restored_without_breaking_second_prompt_paths():
    project_root = Path(r"E:\kanda_reasoner")
    show_root = project_analysis_evidence_root(project_root)

    assert FIRST_PROMPT_FILES_DIR == "first_prompt_files"
    assert SECOND_PROMPT_FILES_DIR == "second_prompt_files"
    assert SECOND_PROMPT_FILES_BUILDING_DIR == "second_prompt_files_building"
    assert analysis_first_prompt_files_dir(project_root) == show_root / "first_prompt_files"
    assert analysis_json_complete_dir(project_root) == show_root / "second_prompt_files"
    assert analysis_json_building_dir(project_root) == show_root / "second_prompt_files_building"


def test_freeze_tab_import_compatibility_symbol_exists():
    import kanda_reasoner_app.project_analysis_evidence_paths as paths

    assert callable(paths.analysis_first_prompt_files_dir)
