# project-path: scripts/validate_error_memory_tab_refactor_completion_guard_v1.py
"""Validate Error Memory tab refactor completion guard.

This guard intentionally performs no source split. It freezes the post-Train-Car-1
state as complete under the v7.2 no-tiny-helper rule while preserving the
high-risk UI builder in the public QWidget tab shell.
"""
from __future__ import annotations

__all__ = [
    "main",
]

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PKG = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui"
TAB_PATH = PKG / "error_memory_tab.py"

FEATURE_ID = "-".join([
    "error",
    "memory",
    "tab",
    "refactor",
    "completion",
    "guard",
    "v1",
])

CORE_MODULES = {
    "error_memory_tab.py": "public QWidget tab shell and high-risk _build_ui wiring",
    "_intake_actions_mixin.py": "pending-intake/general action wrappers",
    "_project_paths_mixin.py": "project-root/path controls and pending path resolution",
    "_table_draft_mixin.py": "table, draft, import/export, preview actions",
}

SUPPORT_MODULES = {
    "_text_payloads.py": "text payload parsing/normalization helpers",
    "_pending_sources.py": "pending intake source discovery and matching",
    "_pending_loader.py": "pending intake load/duplicate warning helpers",
    "_table_view.py": "table rendering and row selection helpers",
    "_lesson_actions.py": "lesson save/delete/status/supersede actions",
    "_memorize_flow.py": "active-ready memorize flow",
    "_clipboard_export.py": "clipboard and AI export helpers",
}

SUBSTANTIVE_MODULES = [
    "_intake_actions_mixin.py",
    "_project_paths_mixin.py",
    "_table_draft_mixin.py",
    "_text_payloads.py",
    "_pending_sources.py",
    "_pending_loader.py",
    "_table_view.py",
    "_lesson_actions.py",
    "_memorize_flow.py",
    "_clipboard_export.py",
]

MIXIN_OWNERSHIP = {
    "_intake_actions_mixin.py": {
        "class_name": "ErrorMemoryIntakeActionsMixin",
        "methods": [
            "load_pending_ai_assisted_error_lesson_intake_now",
            "_load_pending_ai_assisted_error_lesson_intake",
            "_copy_error_lesson_intake_blueprint_to_clipboard",
            "_copy_ai_assisted_intake_error_draft_to_clipboard",
            "_clean_intake_window",
            "_delete_matching_pending_intake_files",
            "_clear_ai_assisted_intake_after_memorize",
            "_memorize_error_from_text_window",
            "_check_against_lessons",
            "_show_repeat_guard_report",
        ],
    },
    "_project_paths_mixin.py": {
        "class_name": "ErrorMemoryProjectPathsMixin",
        "methods": [
            "set_project_root",
            "_on_project_root_field_changed",
            "_current_project_root",
            "_search_project_root",
            "_copy_path_to_clipboard",
            "_refresh_paths",
            "_pending_path_for_row",
            "_open_folder",
        ],
    },
    "_table_draft_mixin.py": {
        "class_name": "ErrorMemoryTableDraftMixin",
        "methods": [
            "_reload_table",
            "_load_selected_lesson_into_preview",
            "_save_preview_lesson",
            "_delete_selected_lesson",
            "_set_selected_lesson_status",
            "_supersede_selected_lesson",
            "_copy_error_draft_to_clipboard",
            "_delete_current_draft_completely",
            "_receive_formulary_from_ai",
            "_import_error_lesson_zip",
            "_export_for_ai",
        ],
    },
}

SUPPORT_OWNERSHIP = {
    "_pending_loader.py": [
        "load_pending_ai_assisted_error_lesson_intake_now",
        "load_pending_ai_assisted_error_lesson_intake",
        "show_duplicate_pending_intake_warning",
    ],
    "_pending_sources.py": [
        "candidate_pending_ai_assisted_intake_dirs",
        "delete_matching_pending_intake_files",
        "pending_intake_files_for_candidate_dirs",
    ],
    "_lesson_actions.py": [
        "save_preview_lesson",
        "delete_selected_lesson",
        "set_selected_lesson_status",
        "supersede_selected_lesson",
    ],
    "_memorize_flow.py": [
        "memorize_error_from_text_window",
        "consume_loaded_pending_intake_file_if_matches",
        "clear_ai_assisted_intake_after_memorize",
    ],
    "_clipboard_export.py": [
        "copy_complete_error_memory_json_to_clipboard",
        "copy_error_draft_to_clipboard",
        "export_for_ai",
    ],
}

MOVED_COMPAT_METHODS = set()
for spec in MIXIN_OWNERSHIP.values():
    MOVED_COMPAT_METHODS.update(spec["methods"])

PROTECTED_TAB_MARKERS = [
    "class ErrorMemoryTab(ErrorMemoryProjectPathsMixin, ErrorMemoryTableDraftMixin, ErrorMemoryIntakeActionsMixin, QWidget):",
    "def _build_ui(self) -> None:",
    "AI-assisted error lesson intake",
    "Paste error formatted from AI",
    "Memorize Error",
    "Check Against Lessons",
    "Import Error Lesson ZIP",
    "QTimer.singleShot(0, self.load_pending_ai_assisted_error_lesson_intake_now)",
    "QTimer.singleShot(250, self.load_pending_ai_assisted_error_lesson_intake_now)",
]

