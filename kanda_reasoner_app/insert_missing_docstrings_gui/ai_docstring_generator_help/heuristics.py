# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/heuristics.py
"""Heuristic fallback helpers for the AI docstring generator."""

from __future__ import annotations

__all__ = []

import re

from ..context_builder import ParameterInfo, SymbolContext
from ..docstring_policy import DocstringPolicy


_OBJECT_TYPES = {"", "object", "Any"}


def _prettify(name: str) -> str:
    """Return a readable lowercase phrase derived from a Python name."""
    return " ".join(
        re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name.replace("_", " ")).split()
    ).lower()


def _sentence(text: str) -> str:
    """Return text as a simple sentence."""
    cleaned = " ".join(str(text).strip().split())
    if not cleaned:
        return "Description derived from source context."
    if cleaned.endswith((".", "!", "?")):
        return cleaned
    return cleaned + "."


def _display_type(type_text: str) -> str:
    """Return a stable display type for fallback docstrings."""
    cleaned = str(type_text or "").strip()
    if cleaned in _OBJECT_TYPES:
        return "object"
    return cleaned


def _name_phrase(name: str) -> str:
    """Return a phrase based only on the symbol name."""
    return _prettify(name) or name


def _heuristic_function_summary(name: str) -> str:
    """Return a conservative one-line summary derived from the function name."""
    lower = name.lower()
    prefix_map = {
        "get_": "Get",
        "set_": "Set",
        "build_": "Build",
        "create_": "Create",
        "make_": "Make",
        "load_": "Load",
        "save_": "Save",
        "update_": "Update",
        "compute_": "Compute",
        "normalize_": "Normalize",
        "resolve_": "Resolve",
        "detect_": "Detect",
        "extract_": "Extract",
        "apply_": "Apply",
        "render_": "Render",
        "show_": "Show",
        "hide_": "Hide",
        "emit_": "Emit",
        "handle_": "Handle",
        "run_": "Run",
        "scan_": "Scan",
        "validate_": "Validate",
    }
    for prefix, verb in prefix_map.items():
        if lower.startswith(prefix):
            tail = _name_phrase(name[len(prefix):])
            return _sentence(f"{verb} {tail}")
    if lower.startswith("is_"):
        return _sentence(f"Return whether {_name_phrase(name[3:])}")
    if lower.startswith("has_"):
        return _sentence(f"Return whether {_name_phrase(name[4:])}")
    return _sentence(f"Handle {_name_phrase(name)}")


def _parameter_description(param: ParameterInfo) -> str:
    """Return a safe parameter description from extracted metadata."""
    phrase = _name_phrase(param.name)
    if param.is_vararg:
        return _sentence(f"Additional positional values for {phrase}")
    if param.is_kwarg:
        return _sentence(f"Additional keyword values for {phrase}")
    if param.has_default:
        return _sentence(f"Optional value for {phrase}")
    return _sentence(f"Value for {phrase}")


def _attribute_description(name: str, hint: str) -> str:
    """Return a safe class-attribute description from extracted metadata."""
    phrase = _name_phrase(hint or name)
    return _sentence(f"Attribute related to {phrase}")


def _return_description(ctx: SymbolContext) -> str:
    """Return a safe return description from the symbol context."""
    symbol_phrase = _name_phrase(ctx.name)
    return _sentence(f"Return value produced by {symbol_phrase}")


def _raise_description(ctx: SymbolContext, exc_name: str) -> str:
    """Return a safe raises description from the exception name and symbol context."""
    symbol_phrase = _name_phrase(ctx.name)
    exc_phrase = _name_phrase(exc_name)
    return _sentence(f"Raised by {symbol_phrase} when {exc_phrase} is reported")


def _heuristic_docstring(ctx: SymbolContext, policy: DocstringPolicy) -> str:
    """Build a conservative fallback docstring from source-extracted evidence."""
    if ctx.kind == "module":
        if ctx.module_summary_block:
            summary = ctx.module_summary_block.splitlines()[0]
            return summary.replace("Module purpose: ", "").strip()
        stem = ctx.name.replace("_", " ").lower()
        if ctx.name == "__init__":
            tail = ctx.module_id.split(".")[-1] or ctx.name
            return _sentence(f"Package facade for {tail}")
        return _sentence(f"Utilities and definitions for {stem or ctx.name}")

    if ctx.kind == "class":
        lines = [_sentence(f"Represent {_name_phrase(ctx.name)}")]
        if policy.include_attributes_for_classes and ctx.class_attributes:
            lines += ["", "Attributes", "----------"]
            for attr in ctx.class_attributes:
                attr_type = _display_type(attr.type_hint)
                lines.append(f"{attr.name} : {attr_type}")
                lines.append(f"    {_attribute_description(attr.name, attr.description_hint)}")
        return "\n".join(lines)

    lines: list[str] = [_heuristic_function_summary(ctx.name), ""]
    if ctx.parameters and not ctx.is_property and not ctx.is_cached_property:
        lines += ["Parameters", "----------"]
        for param in ctx.parameters:
            suffix = ", optional" if param.has_default else ""
            prefix = "**" if param.is_kwarg else ("*" if param.is_vararg else "")
            lines.append(f"{prefix}{param.name} : {_display_type(param.annotation)}{suffix}")
            lines.append(f"    {_parameter_description(param)}")
        lines.append("")
    if ctx.return_annotation and ctx.return_annotation != "None":
        lines += [
            "Returns",
            "-------",
            _display_type(ctx.return_annotation),
            f"    {_return_description(ctx)}",
            "",
        ]
    if policy.include_raises_section and ctx.raises_types:
        lines += ["Raises", "------"]
        for exc_name in ctx.raises_types:
            lines.append(exc_name)
            lines.append(f"    {_raise_description(ctx, exc_name)}")
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)
