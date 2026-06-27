#!/usr/bin/env python3
"""Build rich symbol context objects for AI-powered docstring generation.

AI CONTEXT: Builds evidence-backed symbol context for local AI docstring generation."""

from __future__ import annotations

__all__ = [
    "AttributeInfo",
    "ParameterInfo",
    "SymbolContext",
    "build_class_context",
    "build_function_context",
    "build_module_context",
]

import ast
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from .context_builder_help.inference_private_impl import (
    _annotation_from_default,
    _dedupe_texts,
    _infer_return_annotation,
    _raise_type_name,
    _walk_without_nested_symbols,
)



@dataclass
class ParameterInfo:
    name: str
    annotation: str
    has_default: bool
    is_vararg: bool = False
    is_kwarg: bool = False
    is_kwonly: bool = False


@dataclass
class AttributeInfo:
    name: str
    type_hint: str = ""
    description_hint: str = ""


@dataclass
class SymbolContext:
    kind: str
    name: str
    module_id: str
    source_lines: list[str] = field(default_factory=list)
    signature: str = ""
    parameters: list[ParameterInfo] = field(default_factory=list)
    return_annotation: str = ""
    decorators: list[str] = field(default_factory=list)
    enclosing_class: str = ""
    module_docstring: str = ""
    module_summary_block: str = ""
    class_docstring: str = ""
    class_attributes: list[AttributeInfo] = field(default_factory=list)
    sibling_docstrings: list[str] = field(default_factory=list)
    overload_siblings: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    raises_types: list[str] = field(default_factory=list)
    is_async: bool = False
    is_property: bool = False
    is_cached_property: bool = False
    is_abstract: bool = False
    is_staticmethod: bool = False
    is_classmethod: bool = False
    is_overload: bool = False
    is_dataclass: bool = False
    is_init: bool = False
    lineno: int = 0

    @property
    def full_name(self) -> str:
        if self.enclosing_class:
            return f"{self.enclosing_class}.{self.name}"
        return self.name


def _safe_unparse(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def _decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[str]:
    names: list[str] = []
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name):
            names.append(dec.id)
        elif isinstance(dec, ast.Attribute):
            names.append(dec.attr)
        else:
            text = _safe_unparse(dec)
            if text:
                names.append(text)
    return names

def _extract_parameters(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ParameterInfo]:
    result: list[ParameterInfo] = []
    args = node.args

    positional = list(args.posonlyargs) + list(args.args)
    positional_defaults: list[ast.AST | None] = [None] * (
        len(positional) - len(args.defaults)
    ) + list(args.defaults)

    for index, (arg, default) in enumerate(zip(positional, positional_defaults)):
        if index == 0 and arg.arg in {"self", "cls"}:
            continue
        annotation = _safe_unparse(arg.annotation) or _annotation_from_default(default)
        result.append(
            ParameterInfo(
                name=arg.arg,
                annotation=annotation,
                has_default=default is not None,
            )
        )

    if args.vararg is not None:
        result.append(
            ParameterInfo(
                name=args.vararg.arg,
                annotation=_safe_unparse(args.vararg.annotation),
                has_default=False,
                is_vararg=True,
            )
        )

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        annotation = _safe_unparse(arg.annotation) or _annotation_from_default(default)
        result.append(
            ParameterInfo(
                name=arg.arg,
                annotation=annotation,
                has_default=default is not None,
                is_kwonly=True,
            )
        )

    if args.kwarg is not None:
        result.append(
            ParameterInfo(
                name=args.kwarg.arg,
                annotation=_safe_unparse(args.kwarg.annotation),
                has_default=False,
                is_kwarg=True,
            )
        )

    return result



def _extract_imports(tree: ast.Module, *, limit: int = 10) -> list[str]:
    lines: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            rendered = _safe_unparse(node)
            if rendered:
                lines.append(rendered)
            if len(lines) >= limit:
                break
        elif not isinstance(node, (ast.Expr, ast.Assign, ast.AnnAssign)):
            break
    return lines


