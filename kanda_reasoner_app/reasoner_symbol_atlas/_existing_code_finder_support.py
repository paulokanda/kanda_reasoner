# project-path: kanda_reasoner_app/reasoner_symbol_atlas/_existing_code_finder_support.py
"""Private support helpers for Project Symbol Atlas existing-code finder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .facade_owner_resolver import resolve_reasoner_symbol_atlas_facade_owner
from .implementation_responsibility_resolver import (
    resolve_reasoner_symbol_atlas_implementation_responsibility,
)
from .logic_placement_advisor import advise_reasoner_symbol_atlas_logic_placement
from .main_helper_mapper import map_reasoner_symbol_atlas_main_helpers
from .pre_patch_gate import run_reasoner_symbol_atlas_pre_patch_gate
from .related_file_finder import find_reasoner_symbol_atlas_related_files
from .schemas import normalize_project_atlas_sequence, normalize_project_atlas_text

__all__: list[str] = []


@dataclass(frozen=True)
class ExistingCodeComponentResult:
    """Private normalized output from query-specific atlas components."""

    facade_owner_path: str = ""
    facade_reasons: tuple[str, ...] = field(default_factory=tuple)
    main_path: str = ""
    helper_paths: tuple[str, ...] = field(default_factory=tuple)
    main_evidence: tuple[str, ...] = field(default_factory=tuple)
    related_files: tuple[str, ...] = field(default_factory=tuple)
    related_tests: tuple[str, ...] = field(default_factory=tuple)
    related_evidence: tuple[str, ...] = field(default_factory=tuple)
    placement_reasons: tuple[str, ...] = field(default_factory=tuple)
    responsibility_reasons: tuple[str, ...] = field(default_factory=tuple)
    responsibility_tests: tuple[str, ...] = field(default_factory=tuple)
    primary_edit_target: str = ""
    files_not_to_touch: tuple[str, ...] = field(default_factory=tuple)
    pre_patch_reasons: tuple[str, ...] = field(default_factory=tuple)
    pre_patch_tests: tuple[str, ...] = field(default_factory=tuple)
    pre_patch_status: str = ""


def run_existing_code_component_plan(
    options: Any,
    query_type: str,
) -> ExistingCodeComponentResult:
    """Run only the component group needed for a query type."""

    facade_owner_path = ""
    facade_reasons: tuple[str, ...] = ()
    main_path = ""
    helper_paths: tuple[str, ...] = ()
    main_evidence: tuple[str, ...] = ()
    related_files: tuple[str, ...] = ()
    related_tests: tuple[str, ...] = ()
    related_evidence: tuple[str, ...] = ()
    placement_reasons: tuple[str, ...] = ()
    responsibility_reasons: tuple[str, ...] = ()
    responsibility_tests: tuple[str, ...] = ()
    primary_edit_target = ""
    files_not_to_touch: tuple[str, ...] = ()
    pre_patch_reasons: tuple[str, ...] = ()
    pre_patch_tests: tuple[str, ...] = ()
    pre_patch_status = ""

    if query_type in {"facade_owner", "pre_patch_gate"}:
        facade = resolve_reasoner_symbol_atlas_facade_owner(options.to_facade_options())
        facade_owner_path = facade.likely_real_owner_path
        facade_reasons = facade.reasons + facade.facade_evidence
    if query_type in {"main_helpers", "pre_patch_gate"}:
        main_helper = map_reasoner_symbol_atlas_main_helpers(options.to_main_helper_options())
        main_path = main_helper.main_path
        helper_paths = main_helper.helper_paths
        main_evidence = main_helper.evidence
        related_tests = _unique_strings(related_tests + main_helper.tests_to_run)
    if query_type in {"related_files", "pre_patch_gate"}:
        related = find_reasoner_symbol_atlas_related_files(options.to_related_options())
        related_files = related.related_files
        related_tests = _unique_strings(related_tests + related.tests_to_run)
        related_evidence = related.evidence
    if query_type in {"logic_placement", "pre_patch_gate"}:
        placement = advise_reasoner_symbol_atlas_logic_placement(
            options.to_logic_placement_options()
        )
        placement_reasons = placement.reasons
    if query_type in {"implementation_responsibility", "pre_patch_gate"}:
        responsibility = resolve_reasoner_symbol_atlas_implementation_responsibility(
            options.to_responsibility_options()
        )
        primary_edit_target = responsibility.primary_edit_target
        files_not_to_touch = responsibility.files_not_to_touch
        responsibility_tests = responsibility.tests_to_run
        responsibility_reasons = responsibility.reasons
    if query_type == "pre_patch_gate":
        pre_patch = run_reasoner_symbol_atlas_pre_patch_gate(options.to_pre_patch_options())
        pre_patch_status = pre_patch.status
        pre_patch_reasons = pre_patch.reasons
        pre_patch_tests = pre_patch.tests_to_run
        if not primary_edit_target:
            primary_edit_target = pre_patch.primary_edit_target
        files_not_to_touch = _unique_strings(
            files_not_to_touch + pre_patch.files_not_to_touch
        )

    return ExistingCodeComponentResult(
        facade_owner_path=facade_owner_path,
        facade_reasons=facade_reasons,
        main_path=main_path,
        helper_paths=helper_paths,
        main_evidence=main_evidence,
        related_files=related_files,
        related_tests=related_tests,
        related_evidence=related_evidence,
        placement_reasons=placement_reasons,
        responsibility_reasons=responsibility_reasons,
        responsibility_tests=responsibility_tests,
        primary_edit_target=primary_edit_target,
        files_not_to_touch=files_not_to_touch,
        pre_patch_reasons=pre_patch_reasons,
        pre_patch_tests=pre_patch_tests,
        pre_patch_status=pre_patch_status,
    )


def format_existing_code_summary(result: Any) -> str:
    """Return a compact decision summary for a result object."""

    parts = [
        "Existing code finder query completed",
        "status=" + result.status,
        "confidence=" + result.confidence,
        "query_type=" + result.query_type,
    ]
    if result.primary_edit_target:
        parts.append("primary_edit_target=" + result.primary_edit_target)
    if result.facade_owner_path:
        parts.append("facade_owner=" + result.facade_owner_path)
    if result.pre_patch_status:
        parts.append("pre_patch_status=" + result.pre_patch_status)
    return "; ".join(parts) + "."


def structured_decision_evidence(result: Any) -> tuple[str, ...]:
    """Return key=value decision evidence for Markdown and JSON reports."""

    values: list[str] = [
        "query_type=" + result.query_type,
        "status=" + result.status,
        "confidence=" + result.confidence,
    ]
    values.extend(_keyed_values("owner_path", result.owner_paths))
    values.extend(_keyed_values("duplicate_symbol", [s.path for s in result.duplicate_symbols]))
    values.extend(_keyed_value("facade_owner_path", result.facade_owner_path))
    values.extend(_keyed_value("main_path", result.main_path))
    values.extend(_keyed_values("helper_path", result.helper_paths))
    values.extend(_keyed_values("related_file", result.related_files))
    values.extend(_keyed_values("test_to_run", result.tests_to_run))
    values.extend(_keyed_value("primary_edit_target", result.primary_edit_target))
    values.extend(_keyed_values("file_not_to_touch", result.files_not_to_touch))
    values.extend(_keyed_value("pre_patch_status", result.pre_patch_status))
    values.extend("reason=" + reason for reason in result.reasons)
    return _unique_strings(values)


def _keyed_value(key: str, value: str) -> tuple[str, ...]:
    """Support keyed value behavior.
    
    Parameters
    ----------
    key : str
        The key value.
    value : str
        The input value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    cleaned = normalize_project_atlas_text(value)
    if not cleaned:
        return ()
    return (key + "=" + cleaned,)


def _keyed_values(key: str, values: Any) -> tuple[str, ...]:
    """Support keyed values behavior.
    
    Parameters
    ----------
    key : str
        The key value.
    values : Any
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return tuple(key + "=" + value for value in _unique_strings(values))


def _unique_strings(values: Any) -> tuple[str, ...]:
    """Support unique strings behavior.
    
    Parameters
    ----------
    values : Any
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    output: list[str] = []
    seen: set[str] = set()
    for value in normalize_project_atlas_sequence(values):
        item = normalize_project_atlas_text(value)
        if item and item not in seen:
            output.append(item)
            seen.add(item)
    return tuple(output)
