# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/docstring_payloads.py
"""Docstring payloads for the AI docstring generator."""

from __future__ import annotations

__all__ = [
]

import json
from typing import Any

from ..context_builder import AttributeInfo, ParameterInfo, SymbolContext
from ..docstring_policy import DocstringPolicy


def _build_system_prompt(policy: DocstringPolicy, structured: bool) -> str:
    """Support build system prompt behavior.
    
    Parameters
    ----------
    policy : DocstringPolicy
        The policy value.
    structured : bool
        The structured value.
    
    Returns
    -------
    str
        The string result.
    """
    
    rules = [
        "You are a Python documentation expert.",
        "Document only what is supported by the provided source and metadata.",
        "Treat all GROUND-TRUTH sections as hard constraints, not suggestions.",
        "Do not invent parameter names, exception types, attributes, return values, side effects, or IO behavior.",
        "Unsupported claims are rejected by validation and must not be added to the docstring.",
        "If information is unclear, use short TODO-style descriptions instead of guessing.",
        "Never output Python code, markdown fences, or prose outside the requested format.",
    ]
    if structured:
        rules.append("Return valid JSON only. Do not wrap the JSON in markdown fences.")
    else:
        rules.extend(
            [
                "Write exactly one NumPy-style docstring body.",
                "Do not include surrounding triple quotes.",
                "Keep the one-line summary concise and end it with a period.",
            ]
        )
    return "\n".join("- " + rule if idx else rule for idx, rule in enumerate(rules))


def _format_attribute(attr: AttributeInfo) -> str:
    """Support format attribute behavior.
    
    Parameters
    ----------
    attr : AttributeInfo
        The attr value.
    
    Returns
    -------
    str
        The string result.
    """
    
    type_hint = attr.type_hint or "object"
    hint = attr.description_hint or ""
    return f"- {attr.name}: {type_hint} {hint}".strip()


def _format_parameter(param: ParameterInfo) -> str:
    """Support format parameter behavior.
    
    Parameters
    ----------
    param : ParameterInfo
        The param value.
    
    Returns
    -------
    str
        The string result.
    """
    
    prefix = "**" if param.is_kwarg else ("*" if param.is_vararg else "")
    suffix = " optional" if param.has_default else ""
    return f"- {prefix}{param.name}: {param.annotation}{suffix}"


def _docstring_schema() -> dict[str, Any]:
    """Support docstring schema behavior.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "extended_description": {"type": "string"},
            "parameters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["name", "description"],
                    "additionalProperties": False,
                },
            },
            "returns": {
                "type": "object",
                "properties": {"description": {"type": "string"}},
                "required": ["description"],
                "additionalProperties": False,
            },
            "raises": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["type", "description"],
                    "additionalProperties": False,
                },
            },
            "attributes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["name", "description"],
                    "additionalProperties": False,
                },
            },
            "notes": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["summary"],
        "additionalProperties": False,
    }

def _evidence_name_list(values: list[str]) -> str:
    """Support evidence name list behavior.
    
    Parameters
    ----------
    values : list[str]
        The input values.
    
    Returns
    -------
    str
        The string result.
    """
    
    clean = [str(value).strip() for value in values if str(value).strip()]
    return ", ".join(clean) if clean else "none"


def _evidence_parameter_names(ctx: SymbolContext) -> list[str]:
    """Support evidence parameter names behavior.
    
    Parameters
    ----------
    ctx : SymbolContext
        The ctx value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    names: list[str] = []
    for param in ctx.parameters:
        name = param.name.strip()
        if name and name not in {"self", "cls"}:
            names.append(name)
    return names


def _evidence_attribute_names(ctx: SymbolContext) -> list[str]:
    """Support evidence attribute names behavior.
    
    Parameters
    ----------
    ctx : SymbolContext
        The ctx value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return [attr.name for attr in ctx.class_attributes if attr.name]


def _evidence_raise_names(ctx: SymbolContext) -> list[str]:
    """Support evidence raise names behavior.
    
    Parameters
    ----------
    ctx : SymbolContext
        The ctx value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return [name for name in ctx.raises_types if name]


