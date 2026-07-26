# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_bindings.py
"""Explicit dependency bindings for widget registry part 1 private methods."""
from __future__ import annotations

import ast
from typing import Any, Callable, Mapping

__all__ = []


class _WidgetRegistryPart1Bindings:
    """Explicit immutable-by-convention dependency contract for implementation owners."""

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
        self.extract_layout_position_from_add_widget = extract_layout_position_from_add_widget
        self.first_arg = first_arg
        self.get_widget_type_from_call = get_widget_type_from_call
        self.node_to_number = node_to_number
        self.node_to_text = node_to_text
        self.node_to_text_list = node_to_text_list
        self.safe_str = safe_str
        self.variable_name_from_ref = variable_name_from_ref


class _WidgetRegistryPart1BindingHolder:
    """Single explicit holder for the active binding contract."""

    __slots__ = ("current",)

    def __init__(self) -> None:
        self.current: _WidgetRegistryPart1Bindings | None = None


_BINDING_HOLDER = _WidgetRegistryPart1BindingHolder()


def _configure_bindings(root_globals: Mapping[str, Any]) -> None:
    """Bind the exact dependency surface formerly injected into module globals."""
    _BINDING_HOLDER.current = _WidgetRegistryPart1Bindings(
        function_scope_kinds=root_globals["FUNCTION_SCOPE_KINDS"],
        layout_methods=root_globals["LAYOUT_METHODS"],
        text_setter_to_field=root_globals["TEXT_SETTER_TO_FIELD"],
        single_item_setter_to_field=root_globals["SINGLE_ITEM_SETTER_TO_FIELD"],
        list_setter_to_field=root_globals["LIST_SETTER_TO_FIELD"],
        build_widget_id=root_globals["_build_widget_id"],
        expr_to_ref=root_globals["_expr_to_ref"],
        extract_constructor_display_text=root_globals["_extract_constructor_display_text"],
        extract_constructor_parent_ref=root_globals["_extract_constructor_parent_ref"],
        extract_layout_position_from_add_widget=root_globals[
            "_extract_layout_position_from_add_widget"
        ],
        first_arg=root_globals["_first_arg"],
        get_widget_type_from_call=root_globals["_get_widget_type_from_call"],
        node_to_number=root_globals["_node_to_number"],
        node_to_text=root_globals["_node_to_text"],
        node_to_text_list=root_globals["_node_to_text_list"],
        safe_str=root_globals["_safe_str"],
        variable_name_from_ref=root_globals["_variable_name_from_ref"],
    )


def _bindings() -> _WidgetRegistryPart1Bindings:
    """Return configured bindings or fail closed before implementation use."""
    current = _BINDING_HOLDER.current
    if current is None:
        raise RuntimeError(
            "widget registry part 1 bindings are not configured; "
            "_bind_root_globals must run before implementation methods"
        )
    return current


def _node_line(node: object, default: Any) -> Any:
    """Read AST line metadata explicitly while preserving missing-value fallback."""
    if isinstance(node, ast.AST):
        try:
            return node.lineno
        except AttributeError:
            return default
    return default


def _node_col(node: object, default: Any) -> Any:
    """Read AST column metadata explicitly while preserving missing fallback."""
    if isinstance(node, ast.AST):
        try:
            return node.col_offset
        except AttributeError:
            return default
    return default


def _node_end_line(node: object, default: Any) -> Any:
    """Read AST end-line metadata explicitly while preserving missing fallback."""
    if isinstance(node, ast.AST):
        try:
            return node.end_lineno
        except AttributeError:
            return default
    return default
