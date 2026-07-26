# project-path: kanda_reasoner_app/error_memory/fingerprint.py
"""Conservative Error Memory fingerprint extraction."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .scrubber import scrub_text

__all__ = ["extract_exception_info", "build_fingerprint"]

_ERROR_TYPE_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Warning))\b(?::\s*(.*))?")
_FILE_RE = re.compile(r'File "([^"]+)", line \d+, in ([A-Za-z_][A-Za-z0-9_]*)')
_PYTEST_TEST_RE = re.compile(r"\b(test_[A-Za-z0-9_]+)\b")
_LINE_NUMBER_RE = re.compile(r"\bline\s+\d+\b", re.IGNORECASE)
_TEMP_RE = re.compile(r"\b(tmp|temp)[-_]?[A-Za-z0-9]{4,}\b", re.IGNORECASE)


def _relative_path(candidate: str, selected_project_root: str | Path | None) -> str:
    """Support relative path behavior.
    
    Parameters
    ----------
    candidate : str
        The candidate value.
    selected_project_root : str | Path | None
        The selected project root value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = str(candidate or "").replace("/", "\\")
    if not text:
        return ""
    if selected_project_root is None:
        return Path(text).name if (":" in text or text.startswith("\\")) else text
    try:
        root = Path(selected_project_root).expanduser().resolve(strict=False)
        path = Path(text).expanduser().resolve(strict=False)
        return str(path.relative_to(root)).replace("/", "\\")
    except Exception:
        parts = [part for part in text.split("\\") if part]
        for marker in ("kanda_reasoner_app", "tests", "validation", "scripts"):
            if marker in parts:
                return "\\".join(parts[parts.index(marker):])
        return Path(text).name


def _normalize_message(message: str) -> str:
    """Support normalize message behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = scrub_text(message).text.strip().lower()
    text = _LINE_NUMBER_RE.sub("line <N>", text)
    text = _TEMP_RE.sub("<TEMP>", text)
    text = re.sub(r"\s+", " ", text)
    return text[:240]


def extract_exception_info(
    raw_text: object,
    *,
    selected_project_root: str | Path | None = None,
    operation_phase: str = "unknown",
) -> dict[str, Any]:
    """Extract stable exception fields from terminal, validation, or traceback text."""
    text = str(raw_text or "")
    scrubbed = scrub_text(text).text
    error_type = ""
    message = ""
    for line in reversed([item.strip() for item in scrubbed.splitlines() if item.strip()]):
        match = _ERROR_TYPE_RE.search(line)
        if match:
            error_type = match.group(1)
            message = match.group(2) or ""
            if not message:
                before, _sep, after = line.partition(error_type)
                candidate = after.strip(" :-\u2014\u2013.") or before.strip(" :-\u2014\u2013.") or line.strip()
                message = candidate
            break
    relative_file = ""
    function_or_test = ""
    for match in _FILE_RE.finditer(scrubbed):
        relative_file = _relative_path(match.group(1), selected_project_root)
        function_or_test = match.group(2)
    test_match = _PYTEST_TEST_RE.search(scrubbed)
    if test_match:
        function_or_test = test_match.group(1)
    return {
        "type": error_type,
        "message_normalized": _normalize_message(message),
        "phase": str(operation_phase or "unknown"),
        "relative_file_path": relative_file,
        "function_or_test_name": function_or_test,
        "stacktrace_scrubbed": scrubbed[:4000],
    }


def build_fingerprint(exception_info: dict[str, Any]) -> dict[str, Any]:
    """Return a stable structural fingerprint for one exception info object."""
    components = [
        str(exception_info.get("type", "") or ""),
        str(exception_info.get("relative_file_path", "") or ""),
        str(exception_info.get("function_or_test_name", "") or ""),
        str(exception_info.get("phase", "") or ""),
        str(exception_info.get("message_normalized", "") or ""),
    ]
    joined = "\x1f".join(components)
    return {
        "strategy": "v1_structural_conservative",
        "components": components,
        "fingerprint_hash": hashlib.sha256(joined.encode("utf-8")).hexdigest(),
    }
