"""Collect widget registry evidence for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "build_widget_registry",
]

import ast
from typing import Any
from .collector_widget_registry_help import widget_registry_methods_part_1_private_impl as _wrg_methods_part_1


SUPPORTED_WIDGET_TYPES = {
    "QPushButton",
    "QLabel",
    "QLineEdit",
    "QComboBox",
    "QCheckBox",
    "QRadioButton",
    "QListWidget",
    "QTableWidget",
    "QPlainTextEdit",
    "QTextEdit",
    "QSpinBox",
    "QDoubleSpinBox",
    "QSlider",
    "QTabWidget",
}

TEXT_CONSTRUCTOR_WIDGET_TYPES = {
    "QPushButton",
    "QLabel",
    "QLineEdit",
    "QCheckBox",
    "QRadioButton",
}

TEXT_SETTER_TO_FIELD = {
    "setText": "display_text",
    "setPlaceholderText": "placeholder_text",
    "setToolTip": "tooltip_text",
    "setObjectName": "object_name",
}

LIST_SETTER_TO_FIELD = {
    "addItems": "items",
    "setHeaderLabels": "header_labels",
}

SINGLE_ITEM_SETTER_TO_FIELD = {
    "addItem": "items",
}

TAB_TEXT_SETTERS = {
    "addTab",
    "setTabText",
}

LAYOUT_METHODS = {
    "addWidget",
    "addRow",
    "addTab",
}

FUNCTION_SCOPE_KINDS = {
    "function",
    "async_function",
}


def build_widget_registry(files_payload: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Build a normalized widget registry in parallel with the existing collectors.

    This module is additive only. It does not alter:
    - extract_localization
    - extract_qt_signal_map
    - build_ui_action_index

    Input
    -----
    files_payload:
        Collector file records that already contain at least:
        - path
        - source

    Output
    ------
    dict[str, dict[str, Any]]
        Keyed by deterministic widget_id.
    """
    registry: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        source_file = _safe_str(file_record.get("path", ""))
        source = _safe_str(file_record.get("source", ""))

        if not source_file or not source:
            continue

        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue

        collector = _WidgetRegistryAstCollector(
            source_file=source_file,
            source=source,
        )
        collector.visit(tree)

        for widget_id, payload in collector.registry.items():
            registry[widget_id] = payload

    return dict(sorted(registry.items()))


