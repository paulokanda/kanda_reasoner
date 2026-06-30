# project-path: kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py
"""Read-only main file and helper file mapper for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .output_policy import is_active_atlas_path, is_active_test_command
from .evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from .schemas import (
    ProjectModuleRecord,
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY = "ready"
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND = "target_not_found"
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND = "no_helpers_found"
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN = "ambiguous_main"
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"

PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES = (
    "_commands",
    "_command",
    "_helpers",
    "_helper",
    "_actions",
    "_action",
    "_adapter",
    "_adapters",
    "_writer",
    "_writers",
    "_schema",
    "_schemas",
    "_mapper",
    "_resolver",
    "_classifier",
    "_scanner",
    "_indexer",
    "_report",
    "_reports",
    "_utils",
    "_utility",
    "_utilities",
)

__all__ = [
    "PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND",
    "ProjectSymbolAtlasMainHelperDecision",
    "ProjectSymbolAtlasMainHelperOptions",
    "build_reasoner_symbol_atlas_main_helper_report",
    "map_reasoner_symbol_atlas_main_helpers",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasMainHelperOptions:
    """Options for resolving main-file and helper-file relationships."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = False
    include_workbench: bool = False
    include_private: bool = False
    max_helpers: int = 25

    def to_merge_options(self) -> ProjectSymbolAtlasEvidenceMergeOptions:
        """Return compatible evidence merge options."""

        return ProjectSymbolAtlasEvidenceMergeOptions(
            project_root=self.project_root,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "include_private": bool(self.include_private),
            "max_helpers": int(self.max_helpers),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasMainHelperDecision:
    """Decision output for main and helper file mapping."""

    project_root: str
    target_path: str = ""
    target_role: str = "unknown"
    main_path: str = ""
    main_module: str = ""
    helper_paths: tuple[str, ...] = field(default_factory=tuple)
    helper_modules: tuple[str, ...] = field(default_factory=tuple)
    private_helper_paths: tuple[str, ...] = field(default_factory=tuple)
    public_helper_warnings: tuple[str, ...] = field(default_factory=tuple)
    public_api_owner_path: str = ""
    status: str = PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE
    confidence: str = "low"
    evidence: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "target_role": normalize_project_atlas_text(self.target_role),
            "main_path": str(Path(self.main_path)) if self.main_path else "",
            "main_module": normalize_project_atlas_text(self.main_module),
            "helper_paths": normalize_project_atlas_sequence(self.helper_paths),
            "helper_modules": normalize_project_atlas_sequence(self.helper_modules),
            "private_helper_paths": normalize_project_atlas_sequence(self.private_helper_paths),
            "public_helper_warnings": normalize_project_atlas_sequence(self.public_helper_warnings),
            "public_api_owner_path": str(Path(self.public_api_owner_path)) if self.public_api_owner_path else "",
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "evidence": normalize_project_atlas_sequence(self.evidence),
            "tests_to_run": normalize_project_atlas_sequence(self.tests_to_run),
        }


