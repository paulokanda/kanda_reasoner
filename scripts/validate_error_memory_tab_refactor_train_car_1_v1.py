# project-path: scripts/validate_error_memory_tab_refactor_train_car_1_v1.py
"""Validate Error Memory tab refactor train car 1."""
from __future__ import annotations

__all__ = [
    "main",
]

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"

FEATURE_ID = "-".join([
    "error",
    "memory",
    "tab",
    "refactor",
    "train",
    "car",
    "1",
    "v1",
])
INTAKE_MIXIN_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "_intake_actions_mixin.py"
PROJECT_PATHS_MIXIN_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "_project_paths_mixin.py"
TABLE_DRAFT_MIXIN_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "_table_draft_mixin.py"

INTAKE_GENERAL_METHODS = {
    "_pending_ai_assisted_error_lesson_intake_dir",
    "_candidate_pending_ai_assisted_intake_dirs",
    "load_pending_ai_assisted_error_lesson_intake_now",
    "_load_pending_ai_assisted_error_lesson_intake",
    "_set_ai_assisted_intake_and_error_editor_from_pending_text",
    "_read_error_memory_intake_template_file",
    "_error_lesson_intake_blueprint_clipboard_text",
    "_copy_error_lesson_intake_blueprint_to_clipboard",
    "_show_duplicate_pending_intake_warning",
    "_safe_pending_lesson_id_from_file",
    "_pending_file_updated_text",
    "_summary_from_pending_raw_text",
    "_draft_lesson_from_pending_raw_text",
    "_delete_pending_file_quietly",
    "_copy_ai_assisted_intake_error_draft_to_clipboard",
    "_dismiss_loaded_pending_intake_file_for_session",
    "_clean_intake_window",
    "_pending_intake_files_for_all_candidate_dirs",
    "_pending_file_matches_draft_identity",
    "_delete_matching_pending_intake_files",
    "_consume_loaded_pending_intake_file_if_matches",
    "_clear_ai_assisted_intake_after_memorize",
    "_existing_directory_from_text",
    "_show_action_done",
    "_lesson_json_text_for_windows",
    "_active_ready_missing_text",
    "_lesson_id_exists_in_lessons",
    "_heuristic_correction_result_for_editor",
    "_apply_heuristic_correction_to_error_editor",
    "_lesson_id_from_text_lenient",
    "_json_payload_from_text",
    "_candidate_text_for_memorize",
    "_save_active_ready_lesson",
    "_memorize_error_from_text_window",
    "_validation_evidence_is_passing",
    "_undo_lesson_action",
    "_operation_phase_for_guard",
    "_check_against_lessons",
    "_show_repeat_guard_report",
}

PROJECT_PATH_METHODS = {
    "set_project_root",
    "_source_root_peer_from_generated_output",
    "_source_root_from_directory_hint",
    "_on_project_root_field_changed",
    "_current_project_root",
    "_search_project_root",
    "_copy_path_to_clipboard",
    "_refresh_paths",
    "_pending_intake_dirs_for_root_hint",
    "_pending_path_for_row",
    "_open_folder",
}

TABLE_DRAFT_METHODS = {
    "_copy_complete_error_memory_json_to_clipboard",
    "_show_active_ready_failure_copy_window",
    "_error_memory_prompt_template_dir",
    "_reload_table",
    "_row_kind_for_row",
    "_lesson_id_for_row",
    "_selected_lesson_id_from_table",
    "_pending_lesson_rows_for_table",
    "_load_pending_intake_row_into_editor",
    "_load_selected_lesson_into_preview",
    "_lesson_from_current_windows_or_selection",
    "_select_saved_active_lesson_row",
    "_save_preview_lesson",
    "_delete_selected_lesson",
    "_lesson_from_preview_or_selection",
    "_set_selected_lesson_status",
    "_supersede_selected_lesson",
    "_copy_error_draft_to_clipboard",
    "_clean_error_editor",
    "_draft_delete_identity_from_windows",
    "_delete_matching_canonical_draft_lessons",
    "_delete_current_draft_completely",
    "_canonical_draft_lesson_from_partial",
    "_save_draft_lesson_from_partial",
    "_formatted_lesson_block",
    "_receive_formulary_from_ai",
    "_text_has_formatted_lesson_payload",
    "_lesson_from_formatted_text",
    "_text_is_formatted_error_lesson_payload",
    "_formatted_text_from_manifested_lesson_zip",
    "_formatted_import_text_for_window",
    "_import_error_lesson_zip",
    "_export_for_ai",
}


def _parse(path: Path) -> ast.Module:
    """Support parse behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    ast.Module
        The module result.
    """
    
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _class(module: ast.Module, name: str) -> ast.ClassDef:
    """Support class behavior.
    
    Parameters
    ----------
    module : ast.Module
        The module value.
    name : str
        The name value.
    
    Returns
    -------
    ast.ClassDef
        The class def result.
    """
    
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise AssertionError(f"Missing class {name}")