class _WidgetRegistryAstCollector(ast.NodeVisitor):
    """
    AST collector that builds a widget registry for a single source file.
    """

    def __init__(self, source_file: str, source: str) -> None:
        self.source_file = source_file
        self.source = source
        self.registry: dict[str, dict[str, Any]] = {}

        self._scope_stack: list[tuple[str, str]] = []
        self._scope_ref_index: dict[str, dict[str, str]] = {}
        self._file_ref_index: dict[str, str] = {}
        self._file_var_index: dict[str, list[str]] = {}

    # -------------------------------------------------
    # Scope helpers
    # -------------------------------------------------

    def _current_source_symbol(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__current_source_symbol_impl(self, *args, **kwargs)

    def _current_class_name(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__current_class_name_impl(self, *args, **kwargs)

    def _current_method_name(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__current_method_name_impl(self, *args, **kwargs)

    def _push_scope(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__push_scope_impl(self, *args, **kwargs)

    def _pop_scope(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__pop_scope_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # AST visitors
    # -------------------------------------------------

    def visit_ClassDef(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg_visit_ClassDef_impl(self, *args, **kwargs)

    def visit_FunctionDef(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg_visit_FunctionDef_impl(self, *args, **kwargs)

    def visit_AsyncFunctionDef(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg_visit_AsyncFunctionDef_impl(self, *args, **kwargs)

    def visit_Assign(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg_visit_Assign_impl(self, *args, **kwargs)

    def visit_AnnAssign(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg_visit_AnnAssign_impl(self, *args, **kwargs)

    def visit_Call(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg_visit_Call_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Widget registration
    # -------------------------------------------------

    def _register_assigned_widget(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__register_assigned_widget_impl(self, *args, **kwargs)

    def _register_inline_widget(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__register_inline_widget_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Property setters
    # -------------------------------------------------

    def _handle_widget_property_call(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__handle_widget_property_call_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Layout and container relationships
    # -------------------------------------------------

    def _handle_layout_call(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__handle_layout_call_impl(self, *args, **kwargs)

    def _handle_add_widget(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__handle_add_widget_impl(self, *args, **kwargs)

    def _handle_add_row(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__handle_add_row_impl(self, *args, **kwargs)

    def _handle_add_tab(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__handle_add_tab_impl(self, *args, **kwargs)

    def _append_layout_record(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__append_layout_record_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Resolution and indexing
    # -------------------------------------------------

    def _index_widget_ref(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__index_widget_ref_impl(self, *args, **kwargs)

    def _index_widget_var(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__index_widget_var_impl(self, *args, **kwargs)

    def _resolve_widget_id(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__resolve_widget_id_impl(self, *args, **kwargs)

    def _resolve_or_create_widget_from_expr(self, *args, **kwargs):
        return _wrg_methods_part_1._wrg__resolve_or_create_widget_from_expr_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Small helpers
    # -------------------------------------------------

    @staticmethod
    def _first_supported_target_ref(targets: list[ast.expr]) -> str:
        for target in targets:
            target_ref = _expr_to_ref(target)
            if target_ref:
                return target_ref
        return ""


def _build_widget_id(
    source_file: str,
    source_symbol: str,
    variable_name: str,
    widget_type: str,
    line: int,
    col: int,
) -> str:
    if variable_name:
        return f"{source_file}::{source_symbol}::{variable_name}"
    return f"{source_file}::{source_symbol}::{widget_type}::line:{line}:col:{col}"


def _get_widget_type_from_call(node: ast.Call) -> str:
    call_name = _callable_name(node.func)
    base_name = call_name.split(".")[-1] if call_name else ""
    return base_name if base_name in SUPPORTED_WIDGET_TYPES else ""


def _callable_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return _safe_str(node.id)

    if isinstance(node, ast.Attribute):
        left = _callable_name(node.value)
        right = _safe_str(node.attr)
        if left:
            return f"{left}.{right}"
        return right

    return ""


def _expr_to_ref(node: ast.AST | None) -> str:
    if node is None:
        return ""

    if isinstance(node, ast.Name):
        return _safe_str(node.id)

    if isinstance(node, ast.Attribute):
        left = _expr_to_ref(node.value)
        right = _safe_str(node.attr)
        if left:
            return f"{left}.{right}"
        return right

    return ""


def _variable_name_from_ref(target_ref: str) -> str:
    ref = _safe_str(target_ref)
    if not ref:
        return ""
    return ref.split(".")[-1]


def _extract_constructor_display_text(widget_type: str, node: ast.Call) -> str:
    if widget_type not in TEXT_CONSTRUCTOR_WIDGET_TYPES:
        return ""

    if not node.args:
        return ""

    first_text = _node_to_text(node.args[0])
    if first_text:
        return first_text

    text_kw = _keyword_value(node, "text")
    return _node_to_text(text_kw)


def _extract_constructor_parent_ref(widget_type: str, node: ast.Call) -> str:
    parent_kw = _keyword_value(node, "parent")
    parent_kw_ref = _expr_to_ref(parent_kw)
    if parent_kw_ref:
        return parent_kw_ref

    if not node.args:
        return ""

    first_arg_text = _node_to_text(node.args[0])

    if widget_type in TEXT_CONSTRUCTOR_WIDGET_TYPES and first_arg_text:
        if len(node.args) >= 2:
            return _expr_to_ref(node.args[1])
        return ""

    return _expr_to_ref(node.args[0])


def _extract_layout_position_from_add_widget(node: ast.Call) -> dict[str, Any]:
    if len(node.args) >= 3:
        row = _node_to_number(node.args[1])
        col = _node_to_number(node.args[2])
        row_span = _node_to_number(node.args[3]) if len(node.args) >= 4 else None
        col_span = _node_to_number(node.args[4]) if len(node.args) >= 5 else None

        if row is not None and col is not None:
            return {
                "row": row,
                "col": col,
                "row_span": row_span,
                "col_span": col_span,
            }

    return {}


def _first_arg(node: ast.Call) -> ast.AST | None:
    if node.args:
        return node.args[0]
    return None


def _keyword_value(node: ast.Call, keyword_name: str) -> ast.AST | None:
    for keyword in node.keywords:
        if _safe_str(keyword.arg) == keyword_name:
            return keyword.value
    return None


def _node_to_text(node: ast.AST | None) -> str:
    if node is None:
        return ""

    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return _safe_str(node.value)

    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(_safe_str(value.value))
            elif isinstance(value, ast.FormattedValue):
                parts.append("{expr}")
        return "".join(parts).strip()

    return ""


def _node_to_text_list(node: ast.AST | None) -> list[str]:
    if node is None:
        return []

    if isinstance(node, (ast.List, ast.Tuple)):
        values: list[str] = []
        for element in node.elts:
            text_value = _node_to_text(element)
            if text_value:
                values.append(text_value)
        return values

    single_value = _node_to_text(node)
    return [single_value] if single_value else []


def _node_to_number(node: ast.AST | None) -> int | float | None:
    if node is None:
        return None

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    return None


def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    try:
        return str(value).strip()
    except Exception:
        return ""

# Bind root globals for private method implementation helpers.
_wrg_methods_part_1._bind_root_globals(globals())
