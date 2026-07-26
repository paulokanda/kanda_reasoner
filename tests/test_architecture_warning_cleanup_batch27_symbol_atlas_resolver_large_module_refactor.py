# project-path: tests/test_architecture_warning_cleanup_batch27_symbol_atlas_resolver_large_module_refactor.py
"""Characterization tests for Batch 27 symbol-atlas resolver refactor."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_freshness import (
    ProjectSymbolAtlasEvidenceFreshnessOptions,
    build_reasoner_symbol_atlas_evidence_freshness_report,
    check_reasoner_symbol_atlas_evidence_freshness,
)
from kanda_reasoner_app.reasoner_symbol_atlas.evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    build_reasoner_symbol_atlas_live_json_merge_report,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from kanda_reasoner_app.reasoner_symbol_atlas.facade_owner_resolver import (
    ProjectSymbolAtlasFacadeOwnerOptions,
    build_reasoner_symbol_atlas_facade_owner_report,
    resolve_reasoner_symbol_atlas_facade_owner,
)
from kanda_reasoner_app.reasoner_symbol_atlas.implementation_responsibility_resolver import (
    ProjectSymbolAtlasImplementationResponsibilityOptions,
    resolve_reasoner_symbol_atlas_implementation_responsibility,
)


def run_characterization() -> None:
    """Run bounded public-facade characterization checks."""

    project_root = Path(__file__).resolve().parents[1]
    freshness_options = ProjectSymbolAtlasEvidenceFreshnessOptions(
        project_root=str(project_root),
        json_path="",
        max_items=5,
    )
    freshness = check_reasoner_symbol_atlas_evidence_freshness(freshness_options)
    assert freshness.project_root
    freshness_report = build_reasoner_symbol_atlas_evidence_freshness_report(
        freshness_options
    )
    assert freshness_report.report_type == "reasoner_symbol_atlas"

    merge_options = ProjectSymbolAtlasEvidenceMergeOptions(
        project_root=str(project_root),
        json_path="",
        include_tests=False,
        include_workbench=False,
        include_private=False,
        max_json_modules=25,
        max_json_symbols=50,
    )
    merge_report_direct, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        merge_options
    )
    assert merge_report_direct.report_type == "reasoner_symbol_atlas"
    assert merge_summary.project_root
    merge_report = build_reasoner_symbol_atlas_live_json_merge_report(merge_options)
    assert merge_report.report_type == "reasoner_symbol_atlas"

    target_path = "kanda_reasoner_app/reasoner_symbol_atlas/evidence_merger.py"
    facade_options = ProjectSymbolAtlasFacadeOwnerOptions(
        project_root=str(project_root),
        target_path=target_path,
        symbol_name="merge_reasoner_symbol_atlas_live_and_json_evidence",
        include_tests=False,
        include_workbench=False,
        include_private=False,
    )
    facade_decision = resolve_reasoner_symbol_atlas_facade_owner(facade_options)
    assert facade_decision.target_path.endswith("evidence_merger.py")
    facade_report = build_reasoner_symbol_atlas_facade_owner_report(facade_options)
    assert facade_report.report_type == "reasoner_symbol_atlas"

    responsibility_options = ProjectSymbolAtlasImplementationResponsibilityOptions(
        project_root=str(project_root),
        task_description="refactor symbol atlas resolver module",
        target_path=target_path,
        symbol_name="merge_reasoner_symbol_atlas_live_and_json_evidence",
        include_tests=False,
        include_workbench=False,
        include_private=False,
    )
    assert responsibility_options.to_dict()["target_path"].endswith("evidence_merger.py")
    assert callable(resolve_reasoner_symbol_atlas_implementation_responsibility)


def test_batch27_symbol_atlas_resolver_public_facades() -> None:
    """Pytest-compatible public facade test."""

    run_characterization()


if __name__ == "__main__":
    run_characterization()
