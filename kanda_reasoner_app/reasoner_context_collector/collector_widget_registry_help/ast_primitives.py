# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/ast_primitives.py
"""AST primitive helpers for collector_widget_registry."""

from __future__ import annotations

import ast
from typing import Any

__all__ = [
    "SUPPORTED_WIDGET_TYPES",
    "TEXT_CONSTRUCTOR_WIDGET_TYPES",
    "TEXT_SETTER_TO_FIELD",
    "LIST_SETTER_TO_FIELD",
    "SINGLE_ITEM_SETTER_TO_FIELD",
    "TAB_TEXT_SETTERS",
    "LAYOUT_METHODS",
    "FUNCTION_SCOPE_KINDS",
]

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


def _build_widget_id(
    source_file: str,
    source_symbol: str,
    variable_name: str,
    widget_type: str,
    line: int,
    col: int,
) -> str:
    """Support build widget id behavior.

    Parameters
    ----------
    source_file : str
        The source file value.
    source_symbol : str
        The source symbol value.
    variable_name : str
        The variable name value.
    widget_type : str
        The widget type value.
    line : int
        The line value.
    col : int
        The col value.

    Returns
    -------
    str
        The string result.
    """

    if variable_name:
        return f"{source_file}::{source_symbol}::{variable_name}"
    return f"{source_file}::{source_symbol}::{widget_type}::line:{line}:col:{col}"


def _get_widget_type_from_call(node: ast.Call) -> str:
    """Support get widget type from call behavior.

    Parameters
    ----------
    node : ast.Call
        The syntax tree node.

    Returns
    -------
    str
        The string result.
    """

    call_name = _callable_name(node.func)
    base_name = call_name.split(".")[-1] if call_name else ""
    return base_name if base_name in SUPPORTED_WIDGET_TYPES else ""


def _callable_name(node: ast.AST) -> str:
    """Support callable name behavior.

    Parameters
    ----------
    node : ast.AST
        The syntax tree node.

    Returns
    -------
    str
        The string result.
    """

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
    """Support expr to ref behavior.

    Parameters
    ----------
    node : ast.AST | None
        The syntax tree node.

    Returns
    -------
    str
        The string result.
    """

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
    """Support variable name from ref behavior.

    Parameters
    ----------
    target_ref : str
        The target ref value.

    Returns
    -------
    str
        The string result.
    """

    ref = _safe_str(target_ref)
    if not ref:
        return ""
    return ref.split(".")[-1]


def _extract_constructor_display_text(widget_type: str, node: ast.Call) -> str:
    """Support extract constructor display text behavior.

    Parameters
    ----------
    widget_type : str
        The widget type value.
    node : ast.Call
        The syntax tree node.

    Returns
    -------
    str
        The string result.
    """

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
    """Support extract constructor parent ref behavior.

    Parameters
    ----------
    widget_type : str
        The widget type value.
    node : ast.Call
        The syntax tree node.

    Returns
    -------
    str
        The string result.
    """

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
    """Support extract layout position from add widget behavior.

    Parameters
    ----------
    node : ast.Call
        The syntax tree node.

    Returns
    -------
    dict[str, Any]
        The mapped values.
    """

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
    """Support first arg behavior.

    Parameters
    ----------
    node : ast.Call
        The syntax tree node.

    Returns
    -------
    ast.AST | None
        The ast result.
    """

    if node.args:
        return node.args[0]
    return None


def _keyword_value(node: ast.Call, keyword_name: str) -> ast.AST | None:
    """Support keyword value behavior.

    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    keyword_name : str
        The keyword name value.

    Returns
    -------
    ast.AST | None
        The ast result.
    """

    for keyword in node.keywords:
        if _safe_str(keyword.arg) == keyword_name:
            return keyword.value
    return None


def _node_to_text(node: ast.AST | None) -> str:
    """Support node to text behavior.

    Parameters
    ----------
    node : ast.AST | None
        The syntax tree node.

    Returns
    -------
    str
        The string result.
    """

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
    """Support node to text list behavior.

    Parameters
    ----------
    node : ast.AST | None
        The syntax tree node.

    Returns
    -------
    list[str]
        The list of values.
    """

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
    """Support node to number behavior.

    Parameters
    ----------
    node : ast.AST | None
        The syntax tree node.

    Returns
    -------
    int | float | None
        The integer result.
    """

    if node is None:
        return None

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    return None


def _safe_str(value: Any) -> str:
    """Support safe str behavior.

    Parameters
    ----------
    value : Any
        The input value.

    Returns
    -------
    str
        The string result.
    """

    if value is None:
        return ""
    try:
        return str(value).strip()
    except Exception:
        return ""