def _method_names(cls: ast.ClassDef) -> set[str]:
    """Support method names behavior.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {node.name for node in cls.body if isinstance(node, ast.FunctionDef)}


def _base_names(cls: ast.ClassDef) -> list[str]:
    """Support base names behavior.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    names: list[str] = []
    for base in cls.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        else:
            names.append(ast.unparse(base))
    return names


def _line_count(path: Path) -> int:
    """Support line count behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(path.read_text(encoding="utf-8").splitlines())


def _assert_line_band(path: Path, *, minimum: int, maximum: int) -> None:
    """Support assert line band behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    minimum : int
        The minimum value.
    maximum : int
        The maximum value.
    """
    
    count = _line_count(path)
    if not (minimum <= count <= maximum):
        raise AssertionError(f"{path.relative_to(PROJECT_ROOT)} line count {count} outside {minimum}-{maximum}")


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    tab_module = _parse(TAB_PATH)
    tab_cls = _class(tab_module, "ErrorMemoryTab")
    tab_methods = _method_names(tab_cls)
    bases = _base_names(tab_cls)

    expected_bases = [
        "ErrorMemoryProjectPathsMixin",
        "ErrorMemoryTableDraftMixin",
        "ErrorMemoryIntakeActionsMixin",
        "QWidget",
    ]
    if bases != expected_bases:
        raise AssertionError(f"Unexpected ErrorMemoryTab bases: {bases}")

    if _line_count(TAB_PATH) > 500:
        raise AssertionError(f"error_memory_tab.py remains above v7.2 maximum: {_line_count(TAB_PATH)}")

    moved = INTAKE_GENERAL_METHODS | PROJECT_PATH_METHODS | TABLE_DRAFT_METHODS
    still_inline = sorted(moved & tab_methods)
    if still_inline:
        raise AssertionError("Moved methods still inline in ErrorMemoryTab: " + ", ".join(still_inline))

    for name, path, expected in [
        ("ErrorMemoryIntakeActionsMixin", INTAKE_MIXIN_PATH, INTAKE_GENERAL_METHODS),
        ("ErrorMemoryProjectPathsMixin", PROJECT_PATHS_MIXIN_PATH, PROJECT_PATH_METHODS),
        ("ErrorMemoryTableDraftMixin", TABLE_DRAFT_MIXIN_PATH, TABLE_DRAFT_METHODS),
    ]:
        module = _parse(path)
        cls = _class(module, name)
        methods = _method_names(cls)
        missing = sorted(expected - methods)
        if missing:
            raise AssertionError(f"{name} missing methods: " + ", ".join(missing))
        _assert_line_band(path, minimum=80, maximum=500)

    tab_text = TAB_PATH.read_text(encoding="utf-8")
    required_tab_markers = [
        "class ErrorMemoryTab(ErrorMemoryProjectPathsMixin, ErrorMemoryTableDraftMixin, ErrorMemoryIntakeActionsMixin, QWidget):",
        "AI-assisted error lesson intake",
        "Paste error formatted from AI",
        "Memorize Error",
        "Check Against Lessons",
        "Import Error Lesson ZIP",
        "QTimer.singleShot(0, self.load_pending_ai_assisted_error_lesson_intake_now)",
        "QTimer.singleShot(250, self.load_pending_ai_assisted_error_lesson_intake_now)",
    ]
    for marker in required_tab_markers:
        if marker not in tab_text:
            raise AssertionError(f"Missing protected tab marker: {marker}")

    mixin_text = INTAKE_MIXIN_PATH.read_text(encoding="utf-8")
    for marker in [
        "PENDING_AI_ASSISTED_INTAKE_DIR_NAME = 'pending_ai_assisted_error_lesson_intake'",
        "PENDING_AI_ASSISTED_INTAKE_SUFFIXES = {'.json', '.txt', '.md'}",
        "delete_matching_pending_intake_files(",
        "consume_loaded_pending_intake_file_if_matches(",
        "clear_ai_assisted_intake_after_memorize(",
    ]:
        if marker not in mixin_text:
            raise AssertionError(f"Missing pending-intake marker: {marker}")

    project_text = PROJECT_PATHS_MIXIN_PATH.read_text(encoding="utf-8")
    for marker in [
        "resolve_project_error_memory_root",
        "resolve_second_prompt_files_root",
        "QDesktopServices.openUrl",
        "QFileDialog.getExistingDirectory",
    ]:
        if marker not in project_text:
            raise AssertionError(f"Missing project-path marker: {marker}")

    table_text = TABLE_DRAFT_MIXIN_PATH.read_text(encoding="utf-8")
    for marker in [
        "Delete draft completely",
        "Active-ready saved lessons are preserved.",
        "receive_formulary_from_ai(self)",
        "import_error_lesson_zip(self)",
        "export_for_ai(self)",
    ]:
        if marker not in table_text:
            raise AssertionError(f"Missing table/draft/import marker: {marker}")

    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
