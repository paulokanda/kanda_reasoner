# project-path: kanda_reasoner_app/reasoner_context_collector/collector_docstrings.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import re


def _clean_lines(docstring: str) -> list[str]:
    """Support clean lines behavior.
    
    Parameters
    ----------
    docstring : str
        The docstring value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    lines = []
    for raw_line in (docstring or "").splitlines():
        line = raw_line.strip()
        if line:
            lines.append(line)
    return lines


def _extract_first_sentence(text: str) -> str:
    """Support extract first sentence behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = " ".join((text or "").split())
    if not text:
        return ""
    match = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)
    return match[0].strip() if match else text.strip()


def _extract_prefixed_values(lines: list[str], prefixes: list[str]) -> list[str]:
    """Support extract prefixed values behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    prefixes : list[str]
        The prefixes value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    found: list[str] = []

    for line in lines:
        lowered = line.lower()
        for prefix in prefixes:
            if lowered.startswith(prefix):
                value = line[len(prefix):].strip(" :-")
                if value:
                    found.append(value)
                break

    return found


def _extract_param_lines(lines: list[str]) -> list[dict]:
    """Support extract param lines behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    
    Returns
    -------
    list[dict]
        The list of values.
    """
    
    params: list[dict] = []

    param_patterns = [
        re.compile(r"^@param\s+(?P<name>[A-Za-z0-9_]+)\s*[:\-]?\s*(?P<desc>.*)$", re.IGNORECASE),
        re.compile(r"^:param\s+(?P<name>[A-Za-z0-9_]+)\s*:\s*(?P<desc>.*)$", re.IGNORECASE),
        re.compile(r"^param\s+(?P<name>[A-Za-z0-9_]+)\s*[:\-]?\s*(?P<desc>.*)$", re.IGNORECASE),
    ]

    for line in lines:
        for pattern in param_patterns:
            match = pattern.match(line)
            if match:
                params.append(
                    {
                        "name": match.group("name").strip(),
                        "description": match.group("desc").strip(),
                    }
                )
                break

    return params


def _extract_return_lines(lines: list[str]) -> list[str]:
    """Support extract return lines behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    prefixes = [
        "@return",
        ":return:",
        "returns",
        "return",
    ]
    return _extract_prefixed_values(lines, prefixes)


def _extract_side_effect_lines(lines: list[str]) -> list[str]:
    """Support extract side effect lines behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    prefixes = [
        "side effects",
        "side effect",
    ]
    return _extract_prefixed_values(lines, prefixes)


def build_docstring_summary(docstring: str) -> dict:
    """Build a docstring summary.
    
    Parameters
    ----------
    docstring : str
        The docstring value.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    lines = _clean_lines(docstring)
    joined = " ".join(lines)

    return {
        "summary": _extract_first_sentence(joined),
        "params": _extract_param_lines(lines),
        "returns": _extract_return_lines(lines),
        "side_effects": _extract_side_effect_lines(lines),
    }
