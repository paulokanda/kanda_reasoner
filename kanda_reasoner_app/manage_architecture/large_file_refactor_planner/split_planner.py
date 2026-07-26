# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/split_planner.py
"""Deterministic split-plan contracts for the Large File Refactor Planner."""
from __future__ import annotations

from pathlib import Path

from .dependency_clusterer import DependencyCluster, build_dependency_clusters
from .planner_dependency_topology import build_module_dependency_topology
from .planner_heuristic_candidates import (
    HeuristicCandidateSelection,
    build_ranked_heuristic_candidates,
)
from .planner_git_cochange import collect_git_cochange_evidence
from .planner_responsibility_labels import ResponsibilityLabel, label_cluster_responsibilities
from .planner_semantic_naming import semantic_helper_filename
from .models import (
    FEATURE_ID,
    MAX_PHYSICAL_LINES,
    MIN_HELPER_PHYSICAL_LINES,
    SCHEMA_VERSION,
    ModuleAnalysisReport,
    PlannerSettings,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
)

__all__ = ["build_split_plan"]

_SIDE_EFFECT_FLAGS = {"GLOBAL_STATE", "DECORATOR_RISK", "NESTED_SYMBOL_CLUSTER"}
_IMPORT_RISK_FLAGS = {"RELATIVE_IMPORT_RISK", "STAR_IMPORT"}
_BLOCKING_RISKS = {
    "TOO_LARGE_CLASS",
    "TOO_LARGE_COHESIVE_GROUP",
    "TOO_SMALL_HELPER",
    "FILENAME_COLLISION",
}


def build_split_plan(
    report: ModuleAnalysisReport,
    settings: PlannerSettings | None = None,
    *,
    source_path: str | Path | None = None,
    preferred_strategy: str = "",
) -> RefactorPlan:
    """Build a read-only split plan without writing preview files."""
    active_settings = settings or PlannerSettings()
    risks: list[str] = list(report.risk_flags)
    blockers: list[str] = []
    target_path = Path(report.target_file)
    proposed: list[ProposedModule] = []

    facade_symbols = _facade_symbols(report.symbols, report.public_api_symbols)
    movable_symbols = [symbol for symbol in report.symbols if symbol.name not in facade_symbols]
    facade_estimate = _estimate_facade_lines(report, facade_symbols)
    proposed.append(
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename=target_path.name,
            role="public_facade",
            symbols=sorted(facade_symbols),
            estimated_lines=facade_estimate,
            preview_physical_lines=0,
            imports=_import_names(report),
            exports=list(report.public_api_symbols),
            risk_flags=_facade_risks(report, facade_estimate, active_settings),
            status="planned",
            line_limit_justification="Original module remains the public facade.",
        )
    )

    for symbol in report.symbols:
        if symbol.kind == "class" and symbol.physical_lines > active_settings.maximum_physical_lines:
            risks.append("TOO_LARGE_CLASS")
            blockers.append(f"Class {symbol.name} exceeds maximum physical lines.")
        if symbol.physical_lines > active_settings.maximum_physical_lines and symbol.kind != "class":
            risks.append("TOO_LARGE_COHESIVE_GROUP")
            blockers.append(f"Symbol {symbol.name} exceeds maximum physical lines.")

    clustering = build_dependency_clusters(
        report,
        active_settings,
        [symbol.name for symbol in movable_symbols],
    )
    risks.extend(clustering.risk_flags)
    blockers.extend(clustering.blockers)
    git_history = collect_git_cochange_evidence(
        source_path,
        report,
        clustering.clusters,
    )
    candidate_selection = build_ranked_heuristic_candidates(
        report,
        active_settings,
        clustering.clusters,
        git_history,
    )
    candidate_selection = _prefer_candidate_strategy(
        candidate_selection,
        preferred_strategy,
    )
    selected_clusters = candidate_selection.selected_clusters
    responsibility_labels = label_cluster_responsibilities(report, selected_clusters)
    proposed.extend(
        _modules_for_clusters(
            target_path,
            selected_clusters,
            movable_symbols,
            active_settings,
            responsibility_labels,
        )
    )

    collision_blockers = _filename_collision_blockers(target_path, proposed)
    if collision_blockers:
        risks.append("FILENAME_COLLISION")
        blockers.extend(collision_blockers)

    projected_topology = build_module_dependency_topology(report, proposed)
    risks.extend(projected_topology.warnings)
    if projected_topology.helper_cycles:
        risks.append("HELPER_DEPENDENCY_CYCLE")
    blockers.extend(projected_topology.blockers)

    for module in proposed:
        if module.estimated_lines > active_settings.maximum_physical_lines:
            risks.append("TOO_LARGE_COHESIVE_GROUP")
            blockers.append(f"Planned module {module.filename} exceeds maximum lines.")
        if _is_tiny_helper(module, active_settings):
            minimum = max(
                MIN_HELPER_PHYSICAL_LINES,
                active_settings.minimum_helper_physical_lines,
            )
            risks.append("TOO_SMALL_HELPER")
            blockers.append(
                "Planned helper "
                + module.filename
                + " is below minimum helper size of "
                + str(minimum)
                + " lines."
            )

    for item in report.imports:
        risks.extend(flag for flag in item.risk_flags if flag in _IMPORT_RISK_FLAGS)

    unique_risks = sorted(set(risks))
    blockers = sorted(set(blockers))
    status = "blocked" if blockers or set(unique_risks) & _BLOCKING_RISKS else "planned"
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=report.target_file,
        source_content_hash=report.source_content_hash,
        settings=active_settings.to_dict(),
        public_api_before=list(report.public_api_symbols),
        public_api_after_expected=list(report.public_api_symbols),
        symbols=list(report.symbols),
        atomic_clusters=sorted(set(_atomic_clusters(report.symbols)) | {cluster.cluster_id for cluster in clustering.clusters}),
        proposed_modules=proposed,
        import_migration={
            "rewrite_project_imports": False,
            "import_migration_preview": True,
            "status": "preview_only_future_train",
            "dependency_clustering": clustering.to_dict(),
            "heuristic_candidate_selection": candidate_selection.to_dict(),
            "git_historical_coupling": git_history.to_dict(),
            "responsibility_labeling": {
                cluster_id: label.to_dict()
                for cluster_id, label in responsibility_labels.items()
            },
            "projected_dependency_topology": projected_topology.to_dict(),
        },
        docstring_proposals=[],
        risks=unique_risks,
        validation_blockers=blockers,
        status=status,
    )