def _extract_source_lines(node: ast.AST, file_lines: list[str], *, limit: int = 80) -> list[str]:
    lineno = getattr(node, "lineno", 1)
    end_lineno = getattr(node, "end_lineno", lineno)
    raw = file_lines[lineno - 1 : end_lineno]
    dedented = textwrap.dedent("\n".join(raw)).splitlines()
    if len(dedented) > limit:
        return dedented[:limit] + ["# ... truncated for prompt ..."]
    return dedented


def _extract_sibling_docstrings(parent_body: list[ast.stmt], current_node: ast.AST, *, limit: int = 3) -> list[str]:
    docs: list[str] = []
    for sibling in parent_body:
        if sibling is current_node:
            continue
        if isinstance(sibling, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(sibling, clean=False)
            if doc:
                docs.append(doc.strip())
            if len(docs) >= limit:
                break
    return docs


def _extract_class_attributes(class_node: ast.ClassDef) -> list[AttributeInfo]:
    attrs: dict[str, AttributeInfo] = {}
    for child in class_node.body:
        if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) or child.name != "__init__":
            continue
        param_annotations: dict[str, str] = {}
        for arg in child.args.args:
            if arg.arg != "self":
                param_annotations[arg.arg] = _safe_unparse(arg.annotation) or "object"
        for node in ast.walk(child):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        attr_name = target.attr
                        type_hint = ""
                        description_hint = _safe_unparse(node.value)[:80]
                        if isinstance(node.value, ast.Name) and node.value.id in param_annotations:
                            type_hint = param_annotations[node.value.id]
                        attrs.setdefault(
                            attr_name,
                            AttributeInfo(
                                name=attr_name,
                                type_hint=type_hint,
                                description_hint=description_hint,
                            ),
                        )
            elif isinstance(node, ast.AnnAssign):
                target = node.target
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    attrs.setdefault(
                        target.attr,
                        AttributeInfo(
                            name=target.attr,
                            type_hint=_safe_unparse(node.annotation),
                            description_hint=_safe_unparse(node.value)[:80] if node.value else "",
                        ),
                    )
    return list(attrs.values())


