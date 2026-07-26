"""Validate Architecture Review Copy Path button for AST target path."""
from __future__ import annotations

import ast
from pathlib import Path

FEATURE_ID = "architecture-review-copy-ast-target-path-v1"
TARGET = Path("kanda_reasoner_app/manage_architecture/manage_architecture_gui.py")


def _source() -> str:
    return TARGET.read_text(encoding="utf-8")


def _class_node(tree: ast.AST, name: str) -> ast.ClassDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise AssertionError(f"class not found: {name}")


def _method_node(cls: ast.ClassDef, name: str) -> ast.FunctionDef:
    for node in cls.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"method not found: {name}")


def _attr_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for item in ast.walk(node):
        if isinstance(item, ast.Attribute):
            names.add(item.attr)
    return names


def _literal_texts(node: ast.AST) -> set[str]:
    return {item.value for item in ast.walk(node) if isinstance(item, ast.Constant) and isinstance(item.value, str)}


def _find_ordered_markers(source: str, markers: list[str]) -> None:
    pos = -1
    for marker in markers:
        next_pos = source.find(marker, pos + 1)
        if next_pos < 0:
            raise AssertionError(f"marker not found after offset {pos}: {marker!r}")
        pos = next_pos


def main() -> int:
    src = _source()
    tree = ast.parse(src)
    cls = _class_node(tree, "ArchitectureManagerWindow")
    build_ui = _method_node(cls, "_build_ui")
    sync = _method_node(cls, "_sync_large_module_target_controls")
    copy_method = _method_node(cls, "copy_large_module_target_path_to_clipboard")

    _find_ordered_markers(
        src,
        [
            "Large Module AST Split Audit",
            "Target .py:",
            "_large_module_target_edit",
            "_large_module_target_count_label",
            "_copy_large_module_target_path_btn = QPushButton('Copy Path')",
            "_prev_large_module_target_btn = QPushButton('<-')",
        ],
    )

    build_attrs = _attr_names(build_ui)
    if "_copy_large_module_target_path_btn" not in build_attrs:
        raise AssertionError("Copy Path button attribute missing from _build_ui")
    build_texts = _literal_texts(build_ui)
    required_texts = {
        "Copy Path",
        "architecture_review_copy_large_module_target_path_button",
        "Copy the selected Large Module AST Audit target .py path to clipboard",
    }
    missing = sorted(required_texts - build_texts)
    if missing:
        raise AssertionError(f"missing button text literals: {missing}")
    if "copy_large_module_target_path_to_clipboard" not in build_attrs:
        raise AssertionError("Copy Path button is not wired to copy_large_module_target_path_to_clipboard")

    sync_src = ast.get_source_segment(src, sync) or ""
    if "_copy_large_module_target_path_btn" not in sync_src:
        raise AssertionError("_sync_large_module_target_controls does not manage Copy Path enabled state")
    if "setEnabled(bool(target_text))" not in sync_src:
        raise AssertionError("Copy Path button must be enabled only when target text is present")

    method_src = ast.get_source_segment(src, copy_method) or ""
    method_attrs = _attr_names(copy_method)
    method_texts = _literal_texts(copy_method)
    for attr in ("clipboard", "setText", "statusBar", "showMessage", "is_absolute"):
        if attr not in method_attrs:
            raise AssertionError(f"copy method missing expected attribute call: {attr}")
    if "No Large Module AST Audit target path to copy" not in method_texts:
        raise AssertionError("copy method must handle empty target text")
    if "Copied Large Module AST Audit target .py path to clipboard" not in method_texts:
        raise AssertionError("copy method must report successful copy")
    if "Path(root_text) / target_path" not in method_src:
        raise AssertionError("relative target paths must be resolved against the project root")

    protected = [
        "_cancel_operation_button = QPushButton('Cancel')",
        "color: #C2185B; font-weight: bold;",
        "cancel_running_operation",
        "Run AST Split Audit",
        "Copy Split Handoff for AI",
        "run_large_module_split_audit_from_gui",
        "copy_large_module_split_handoff",
    ]
    for marker in protected:
        if marker not in src:
            raise AssertionError(f"protected existing behavior marker missing: {marker}")

    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
