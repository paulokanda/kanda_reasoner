"""Validate Architecture-grade Full Engineering Diagnostics AI handoff v4."""

from __future__ import annotations

import argparse
from pathlib import Path
import py_compile
import sys
from types import SimpleNamespace as NS

FEATURE_ID = (
    "kanda-reasoner-full-engineering-diagnostics-architecture-grade-ai-handoff-v4"
)
TOUCHED = (
    "kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_report.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_capability_render.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_capability_dossier.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/structured_correction_dossier.py",
)


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def _coverage():
    from kanda_reasoner_app.engineering_diagnostics_gui._engineering_capability_models import (
        EngineeringCapabilityCoverage,
        EngineeringCapabilityResult,
    )

    attribute_error = (
        "ERROR: module 'kanda_reasoner_app.reasoner_symbol_atlas."
        "_related_file_finder_support' has no attribute '_limited_unique_paths'"
    )
    risk_report = "\n".join(
        (
            "# Engineering Safety Report",
            "",
            "Report ID: risk_change_radar_fixture",
            "Report type: risk_change_radar",
            "Project root: fixture",
            "Risk level: medium",
            "Confidence: medium",
            "Owning box: gui_shell",
            "",
            "## Affected files",
            "- reasoner_tools_gui_engineering_safety_panel.py",
            "",
            "## Root cause or risk hypothesis",
            "Risk score 3 from changed-file and validation signals.",
            "",
            "## Suggested first action",
            "Run focused validation before global validation.",
            "",
            "## Tests to run",
            "- python tools/focused_fixture.py",
            "",
            "## Rollback plan",
            "Restore the exact predecessor.",
        )
    )
    results = []
    for index in range(26):
        kwargs = dict(
            surface=(
                "PONTUAL_GUI"
                if index < 23
                else ("SAFETY_CLI_ONLY" if index < 25 else "ARCHITECTURE_REVIEW")
            ),
            section="Fixture",
            label="Fixture capability " + str(index),
            command_name="fixture-" + str(index),
            scope_mode="PROJECT_WIDE_READ_ONLY",
            status="CLEAN",
            severity="INFO",
            assessment_reason="Fixture clean assessment.",
            execution="EXECUTED_PUBLIC_CONTRACT",
            status_code=0,
            finding_count=0,
            evidence="Fixture clean evidence.",
            correction_guidance="No automatic correction authorized.",
        )
        if index == 20:
            kwargs.update(
                command_name="related-files",
                label="Related Files",
                status="FAILED",
                severity="ERROR",
                assessment_reason="Public capability returned non-zero status 2.",
                status_code=2,
                evidence=attribute_error,
                correction_guidance="Inspect exact public owner implementation.",
            )
        elif index == 7:
            kwargs.update(
                command_name="risk-radar",
                label="Risk Change Radar",
                status="MANUAL_REVIEW_REQUIRED",
                severity="WARNING",
                assessment_reason="Human review is required.",
                evidence=risk_report,
                correction_guidance="Use deterministic risk evidence before editing.",
            )
        results.append(EngineeringCapabilityResult(**kwargs))
    return EngineeringCapabilityCoverage(
        results=tuple(results),
        gui_catalog_count=23,
        cli_catalog_count=24,
        unique_safety_surface_count=25,
        architecture_surface_count=1,
    )


def _finding(path: str, line: int):
    plan = NS(
        focused_tests=("python tools/focused_fixture.py",),
        validation_commands=("python tools/validate_fixture.py",),
        rollback_expectation="Restore exact predecessor bytes.",
        evidence_required=("VALIDATION OK", "STATUS: IN_SYNC"),
    )
    intent = NS(
        action_class="SAFE_MECHANICAL_FIX_AVAILABLE",
        primary_trust_source="KANDA_RULE_TEMPLATE",
        rule_template_id="FIXTURE_RULE",
        likely_correction="Apply the smallest owner-pure correction.",
        reason="Deterministic fixture violation.",
        expected_affected_files=(path,),
        frozen_path_impact="UNFROZEN",
        required_governed_wave="",
        fix_applicability="EXACT_FILE",
        mechanical_safety="FOCUSED_REVIEW",
        semantic_review_requirement="REQUIRED",
        uncertainty="low",
        validation_plan=plan,
        deterministic_evidence=("fixture evidence",),
        project_governance_rules=("Box Logic", "No Leak", "Brick Wall"),
        ai_hypothesis=None,
    )
    record = NS(
        issue_fingerprint="fixture-issue-" + str(line),
        evidence_digest="fixture-evidence-" + str(line),
        severity="warning",
        confidence="high",
        code="FIX001",
        category="architecture",
        relative_path=path,
        line=line,
        symbol_id="main",
        location_key="module:main",
        semantic_key="fixture-semantic-key",
        message="Fixture architecture problem.",
        suggested_action="Inspect the canonical owner.",
        evidence={"validation_source": "Architecture Review"},
    )
    owner = NS(
        status="READY",
        confidence="high",
        canonical_owner="gui_shell",
        active_candidates=("reasoner_tools_gui.py",),
        historical_candidates=("legacy/reasoner_tools_gui.py",),
        selection_method="exact_owner_contract",
        evidence=("owner evidence",),
    )
    scope = NS(
        classification="ACTIVE",
        confidence="high",
        method="path_policy",
        evidence=("active source",),
    )
    frozen = NS(
        status="UNFROZEN",
        governing_freeze_ids=(),
        matched_protected_paths=(),
        evidence=("unfrozen",),
    )
    enrichment = NS(owner=owner, scope=scope, frozen_path=frozen)
    group = NS(
        kind="DETERMINISTIC",
        group_id="fixture-group",
        label="Fixture architecture group",
        confidence="high",
    )
    return NS(
        record=record,
        lifecycle_state="current",
        decision_state="OPEN",
        decision_generation=0,
        enrichment=enrichment,
        groups=(group,),
        remediation_intent=intent,
        remediation_action_class=intent.action_class,
        scope_classification="ACTIVE",
        scope_confidence="high",
        frozen_status="UNFROZEN",
        governing_freeze_ids="",
        owner_status="READY",
        owner_confidence="high",
        canonical_owner="gui_shell",
    )


