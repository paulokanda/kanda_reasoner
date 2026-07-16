"""Shared schemas for Project Symbol Atlas reports."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

PROJECT_ATLAS_VALID_REPORT_TYPES = (
    "reasoner_symbol_atlas",
    "symbol_query_result",
    "owner_map",
    "facade_map",
    "test_protection_map",
)

PROJECT_ATLAS_VALID_SYMBOL_KINDS = (
    "module",
    "function",
    "class",
    "dataclass",
    "constant",
    "import",
    "unknown",
)

PROJECT_ATLAS_VALID_OWNER_ROLES = (
    "canonical_owner",
    "facade",
    "compatibility_facade",
    "private_helper",
    "test_only",
    "generated_or_stale",
    "ambiguous_owner",
    "unknown",
)

PROJECT_ATLAS_DEFAULT_REPORT_TYPE = "reasoner_symbol_atlas"
PROJECT_ATLAS_DEFAULT_OWNER_ROLE = "unknown"
PROJECT_ATLAS_DEFAULT_SYMBOL_KIND = "unknown"

__all__ = [
    "PROJECT_ATLAS_DEFAULT_OWNER_ROLE",
    "PROJECT_ATLAS_DEFAULT_REPORT_TYPE",
    "PROJECT_ATLAS_DEFAULT_SYMBOL_KIND",
    "PROJECT_ATLAS_VALID_OWNER_ROLES",
    "PROJECT_ATLAS_VALID_REPORT_TYPES",
    "PROJECT_ATLAS_VALID_SYMBOL_KINDS",
    "ProjectAtlasWriteResult",
    "ProjectModuleRecord",
    "ProjectSymbol",
    "ProjectSymbolAtlasReport",
    "ProjectSymbolQuery",
    "ProjectSymbolQueryResult",
    "make_project_atlas_report_id",
    "make_project_atlas_timestamp",
    "normalize_project_atlas_owner_role",
    "normalize_project_atlas_report_type",
    "normalize_project_atlas_sequence",
    "normalize_project_atlas_symbol_kind",
    "normalize_project_atlas_text",
]


def make_project_atlas_timestamp() -> str:
    """Return an ISO 8601 UTC timestamp for atlas metadata."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_project_atlas_report_id(report_type: str) -> str:
    """Create a stable human-readable report identifier."""
    safe_type = normalize_project_atlas_report_type(report_type)
    return safe_type + "_" + uuid4().hex[:12]


def normalize_project_atlas_report_type(report_type: str | None) -> str:
    """Normalize and validate a Project Symbol Atlas report type."""
    normalized = normalize_project_atlas_text(
        report_type or PROJECT_ATLAS_DEFAULT_REPORT_TYPE
    ).lower()
    if normalized not in PROJECT_ATLAS_VALID_REPORT_TYPES:
        raise ValueError("Unsupported project atlas report type: " + str(report_type))
    return normalized


def normalize_project_atlas_symbol_kind(kind: str | None) -> str:
    """Normalize and validate a Project Symbol Atlas symbol kind."""
    normalized = normalize_project_atlas_text(
        kind or PROJECT_ATLAS_DEFAULT_SYMBOL_KIND
    ).lower()
    if normalized not in PROJECT_ATLAS_VALID_SYMBOL_KINDS:
        raise ValueError("Unsupported project atlas symbol kind: " + str(kind))
    return normalized


def normalize_project_atlas_owner_role(role: str | None) -> str:
    """Normalize and validate a Project Symbol Atlas owner role."""
    normalized = normalize_project_atlas_text(
        role or PROJECT_ATLAS_DEFAULT_OWNER_ROLE
    ).lower()
    if normalized not in PROJECT_ATLAS_VALID_OWNER_ROLES:
        raise ValueError("Unsupported project atlas owner role: " + str(role))
    return normalized


def normalize_project_atlas_text(value: object) -> str:
    """Return a clean string for atlas fields."""
    return " ".join(str(value or "").strip().split())


def normalize_project_atlas_sequence(values: object) -> list[str]:
    """Return a clean string list from a scalar or iterable value."""
    if values is None:
        return []
    if isinstance(values, (str, Path)):
        cleaned = normalize_project_atlas_text(values)
        return [cleaned] if cleaned else []
    if isinstance(values, Iterable):
        result: list[str] = []
        for value in values:
            cleaned = normalize_project_atlas_text(value)
            if cleaned:
                result.append(cleaned)
        return result
    cleaned = normalize_project_atlas_text(values)
    return [cleaned] if cleaned else []


