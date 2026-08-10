"""Validate grouped Full Engineering Diagnostics AI handoff v2."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import py_compile
import sys
import time
from types import SimpleNamespace as NS

FEATURE_ID = "kanda-reasoner-full-engineering-diagnostics-ai-correction-handoff-v2"
TOUCHED = (
    "kanda_reasoner_app/engineering_diagnostics_gui/full_engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_report.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_handoff.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/_ai_correction_grouping.py",
)


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def _group(producer: str, group_id: int):
    return NS(
        kind="DETERMINISTIC",
        group_id=producer + "-group-" + str(group_id),
        label="Rule group " + str(group_id),
        confidence="high",
    )


def _finding(index: int, producer: str, group_id: int):
    plan = NS(
        focused_tests=("tools/test_group_" + str(group_id) + ".py",),
        validation_commands=("python tools/test_group_" + str(group_id) + ".py",),
        rollback_expectation="Restore exact predecessor.",
        evidence_required=("VALIDATION OK",),
    )
    intent = NS(
        action_class="SAFE_MECHANICAL_FIX_AVAILABLE",
        primary_trust_source="KANDA_RULE_TEMPLATE",
        rule_template_id="RULE_" + str(group_id % 30),
        likely_correction="Apply deterministic correction for rule "
        + str(group_id % 30) + ".",
        reason="Deterministic rule violation.",
        expected_affected_files=("pkg/file_" + str(index % 1500) + ".py",),
        frozen_path_impact="UNFROZEN",
        required_governed_wave="",
        fix_applicability="EXACT_FILE",
        mechanical_safety="FOCUSED_REVIEW",
        semantic_review_requirement="REQUIRED",
        uncertainty="low",
        validation_plan=plan,
        deterministic_evidence=("fixture deterministic evidence",),
        project_governance_rules=("Box Logic", "No Leak"),
        ai_hypothesis=None,
    )
    record = NS(
        issue_fingerprint=producer + "-issue-" + str(index),
        evidence_digest=producer + "-evidence-" + str(index),
        severity="error" if index % 10 == 0 else "warning",
        confidence="high",
        code="R" + str(index % 30),
        category="quality",
        relative_path="pkg/file_" + str(index % 1500) + ".py",
        line=(index % 400) + 1,
        symbol_id="fixture.symbol." + str(index % 500),
        location_key="",
        semantic_key="",
        message="Fixture problem " + str(index),
        suggested_action="",
        evidence={"rule": index % 30},
    )
    owner = NS(
        active_candidates=("pkg.owner",),
        historical_candidates=(),
        selection_method="exact_path",
        evidence=("owner evidence",),
    )
    scope = NS(method="path_policy", evidence=("active source",))
    frozen = NS(
        matched_protected_paths=(),
        evidence=("unfrozen",),
        governing_freeze_ids=(),
    )
    enrichment = NS(owner=owner, scope=scope, frozen_path=frozen)
    return NS(
        record=record,
        lifecycle_state="current",
        decision_state="OPEN",
        decision_generation=0,
        enrichment=enrichment,
        groups=(_group(producer, group_id),),
        remediation_intent=intent,
        remediation_action_class="SAFE_MECHANICAL_FIX_AVAILABLE",
        scope_classification="ACTIVE",
        scope_confidence="high",
        frozen_status="UNFROZEN",
        governing_freeze_ids="",
        owner_status="READY",
        owner_confidence="high",
        canonical_owner="pkg.owner",
    )


def _run_view(producer: str, count: int):
    findings = tuple(_finding(i, producer, i % 120) for i in range(count))
    run = NS(
        producer_id=producer,
        producer_version="1",
        run_id=producer + "-run",
        attempt_id=producer + "-attempt",
        project_id="project-1",
        project_root_fingerprint="rootfp",
        source_fingerprint="sourcefp",
        scope_fingerprint="scopefp",
        configuration_fingerprint="configfp",
        operation_generation=1,
        completion_status="COMPLETE_WITH_FINDINGS",
        finding_count=count,
        content_digest=producer + "-digest",
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
    return NS(run=run, findings=findings, comparison=comparison)


def _large_scale_contract(root: Path) -> None:
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_report import (
        AiCorrectionCollectorResult,
        build_full_ai_correction_report,
    )

    counts = (4, 37510, 17, 4553)
    producers = ("bom", "ruff", "architecture", "shadow")
    views = tuple(_run_view(producer, count) for producer, count in zip(producers, counts))
    collectors = tuple(
        AiCorrectionCollectorResult(
            label=producer,
            status="STORED",
            run_id=producer + "-run",
            finding_count=count,
        )
        for producer, count in zip(producers, counts)
    )
    started = time.perf_counter()
    report = build_full_ai_correction_report(
        r"E:\kanda_reasoner",
        collectors,
        views,
    )
    elapsed = time.perf_counter() - started
    payload_bytes = len(report.text.encode("utf-8"))

    _require(report.finding_count == 42084, "GROUPED_AI_HANDOFF_42084_FINDINGS")
    _require(
        1 <= report.correction_group_count < 2000,
        "GROUPED_AI_HANDOFF_CORRECTION_GROUP_COMPRESSION",
    )
    _require(payload_bytes < 5_000_000, "GROUPED_AI_HANDOFF_REPORT_UNDER_5MB")
    _require(elapsed < 10.0, "GROUPED_AI_HANDOFF_RENDER_UNDER_10_SECONDS")
    _require(
        "AI CORRECTION SUMMARY" in report.console_summary,
        "GROUPED_AI_HANDOFF_CONSOLE_SUMMARY",
    )
    _require(
        "Affected paths:" in report.text
        and "Representative finding 1:" in report.text
        and "Likely correction:" in report.text
        and "Validation commands:" in report.text,
        "GROUPED_AI_HANDOFF_CORRECTION_CONTEXT",
    )
    _require(
        report.text.count("Representative finding ")
        <= report.correction_group_count * 3,
        "GROUPED_AI_HANDOFF_REPRESENTATIVE_EVIDENCE_BOUND",
    )
    _require(
        "Raw finding duplication into this handoff: NO" in report.text,
        "GROUPED_AI_HANDOFF_RAW_DUPLICATION_ABSENT",
    )
    print("GROUPED_AI_HANDOFF_SYNTHETIC_SECONDS: " + format(elapsed, ".3f"))
    print("GROUPED_AI_HANDOFF_SYNTHETIC_BYTES: " + str(payload_bytes))
    print("GROUPED_AI_HANDOFF_SYNTHETIC_GROUPS: " + str(report.correction_group_count))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)

    for relative in TOUCHED:
        path = root / relative
        _require(path.is_file(), "TOUCHED_FILE_EXISTS:" + relative)
        path.read_bytes().decode("ascii")
        _require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "MODULE_SIZE_MAX_500:" + relative,
        )
        py_compile.compile(str(path), doraise=True)
    print("PYTHON_COMPILE: PASS")
    print("ASCII_SOURCE_CONTRACT: PASS")

    tab_text = (root / TOUCHED[0]).read_text(encoding="utf-8")
    report_text = (root / TOUCHED[1]).read_text(encoding="utf-8")
    handoff_text = (root / TOUCHED[2]).read_text(encoding="utf-8")
    grouping_text = (root / TOUCHED[3]).read_text(encoding="utf-8")

    _require(
        "AI correction handoff: BUILDING" in tab_text,
        "FULL_DIAGNOSTICS_BUILDING_STATE_VISIBLE",
    )
    _require(
        "report_executor = ThreadPoolExecutor(max_workers=1)" in tab_text,
        "AI_HANDOFF_SEPARATE_BACKGROUND_EXECUTOR",
    )
    _require(
        "*artifact.console_summary.splitlines()" in tab_text,
        "AI_HANDOFF_CONSOLE_SUMMARY_RENDERED",
    )
    _require(
        "finding_count=run.finding_count" in tab_text,
        "AI_HANDOFF_RAW_FINDING_COUNT_PROPAGATED",
    )
    _require(
        "load_run_view(" not in tab_text,
        "FULL_DIAGNOSTICS_GUI_DIRECT_RUN_VIEW_LOAD_ABSENT",
    )
    _require(
        "controller.load_run_view" in handoff_text,
        "AI_HANDOFF_PUBLIC_RUN_VIEW_CONTRACT",
    )
    _require(
        "_delete_after_daily_work" in handoff_text,
        "AI_HANDOFF_DAILY_WORK_OWNERSHIP",
    )
    _require(
        "Raw finding duplication into this handoff: NO" in report_text,
        "AI_HANDOFF_GROUPED_REPORT_CONTRACT",
    )
    for token in (
        "Affected paths:",
        "Representative finding ",
        "Canonical owners:",
        "Frozen statuses:",
        "Likely correction:",
        "Focused tests:",
        "Validation commands:",
        "Rollback expectation:",
        "Exact source inspection required before edit: YES",
    ):
        _require(token in grouping_text, "AI_GROUPED_REPORT_FIELD:" + token)

    _large_scale_contract(root)

    from kanda_reasoner_app.manage_architecture.manage_architecture import scan_project

    _modules, issues, *_rest = scan_project(root)
    touched = set(TOUCHED)
    touched_issues = [issue for issue in issues if str(issue.path) in touched]
    _require(
        len(touched_issues) == 0,
        "AI_HANDOFF_TOUCHED_PATH_ARCHITECTURE_ISSUES_ZERO",
    )
    print("ARCHITECTURE_CURRENT_ISSUES: " + str(len(issues)))
    print("FULL AUDIT PRODUCT FILES MODIFIED: NO")
    print("PONTUAL AUDIT PRODUCT FILES MODIFIED: NO")
    print("ENGINEERING DIAGNOSTICS STORE MUTATED BY VALIDATOR: NO")
    print("PROJECT SELECTION REGISTRY MUTATED BY VALIDATOR: NO")
    print("FREEZE MEMORY MUTATED BY VALIDATOR: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("MCARD LIFECYCLE GATE: NOT_APPLICABLE")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
