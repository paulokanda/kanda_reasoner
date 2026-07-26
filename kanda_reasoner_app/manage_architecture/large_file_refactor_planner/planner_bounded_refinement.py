# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_bounded_refinement.py
"""Shared bounded architecture refinement rules for local and Web AI proposals."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from .models import (
    MIN_HELPER_PHYSICAL_LINES,
    DocstringProposal,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
)

__all__ = [
    "apply_bounded_architecture_refinement",
    "apply_bounded_docstring_updates",
    "apply_bounded_plan_reassignments",
    "attach_docstring_proposals_to_plan",
    "plan_allows_ai_architecture_correction",
]

_SIZE_BLOCKER_PREFIXES = (
    "Planned helper ",
    "Planned module ",
)
_REPEATED_FILENAME_BLOCKER_PREFIX = "Repeated proposed filename: "
_SIZE_RISKS = {"TOO_SMALL_HELPER", "TOO_LARGE_COHESIVE_GROUP"}


def attach_docstring_proposals_to_plan(
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
) -> RefactorPlan:
    """Return a plan carrying accepted Planner docstring proposals."""

    return replace(plan, docstring_proposals=list(proposals))


def plan_allows_ai_architecture_correction(plan: RefactorPlan) -> bool:
    """Return whether a plan is ready or blocked only by AI-correctable size gates."""

    if plan.status != "blocked":
        return True
    blockers = list(plan.validation_blockers)
    return bool(blockers) and all(
        item.startswith(_SIZE_BLOCKER_PREFIXES) for item in blockers
    )


def apply_bounded_plan_reassignments(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    reassignments: list[dict[str, str]],
) -> RefactorPlan:
    """Compatibility wrapper for bounded symbol reassignment refinement."""

    return apply_bounded_architecture_refinement(
        report,
        plan,
        reassignments=reassignments,
        module_merges=[],
        module_renames=[],
    )


def apply_bounded_architecture_refinement(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    *,
    reassignments: list[dict[str, str]],
    module_merges: list[dict[str, str]],
    module_renames: list[dict[str, str]],
) -> RefactorPlan:
    """Apply safe structural changes and deterministically revalidate architecture."""

    helpers = [
        module
        for module in plan.proposed_modules
        if module.role != "public_facade"
    ]
    helper_names = {module.filename for module in helpers}
    assignments = {
        symbol_name: module.filename
        for module in helpers
        for symbol_name in module.symbols
    }
    merges = _normalize_module_merges(module_merges, helper_names)
    requested = _normalize_reassignments(reassignments, assignments, helper_names)
    merged_away = set(merges)
    if any(target in merged_away for target in requested.values()):
        raise ValueError(
            "A reassignment cannot target a helper merged away in the same round."
        )
    _apply_module_merges(assignments, merges)
    assignments.update(requested)
    _validate_atomic_cluster_cohesion(report, assignments)
    _validate_helper_dependency_cycles(report, assignments)

    surviving_names = set(assignments.values())
    renames = _normalize_module_renames(
        plan,
        module_renames,
        surviving_names,
    )
    return _rebuild_plan(
        report,
        plan,
        helpers,
        assignments,
        renames,
    )


def apply_bounded_docstring_updates(
    proposals: list[DocstringProposal],
    updates: list[dict[str, str]],
    *,
    provenance: str,
) -> list[DocstringProposal]:
    """Apply updates only to already-known docstring proposal targets."""

    allowed = {
        (proposal.target_kind, proposal.target_name): proposal
        for proposal in proposals
    }
    normalized: dict[tuple[str, str], str] = {}
    for item in updates:
        key = (
            str(item.get("target_kind", "")).strip(),
            str(item.get("target_name", "")).strip(),
        )
        text = str(item.get("proposed_docstring", "")).strip()
        if key not in allowed:
            raise ValueError(
                "Docstring update target is not in the deterministic proposal set: "
                + key[0]
                + ":"
                + key[1]
            )
        if key in normalized:
            raise ValueError(
                "Duplicate docstring update target: " + key[0] + ":" + key[1]
            )
        _validate_docstring_text(text)
        normalized[key] = text

    result: list[DocstringProposal] = []
    for proposal in proposals:
        key = (proposal.target_kind, proposal.target_name)
        replacement = normalized.get(key)
        if replacement is None:
            result.append(proposal)
            continue
        result.append(
            replace(
                proposal,
                proposed_docstring=replacement,
                provenance=provenance,
                confidence="medium",
                status="proposed",
                reason=(
                    proposal.reason
                    + " Refined by bounded planning review and requires human review."
                ).strip(),
            )
        )
    return result


def _normalize_module_merges(
    items: list[dict[str, str]],
    helper_names: set[str],
) -> dict[str, str]:
    """Validate direct helper-to-helper merges with no chains or cycles."""

    merges: dict[str, str] = {}
    for item in items:
        source = str(item.get("source_module", "")).strip()
        target = str(item.get("target_module", "")).strip()
        if not source or not target:
            raise ValueError("Each module merge needs source_module and target_module.")
        if source == target:
            raise ValueError("A helper cannot merge into itself: " + source)
        if source not in helper_names or target not in helper_names:
            raise ValueError("Module merge must use known helper modules only.")
        if source in merges:
            raise ValueError("Duplicate module merge source: " + source)
        merges[source] = target
    sources = set(merges)
    if any(target in sources for target in merges.values()):
        raise ValueError("Module merge chains and cycles are not allowed in one round.")
    return merges


def _normalize_reassignments(
    items: list[dict[str, str]],
    assignments: dict[str, str],
    helper_names: set[str],
) -> dict[str, str]:
    """Validate known symbol-to-known-helper moves with duplicate rejection."""

    requested: dict[str, str] = {}
    for item in items:
        symbol_name = str(item.get("symbol", "")).strip()
        target_module = str(item.get("target_module", "")).strip()
        if not symbol_name or not target_module:
            raise ValueError("Each reassignment needs symbol and target_module.")
        if symbol_name not in assignments:
            raise ValueError("Symbol is not movable in the current plan: " + symbol_name)
        if target_module not in helper_names:
            raise ValueError(
                "Target module is outside the allowed helper set: " + target_module
            )
        if symbol_name in requested:
            raise ValueError("Duplicate symbol reassignment: " + symbol_name)
        requested[symbol_name] = target_module
    return requested


def _apply_module_merges(
    assignments: dict[str, str],
    merges: dict[str, str],
) -> None:
    """Move every symbol from each source helper into its approved target helper."""

    for symbol_name, current_module in list(assignments.items()):
        target_module = merges.get(current_module)
        if target_module is not None:
            assignments[symbol_name] = target_module


def _normalize_module_renames(
    plan: RefactorPlan,
    items: list[dict[str, str]],
    surviving_names: set[str],
) -> dict[str, str]:
    """Validate semantic renames of surviving helpers without creating modules."""

    renames: dict[str, str] = {}
    new_names: set[str] = set()
    target_path = Path(plan.target_file)
    for item in items:
        module_name = str(item.get("module", "")).strip()
        new_filename = str(item.get("new_filename", "")).strip()
        if module_name not in surviving_names:
            raise ValueError("Only surviving known helpers may be renamed: " + module_name)
        _validate_private_helper_filename(new_filename)
        if module_name in renames:
            raise ValueError("Duplicate module rename: " + module_name)
        if new_filename in new_names:
            raise ValueError("Duplicate renamed helper filename: " + new_filename)
        if new_filename == target_path.name:
            raise ValueError("Helper rename cannot take the public facade filename.")
        existing = target_path.parent / new_filename
        if existing.exists() and new_filename != module_name:
            raise ValueError("Renamed helper filename already exists: " + new_filename)
        renames[module_name] = new_filename
        new_names.add(new_filename)
    final_names = {
        renames.get(module_name, module_name) for module_name in surviving_names
    }
    if len(final_names) != len(surviving_names):
        raise ValueError("Module renames must remain unique.")
    return renames


def _validate_private_helper_filename(filename: str) -> None:
    """Require a simple private Python helper basename."""

    path = Path(filename)
    if not filename or path.name != filename or path.suffix != ".py":
        raise ValueError("Renamed helper must be one Python basename.")
    if not path.stem.startswith("_") or path.stem in {"_", "__init__"}:
        raise ValueError("Renamed helper must remain a private underscore-prefixed module.")
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    if any(char not in allowed for char in path.stem):
        raise ValueError("Renamed helper contains unsupported filename characters.")


def _rebuild_plan(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    helpers: list[ProposedModule],
    assignments: dict[str, str],
    renames: dict[str, str],
) -> RefactorPlan:
    """Rebuild helper contracts and all size blockers from deterministic evidence."""

    line_map = {symbol.name: symbol.physical_lines for symbol in report.symbols}
    original_lines = {
        module.filename: sum(line_map.get(name, 0) for name in module.symbols)
        for module in helpers
    }
    overhead = {
        module.filename: max(
            0,
            module.estimated_lines - original_lines[module.filename],
        )
        for module in helpers
    }
    minimum = max(
        MIN_HELPER_PHYSICAL_LINES,
        int(plan.settings.get("minimum_helper_physical_lines", 100)),
    )
    maximum = int(plan.settings.get("maximum_physical_lines", 500))
    blockers = [
        item
        for item in plan.validation_blockers
        if not item.startswith(_SIZE_BLOCKER_PREFIXES)
        and not item.startswith(_REPEATED_FILENAME_BLOCKER_PREFIX)
    ]
    proposed: list[ProposedModule] = [
        module
        for module in plan.proposed_modules
        if module.role == "public_facade"
    ]
    small_found = False
    large_found = False
    helper_by_name = {module.filename: module for module in helpers}
    for module_name in sorted(set(assignments.values())):
        module = helper_by_name[module_name]
        symbols = sorted(
            name
            for name, assigned in assignments.items()
            if assigned == module_name
        )
        estimated_lines = overhead[module_name] + sum(
            line_map.get(name, 0) for name in symbols
        )
        flags = [flag for flag in module.risk_flags if flag not in _SIZE_RISKS]
        if estimated_lines < minimum:
            small_found = True
            flags.append("TOO_SMALL_HELPER")
            blockers.append(
                "Planned helper "
                + renames.get(module_name, module_name)
                + " is below minimum helper size of "
                + str(minimum)
                + " lines."
            )
        if estimated_lines > maximum:
            large_found = True
            flags.append("TOO_LARGE_COHESIVE_GROUP")
            blockers.append(
                "Planned module "
                + renames.get(module_name, module_name)
                + " exceeds maximum lines."
            )
        proposed.append(
            replace(
                module,
                filename=renames.get(module_name, module_name),
                symbols=symbols,
                estimated_lines=estimated_lines,
                risk_flags=sorted(set(flags)),
                status="warning" if flags else "planned",
                line_limit_justification=(
                    "AI-refined bounded architecture; deterministically revalidated."
                ),
            )
        )

    final_assignment = {
        symbol_name: renames.get(module_name, module_name)
        for symbol_name, module_name in assignments.items()
    }
    symbol_records = [
        replace(
            symbol,
            assigned_module=final_assignment.get(
                symbol.name,
                symbol.assigned_module,
            ),
        )
        for symbol in plan.symbols
    ]
    repeated_filename_blockers = _repeated_filename_blockers(proposed)
    blockers.extend(repeated_filename_blockers)

    risks = [
        item
        for item in plan.risks
        if item not in _SIZE_RISKS and item != "FILENAME_COLLISION"
    ]
    if small_found:
        risks.append("TOO_SMALL_HELPER")
    if large_found:
        risks.append("TOO_LARGE_COHESIVE_GROUP")
    if repeated_filename_blockers or any(
        item.startswith("Proposed filename already exists: ")
        for item in blockers
    ):
        risks.append("FILENAME_COLLISION")
    unique_blockers = sorted(set(blockers))
    return replace(
        plan,
        symbols=symbol_records,
        proposed_modules=proposed,
        risks=sorted(set(risks)),
        validation_blockers=unique_blockers,
        status="blocked" if unique_blockers else "planned",
    )



def _repeated_filename_blockers(
    proposed: list[ProposedModule],
) -> list[str]:
    """Recompute repeated-filename blockers from the rebuilt module set."""

    blockers: list[str] = []
    seen: set[str] = set()
    for module in proposed:
        if module.filename in seen:
            blockers.append(_REPEATED_FILENAME_BLOCKER_PREFIX + module.filename)
        seen.add(module.filename)
    return blockers

def _validate_atomic_cluster_cohesion(
    report: ModuleAnalysisReport,
    assignments: dict[str, str],
) -> None:
    """Reject a final assignment that splits any movable atomic cluster."""

    clusters: dict[str, set[str]] = {}
    for symbol in report.symbols:
        if symbol.atomic_cluster_id and symbol.name in assignments:
            clusters.setdefault(symbol.atomic_cluster_id, set()).add(symbol.name)
    for members in clusters.values():
        targets = {assignments[name] for name in members}
        if len(targets) > 1:
            raise ValueError(
                "Architectural correction would split an atomic symbol cluster."
            )


def _validate_helper_dependency_cycles(
    report: ModuleAnalysisReport,
    assignments: dict[str, str],
) -> None:
    """Reject helper assignment graphs that create cross-helper dependency cycles."""

    known_symbols = {symbol.name for symbol in report.symbols}
    graph: dict[str, set[str]] = {
        module_name: set() for module_name in set(assignments.values())
    }
    for symbol in report.symbols:
        source_module = assignments.get(symbol.name)
        if source_module is None:
            continue
        for reference in set(symbol.references) & known_symbols:
            target_module = assignments.get(reference)
            if target_module and target_module != source_module:
                graph[source_module].add(target_module)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module_name: str) -> None:
        if module_name in visiting:
            raise ValueError("Architectural correction introduces a helper dependency cycle.")
        if module_name in visited:
            return
        visiting.add(module_name)
        for dependency in graph.get(module_name, set()):
            visit(dependency)
        visiting.remove(module_name)
        visited.add(module_name)

    for module_name in graph:
        visit(module_name)


def _validate_docstring_text(text: str) -> None:
    """Fail closed on malformed or oversized docstring proposal text."""

    if not text:
        raise ValueError("Docstring update text cannot be empty.")
    if len(text) > 6000:
        raise ValueError("Docstring update exceeds 6000 characters.")
    if not (text.startswith('"""') and text.endswith('"""')):
        raise ValueError("Docstring update must be wrapped in triple double quotes.")
    if "```" in text:
        raise ValueError("Docstring update must not contain Markdown code fences.")
