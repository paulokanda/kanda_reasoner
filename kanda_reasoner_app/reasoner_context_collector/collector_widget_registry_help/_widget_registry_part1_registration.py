# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_registration.py
"""Widget construction and property-registration implementations."""
from __future__ import annotations

import ast
from typing import Any

from ._widget_registry_part1_bindings import (
    _bindings,
    _node_col,
    _node_end_line,
    _node_line,
)

__all__ = []


def _wrg_visit_Assign_impl(self, node: ast.Assign) -> None:
    """Support wrg visit assign impl behavior.
    
    Parameters
    ----------
    node : ast.Assign
        The syntax tree node.
    """
    b = _bindings()
    widget_call = node.value if isinstance(node.value, ast.Call) else None
    if widget_call is not None:
        widget_type = b.get_widget_type_from_call(widget_call)
        if widget_type:
            target_ref = self._first_supported_target_ref(node.targets)
            if target_ref:
                self._register_assigned_widget(target_ref=target_ref, widget_type=widget_type, call_node=widget_call, assign_node=node, creation_style='assignment_constructor')
    self.generic_visit(node)


def _wrg_visit_AnnAssign_impl(self, node: ast.AnnAssign) -> None:
    """Support wrg visit ann assign impl behavior.
    
    Parameters
    ----------
    node : ast.AnnAssign
        The syntax tree node.
    """
    b = _bindings()
    widget_call = node.value if isinstance(node.value, ast.Call) else None
    if widget_call is not None:
        widget_type = b.get_widget_type_from_call(widget_call)
        if widget_type:
            target_ref = b.expr_to_ref(node.target)
            if target_ref:
                self._register_assigned_widget(target_ref=target_ref, widget_type=widget_type, call_node=widget_call, assign_node=node, creation_style='annotated_assignment_constructor')
    self.generic_visit(node)


def _wrg_visit_Call_impl(self, node: ast.Call) -> None:
    """Support wrg visit call impl behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    """
    self._handle_widget_property_call(node)
    self._handle_layout_call(node)
    self.generic_visit(node)


def _wrg__register_assigned_widget_impl(self, target_ref: str, widget_type: str, call_node: ast.Call, assign_node: ast.AST, creation_style: str) -> str:
    """Support wrg register assigned widget impl behavior.
    
    Parameters
    ----------
    target_ref : str
        The target ref value.
    widget_type : str
        The widget type value.
    call_node : ast.Call
        The call node value.
    assign_node : ast.AST
        The assign node value.
    creation_style : str
        The creation style value.
    
    Returns
    -------
    str
        The string result.
    """
    b = _bindings()
    variable_name = b.variable_name_from_ref(target_ref)
    source_symbol = self._current_source_symbol()
    class_name = self._current_class_name()
    method_name = self._current_method_name()
    widget_id = b.build_widget_id(source_file=self.source_file, source_symbol=source_symbol, variable_name=variable_name, widget_type=widget_type, line=_node_line(assign_node, 0) or 0, col=_node_col(assign_node, 0) or 0)
    display_text = b.extract_constructor_display_text(widget_type, call_node)
    parent_ref = b.extract_constructor_parent_ref(widget_type, call_node)
    record = {'widget_id': widget_id, 'widget_type': widget_type, 'variable_name': variable_name, 'widget_ref': target_ref, 'display_text': display_text, 'placeholder_text': '', 'tooltip_text': '', 'object_name': '', 'items': [], 'header_labels': [], 'tab_texts': [], 'source_file': self.source_file, 'source_symbol': source_symbol, 'class_name': class_name, 'method_name': method_name, 'line': _node_line(assign_node, None), 'end_line': _node_end_line(assign_node, _node_line(assign_node, None)), 'col': _node_col(assign_node, None), 'parent_layout': '', 'layout_kind': '', 'layout_position': {}, 'container_widget': parent_ref, 'creation_style': creation_style, 'connections': [], 'layout_records': [], 'confidence': 1.0}
    existing = self.registry.get(widget_id)
    if existing:
        record = existing
        if display_text and (not existing.get('display_text')):
            record['display_text'] = display_text
        if parent_ref and (not existing.get('container_widget')):
            record['container_widget'] = parent_ref
    else:
        self.registry[widget_id] = record
    self._index_widget_ref(source_symbol, target_ref, widget_id)
    if variable_name:
        self._index_widget_var(variable_name, widget_id)
    return widget_id


