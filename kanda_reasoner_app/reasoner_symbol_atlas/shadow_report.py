# project-path: kanda_reasoner_app/reasoner_symbol_atlas/shadow_report.py
"""Read-only duplicate public symbol reports for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .owner_classifier import (
    ProjectSymbolAtlasOwnerClassifyOptions,
    classify_reasoner_symbol_atlas_owners,
)
from .schemas import ProjectModuleRecord, ProjectSymbol, ProjectSymbolAtlasReport

__all__ = [
    "ProjectSymbolAtlasShadowReportOptions",
    "build_reasoner_symbol_atlas_shadow_report",
    "collect_reasoner_symbol_atlas_shadow_findings",
]

_IGNORED_OWNER_ROLES = frozenset({"test_only", "generated_or_stale", "private_helper"})
_DEFINITION_KINDS = frozenset({"function", "class", "dataclass", "constant"})


@dataclass(frozen=True)
class ProjectSymbolAtlasShadowReportOptions:
    """Options for read-only duplicate public symbol reports."""

    include_tests: bool = False
    include_workbench: bool = False
    include_facades: bool = True
    include_import_symbols: bool = True
    include_constants: bool = True
    include_private: bool = False
    include_private_reexports: bool = False
    include_wildcard_symbols: bool = False

    def to_owner_options(self) -> ProjectSymbolAtlasOwnerClassifyOptions:
        """Return compatible owner-classifier options."""
        return ProjectSymbolAtlasOwnerClassifyOptions(
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
            include_constants=self.include_constants,
            include_private_reexports=self.include_private_reexports,
            include_wildcard_symbols=self.include_wildcard_symbols,
        )


def _coerce_project_root(project_root: str | Path) -> Path:
    """Support coerce project root behavior.
    
    Parameters
    ----------
    project_root : str | Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    root = Path(project_root).resolve()
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _is_public_candidate(
    symbol: ProjectSymbol,
    record: ProjectModuleRecord,
    options: ProjectSymbolAtlasShadowReportOptions,
) -> bool:
    """Support is public candidate behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    record : ProjectModuleRecord
        The record value.
    options : ProjectSymbolAtlasShadowReportOptions
        The option values.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not symbol.is_public or symbol.name.startswith("_"):
        return False
    if record.owner_role in _IGNORED_OWNER_ROLES:
        return False
    if symbol.owner_role in _IGNORED_OWNER_ROLES:
        return False
    if not options.include_facades and symbol.owner_role in {"facade", "compatibility_facade"}:
        return False
    if symbol.kind == "import" and not options.include_import_symbols:
        return False
    if symbol.kind == "constant" and not options.include_constants:
        return False
    return symbol.kind in _DEFINITION_KINDS or symbol.kind == "import"


def _symbol_key(symbol: ProjectSymbol) -> str:
    """Support symbol key behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return symbol.name.strip()


def _format_symbol_location(symbol: ProjectSymbol) -> str:
    """Support format symbol location behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    
    Returns
    -------
    str
        The string result.
    """
    
    line_text = str(symbol.line) if symbol.line is not None else "unknown"
    return (
        symbol.module
        + " | "
        + symbol.path
        + ":"
        + line_text
        + " | kind="
        + symbol.kind
        + " | role="
        + symbol.owner_role
    )


def _duplicate_reason(symbols: tuple[ProjectSymbol, ...]) -> str:
    """Support duplicate reason behavior.
    
    Parameters
    ----------
    symbols : tuple[ProjectSymbol, ...]
        The symbols value.
    
    Returns
    -------
    str
        The string result.
    """
    
    canonical_count = sum(1 for item in symbols if item.owner_role == "canonical_owner")
    facade_count = sum(1 for item in symbols if item.owner_role in {"facade", "compatibility_facade"})
    definition_count = sum(1 for item in symbols if item.kind in _DEFINITION_KINDS)
    if canonical_count > 1:
        return "duplicate_canonical_public_owner"
    if definition_count > 1:
        return "duplicate_public_definition"
    if canonical_count == 1 and facade_count > 0:
        return "canonical_owner_with_facade_reexport"
    if facade_count > 1:
        return "multiple_facade_reexports"
    return "duplicate_public_symbol"


