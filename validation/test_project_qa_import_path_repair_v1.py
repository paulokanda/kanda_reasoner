"""Validate Project Q&A import path repair v1.

This validation is static by design because local developer machines have
PySide6 while the AI build sandbox may not. It protects the load failure that
happened after the normal-source migration: helper modules imported the stale
reasoner_engine.main_window_help package and the shell still advertised the old
project_reasoner_v10 candidate.
"""

from __future__ import annotations

import ast
import py_compile
import zipfile
from pathlib import Path

FEATURE_ID = "project-qa-import-path-repair-v1"
VALIDATION_MARKER = "VALIDATION OK: project-qa-import-path-repair-v1"
STATUS_MARKER = "STATUS: IN_SYNC"
ZIP_MARKER = "ZIP CONTRACT: PASS"
PATCH_NAME = "kanda_project_qa_import_path_repair_v1_patch.zip"

PROJECT_ROOT = Path.cwd()

TOOL_SPECS = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "tool_specs.py"
ANALYSIS_CONTROLLER = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine" / "ai_reasoner_main_window_help" / "analysis_controller.py"
ANSWER_PRESENTER = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine" / "ai_reasoner_main_window_help" / "answer_presenter.py"
MAIN_WINDOW = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine" / "ai_reasoner_main_window.py"
UI_COMPONENTS = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine" / "ai_reasoner_main_window_help" / "ui_components.py"

EXPECTED_ZIP_MEMBERS = {
    "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/analysis_controller.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/answer_presenter.py",
    "validation/test_project_qa_import_path_repair_v1.py",
    "KANDA_FREEZE_HINT.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    require(path.exists(), "missing file: " + str(path))
    text = path.read_text(encoding="utf-8")
    require(text.isascii(), "non-ASCII character found in " + str(path))
    return text


def assert_compiles() -> None:
    for path in (TOOL_SPECS, ANALYSIS_CONTROLLER, ANSWER_PRESENTER, MAIN_WINDOW, UI_COMPONENTS):
        py_compile.compile(str(path), doraise=True)


def assert_helper_imports() -> None:
    expected = "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.ui_components"
    stale = "kanda_reasoner_app.reasoner_engine.main_window_help.ui_components"
    for path in (ANALYSIS_CONTROLLER, ANSWER_PRESENTER):
        text = read_text(path)
        require(expected in text, "expected canonical ui_components import missing in " + str(path))
        require(stale not in text, "stale main_window_help import remains in " + str(path))


def _project_qa_tool_spec_node(tree: ast.Module) -> ast.Call:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func_name = getattr(node.func, "id", "")
        if func_name != "ToolSpec":
            continue
        for keyword in node.keywords:
            if keyword.arg == "step_title" and isinstance(keyword.value, ast.Constant):
                if keyword.value.value == "Project Q&A":
                    return node
    raise AssertionError("Project Q&A ToolSpec not found")


def _literal_tuple_of_strings(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Tuple):
        values = []
        for item in node.elts:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                values.append(item.value)
            elif isinstance(item, ast.Call) and getattr(item.func, "id", "") == "_module_path":
                parts = []
                for arg in item.args:
                    require(isinstance(arg, ast.Constant) and isinstance(arg.value, str), "nonliteral _module_path argument")
                    parts.append(arg.value)
                values.append("kanda_reasoner_app." + ".".join(parts))
            else:
                raise AssertionError("unsupported module candidate expression")
        return tuple(values)
    raise AssertionError("expected tuple literal")


def assert_tool_spec() -> None:
    text = read_text(TOOL_SPECS)
    tree = ast.parse(text)
    node = _project_qa_tool_spec_node(tree)
    keyword_map = {kw.arg: kw.value for kw in node.keywords}

    module_candidates = _literal_tuple_of_strings(keyword_map["module_candidates"])
    require(
        module_candidates == ("kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window",),
        "Project Q&A must have only the canonical normal-source module candidate",
    )
    require(
        not any("project_reasoner_v10" in item for item in module_candidates),
        "Project Q&A module candidates must not include project_reasoner_v10",
    )

    source_node = keyword_map["source_hint"]
    require(isinstance(source_node, ast.Call), "source_hint must use _source_path")
    require(getattr(source_node.func, "id", "") == "_source_path", "source_hint must use _source_path")
    source_parts = [arg.value for arg in source_node.args if isinstance(arg, ast.Constant)]
    require(source_parts == ["reasoner_engine", "ai_reasoner_main_window.py"], "Project Q&A source_hint must point to reasoner_engine normal source")
    require('source_hint=_source_path("project_reasoner_v10", "ai_reasoner_main_window.py")' not in text, "stale project_reasoner_v10 source_hint remains")


def locate_patch_zip() -> Path:
    project_name = PROJECT_ROOT.name
    drive = PROJECT_ROOT.anchor
    candidates = []
    if drive:
        candidates.append(Path(drive) / PATCH_NAME)
        candidates.append(Path(drive) / (project_name + "_delete_after_daily_work") / PATCH_NAME)
    candidates.append(PROJECT_ROOT / PATCH_NAME)
    for path in candidates:
        if path.exists():
            return path
    raise AssertionError("patch ZIP not found for ZIP contract check: " + PATCH_NAME)


def assert_zip_contract() -> None:
    patch_zip = locate_patch_zip()
    with zipfile.ZipFile(patch_zip, "r") as zf:
        members = set(zf.namelist())
    require(members == EXPECTED_ZIP_MEMBERS, "unexpected ZIP members: " + repr(sorted(members)))


def main() -> int:
    assert_compiles()
    assert_helper_imports()
    assert_tool_spec()
    assert_zip_contract()
    print(VALIDATION_MARKER)
    print(STATUS_MARKER)
    print(ZIP_MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
