"""Read-only facade versus real-owner resolver for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

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

PROJECT_SYMBOL_ATLAS_FACADE_STATUS_READY = "ready"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NO_FACADE = "not_a_facade"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND = "target_not_found"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_OWNER_NOT_FOUND = "owner_not_found"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NO_FACADE",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_OWNER_NOT_FOUND",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND",
    "ProjectSymbolAtlasFacadeOwnerDecision",
    "ProjectSymbolAtlasFacadeOwnerOptions",
    "build_reasoner_symbol_atlas_facade_owner_report",
    "resolve_reasoner_symbol_atlas_facade_owner",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasFacadeOwnerOptions:
    """Options for resolving whether a target is a facade or true owner."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = True
    include_workbench: bool = False
    include_private: bool = False

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
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasFacadeOwnerDecision:
    """Decision output for facade versus real-owner resolution."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    target_is_facade: bool = False
    target_owner_role: str = "unknown"
    likely_real_owner_path: str = ""
    likely_real_owner_module: str = ""
    should_patch_target: bool = False
    status: str = PROJECT_SYMBOL_ATLAS_FACADE_STATUS_INSUFFICIENT_EVIDENCE
    confidence: str = "low"
    owner_candidates: tuple[str, ...] = field(default_factory=tuple)
    facade_evidence: tuple[str, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "target_is_facade": bool(self.target_is_facade),
            "target_owner_role": normalize_project_atlas_text(self.target_owner_role),
            "likely_real_owner_path": str(Path(self.likely_real_owner_path)) if self.likely_real_owner_path else "",
            "likely_real_owner_module": normalize_project_atlas_text(self.likely_real_owner_module),
            "should_patch_target": bool(self.should_patch_target),
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "owner_candidates": normalize_project_atlas_sequence(self.owner_candidates),
            "facade_evidence": normalize_project_atlas_sequence(self.facade_evidence),
            "reasons": normalize_project_atlas_sequence(self.reasons),
        }


def resolve_reasoner_symbol_atlas_facade_owner(
    options: ProjectSymbolAtlasFacadeOwnerOptions,
) -> ProjectSymbolAtlasFacadeOwnerDecision:
    """Resolve whether the target path is a facade and identify likely owner."""

    project_root = _coerce_project_root(options.project_root)
    report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        options.to_merge_options()
    )
    modules = report.modules
    symbols = report.symbols
    target_record = _find_target_record(project_root, modules, options.target_path)
    if target_record is None:
        return ProjectSymbolAtlasFacadeOwnerDecision(
            project_root=str(project_root),
            target_path=options.target_path,
            symbol_name=options.symbol_name,
            status=PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND,
            confidence="high" if options.target_path else "low",
            reasons=("Target file was not found in live atlas evidence.",),
        )

    target_is_facade = _record_is_facade(target_record)
    facade_evidence = _facade_evidence(target_record)
    owner_candidates = _candidate_owner_paths(
        target_record=target_record,
        modules=modules,
        symbols=symbols,
        symbol_name=options.symbol_name,
    )
    likely_owner = _select_likely_owner(modules, owner_candidates)
    likely_owner_path = likely_owner.path if likely_owner is not None else ""
    likely_owner_module = likely_owner.module if likely_owner is not None else ""
    status, confidence, should_patch_target, reasons = _decision_status(
        target_record=target_record,
        target_is_facade=target_is_facade,
        likely_owner=likely_owner,
        owner_candidates=owner_candidates,
        merge_status=merge_summary.status,
    )
    return ProjectSymbolAtlasFacadeOwnerDecision(
        project_root=str(project_root),
        target_path=target_record.path,
        symbol_name=options.symbol_name,
        target_is_facade=target_is_facade,
        target_owner_role=target_record.owner_role,
        likely_real_owner_path=likely_owner_path,
        likely_real_owner_module=likely_owner_module,
        should_patch_target=should_patch_target,
        status=status,
        confidence=confidence,
        owner_candidates=owner_candidates,
        facade_evidence=facade_evidence,
        reasons=reasons,
    )


def build_reasoner_symbol_atlas_facade_owner_report(
    options: ProjectSymbolAtlasFacadeOwnerOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for facade versus real-owner resolution."""

    decision = resolve_reasoner_symbol_atlas_facade_owner(options)
    evidence_symbol = ProjectSymbol(
        name="facade_owner_decision",
        kind="unknown",
        module="reasoner_symbol_atlas.facade_owner_resolver",
        path=decision.likely_real_owner_path or decision.target_path,
        is_public=False,
        owner_role="unknown",
        evidence=decision.reasons + decision.facade_evidence,
    )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_decision_summary(decision),
        symbols=(evidence_symbol,),
        input_sources=("live_ast", "complete_json_if_fresh", "facade_owner_resolver"),
    )


def _coerce_project_root(project_root: str | Path) -> Path:
    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _normalize_relative_path(path_text: str) -> str:
    if not path_text:
        return ""
    return str(Path(path_text)).replace("\\", "/")


def _find_target_record(
    project_root: Path,
    modules: tuple[ProjectModuleRecord, ...],
    target_path: str,
) -> ProjectModuleRecord | None:
    if not target_path:
        return None
    target = Path(target_path)
    if target.is_absolute():
        try:
            target_key = str(target.resolve(strict=False).relative_to(project_root)).replace("\\", "/")
        except ValueError:
            target_key = str(target).replace("\\", "/")
    else:
        target_key = _normalize_relative_path(target_path)
    for record in modules:
        record_key = _normalize_relative_path(record.path)
        if record_key == target_key:
            return record
    target_name = target.name
    matches = [record for record in modules if Path(record.path).name == target_name]
    if len(matches) == 1:
        return matches[0]
    return None


