# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_layout.py
"""Layout and container relationship implementations for the widget registry."""
from __future__ import annotations

import ast
from typing import Any

from ._widget_registry_part1_bindings import (
    _bindings,
    _node_line,
)

__all__ = []


def _wrg__handle_layout_call_impl(self, node: ast.Call) -> None:
    """Support wrg handle layout call impl behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    """
    b = _bindings()
    if not isinstance(node.func, ast.Attribute):
        return
    method_name = b.safe_str(node.func.attr)
    if method_name not in b.layout_methods:
        return
    layout_ref = b.expr_to_ref(node.func.value)
    if method_name == 'addWidget':
        self._handle_add_widget(node, layout_ref)
        return
    if method_name == 'addRow':
        self._handle_add_row(node, layout_ref)
        return
    if method_name == 'addTab':
        self._handle_add_tab(node, layout_ref)
        return


def _wrg__handle_add_widget_impl(self, node: ast.Call, layout_ref: str) -> None:
    """Support wrg handle add widget impl behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    layout_ref : str
        The layout ref value.
    """
    b = _bindings()
    if not node.args:
        return
    widget_id = self._resolve_or_create_widget_from_expr(node.args[0], parent_layout=layout_ref, layout_kind='layout_add_widget', layout_position=b.extract_layout_position_from_add_widget(node))
    if not widget_id:
        return
    self._append_layout_record(widget_id=widget_id, parent_layout=layout_ref, layout_kind='layout_add_widget', layout_position=b.extract_layout_position_from_add_widget(node), line=_node_line(node, None))


def _wrg__handle_add_row_impl(self, node: ast.Call, layout_ref: str) -> None:
    """Support wrg handle add row impl behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    layout_ref : str
        The layout ref value.
    """
    if len(node.args) < 2:
        return
    label_expr = node.args[0]
    field_expr = node.args[1]
    label_widget_id = self._resolve_or_create_widget_from_expr(label_expr, parent_layout=layout_ref, layout_kind='form_row_label', layout_position={'role': 'label'})
    field_widget_id = self._resolve_or_create_widget_from_expr(field_expr, parent_layout=layout_ref, layout_kind='form_row_field', layout_position={'role': 'field'})
    if label_widget_id:
        self._append_layout_record(widget_id=label_widget_id, parent_layout=layout_ref, layout_kind='form_row_label', layout_position={'role': 'label'}, line=_node_line(node, None))
    if field_widget_id:
        self._append_layout_record(widget_id=field_widget_id, parent_layout=layout_ref, layout_kind='form_row_field', layout_position={'role': 'field'}, line=_node_line(node, None))


def _wrg__handle_add_tab_impl(self, node: ast.Call, layout_ref: str) -> None:
    """Support wrg handle add tab impl behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    layout_ref : str
        The layout ref value.
    """
    b = _bindings()
    if len(node.args) < 2:
        return
    widget_expr = node.args[0]
    tab_text = b.node_to_text(node.args[1])
    widget_id = self._resolve_or_create_widget_from_expr(widget_expr, parent_layout=layout_ref, layout_kind='tab_page', layout_position={'tab_text': tab_text})
    if not widget_id:
        return
    self._append_layout_record(widget_id=widget_id, parent_layout=layout_ref, layout_kind='tab_page', layout_position={'tab_text': tab_text}, line=_node_line(node, None))
    record = self.registry.get(widget_id, {})
    current_tab_texts = list(record.get('tab_texts', []))
    current_tab_texts.append({'index': None, 'text': tab_text, 'line': _node_line(node, None)})
    record['tab_texts'] = current_tab_texts


def _wrg__append_layout_record_impl(self, widget_id: str, parent_layout: str, layout_kind: str, layout_position: dict[str, Any], line: int | None) -> None:
    """Support wrg append layout record impl behavior.
    
    Parameters
    ----------
    widget_id : str
        The widget id value.
    parent_layout : str
        The parent layout value.
    layout_kind : str
        The layout kind value.
    layout_position : dict[str, Any]
        The layout position value.
    line : int | None
        The line value.
    """
    record = self.registry.get(widget_id)
    if not record:
        return
    if parent_layout and (not record.get('parent_layout')):
        record['parent_layout'] = parent_layout
    if layout_kind and (not record.get('layout_kind')):
        record['layout_kind'] = layout_kind
    if layout_position and (not record.get('layout_position')):
        record['layout_position'] = layout_position
    current_layout_records = list(record.get('layout_records', []))
    current_layout_records.append({'parent_layout': parent_layout, 'layout_kind': layout_kind, 'layout_position': layout_position, 'line': line})
    record['layout_records'] = current_layout_records
