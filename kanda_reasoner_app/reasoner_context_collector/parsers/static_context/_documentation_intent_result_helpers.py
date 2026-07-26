# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_documentation_intent_result_helpers.py
"""Result assembly helpers for documentation intent parsing."""

from __future__ import annotations

from typing import Any

__all__: list[str] = []


def _truncate_text(value: str, max_chars: int) -> str:
    """Support truncate text behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    max_chars : int
        The max chars value.
    
    Returns
    -------
    str
        The string result.
    """
    
    value = value.strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def _dedupe_keep_order(items: list[str]) -> list[str]:
    """Support dedupe keep order behavior.
    
    Parameters
    ----------
    items : list[str]
        The item values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        cleaned = str(item).strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
    return out


def _new_result() -> dict[str, Any]:
    """Support new result behavior.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "project_purpose_summary": "",
        "project_purpose_summary_confidence": "unknown",
        "declared_workflows": [],
        "architecture_terms": [],
        "run_instructions": [],
        "named_features": [],
        "external_integrations": [],
        "documentation_files_found": [],
        "documentation_evidence": [],
        "documentation_parse_warnings": [],
    }


def _append_evidence(
    result: dict[str, Any],
    source_file: str,
    field_name: str,
    value: str,
    max_excerpt_chars: int,
) -> None:
    """Support append evidence behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    field_name : str
        The field name value.
    value : str
        The input value.
    max_excerpt_chars : int
        The max excerpt chars value.
    """
    
    result["documentation_evidence"].append(
        {
            "source_file": source_file,
            "field": field_name,
            "value_excerpt": _truncate_text(value, max_excerpt_chars),
        }
    )


def _append_warning(result: dict[str, Any], source_file: str, message: str) -> None:
    """Support append warning behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    message : str
        The message text.
    """
    
    warning = f"{source_file}: {message}" if source_file else message
    result["documentation_parse_warnings"].append(warning)


def _set_if_empty(
    result: dict[str, Any],
    key: str,
    value: str,
    source_file: str,
    max_excerpt_chars: int,
) -> None:
    """Support set if empty behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    key : str
        The key value.
    value : str
        The input value.
    source_file : str
        The source file value.
    max_excerpt_chars : int
        The max excerpt chars value.
    """
    
    cleaned = value.strip()
    if cleaned and not result.get(key):
        result[key] = cleaned
        _append_evidence(result, source_file, key, cleaned, max_excerpt_chars)


def _merge_list_field(
    result: dict[str, Any],
    field_name: str,
    values: list[str],
    source_file: str,
    max_evidence_snippets: int,
    max_excerpt_chars: int,
) -> None:
    """Support merge list field behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    field_name : str
        The field name value.
    values : list[str]
        The input values.
    source_file : str
        The source file value.
    max_evidence_snippets : int
        The max evidence snippets value.
    max_excerpt_chars : int
        The max excerpt chars value.
    """
    
    current = list(result[field_name])
    result[field_name] = _dedupe_keep_order(current + values)
    for value in values[:max_evidence_snippets]:
        _append_evidence(result, source_file, field_name, value, max_excerpt_chars)
