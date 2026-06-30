# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_style_runtime.py
"""AI docstring style enforcement helpers for Tab 3 review drafts."""

from __future__ import annotations

import re
from typing import Any

__all__ = [
    "AI_DOCSTRING_STYLE_CONTRACT",
    "apply_ai_docstring_style_contract",
    "normalize_normalized_docstring_for_verbosity",
    "selected_ai_docstring_verbosity_from_owner",
]

AI_DOCSTRING_STYLE_CONTRACT = "tab3_ai_docstring_style_contract_v1"


def selected_ai_docstring_verbosity_from_owner(owner: object) -> str:
    """Return the selected AI docstring verbosity from Tab 3 owner controls."""
    for name in (
        "_ai_docstring_verbosity_combo",
        "ai_docstring_verbosity_combo",
        "_docstring_verbosity_combo",
    ):
        widget = getattr(owner, name, None)
        current_text = getattr(widget, "currentText", None)
        if callable(current_text):
            value = _normalize_verbosity(current_text())
            if value:
                return value
        current_data = getattr(widget, "currentData", None)
        if callable(current_data):
            value = _normalize_verbosity(current_data())
            if value:
                return value
    return "concise"


def apply_ai_docstring_style_contract(body: str, request: Any) -> str:
    """Apply request-aware verbosity rules to a normalized docstring body."""
    mode = _normalize_verbosity(getattr(request, "docstring_verbosity", "concise"))
    normalized = str(body or "").strip()
    if mode == "concise":
        return _concise_docstring_body(normalized)
    if mode == "balanced":
        expanded = _expand_short_docstring_for_mode(normalized, request, "balanced")
        return _balanced_docstring_body(expanded)
    return _detailed_docstring_body(normalized, request)


def normalize_normalized_docstring_for_verbosity(body: str, verbosity: str) -> str:
    """Apply deterministic verbosity rules to an already normalized body."""
    mode = _normalize_verbosity(verbosity)
    normalized = str(body or "").strip()
    if mode == "concise":
        return _concise_docstring_body(normalized)
    if mode == "balanced":
        return _balanced_docstring_body(normalized)
    return normalized


def _detailed_docstring_body(body: str, request: Any) -> str:
    """Return a detailed body when the model returned a short body."""
    normalized = str(body or "").strip()
    if not normalized:
        return ""
    if _has_multiline_detail(normalized):
        return normalized
    return _expand_short_docstring_for_mode(normalized, request, "detailed")


def _expand_short_docstring_for_mode(body: str, request: Any, mode: str) -> str:
    """Expand a short one-line body using visible request metadata only."""
    summary = _first_non_empty_line(body)
    if not summary:
        return ""
    kind = str(getattr(request, "symbol_kind", "") or "").strip().lower()
    signature = str(getattr(request, "signature", "") or "")
    source = str(getattr(request, "source_snippet", "") or "")

    if kind in {"function", "method", "async_function", "async method"}:
        return _expand_function_docstring(summary, signature, mode)

    visible_names = _visible_source_names(source)
    if mode == "balanced":
        if visible_names:
            return summary + "\n" + "Includes " + _join_names(visible_names) + "."
        return summary + "\n" + "Documents the visible module behavior."

    if visible_names:
        detail = "This " + (kind or "module") + " includes " + _join_names(visible_names)
        detail += " based on the selected source snippet."
    else:
        detail = "This " + (kind or "module")
        detail += " documents the selected source behavior for review."
    return summary + "\n\n" + detail


def _expand_function_docstring(summary: str, signature: str, mode: str) -> str:
    """Expand a short function body from its visible signature."""
    params = _parse_signature_parameters(signature)
    return_type = _parse_return_type(signature)
    lines = [summary]

    if mode == "detailed":
        details = _function_detail_sentence(params, return_type)
        if details:
            lines.extend(["", details])

    if params:
        lines.extend(["", "Parameters", "----------"])
        for name, annotation, optional in params:
            type_text = annotation or "object"
            if optional:
                type_text += ", optional"
            lines.append(name + " : " + type_text)
            lines.append("    " + _parameter_description(name))

    if return_type and return_type.lower() not in {"none", "nonetype"}:
        lines.extend(["", "Returns", "-------", return_type])
        lines.append("    " + _return_description(return_type))

    return "\n".join(lines).strip()


def _function_detail_sentence(
    params: list[tuple[str, str, bool]], return_type: str
) -> str:
    """Return one factual function detail sentence from signature metadata."""
    parts: list[str] = []
    if params:
        parts.append("accepts " + _join_names([item[0] for item in params]))
    if return_type and return_type.lower() not in {"none", "nonetype"}:
        parts.append("returns " + return_type)
    if not parts:
        return ""
    return "This function " + " and ".join(parts) + "."


def _parse_signature_parameters(signature: str) -> list[tuple[str, str, bool]]:
    """Parse visible parameters from a Python-like signature string."""
    match = re.search(r"\((.*?)\)", str(signature or ""), flags=re.DOTALL)
    if not match:
        return []
    raw_params = match.group(1).strip()
    if not raw_params:
        return []
    result: list[tuple[str, str, bool]] = []
    for item in _split_signature_items(raw_params):
        name, annotation, optional = _parse_one_parameter(item)
        if name and name not in {"self", "cls"}:
            result.append((name, annotation, optional))
    return result


def _parse_one_parameter(item: str) -> tuple[str, str, bool]:
    """Parse one parameter item from a signature."""
    text = str(item or "").strip()
    if not text or text in {"*", "/"}:
        return "", "", False
    optional = "=" in text
    if "=" in text:
        text = text.split("=", 1)[0].strip()
    if ":" in text:
        name, annotation = text.split(":", 1)
    else:
        name, annotation = text, ""
    return name.strip().lstrip("*"), annotation.strip(), optional


