# project-path: scripts/validate_local_freeze_single_formulary_window_v1.py
"""Validate the Local Freeze Entry single-formulary-window guard."""
from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "_local_freeze_dialog_runtime.py"
SUPPORT_TARGET = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "_local_freeze_dialog_widgets.py"
TAB_TARGET = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"
FEATURE_ID = "local-freeze-single-formulary-window-v1"


def _source() -> str:
    """Support source behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    return TARGET.read_text(encoding="utf-8")


def _method_source(tree: ast.Module, name: str, source: str) -> str:
    """Support method source behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    name : str
        The name value.
    source : str
        The source value.
    
    Returns
    -------
    str
        The string result.
    """
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            segment = ast.get_source_segment(source, node)
            if not segment:
                raise AssertionError(f"Could not recover source segment for {name}")
            return segment
    raise AssertionError(f"Missing method: {name}")


def _assert_contains(text: str, fragment: str, label: str) -> None:
    """Support assert contains behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    fragment : str
        The fragment value.
    label : str
        The label value.
    """
    
    if fragment not in text:
        raise AssertionError(f"Missing {label}: {fragment}")


def _validate_guard_methods(tree: ast.Module, source: str) -> None:
    """Support validate guard methods behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    source : str
        The source value.
    """
    
    guard = _method_source(tree, "_raise_existing_local_freeze_dialog", source)
    cleanup = _method_source(tree, "_clear_local_freeze_dialog_reference", source)

    _assert_contains(guard, "self._local_freeze_dialog", "dialog reference read")
    _assert_contains(guard, "dialog.isVisible()", "visible-dialog check")
    _assert_contains(guard, "dialog.raise_()", "existing dialog raise")
    _assert_contains(guard, "dialog.activateWindow()", "existing dialog activation")
    _assert_contains(guard, "return True", "duplicate-open block return")
    _assert_contains(guard, "self._local_freeze_dialog = None", "stale dialog reference cleanup")
    _assert_contains(guard, "A Local Freeze Entry formulary window is already open.", "user-facing duplicate-open message")
    _assert_contains(guard, "Close it before opening another one.", "user-facing duplicate-open close guidance")

    _assert_contains(cleanup, "if self._local_freeze_dialog is dialog", "same-dialog cleanup guard")
    _assert_contains(cleanup, "self._local_freeze_dialog = None", "close releases dialog guard")
    _assert_contains(cleanup, "self._local_freeze_preview = None", "close clears stale preview")


def _validate_open_method(tree: ast.Module, source: str) -> None:
    """Support validate open method behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    source : str
        The source value.
    """
    
    open_method = _method_source(tree, "_open_local_freeze_entry_dialog", source)
    guard_index = open_method.find("self._raise_existing_local_freeze_dialog()")
    require_root_index = open_method.find("self._require_project_root()")
    create_dialog_index = open_method.find("widgets = build_local_freeze_dialog_widgets")
    if guard_index < 0:
        raise AssertionError("_open_local_freeze_entry_dialog must call the single-window guard")
    if require_root_index < 0:
        raise AssertionError("_open_local_freeze_entry_dialog must still require a project root")
    if create_dialog_index < 0:
        raise AssertionError("_open_local_freeze_entry_dialog must still create the local freeze dialog")
    if not guard_index < require_root_index < create_dialog_index:
        raise AssertionError("single-window guard must run before project-root resolution and before QDialog creation")

    _assert_contains(open_method, "def on_finished", "finished handler")
    _assert_contains(open_method, "ai_runtime.close()", "AI runtime shutdown")
    _assert_contains(open_method, "self._clear_local_freeze_dialog_reference(dialog)", "finished handler cleanup")
    _assert_contains(open_method, "dialog.finished.connect(on_finished)", "finished signal binding")
    _assert_contains(open_method, "self._local_freeze_dialog = dialog", "active dialog assignment")


def _validate_protected_freeze_flow_strings(source: str) -> None:
    """Support validate protected freeze flow strings behavior.
    
    Parameters
    ----------
    source : str
        The source value.
    """
    
    protected_fragments = [
        "Preview Freeze Entry",
        "Confirm and Write Freeze Entry",
        "Ignore this Freeze",
        "Preview is read-only;",
        "Confirm and Write uses the button click as confirmation and closes immediately.",
        "write_confirmed_freeze_entry(",
        "confirmation=True",
        "mark_latest_freeze_hint_used(",
        "project_root, freeze_id=",
        "refresh_ai_compliance_context(project_root)",
        "parse_args([]) must keep the safe read-only --check default",  # absent by design, checked in startup guard, not here
    ]
    for fragment in protected_fragments[:-1]:
        _assert_contains(source, fragment, "protected local-freeze behavior")


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    source = _source()
    tree = ast.parse(source, filename=str(TARGET))
    support_source = SUPPORT_TARGET.read_text(encoding="utf-8")
    support_tree = ast.parse(support_source, filename=str(SUPPORT_TARGET))
    tab_source = TAB_TARGET.read_text(encoding="utf-8")
    ast.parse(tab_source, filename=str(TAB_TARGET))
    _validate_guard_methods(support_tree, support_source)
    _validate_open_method(tree, source)
    _validate_protected_freeze_flow_strings(source + support_source)
    _assert_contains(tab_source, "FreezeLocalEntryRuntimeMixin", "runtime mixin delegation")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