def _prefer_candidate_strategy(
    selection: HeuristicCandidateSelection,
    preferred_strategy: str,
) -> HeuristicCandidateSelection:
    """Select one requested deterministic strategy without changing default ranking."""
    requested = str(preferred_strategy or "").strip()
    if not requested:
        return selection
    for candidate in selection.candidates:
        if candidate.strategy == requested:
            return HeuristicCandidateSelection(
                selected_candidate_id=candidate.candidate_id,
                selected_strategy=candidate.strategy,
                candidates=list(selection.candidates),
            )
    return selection


def _facade_symbols(symbols: list[RefactorSymbol], public_api: list[str]) -> set[str]:
    """Return symbols that should stay facade-owned in the contract plan."""
    facade = set(public_api)
    for symbol in symbols:
        if set(symbol.risk_flags) & _SIDE_EFFECT_FLAGS:
            facade.add(symbol.name)
        if symbol.visibility == "public" and not public_api:
            facade.add(symbol.name)
    return facade


def _estimate_facade_lines(report: ModuleAnalysisReport, facade_symbols: set[str]) -> int:
    """Estimate facade size without generating files."""
    import_lines = len(report.imports)
    export_lines = 2 if report.public_api_symbols else 0
    side_effect_lines = len(report.module_level_calls) + len(report.assignments)
    symbol_lines = sum(
        symbol.physical_lines for symbol in report.symbols if symbol.name in facade_symbols
    )
    base_lines = 12 if report.module_docstring_present else 8
    return base_lines + import_lines + export_lines + side_effect_lines + symbol_lines


def _facade_risks(
    report: ModuleAnalysisReport,
    facade_estimate: int,
    settings: PlannerSettings,
) -> list[str]:
    """Return risk flags for the planned facade module."""
    flags: list[str] = []
    if facade_estimate > settings.maximum_physical_lines:
        flags.append("TOO_LARGE_COHESIVE_GROUP")
    if report.if_main_present:
        flags.append("FACADE_REEXPORT_RISK")
    if any(item.is_star for item in report.imports):
        flags.append("STAR_IMPORT")
    if any(item.is_relative for item in report.imports):
        flags.append("RELATIVE_IMPORT_RISK")
    return sorted(set(flags))


