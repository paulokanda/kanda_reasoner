# project-path: kanda_reasoner_app/manage_architecture/ai_review/heuristic.py
"""Deterministic advisory summary for Audit Project output."""

from __future__ import annotations

import re
from collections import Counter

from .formatter import format_advisory_review_text
from .models import HEURISTIC_MODE, Tab1AIReviewRequest, Tab1AIReviewResult
from .review_message_builder import limit_audit_text, mark_project_root

__all__ = ["review_audit_with_heuristic"]

_FINDING_PREFIXES = ("ERROR", "FAIL", "WARNING", "SKIP", "PASS")
_PATH_PATTERN = re.compile(r"(?P<path>[A-Za-z0-9_.-]+(?:[/\\][A-Za-z0-9_.-]+)+\.py)")


def _finding_lines(text: str) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        upper = line.upper()
        for prefix in _FINDING_PREFIXES:
            if upper.startswith(prefix + " ") or upper.startswith(prefix + ":"):
                findings.append((prefix, line))
                break
    return findings


def _suggested_files(text: str) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for match in _PATH_PATTERN.finditer(text):
        path = match.group("path").replace("\\", "/")
        if path in seen:
            continue
        seen.add(path)
        output.append(path)
        if len(output) >= 8:
            break
    return output


def review_audit_with_heuristic(request: Tab1AIReviewRequest) -> Tab1AIReviewResult:
    """Return a deterministic, read-only summary of current audit text."""
    if not request.audit_text.strip():
        return Tab1AIReviewResult(
            False,
            "",
            error_message="No Project Audit Results are available.",
            provider_mode=HEURISTIC_MODE,
            request_id=request.request_id,
        )

    marked = mark_project_root(request.audit_text, request.project_root)
    bounded, truncated = limit_audit_text(marked, request.max_audit_chars)
    findings = _finding_lines(bounded)
    counts = Counter(prefix for prefix, _line in findings)
    highest = [line for prefix, line in findings if prefix in {"ERROR", "FAIL"}]
    highest.extend(line for prefix, line in findings if prefix == "WARNING")
    highest = highest[:10]
    files = _suggested_files(bounded)

    summary = (
        "Finding counts: "
        + ", ".join(
            prefix + "=" + str(counts.get(prefix, 0))
            for prefix in _FINDING_PREFIXES
        )
        + "."
    )
    lines = ["1. Advisory summary", summary]
    if truncated:
        lines.append("The supplied audit text was bounded for review.")
    lines.extend(["", "2. Highest risks first"])
    lines.extend("- " + item for item in highest)
    if not highest:
        lines.append("- No ERROR, FAIL, or WARNING finding lines were detected.")
    lines.extend(["", "3. Suggested next inspection files"])
    lines.extend("- " + path for path in files)
    if not files:
        lines.append("- No Python file path was extracted from the current output.")
    lines.extend(
        [
            "",
            "4. Safest next actions",
            "- Resolve deterministic ERROR and FAIL findings before advisory cleanup.",
            "- Re-run the same deterministic audit after each bounded correction.",
            "- Keep write and freeze actions behind their existing human gates.",
            "",
            "5. What deterministic validation still decides",
            "- Pass/fail status, architecture errors, source-write eligibility, and Freeze readiness.",
        ]
    )
    return Tab1AIReviewResult(
        True,
        format_advisory_review_text("\n".join(lines), "Heuristic"),
        model_name="Heuristic",
        provider_mode=HEURISTIC_MODE,
        request_id=request.request_id,
    )
