# project-path: kanda_reasoner_app/reasoner_symbol_atlas/final_status.py
"""Final Project Symbol Atlas status collector.

This module is intentionally read-only for analyzed project source. It checks
that the Project Symbol Atlas implementation, producer path updates, CLI
integration, Engineering Safety integration, and GUI wiring artifacts are
present, then writes optional JSON and Markdown status reports.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .evidence_paths import resolve_project_analysis_evidence_paths

PRODUCT_PACKAGE_PLACEHOLDER = "<PRODUCT_PACKAGE>"

EXPECTED_PROJECT_SYMBOL_ATLAS_FILES = [
    "schemas.py",
    "report_writer.py",
    "module_scanner.py",
    "symbol_indexer.py",
    "import_analyzer.py",
    "owner_classifier.py",
    "shadow_report.py",
    "test_protection_mapper.py",
    "evidence_paths.py",
    "evidence_migration.py",
    "evidence_producer_status.py",
    "complete_json_adapter.py",
    "evidence_freshness.py",
    "evidence_merger.py",
    "json_active_scope_quality.py",
    "logic_placement_advisor.py",
    "facade_owner_resolver.py",
    "main_helper_mapper.py",
    "implementation_responsibility_resolver.py",
    "related_file_finder.py",
    "_related_file_finder_support.py",
    "pre_patch_gate.py",
    "existing_code_finder.py",
    "atlas_report_builder.py",
]

EXPECTED_ADJACENT_PACKAGE_FILES = [
    ("safety_suite_cli", "reasoner_symbol_atlas_commands.py"),
    ("engineering_safety", "reasoner_symbol_atlas_integration.py"),
]

EXPECTED_SOURCE_FILES = [
    f"{PRODUCT_PACKAGE_PLACEHOLDER}/reasoner_symbol_atlas/{file_name}"
    for file_name in EXPECTED_PROJECT_SYMBOL_ATLAS_FILES
] + [
    f"{PRODUCT_PACKAGE_PLACEHOLDER}/{directory}/{file_name}"
    for directory, file_name in EXPECTED_ADJACENT_PACKAGE_FILES
]

EXPECTED_GUI_FILES = [
    "reasoner_tools_gui_engineering_safety_panel.py",
    "_reasoner_tools_gui_engineering_safety_panel_commands.py",
]

EXPECTED_FOCUSED_TESTS = [
    "tests/test_pa001_reasoner_symbol_atlas_schema.py",
    "tests/test_pa002_project_module_scanner.py",
    "tests/test_pa003_public_symbol_indexer.py",
    "tests/test_pa004_import_facade_analyzer.py",
    "tests/test_pa005_symbol_owner_classifier.py",
    "tests/test_pa006_symbol_shadow_report.py",
    "tests/test_pa007a_project_analysis_evidence_paths.py",
    "tests/test_pa007b_project_analysis_evidence_migration.py",
    "tests/test_pa007c_tab4_complete_json_output_path.py",
    "tests/test_pa007d_tab5_split_json_output_path.py",
    "tests/test_pa007e_project_analysis_evidence_status.py",
    "tests/test_pa008_complete_json_atlas_adapter.py",
    "tests/test_pa009_evidence_freshness_checker.py",
    "tests/test_pa010_live_and_json_evidence_merger.py",
    "tests/test_pa011_logic_placement_advisor.py",
    "tests/test_pa012_facade_owner_resolver.py",
    "tests/test_pa013_main_helper_mapper.py",
    "tests/test_pa014_implementation_responsibility_resolver.py",
    "tests/test_pa015_related_file_finder.py",
    "tests/test_pa016_pre_patch_ownership_gate.py",
    "tests/test_pa017_existing_code_finder.py",
    "tests/test_pa018_atlas_report_builder.py",
    "tests/test_pa019_reasoner_symbol_atlas_cli.py",
    "tests/test_reasoner_symbol_atlas_commands.py",
    "tests/test_reasoner_symbol_atlas_integration.py",
    "tests/test_pa021_reasoner_symbol_atlas_gui_integration.py",
]

EXPECTED_CLI_COMMANDS = [
    "atlas-report",
    "symbol-atlas",
    "evidence-freshness",
    "find-symbol",
    "find-owner",
    "facade-owner",
    "main-helpers",
    "related-files",
    "logic-placement",
    "pre-patch-gate",
]

EXPECTED_GUI_COMMANDS = [
    "atlas-report",
    "evidence-freshness",
    "find-symbol",
    "find-owner",
    "facade-owner",
    "main-helpers",
    "related-files",
    "pre-patch-gate",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasFinalStatusOptions:
    """Options for the final status collector."""

    project_root: str | Path
    output_dir: str | Path | None = None
    write_reports: bool = False


@dataclass(frozen=True)
class ProjectSymbolAtlasFinalStatusResult:
    """Final status result for Project Symbol Atlas."""

    project_root: str
    status: str
    missing_source_files: list[str] = field(default_factory=list)
    missing_gui_files: list[str] = field(default_factory=list)
    missing_focused_tests: list[str] = field(default_factory=list)
    canonical_evidence_dir: str = ""
    legacy_evidence_dir: str = ""
    canonical_evidence_exists: bool = False
    legacy_evidence_exists: bool = False
    legacy_evidence_required: bool = False
    expected_cli_commands: list[str] = field(default_factory=list)
    expected_gui_commands: list[str] = field(default_factory=list)
    json_report_path: str = ""
    markdown_report_path: str = ""
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping."""
        return {
            "project_root": self.project_root,
            "status": self.status,
            "missing_source_files": list(self.missing_source_files),
            "missing_gui_files": list(self.missing_gui_files),
            "missing_focused_tests": list(self.missing_focused_tests),
            "canonical_evidence_dir": self.canonical_evidence_dir,
            "legacy_evidence_dir": self.legacy_evidence_dir,
            "canonical_evidence_exists": self.canonical_evidence_exists,
            "legacy_evidence_exists": self.legacy_evidence_exists,
            "legacy_evidence_required": self.legacy_evidence_required,
            "expected_cli_commands": list(self.expected_cli_commands),
            "expected_gui_commands": list(self.expected_gui_commands),
            "json_report_path": self.json_report_path,
            "markdown_report_path": self.markdown_report_path,
            "notes": list(self.notes),
        }