def _format_source_evidence(ctx: SymbolContext) -> str:
    """Support format source evidence behavior.
    
    Parameters
    ----------
    ctx : SymbolContext
        The ctx value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not ctx.source_lines:
        return "SOURCE EVIDENCE:\n- no source lines available"

    start_line = ctx.lineno or 1
    rows = ["SOURCE EVIDENCE:"]
    for offset, line in enumerate(ctx.source_lines[:80]):
        line_number = start_line + offset
        rows.append(f"{line_number}: {line}")
    if len(ctx.source_lines) > 80:
        rows.append("# source truncated after 80 lines")
    return "\n".join(rows)


def _build_evidence_ledger(ctx: SymbolContext) -> str:
    """Support build evidence ledger behavior.
    
    Parameters
    ----------
    ctx : SymbolContext
        The ctx value.
    
    Returns
    -------
    str
        The string result.
    """
    
    parameter_names = _evidence_parameter_names(ctx)
    attribute_names = _evidence_attribute_names(ctx)
    raise_names = _evidence_raise_names(ctx)

    rows = [
        "EVIDENCE LEDGER:",
        "- The following entries are the only allowed factual sources.",
        "- If a fact is not present here or in SOURCE EVIDENCE, omit it or mark it TODO.",
        f"- Allowed parameter names: {_evidence_name_list(parameter_names)}",
        f"- Allowed class attribute names: {_evidence_name_list(attribute_names)}",
        f"- Allowed explicit raise types: {_evidence_name_list(raise_names)}",
        f"- Allowed decorators: {_evidence_name_list(ctx.decorators)}",
        f"- Return annotation: {ctx.return_annotation or 'none'}",
        f"- Async: {ctx.is_async}",
        f"- Property: {ctx.is_property or ctx.is_cached_property}",
        f"- Classmethod: {ctx.is_classmethod}",
        f"- Staticmethod: {ctx.is_staticmethod}",
    ]
    return "\n".join(rows)

def _build_user_prompt(ctx: SymbolContext, policy: DocstringPolicy, structured: bool) -> str:
    """Support build user prompt behavior.
    
    Parameters
    ----------
    ctx : SymbolContext
        The ctx value.
    policy : DocstringPolicy
        The policy value.
    structured : bool
        The structured value.
    
    Returns
    -------
    str
        The string result.
    """
    
    parts = [
        f"KIND: {ctx.kind}",
        f"MODULE: {ctx.module_id}",
        f"NAME: {ctx.full_name}",
        "",
        "HALLUCINATION GUARDRAILS:",
        "- Do not invent parameters, return values, exceptions, attributes, IO, side effects, or state changes.",
        "- Use only names present in EVIDENCE LEDGER or SOURCE EVIDENCE.",
        "- If evidence is incomplete, write a concise TODO instead of guessing.",
        "- Omit unsupported sections by returning empty arrays or omitting optional objects.",
        "",
        _build_evidence_ledger(ctx),
    ]

    if ctx.signature:
        parts.append(f"SIGNATURE: {ctx.signature}")
    if ctx.decorators:
        parts.append("DECORATORS: " + ", ".join("@" + item for item in ctx.decorators))
    if ctx.module_docstring:
        parts.append("MODULE DOCSTRING:\n" + "\n".join(ctx.module_docstring.strip().splitlines()[:8]))
    if ctx.module_summary_block:
        parts.append("MODULE SUMMARY CONTEXT:\n" + ctx.module_summary_block)
    if ctx.class_docstring:
        parts.append("CLASS DOCSTRING: " + " ".join(ctx.class_docstring.strip().splitlines()[:6]))
    if ctx.imports:
        parts.append("IMPORTS:\n" + "\n".join("- " + item for item in ctx.imports[:25]))
    if ctx.parameters:
        parts.append("GROUND-TRUTH PARAMETERS:\n" + "\n".join(_format_parameter(param) for param in ctx.parameters))
    if ctx.class_attributes:
        parts.append("CLASS ATTRIBUTES:\n" + "\n".join(_format_attribute(attr) for attr in ctx.class_attributes[:30]))
    if ctx.raises_types:
        parts.append("GROUND-TRUTH EXPLICIT RAISES:\n" + "\n".join("- " + item for item in ctx.raises_types))
    if ctx.overload_siblings:
        parts.append("OVERLOADS:\n" + "\n".join(ctx.overload_siblings[:6]))
    if ctx.sibling_docstrings:
        parts.append("SIBLING DOCSTRINGS:\n" + "\n---\n".join(ctx.sibling_docstrings[:5]))

    parts.append(_format_source_evidence(ctx))

    if structured:
        parts.append("Return JSON that matches this schema exactly:")
        parts.append(json.dumps(_docstring_schema(), indent=2, ensure_ascii=False))
    else:
        parts.append(
            "Write the NumPy-style docstring body for the "
            f"{ctx.kind} '{ctx.full_name}'. Output ONLY the raw body "
            "no triple quotes, no indentation, no extra text."
        )

    if policy.prompt_rules_for_kind(ctx.kind):
        parts.append("PROJECT RULES:\n" + "\n".join("- " + rule for rule in policy.prompt_rules_for_kind(ctx.kind)))

    return "\n\n".join(parts)

