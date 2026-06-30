# project-path: kanda_reasoner_app/reasoner_symbol_atlas/complete_json_adapter.py
"""Read-only adapter for generated complete Project Analysis Evidence JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from kanda_reasoner_app.project_analysis_evidence_paths import project_name_from_root

from .evidence_paths import get_reasoner_symbol_atlas_canonical_evidence_dir
from .schemas import (
    ProjectModuleRecord,
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_REQUIRED_SECTIONS = (
    "source_file_index",
    "symbol_index",
    "primary_definition_index",
)

PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_RECOMMENDED_SECTIONS = (
    "duplicate_symbols",
    "canonical_conflict_index",
    "import_graph",
    "web_ai_file_responsibility_index",
    "web_ai_test_protection_index",
    "edit_ready_symbol_index",
    "snippet_index",
    "active_code_index",
    "boundary_index",
    "change_impact_index",
)

PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY = "complete_json_ready"
PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_JSON = "missing_json"
PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_SECTIONS = "missing_sections"
PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_INVALID_JSON = "invalid_json"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_RECOMMENDED_SECTIONS",
    "PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_REQUIRED_SECTIONS",
    "PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_INVALID_JSON",
    "PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_JSON",
    "PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_SECTIONS",
    "PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY",
    "ProjectSymbolAtlasCompleteJsonOptions",
    "ProjectSymbolAtlasCompleteJsonSummary",
    "build_reasoner_symbol_atlas_complete_json_report",
    "expected_reasoner_symbol_atlas_complete_json_name",
    "collect_reasoner_symbol_atlas_complete_json_files",
    "load_reasoner_symbol_atlas_complete_json",
    "summarize_reasoner_symbol_atlas_complete_json",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasCompleteJsonOptions:
    """Options for adapting generated complete JSON evidence."""

    project_root: str
    json_path: str = ""
    max_modules: int = 100
    max_symbols: int = 250
    required_sections: tuple[str, ...] = field(
        default_factory=lambda: PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_REQUIRED_SECTIONS
    )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "max_modules": int(self.max_modules),
            "max_symbols": int(self.max_symbols),
            "required_sections": list(self.required_sections),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasCompleteJsonSummary:
    """Summary of a generated complete JSON evidence file."""

    project_root: str
    json_path: str = ""
    status: str = PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_JSON
    available_sections: tuple[str, ...] = field(default_factory=tuple)
    missing_sections: tuple[str, ...] = field(default_factory=tuple)
    recommended_sections_present: tuple[str, ...] = field(default_factory=tuple)
    source_file_count: int = 0
    symbol_count: int = 0
    primary_definition_count: int = 0
    duplicate_symbol_count: int = 0
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible summary dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "status": normalize_project_atlas_text(self.status),
            "available_sections": list(self.available_sections),
            "missing_sections": list(self.missing_sections),
            "recommended_sections_present": list(self.recommended_sections_present),
            "source_file_count": int(self.source_file_count),
            "symbol_count": int(self.symbol_count),
            "primary_definition_count": int(self.primary_definition_count),
            "duplicate_symbol_count": int(self.duplicate_symbol_count),
            "notes": list(self.notes),
        }


def collect_reasoner_symbol_atlas_complete_json_files(
    project_root: str | Path,
    evidence_dir: str | Path | None = None,
) -> tuple[Path, ...]:
    """Return candidate generated complete JSON evidence files.

    The search is recursive under the canonical evidence directory so it can
    support both flat layouts and the json_complete subfolder created by Tab 4.
    Runtime-trace and split-part JSON files are intentionally excluded. Files
    named with the current project prefix, for example
    ``<project_slug>__complete.json``, are ranked ahead of generic fallback
    matches so Tab 8 reads the active project's evidence when several projects
    have JSON files in the same evidence tree.
    """

    root = Path(evidence_dir) if evidence_dir is not None else (
        get_reasoner_symbol_atlas_canonical_evidence_dir(project_root)
    )
    if not root.is_dir():
        return ()

    expected_name = expected_reasoner_symbol_atlas_complete_json_name(project_root).lower()
    ranked_candidates: list[tuple[int, float, str, Path]] = []
    for path in root.rglob("*.json"):
        name = path.name.lower()
        if "runtime_trace" in name:
            continue
        if "split" in path.as_posix().lower() or "json_splitted" in path.as_posix().lower():
            continue
        rank = _complete_json_name_rank(name, expected_name)
        if rank is None:
            continue
        try:
            modified = path.stat().st_mtime
        except OSError:
            modified = 0.0
        ranked_candidates.append((rank, -modified, str(path), path))

    ranked_candidates.sort()
    return tuple(item[3] for item in ranked_candidates)


def expected_reasoner_symbol_atlas_complete_json_name(project_root: str | Path) -> str:
    """Return the preferred complete JSON filename for the supplied project."""

    return project_name_from_root(project_root) + "__complete.json"


def _complete_json_name_rank(name: str, expected_name: str) -> int | None:
    """Return a selection rank for a complete JSON filename."""

    if name == expected_name:
        return 0
    if name.endswith("__complete.json"):
        return 1
    if name.endswith("_complete.json"):
        return 2
    return None


def load_reasoner_symbol_atlas_complete_json(json_path: str | Path) -> dict[str, Any]:
    """Load a generated complete JSON evidence file as a dictionary."""

    path = Path(json_path)
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid complete JSON evidence: " + str(path)) from exc
    if not isinstance(payload, dict):
        raise ValueError("Complete JSON evidence must contain a JSON object: " + str(path))
    return payload


def summarize_reasoner_symbol_atlas_complete_json(
    project_root: str | Path,
    json_path: str | Path | None = None,
    required_sections: Iterable[str] | None = None,
) -> ProjectSymbolAtlasCompleteJsonSummary:
    """Summarize a generated complete JSON evidence file.

    Missing evidence and invalid JSON are reported as statuses instead of being
    treated as source-tree failures. This keeps the adapter safe for projects
    that have not generated evidence yet.
    """

    root = Path(project_root).expanduser().resolve(strict=False)
    required = tuple(required_sections or PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_REQUIRED_SECTIONS)
    selected_path = _select_complete_json_path(root, json_path)
    if selected_path is None:
        return ProjectSymbolAtlasCompleteJsonSummary(
            project_root=str(root),
            status=PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_JSON,
            missing_sections=required,
            notes=("No complete JSON evidence file was found.",),
        )

    try:
        payload = load_reasoner_symbol_atlas_complete_json(selected_path)
    except ValueError as exc:
        return ProjectSymbolAtlasCompleteJsonSummary(
            project_root=str(root),
            json_path=str(selected_path),
            status=PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_INVALID_JSON,
            missing_sections=required,
            notes=(str(exc),),
        )

    available_sections = tuple(sorted(str(key) for key in payload.keys()))
    missing_sections = tuple(section for section in required if section not in payload)
    if missing_sections:
        status = PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_SECTIONS
        notes = ["Complete JSON evidence is missing required sections."]
    else:
        status = PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY
        notes = ["Complete JSON evidence is readable and has required sections."]

    expected_name = expected_reasoner_symbol_atlas_complete_json_name(root).lower()
    if selected_path.name.lower() == expected_name:
        notes.append("Selected complete JSON matches the current project prefix.")
    else:
        notes.append("Selected complete JSON is a fallback match, not the current project prefix.")

    recommended_present = tuple(
        section for section in PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_RECOMMENDED_SECTIONS
        if section in payload
    )

    return ProjectSymbolAtlasCompleteJsonSummary(
        project_root=str(root),
        json_path=str(selected_path),
        status=status,
        available_sections=available_sections,
        missing_sections=missing_sections,
        recommended_sections_present=recommended_present,
        source_file_count=_mapping_count(payload.get("source_file_index")),
        symbol_count=_mapping_count(payload.get("symbol_index")),
        primary_definition_count=_mapping_count(payload.get("primary_definition_index")),
        duplicate_symbol_count=_sequence_count(payload.get("duplicate_symbols")),
        notes=tuple(notes),
    )


def build_reasoner_symbol_atlas_complete_json_report(
    options: ProjectSymbolAtlasCompleteJsonOptions,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas report from complete JSON evidence."""

    summary = summarize_reasoner_symbol_atlas_complete_json(
        project_root=options.project_root,
        json_path=options.json_path or None,
        required_sections=options.required_sections,
    )
    modules: tuple[ProjectModuleRecord, ...] = ()
    symbols: tuple[ProjectSymbol, ...] = ()
    if summary.json_path and summary.status != PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_INVALID_JSON:
        payload = load_reasoner_symbol_atlas_complete_json(summary.json_path)
        modules = _modules_from_complete_json(payload, options.max_modules)
        symbols = _symbols_from_complete_json(payload, options.max_symbols)

    return ProjectSymbolAtlasReport(
        project_root=options.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_summary_line(summary),
        modules=modules,
        symbols=symbols,
        input_sources=("complete_json", summary.json_path),
    )


