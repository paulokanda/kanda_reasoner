# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/response_parsing.py
"""Response parsing for the AI docstring generator."""

from __future__ import annotations

__all__ = [
]

import json
from typing import Any

from ..context_builder import SymbolContext
from ..docstring_policy import DocstringPolicy
from .heuristics import _prettify


def _clean_summary(text: str, fallback: str) -> str:
    """Support clean summary behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    fallback : str
        The fallback value.
    
    Returns
    -------
    str
        The string result.
    """
    
    cleaned = " ".join((text or "").strip().split())
    if not cleaned:
        cleaned = fallback
    cleaned = cleaned.replace('"""', "").replace("'" * 3, "").strip()
    if cleaned and cleaned[-1] not in ".!?":
        cleaned += "."
    return cleaned


def _json_from_text(text: str) -> dict[str, Any]:
    """Support json from text behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 3:
            cleaned = "\n".join(lines[1:-1]).strip()
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end > start:
        candidate = cleaned[start : end + 1]
        data = json.loads(candidate)
        if isinstance(data, dict):
            return data
    raise ValueError("Model did not return valid JSON.")


def _render_structured_docstring(ctx: SymbolContext, policy: DocstringPolicy, payload: dict[str, Any]) -> str:
    """Support render structured docstring behavior.
    
    Parameters
    ----------
    ctx : SymbolContext
        The ctx value.
    policy : DocstringPolicy
        The policy value.
    payload : dict[str, Any]
        The payload value.
    
    Returns
    -------
    str
        The string result.
    """
    
    summary_fallback = (
        ctx.module_id.split(".")[-1].replace("_", " ")
        if ctx.kind == "module"
        else f"{_prettify(ctx.name) or ctx.name}"
    )
    lines: list[str] = [_clean_summary(str(payload.get("summary", "")), f"Describe {summary_fallback}.")]

    extended = str(payload.get("extended_description", "") or "").strip()
    if extended:
        lines.append("")
        lines.extend(line.rstrip() for line in extended.splitlines())

    if ctx.kind == "class" and policy.include_attributes_for_classes and ctx.class_attributes:
        attr_desc = {
            str(item.get("name", "")).strip(): str(item.get("description", "")).strip()
            for item in payload.get("attributes", []) or []
            if isinstance(item, dict) and str(item.get("name", "")).strip()
        }
        lines.extend(["", "Attributes", "----------"])
        for attr in ctx.class_attributes:
            lines.append(f"{attr.name} : {attr.type_hint or 'object'}")
            desc = attr_desc.get(attr.name) or f"TODO: describe {attr.name}."
            if not desc.endswith("."):
                desc += "."
            lines.append(f"    {desc}")

    if ctx.kind in {"function", "method"}:
        if ctx.parameters and not ctx.is_property and not ctx.is_cached_property:
            param_desc = {
                str(item.get("name", "")).lstrip("*").strip(): str(item.get("description", "")).strip()
                for item in payload.get("parameters", []) or []
                if isinstance(item, dict) and str(item.get("name", "")).strip()
            }
            lines.extend(["", "Parameters", "----------"])
            for param in ctx.parameters:
                suffix = ", optional" if param.has_default else ""
                prefix = "**" if param.is_kwarg else ("*" if param.is_vararg else "")
                lines.append(f"{prefix}{param.name} : {param.annotation}{suffix}")
                desc = param_desc.get(param.name) or f"TODO: describe {param.name}."
                if not desc.endswith("."):
                    desc += "."
                lines.append(f"    {desc}")

        if ctx.return_annotation and ctx.return_annotation != "None":
            return_obj = payload.get("returns") or {}
            return_desc = ""
            if isinstance(return_obj, dict):
                return_desc = str(return_obj.get("description", "")).strip()
            if not return_desc:
                return_desc = "TODO: describe the return value."
            if not return_desc.endswith("."):
                return_desc += "."
            lines.extend(["", "Returns", "-------", ctx.return_annotation, f"    {return_desc}"])

        if policy.include_raises_section and ctx.raises_types:
            raise_desc = {
                str(item.get("type", "")).strip(): str(item.get("description", "")).strip()
                for item in payload.get("raises", []) or []
                if isinstance(item, dict) and str(item.get("type", "")).strip()
            }
            lines.extend(["", "Raises", "------"])
            for exc_name in ctx.raises_types:
                lines.append(exc_name)
                desc = raise_desc.get(exc_name) or f"TODO: describe when {exc_name} is raised."
                if not desc.endswith("."):
                    desc += "."
                lines.append(f"    {desc}")

    notes = payload.get("notes") or []
    if policy.notes_enabled and isinstance(notes, list):
        cleaned_notes = [str(item).strip() for item in notes if str(item).strip()]
        if cleaned_notes:
            lines.extend(["", "Notes", "-----"])
            lines.extend(cleaned_notes)

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)
