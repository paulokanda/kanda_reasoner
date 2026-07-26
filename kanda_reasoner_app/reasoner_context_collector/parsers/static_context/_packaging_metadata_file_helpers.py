# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_packaging_metadata_file_helpers.py
"""File discovery and text parsing helpers for packaging metadata parsing."""

from __future__ import annotations

import re
from pathlib import Path

__all__: list[str] = []


def _looks_nul_padded(text: str) -> bool:
    """Support looks nul padded behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not text:
        return False
    nul_count = text.count("\x00")
    return nul_count > 0 and (nul_count / max(1, len(text))) >= 0.05


def _read_text_best_effort(path: Path) -> tuple[str, list[str]]:
    """Support read text best effort behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    tuple[str, list[str]]
        The tuple of values.
    """
    
    warnings: list[str] = []
    raw = path.read_bytes()
    if not raw:
        return "", warnings
    if b"\x00" in raw:
        for encoding in ("utf-16", "utf-16-le", "utf-16-be"):
            try:
                text = raw.decode(encoding)
                warnings.append(f"decoded with {encoding} after NUL-byte detection")
                return text.replace("\ufeff", ""), warnings
            except Exception:
                continue
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
        warnings.append("decoded with utf-8 replacement")
    if _looks_nul_padded(text):
        warnings.append("removed NUL padding from decoded text")
        text = text.replace("\x00", "")
    return text.replace("\ufeff", ""), warnings


def _clean_dependency_line(line: str) -> str:
    """Support clean dependency line behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    str
        The string result.
    """
    
    cleaned = line.strip().replace("\x00", "")
    if not cleaned:
        return ""
    if " #" in cleaned:
        cleaned = cleaned.split(" #", 1)[0].rstrip()
    if " ;" in cleaned:
        cleaned = cleaned.split(" ;", 1)[0].rstrip()
    if cleaned.lower().startswith("-e "):
        cleaned = cleaned[3:].strip()
    if "@ file://" in cleaned.lower():
        cleaned = cleaned.split("@", 1)[0].strip()
    return cleaned


def _is_suspicious_dependency_line(line: str) -> bool:
    """Support is suspicious dependency line behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not line:
        return True
    lowered = line.lower()
    if "\ufffd" in line or "\x00" in line:
        return True
    if any(token in lowered for token in ("original file:", "source file:", "included fonts", "pytest's cache plugin")):
        return True
    alnum = sum(ch.isalnum() for ch in line)
    return alnum == 0


def _parse_dependency_lines(text: str) -> list[str]:
    """Support parse dependency lines behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    dependencies: list[str] = []
    for raw_line in text.splitlines():
        if "\x00" in raw_line:
            continue
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-r", "--requirement", "--find-links", "-f", "--extra-index-url", "--index-url")):
            continue
        cleaned = _clean_dependency_line(line)
        if not cleaned or _is_suspicious_dependency_line(cleaned):
            continue
        dependencies.append(cleaned)
    return _dedupe_keep_order(dependencies)


def _discover_packaging_files(root, *args, **kwargs):
    """Support discover packaging files behavior.
    
    Parameters
    ----------
    root : object
        The root path.
    *args : object
        The positional arguments.
    **kwargs : object
        The kwargs value.
    """
    
    from kanda_reasoner_app.reasoner_context_collector.collector_scope import iter_project_packaging_files
    return list(iter_project_packaging_files(root))
