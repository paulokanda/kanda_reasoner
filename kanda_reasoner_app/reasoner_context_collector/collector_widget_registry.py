# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_registry.py
"""Collect widget registry evidence for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "build_widget_registry",
]

import ast
from typing import Any

from .collector_widget_registry_help.widget_registry_methods_part_1_private_impl import (
    _bind_root_globals, _wrg__current_source_symbol_impl,
    _wrg__current_class_name_impl, _wrg__current_method_name_impl,
    _wrg__push_scope_impl, _wrg__pop_scope_impl, _wrg_visit_ClassDef_impl,
    _wrg_visit_FunctionDef_impl, _wrg_visit_AsyncFunctionDef_impl,
    _wrg__index_widget_ref_impl, _wrg__index_widget_var_impl,
    _wrg__resolve_widget_id_impl,
)

from .collector_widget_registry_help._widget_registry_part1_registration import (
    _wrg_visit_Assign_impl, _wrg_visit_AnnAssign_impl, _wrg_visit_Call_impl,
    _wrg__register_assigned_widget_impl, _wrg__register_inline_widget_impl,
    _wrg__handle_widget_property_call_impl,
    _wrg__resolve_or_create_widget_from_expr_impl,
)

from .collector_widget_registry_help._widget_registry_part1_layout import (
    _wrg__handle_layout_call_impl, _wrg__handle_add_widget_impl,
    _wrg__handle_add_row_impl, _wrg__handle_add_tab_impl,
    _wrg__append_layout_record_impl,
)

from .collector_widget_registry_help.ast_primitives import (
    _expr_to_ref,
    _safe_str,
)


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
        """Support init behavior.
        
        Parameters
        ----------
        source_file : str
            The source file value.
        source : str
            The source value.
        """
        
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
        """Support current source symbol behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__current_source_symbol_impl(self, *args, **kwargs)

    def _current_class_name(self, *args, **kwargs):
        """Support current class name behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__current_class_name_impl(self, *args, **kwargs)

    def _current_method_name(self, *args, **kwargs):
        """Support current method name behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__current_method_name_impl(self, *args, **kwargs)

    def _push_scope(self, *args, **kwargs):
        """Support push scope behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__push_scope_impl(self, *args, **kwargs)

    def _pop_scope(self, *args, **kwargs):
        """Support pop scope behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__pop_scope_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # AST visitors
    # -------------------------------------------------

    def visit_ClassDef(self, *args, **kwargs):
        """Support visit class def behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg_visit_ClassDef_impl(self, *args, **kwargs)

    def visit_FunctionDef(self, *args, **kwargs):
        """Support visit function def behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg_visit_FunctionDef_impl(self, *args, **kwargs)

    def visit_AsyncFunctionDef(self, *args, **kwargs):
        """Support visit async function def behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg_visit_AsyncFunctionDef_impl(self, *args, **kwargs)

    def visit_Assign(self, *args, **kwargs):
        """Support visit assign behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg_visit_Assign_impl(self, *args, **kwargs)

    def visit_AnnAssign(self, *args, **kwargs):
        """Support visit ann assign behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg_visit_AnnAssign_impl(self, *args, **kwargs)

    def visit_Call(self, *args, **kwargs):
        """Support visit call behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg_visit_Call_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Widget registration
    # -------------------------------------------------

    def _register_assigned_widget(self, *args, **kwargs):
        """Support register assigned widget behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__register_assigned_widget_impl(self, *args, **kwargs)

    def _register_inline_widget(self, *args, **kwargs):
        """Support register inline widget behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__register_inline_widget_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Property setters
    # -------------------------------------------------

    def _handle_widget_property_call(self, *args, **kwargs):
        """Support handle widget property call behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__handle_widget_property_call_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Layout and container relationships
    # -------------------------------------------------

    def _handle_layout_call(self, *args, **kwargs):
        """Support handle layout call behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__handle_layout_call_impl(self, *args, **kwargs)

    def _handle_add_widget(self, *args, **kwargs):
        """Support handle add widget behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__handle_add_widget_impl(self, *args, **kwargs)

    def _handle_add_row(self, *args, **kwargs):
        """Support handle add row behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__handle_add_row_impl(self, *args, **kwargs)

    def _handle_add_tab(self, *args, **kwargs):
        """Support handle add tab behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__handle_add_tab_impl(self, *args, **kwargs)

    def _append_layout_record(self, *args, **kwargs):
        """Support append layout record behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__append_layout_record_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Resolution and indexing
    # -------------------------------------------------

    def _index_widget_ref(self, *args, **kwargs):
        """Support index widget ref behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__index_widget_ref_impl(self, *args, **kwargs)

    def _index_widget_var(self, *args, **kwargs):
        """Support index widget var behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__index_widget_var_impl(self, *args, **kwargs)

    def _resolve_widget_id(self, *args, **kwargs):
        """Support resolve widget id behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__resolve_widget_id_impl(self, *args, **kwargs)

    def _resolve_or_create_widget_from_expr(self, *args, **kwargs):
        """Support resolve or create widget from expr behavior.
        
        Parameters
        ----------
        *args : object
            The positional arguments.
        **kwargs : object
            The kwargs value.
        """
        
        return _wrg__resolve_or_create_widget_from_expr_impl(self, *args, **kwargs)

    # -------------------------------------------------
    # Small helpers
    # -------------------------------------------------

    @staticmethod
    def _first_supported_target_ref(targets: list[ast.expr]) -> str:
        """Support first supported target ref behavior.
        
        Parameters
        ----------
        targets : list[ast.expr]
            The targets value.
        
        Returns
        -------
        str
            The string result.
        """
        
        for target in targets:
            target_ref = _expr_to_ref(target)
            if target_ref:
                return target_ref
        return ""


# Bind root globals for private method implementation helpers.
_bind_root_globals(globals())
