# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/heuristic_docstrings.py
# ---------------------------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/heuristic_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Deterministic heuristic docstring builders
# EXPORTS       : function_summary, class_summary, module_summary, build_module_docstring, build_class_docstring, iter_function_parameters, build_function_docstring
# DEPENDS ON    : symbol_naming.py
# REFACTOR DATE : 2026-06-06
# ---------------------------------------------------------------------------
"""Deterministic heuristic docstring builders."""

from __future__ import annotations

import ast
from pathlib import Path

from .symbol_naming import expr_to_text, prettify_name

__all__ = [
    "function_summary",
    "class_summary",
    "module_summary",
    "build_module_docstring",
    "build_class_docstring",
    "iter_function_parameters",
    "build_function_docstring",
]

_PREFIX_VERBS = {
    "get_": "Return the",
    "read_": "Return the",
    "load_": "Load the",
    "find_": "Find the",
    "build_": "Build a",
    "create_": "Create a",
    "make_": "Make a",
    "format_": "Format the",
    "parse_": "Parse the",
    "normalize_": "Normalize the",
    "resolve_": "Resolve the",
    "compute_": "Compute the",
    "calculate_": "Calculate the",
    "validate_": "Validate the",
    "check_": "Check the",
    "detect_": "Detect the",
    "extract_": "Extract the",
    "render_": "Render the",
    "show_": "Show the",
    "hide_": "Hide the",
    "emit_": "Emit the",
    "scan_": "Scan the",
    "run_": "Run the",
    "save_": "Save the",
    "write_": "Write the",
    "update_": "Update the",
    "set_": "Set the",
    "apply_": "Apply the",
    "delete_": "Delete the",
    "remove_": "Remove the",
}

_PARAMETER_DESCRIPTIONS = {
    "args": "The positional arguments.",
    "callback": "The callback function.",
    "callbacks": "The callback functions.",
    "cfg": "The configuration data.",
    "config": "The configuration data.",
    "data": "The input data.",
    "default": "The default value.",
    "defaults": "The default values.",
    "destination": "The destination path.",
    "error": "The error value.",
    "errors": "The error values.",
    "event": "The event object.",
    "events": "The event objects.",
    "fallback": "The fallback value.",
    "file": "The file value.",
    "file_path": "The file path.",
    "filename": "The file name.",
    "folder": "The folder path.",
    "index": "The index value.",
    "item": "The item value.",
    "items": "The item values.",
    "key": "The key value.",
    "keys": "The key values.",
    "line": "The line value.",
    "lines": "The line values.",
    "message": "The message text.",
    "messages": "The message values.",
    "mode": "The selected mode.",
    "name": "The name value.",
    "names": "The name values.",
    "node": "The syntax tree node.",
    "options": "The option values.",
    "other": "The comparison value.",
    "owner": "The owning object.",
    "path": "The file or folder path.",
    "paths": "The file or folder paths.",
    "project_root": "The project root path.",
    "raw": "The raw input value.",
    "raw_text": "The raw text value.",
    "record": "The record value.",
    "records": "The record values.",
    "retries": "The retry count.",
    "root": "The root path.",
    "row": "The row data.",
    "rows": "The row data values.",
    "source": "The source value.",
    "source_text": "The source text.",
    "target": "The target value.",
    "text": "The text value.",
    "timeout": "The timeout value.",
    "tree": "The parsed syntax tree.",
    "value": "The input value.",
    "values": "The input values.",
}

_RETURN_DESCRIPTIONS = {
    "bool": "True if the condition is met; otherwise, False.",
    "dict": "The mapped values.",
    "float": "The floating-point result.",
    "int": "The integer result.",
    "list": "The list of values.",
    "Path": "The resolved path.",
    "str": "The string result.",
    "tuple": "The tuple of values.",
}


def _sentence(text: str) -> str:
    """Return text as a normalized sentence."""
    cleaned = " ".join(str(text or "").strip().split())
    if not cleaned:
        return "The generated result."
    if cleaned.endswith((".", "!", "?")):
        return cleaned
    return cleaned + "."


def _words(name: str) -> str:
    """Return a readable lowercase phrase for a Python identifier."""
    return " ".join(prettify_name(str(name or "")).split())


def _tail_for_prefix(name: str, prefix: str) -> str:
    """Return the readable identifier tail after a prefix."""
    tail = str(name or "")[len(prefix):]
    words = _words(tail)
    return words or _words(name) or "target"


def function_summary(name: str) -> str:
    """Return a conservative one-line summary for a function name."""
    raw_name = str(name or "").strip()
    lower = raw_name.lower()
    for prefix, phrase in _PREFIX_VERBS.items():
        if lower.startswith(prefix):
            tail = _tail_for_prefix(raw_name, prefix)
            return _sentence(f"{phrase} {tail}")
    if lower.startswith("is_"):
        tail = _tail_for_prefix(raw_name, "is_")
        return _sentence(f"Return whether {tail}")
    if lower.startswith("has_"):
        tail = _tail_for_prefix(raw_name, "has_")
        return _sentence(f"Return whether {tail}")
    words = _words(raw_name) or "target"
    return _sentence(f"Support {words} behavior")


