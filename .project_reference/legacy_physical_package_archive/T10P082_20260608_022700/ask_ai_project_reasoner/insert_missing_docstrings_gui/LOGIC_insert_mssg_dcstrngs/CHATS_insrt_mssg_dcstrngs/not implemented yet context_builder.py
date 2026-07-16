#!/usr/bin/env python3
"""Build rich symbol context objects for AI-powered docstring generation.

Phase 3 upgrades
----------------
- :class:`SymbolContext` gains ``module_summary_block``, ``class_attributes``,
  ``raises_types``, ``overload_siblings``, ``is_staticmethod``,
  ``is_classmethod``, ``is_cached_property``, ``is_overload``,
  ``is_dataclass``, and ``is_init`` fields.
- :func:`build_class_context` propagates :class:`ClassProfile` attribute data
  so the AI writes an ``Attributes`` section without guessing.
- :func:`build_function_context` extracts explicit ``raise`` targets from the
  body so the AI can populate a ``Raises`` section accurately.
- Decorator routing suppresses irrelevant sections: ``@property`` /
  ``@cached_property`` strip the Parameters list; ``@staticmethod`` /
  ``@classmethod`` are flagged explicitly; ``@overload`` variants are
  collected as signature hints rather than documented individually.
"""

from __future__ import annotations

import ast
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class ParameterInfo:
    """Represent a single callable parameter extracted from the AST."""

    name: str
    annotation: str
    has_default: bool
    is_vararg: bool = False
    is_kwarg: bool = False
    is_kwonly: bool = False


@dataclass
class AttributeInfo:
    """Represent a ``self.<attr>`` field for the Attributes docstring section.

    Parameters
    ----------
    name : str
        Attribute name without the ``self.`` prefix.
    type_hint : str
        Resolved type annotation, or ``""`` if unknown.
    description_hint : str
        Compact hint derived from the assigned expression — helps the AI write
        a meaningful description rather than ``TODO``.
    """

    name: str
    type_hint: str = ""
    description_hint: str = ""


@dataclass
class SymbolContext:
    """All information the AI needs to write one precise docstring.

    Parameters
    ----------
    kind : str
        One of ``"module"``, ``"class"``, ``"function"``, ``"method"``.
    name : str
        Simple symbol name (e.g. ``"parse_source"``).
    module_id : str
        Dotted import path of the module (e.g. ``"mypackage.utils"``).
    source_lines : list[str]
        De-indented source lines of the symbol body.
    signature : str
        Full ``def``/``class`` line.  Empty for modules.
    parameters : list[ParameterInfo]
        Ordered parameters (empty for modules and classes, and for
        ``@property`` / ``@cached_property`` getters).
    return_annotation : str
        Return annotation text, or ``""`` if absent or ``"None"``.
    decorators : list[str]
        Decorator names in source order.
    enclosing_class : str
        Name of the enclosing class, or ``""`` for module-level symbols.
    module_docstring : str
        Existing module docstring, or ``""``.
    module_summary_block : str
        AI-generated prose block from :class:`ModuleSummary` — richer than
        ``module_docstring`` because it includes the purpose paragraph and
        a class/function inventory.  Empty when no pre-pass was run.
    class_docstring : str
        Existing or just-generated class docstring for method contexts.
    class_attributes : list[AttributeInfo]
        Resolved ``self.*`` attributes for the ``Attributes`` section.
        Populated only for class-kind contexts.
    sibling_docstrings : list[str]
        Up to 3 docstrings from adjacent siblings for style mirroring.
    overload_siblings : list[str]
        Signatures of ``@overload`` variants of this function/method.
    imports : list[str]
        Top-level import lines from the module.
    raises_types : list[str]
        Exception class names raised explicitly in the function body.
    is_async : bool
        True for ``async def``.
    is_property : bool
        True for ``@property`` getters.
    is_cached_property : bool
        True for ``@cached_property`` or ``@functools.cached_property``.
    is_abstract : bool
        True for ``@abstractmethod``.
    is_staticmethod : bool
        True for ``@staticmethod``.
    is_classmethod : bool
        True for ``@classmethod``.
    is_overload : bool
        True for ``@overload`` stub variants.
    is_dataclass : bool
        True when the enclosing class is a ``@dataclass``.
    is_init : bool
        True when the method name is ``__init__``.
    lineno : int
        1-based line number of the ``def``/``class`` keyword.
    """

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


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _safe_unparse(node: ast.expr | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def _decorator_names(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
) -> list[str]:
    names: list[str] = []
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name):
            names.append(dec.id)
        elif isinstance(dec, ast.Attribute):
            names.append(dec.attr)   # functools.cached_property → "cached_property"
        else:
            try:
                names.append(ast.unparse(dec))
            except Exception:
                pass
    return names