def map_reasoner_symbol_atlas_main_helpers(
    options: ProjectSymbolAtlasMainHelperOptions,
) -> ProjectSymbolAtlasMainHelperDecision:
    """Map the main file and helper files for a target path or symbol."""

    project_root = _coerce_project_root(options.project_root)
    report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        options.to_merge_options()
    )
    modules = tuple(record for record in report.modules if _record_is_active(record))
    target_record = _find_target_record(
        project_root=project_root,
        modules=modules,
        target_path=options.target_path,
        symbol_name=options.symbol_name,
    )
    if target_record is None:
        return ProjectSymbolAtlasMainHelperDecision(
            project_root=str(project_root),
            target_path=options.target_path,
            status=PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND,
            confidence="high" if options.target_path or options.symbol_name else "low",
            evidence=("Target file or symbol was not found in atlas evidence.",),
        )

    target_role = _target_role(target_record)
    main_record = _select_main_record(target_record, modules)
    helper_records = _select_helper_records(
        target_record=target_record,
        main_record=main_record,
        modules=modules,
        max_helpers=options.max_helpers,
    )
    helper_records = tuple(record for record in helper_records if record.path != main_record.path)
    private_helpers = tuple(
        record.path for record in helper_records if _record_is_private_helper(record)
    )
    warnings = _public_helper_warnings(helper_records)
    status, confidence, evidence = _decision_status(
        target_record=target_record,
        main_record=main_record,
        helper_records=helper_records,
        merge_status=merge_summary.status,
    )
    tests_to_run = _related_tests_to_run(modules, main_record, helper_records)
    return ProjectSymbolAtlasMainHelperDecision(
        project_root=str(project_root),
        target_path=target_record.path,
        target_role=target_role,
        main_path=main_record.path,
        main_module=main_record.module,
        helper_paths=tuple(record.path for record in helper_records),
        helper_modules=tuple(record.module for record in helper_records),
        private_helper_paths=private_helpers,
        public_helper_warnings=warnings,
        public_api_owner_path=main_record.path,
        status=status,
        confidence=confidence,
        evidence=evidence,
        tests_to_run=tests_to_run,
    )