def _wrg__register_inline_widget_impl(self, widget_call: ast.Call, parent_layout: str='', layout_kind: str='', layout_position: dict[str, Any] | None=None, creation_style: str='inline_constructor') -> str:
    """Support wrg register inline widget impl behavior.
    
    Parameters
    ----------
    widget_call : ast.Call
        The widget call value.
    parent_layout : str, optional
        The optional parent layout value.
    layout_kind : str, optional
        The optional layout kind value.
    layout_position : dict[str, Any] | None, optional
        The optional layout position value.
    creation_style : str, optional
        The optional creation style value.
    
    Returns
    -------
    str
        The string result.
    """
    b = _bindings()
    widget_type = b.get_widget_type_from_call(widget_call)
    if not widget_type:
        return ''
    source_symbol = self._current_source_symbol()
    class_name = self._current_class_name()
    method_name = self._current_method_name()
    line = _node_line(widget_call, 0) or 0
    col = _node_col(widget_call, 0) or 0
    widget_id = b.build_widget_id(source_file=self.source_file, source_symbol=source_symbol, variable_name='', widget_type=widget_type, line=line, col=col)
    if widget_id not in self.registry:
        self.registry[widget_id] = {'widget_id': widget_id, 'widget_type': widget_type, 'variable_name': '', 'widget_ref': '', 'display_text': b.extract_constructor_display_text(widget_type, widget_call), 'placeholder_text': '', 'tooltip_text': '', 'object_name': '', 'items': [], 'header_labels': [], 'tab_texts': [], 'source_file': self.source_file, 'source_symbol': source_symbol, 'class_name': class_name, 'method_name': method_name, 'line': line, 'end_line': _node_end_line(widget_call, line), 'col': col, 'parent_layout': parent_layout, 'layout_kind': layout_kind, 'layout_position': layout_position or {}, 'container_widget': b.extract_constructor_parent_ref(widget_type, widget_call), 'creation_style': creation_style, 'connections': [], 'layout_records': [], 'confidence': 0.9}
    if parent_layout or layout_kind or layout_position:
        self._append_layout_record(widget_id=widget_id, parent_layout=parent_layout, layout_kind=layout_kind, layout_position=layout_position or {}, line=line)
    return widget_id


def _wrg__handle_widget_property_call_impl(self, node: ast.Call) -> None:
    """Support wrg handle widget property call impl behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    """
    b = _bindings()
    if not isinstance(node.func, ast.Attribute):
        return
    method_name = b.safe_str(node.func.attr)
    target_ref = b.expr_to_ref(node.func.value)
    widget_id = self._resolve_widget_id(target_ref)
    if not widget_id:
        return
    record = self.registry.get(widget_id)
    if not record:
        return
    if method_name in b.text_setter_to_field:
        text_value = b.node_to_text(b.first_arg(node))
        if text_value:
            record[b.text_setter_to_field[method_name]] = text_value
        return
    if method_name in b.single_item_setter_to_field:
        item_value = b.node_to_text(b.first_arg(node))
        if item_value:
            target_field = b.single_item_setter_to_field[method_name]
            current_items = list(record.get(target_field, []))
            current_items.append(item_value)
            record[target_field] = current_items
        return
    if method_name in b.list_setter_to_field:
        values = b.node_to_text_list(b.first_arg(node))
        if values:
            record[b.list_setter_to_field[method_name]] = values
        return
    if method_name == 'setTabText':
        if len(node.args) >= 2:
            tab_index = b.node_to_number(node.args[0])
            tab_text = b.node_to_text(node.args[1])
            if tab_text:
                current_tab_texts = list(record.get('tab_texts', []))
                current_tab_texts.append({'index': tab_index, 'text': tab_text, 'line': _node_line(node, None)})
                record['tab_texts'] = current_tab_texts
        return


def _wrg__resolve_or_create_widget_from_expr_impl(self, expr: ast.AST, parent_layout: str, layout_kind: str, layout_position: dict[str, Any]) -> str:
    """Support wrg resolve or create widget from expr impl behavior.
    
    Parameters
    ----------
    expr : ast.AST
        The expr value.
    parent_layout : str
        The parent layout value.
    layout_kind : str
        The layout kind value.
    layout_position : dict[str, Any]
        The layout position value.
    
    Returns
    -------
    str
        The string result.
    """
    b = _bindings()
    ref = b.expr_to_ref(expr)
    widget_id = self._resolve_widget_id(ref)
    if widget_id:
        return widget_id
    if isinstance(expr, ast.Call):
        widget_type = b.get_widget_type_from_call(expr)
        if widget_type:
            return self._register_inline_widget(widget_call=expr, parent_layout=parent_layout, layout_kind=layout_kind, layout_position=layout_position, creation_style='inline_constructor')
    return ''