def _extract_raises_types(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    result: list[str] = []
    for inner in _walk_without_nested_symbols(node):
        if not isinstance(inner, ast.Raise) or inner.exc is None:
            continue
        name = _raise_type_name(inner.exc)
        if name:
            result.append(name)
    return _dedupe_texts(result)



def _find_parent_class(tree: ast.Module, node: ast.AST) -> ast.ClassDef | None:
    for parent in ast.walk(tree):
        if isinstance(parent, ast.ClassDef) and node in parent.body:
            return parent
    return None


def _collect_overload_siblings(parent_body: list[ast.stmt], name: str, current_node: ast.AST) -> list[str]:
    results: list[str] = []
    for sibling in parent_body:
        if sibling is current_node:
            continue
        if isinstance(sibling, (ast.FunctionDef, ast.AsyncFunctionDef)) and sibling.name == name:
            decs = _decorator_names(sibling)
            if "overload" not in decs:
                continue
            prefix = "async def" if isinstance(sibling, ast.AsyncFunctionDef) else "def"
            try:
                args_text = ast.unparse(sibling.args)
                if not args_text.startswith("("):
                    args_text = f"({args_text})"
            except Exception:
                args_text = "(...)"
            return_text = ""
            if getattr(sibling, "returns", None) is not None:
                ret = _safe_unparse(sibling.returns)
                if ret:
                    return_text = f" -> {ret}"
            results.append(f"{prefix} {sibling.name}{args_text}{return_text}")
    return results


def _module_summary_block(module_summary: Any | None) -> str:
    return getattr(module_summary, "context_block", "") if module_summary is not None else ""


def _class_profile_attributes(module_summary: Any | None, class_name: str) -> list[AttributeInfo]:
    if module_summary is None:
        return []
    profiles = getattr(module_summary, "classes", [])
    for profile in profiles:
        if getattr(profile, "name", None) != class_name:
            continue
        attrs: list[AttributeInfo] = []
        for item in getattr(profile, "init_attributes", []):
            attrs.append(
                AttributeInfo(
                    name=getattr(item, "name", ""),
                    type_hint=getattr(item, "type_hint", ""),
                    description_hint=getattr(item, "assigned_from", ""),
                )
            )
        return attrs
    return []


def build_module_context(
    path: Path,
    module_id: str,
    tree: ast.Module,
    source_lines: list[str],
    module_summary: Any | None = None,
) -> SymbolContext:
    module_doc = ast.get_docstring(tree, clean=False) or ""
    return SymbolContext(
        kind="module",
        name=path.stem,
        module_id=module_id,
        source_lines=source_lines[:80],
        signature="",
        module_docstring=module_doc,
        module_summary_block=_module_summary_block(module_summary),
        imports=_extract_imports(tree),
        sibling_docstrings=[],
        lineno=1,
    )


def build_class_context(
    node: ast.ClassDef,
    tree: ast.Module,
    module_id: str,
    source_lines: list[str],
    module_summary: Any | None = None,
    class_docstring_override: str = "",
) -> SymbolContext:
    class_attributes = _class_profile_attributes(module_summary, node.name) or _extract_class_attributes(node)
    return SymbolContext(
        kind="class",
        name=node.name,
        module_id=module_id,
        source_lines=_extract_source_lines(node, source_lines),
        signature=_safe_unparse(node).split(":", 1)[0],
        decorators=_decorator_names(node),
        module_docstring=ast.get_docstring(tree, clean=False) or "",
        module_summary_block=_module_summary_block(module_summary),
        class_docstring=class_docstring_override,
        class_attributes=class_attributes,
        sibling_docstrings=_extract_sibling_docstrings(tree.body, node),
        imports=_extract_imports(tree),
        is_dataclass="dataclass" in _decorator_names(node),
        lineno=node.lineno,
    )


def build_function_context(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    tree: ast.Module,
    module_id: str,
    source_lines: list[str],
    module_summary: Any | None = None,
) -> SymbolContext:
    parent_class = _find_parent_class(tree, node)
    parent_body = parent_class.body if parent_class is not None else tree.body
    decorators = _decorator_names(node)
    parameters = _extract_parameters(node)
    if "property" in decorators or "cached_property" in decorators:
        parameters = []

    class_docstring = ""
    class_attributes: list[AttributeInfo] = []
    is_dataclass = False
    if parent_class is not None:
        class_docstring = ast.get_docstring(parent_class, clean=False) or ""
        class_attributes = _class_profile_attributes(module_summary, parent_class.name) or _extract_class_attributes(parent_class)
        is_dataclass = "dataclass" in _decorator_names(parent_class)

    signature = _safe_unparse(node)
    if ":" in signature:
        signature = signature.split(":", 1)[0]

    return SymbolContext(
        kind="method" if parent_class is not None else "function",
        name=node.name,
        module_id=module_id,
        source_lines=_extract_source_lines(node, source_lines),
        signature=signature,
        parameters=parameters,
        return_annotation=_safe_unparse(node.returns) or _infer_return_annotation(node),
        decorators=decorators,
        enclosing_class=parent_class.name if parent_class is not None else "",
        module_docstring=ast.get_docstring(tree, clean=False) or "",
        module_summary_block=_module_summary_block(module_summary),
        class_docstring=class_docstring,
        class_attributes=class_attributes,
        sibling_docstrings=_extract_sibling_docstrings(parent_body, node),
        overload_siblings=_collect_overload_siblings(parent_body, node.name, node),
        imports=_extract_imports(tree),
        raises_types=_extract_raises_types(node),
        is_async=isinstance(node, ast.AsyncFunctionDef),
        is_property="property" in decorators,
        is_cached_property="cached_property" in decorators,
        is_abstract="abstractmethod" in decorators,
        is_staticmethod="staticmethod" in decorators,
        is_classmethod="classmethod" in decorators,
        is_overload="overload" in decorators,
        is_dataclass=is_dataclass,
        is_init=node.name == "__init__",
        lineno=node.lineno,
    )