def _extract_parameters(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[ParameterInfo]:
    args = node.args
    result: list[ParameterInfo] = []

    posonly = list(args.posonlyargs)
    normal = list(args.args)
    all_regular = posonly + normal
    defaults_offset = len(all_regular) - len(args.defaults)

    for idx, arg in enumerate(all_regular):
        if arg.arg in {"self", "cls"}:
            continue
        result.append(ParameterInfo(
            name=arg.arg,
            annotation=_safe_unparse(arg.annotation) or "object",
            has_default=idx >= defaults_offset,
        ))

    if args.vararg is not None:
        result.append(ParameterInfo(
            name=args.vararg.arg,
            annotation=_safe_unparse(args.vararg.annotation) or "object",
            has_default=False,
            is_vararg=True,
        ))

    for idx, arg in enumerate(args.kwonlyargs):
        result.append(ParameterInfo(
            name=arg.arg,
            annotation=_safe_unparse(arg.annotation) or "object",
            has_default=args.kw_defaults[idx] is not None,
            is_kwonly=True,
        ))

    if args.kwarg is not None:
        result.append(ParameterInfo(
            name=args.kwarg.arg,
            annotation=_safe_unparse(args.kwarg.annotation) or "object",
            has_default=False,
            is_kwarg=True,
        ))

    return result


def _extract_imports(tree: ast.Module) -> list[str]:
    lines: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            try:
                lines.append(ast.unparse(node))
            except Exception:
                pass
        elif not isinstance(node, (ast.Expr, ast.Assign)):
            break
    return lines


def _extract_sibling_docstrings(
    parent_body: Sequence[ast.stmt],
    target_lineno: int,
    max_siblings: int = 3,
) -> list[str]:
    """Return up to *max_siblings* existing docstrings from sibling callables.

    Parameters
    ----------
    parent_body : Sequence[ast.stmt]
        Body of the enclosing scope.
    target_lineno : int
        Line of the symbol being documented — excluded.
    max_siblings : int, optional
        Maximum number of docstrings to collect.

    Returns
    -------
    list[str]
        Docstring bodies of sibling callables.
    """
    siblings: list[str] = []
    for node in parent_body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if node.lineno == target_lineno:
            continue
        doc = ast.get_docstring(node, clean=True)
        if doc:
            siblings.append(doc)
        if len(siblings) >= max_siblings:
            break
    return siblings


def _extract_overload_siblings(
    class_node: ast.ClassDef | None,
    module_body: list[ast.stmt],
    func_name: str,
    target_lineno: int,
) -> list[str]:
    """Collect ``@overload`` signatures for the same function name.

    Parameters
    ----------
    class_node : ast.ClassDef or None
        Enclosing class, or ``None`` for module-level functions.
    module_body : list[ast.stmt]
        Module-level statements.
    func_name : str
        Function name to search for.
    target_lineno : int
        Line of the implementation variant — excluded.

    Returns
    -------
    list[str]
        One signature string per ``@overload`` variant.
    """
    search_body: Sequence[ast.stmt] = class_node.body if class_node else module_body
    overloads: list[str] = []
    for node in search_body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name != func_name or node.lineno == target_lineno:
            continue
        dec_names = [
            d.id if isinstance(d, ast.Name)
            else (d.attr if isinstance(d, ast.Attribute) else "")
            for d in node.decorator_list
        ]
        if "overload" in dec_names:
            try:
                sig = ast.unparse(node).splitlines()[0].rstrip(":")
                overloads.append(sig)
            except Exception:
                pass
    return overloads


def _extract_raises(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[str]:
    """Return exception class names raised explicitly inside *node*.

    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        Function or method to scan.

    Returns
    -------
    list[str]
        Deduplicated exception names in order of first appearance.
    """
    seen: set[str] = set()
    raises: list[str] = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Raise) or child.exc is None:
            continue
        exc = child.exc
        if isinstance(exc, ast.Call):
            exc = exc.func
        name = _safe_unparse(exc).split(".")[-1]
        if name and name not in seen:
            seen.add(name)
            raises.append(name)
    return raises


def _source_of_node(source_lines: list[str], node: ast.AST) -> list[str]:
    start = getattr(node, "lineno", 1) - 1
    end = getattr(node, "end_lineno", start + 1)
    raw = source_lines[start:end]
    return textwrap.dedent("\n".join(raw)).splitlines()


def _class_containing(tree: ast.Module, lineno: int) -> ast.ClassDef | None:
    """Return the innermost ClassDef that contains *lineno*, or None.

    Parameters
    ----------
    tree : ast.Module
        Root AST.
    lineno : int
        Source line to locate.

    Returns
    -------
    ast.ClassDef or None
        Innermost enclosing class node.
    """
    best: ast.ClassDef | None = None
    best_span = float("inf")
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        end = getattr(node, "end_lineno", node.lineno)
        if node.lineno <= lineno <= end:
            span = end - node.lineno
            if span < best_span:
                best = node
                best_span = span
    return best


def _build_attribute_infos(class_profile: object) -> list[AttributeInfo]:
    """Convert a :class:`ClassProfile` into :class:`AttributeInfo` objects.

    Parameters
    ----------
    class_profile : ClassProfile
        Profile from the module summarizer — accessed duck-typed so
        this module has no hard import dependency on ``module_summarizer``.

    Returns
    -------
    list[AttributeInfo]
        One entry per ``self.*`` attribute.
    """
    result: list[AttributeInfo] = []
    for init_attr in getattr(class_profile, "init_attributes", []):
        name = getattr(init_attr, "name", "")
        type_hint = getattr(init_attr, "type_hint", "")
        assigned_from = getattr(init_attr, "assigned_from", "")
        hint = f"Initialised from {assigned_from}." if assigned_from and assigned_from != name else ""
        result.append(AttributeInfo(name=name, type_hint=type_hint, description_hint=hint))
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_module_context(
    path: Path,
    module_id: str,
    tree: ast.Module,
    source_lines: list[str],
    module_summary: object | None = None,
) -> SymbolContext:
    """Build a :class:`SymbolContext` for a module-level docstring insertion.

    Parameters
    ----------
    path : Path
        Filesystem path to the module file.
    module_id : str
        Dotted module identifier (e.g. ``"mypackage.utils"``).
    tree : ast.Module
        Parsed AST of the module.
    source_lines : list[str]
        Raw lines of the source file.
    module_summary : ModuleSummary, optional
        Pre-pass summary; when present, populates ``module_summary_block``.

    Returns
    -------
    SymbolContext
        Populated context ready to pass to the AI generator.
    """
    summary_block = getattr(module_summary, "context_block", "") if module_summary else ""
    return SymbolContext(
        kind="module",
        name=path.stem,
        module_id=module_id,
        source_lines=source_lines[:60],
        imports=_extract_imports(tree),
        module_summary_block=summary_block,
        lineno=1,
    )


def build_class_context(
    node: ast.ClassDef,
    tree: ast.Module,
    module_id: str,
    source_lines: list[str],
    module_docstring: str = "",
    module_summary: object | None = None,
) -> SymbolContext:
    """Build a :class:`SymbolContext` for a class-level docstring insertion.

    Parameters
    ----------
    node : ast.ClassDef
        The class AST node.
    tree : ast.Module
        Root AST of the module.
    module_id : str
        Dotted module identifier.
    source_lines : list[str]
        Raw lines of the source file.
    module_docstring : str, optional
        Existing module docstring for additional context.
    module_summary : ModuleSummary, optional
        Pre-pass module summary; provides ``class_attributes`` via the
        pre-computed :class:`ClassProfile` and ``module_summary_block``.

    Returns
    -------
    SymbolContext
        Populated context ready to pass to the AI generator.
    """
    # Resolve ClassProfile from module summary for attribute inference.
    class_profile: object | None = None
    if module_summary is not None:
        try:
            from module_summarizer import get_class_profile
            class_profile = get_class_profile(module_summary, node.name)
        except ImportError:
            pass

    class_src = _source_of_node(source_lines, node)
    if len(class_src) > 80:
        class_src = class_src[:80]

    init_node = next(
        (
            n for n in node.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and n.name == "__init__"
        ),
        None,
    )
    params: list[ParameterInfo] = []
    if init_node is not None:
        params = _extract_parameters(init_node)

    decorators = _decorator_names(node)
    base_names = [_safe_unparse(b) for b in node.bases if _safe_unparse(b)]
    sig = f"class {node.name}"
    if base_names:
        sig += f"({', '.join(base_names)})"
    sig += ":"

    siblings = _extract_sibling_docstrings(tree.body, node.lineno)
    attrs = _build_attribute_infos(class_profile) if class_profile else []
    is_dataclass = "dataclass" in decorators
    is_abstract = any(b in {"ABC", "ABCMeta"} for b in base_names)
    summary_block = getattr(module_summary, "context_block", "") if module_summary else ""

    return SymbolContext(
        kind="class",
        name=node.name,
        module_id=module_id,
        source_lines=class_src,
        signature=sig,
        parameters=params,
        decorators=decorators,
        module_docstring=module_docstring,
        module_summary_block=summary_block,
        class_attributes=attrs,
        sibling_docstrings=siblings,
        imports=_extract_imports(tree),
        is_abstract=is_abstract,
        is_dataclass=is_dataclass,
        lineno=node.lineno,
    )


def build_function_context(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    tree: ast.Module,
    module_id: str,
    source_lines: list[str],
    module_docstring: str = "",
    class_docstring: str = "",
    module_summary: object | None = None,
) -> SymbolContext:
    """Build a :class:`SymbolContext` for a function or method docstring insertion.

    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        The function or method AST node.
    tree : ast.Module
        Root AST of the module.
    module_id : str
        Dotted module identifier.
    source_lines : list[str]
        Raw lines of the source file.
    module_docstring : str, optional
        Existing module docstring for context.
    class_docstring : str, optional
        Enclosing class docstring — pass the just-generated one when using
        the two-pass ``__init__``-first pattern.
    module_summary : ModuleSummary, optional
        Pre-pass summary; provides ``module_summary_block`` and
        ``is_dataclass`` resolution from :class:`ClassProfile`.

    Returns
    -------
    SymbolContext
        Populated context ready to pass to the AI generator.
    """
    func_src = _source_of_node(source_lines, node)
    if len(func_src) > 60:
        func_src = func_src[:60]

    decorators = _decorator_names(node)
    params = _extract_parameters(node)

    ret = _safe_unparse(node.returns)
    if ret in {"None", ""}:
        ret = ""

    is_async = isinstance(node, ast.AsyncFunctionDef)
    is_property = "property" in decorators
    is_cached_property = "cached_property" in decorators
    is_abstract = "abstractmethod" in decorators
    is_staticmethod = "staticmethod" in decorators
    is_classmethod = "classmethod" in decorators
    is_overload = "overload" in decorators
    is_init = node.name == "__init__"

    # Property / cached_property getters: strip parameters from context.
    if is_property or is_cached_property:
        params = []

    enclosing = _class_containing(tree, node.lineno)
    enclosing_name = enclosing.name if enclosing else ""

    # Resolve dataclass flag from ClassProfile when available.
    is_dataclass_ctx = False
    if enclosing is not None:
        enc_decs = _decorator_names(enclosing)
        is_dataclass_ctx = "dataclass" in enc_decs
    if module_summary is not None and enclosing_name:
        try:
            from module_summarizer import get_class_profile
            cp = get_class_profile(module_summary, enclosing_name)
            if cp is not None:
                is_dataclass_ctx = getattr(cp, "is_dataclass", False)
        except ImportError:
            pass

    parent_body: list[ast.stmt] = tree.body
    if enclosing is not None:
        parent_body = enclosing.body  # type: ignore[assignment]

    siblings = _extract_sibling_docstrings(parent_body, node.lineno)
    overloads = _extract_overload_siblings(enclosing, tree.body, node.name, node.lineno)
    raises = _extract_raises(node)

    try:
        signature = ast.unparse(node).splitlines()[0].rstrip(":")
        if len(signature) > 200:
            signature = signature[:200] + " ..."
    except Exception:
        signature = f"def {node.name}(...)"

    kind = "method" if enclosing_name else "function"
    summary_block = getattr(module_summary, "context_block", "") if module_summary else ""

    return SymbolContext(
        kind=kind,
        name=node.name,
        module_id=module_id,
        source_lines=func_src,
        signature=signature,
        parameters=params,
        return_annotation=ret,
        decorators=decorators,
        enclosing_class=enclosing_name,
        module_docstring=module_docstring,
        module_summary_block=summary_block,
        class_docstring=class_docstring,
        sibling_docstrings=siblings,
        overload_siblings=overloads,
        imports=_extract_imports(tree),
        raises_types=raises,
        is_async=is_async,
        is_property=is_property,
        is_cached_property=is_cached_property,
        is_abstract=is_abstract,
        is_staticmethod=is_staticmethod,
        is_classmethod=is_classmethod,
        is_overload=is_overload,
        is_dataclass=is_dataclass_ctx,
        is_init=is_init,
        lineno=node.lineno,
    )