def _parse_return_type(signature: str) -> str:
    """Parse a visible return type from a Python-like signature string."""
    if "->" not in str(signature or ""):
        return ""
    return str(signature).rsplit("->", 1)[1].strip().rstrip(":")


def _split_signature_items(raw_params: str) -> list[str]:
    """Split signature parameters while respecting shallow brackets."""
    result: list[str] = []
    current: list[str] = []
    depth = 0
    for char in raw_params:
        if char in "([{":
            depth += 1
        elif char in ")]}" and depth > 0:
            depth -= 1
        if char == "," and depth == 0:
            result.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        result.append("".join(current).strip())
    return result


def _parameter_description(name: str) -> str:
    """Return a neutral parameter description."""
    normalized = str(name or "").strip().lower()
    mapping = {
        "raw": "The raw input value.",
        "name": "The name value.",
        "path": "The file or folder path.",
        "config": "The configuration data.",
        "value": "The input value.",
        "values": "The input values.",
        "retries": "The retry count.",
    }
    return mapping.get(normalized, "The " + normalized.replace("_", " ") + " value.")


def _return_description(return_type: str) -> str:
    """Return a neutral return description."""
    normalized = str(return_type or "").strip()
    lower = normalized.lower()
    if lower == "str":
        return "The string result."
    if lower == "int":
        return "The integer result."
    if lower == "bool":
        return "True if the condition is met; otherwise, False."
    return "The returned " + normalized + " value."


def _visible_source_names(source: str) -> list[str]:
    """Return visible class/function names from a source snippet."""
    names: list[str] = []
    for pattern in (r"^\s*(?:async\s+def|def)\s+([A-Za-z_]\w*)\s*\(", r"^\s*class\s+([A-Za-z_]\w*)\b"):
        for match in re.finditer(pattern, str(source or ""), flags=re.MULTILINE):
            name = match.group(1)
            if not name.startswith("_") and name not in names:
                names.append(name)
    return names[:4]


def _join_names(names: list[str]) -> str:
    """Join names for a short English sentence."""
    clean = [str(name).strip() for name in names if str(name).strip()]
    if not clean:
        return "visible symbols"
    if len(clean) == 1:
        return clean[0]
    return ", ".join(clean[:-1]) + " and " + clean[-1]


def _has_multiline_detail(body: str) -> bool:
    """Return True if the body already has detailed content or sections."""
    lines = [line for line in str(body or "").splitlines() if line.strip()]
    if len(lines) >= 2:
        return True
    return any(_is_numpy_section_header(line) for line in lines)


def _concise_docstring_body(body: str) -> str:
    """Remove verbose free-text paragraphs from a concise AI docstring."""
    lines = body.splitlines()
    if not lines:
        return ""
    section_indices = [
        index for index, line in enumerate(lines) if _is_numpy_section_header(line)
    ]
    if not section_indices:
        return _first_non_empty_line(body)
    first_section = section_indices[0]
    summary = _first_non_empty_line("\n".join(lines[:first_section]))
    kept = [summary] if summary else []
    if kept:
        kept.append("")
    kept.extend(lines[first_section:])
    return _trim_section_descriptions("\n".join(kept).strip(), max_words=12)


def _balanced_docstring_body(body: str) -> str:
    """Limit excessive paragraphs while preserving useful sections."""
    lines = body.splitlines()
    if not lines:
        return ""
    section_indices = [
        index for index, line in enumerate(lines) if _is_numpy_section_header(line)
    ]
    if not section_indices:
        return "\n".join(_first_paragraph_lines(body, max_lines=2)).strip()
    first_section = section_indices[0]
    intro = _first_paragraph_lines("\n".join(lines[:first_section]), max_lines=2)
    kept = list(intro)
    if kept:
        kept.append("")
    kept.extend(lines[first_section:])
    return _trim_section_descriptions("\n".join(kept).strip(), max_words=22)


def _first_non_empty_line(body: str) -> str:
    """Return the first non-empty line from a docstring body."""
    for line in str(body or "").splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _first_paragraph_lines(body: str, max_lines: int) -> list[str]:
    """Return the first paragraph, capped to a small number of lines."""
    result: list[str] = []
    for line in str(body or "").splitlines():
        stripped = line.strip()
        if not stripped:
            if result:
                break
            continue
        result.append(stripped)
        if len(result) >= max(1, int(max_lines)):
            break
    return result


def _is_numpy_section_header(line: str) -> bool:
    """Return True if a line starts a common NumPy docstring section."""
    return line.strip() in {
        "Parameters",
        "Returns",
        "Raises",
        "Yields",
        "Notes",
        "Examples",
        "Attributes",
    }


def _trim_section_descriptions(body: str, max_words: int) -> str:
    """Trim obviously long indented section description lines."""
    result: list[str] = []
    for line in str(body or "").splitlines():
        if line.startswith("    ") and len(line.split()) > max_words:
            result.append("    " + _trim_sentence_words(line.strip(), max_words))
        else:
            result.append(line.rstrip())
    return "\n".join(result).strip()


def _trim_sentence_words(text: str, max_words: int) -> str:
    """Trim one sentence to a maximum number of words."""
    words = str(text or "").split()
    if len(words) <= max_words:
        return str(text or "").strip()
    trimmed = " ".join(words[:max_words]).rstrip(".,;:")
    return trimmed + "."


def _normalize_verbosity(value: str) -> str:
    """Return a supported verbosity value."""
    normalized = str(value or "").strip().lower()
    if normalized in {"concise", "balanced", "detailed"}:
        return normalized
    return "concise"