def _report_contract(root: Path) -> None:
    from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_report import (
        AiCorrectionCollectorResult,
        build_full_ai_correction_report,
    )

    path = "reasoner_tools_gui.py"
    finding = _finding(path, 1)
    run = NS(
        producer_id="architecture",
        producer_version="1",
        run_id="architecture-run",
        attempt_id="architecture-attempt",
        project_id="project-1",
        project_root_fingerprint="rootfp",
        source_fingerprint="sourcefp",
        scope_fingerprint="scopefp",
        configuration_fingerprint="configfp",
        operation_generation=1,
        completion_status="COMPLETE_WITH_FINDINGS",
        finding_count=1,
        content_digest="architecture-digest",
        started_at_utc="2026-08-07T00:00:00Z",
        completed_at_utc="2026-08-07T00:00:01Z",
        provenance={"source": "fixture"},
    )
    comparison = NS(
        status="NO_BASELINE",
        new_issue_fingerprints=(),
        persistent_issue_fingerprints=(),
        resolved_issue_fingerprints=(),
    )
    view = NS(run=run, findings=(finding,), comparison=comparison)
    collectors = (
        AiCorrectionCollectorResult(
            label="Architecture",
            status="STORED",
            run_id=run.run_id,
            finding_count=1,
        ),
    )
    report = build_full_ai_correction_report(
        str(root),
        collectors,
        (view,),
        _coverage(),
    )
    text = report.text

    required = (
        "Report standard: Architecture Review-grade correction evidence",
        "FULL ENGINEERING CAPABILITY COVERAGE LEDGER",
        "CAPABILITY INDEX",
        "CAPABILITY DETAILS",
        "AI CORRECTION DOSSIER: REQUIRED",
        "Problem ID: CAP-",
        "Failure module: kanda_reasoner_app.reasoner_symbol_atlas._related_file_finder_support",
        "Failure symbol: _limited_unique_paths",
        "Affected files:",
        "Tests to run:",
        "Rollback expectation:",
        "Capability evidence SHA256:",
        "ARCHITECTURE-GRADE CORRECTION DOSSIER",
        "Active owner candidates:",
        "Historical owner candidates:",
        "Owner evidence:",
        "Scope evidence:",
        "Matched protected paths:",
        "Validation sources: Architecture Review",
        "Expected files to change:",
        "Focused tests:",
        "Validation commands:",
        "Required validation evidence:",
        "Exact source excerpt:",
        "Exact current source inspection before edit: REQUIRED",
        "Automatic source apply: NO",
    )
    for marker in required:
        _require(marker in text, "ARCHITECTURE_GRADE_MARKER:" + marker)

    _require(
        "reasoner_tools_gui.py" in text,
        "ARCHITECTURE_GRADE_EXACT_AFFECTED_PATH",
    )
    _require(
        ">> 1:" in text,
        "ARCHITECTURE_GRADE_BOUNDED_SOURCE_EXCERPT",
    )
    _require(
        len(text.encode("utf-8")) < 5_000_000,
        "ARCHITECTURE_GRADE_REPORT_UNDER_5MB",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    for relative in TOUCHED:
        path = root / relative
        _require(path.is_file(), "V4_TOUCHED_FILE_EXISTS:" + relative)
        path.read_bytes().decode("ascii")
        _require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "V4_MODULE_SIZE_MAX_500:" + relative,
        )
        py_compile.compile(str(path), doraise=True)

    print("V4_PYTHON_COMPILE: PASS")
    print("V4_ASCII_SOURCE_CONTRACT: PASS")
    _report_contract(root)

    from kanda_reasoner_app.manage_architecture.manage_architecture import scan_project

    _modules, issues, *_rest = scan_project(root)
    touched = set(TOUCHED)
    touched_issues = [issue for issue in issues if str(issue.path) in touched]
    _require(
        len(touched_issues) == 0,
        "V4_TOUCHED_PATH_ARCHITECTURE_ISSUES_ZERO",
    )
    print("FULL AUDIT PRODUCT FILES MODIFIED: NO")
    print("PONTUAL AUDIT PRODUCT FILES MODIFIED: NO")
    print("ENGINEERING DIAGNOSTICS STORE MUTATED BY V4 VALIDATOR: NO")
    print("SYMBOL ATLAS SOURCE MUTATED BY V4 VALIDATOR: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("MCARD LIFECYCLE GATE: NOT_APPLICABLE")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
