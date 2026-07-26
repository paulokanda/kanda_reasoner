# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_documentation_intent_extractors.py
"""Text extraction helpers for documentation intent parsing."""

from __future__ import annotations

import re

from ._documentation_intent_result_helpers import _dedupe_keep_order, _truncate_text

__all__: list[str] = []


def _extract_heading_lines(text: str) -> list[str]:
    """Support extract heading lines behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    headings: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            headings.append(line.lstrip("#").strip())
            continue
        if re.match(r"^[A-Za-z0-9][A-Za-z0-9\s\-_]{2,}$", line):
            headings.append(line)
    return _dedupe_keep_order(headings)


def _extract_run_instructions(text: str) -> list[str]:
    """Support extract run instructions behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    matches: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        lowered = line.lower()
        if not line:
            continue
        if (
            "python " in lowered
            or "pip install" in lowered
            or "pytest" in lowered
            or "uv run" in lowered
            or "poetry run" in lowered
            or "streamlit run" in lowered
            or "flask run" in lowered
            or "uvicorn " in lowered
        ):
            matches.append(line)
    return _dedupe_keep_order(matches)


def _extract_named_features(headings: list[str]) -> list[str]:
    """Support extract named features behavior.
    
    Parameters
    ----------
    headings : list[str]
        The headings value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    features: list[str] = []
    for heading in headings:
        lowered = heading.lower()
        if any(
            keyword in lowered
            for keyword in (
                "feature",
                "capability",
                "workflow",
                "pipeline",
                "module",
                "architecture",
                "overview",
                "system",
            )
        ):
            features.append(heading)
    return _dedupe_keep_order(features)


def _extract_external_integrations(text: str) -> list[str]:
    """Support extract external integrations behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    integrations: list[str] = []
    patterns = (
        "openai",
        "anthropic",
        "ollama",
        "postgres",
        "sqlite",
        "redis",
        "mongodb",
        "docker",
        "fastapi",
        "flask",
        "django",
        "pyside",
        "pyqt",
        "slack",
        "github",
        "gitlab",
        "s3",
        "azure",
        "gcp",
    )
    lowered = text.lower()
    for item in patterns:
        if item in lowered:
            integrations.append(item)
    return _dedupe_keep_order(integrations)


def _extract_architecture_terms(headings: list[str], text: str) -> list[str]:
    """Support extract architecture terms behavior.
    
    Parameters
    ----------
    headings : list[str]
        The headings value.
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    candidates = list(headings)
    patterns = re.findall(
        r"\b(controller|service|manager|builder|registry|router|pipeline|adapter|bridge|collector|parser|orchestrator|plugin|engine|loader)\b",
        text,
        flags=re.IGNORECASE,
    )
    candidates.extend(patterns)
    return _dedupe_keep_order(candidates)


def _extract_first_meaningful_paragraph(text: str) -> str:
    """Support extract first meaningful paragraph behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    disallowed_starts = (
        "#",
        "##",
        "###",
        "ai analysis summary",
        "analysis summary",
        "summary",
    )
    blocks = re.split(r"\n\s*\n", text)
    for block in blocks:
        cleaned_lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not cleaned_lines:
            continue
        cleaned = " ".join(cleaned_lines).strip()
        lowered = cleaned.lower()
        if len(cleaned) < 40:
            continue
        if any(lowered.startswith(prefix) for prefix in disallowed_starts):
            continue
        if any(
            marker in lowered
            for marker in (
                "**original file:**",
                "original file:",
                "**created:**",
                "created:",
                "**source file:**",
                "source file:",
                "**generated:**",
                "generated:",
                "last updated:",
                "auto-generated",
                "autogenerated",
            )
        ):
            continue
        if cleaned.startswith("#"):
            continue
        sentence_like = (
            "." in cleaned
            or " is " in lowered
            or " are " in lowered
            or " provides " in lowered
            or " application " in lowered
            or " project " in lowered
            or " tool " in lowered
            or " system " in lowered
        )
        if not sentence_like:
            continue
        return cleaned
    return ""