def build_reasoner_symbol_atlas_final_status(
    options: ProjectSymbolAtlasFinalStatusOptions,
) -> ProjectSymbolAtlasFinalStatusResult:
    """Build a final status report for the Project Symbol Atlas series."""
    root = Path(options.project_root).resolve()
    evidence_paths = resolve_project_analysis_evidence_paths(root)
    canonical_evidence_dir = Path(evidence_paths.canonical_evidence_dir)
    legacy_evidence_dir = Path(evidence_paths.legacy_evidence_dir)

    expected_source_files = _resolve_product_package_placeholders(root, EXPECTED_SOURCE_FILES)
    missing_sources = _missing_relative_paths(root, expected_source_files)
    missing_gui = _missing_relative_paths(root, EXPECTED_GUI_FILES)
    missing_tests = _missing_relative_paths(root, EXPECTED_FOCUSED_TESTS)

    notes = [
        "Project Symbol Atlas uses project_analysis_evidence as canonical evidence path.",
        "Inactive reference evidence is optional and should not be required at runtime.",
        "Reference folders are memo/comment folders, not active project source.",
        "Atlas tools are read-only for analyzed project source.",
        "CLI and GUI integrations call validated backend analysis logic.",
    ]

    status = "complete"
    if missing_sources or missing_gui or missing_tests:
        status = "incomplete"
        notes.append("One or more expected implementation or focused-test files are missing.")

    result = ProjectSymbolAtlasFinalStatusResult(
        project_root=str(root),
        status=status,
        missing_source_files=missing_sources,
        missing_gui_files=missing_gui,
        missing_focused_tests=missing_tests,
        canonical_evidence_dir=str(canonical_evidence_dir),
        legacy_evidence_dir=str(legacy_evidence_dir),
        canonical_evidence_exists=canonical_evidence_dir.exists(),
        legacy_evidence_exists=legacy_evidence_dir.exists(),
        legacy_evidence_required=False,
        expected_cli_commands=list(EXPECTED_CLI_COMMANDS),
        expected_gui_commands=list(EXPECTED_GUI_COMMANDS),
        notes=notes,
    )

    if options.write_reports:
        result = write_reasoner_symbol_atlas_final_status(result, options.output_dir)
    return result


