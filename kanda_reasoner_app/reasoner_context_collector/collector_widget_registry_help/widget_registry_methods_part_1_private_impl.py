# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/widget_registry_methods_part_1_private_impl.py
"""Private method implementations for collector_widget_registry.

This facade preserves the historical implementation-function names while
delegating widget registration and layout ownership to cohesive private modules.
"""
from __future__ import annotations

import ast

from ._widget_registry_part1_bindings import _bindings, _configure_bindings
from ._widget_registry_part1_layout import (
    _wrg__append_layout_record_impl,
    _wrg__handle_add_row_impl,
    _wrg__handle_add_tab_impl,
    _wrg__handle_add_widget_impl,
    _wrg__handle_layout_call_impl,
)
from ._widget_registry_part1_registration import (
    _wrg__handle_widget_property_call_impl,
    _wrg__register_assigned_widget_impl,
    _wrg__register_inline_widget_impl,
    _wrg__resolve_or_create_widget_from_expr_impl,
    _wrg_visit_AnnAssign_impl,
    _wrg_visit_Assign_impl,
    _wrg_visit_Call_impl,
)

__all__ = []


def _bind_root_globals(root_globals):
    """Configure the explicit dependency contract used by all implementation owners."""
    _configure_bindings(root_globals)



def _wrg__current_source_symbol_impl(self) -> str:
    """Support wrg current source symbol impl behavior.
    
    Returns
    -------
    str
        The string result.
    """
    names = [name for _kind, name in self._scope_stack if name]
    return '.'.join(names) if names else '<module>'


def _wrg__current_class_name_impl(self) -> str:
    """Support wrg current class name impl behavior.
    
    Returns
    -------
    str
        The string result.
    """
    for kind, name in reversed(self._scope_stack):
        if kind == 'class':
            return name
    return ''


def _wrg__current_method_name_impl(self) -> str:
    """Support wrg current method name impl behavior.
    
    Returns
    -------
    str
        The string result.
    """
    b = _bindings()
    for kind, name in reversed(self._scope_stack):
        if kind in b.function_scope_kinds:
            return name
    return ''


def _wrg__push_scope_impl(self, kind: str, name: str) -> None:
    """Support wrg push scope impl behavior.
    
    Parameters
    ----------
    kind : str
        The kind value.
    name : str
        The name value.
    """
    self._scope_stack.append((kind, name))


def _wrg__pop_scope_impl(self) -> None:
    """Support wrg pop scope impl behavior.
    """
    if self._scope_stack:
        self._scope_stack.pop()


def _wrg_visit_ClassDef_impl(self, node: ast.ClassDef) -> None:
    """Support wrg visit class def impl behavior.
    
    Parameters
    ----------
    node : ast.ClassDef
        The syntax tree node.
    """
    self._push_scope('class', node.name)
    self.generic_visit(node)
    self._pop_scope()


def _wrg_visit_FunctionDef_impl(self, node: ast.FunctionDef) -> None:
    """Support wrg visit function def impl behavior.
    
    Parameters
    ----------
    node : ast.FunctionDef
        The syntax tree node.
    """
    self._push_scope('function', node.name)
    self.generic_visit(node)
    self._pop_scope()


def _wrg_visit_AsyncFunctionDef_impl(self, node: ast.AsyncFunctionDef) -> None:
    """Support wrg visit async function def impl behavior.
    
    Parameters
    ----------
    node : ast.AsyncFunctionDef
        The syntax tree node.
    """
    self._push_scope('async_function', node.name)
    self.generic_visit(node)
    self._pop_scope()


def _wrg__index_widget_ref_impl(self, source_symbol: str, target_ref: str, widget_id: str) -> None:
    """Support wrg index widget ref impl behavior.
    
    Parameters
    ----------
    source_symbol : str
        The source symbol value.
    target_ref : str
        The target ref value.
    widget_id : str
        The widget id value.
    """
    if source_symbol not in self._scope_ref_index:
        self._scope_ref_index[source_symbol] = {}
    self._scope_ref_index[source_symbol][target_ref] = widget_id
    self._file_ref_index[target_ref] = widget_id


def _wrg__index_widget_var_impl(self, variable_name: str, widget_id: str) -> None:
    """Support wrg index widget var impl behavior.
    
    Parameters
    ----------
    variable_name : str
        The variable name value.
    widget_id : str
        The widget id value.
    """
    if variable_name not in self._file_var_index:
        self._file_var_index[variable_name] = []
    if widget_id not in self._file_var_index[variable_name]:
        self._file_var_index[variable_name].append(widget_id)


def _wrg__resolve_widget_id_impl(self, target_ref: str) -> str:
    """Support wrg resolve widget id impl behavior.
    
    Parameters
    ----------
    target_ref : str
        The target ref value.
    
    Returns
    -------
    str
        The string result.
    """
    b = _bindings()
    if not target_ref:
        return ''
    source_symbol = self._current_source_symbol()
    scope_map = self._scope_ref_index.get(source_symbol, {})
    if target_ref in scope_map:
        return scope_map[target_ref]
    if target_ref in self._file_ref_index:
        return self._file_ref_index[target_ref]
    variable_name = b.variable_name_from_ref(target_ref)
    if variable_name:
        matches = self._file_var_index.get(variable_name, [])
        if len(matches) == 1:
            return matches[0]
    return ''
