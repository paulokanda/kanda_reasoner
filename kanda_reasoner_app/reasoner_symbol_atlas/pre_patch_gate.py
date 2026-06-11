"""Read-only pre-patch ownership gate for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .evidence_freshness import (
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT,
    ProjectSymbolAtlasEvidenceFreshnessOptions,
    check_reasoner_symbol_atlas_evidence_freshness,
)
from .implementation_responsibility_resolver import (
    PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY,
    ProjectSymbolAtlasImplementationResponsibilityOptions,
    resolve_reasoner_symbol_atlas_implementation_responsibility,
)
from .related_file_finder import (
    ProjectSymbolAtlasRelatedFileOptions,
    find_reasoner_symbol_atlas_related_files,
)
from .schemas import (
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)
from .shadow_report import (
    ProjectSymbolAtlasShadowReportOptions,
    collect_reasoner_symbol_atlas_shadow_findings,
)

PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH = "safe_to_patch"
PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_WRONG_TARGET_FILE = "wrong_target_file"
PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_DUPLICATE_SYMBOL_RISK = "duplicate_symbol_risk"
PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_FACADE_PATCH_RISK = "facade_patch_risk"
PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_MISSING_TEST_PROTECTION = "missing_test_protection"
PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_EVIDENCE_STALE = "evidence_stale"
PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_DUPLICATE_SYMBOL_RISK",
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_EVIDENCE_STALE",
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_FACADE_PATCH_RISK",
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_MISSING_TEST_PROTECTION",
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_NEEDS_OWNER_REVIEW",
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH",
    "PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_WRONG_TARGET_FILE",
    "ProjectSymbolAtlasPrePatchGateDecision",
    "ProjectSymbolAtlasPrePatchGateOptions",
    "build_reasoner_symbol_atlas_pre_patch_gate_report",
    "run_reasoner_symbol_atlas_pre_patch_gate",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasPrePatchGateOptions:
    """Options for the read-only pre-patch ownership gate."""

    project_root: str
    task_description: str = ""
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = False
    include_workbench: bool = False
    include_private: bool = False
    require_test_protection: bool = False
    fail_on_stale_evidence: bool = False

    def to_responsibility_options(self) -> ProjectSymbolAtlasImplementationResponsibilityOptions:
        """Return compatible implementation responsibility options."""

        return ProjectSymbolAtlasImplementationResponsibilityOptions(
            project_root=self.project_root,
            task_description=self.task_description,
            target_path=self.target_path,
            symbol_name=self.symbol_name,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_related_file_options(self) -> ProjectSymbolAtlasRelatedFileOptions:
        """Return compatible related-file finder options."""

        return ProjectSymbolAtlasRelatedFileOptions(
            project_root=self.project_root,
            target_path=self.target_path,
            symbol_name=self.symbol_name,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=True,
            include_private=self.include_private,
            include_evidence_files=True,
        )

    def to_freshness_options(self) -> ProjectSymbolAtlasEvidenceFreshnessOptions:
        """Return compatible evidence freshness options."""

        return ProjectSymbolAtlasEvidenceFreshnessOptions(
            project_root=self.project_root,
            json_path=self.json_path,
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "task_description": normalize_project_atlas_text(self.task_description),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "include_private": bool(self.include_private),
            "require_test_protection": bool(self.require_test_protection),
            "fail_on_stale_evidence": bool(self.fail_on_stale_evidence),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasPrePatchGateDecision:
    """Decision output for the pre-patch ownership gate."""

    project_root: str
    task_description: str = ""
    target_path: str = ""
    symbol_name: str = ""
    status: str = PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_INSUFFICIENT_EVIDENCE
    safe_to_patch: bool = False
    primary_edit_target: str = ""
    secondary_helper_targets: tuple[str, ...] = field(default_factory=tuple)
    files_not_to_touch: tuple[str, ...] = field(default_factory=tuple)
    related_files: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)
    duplicate_symbol_risk: bool = False
    facade_patch_risk: bool = False
    wrong_target_file: bool = False
    missing_test_protection: bool = False
    evidence_stale: bool = False
    needs_owner_review: bool = False
    evidence_status: str = ""
    confidence: str = "low"
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "task_description": normalize_project_atlas_text(self.task_description),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "status": normalize_project_atlas_text(self.status),
            "safe_to_patch": bool(self.safe_to_patch),
            "primary_edit_target": self.primary_edit_target,
            "secondary_helper_targets": list(self.secondary_helper_targets),
            "files_not_to_touch": list(self.files_not_to_touch),
            "related_files": list(self.related_files),
            "tests_to_run": list(self.tests_to_run),
            "duplicate_symbol_risk": bool(self.duplicate_symbol_risk),
            "facade_patch_risk": bool(self.facade_patch_risk),
            "wrong_target_file": bool(self.wrong_target_file),
            "missing_test_protection": bool(self.missing_test_protection),
            "evidence_stale": bool(self.evidence_stale),
            "needs_owner_review": bool(self.needs_owner_review),
            "evidence_status": normalize_project_atlas_text(self.evidence_status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "reasons": list(self.reasons),
        }


def run_reasoner_symbol_atlas_pre_patch_gate(
    options: ProjectSymbolAtlasPrePatchGateOptions,
) -> ProjectSymbolAtlasPrePatchGateDecision:
    """Run a read-only pre-patch ownership gate.

    The gate never edits source files and never imports analyzed project modules.
    """

    project_root = str(Path(options.project_root).expanduser().resolve(strict=False))
    responsibility = resolve_reasoner_symbol_atlas_implementation_responsibility(
        options.to_responsibility_options()
    )
    related = find_reasoner_symbol_atlas_related_files(options.to_related_file_options())
    freshness = check_reasoner_symbol_atlas_evidence_freshness(options.to_freshness_options())
    duplicate_findings = _matching_duplicate_findings(options)

    duplicate_symbol_risk = bool(duplicate_findings)
    facade_patch_risk = bool(responsibility.facade_patch_risk)
    wrong_target_file = _wrong_target_file(options.target_path, responsibility.primary_edit_target)
    evidence_stale = _evidence_is_stale(freshness.status, options.fail_on_stale_evidence)
    missing_test_protection = _missing_test_protection(options, related.test_files)
    needs_owner_review = bool(
        responsibility.needs_owner_review
        or facade_patch_risk
        or wrong_target_file
        or duplicate_symbol_risk
        or evidence_stale
        or missing_test_protection
    )
    safe_to_patch = bool(
        responsibility.status == PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY
        and not needs_owner_review
    )
    status = _status_for_decision(
        safe_to_patch=safe_to_patch,
        wrong_target_file=wrong_target_file,
        facade_patch_risk=facade_patch_risk,
        duplicate_symbol_risk=duplicate_symbol_risk,
        missing_test_protection=missing_test_protection,
        evidence_stale=evidence_stale,
        needs_owner_review=needs_owner_review,
    )
    reasons = _reasons(
        responsibility_reasons=responsibility.reasons,
        related_evidence=related.evidence,
        duplicate_findings=duplicate_findings,
        evidence_status=freshness.status,
        duplicate_symbol_risk=duplicate_symbol_risk,
        facade_patch_risk=facade_patch_risk,
        wrong_target_file=wrong_target_file,
        missing_test_protection=missing_test_protection,
        evidence_stale=evidence_stale,
        safe_to_patch=safe_to_patch,
    )
    return ProjectSymbolAtlasPrePatchGateDecision(
        project_root=project_root,
        task_description=options.task_description,
        target_path=options.target_path,
        symbol_name=options.symbol_name,
        status=status,
        safe_to_patch=safe_to_patch,
        primary_edit_target=responsibility.primary_edit_target,
        secondary_helper_targets=responsibility.secondary_helper_targets,
        files_not_to_touch=responsibility.files_not_to_touch,
        related_files=related.related_files,
        tests_to_run=_merge_tests(responsibility.tests_to_run, related.tests_to_run),
        duplicate_symbol_risk=duplicate_symbol_risk,
        facade_patch_risk=facade_patch_risk,
        wrong_target_file=wrong_target_file,
        missing_test_protection=missing_test_protection,
        evidence_stale=evidence_stale,
        needs_owner_review=needs_owner_review,
        evidence_status=freshness.status,
        confidence="high" if safe_to_patch or needs_owner_review else "medium",
        reasons=reasons,
    )


def build_reasoner_symbol_atlas_pre_patch_gate_report(
    options: ProjectSymbolAtlasPrePatchGateOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for the pre-patch ownership gate."""

    decision = run_reasoner_symbol_atlas_pre_patch_gate(options)
    symbol = ProjectSymbol(
        name="pre_patch_ownership_gate",
        kind="unknown",
        module="reasoner_symbol_atlas.pre_patch_gate",
        path=decision.primary_edit_target,
        is_public=False,
        owner_role="unknown",
        evidence=decision.reasons,
    )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_summary(decision),
        symbols=(symbol,),
        input_sources=(
            "implementation_responsibility_resolver",
            "related_file_finder",
            "shadow_report",
            "evidence_freshness",
            "pre_patch_gate",
        ),
    )