@dataclass(frozen=True)
class ProjectSymbol:
    """One indexed symbol in a project source file."""

    name: str
    kind: str = PROJECT_ATLAS_DEFAULT_SYMBOL_KIND
    module: str = ""
    path: str = ""
    line: int | None = None
    is_public: bool = True
    owner_role: str = PROJECT_ATLAS_DEFAULT_OWNER_ROLE
    exported_by_all: bool = False
    evidence: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible symbol dictionary."""
        return {
            "name": normalize_project_atlas_text(self.name),
            "kind": normalize_project_atlas_symbol_kind(self.kind),
            "module": normalize_project_atlas_text(self.module),
            "path": str(Path(self.path)) if self.path else "",
            "line": self.line,
            "is_public": bool(self.is_public),
            "owner_role": normalize_project_atlas_owner_role(self.owner_role),
            "exported_by_all": bool(self.exported_by_all),
            "evidence": normalize_project_atlas_sequence(self.evidence),
        }


@dataclass(frozen=True)
class ProjectModuleRecord:
    """One source module entry in the symbol atlas."""

    module: str
    path: str
    line_count: int = 0
    is_package_init: bool = False
    is_test_file: bool = False
    owner_role: str = PROJECT_ATLAS_DEFAULT_OWNER_ROLE
    symbols: tuple[ProjectSymbol, ...] = field(default_factory=tuple)
    imports: tuple[str, ...] = field(default_factory=tuple)
    evidence: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible module dictionary."""
        return {
            "module": normalize_project_atlas_text(self.module),
            "path": str(Path(self.path)),
            "line_count": int(self.line_count),
            "is_package_init": bool(self.is_package_init),
            "is_test_file": bool(self.is_test_file),
            "owner_role": normalize_project_atlas_owner_role(self.owner_role),
            "symbol_count": len(self.symbols),
            "symbols": [symbol.to_dict() for symbol in self.symbols],
            "imports": normalize_project_atlas_sequence(self.imports),
            "evidence": normalize_project_atlas_sequence(self.evidence),
        }


@dataclass(frozen=True)
class ProjectSymbolQuery:
    """Input for a future existing-code query."""

    project_root: str
    name: str
    exact: bool = True
    include_private: bool = False
    path_hint: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible query dictionary."""
        return {
            "project_root": str(Path(self.project_root)),
            "name": normalize_project_atlas_text(self.name),
            "exact": bool(self.exact),
            "include_private": bool(self.include_private),
            "path_hint": normalize_project_atlas_text(self.path_hint),
        }


@dataclass(frozen=True)
class ProjectSymbolQueryResult:
    """Result for a future existing-code query."""

    query: ProjectSymbolQuery
    matches: tuple[ProjectSymbol, ...] = field(default_factory=tuple)
    summary: str = ""
    status: str = "not_run"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible query-result dictionary."""
        return {
            "query": self.query.to_dict(),
            "status": normalize_project_atlas_text(self.status) or "not_run",
            "summary": normalize_project_atlas_text(self.summary),
            "match_count": len(self.matches),
            "matches": [match.to_dict() for match in self.matches],
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasReport:
    """Structured Project Symbol Atlas report."""

    project_root: str
    report_type: str = PROJECT_ATLAS_DEFAULT_REPORT_TYPE
    report_id: str = ""
    created_at: str = ""
    summary: str = ""
    modules: tuple[ProjectModuleRecord, ...] = field(default_factory=tuple)
    symbols: tuple[ProjectSymbol, ...] = field(default_factory=tuple)
    query_results: tuple[ProjectSymbolQueryResult, ...] = field(default_factory=tuple)
    input_sources: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible atlas report dictionary."""
        report_type = normalize_project_atlas_report_type(self.report_type)
        created_at = self.created_at or make_project_atlas_timestamp()
        report_id = self.report_id or make_project_atlas_report_id(report_type)
        module_payloads = [module.to_dict() for module in self.modules]
        symbol_payloads = [symbol.to_dict() for symbol in self.symbols]
        query_payloads = [result.to_dict() for result in self.query_results]
        return {
            "report_id": report_id,
            "report_type": report_type,
            "created_at": created_at,
            "project_root": str(Path(self.project_root)),
            "summary": normalize_project_atlas_text(self.summary),
            "input_sources": normalize_project_atlas_sequence(self.input_sources),
            "module_count": len(module_payloads),
            "symbol_count": len(symbol_payloads),
            "query_result_count": len(query_payloads),
            "modules": module_payloads,
            "symbols": symbol_payloads,
            "query_results": query_payloads,
        }


@dataclass(frozen=True)
class ProjectAtlasWriteResult:
    """Paths written for a Project Symbol Atlas report."""

    json_path: Path
    markdown_path: Path

    def to_dict(self) -> dict[str, str]:
        """Return written report paths as strings."""
        return {
            "json_path": str(self.json_path),
            "markdown_path": str(self.markdown_path),
        }