def _select_complete_json_path(
    project_root: Path,
    json_path: str | Path | None,
) -> Path | None:
    """Support select complete json path behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    json_path : str | Path | None
        The json path value.
    
    Returns
    -------
    Path | None
        The resolved path.
    """
    
    if json_path is not None and str(json_path).strip():
        return Path(json_path).expanduser().resolve(strict=False)
    candidates = collect_reasoner_symbol_atlas_complete_json_files(project_root)
    return candidates[0] if candidates else None


def _mapping_count(value: object) -> int:
    """Support mapping count behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(value) if isinstance(value, dict) else 0


def _sequence_count(value: object) -> int:
    """Support sequence count behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(value) if isinstance(value, list) else 0


def _format_summary_line(summary: ProjectSymbolAtlasCompleteJsonSummary) -> str:
    """Support format summary line behavior.
    
    Parameters
    ----------
    summary : ProjectSymbolAtlasCompleteJsonSummary
        The summary value.
    
    Returns
    -------
    str
        The string result.
    """
    
    data = summary.to_dict()
    return (
        "Complete JSON adapter status="
        + str(data["status"])
        + "; files="
        + str(data["source_file_count"])
        + "; symbols="
        + str(data["symbol_count"])
        + "; primary_definitions="
        + str(data["primary_definition_count"])
        + "; duplicate_symbols="
        + str(data["duplicate_symbol_count"])
    )