def _finding_from_duplicate(name: str, symbols: tuple[ProjectSymbol, ...]) -> ProjectSymbol:
    """Support finding from duplicate behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    symbols : tuple[ProjectSymbol, ...]
        The symbols value.
    
    Returns
    -------
    ProjectSymbol
        The project symbol result.
    """
    
    locations = tuple(_format_symbol_location(symbol) for symbol in symbols)
    reason = _duplicate_reason(symbols)
    evidence = (
        "shadow_report: read_only",
        "duplicate_reason: " + reason,
        "duplicate_public_symbol_count: " + str(len(symbols)),
    ) + tuple("location: " + location for location in locations)
    return ProjectSymbol(
        name=name,
        kind="unknown",
        module="multiple_modules",
        path="",
        line=None,
        is_public=True,
        owner_role="ambiguous_owner",
        exported_by_all=False,
        evidence=evidence,
    )


def _involved_records(
    records: tuple[ProjectModuleRecord, ...],
    findings: tuple[ProjectSymbol, ...],
) -> tuple[ProjectModuleRecord, ...]:
    """Support involved records behavior.
    
    Parameters
    ----------
    records : tuple[ProjectModuleRecord, ...]
        The record values.
    findings : tuple[ProjectSymbol, ...]
        The findings value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    involved_paths: set[str] = set()
    for finding in findings:
        for item in finding.evidence:
            if not item.startswith("location: "):
                continue
            parts = item.removeprefix("location: ").split(" | ")
            if len(parts) >= 2:
                involved_paths.add(parts[1].split(":", 1)[0])
    selected = [record for record in records if record.path in involved_paths]
    selected.sort(key=lambda record: (record.path, record.module))
    return tuple(selected)


def collect_reasoner_symbol_atlas_shadow_findings(
    project_root: str | Path,
    options: ProjectSymbolAtlasShadowReportOptions | None = None,
) -> tuple[ProjectSymbol, ...]:
    """Collect duplicate public symbol findings without editing source."""
    root = _coerce_project_root(project_root)
    report_options = options or ProjectSymbolAtlasShadowReportOptions()
    records = classify_reasoner_symbol_atlas_owners(
        root,
        options=report_options.to_owner_options(),
    )
    grouped: dict[str, list[ProjectSymbol]] = {}
    for record in records:
        for symbol in record.symbols:
            if _is_public_candidate(symbol, record, report_options):
                grouped.setdefault(_symbol_key(symbol), []).append(symbol)
    findings: list[ProjectSymbol] = []
    for name, symbols in grouped.items():
        unique_locations = tuple(
            sorted(
                symbols,
                key=lambda item: (item.module, item.path, item.line or 0, item.kind),
            )
        )
        location_keys = {
            (item.module, item.path, item.line, item.kind, item.owner_role)
            for item in unique_locations
        }
        if len(location_keys) > 1:
            findings.append(_finding_from_duplicate(name, unique_locations))
    findings.sort(key=lambda item: (item.name.lower(), item.module, item.path))
    return tuple(findings)


def build_reasoner_symbol_atlas_shadow_report(
    project_root: str | Path,
    options: ProjectSymbolAtlasShadowReportOptions | None = None,
) -> ProjectSymbolAtlasReport:
    """Build a read-only duplicate public symbol report."""
    root = _coerce_project_root(project_root)
    report_options = options or ProjectSymbolAtlasShadowReportOptions()
    records = classify_reasoner_symbol_atlas_owners(
        root,
        options=report_options.to_owner_options(),
    )
    findings = collect_reasoner_symbol_atlas_shadow_findings(root, options=report_options)
    involved = _involved_records(records, findings)
    summary = (
        "Duplicate public symbol scan completed. "
        + "findings="
        + str(len(findings))
        + "; involved_modules="
        + str(len(involved))
        + "."
    )
    return ProjectSymbolAtlasReport(
        project_root=str(root),
        report_type="reasoner_symbol_atlas",
        summary=summary,
        modules=involved,
        symbols=findings,
        input_sources=(
            "module_scanner",
            "symbol_indexer",
            "import_analyzer",
            "owner_classifier",
            "shadow_report",
        ),
    )