def _modules_for_clusters(
    target_path: Path,
    clusters: list[DependencyCluster],
    movable_symbols: list[RefactorSymbol],
    settings: PlannerSettings,
    responsibility_labels: dict[str, ResponsibilityLabel],
) -> list[ProposedModule]:
    """Create helper modules from dependency-aware clusters."""
    if not clusters:
        return []
    symbol_by_name = {symbol.name: symbol for symbol in movable_symbols}
    responsibility_index: dict[str, int] = {}
    modules: list[ProposedModule] = []
    for cluster in sorted(clusters, key=lambda item: _cluster_start_line(item, symbol_by_name)):
        symbols = [symbol_by_name[name] for name in cluster.symbols if name in symbol_by_name]
        if not symbols:
            continue
        label = responsibility_labels[cluster.cluster_id]
        responsibility_index[label.primary_responsibility] = (
            responsibility_index.get(label.primary_responsibility, 0) + 1
        )
        modules.append(
            _proposed_helper(
                target_path,
                cluster.role,
                sorted(symbols, key=lambda item: item.start_line),
                cluster.estimated_lines,
                responsibility_index[label.primary_responsibility],
                settings,
                cluster,
                label,
            )
        )
    return modules


def _cluster_start_line(
    cluster: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> int:
    """Return the first source line for a dependency cluster."""
    starts = [symbol_by_name[name].start_line for name in cluster.symbols if name in symbol_by_name]
    return min(starts) if starts else 0


def _proposed_helper(
    target_path: Path,
    role: str,
    symbols: list[RefactorSymbol],
    estimated_lines: int,
    index: int,
    settings: PlannerSettings,
    cluster: DependencyCluster | None = None,
    responsibility_label: ResponsibilityLabel | None = None,
) -> ProposedModule:
    """Create one helper-module contract record."""
    filename = (
        semantic_helper_filename(target_path, responsibility_label, index)
        if responsibility_label is not None
        else _helper_filename(target_path, role, index)
    )
    flags: list[str] = []
    justification = "Cohesive helper created to keep modules below 500 physical lines."
    if cluster is not None and cluster.dependency_edges:
        justification = "Cohesive dependency cluster preserved by split planning."
    minimum = max(
        MIN_HELPER_PHYSICAL_LINES, settings.minimum_helper_physical_lines
    )
    if estimated_lines < minimum:
        flags.append("TOO_SMALL_HELPER")
        justification = (
            "Below minimum helper size; architectural correction must consolidate "
            "the helper before Workbench handoff."
        )
    if estimated_lines > settings.maximum_physical_lines:
        flags.append("TOO_LARGE_COHESIVE_GROUP")
    if cluster is not None:
        flags.extend(cluster.risk_flags)
    return ProposedModule(
        schema_version=SCHEMA_VERSION,
        filename=filename,
        role=role,
        symbols=[symbol.name for symbol in symbols],
        estimated_lines=estimated_lines,
        preview_physical_lines=0,
        imports=[],
        exports=[],
        risk_flags=sorted(set(flags)),
        status="planned" if not flags else "warning",
        line_limit_justification=justification,
    )


def _helper_filename(target_path: Path, role: str, index: int) -> str:
    """Return a deterministic private helper filename."""
    suffix = role.replace("_helper", "")
    serial = "" if index == 1 else f"_{index}"
    return f"_{target_path.stem}_{suffix}{serial}.py"


def _is_tiny_helper(
    module: ProposedModule,
    settings: PlannerSettings,
) -> bool:
    """Return whether a non-facade helper violates the hard minimum-size gate."""

    minimum = max(
        MIN_HELPER_PHYSICAL_LINES, settings.minimum_helper_physical_lines
    )
    return module.role != "public_facade" and module.estimated_lines < minimum


def _filename_collision_blockers(
    target_path: Path,
    proposed: list[ProposedModule],
) -> list[str]:
    """Return filename collision blockers for proposed outputs."""
    blockers: list[str] = []
    seen: set[str] = set()
    for module in proposed:
        name = module.filename
        if name in seen:
            blockers.append(f"Repeated proposed filename: {name}")
        seen.add(name)
        if name != target_path.name and (target_path.parent / name).exists():
            blockers.append(f"Proposed filename already exists: {name}")
    return blockers


def _import_names(report: ModuleAnalysisReport) -> list[str]:
    """Return stable import display names."""
    return [item.imported_name for item in report.imports]


def _atomic_clusters(symbols: list[RefactorSymbol]) -> set[str]:
    """Return atomic cluster ids for preserved symbol groups."""
    clusters = {symbol.atomic_cluster_id for symbol in symbols if symbol.atomic_cluster_id}
    for symbol in symbols:
        if symbol.risk_flags:
            clusters.add(f"risk:{symbol.name}")
    return clusters