PROTECTED_BEHAVIOR_MARKERS = {
    "_intake_actions_mixin.py": [
        "PENDING_AI_ASSISTED_INTAKE_DIR_NAME = 'pending_ai_assisted_error_lesson_intake'",
        "PENDING_AI_ASSISTED_INTAKE_SUFFIXES = {'.json', '.txt', '.md'}",
        "delete_matching_pending_intake_files(",
        "consume_loaded_pending_intake_file_if_matches(",
        "clear_ai_assisted_intake_after_memorize(",
    ],
    "_table_draft_mixin.py": [
        "Active-ready saved lessons are preserved.",
        "delete_current_draft_completely(self)",
        "receive_formulary_from_ai(self)",
        "import_error_lesson_zip(self)",
        "export_for_ai(self)",
    ],
    "_project_paths_mixin.py": [
        "resolve_project_error_memory_root",
        "resolve_second_prompt_files_root",
        "QDesktopServices.openUrl",
        "QFileDialog.getExistingDirectory",
    ],
}


def _assert(condition: bool, message: str) -> None:
    """Support assert behavior.
    
    Parameters
    ----------
    condition : bool
        The condition value.
    message : str
        The message text.
    """
    
    if not condition:
        raise AssertionError(message)


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
    raise AssertionError(f"missing class {name}")


def _method_names(cls: ast.ClassDef) -> set[str]:
    """Support method names behavior.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {node.name for node in cls.body if isinstance(node, ast.FunctionDef)}


def _top_level_functions(path: Path) -> set[str]:
    """Support top level functions behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {node.name for node in _parse(path).body if isinstance(node, ast.FunctionDef)}


def _base_names(cls: ast.ClassDef) -> list[str]:
    """Support base names behavior.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    result: list[str] = []
    for base in cls.bases:
        if isinstance(base, ast.Name):
            result.append(base.id)
        else:
            result.append(ast.unparse(base))
    return result


def _module_text(name: str) -> str:
    """Support module text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return (PKG / name).read_text(encoding="utf-8")


def _assert_line_policy() -> None:
    """Support assert line policy behavior.
    """
    
    counts = {name: _line_count(PKG / name) for name in {**CORE_MODULES, **SUPPORT_MODULES}}
    _assert(counts["error_memory_tab.py"] <= 500, f"error_memory_tab.py exceeds v7.2 maximum: {counts['error_memory_tab.py']}")
    _assert(counts["error_memory_tab.py"] >= 300, "error_memory_tab.py became suspiciously hollow; high-risk _build_ui should remain in shell")
    for name in SUBSTANTIVE_MODULES:
        _assert(counts[name] <= 500, f"substantive Error Memory GUI helper exceeds v7.2 maximum: {name}={counts[name]}")
        _assert(counts[name] >= 80, f"substantive Error Memory GUI helper became suspiciously tiny: {name}={counts[name]}")


def _assert_tab_shell() -> None:
    """Support assert tab shell behavior.
    """
    
    module = _parse(TAB_PATH)
    cls = _class(module, "ErrorMemoryTab")
    bases = _base_names(cls)
    expected = [
        "ErrorMemoryProjectPathsMixin",
        "ErrorMemoryTableDraftMixin",
        "ErrorMemoryIntakeActionsMixin",
        "QWidget",
    ]
    _assert(bases == expected, f"unexpected ErrorMemoryTab bases: {bases}")
    tab_methods = _method_names(cls)
    _assert("__init__" in tab_methods, "ErrorMemoryTab no longer owns __init__")
    _assert("showEvent" in tab_methods, "ErrorMemoryTab no longer owns showEvent")
    _assert("_build_ui" in tab_methods, "high-risk _build_ui no longer remains in ErrorMemoryTab shell")
    still_inline = sorted(MOVED_COMPAT_METHODS & tab_methods)
    _assert(not still_inline, "moved compatibility wrappers returned inline to ErrorMemoryTab: " + ", ".join(still_inline))
    tab_text = TAB_PATH.read_text(encoding="utf-8")
    for marker in PROTECTED_TAB_MARKERS:
        _assert(marker in tab_text, f"missing protected Error Memory tab marker: {marker}")


def _assert_mixins_and_support_ownership() -> None:
    """Support assert mixins and support ownership behavior.
    """
    
    for module_name, spec in MIXIN_OWNERSHIP.items():
        path = PKG / module_name
        cls = _class(_parse(path), spec["class_name"])
        methods = _method_names(cls)
        for method in spec["methods"]:
            _assert(method in methods, f"{module_name} no longer exposes compatibility wrapper: {method}")

    for module_name, functions in SUPPORT_OWNERSHIP.items():
        top_functions = _top_level_functions(PKG / module_name)
        for function_name in functions:
            _assert(function_name in top_functions, f"{module_name} no longer owns support function: {function_name}")

    for module_name, markers in PROTECTED_BEHAVIOR_MARKERS.items():
        text = _module_text(module_name)
        for marker in markers:
            _assert(marker in text, f"{module_name} missing protected behavior marker: {marker}")


def _assert_public_api_and_compat_text() -> None:
    """Support assert public api and compat text behavior.
    """
    
    tab_text = TAB_PATH.read_text(encoding="utf-8")
    for marker in [
        "__all__ = [",
        "'ErrorMemoryTab'",
        "'PENDING_AI_ASSISTED_INTAKE_DIR_NAME'",
        "'PENDING_AI_ASSISTED_INTAKE_SUFFIXES'",
    ]:
        _assert(marker in tab_text, f"missing public export marker: {marker}")



def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    for name in {**CORE_MODULES, **SUPPORT_MODULES}:
        _assert((PKG / name).exists(), f"missing Error Memory GUI refactor module: {name}")

    _assert_line_policy()
    _assert_tab_shell()
    _assert_mixins_and_support_ownership()
    _assert_public_api_and_compat_text()

    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
