# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_bindings.py
"""Canonical immutable bindings for widget registry private methods."""
from __future__ import annotations

import ast
from typing import Any, Callable, Mapping

from .ast_primitives import (
    FUNCTION_SCOPE_KINDS,
    LAYOUT_METHODS,
    LIST_SETTER_TO_FIELD,
    SINGLE_ITEM_SETTER_TO_FIELD,
    TEXT_SETTER_TO_FIELD,
    _build_widget_id,
    _expr_to_ref,
    _extract_constructor_display_text,
    _extract_constructor_parent_ref,
    _extract_layout_position_from_add_widget,
    _first_arg,
    _get_widget_type_from_call,
    _node_to_number,
    _node_to_text,
    _node_to_text_list,
    _safe_str,
    _variable_name_from_ref,
)

__all__ = []


class _WidgetRegistryPart1Bindings:
    """Immutable-by-convention dependency contract for implementation owners."""

    __slots__ = (
        "function_scope_kinds",
        "layout_methods",
        "text_setter_to_field",
        "single_item_setter_to_field",
        "list_setter_to_field",
        "build_widget_id",
        "expr_to_ref",
        "extract_constructor_display_text",
        "extract_constructor_parent_ref",
        "extract_layout_position_from_add_widget",
        "first_arg",
        "get_widget_type_from_call",
        "node_to_number",
        "node_to_text",
        "node_to_text_list",
        "safe_str",
        "variable_name_from_ref",
    )

    def __init__(
        self,
        *,
        function_scope_kinds: object,
        layout_methods: object,
        text_setter_to_field: Mapping[str, str],
        single_item_setter_to_field: Mapping[str, str],
        list_setter_to_field: Mapping[str, str],
        build_widget_id: Callable[..., str],
        expr_to_ref: Callable[..., str],
        extract_constructor_display_text: Callable[..., str],
        extract_constructor_parent_ref: Callable[..., str],
        extract_layout_position_from_add_widget: Callable[..., dict[str, Any]],
        first_arg: Callable[..., Any],
        get_widget_type_from_call: Callable[..., str],
        node_to_number: Callable[..., Any],
        node_to_text: Callable[..., str],
        node_to_text_list: Callable[..., list[str]],
        safe_str: Callable[..., str],
        variable_name_from_ref: Callable[..., str],
    ) -> None:
        self.function_scope_kinds = function_scope_kinds
        self.layout_methods = layout_methods
        self.text_setter_to_field = text_setter_to_field
        self.single_item_setter_to_field = single_item_setter_to_field
        self.list_setter_to_field = list_setter_to_field
        self.build_widget_id = build_widget_id
        self.expr_to_ref = expr_to_ref
        self.extract_constructor_display_text = extract_constructor_display_text
        self.extract_constructor_parent_ref = extract_constructor_parent_ref
        self.extract_layout_position_from_add_widget = (
            extract_layout_position_from_add_widget
        )
        self.first_arg = first_arg
        self.get_widget_type_from_call = get_widget_type_from_call
        self.node_to_number = node_to_number
        self.node_to_text = node_to_text
        self.node_to_text_list = node_to_text_list
        self.safe_str = safe_str
        self.variable_name_from_ref = variable_name_from_ref


_CANONICAL_BINDINGS = _WidgetRegistryPart1Bindings(
    function_scope_kinds=FUNCTION_SCOPE_KINDS,
    layout_methods=LAYOUT_METHODS,
    text_setter_to_field=TEXT_SETTER_TO_FIELD,
    single_item_setter_to_field=SINGLE_ITEM_SETTER_TO_FIELD,
    list_setter_to_field=LIST_SETTER_TO_FIELD,
    build_widget_id=_build_widget_id,
    expr_to_ref=_expr_to_ref,
    extract_constructor_display_text=_extract_constructor_display_text,
    extract_constructor_parent_ref=_extract_constructor_parent_ref,
    extract_layout_position_from_add_widget=(
        _extract_layout_position_from_add_widget
    ),
    first_arg=_first_arg,
    get_widget_type_from_call=_get_widget_type_from_call,
    node_to_number=_node_to_number,
    node_to_text=_node_to_text,
    node_to_text_list=_node_to_text_list,
    safe_str=_safe_str,
    variable_name_from_ref=_variable_name_from_ref,
)


def _configure_bindings(_root_globals: Mapping[str, Any]) -> None:
    """Preserve the old call surface without accepting injected state."""
    return None


def _bindings() -> _WidgetRegistryPart1Bindings:
    """Return the single canonical binding state."""
    return _CANONICAL_BINDINGS


def _node_line(node: object, default: Any) -> Any:
    """Read AST line metadata with an explicit missing-value fallback."""
    if isinstance(node, ast.AST):
        try:
            return node.lineno
        except AttributeError:
            return default
    return default


def _node_col(node: object, default: Any) -> Any:
    """Read AST column metadata with an explicit missing-value fallback."""
    if isinstance(node, ast.AST):
        try:
            return node.col_offset
        except AttributeError:
            return default
    return default


def _node_end_line(node: object, default: Any) -> Any:
    """Read AST end-line metadata with an explicit missing-value fallback."""
    if isinstance(node, ast.AST):
        try:
            return node.end_lineno
        except AttributeError:
            return default
    return default