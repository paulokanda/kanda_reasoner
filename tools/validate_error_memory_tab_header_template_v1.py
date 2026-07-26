"""Validate Error Memory header-template layout behavior."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "error-memory-tab-header-template-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAZY_TABS = PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"
ERROR_MEMORY_TAB = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
MAX_MODULE_LINES = 500


def read_text(path: Path) -> str:
    """Read a project file as UTF-8 text."""
    if not path.exists():
        raise AssertionError(f"Missing expected file: {path.relative_to(PROJECT_ROOT)}")
    return path.read_text(encoding="utf-8")


def assert_contains(path: Path, marker: str) -> None:
    """Assert that a file contains a required marker."""
    text = read_text(path)
    if marker not in text:
        raise AssertionError(f"Missing marker in {path.relative_to(PROJECT_ROOT)}: {marker}")


def assert_not_contains(path: Path, marker: str) -> None:
    """Assert that a file does not contain a retired marker."""
    text = read_text(path)
    if marker in text:
        raise AssertionError(f"Retired marker still present in {path.relative_to(PROJECT_ROOT)}: {marker}")


def line_count(path: Path) -> int:
    """Return the physical line count for a source file."""
    return len(read_text(path).splitlines())


def assert_module_size(path: Path) -> None:
    """Assert that a touched module respects the 500-line hard gate."""
    count = line_count(path)
    if count > MAX_MODULE_LINES:
        raise AssertionError(
            f"{path.relative_to(PROJECT_ROOT)} has {count} lines; "
            f"maximum is {MAX_MODULE_LINES}"
        )


def class_node(path: Path, class_name: str) -> ast.ClassDef:
    """Return a class node from a Python source file."""
    tree = ast.parse(read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise AssertionError(f"Missing class {class_name} in {path.relative_to(PROJECT_ROOT)}")


def method_node(cls: ast.ClassDef, method_name: str) -> ast.FunctionDef:
    """Return a method node from a class node."""
    for node in cls.body:
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            return node
    raise AssertionError(f"Missing method {method_name}")


def call_names(node: ast.AST) -> list[str]:
    """Collect method/function attribute names called in an AST node."""
    names: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Attribute):
                names.append(func.attr)
            elif isinstance(func, ast.Name):
                names.append(func.id)
    return names


def list_literal_names(assign: ast.Assign) -> list[str]:
    """Return names from a simple list assignment."""
    if not isinstance(assign.value, ast.List):
        return []
    names: list[str] = []
    for item in assign.value.elts:
        if isinstance(item, ast.Attribute):
            names.append(item.attr)
        elif isinstance(item, ast.Name):
            names.append(item.id)
    return names


def assert_project_root_mover_scope() -> None:
    """Ensure the mover exports only Project Root label, path, and Search."""
    cls = class_node(ERROR_MEMORY_TAB, "ErrorMemoryTab")
    method = method_node(cls, "move_project_root_controls_to_layout")
    controls: list[str] = []
    for node in ast.walk(method):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "controls":
                    controls = list_literal_names(node)
    expected = [
        "project_root_header_label",
        "project_root_value_label",
        "search_project_button",
    ]
    if controls != expected:
        raise AssertionError(f"Unexpected Error Memory header controls: {controls}")

    forbidden = {
        "open_memory_button",
        "open_second_prompt_button",
        "copy_memory_path_button",
        "copy_second_prompt_path_button",
    }
    overlap = sorted(forbidden.intersection(controls))
    if overlap:
        raise AssertionError("Path action buttons moved to header: " + ", ".join(overlap))


def assert_path_buttons_remain_in_content() -> None:
    """Ensure folder/path buttons remain in the Error Memory tab content."""
    cls = class_node(ERROR_MEMORY_TAB, "ErrorMemoryTab")
    build_ui = method_node(cls, "_build_ui")
    names = call_names(build_ui)
    required_markers = [
        "path_action_row = QHBoxLayout()",
        "path_action_row.addWidget(self.open_memory_button)",
        "path_action_row.addWidget(self.open_second_prompt_button)",
        "path_action_row.addWidget(self.copy_memory_path_button)",
        "path_action_row.addWidget(self.copy_second_prompt_path_button)",
        "outer.addLayout(path_action_row)",
    ]
    for marker in required_markers:
        assert_contains(ERROR_MEMORY_TAB, marker)
    if names.count("addWidget") < 4:
        raise AssertionError("Expected path action buttons to remain in content layout")


def assert_lazy_shell_header_behavior() -> None:
    """Ensure Error Memory uses header template and hides LOADED/source row."""
    assert_contains(LAZY_TABS, "_ERROR_MEMORY_GUI_SOURCE,")
    assert_contains(LAZY_TABS, "_HEADER_TEMPLATE_ONLY_SOURCES = {")
    assert_contains(LAZY_TABS, "def _move_error_memory_project_root_controls_to_header_row")
    assert_contains(LAZY_TABS, "mover(self.tab_header_template.project_root_layout)")
    assert_contains(LAZY_TABS, "self._move_error_memory_project_root_controls_to_header_row(widget)")
    assert_not_contains(LAZY_TABS, "_move_error_memory_project_root_controls_to_status_row")
    assert_not_contains(LAZY_TABS, "Move Error Memory Project Root controls beside LOADED / Source")


def main() -> int:
    """Run focused validation for the Error Memory header-template patch."""
    assert_module_size(LAZY_TABS)
    assert_module_size(ERROR_MEMORY_TAB)
    assert_module_size(Path(__file__).resolve())
    ast.parse(read_text(LAZY_TABS), filename=str(LAZY_TABS))
    ast.parse(read_text(ERROR_MEMORY_TAB), filename=str(ERROR_MEMORY_TAB))
    assert_lazy_shell_header_behavior()
    assert_project_root_mover_scope()
    assert_path_buttons_remain_in_content()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