def class_summary(name: str) -> str:
    """Return a conservative one-line summary for a class name."""
    words = _words(name) or str(name or "target")
    return _sentence(f"Represent {words}")


def module_summary(path: Path, module_id: str) -> str:
    """Return a conservative one-line summary for a module path."""
    if path.name == "__init__.py":
        package_name = module_id or path.parent.name
        package_words = _words(package_name.split(".")[-1])
        return _sentence(f"Package facade for {package_words or package_name}")
    stem_words = _words(path.stem)
    return _sentence(f"Utilities and definitions for {stem_words or path.stem}")


def _target_phrase_from_function(function_name: str) -> str:
    """Return a likely target phrase from a function name."""
    raw_name = str(function_name or "").strip()
    lower = raw_name.lower()
    for prefix in _PREFIX_VERBS:
        if lower.startswith(prefix):
            return _tail_for_prefix(raw_name, prefix)
    return ""


def _parameter_description(
    name: str,
    annotation: str,
    has_default: bool,
    function_name: str,
) -> str:
    """Return a neutral parameter description without placeholders."""
    del annotation
    clean_name = str(name or "").lstrip("*")
    if clean_name == "name":
        target = _target_phrase_from_function(function_name)
        if target:
            return _sentence(f"The {target} name")
    if clean_name in _PARAMETER_DESCRIPTIONS:
        return _PARAMETER_DESCRIPTIONS[clean_name]
    words = _words(clean_name) or "value"
    if has_default:
        return _sentence(f"The optional {words} value")
    return _sentence(f"The {words} value")


def _type_base(type_text: str) -> str:
    """Return the outermost type name from an annotation string."""
    cleaned = str(type_text or "").strip()
    if not cleaned:
        return ""
    for marker in ("[", "(", "|"):
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0].strip()
    if "." in cleaned:
        cleaned = cleaned.rsplit(".", 1)[-1]
    return cleaned


def _return_description(return_text: str, function_name: str) -> str:
    """Return a neutral return description without placeholders."""
    clean_return = str(return_text or "").strip()
    base = _type_base(clean_return)
    if function_name == "main" and base == "int":
        return "The integer status code."
    if base in _RETURN_DESCRIPTIONS:
        return _RETURN_DESCRIPTIONS[base]
    if base.startswith("Sequence") or base.startswith("Iterable"):
        return "The sequence of values."
    if base.startswith("Mapping") or base.startswith("MutableMapping"):
        return "The mapped values."
    if base.endswith("Runner"):
        words = _words(base)
        return _sentence(f"A {words} instance")
    if base:
        words = _words(base)
        return _sentence(f"The {words} result")
    target = _target_phrase_from_function(function_name) or _words(function_name)
    return _sentence(f"The result produced by {target or 'the function'}")


def iter_function_parameters(node: ast.FunctionDef | ast.AsyncFunctionDef):
    """Yield parameter metadata in deterministic signature order."""
    args = node.args
    posonly = list(args.posonlyargs)
    normal = list(args.args)
    kwonly = list(args.kwonlyargs)

    ordered = []
    defaults_offset = len(posonly) + len(normal) - len(args.defaults)
    all_regular = posonly + normal

    for idx, arg in enumerate(all_regular):
        if arg.arg in {"self", "cls"}:
            continue
        default = None
        if idx >= defaults_offset:
            default = args.defaults[idx - defaults_offset]
        ordered.append((arg.arg, expr_to_text(arg.annotation), default is not None))

    if args.vararg is not None:
        ordered.append((f"*{args.vararg.arg}", expr_to_text(args.vararg.annotation), False))

    for idx, arg in enumerate(kwonly):
        default = args.kw_defaults[idx]
        ordered.append((arg.arg, expr_to_text(arg.annotation), default is not None))

    if args.kwarg is not None:
        ordered.append((f"**{args.kwarg.arg}", expr_to_text(args.kwarg.annotation), False))

    return ordered


def build_module_docstring(
    path: Path,
    module_id: str,
    tree: ast.Module,
    root: Path,
    manifest: dict | None,
) -> str:
    """Return a module docstring using neutral heuristic text."""
    del tree, root, manifest
    return f'"""{module_summary(path, module_id)}"""'


def build_class_docstring(node: ast.ClassDef) -> str:
    """Return a class docstring using neutral heuristic text."""
    return f'"""{class_summary(node.name)}"""'


def build_function_docstring(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Return a function docstring using neutral heuristic text."""
    lines: list[str] = []
    lines.append('"""' + function_summary(node.name))
    lines.append("")

    params = list(iter_function_parameters(node))
    if params:
        lines.append("Parameters")
        lines.append("----------")
        for name, annotation, has_default in params:
            suffix = ", optional" if has_default else ""
            lines.append(f"{name} : {annotation}{suffix}")
            description = _parameter_description(
                name,
                annotation,
                has_default,
                node.name,
            )
            lines.append(f"    {description}")
        lines.append("")

    returns_text = expr_to_text(node.returns) if node.returns is not None else ""
    if returns_text and returns_text != "None":
        lines.append("Returns")
        lines.append("-------")
        lines.append(f"{returns_text}")
        lines.append(f"    {_return_description(returns_text, node.name)}")
        lines.append("")

    if lines[-1] == "":
        lines.pop()

    lines.append('"""')
    return "\n".join(lines)
