# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Single-file missing-docstring insertion collection
# EXPORTS       : collect_missing_docstring_insertions
# DEPENDS ON    : source_io.py, symbol_naming.py, heuristic_docstrings.py, insertion_formatting.py, reporting.py
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Single-file missing-docstring insertion collection."""

from __future__ import annotations

import logging

import ast
from pathlib import Path

from .heuristic_docstrings import (
    build_class_docstring,
    build_function_docstring,
    build_module_docstring,
)
from .insertion_formatting import (
    build_module_header_payload,
    has_inline_body,
    indentation_for_body,
    is_overload_function,
    module_insert_index,
    payload_with_optional_uncertainty,
    render_docstring_body,
    wrap_docstring_lines,
)
from .reporting import (
    build_report_row as _report_row,
    function_report_kind_and_name as _function_report_kind_and_name,
    result_confidence as _result_confidence,
    result_failure_reason as _result_failure_reason,
    result_generation_source as _result_generation_source,
    result_issues as _result_issues,
    result_source as _result_source,
)
from .source_io import read_source_text, parse_source
from .symbol_naming import to_module_id

try:
    from ..context_builder import (
        build_class_context,
        build_function_context,
        build_module_context,
    )
    from ..module_summarizer import build_module_summary
    _AI_AVAILABLE = True
except ImportError:
    try:
        from context_builder import (
            build_class_context,
            build_function_context,
            build_module_context,
        )
        from module_summarizer import build_module_summary
        _AI_AVAILABLE = True
    except ImportError:
        _AI_AVAILABLE = False

__all__ = [
    "collect_missing_docstring_insertions",
]


def _suggested_docstring_from_payload(payload: list[str]) -> str:
    """Return the generated docstring text stored in a report-friendly field."""
    lines = [str(line).rstrip() for line in payload]
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines).strip()


def collect_missing_docstring_insertions(
    root: Path,
    path: Path,
    include_module: bool,
    include_classes: bool,
    include_functions: bool,
    include_init: bool,
    manifest: dict | None,
    generator: "AIDocstringGenerator | None" = None,
) -> tuple[list[tuple[int, list[str]]], list[str], str, bool, list[dict[str, object]]]:
    """Collect safe docstring insertions and detailed report rows for one file."""
    text, had_bom = read_source_text(path)
    report_rows: list[dict[str, object]] = []

    try:
        tree = parse_source(text, path)
    except SyntaxError as exc:
        message = f"{path}: source parse failed; skipped ({exc})"
        report_rows.append(
            _report_row(
                root,
                path,
                target_kind="file",
                target_name=path.name,
                line=None,
                action="failed",
                reason=f"source parse failed: {exc}",
            )
        )
        return [], [message], text, had_bom, report_rows

    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    module_id = to_module_id(root, path)
    lines = text.splitlines()
    insertions: list[tuple[int, list[str]]] = []
    skipped: list[str] = []

    module_prepass = None
    if generator is not None and _AI_AVAILABLE:
        try:
            module_prepass = build_module_summary(
                path,
                module_id,
                tree,
                lines,
                ai_config=getattr(generator, "_config", None),
            )
        except Exception:
            logging.exception("Boundary failure in collect_missing_docstring_insertions")
            module_prepass = None

    if include_module:
        module_has_docstring = ast.get_docstring(tree, clean=False) is not None
        if module_has_docstring:
            report_rows.append(
                _report_row(
                    root,
                    path,
                    target_kind="module",
                    target_name=module_id or path.stem,
                    line=1,
                    action="existing",
                    reason="module docstring already exists",
                    source="existing",
                )
            )
        elif not include_init and path.name == "__init__.py":
            report_rows.append(
                _report_row(
                    root,
                    path,
                    target_kind="module",
                    target_name=module_id or path.stem,
                    line=1,
                    action="skipped",
                    reason="__init__.py module docstrings are disabled",
                )
            )
        else:
            idx = module_insert_index(lines)
            if generator is not None and _AI_AVAILABLE:
                ctx = build_module_context(path, module_id, tree, lines, module_prepass)
                result = generator.generate(ctx)
                module_doc = render_docstring_body(result.body)
                payload = build_module_header_payload(
                    root,
                    path,
                    lines,
                    idx,
                    module_doc,
                    result.uncertain_comment,
                )
                source = _result_source(result)
                confidence = _result_confidence(result)
                generation_source = _result_generation_source(result)
                failure_reason = _result_failure_reason(result)
                issues = _result_issues(result)
            else:
                module_doc = build_module_docstring(path, module_id, tree, root, manifest)
                payload = build_module_header_payload(root, path, lines, idx, module_doc)
                source = "heuristic"
                confidence = "low"
                generation_source = "heuristic"
                failure_reason = "none"
                issues = []

            insertions.append((idx, payload))
            row = _report_row(
                root,
                path,
                target_kind="module",
                target_name=module_id or path.stem,
                line=1,
                insert_line=idx + 1,
                action="inserted",
                reason="missing module docstring",
                source=source,
                confidence=confidence,
                generation_source=generation_source,
                failure_reason=failure_reason,
                issues=issues,
            )
            row["suggested_docstring"] = _suggested_docstring_from_payload(payload)
            row["suggested_docstring_source"] = source
            report_rows.append(row)

    class_nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
        and isinstance(parent_map.get(node), (ast.Module, ast.ClassDef))
    ]
    function_nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and isinstance(parent_map.get(node), (ast.Module, ast.ClassDef))
    ]
    init_nodes = [node for node in function_nodes if node.name == "__init__"]
    other_functions = [node for node in function_nodes if node.name != "__init__"]

    def _body_docstring_insert_index(
        node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
        first_stmt: ast.stmt | None,
    ) -> int:
        """Return a body-docstring insertion index before nested decorators."""
        if first_stmt is None:
            return getattr(node, "lineno", 1)

        decorator_list = getattr(first_stmt, "decorator_list", None)
        if decorator_list:
            first_decorator_line = min(
                getattr(decorator, "lineno", first_stmt.lineno)
                for decorator in decorator_list
            )
            return first_decorator_line - 1

        return first_stmt.lineno - 1

    def _record_existing_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Handle record existing function.
        
        Parameters
        ----------
        node : ast.FunctionDef | ast.AsyncFunctionDef
            TODO: describe node.
        """
        
        kind, name = _function_report_kind_and_name(node, parent_map)
        report_rows.append(
            _report_row(
                root,
                path,
                target_kind=kind,
                target_name=name,
                line=getattr(node, "lineno", None),
                action="existing",
                reason="docstring already exists",
                source="existing",
            )
        )

    def _insert_function_docstring(node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Handle insert function docstring.
        
        Parameters
        ----------
        node : ast.FunctionDef | ast.AsyncFunctionDef
            TODO: describe node.
        """
        
        kind, name = _function_report_kind_and_name(node, parent_map)

        if is_overload_function(node):
            report_rows.append(
                _report_row(
                    root,
                    path,
                    target_kind=kind,
                    target_name=name,
                    line=getattr(node, "lineno", None),
                    action="skipped",
                    reason="overload stub",
                )
            )
            return

        if ast.get_docstring(node, clean=False) is not None:
            _record_existing_function(node)
            return

        if has_inline_body(node):
            message = f"{path}: function {node.name} on line {node.lineno} has inline body; skipped"
            skipped.append(message)
            report_rows.append(
                _report_row(
                    root,
                    path,
                    target_kind=kind,
                    target_name=name,
                    line=getattr(node, "lineno", None),
                    action="skipped",
                    reason="inline body",
                )
            )
            return

        first_stmt = node.body[0] if node.body else None
        insert_at = _body_docstring_insert_index(node, first_stmt)
        indent = indentation_for_body(node, first_stmt)

        if generator is not None and _AI_AVAILABLE:
            ctx = build_function_context(node, tree, module_id, lines, module_prepass)
            result = generator.generate(ctx)
            payload = payload_with_optional_uncertainty(
                render_docstring_body(result.body),
                indent,
                result.uncertain_comment,
            )
            source = _result_source(result)
            confidence = _result_confidence(result)
            generation_source = _result_generation_source(result)
            failure_reason = _result_failure_reason(result)
            issues = _result_issues(result)
        else:
            payload = wrap_docstring_lines(build_function_docstring(node), indent) + [indent]
            source = "heuristic"
            confidence = "low"
            generation_source = "heuristic"
            failure_reason = "none"
            issues = []

        insertions.append((insert_at, payload))
        row = _report_row(
            root,
            path,
            target_kind=kind,
            target_name=name,
            line=getattr(node, "lineno", None),
            insert_line=insert_at + 1,
            action="inserted",
            reason="missing docstring",
            source=source,
            confidence=confidence,
            generation_source=generation_source,
            failure_reason=failure_reason,
            issues=issues,
        )
        row["suggested_docstring"] = _suggested_docstring_from_payload(payload)
        row["suggested_docstring_source"] = source
        report_rows.append(row)

    for node in init_nodes:
        if not include_functions:
            break
        _insert_function_docstring(node)

    for node in class_nodes:
        if not include_classes:
            break

        if ast.get_docstring(node, clean=False) is not None:
            report_rows.append(
                _report_row(
                    root,
                    path,
                    target_kind="class",
                    target_name=node.name,
                    line=getattr(node, "lineno", None),
                    action="existing",
                    reason="docstring already exists",
                    source="existing",
                )
            )
            continue

        if has_inline_body(node):
            message = f"{path}: class {node.name} on line {node.lineno} has inline body; skipped"
            skipped.append(message)
            report_rows.append(
                _report_row(
                    root,
                    path,
                    target_kind="class",
                    target_name=node.name,
                    line=getattr(node, "lineno", None),
                    action="skipped",
                    reason="inline body",
                )
            )
            continue

        first_stmt = node.body[0] if node.body else None
        insert_at = _body_docstring_insert_index(node, first_stmt)
        indent = indentation_for_body(node, first_stmt)

        if generator is not None and _AI_AVAILABLE:
            ctx = build_class_context(node, tree, module_id, lines, module_prepass)
            result = generator.generate(ctx)
            payload = payload_with_optional_uncertainty(
                render_docstring_body(result.body),
                indent,
                result.uncertain_comment,
            )
            source = _result_source(result)
            confidence = _result_confidence(result)
            generation_source = _result_generation_source(result)
            failure_reason = _result_failure_reason(result)
            issues = _result_issues(result)
        else:
            payload = wrap_docstring_lines(build_class_docstring(node), indent) + [indent]
            source = "heuristic"
            confidence = "low"
            generation_source = "heuristic"
            failure_reason = "none"
            issues = []

        insertions.append((insert_at, payload))
        row = _report_row(
            root,
            path,
            target_kind="class",
            target_name=node.name,
            line=getattr(node, "lineno", None),
            insert_line=insert_at + 1,
            action="inserted",
            reason="missing docstring",
            source=source,
            confidence=confidence,
            generation_source=generation_source,
            failure_reason=failure_reason,
            issues=issues,
        )
        row["suggested_docstring"] = _suggested_docstring_from_payload(payload)
        row["suggested_docstring_source"] = source
        report_rows.append(row)

    for node in other_functions:
        if not include_functions:
            break
        _insert_function_docstring(node)

    return sorted(insertions, key=lambda x: x[0], reverse=True), skipped, text, had_bom, report_rows