def build_reasoner_symbol_atlas_main_helper_report(
    options: ProjectSymbolAtlasMainHelperOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for main-file and helper-file mapping."""

    decision = map_reasoner_symbol_atlas_main_helpers(options)
    symbols = [
        ProjectSymbol(
            name="main_file",
            kind="unknown",
            module=decision.main_module,
            path=decision.main_path,
            is_public=False,
            owner_role="canonical_owner" if decision.main_path else "unknown",
            evidence=decision.evidence,
        )
    ]
    for helper_path, helper_module in zip(decision.helper_paths, decision.helper_modules):
        symbols.append(
            ProjectSymbol(
                name="helper_file",
                kind="unknown",
                module=helper_module,
                path=helper_path,
                is_public=False,
                owner_role="private_helper",
                evidence=("main/helper map helper candidate",),
            )
        )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_decision_summary(decision),
        symbols=tuple(symbols),
        input_sources=("live_ast", "complete_json_if_fresh", "main_helper_mapper"),
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
    
    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _find_target_record(
    project_root: Path,
    modules: tuple[ProjectModuleRecord, ...],
    target_path: str,
    symbol_name: str,
) -> ProjectModuleRecord | None:
    """Support find target record behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    target_path : str
        The target path value.
    symbol_name : str
        The symbol name value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    if target_path:
        normalized_target = _normalize_path_for_compare(project_root, target_path)
        for record in modules:
            if _normalize_record_path(record.path) == normalized_target:
                return record
    if symbol_name:
        matches = [
            record
            for record in modules
            for symbol in record.symbols
            if symbol.name == symbol_name and symbol.is_public
        ]
        if matches:
            return sorted(matches, key=lambda item: (item.owner_role != "canonical_owner", item.path))[0]
    return None


def _normalize_path_for_compare(project_root: Path, path_text: str) -> str:
    """Support normalize path for compare behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    path = Path(path_text)
    if path.is_absolute():
        try:
            path = path.relative_to(project_root)
        except ValueError:
            pass
    return _normalize_record_path(str(path))


def _normalize_record_path(path_text: str) -> str:
    """Support normalize record path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(Path(path_text)).replace("\\", "/")




def _record_is_active(record: ProjectModuleRecord) -> bool:
    """Support record is active behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return is_active_atlas_path(record.path)


def _active_records(records: tuple[ProjectModuleRecord, ...]) -> tuple[ProjectModuleRecord, ...]:
    """Support active records behavior.
    
    Parameters
    ----------
    records : tuple[ProjectModuleRecord, ...]
        The record values.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    return tuple(record for record in records if _record_is_active(record))


def _target_is_helper_like(record: ProjectModuleRecord) -> bool:
    """Support target is helper like behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if _record_is_private_helper(record):
        return True
    return _has_helper_suffix(record)


def _record_is_low_signal_support_file(record: ProjectModuleRecord) -> bool:
    """Support record is low signal support file behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    stem = _module_stem(record).lower()
    low_signal_tokens = (
        "smoke",
        "probe",
        "static_context",
        "diagnostic",
        "status",
        "validation",
    )
    return any(token in stem for token in low_signal_tokens)

def _target_role(record: ProjectModuleRecord) -> str:
    """Support target role behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if _record_is_private_helper(record):
        return "helper"
    if _has_helper_suffix(record):
        return "helper"
    if record.owner_role in {"facade", "compatibility_facade"}:
        return "facade"
    return "main"


def _select_main_record(
    target_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
) -> ProjectModuleRecord:
    """Select the main owner for a target without inventing weak owners.

    Facade classification is a review signal, not enough evidence to move
    ownership to a loosely related smoke/probe file. Only helper-shaped targets
    should search for a separate main owner.
    """

    if not _target_is_helper_like(target_record):
        return target_record
    candidates = _main_candidates_for_helper(target_record, modules)
    if candidates:
        return candidates[0]
    return target_record


def _main_candidates_for_helper(
    helper_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
) -> tuple[ProjectModuleRecord, ...]:
    """Support main candidates for helper behavior.
    
    Parameters
    ----------
    helper_record : ProjectModuleRecord
        The helper record value.
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    helper_stem = _module_stem(helper_record)
    base_stem = _strip_helper_suffix(helper_stem)
    candidates: list[tuple[int, ProjectModuleRecord]] = []
    for record in modules:
        if record.path == helper_record.path or record.is_test_file or not _record_is_active(record):
            continue
        if _record_is_low_signal_support_file(record):
            continue
        score = 0
        record_stem = _module_stem(record)
        if record_stem == base_stem:
            score += 60
        if _module_imports(record, helper_record):
            score += 40
        if record.owner_role == "canonical_owner":
            score += 10
        if score > 0:
            candidates.append((score, record))
    return tuple(record for _score, record in sorted(candidates, key=lambda item: (-item[0], item[1].path)))


def _select_helper_records(
    target_record: ProjectModuleRecord,
    main_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
    max_helpers: int,
) -> tuple[ProjectModuleRecord, ...]:
    """Support select helper records behavior.
    
    Parameters
    ----------
    target_record : ProjectModuleRecord
        The target record value.
    main_record : ProjectModuleRecord
        The main record value.
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    max_helpers : int
        The max helpers value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    scored: list[tuple[int, ProjectModuleRecord]] = []
    for record in modules:
        if record.path == main_record.path or record.is_test_file or not _record_is_active(record):
            continue
        score = _helper_score(main_record, record)
        if record.path == target_record.path and _target_role(target_record) == "helper":
            score += 100
        if score > 0:
            scored.append((score, record))
    ordered = [record for _score, record in sorted(scored, key=lambda item: (-item[0], item[1].path))]
    return tuple(ordered[: max(0, int(max_helpers))])


def _helper_score(main_record: ProjectModuleRecord, candidate: ProjectModuleRecord) -> int:
    """Support helper score behavior.
    
    Parameters
    ----------
    main_record : ProjectModuleRecord
        The main record value.
    candidate : ProjectModuleRecord
        The candidate value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    score = 0
    main_stem = _module_stem(main_record)
    candidate_stem = _module_stem(candidate)
    if candidate_stem.startswith(main_stem + "_") and _has_helper_suffix(candidate):
        score += 80
    if _module_imports(main_record, candidate):
        score += 50
    if _module_imports(candidate, main_record):
        score += 15
    if score > 0 and _record_is_private_helper(candidate):
        score += 10
    return score


def _module_imports(source: ProjectModuleRecord, target: ProjectModuleRecord) -> bool:
    """Support module imports behavior.
    
    Parameters
    ----------
    source : ProjectModuleRecord
        The source value.
    target : ProjectModuleRecord
        The target value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    target_module = normalize_project_atlas_text(target.module)
    if not target_module:
        return False
    imports = {normalize_project_atlas_text(item) for item in source.imports}
    if target_module in imports:
        return True
    return any(item.endswith("." + target_module.rsplit(".", 1)[-1]) for item in imports)


def _module_stem(record: ProjectModuleRecord) -> str:
    """Support module stem behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    path = Path(record.path)
    if path.name == "__init__.py":
        return path.parent.name
    return path.stem


def _strip_helper_suffix(stem: str) -> str:
    """Support strip helper suffix behavior.
    
    Parameters
    ----------
    stem : str
        The stem value.
    
    Returns
    -------
    str
        The string result.
    """
    
    for suffix in sorted(PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES, key=len, reverse=True):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def _has_helper_suffix(record: ProjectModuleRecord) -> bool:
    """Support has helper suffix behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    stem = _module_stem(record)
    return any(stem.endswith(suffix) for suffix in PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES)


def _record_is_private_helper(record: ProjectModuleRecord) -> bool:
    """Support record is private helper behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return record.owner_role == "private_helper" or "private_helper" in tuple(record.evidence)


def _public_helper_warnings(
    helper_records: tuple[ProjectModuleRecord, ...],
) -> tuple[str, ...]:
    """Support public helper warnings behavior.
    
    Parameters
    ----------
    helper_records : tuple[ProjectModuleRecord, ...]
        The helper records value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    warnings: list[str] = []
    for record in helper_records:
        public_symbols = [symbol.name for symbol in record.symbols if symbol.is_public]
        if public_symbols and not _record_is_private_helper(record):
            warnings.append(
                "Helper exposes public symbols: " + record.path + " -> " + ", ".join(sorted(public_symbols)[:8])
            )
    return tuple(warnings)


def _related_tests_to_run(
    modules: tuple[ProjectModuleRecord, ...],
    main_record: ProjectModuleRecord,
    helper_records: tuple[ProjectModuleRecord, ...],
) -> tuple[str, ...]:
    """Support related tests to run behavior.
    
    Parameters
    ----------
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    main_record : ProjectModuleRecord
        The main record value.
    helper_records : tuple[ProjectModuleRecord, ...]
        The helper records value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return tuple()

def _decision_status(
    target_record: ProjectModuleRecord,
    main_record: ProjectModuleRecord,
    helper_records: tuple[ProjectModuleRecord, ...],
    merge_status: str,
) -> tuple[str, str, tuple[str, ...]]:
    """Support decision status behavior.
    
    Parameters
    ----------
    target_record : ProjectModuleRecord
        The target record value.
    main_record : ProjectModuleRecord
        The main record value.
    helper_records : tuple[ProjectModuleRecord, ...]
        The helper records value.
    merge_status : str
        The merge status value.
    
    Returns
    -------
    tuple[str, str, tuple[str, ...]]
        The tuple of values.
    """
    
    evidence = ["Evidence merge status: " + merge_status]
    if target_record.path != main_record.path:
        evidence.append("Target is helper-like; main owner selected from related files.")
    if helper_records:
        evidence.append("Helper candidates found: " + str(len(helper_records)))
        return PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY, "medium", tuple(evidence)
    evidence.append("No helper candidates were found for the selected main file.")
    return PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND, "medium", tuple(evidence)


def _format_decision_summary(decision: ProjectSymbolAtlasMainHelperDecision) -> str:
    """Support format decision summary behavior.
    
    Parameters
    ----------
    decision : ProjectSymbolAtlasMainHelperDecision
        The decision value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return (
        f"Main/helper map status={decision.status}; "
        f"target_role={decision.target_role}; main={decision.main_path}; "
        f"helper_count={len(decision.helper_paths)}; confidence={decision.confidence}"
    )
