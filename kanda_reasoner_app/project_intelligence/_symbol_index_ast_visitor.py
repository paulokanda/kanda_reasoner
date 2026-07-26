# project-path: kanda_reasoner_app/project_intelligence/_symbol_index_ast_visitor.py
"""Private AST collection helper for the Project Intelligence Symbol Indexer."""

from __future__ import annotations

import ast

from .models import ImportRecord, SymbolRecord


class _SymbolVisitor(ast.NodeVisitor):
    """AST visitor that records definitions and imports without executing code."""

    def __init__(self, relative_path: str) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        relative_path : str
            The relative path value.
        """
        
        self.relative_path = relative_path
        self.symbols: list[SymbolRecord] = []
        self.imports: list[ImportRecord] = []
        self._scope_stack: list[str] = []

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        """Support visit import behavior.
        
        Parameters
        ----------
        node : ast.Import
            The syntax tree node.
        """
        
        for alias in node.names:
            self.imports.append(
                ImportRecord(
                    module=alias.name,
                    imported_name=alias.asname or alias.name,
                    import_type="import",
                    file_path=self.relative_path,
                    line_number=int(node.lineno or 0),
                )
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        """Support visit import from behavior.
        
        Parameters
        ----------
        node : ast.ImportFrom
            The syntax tree node.
        """
        
        module_name = "." * int(node.level or 0) + str(node.module or "")
        for alias in node.names:
            self.imports.append(
                ImportRecord(
                    module=module_name,
                    imported_name=alias.asname or alias.name,
                    import_type="from_import",
                    file_path=self.relative_path,
                    line_number=int(node.lineno or 0),
                )
            )
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        """Support visit class def behavior.
        
        Parameters
        ----------
        node : ast.ClassDef
            The syntax tree node.
        """
        
        parent_name = self._current_parent_name()
        self.symbols.append(
            SymbolRecord(
                name=node.name,
                symbol_type="class",
                file_path=self.relative_path,
                line_number=int(node.lineno or 0),
                end_line_number=int(node.end_lineno or 0),
                parent_name=parent_name,
                has_docstring=ast.get_docstring(node, clean=False) is not None,
                is_async=False,
            )
        )
        self._scope_stack.append(node.name)
        self.generic_visit(node)
        self._scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """Support visit function def behavior.
        
        Parameters
        ----------
        node : ast.FunctionDef
            The syntax tree node.
        """
        
        self._visit_function(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        """Support visit async function def behavior.
        
        Parameters
        ----------
        node : ast.AsyncFunctionDef
            The syntax tree node.
        """
        
        self._visit_function(node, is_async=True)

    def _current_parent_name(self) -> str:
        """Support current parent name behavior.
        
        Returns
        -------
        str
            The string result.
        """
        
        return ".".join(self._scope_stack)

    def _function_type(self, is_async: bool) -> str:
        """Support function type behavior.
        
        Parameters
        ----------
        is_async : bool
            The is async value.
        
        Returns
        -------
        str
            The string result.
        """
        
        if not self._scope_stack:
            return "async_function" if is_async else "function"
        parent = self._scope_stack[-1]
        if parent and parent[:1].isupper():
            return "async_method" if is_async else "method"
        return "nested_async_function" if is_async else "nested_function"

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, *, is_async: bool) -> None:
        """Support visit function behavior.
        
        Parameters
        ----------
        node : ast.FunctionDef | ast.AsyncFunctionDef
            The syntax tree node.
        is_async : bool
            The is async value.
        """
        
        parent_name = self._current_parent_name()
        self.symbols.append(
            SymbolRecord(
                name=node.name,
                symbol_type=self._function_type(is_async),
                file_path=self.relative_path,
                line_number=int(node.lineno or 0),
                end_line_number=int(node.end_lineno or 0),
                parent_name=parent_name,
                has_docstring=ast.get_docstring(node, clean=False) is not None,
                is_async=is_async,
            )
        )
        self._scope_stack.append(node.name)
        self.generic_visit(node)
        self._scope_stack.pop()

