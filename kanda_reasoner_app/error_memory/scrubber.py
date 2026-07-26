# project-path: kanda_reasoner_app/error_memory/scrubber.py
"""Redaction helpers for Error Memory AI exports."""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = ["RedactionResult", "scrub_text"]


@dataclass(frozen=True)
class RedactionResult:
    """Redacted text plus names of rules that changed it."""

    text: str
    rules: tuple[str, ...]


_USER_PATH_RE = re.compile(r"([A-Za-z]:\\Users\\)([^\\\r\n]+)(?=\\)")
_POSIX_USER_PATH_RE = re.compile(r"(/Users/)([^/\r\n]+)(?=/)")
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(api[_-]?key|token|secret|password|passwd|authorization)\s*[:=]\s*[^\s,;]+"
)
_LONG_SECRET_RE = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{8,}|[A-Za-z0-9_/-]{32,})\b")


def _apply_rule(text: str, pattern: re.Pattern[str], replacement: str, rule: str, rules: list[str]) -> str:
    """Support apply rule behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    pattern : re.Pattern[str]
        The pattern value.
    replacement : str
        The replacement value.
    rule : str
        The rule value.
    rules : list[str]
        The rules value.
    
    Returns
    -------
    str
        The string result.
    """
    
    updated = pattern.sub(replacement, text)
    if updated != text and rule not in rules:
        rules.append(rule)
    return updated


def scrub_text(text: object) -> RedactionResult:
    """Return a conservative AI-export-safe redaction of text."""
    value = str(text or "")
    rules: list[str] = []
    value = _USER_PATH_RE.sub(r"\1<USER>", value)
    if "<USER>" in value:
        rules.append("user_paths")
    before = value
    value = _POSIX_USER_PATH_RE.sub(r"\1<USER>", value)
    if value != before and "user_paths" not in rules:
        rules.append("user_paths")
    value = _apply_rule(value, _EMAIL_RE, "<EMAIL>", "emails", rules)
    value = _apply_rule(value, _IP_RE, "<IP>", "ips", rules)

    def _secret_repl(match: re.Match[str]) -> str:
        key = match.group(1)
        separator = ":" if ":" in match.group(0).split(key, 1)[-1][:3] else "="
        return key + separator + "<SECRET>"

    updated = _SECRET_ASSIGNMENT_RE.sub(_secret_repl, value)
    if updated != value:
        rules.append("tokens")
        value = updated
    value = _apply_rule(value, _LONG_SECRET_RE, "<SECRET>", "tokens", rules)
    return RedactionResult(value, tuple(sorted(set(rules))))