def _record_is_facade(record: ProjectModuleRecord) -> bool:
    if record.owner_role in {"facade", "compatibility_facade"}:
        return True
    evidence_text = "\n".join(record.evidence).lower()
    if "facade_shape_candidate: true" in evidence_text:
        return True
    if "module_getattr_export_detected: true" in evidence_text:
        return True
    if "reexport_" in evidence_text:
        return True
    import_symbol_count = len([symbol for symbol in record.symbols if symbol.kind == "import"])
    local_public_count = len(
        [
            symbol
            for symbol in record.symbols
            if symbol.kind != "import" and symbol.is_public and symbol.name != "__all__"
        ]
    )
    return import_symbol_count > 0 and local_public_count == 0


def _facade_evidence(record: ProjectModuleRecord) -> tuple[str, ...]:
    values: list[str] = []
    for item in record.evidence:
        lowered = item.lower()
        if "facade" in lowered or "reexport" in lowered or "explicit_all" in lowered or "getattr" in lowered:
            values.append(item)
    for symbol in record.symbols:
        if symbol.kind == "import":
            values.extend(symbol.evidence)
    return tuple(dict.fromkeys(values))


def _source_modules_from_import_symbol(symbol: ProjectSymbol) -> tuple[str, ...]:
    values: list[str] = []
    for item in symbol.evidence:
        if not item.startswith("source: "):
            continue
        source = item[len("source: ") :].strip()
        if not source:
            continue
        if source.startswith("."):
            continue
        parts = source.split(".")
        if len(parts) > 1:
            values.append(".".join(parts[:-1]))
        values.append(source)
    return tuple(dict.fromkeys(values))


def _record_for_module_name(
    modules: tuple[ProjectModuleRecord, ...],
    module_name: str,
) -> ProjectModuleRecord | None:
    if not module_name:
        return None
    for record in modules:
        if record.module == module_name:
            return record
    module_suffix = "." + module_name
    for record in modules:
        if record.module.endswith(module_suffix):
            return record
    return None


def _candidate_owner_paths(
    target_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
    symbols: tuple[ProjectSymbol, ...],
    symbol_name: str,
) -> tuple[str, ...]:
    candidates: list[str] = []
    for symbol in target_record.symbols:
        if symbol.kind != "import":
            continue
        if symbol_name and symbol.name != symbol_name:
            continue
        for module_name in _source_modules_from_import_symbol(symbol):
            record = _record_for_module_name(modules, module_name)
            if record is not None and record.path != target_record.path:
                candidates.append(record.path)
    if symbol_name:
        for symbol in symbols:
            if symbol.name != symbol_name or symbol.path == target_record.path:
                continue
            if symbol.kind == "import":
                continue
            record = _record_for_path(modules, symbol.path)
            if record is not None and not _record_is_facade(record):
                candidates.append(record.path)
    return tuple(dict.fromkeys(candidates))


def _record_for_path(
    modules: tuple[ProjectModuleRecord, ...],
    path_text: str,
) -> ProjectModuleRecord | None:
    key = _normalize_relative_path(path_text)
    for record in modules:
        if _normalize_relative_path(record.path) == key:
            return record
    return None


def _select_likely_owner(
    modules: tuple[ProjectModuleRecord, ...],
    candidate_paths: tuple[str, ...],
) -> ProjectModuleRecord | None:
    records = [_record_for_path(modules, path) for path in candidate_paths]
    records = [record for record in records if record is not None]
    if not records:
        return None
    non_facades = [record for record in records if not _record_is_facade(record)]
    if non_facades:
        records = non_facades
    role_order = {
        "canonical_owner": 0,
        "private_helper": 1,
        "unknown": 2,
        "ambiguous_owner": 3,
        "facade": 4,
        "compatibility_facade": 4,
    }
    records.sort(key=lambda record: (role_order.get(record.owner_role, 9), record.path))
    return records[0]


def _decision_status(
    target_record: ProjectModuleRecord,
    target_is_facade: bool,
    likely_owner: ProjectModuleRecord | None,
    owner_candidates: tuple[str, ...],
    merge_status: str,
) -> tuple[str, str, bool, tuple[str, ...]]:
    reasons: list[str] = []
    reasons.append("Target owner role: " + target_record.owner_role + ".")
    reasons.append("Evidence merge status: " + merge_status + ".")
    if target_is_facade:
        reasons.append("Target appears to be a facade or compatibility re-export surface.")
        if likely_owner is not None:
            reasons.append("Patch the likely real owner instead of the facade.")
            return (
                PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW,
                "high",
                False,
                tuple(reasons),
            )
        reasons.append("No real owner candidate was identified from current evidence.")
        return (
            PROJECT_SYMBOL_ATLAS_FACADE_STATUS_OWNER_NOT_FOUND,
            "medium" if owner_candidates else "low",
            False,
            tuple(reasons),
        )
    reasons.append("Target does not look like a facade from current evidence.")
    return (
        PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NO_FACADE,
        "medium",
        True,
        tuple(reasons),
    )


def _format_decision_summary(decision: ProjectSymbolAtlasFacadeOwnerDecision) -> str:
    if decision.target_is_facade and decision.likely_real_owner_path:
        return (
            "Target appears to be a facade. Likely real owner: "
            + decision.likely_real_owner_path
            + "."
        )
    if decision.target_is_facade:
        return "Target appears to be a facade, but no real owner candidate was found."
    if decision.status == PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND:
        return "Target file was not found in atlas evidence."
    return "Target does not appear to be a facade from current atlas evidence."