def _modules_from_complete_json(
    payload: dict[str, Any],
    limit: int,
) -> tuple[ProjectModuleRecord, ...]:
    """Support modules from complete json behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    limit : int
        The limit value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    source_index = payload.get("source_file_index")
    if not isinstance(source_index, dict) or limit <= 0:
        return ()
    responsibility_index = payload.get("web_ai_file_responsibility_index")
    if not isinstance(responsibility_index, dict):
        responsibility_index = {}

    modules: list[ProjectModuleRecord] = []
    for key in sorted(source_index.keys())[:limit]:
        item = source_index.get(key)
        if not isinstance(item, dict):
            continue
        file_path = normalize_project_atlas_text(item.get("file") or key)
        responsibility = responsibility_index.get(file_path, {})
        if not isinstance(responsibility, dict):
            responsibility = {}
        evidence = ["source_file_index"]
        owner_box = normalize_project_atlas_text(responsibility.get("owner_box"))
        primary_responsibility = normalize_project_atlas_text(
            responsibility.get("primary_responsibility")
        )
        if owner_box:
            evidence.append("owner_box: " + owner_box)
        if primary_responsibility:
            evidence.append("responsibility: " + primary_responsibility)
        modules.append(
            ProjectModuleRecord(
                module=normalize_project_atlas_text(
                    item.get("module_name") or _module_name_from_path(file_path)
                ),
                path=file_path,
                line_count=_safe_int(item.get("line_count")),
                is_package_init=Path(file_path).name == "__init__.py",
                is_test_file=_is_test_path(file_path),
                owner_role="unknown",
                symbols=(),
                imports=(),
                evidence=tuple(evidence),
            )
        )
    return tuple(modules)


def _symbols_from_complete_json(
    payload: dict[str, Any],
    limit: int,
) -> tuple[ProjectSymbol, ...]:
    """Support symbols from complete json behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    limit : int
        The limit value.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    symbol_index = payload.get("symbol_index")
    if not isinstance(symbol_index, dict) or limit <= 0:
        return ()
    web_symbol_index = payload.get("web_ai_symbol_index")
    if not isinstance(web_symbol_index, dict):
        web_symbol_index = {}

    symbols: list[ProjectSymbol] = []
    for key in sorted(symbol_index.keys())[:limit]:
        item = symbol_index.get(key)
        web_item = web_symbol_index.get(key)
        if not isinstance(item, dict):
            item = {}
        if not isinstance(web_item, dict):
            web_item = {}
        file_path = normalize_project_atlas_text(
            web_item.get("file") or item.get("file") or ""
        )
        kind = _coerce_symbol_kind(web_item.get("kind") or item.get("kind"))
        module = normalize_project_atlas_text(
            web_item.get("module_name") or _module_name_from_path(file_path)
        )
        line = _safe_int(web_item.get("line_start") or item.get("line")) or None
        evidence = ["symbol_index"]
        if key in web_symbol_index:
            evidence.append("web_ai_symbol_index")
        symbols.append(
            ProjectSymbol(
                name=normalize_project_atlas_text(
                    web_item.get("qualified_name") or web_item.get("symbol") or key
                ),
                kind=kind,
                module=module,
                path=file_path,
                line=line,
                is_public=not str(key).split(".")[-1].startswith("_"),
                owner_role="unknown",
                exported_by_all=False,
                evidence=tuple(evidence),
            )
        )
    return tuple(symbols)


def _coerce_symbol_kind(kind: object) -> str:
    """Support coerce symbol kind behavior.
    
    Parameters
    ----------
    kind : object
        The kind value.
    
    Returns
    -------
    str
        The string result.
    """
    
    normalized = normalize_project_atlas_text(kind).lower()
    if normalized in {"function", "method"}:
        return "function"
    if normalized in {"class", "dataclass", "constant", "import", "module"}:
        return normalized
    return "unknown"


def _module_name_from_path(path_text: str) -> str:
    """Support module name from path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not path_text:
        return ""
    path = Path(path_text)
    parts = list(path.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _is_test_path(path_text: str) -> bool:
    """Support is test path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    normalized = path_text.replace("\\", "/").lower()
    name = Path(normalized).name
    return normalized.startswith("tests/") or name.startswith("test_") or name.endswith("_test.py")


def _safe_int(value: object) -> int:
    """Support safe int behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    try:
        if value is None:
            return 0
        return int(value)
    except (TypeError, ValueError):
        return 0
