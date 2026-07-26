# project-path: kanda_reasoner_app/reasoner_symbol_atlas/pre_patch_gate_helpers_private.py
"""Private helper logic for the Project Symbol Atlas pre-patch gate."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .evidence_freshness import (
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT,
)
from .schemas import ProjectSymbol, normalize_project_atlas_text
from .shadow_report import (
    ProjectSymbolAtlasShadowReportOptions,
    collect_reasoner_symbol_atlas_shadow_findings,
)

__all__: list[str] = []


def _matching_duplicate_findings(options: Any) -> tuple[ProjectSymbol, ...]:
    symbol_name = normalize_project_atlas_text(options.symbol_name)
    if not symbol_name:
        return tuple()
    try:
        findings = collect_reasoner_symbol_atlas_shadow_findings(
            options.project_root,
            options=ProjectSymbolAtlasShadowReportOptions(
                include_tests=False,
                include_workbench=False,
                include_facades=True,
                include_import_symbols=False,
                include_constants=True,
                include_private=options.include_private,
            ),
        )
    except (FileNotFoundError, NotADirectoryError):
        return tuple()
    return tuple(item for item in findings if item.name == symbol_name)


def _wrong_target_file(target_path: str, primary_edit_target: str) -> bool:
    target = _normalize_path(target_path)
    primary = _normalize_path(primary_edit_target)
    return bool(target and primary and target.lower() != primary.lower())


def _evidence_is_stale(status: str, fail_on_stale: bool) -> bool:
    if not fail_on_stale:
        return False
    return status in {
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE,
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE,
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT,
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE,
    }


def _missing_test_protection(
    options: Any,
    related_test_files: tuple[str, ...],
) -> bool:
    if not options.require_test_protection:
        return False
    if not options.include_tests:
        return False
    return len(related_test_files) == 0


def _reasons(
    responsibility_reasons: tuple[str, ...],
    related_evidence: tuple[str, ...],
    duplicate_findings: tuple[ProjectSymbol, ...],
    evidence_status: str,
    duplicate_symbol_risk: bool,
    facade_patch_risk: bool,
    wrong_target_file: bool,
    missing_test_protection: bool,
    evidence_stale: bool,
    safe_to_patch: bool,
) -> tuple[str, ...]:
    values: list[str] = []
    for value in responsibility_reasons + related_evidence:
        _append_unique(values, value)
    _append_unique(values, "Evidence freshness status: " + evidence_status)
    for finding in duplicate_findings:
        _append_unique(values, "Duplicate public symbol risk: " + finding.name)
    if duplicate_symbol_risk:
        _append_unique(values, "Duplicate public symbol found before patching.")
    if facade_patch_risk:
        _append_unique(values, "Target appears to be a facade; patch real owner instead.")
    if wrong_target_file:
        _append_unique(values, "Target differs from selected primary edit target.")
    if missing_test_protection:
        _append_unique(values, "No related focused test file was found.")
    if evidence_stale:
        _append_unique(values, "Evidence is stale or wrong-project and was treated as unsafe.")
    if safe_to_patch:
        _append_unique(values, "No blocking ownership risk detected.")
    return tuple(values)


def _merge_tests(first: tuple[str, ...], second: tuple[str, ...]) -> tuple[str, ...]:
    values: list[str] = []
    for item in first + second:
        _append_unique(values, item)
    return tuple(values)


def _normalize_path(path_text: str) -> str:
    if not path_text:
        return ""
    return str(Path(path_text)).replace("\\", "/")


def _append_unique(values: list[str], value: str) -> None:
    cleaned = normalize_project_atlas_text(value)
    if cleaned and cleaned not in values:
        values.append(cleaned)
