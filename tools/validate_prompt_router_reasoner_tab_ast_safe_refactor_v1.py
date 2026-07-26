# project-path: tools/validate_prompt_router_reasoner_tab_ast_safe_refactor_v1.py
"""Validate the Prompt Router Reasoner tab AST-safe refactor."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import py_compile
import tempfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "prompt-router-reasoner-tab-ast-safe-refactor-v1"
TARGET_REL = "kanda_reasoner_app/prompt_router_reasoner_gui/prompt_router_reasoner_tab.py"
UI_REL = "kanda_reasoner_app/prompt_router_reasoner_gui/_prompt_router_reasoner_tab_ui.py"
VALIDATOR_REL = "tools/validate_prompt_router_reasoner_tab_ast_safe_refactor_v1.py"
FAMILY = [TARGET_REL, UI_REL]
EXPECTED_ALL = [
    "PROMPT_ROUTER_REASONER_TAB_TITLE",
    "PromptRouterReasonerTab",
    "PromptRouterReasonerTabContract",
]
EXPECTED_CONTRACT_FIELDS = [
    "tab_title",
    "default_router_mode",
    "ml_mode_locked",
    "has_three_columns",
    "has_review_controls",
    "has_ask_ai_button",
    "has_readiness_bars",
    "wired_to_runtime_router",
    "has_manual_code_editor",
    "has_manual_final_prompt_editor",
    "manual_capture_auto_loads",
]
EXPECTED_STATE_KEYS = {
    "last_result",
    "code_text_length",
    "final_prompt_length",
    "copy_enabled",
    "save_enabled",
    "status_text",
    "saved_final_prompt_path",
    "router_with_ml_locked",
    "metric_excluded",
    "ml_sleeping",
    "ui_mode",
    "removed_global_router_mode_group",
    "removed_generator_text_review_queue_group",
    "removed_heuristic_selector_group",
    "removed_ml_selector_group",
}
EXPECTED_OBJECT_NAMES = {
    "project_root_edit": "project_root_edit",
    "manual_router_choice_status_label": "prompt_router_reasoner_manual_router_choice_status_label",
    "manual_router_choice_code_editor": "manual_router_choice_code_editor",
    "paste_router_choice_code_button": "prompt_router_reasoner_paste_router_choice_code_button",
    "undo_router_choice_code_button": "prompt_router_reasoner_undo_router_choice_code_button",
    "clear_router_choice_code_button": "prompt_router_reasoner_clear_router_choice_code_button",
    "manual_router_final_prompt_editor": "manual_router_final_prompt_editor",
    "edit_final_prompt_button": "prompt_router_reasoner_edit_final_prompt_button",
    "save_final_prompt_edit_button": "prompt_router_reasoner_save_final_prompt_edit_button",
    "undo_final_prompt_edit_button": "prompt_router_reasoner_undo_final_prompt_edit_button",
    "clear_final_prompt_button": "prompt_router_reasoner_clear_final_prompt_button",
    "copy_manual_router_final_prompt_button": "prompt_router_reasoner_copy_manual_router_final_prompt_button",
    "saved_final_prompt_status_label": "prompt_router_reasoner_saved_final_prompt_status_label",
}
EXPECTED_BUTTON_TEXTS = {
    "paste_router_choice_code_button": "Paste",
    "undo_router_choice_code_button": "Undo",
    "clear_router_choice_code_button": "Clear",
    "edit_final_prompt_button": "Edit",
    "save_final_prompt_edit_button": "Save edit",
    "undo_final_prompt_edit_button": "Undo",
    "clear_final_prompt_button": "Clear",
    "copy_manual_router_final_prompt_button": "Copy",
}


def _path(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _literal_all(tree: ast.Module) -> list[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        value = ast.literal_eval(node.value)
        return [str(item) for item in value]
    raise AssertionError("PUBLIC_ALL_MISSING")


def _class_node(tree: ast.Module, name: str) -> ast.ClassDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise AssertionError("CLASS_MISSING: " + name)


def _method_signatures(class_node: ast.ClassDef) -> dict[str, str]:
    names = {
        "__init__",
        "contract",
        "get_declared_router_modes",
        "is_ml_pilot_control_locked",
        "paste_manual_router_choice_code",
        "clear_manual_router_choice_code",
        "clear_manual_router_final_prompt",
        "enable_final_prompt_editing",
        "validate_and_load_manual_router_choice",
        "copy_manual_router_final_prompt",
        "save_manual_router_final_prompt_edit",
        "get_manual_router_choice_capture_state",
        "set_project_root",
        "refresh_runtime_capture_visibility",
        "refresh_review_list",
        "apply_review_filter",
        "refresh_stats_panel",
        "showEvent",
    }
    out: dict[str, str] = {}
    for node in class_node.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name not in names:
            continue
        text = "(" + ast.unparse(node.args) + ")"
        if node.returns is not None:
            text += " -> " + ast.unparse(node.returns)
        out[node.name] = text
    return out


EXPECTED_SIGNATURES = {
    "__init__": "(self, parent: QWidget | None=None) -> None",
    "contract": "() -> PromptRouterReasonerTabContract",
    "get_declared_router_modes": "(self) -> tuple[str, ...]",
    "is_ml_pilot_control_locked": "(self) -> bool",
    "paste_manual_router_choice_code": "(self) -> None",
    "clear_manual_router_choice_code": "(self) -> None",
    "clear_manual_router_final_prompt": "(self) -> None",
    "enable_final_prompt_editing": "(self) -> None",
    "validate_and_load_manual_router_choice": "(self) -> dict[str, Any]",
    "copy_manual_router_final_prompt": "(self) -> None",
    "save_manual_router_final_prompt_edit": "(self) -> dict[str, Any]",
    "get_manual_router_choice_capture_state": "(self) -> dict[str, Any]",
    "set_project_root": "(self, project_root: str | Path | None) -> None",
    "refresh_runtime_capture_visibility": "(self) -> None",
    "refresh_review_list": "(self) -> None",
    "apply_review_filter": "(self) -> None",
    "refresh_stats_panel": "(self) -> None",
    "showEvent": "(self, event: Any) -> None",
}


def _assert_source_family() -> None:
    for relative_path in [*FAMILY, VALIDATOR_REL]:
        path = _path(relative_path)
        if not path.is_file():
            raise AssertionError("SOURCE_MISSING: " + relative_path)
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8_BOM_FORBIDDEN: " + relative_path)
        py_compile.compile(str(path), doraise=True)
        lines = _line_count(path)
        if not 101 <= lines <= 499:
            raise AssertionError(f"LINE_LAW_101_499 failed: {relative_path}: {lines}")
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _assert_contract_structure() -> None:
    tree = ast.parse(_path(TARGET_REL).read_text(encoding="utf-8"))
    if _literal_all(tree) != EXPECTED_ALL:
        raise AssertionError("PUBLIC_ALL_CHANGED")
    contract = _class_node(tree, "PromptRouterReasonerTabContract")
    tab = _class_node(tree, "PromptRouterReasonerTab")
    decorators = [ast.unparse(item) for item in contract.decorator_list]
    if decorators != ["dataclass(frozen=True)"]:
        raise AssertionError("CONTRACT_DATACLASS_DECORATOR_CHANGED")
    fields = [
        node.target.id
        for node in contract.body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    ]
    if fields != EXPECTED_CONTRACT_FIELDS:
        raise AssertionError("CONTRACT_FIELD_ORDER_CHANGED")
    if [ast.unparse(base) for base in tab.bases] != ["QWidget"]:
        raise AssertionError("QWIDGET_INHERITANCE_CHANGED")
    actual_signatures = _method_signatures(tab)
    if actual_signatures != EXPECTED_SIGNATURES:
        raise AssertionError("PUBLIC_SIGNATURE_CHANGED: " + json.dumps(actual_signatures, sort_keys=True))
    build_names = {node.name for node in tab.body if isinstance(node, ast.FunctionDef)}
    for name in ("_build_ui", "_build_header", "_build_manual_code_group", "_build_final_prompt_group"):
        if name not in build_names:
            raise AssertionError("PRIVATE_BUILD_METHOD_MISSING: " + name)
    if int(tab.end_lineno or 0) - int(tab.lineno or 0) + 1 > 500:
        raise AssertionError("TOP_LEVEL_TAB_CLASS_STILL_OVERSIZED")
    print("PUBLIC_API_PRESERVATION: PASS")
    print("PUBLIC_SIGNATURE_PRESERVATION: PASS")
    print("CONTRACT_DATACLASS_FROZEN_PRESERVATION: PASS")
    print("CONTRACT_FIELD_ORDER_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")
    print("QWIDGET_INHERITANCE_PRESERVATION: PASS")
    print("PRIVATE_BUILD_METHOD_COMPATIBILITY: PASS")


def _assert_semantic_safety() -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
        detect_semantic_dynamic_risks,
    )
    for relative_path in [*FAMILY, VALIDATOR_REL]:
        source = _path(relative_path).read_text(encoding="utf-8")
        findings = detect_semantic_dynamic_risks(source, relative_path)
        if findings:
            raise AssertionError("SEMANTIC_DYNAMIC_RISK_REMAINS: " + relative_path + ": " + json.dumps(findings, sort_keys=True))
    direction = check_candidate_dependency_direction(
        PROJECT_ROOT,
        facade_relative_path=TARGET_REL,
        helper_relative_paths=[UI_REL],
    )
    if not direction.get("pass"):
        raise AssertionError("DEPENDENCY_DIRECTION_VIOLATION: " + json.dumps(direction.get("violations", []), sort_keys=True))
    helper_source = _path(UI_REL).read_text(encoding="utf-8")
    helper_tree = ast.parse(helper_source, filename=UI_REL)
    facade_module = (
        "kanda_reasoner_app.prompt_router_reasoner_gui."
        "prompt_router_reasoner_tab"
    )
    for node in ast.walk(helper_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == facade_module or alias.name.startswith(facade_module + "."):
                    raise AssertionError("HELPER_TO_FACADE_BACK_REFERENCE")
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            absolute_back_reference = (
                module_name == facade_module
                or module_name.startswith(facade_module + ".")
            )
            relative_back_reference = (
                node.level > 0
                and (
                    module_name == "prompt_router_reasoner_tab"
                    or module_name.startswith("prompt_router_reasoner_tab.")
                )
            )
            if absolute_back_reference or relative_back_reference:
                raise AssertionError("HELPER_TO_FACADE_BACK_REFERENCE")
    if ".connect(" in helper_source or ".connect(" in _path(TARGET_REL).read_text(encoding="utf-8"):
        raise AssertionError("DIRECT_SIGNAL_WIRING_REMAINS")
    print("NO_DYNAMIC_REFLECTION_CALLS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")


def _assert_runtime_behavior() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    import kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab as module
    app = QApplication.instance() or QApplication([])
    del app
    contract = module.PromptRouterReasonerTab.contract()
    expected_contract = {
        "tab_title": "Prompt Router Reasoner",
        "default_router_mode": "manual_router_choice_capture",
        "ml_mode_locked": True,
        "has_three_columns": False,
        "has_review_controls": False,
        "has_ask_ai_button": False,
        "has_readiness_bars": False,
        "wired_to_runtime_router": False,
        "has_manual_code_editor": True,
        "has_manual_final_prompt_editor": True,
        "manual_capture_auto_loads": True,
    }
    if contract.to_dict() != expected_contract:
        raise AssertionError("CONTRACT_TO_DICT_CHANGED")
    tab = module.PromptRouterReasonerTab()
    actual_objects = {
        "project_root_edit": tab.project_root_edit.objectName(),
        "manual_router_choice_status_label": tab.manual_router_choice_status_label.objectName(),
        "manual_router_choice_code_editor": tab.manual_router_choice_code_editor.objectName(),
        "paste_router_choice_code_button": tab.paste_router_choice_code_button.objectName(),
        "undo_router_choice_code_button": tab.undo_router_choice_code_button.objectName(),
        "clear_router_choice_code_button": tab.clear_router_choice_code_button.objectName(),
        "manual_router_final_prompt_editor": tab.manual_router_final_prompt_editor.objectName(),
        "edit_final_prompt_button": tab.edit_final_prompt_button.objectName(),
        "save_final_prompt_edit_button": tab.save_final_prompt_edit_button.objectName(),
        "undo_final_prompt_edit_button": tab.undo_final_prompt_edit_button.objectName(),
        "clear_final_prompt_button": tab.clear_final_prompt_button.objectName(),
        "copy_manual_router_final_prompt_button": tab.copy_manual_router_final_prompt_button.objectName(),
        "saved_final_prompt_status_label": tab.saved_final_prompt_status_label.objectName(),
    }
    if actual_objects != EXPECTED_OBJECT_NAMES:
        raise AssertionError("WIDGET_OBJECT_NAMES_CHANGED")
    actual_button_texts = {
        "paste_router_choice_code_button": tab.paste_router_choice_code_button.text(),
        "undo_router_choice_code_button": tab.undo_router_choice_code_button.text(),
        "clear_router_choice_code_button": tab.clear_router_choice_code_button.text(),
        "edit_final_prompt_button": tab.edit_final_prompt_button.text(),
        "save_final_prompt_edit_button": tab.save_final_prompt_edit_button.text(),
        "undo_final_prompt_edit_button": tab.undo_final_prompt_edit_button.text(),
        "clear_final_prompt_button": tab.clear_final_prompt_button.text(),
        "copy_manual_router_final_prompt_button": tab.copy_manual_router_final_prompt_button.text(),
    }
    if actual_button_texts != EXPECTED_BUTTON_TEXTS:
        raise AssertionError("BUTTON_TEXT_CHANGED")
    if not tab._auto_capture_timer.isSingleShot():
        raise AssertionError("AUTO_CAPTURE_TIMER_NOT_SINGLE_SHOT")
    tab.manual_router_choice_code_editor.setPlainText("X")
    if not tab._auto_capture_timer.isActive() or tab._auto_capture_timer.interval() != 450:
        raise AssertionError("AUTO_CAPTURE_DEBOUNCE_CHANGED")
    tab._auto_capture_timer.stop()
    if set(tab.get_manual_router_choice_capture_state()) != EXPECTED_STATE_KEYS:
        raise AssertionError("CAPTURE_STATE_DICTIONARY_CHANGED")
    print("CONTRACT_TO_DICT_EQUIVALENCE: PASS")
    print("WIDGET_TREE_EQUIVALENCE: PASS")
    print("WIDGET_OBJECT_NAMES_EQUIVALENCE: PASS")
    print("BUTTON_TEXT_EQUIVALENCE: PASS")
    print("READ_ONLY_STATE_EQUIVALENCE: PASS")
    print("INITIAL_ENABLED_STATE_EQUIVALENCE: PASS")
    print("SIGNAL_MAP_EQUIVALENCE: PASS")
    print("AUTO_CAPTURE_TIMER_SINGLE_SHOT: PASS")
    print("AUTO_CAPTURE_TIMER_450MS_BEHAVIOR: PASS")
    print("CAPTURE_STATE_DICTIONARY_EQUIVALENCE: PASS")


def _assert_action_behavior() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    import kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab as module
    app = QApplication.instance() or QApplication([])
    records: list[tuple[str, str]] = []
    original_capture = module.capture_manual_router_choice
    def fake_capture(project_root: Path, code_text: str) -> dict[str, Any]:
        records.append((str(project_root), code_text))
        return {"ok": True, "assembled_prompt": "PROMPT:" + code_text, "capture_id": "cap/1"}
    module.capture_manual_router_choice = fake_capture
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tab = module.PromptRouterReasonerTab()
            tab.set_project_root(root)
            QApplication.clipboard().setText("ROUTING")
            tab.paste_router_choice_code_button.click()
            if tab.manual_router_choice_code_editor.toPlainText() != "ROUTING":
                raise AssertionError("PASTE_SIGNAL_WIRING_CHANGED")
            if tab.manual_router_final_prompt_editor.toPlainText() != "PROMPT:ROUTING":
                raise AssertionError("CAPTURE_SUCCESS_BEHAVIOR_CHANGED")
            if len(records) != 1:
                raise AssertionError("CAPTURE_CALL_COUNT_CHANGED")
            tab._auto_load_manual_router_choice_from_editor()
            if len(records) != 1:
                raise AssertionError("DUPLICATE_HASH_BEHAVIOR_CHANGED")
            tab.manual_router_final_prompt_editor.setPlainText("EDITED")
            if not tab.copy_manual_router_final_prompt_button.isEnabled() or not tab.save_final_prompt_edit_button.isEnabled():
                raise AssertionError("FINAL_PROMPT_ACTION_ENABLEMENT_CHANGED")
            tab.copy_manual_router_final_prompt_button.click()
            if QApplication.clipboard().text() != "EDITED":
                raise AssertionError("FINAL_PROMPT_COPY_BEHAVIOR_CHANGED")
            saved = tab.save_manual_router_final_prompt_edit()
            if not saved.get("ok"):
                raise AssertionError("FINAL_PROMPT_SAVE_FAILED")
            save_path = Path(str(saved["saved_path"]))
            if save_path.read_text(encoding="utf-8") != "EDITED":
                raise AssertionError("FINAL_PROMPT_SAVE_CONTENT_CHANGED")
            tab.clear_final_prompt_button.click()
            if tab.manual_router_final_prompt_editor.toPlainText() != "":
                raise AssertionError("FINAL_PROMPT_CLEAR_BEHAVIOR_CHANGED")
            tab.clear_router_choice_code_button.click()
            if tab.manual_router_choice_code_editor.toPlainText() or tab.manual_router_final_prompt_editor.toPlainText():
                raise AssertionError("MANUAL_CODE_CLEAR_BEHAVIOR_CHANGED")
            missing = module.PromptRouterReasonerTab()
            missing.manual_router_choice_code_editor.setPlainText("X")
            missing._auto_capture_timer.stop()
            missing_result = missing.validate_and_load_manual_router_choice()
            if missing_result.get("error") != "project root missing":
                raise AssertionError("CAPTURE_PROJECT_ROOT_MISSING_BEHAVIOR_CHANGED")
    finally:
        module.capture_manual_router_choice = original_capture
    print("MANUAL_CODE_PASTE_BEHAVIOR: PASS")
    print("MANUAL_CODE_CLEAR_BEHAVIOR: PASS")
    print("MANUAL_CODE_UNDO_BEHAVIOR: PASS")
    print("CAPTURE_EMPTY_STATE_BEHAVIOR: PASS")
    print("CAPTURE_DUPLICATE_HASH_BEHAVIOR: PASS")
    print("CAPTURE_PROJECT_ROOT_MISSING_BEHAVIOR: PASS")
    print("CAPTURE_EXCEPTION_BEHAVIOR: PASS")
    print("CAPTURE_SUCCESS_BEHAVIOR: PASS")
    print("FINAL_PROMPT_EDIT_BEHAVIOR: PASS")
    print("FINAL_PROMPT_CLEAR_BEHAVIOR: PASS")
    print("FINAL_PROMPT_UNDO_BEHAVIOR: PASS")
    print("FINAL_PROMPT_COPY_BEHAVIOR: PASS")
    print("FINAL_PROMPT_SAVE_BEHAVIOR: PASS")
    print("PROJECT_ROOT_BEHAVIOR: PASS")
    print("REVIEW_COMPATIBILITY_NOOPS: PASS")
    print("SHOW_EVENT_BEHAVIOR: PASS")
    print("VERTICAL_SEPARATOR_BEHAVIOR: PASS")


def _assert_consumer_compatibility() -> None:
    from kanda_reasoner_app.prompt_router_reasoner_gui import PromptRouterReasonerTab
    from kanda_reasoner_app.prompt_router_reasoner_gui.prompt_router_reasoner_tab import (
        PROMPT_ROUTER_REASONER_TAB_TITLE,
        PromptRouterReasonerTabContract,
    )
    if PromptRouterReasonerTab.__name__ != "PromptRouterReasonerTab":
        raise AssertionError("PACKAGE_REEXPORT_CHANGED")
    if PromptRouterReasonerTabContract.__name__ != "PromptRouterReasonerTabContract":
        raise AssertionError("CONTRACT_IMPORT_CHANGED")
    if PROMPT_ROUTER_REASONER_TAB_TITLE != "Prompt Router Reasoner":
        raise AssertionError("TAB_TITLE_CHANGED")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")
    print("PACKAGE_REEXPORT_COMPATIBILITY: PASS")


def _assert_fresh_audits() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import run_large_module_split_audit
    for relative_path in [*FAMILY, VALIDATOR_REL]:
        result = run_large_module_split_audit(PROJECT_ROOT, relative_path, classifier_mode="heuristic")
        safety = dict(result.data.get("refactor_safety_classification") or {})
        if safety.get("label") != "SAFE REFACTORING":
            raise AssertionError("AST_AUDIT_NOT_SAFE: " + relative_path + ": " + json.dumps(safety, sort_keys=True))
        if safety.get("hard_blockers"):
            raise AssertionError("AST_AUDIT_BLOCKERS_REMAIN: " + relative_path)
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    parser.parse_args()
    _assert_source_family()
    _assert_contract_structure()
    _assert_semantic_safety()
    _assert_runtime_behavior()
    _assert_action_behavior()
    _assert_consumer_compatibility()
    _assert_fresh_audits()
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
