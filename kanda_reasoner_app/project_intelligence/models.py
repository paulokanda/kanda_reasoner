# project-path: kanda_reasoner_app/project_intelligence/models.py
"""Shared data models for deterministic Project Intelligence engines."""

from __future__ import annotations


__all__ = ['EngineFinding', 'EngineReport', 'FileSymbolSummary', 'ImportRecord', 'SymbolRecord']
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ADVISORY_SOURCE_TRUTH_WARNING = (
    "This generated report is advisory evidence. It is not canonical source. "
    "Exact source files must be inspected before editing."
)

VALID_SEVERITIES = ("info", "advisory", "warning", "high", "critical")
VALID_STATUSES = (
    "ok",
    "completed_with_findings",
    "completed_with_warnings",
    "failed_gracefully",
    "blocked",
)


def _clean_text(value: object) -> str:
    """Return a compact string safe for JSON report fields."""
    return " ".join(str(value or "").strip().split())


def _normalize_path(value: object) -> str:
    """Return a stable slash-separated relative path string."""
    text = str(value or "").strip()
    if not text:
        return ""
    return Path(text).as_posix()


def _clean_list(values: object) -> list[str]:
    """Return a JSON-safe list of non-empty strings."""
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    try:
        iterator = iter(values)  # type: ignore[arg-type]
    except TypeError:
        iterator = iter([values])
    output: list[str] = []
    for value in iterator:
        text = _clean_text(value)
        if text:
            output.append(text)
    return output


@dataclass(frozen=True)
class EngineFinding:
    """One advisory finding produced by a Project Intelligence engine."""

    finding_id: str
    severity: str
    category: str
    title: str
    message: str
    file_path: str
    line_number: int
    evidence: str
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible finding dictionary."""
        severity = _clean_text(self.severity).lower() or "info"
        if severity not in VALID_SEVERITIES:
            severity = "info"
        return {
            "finding_id": _clean_text(self.finding_id),
            "severity": severity,
            "category": _clean_text(self.category),
            "title": _clean_text(self.title),
            "message": _clean_text(self.message),
            "file_path": _normalize_path(self.file_path),
            "line_number": int(self.line_number or 0),
            "evidence": _clean_text(self.evidence),
            "recommendation": _clean_text(self.recommendation),
        }


@dataclass(frozen=True)
class EngineReport:
    """Standard advisory report returned by every intelligence engine."""

    engine_id: str
    engine_version: str
    status: str
    generated_at: str
    project_root_label: str
    summary: str
    findings: list[EngineFinding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    ai_must_not_assume: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible engine report dictionary."""
        status = _clean_text(self.status).lower() or "ok"
        if status not in VALID_STATUSES:
            status = "ok"
        ai_limits = _clean_list(self.ai_must_not_assume)
        if ADVISORY_SOURCE_TRUTH_WARNING not in ai_limits:
            ai_limits.insert(0, ADVISORY_SOURCE_TRUTH_WARNING)
        return {
            "engine_id": _clean_text(self.engine_id),
            "engine_version": _clean_text(self.engine_version),
            "status": status,
            "generated_at": _clean_text(self.generated_at),
            "project_root_label": _clean_text(self.project_root_label),
            "summary": _clean_text(self.summary),
            "findings": [finding.to_dict() for finding in self.findings],
            "warnings": _clean_list(self.warnings),
            "errors": _clean_list(self.errors),
            "next_steps": _clean_list(self.next_steps),
            "ai_must_not_assume": ai_limits,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class SymbolRecord:
    """One discovered Python symbol in a scanned project file."""

    name: str
    symbol_type: str
    file_path: str
    line_number: int
    end_line_number: int
    parent_name: str
    has_docstring: bool
    is_async: bool

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible symbol dictionary."""
        return {
            "name": _clean_text(self.name),
            "symbol_type": _clean_text(self.symbol_type),
            "file_path": _normalize_path(self.file_path),
            "line_number": int(self.line_number or 0),
            "end_line_number": int(self.end_line_number or 0),
            "parent_name": _clean_text(self.parent_name),
            "has_docstring": bool(self.has_docstring),
            "is_async": bool(self.is_async),
        }


@dataclass(frozen=True)
class ImportRecord:
    """One import statement discovered in a scanned project file."""

    module: str
    imported_name: str
    import_type: str
    file_path: str
    line_number: int

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible import dictionary."""
        return {
            "module": _clean_text(self.module),
            "imported_name": _clean_text(self.imported_name),
            "import_type": _clean_text(self.import_type),
            "file_path": _normalize_path(self.file_path),
            "line_number": int(self.line_number or 0),
        }


@dataclass(frozen=True)
class FileSymbolSummary:
    """Per-file scan counts and syntax status."""

    file_path: str
    function_count: int
    class_count: int
    method_count: int
    import_count: int
    syntax_error: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible per-file summary dictionary."""
        return {
            "file_path": _normalize_path(self.file_path),
            "function_count": int(self.function_count or 0),
            "class_count": int(self.class_count or 0),
            "method_count": int(self.method_count or 0),
            "import_count": int(self.import_count or 0),
            "syntax_error": _clean_text(self.syntax_error),
        }
