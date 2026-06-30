# project-path: kanda_reasoner_app/reasoner_engine/v10_static_context_evidence_formatter.py
"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from typing import Any


def _clean_list(values: list[Any]) -> list[str]:
    """Support clean list behavior.
    
    Parameters
    ----------
    values : list[Any]
        The input values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return [str(value).strip() for value in values if str(value).strip()]


def _preview_lines(values: list[str], limit: int = 8) -> list[str]:
    """Support preview lines behavior.
    
    Parameters
    ----------
    values : list[str]
        The input values.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    preview = values[:limit]
    if len(values) > limit:
        preview.append(f"... (+{len(values) - limit} more)")
    return preview


def build_static_context_evidence_preview(
    packaging_metadata: dict[str, Any],
    documentation_intent: dict[str, Any],
) -> str:
    """Build a static context evidence preview.
    
    Parameters
    ----------
    packaging_metadata : dict[str, Any]
        The packaging metadata value.
    documentation_intent : dict[str, Any]
        The documentation intent value.
    
    Returns
    -------
    str
        The string result.
    """
    
    packaging_files = _clean_list(packaging_metadata.get("packaging_files_found", []))
    documentation_files = _clean_list(
        documentation_intent.get("documentation_files_found", [])
    )

    packaging_evidence_raw = packaging_metadata.get("packaging_evidence", [])
    documentation_evidence_raw = documentation_intent.get("documentation_evidence", [])

    packaging_evidence: list[str] = []
    for item in packaging_evidence_raw[:8]:
        if not isinstance(item, dict):
            continue
        source_file = str(item.get("source_file", "")).strip()
        field_name = str(item.get("field", "")).strip()
        value_excerpt = str(item.get("value_excerpt", "")).strip()
        if source_file or field_name or value_excerpt:
            packaging_evidence.append(
                f"{source_file} | {field_name} | {value_excerpt}"
            )

    documentation_evidence: list[str] = []
    for item in documentation_evidence_raw[:8]:
        if not isinstance(item, dict):
            continue
        source_file = str(item.get("source_file", "")).strip()
        field_name = str(item.get("field", "")).strip()
        value_excerpt = str(item.get("value_excerpt", "")).strip()
        if source_file or field_name or value_excerpt:
            documentation_evidence.append(
                f"{source_file} | {field_name} | {value_excerpt}"
            )

    lines = [
        "STATIC CONTEXT EVIDENCE PREVIEW",
        "=" * 80,
        "",
        "[PACKAGING FILES]",
    ]

    if packaging_files:
        for line in _preview_lines(packaging_files, limit=12):
            lines.append(line)
    else:
        lines.append("-")

    lines.extend(
        [
            "",
            "[PACKAGING EVIDENCE]",
        ]
    )

    if packaging_evidence:
        for line in _preview_lines(packaging_evidence, limit=8):
            lines.append(line)
    else:
        lines.append("-")

    lines.extend(
        [
            "",
            "[DOCUMENTATION FILES]",
        ]
    )

    if documentation_files:
        for line in _preview_lines(documentation_files, limit=12):
            lines.append(line)
    else:
        lines.append("-")

    lines.extend(
        [
            "",
            "[DOCUMENTATION EVIDENCE]",
        ]
    )

    if documentation_evidence:
        for line in _preview_lines(documentation_evidence, limit=8):
            lines.append(line)
    else:
        lines.append("-")

    return "\n".join(lines)