def _matching_duplicate_findings(
    options: ProjectSymbolAtlasPrePatchGateOptions,
) -> tuple[ProjectSymbol, ...]:
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
    options: ProjectSymbolAtlasPrePatchGateOptions,
    related_test_files: tuple[str, ...],
) -> bool:
    if not options.require_test_protection:
        return False
    if not options.include_tests:
        return False
    return len(related_test_files) == 0


def _status_for_decision(
    safe_to_patch: bool,
    wrong_target_file: bool,
    facade_patch_risk: bool,
    duplicate_symbol_risk: bool,
    missing_test_protection: bool,
    evidence_stale: bool,
    needs_owner_review: bool,
) -> str:
    if safe_to_patch:
        return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH
    if wrong_target_file:
        return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_WRONG_TARGET_FILE
    if facade_patch_risk:
        return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_FACADE_PATCH_RISK
    if duplicate_symbol_risk:
        return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_DUPLICATE_SYMBOL_RISK
    if missing_test_protection:
        return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_MISSING_TEST_PROTECTION
    if evidence_stale:
        return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_EVIDENCE_STALE
    if needs_owner_review:
        return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_NEEDS_OWNER_REVIEW
    return PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_INSUFFICIENT_EVIDENCE


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


def _format_summary(decision: ProjectSymbolAtlasPrePatchGateDecision) -> str:
    return (
        "Pre-patch ownership gate status="
        + decision.status
        + "; safe_to_patch="
        + str(decision.safe_to_patch).lower()
        + "; primary_edit_target="
        + decision.primary_edit_target
    )
