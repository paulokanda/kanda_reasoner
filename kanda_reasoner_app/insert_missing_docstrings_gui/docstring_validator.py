#!/usr/bin/env python3
# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/docstring_validator.py
"""Post-generation docstring validator with confidence scoring."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .context_builder import SymbolContext


@dataclass
class ValidationConfig:
    """Represent validation config."""
    
    max_line_length: int = 88
    max_todo_ratio: float = 0.5
    min_confidence: str = "low"
    max_length: int = 4000
    allow_invented_params: bool = False
    allow_invented_raises: bool = False


@dataclass
class ValidationResult:
    """Represent validation result."""
    
    ok: bool
    cleaned: str
    confidence: str = "high"
    issues: list[str] = field(default_factory=list)
    fatal_reason: str = ""
    ai_uncertain_comment: str = ""

    @classmethod
    def fatal(cls, reason: str) -> "ValidationResult":
        """Support fatal behavior.
        
        Parameters
        ----------
        reason : str
            The reason value.
        
        Returns
        -------
        'ValidationResult'
            The 'validation result' result.
        """
        
        return cls(ok=False, cleaned="", confidence="low", issues=[reason], fatal_reason=reason)


_SECTION_NAMES = ("Parameters", "Returns", "Raises", "Attributes", "Notes", "Examples")
_SECTION_RE = re.compile(r"^(%s)\s*$" % "|".join(re.escape(s) for s in _SECTION_NAMES), re.MULTILINE)



def _strip_quotes_and_fences(text: str) -> str:
    """Support strip quotes and fences behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    cleaned = text.strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 3:
            cleaned = "\n".join(lines[1:-1]).strip()
        else:
            cleaned = ""
    if cleaned.startswith('"""') and cleaned.endswith('"""') and len(cleaned) >= 6:
        cleaned = cleaned[3:-3].strip()
    elif cleaned.startswith("'''") and cleaned.endswith("'''") and len(cleaned) >= 6:
        cleaned = cleaned[3:-3].strip()
    return cleaned


def _contains_triple_quote_token(text: str) -> bool:
    """Support contains triple quote token behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return ('"""' in text) or ("'''" in text)


def _looks_like_quote_only_output(text: str) -> bool:
    """Support looks like quote only output behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    stripped = text.strip()
    return stripped in {'"""', "'''", '"', "'", '""', "''"}

def _find_section(lines: list[str], title: str) -> tuple[int, int] | None:
    """Support find section behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    title : str
        The title value.
    
    Returns
    -------
    tuple[int, int] | None
        The tuple of values.
    """
    
    for idx, line in enumerate(lines):
        if line.strip() != title:
            continue
        if idx + 1 < len(lines) and set(lines[idx + 1].strip()) == {"-"}:
            return idx, idx + 2
    return None


def _extract_param_names(lines: list[str]) -> list[str]:
    """Support extract param names behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    span = _find_section(lines, "Parameters")
    if span is None:
        return []
    _, start = span
    names: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped in _SECTION_NAMES:
            break
        if ":" in stripped and not line.startswith(" "):
            names.append(stripped.split(":", 1)[0].strip().lstrip("*"))
    return names


def _extract_raise_names(lines: list[str]) -> list[str]:
    """Support extract raise names behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    span = _find_section(lines, "Raises")
    if span is None:
        return []
    _, start = span
    names: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped in _SECTION_NAMES:
            break
        if not line.startswith(" "):
            names.append(stripped)
    return names


def validate(docstring: str, ctx: SymbolContext, config: ValidationConfig) -> ValidationResult:
    """Support validate behavior.
    
    Parameters
    ----------
    docstring : str
        The docstring value.
    ctx : SymbolContext
        The ctx value.
    config : ValidationConfig
        The configuration data.
    
    Returns
    -------
    ValidationResult
        The validation result result.
    """
    
    cleaned = _strip_quotes_and_fences(docstring)
    if not cleaned:
        return ValidationResult.fatal("Empty docstring output.")
    if len(cleaned) > config.max_length:
        return ValidationResult.fatal(f"Docstring exceeds max length of {config.max_length} characters.")

    if _looks_like_quote_only_output(cleaned):
        return ValidationResult.fatal("Output is only quote delimiters, not a docstring body.")

    if _contains_triple_quote_token(cleaned):
        return ValidationResult.fatal("Output contains triple-quote delimiters and is unsafe to insert.")

    lowered = cleaned.lstrip()
    if lowered.startswith(("def ", "class ", "import ", "from ")):
        return ValidationResult.fatal("Output looks like source code, not a docstring.")

    first_non_blank = next((line.strip() for line in cleaned.splitlines() if line.strip()), "")
    if _looks_like_quote_only_output(first_non_blank):
        return ValidationResult.fatal("Output starts with quote delimiters instead of docstring content.")

    lines = [line.rstrip() for line in cleaned.splitlines()]
    issues: list[str] = []

    long_lines = [idx + 1 for idx, line in enumerate(lines) if len(line) > config.max_line_length]
    if long_lines:
        issues.append(f"Lines exceed max length {config.max_line_length}: {long_lines[:5]}")

    non_blank = [line for line in lines if line.strip()]
    todo_count = sum(1 for line in non_blank if "TODO" in line)
    if non_blank:
        todo_ratio = todo_count / len(non_blank)
        if todo_ratio > config.max_todo_ratio:
            issues.append(
                f"TODO ratio {todo_ratio:.2f} exceeds configured maximum {config.max_todo_ratio:.2f}"
            )

    documented_params = _extract_param_names(lines)
    valid_params = {param.name for param in ctx.parameters}
    invented_params = [name for name in documented_params if name not in valid_params]
    if invented_params and not config.allow_invented_params:
        return ValidationResult.fatal(
            f"Docstring invents parameter names not in signature: {invented_params}"
        )
    if invented_params:
        issues.append(f"Invented parameters allowed by config: {invented_params}")

    documented_raises = _extract_raise_names(lines)
    valid_raises = set(ctx.raises_types)
    invented_raises = [name for name in documented_raises if valid_raises and name not in valid_raises]
    if invented_raises and not config.allow_invented_raises:
        return ValidationResult.fatal(
            f"Docstring invents exception types not found in body: {invented_raises}"
        )
    if invented_raises:
        issues.append(f"Invented raises allowed by config: {invented_raises}")

    section_titles = [m.group(1) for m in _SECTION_RE.finditer(cleaned)]
    ordered = [name for name in _SECTION_NAMES if name in section_titles]
    if section_titles != ordered:
        issues.append(f"Non-canonical section order: {section_titles}")

    confidence = "high"
    if issues:
        confidence = "medium"
    if any("TODO ratio" in issue for issue in issues):
        confidence = "low"

    threshold = {"low": 0, "medium": 1, "high": 2}
    if threshold[confidence] < threshold[config.min_confidence]:
        return ValidationResult(
            ok=False,
            cleaned="",
            confidence=confidence,
            issues=issues,
            fatal_reason=f"Confidence {confidence} is below configured minimum {config.min_confidence}.",
        )

    uncertain_comment = "# AI-UNCERTAIN" if confidence == "low" else ""
    return ValidationResult(
        ok=True,
        cleaned=cleaned,
        confidence=confidence,
        issues=issues,
        ai_uncertain_comment=uncertain_comment,
    )