def write_reasoner_symbol_atlas_final_status(
    result: ProjectSymbolAtlasFinalStatusResult,
    output_dir: str | Path | None = None,
) -> ProjectSymbolAtlasFinalStatusResult:
    """Write JSON and Markdown final status reports."""
    root = Path(result.project_root)
    target_dir = Path(output_dir) if output_dir is not None else root / "workbench" / "_bundle_temp"
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "PA022_reasoner_symbol_atlas_final_status.json"
    markdown_path = target_dir / "PA022_reasoner_symbol_atlas_final_status.md"

    json_path.write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    markdown_path.write_text(_build_markdown(result), encoding="utf-8")

    data = result.to_dict()
    data["json_report_path"] = str(json_path)
    data["markdown_report_path"] = str(markdown_path)
    return ProjectSymbolAtlasFinalStatusResult(**data)


def _detect_product_package_relative_root(root: Path) -> str:
    """Return the relative package root that owns this module."""
    module_path = Path(__file__).resolve()
    try:
        relative_module = module_path.relative_to(root.resolve())
    except ValueError:
        return "kanda_reasoner_app"
    if not relative_module.parts:
        return "kanda_reasoner_app"
    return relative_module.parts[0]


def _resolve_product_package_placeholders(
    root: Path,
    relative_paths: list[str],
) -> list[str]:
    """Replace product-package placeholders with the active package root."""
    product_package = _detect_product_package_relative_root(root)
    return [
        relative_path.replace(PRODUCT_PACKAGE_PLACEHOLDER, product_package, 1)
        for relative_path in relative_paths
    ]


def _missing_relative_paths(root: Path, relative_paths: list[str]) -> list[str]:
    """Return relative paths that do not exist below root."""
    missing: list[str] = []
    for relative_path in relative_paths:
        path = root / Path(*relative_path.split("/"))
        if not path.exists():
            missing.append(relative_path)
    return missing


def _build_markdown(result: ProjectSymbolAtlasFinalStatusResult) -> str:
    """Build a Markdown final status report."""
    lines = [
        "# PA022 Project Symbol Atlas Final Status",
        "",
        f"Status: {result.status}",
        f"Project root: {result.project_root}",
        "",
        "## Evidence paths",
        "",
        f"Canonical evidence dir: {result.canonical_evidence_dir}",
        f"Canonical evidence exists: {result.canonical_evidence_exists}",
        f"Legacy evidence dir: {result.legacy_evidence_dir}",
        f"Legacy evidence exists: {result.legacy_evidence_exists}",
        f"Legacy evidence required: {result.legacy_evidence_required}",
        "",
        "## Missing source files",
        "",
    ]
    lines.extend(_markdown_list_or_none(result.missing_source_files))
    lines.extend(["", "## Missing GUI files", ""])
    lines.extend(_markdown_list_or_none(result.missing_gui_files))
    lines.extend(["", "## Missing focused tests", ""])
    lines.extend(_markdown_list_or_none(result.missing_focused_tests))
    lines.extend(["", "## Expected CLI commands", ""])
    lines.extend(_markdown_list_or_none(result.expected_cli_commands))
    lines.extend(["", "## Expected GUI commands", ""])
    lines.extend(_markdown_list_or_none(result.expected_gui_commands))
    lines.extend(["", "## Notes", ""])
    lines.extend(_markdown_list_or_none(result.notes))
    lines.append("")
    return "\n".join(lines)


def _markdown_list_or_none(values: list[str]) -> list[str]:
    """Return Markdown bullet lines or a None marker."""
    if not values:
        return ["None"]
    return [f"- {value}" for value in values]


__all__ = [
    "EXPECTED_ADJACENT_PACKAGE_FILES",
    "EXPECTED_CLI_COMMANDS",
    "EXPECTED_FOCUSED_TESTS",
    "EXPECTED_GUI_COMMANDS",
    "EXPECTED_GUI_FILES",
    "EXPECTED_PROJECT_SYMBOL_ATLAS_FILES",
    "EXPECTED_SOURCE_FILES",
    "PRODUCT_PACKAGE_PLACEHOLDER",
    "ProjectSymbolAtlasFinalStatusOptions",
    "ProjectSymbolAtlasFinalStatusResult",
    "build_reasoner_symbol_atlas_final_status",
    "write_reasoner_symbol_atlas_final_status",
]
