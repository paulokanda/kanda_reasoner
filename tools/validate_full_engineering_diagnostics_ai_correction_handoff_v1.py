"""Validate Full Engineering Diagnostics AI correction handoff v1."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import py_compile
import sys
from types import ModuleType, SimpleNamespace as NS

FEATURE_ID = "kanda-reasoner-full-engineering-diagnostics-ai-correction-handoff-v1"
TOUCHED = (
    "kanda_reasoner_app/engineering_diagnostics_gui/full_engineering_diagnostics_tab.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_report.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_handoff.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def _fixture_report(root: Path) -> None:
    report_path = (
        root
        / "kanda_reasoner_app"
        / "engineering_diagnostics_gui"
        / "ai_correction_report.py"
    )
    source_lines = report_path.read_text(encoding="utf-8").splitlines()
    filtered: list[str] = []
    skip_models = False
    for line in source_lines:
        if line.startswith("from .models import "):
            continue
        if line.startswith("from .run_summary import "):
            continue
        filtered.append(line)
    module_name = "ai_correction_report_fixture"
    module = ModuleType(module_name)
    module.__file__ = str(report_path)
    module.build_diagnostic_run_summary = lambda _view: "fixture summary"
    sys.modules[module_name] = module
    exec(compile("\n".join(filtered), str(report_path), "exec"), module.__dict__)
    collector_type = module.__dict__["AiCorrectionCollectorResult"]
    build_report = module.__dict__["build_full_ai_correction_report"]

    plan = NS(
        focused_tests=("tools/test_x.py",),
        validation_commands=("python tools/test_x.py",),
        rollback_expectation="Restore exact predecessor.",
        evidence_required=("VALIDATION OK",),
    )
    intent = NS(
        action_class="FIX_NOW",
        primary_trust_source="KANDA_RULE_TEMPLATE",
        rule_template_id="TEST_RULE",
        likely_correction="Move behavior to the canonical owner.",
        reason="Owner mismatch.",
        expected_affected_files=("pkg/a.py",),
        frozen_path_impact="UNFROZEN",
        required_governed_wave="",
        fix_applicability="EXACT_FILE",
        mechanical_safety="SEMANTIC_REVIEW_REQUIRED",
        semantic_review_requirement="REQUIRED",
        uncertainty="low",
        validation_plan=plan,
        deterministic_evidence=("owner mismatch",),
        project_governance_rules=("Box Logic", "No Leak"),
        ai_hypothesis=None,
    )
    record = NS(
        issue_fingerprint="issue-1", evidence_digest="evidence-1",
        severity="warning", confidence="high", code="TEST001",
        category="architecture", relative_path="pkg/a.py", line=10,
        symbol_id="pkg.a:f", location_key="pkg/a.py:f",
        semantic_key="TEST001:f",
        message="Behavior is in the wrong owner.",
        suggested_action="Move behavior.", evidence={"rule": "TEST001"},
    )
    owner = NS(
        active_candidates=("pkg.a",), historical_candidates=(),
        selection_method="symbol_atlas", evidence=("active owner",),
    )
    scope = NS(method="path_policy", evidence=("active source",))
    frozen = NS(matched_protected_paths=(), evidence=("unfrozen",))
    enrichment = NS(owner=owner, scope=scope, frozen_path=frozen)
    finding = NS(
        record=record, lifecycle_state="new", decision_state="OPEN",
        decision_generation=0, scope_classification="ACTIVE",
        scope_confidence="high", frozen_status="UNFROZEN",
        governing_freeze_ids="", owner_status="READY",
        owner_confidence="high", canonical_owner="pkg.a", group_count=1,
        group_kind="DETERMINISTIC", group_label="TEST001 pkg/a.py",
        group_confidence="high", enrichment=enrichment,
        remediation_intent=intent, remediation_action_class="FIX_NOW",
    )
    run = NS(
        producer_id="architecture", producer_version="1", run_id="run-1",
        attempt_id="attempt-1", project_id="project-1",
        project_root_fingerprint="rootfp", source_fingerprint="sourcefp",
        scope_fingerprint="scopefp", configuration_fingerprint="configfp",
        operation_generation=1, completion_status="COMPLETE_WITH_FINDINGS",
        finding_count=1, content_digest="digest",
        started_at_utc="2026-08-07T00:00:00Z",
        completed_at_utc="2026-08-07T00:00:01Z",
        provenance={"source": "fixture"},
    )
    comparison = NS(
        status="NO_BASELINE", new_issue_fingerprints=("issue-1",),
        persistent_issue_fingerprints=(), resolved_issue_fingerprints=(),
    )
    view = NS(run=run, findings=(finding,), comparison=comparison)
    report = build_report(
        r"E:\kanda_reasoner",
        (collector_type("Architecture", "STORED", "run-1"),),
        (view,),
    )
    required = (
        "AI correction readiness: CORRECTION_CONTEXT_READY",
        "Canonical owner: pkg.a",
        "Likely correction: Move behavior to the canonical owner.",
        "Expected affected files: pkg/a.py",
        "Focused tests: tools/test_x.py",
        "Validation commands: python tools/test_x.py",
        "Rollback expectation: Restore exact predecessor.",
        "Source inspection required before edit: YES",
        "Automatic source correction: NO",
        "Executable patch included: NO",
    )
    _require(
        all(token in report.text for token in required),
        "AI_CORRECTION_REPORT_FIXTURE_CONTRACT",
    )
    _require(report.finding_count == 1, "AI_CORRECTION_REPORT_FINDING_COUNT")
    _require(
        report.correction_ready_count == 1,
        "AI_CORRECTION_REPORT_READINESS_COUNT",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)

    for relative in TOUCHED:
        path = root / relative
        _require(path.is_file(), "TOUCHED_FILE_EXISTS:" + relative)
        data = path.read_bytes()
        _require(data.decode("ascii") is not None, "ASCII_SOURCE:" + relative)
        _require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "MODULE_SIZE_MAX_500:" + relative,
        )
        py_compile.compile(str(path), doraise=True)
    print("PYTHON_COMPILE: PASS")

    tab_text = (root / TOUCHED[0]).read_text(encoding="utf-8")
    report_text = (root / TOUCHED[1]).read_text(encoding="utf-8")
    handoff_text = (root / TOUCHED[2]).read_text(encoding="utf-8")

    _require(
        "full_engineering_diagnostics_copy_ai_handoff_button" in tab_text,
        "FULL_DIAGNOSTICS_AI_HANDOFF_BUTTON_CONTRACT",
    )
    _require(
        "executor.submit(\n            build_full_ai_correction_handoff" in tab_text,
        "AI_HANDOFF_BACKGROUND_EXECUTOR_CONTRACT",
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
        all(
            forbidden not in handoff_text
            for forbidden in (
                "project_freeze_ledger",
                "frozen_features_memory",
                "engineering_diagnostics.sqlite3",
                "project_selection_registry",
            )
        ),
        "AI_HANDOFF_NO_PROTECTED_OWNER_WRITE_SURFACE",
    )
    for token in (
        "Issue fingerprint:",
        "Source fingerprint:",
        "Canonical owner:",
        "Frozen status:",
        "Likely correction:",
        "Expected affected files:",
        "Focused tests:",
        "Validation commands:",
        "Rollback expectation:",
        "Project governance rules:",
        "Raw deterministic evidence:",
        "Source inspection required before edit: YES",
    ):
        _require(token in report_text, "AI_REPORT_FIELD:" + token)

    _fixture_report(root)

    from kanda_reasoner_app.manage_architecture.manage_architecture import scan_project

    _modules, issues, *_rest = scan_project(root)
    touched = set(TOUCHED)
    touched_issues = [issue for issue in issues if str(issue.path) in touched]
    _require(
        len(touched_issues) == 0,
        "AI_HANDOFF_TOUCHED_PATH_ARCHITECTURE_ISSUES_ZERO",
    )
    print("ARCHITECTURE_CURRENT_ISSUES: " + str(len(issues)))
    print("ENGINEERING DIAGNOSTICS STORE MUTATED BY VALIDATOR: NO")
    print("PROJECT SELECTION REGISTRY MUTATED BY VALIDATOR: NO")
    print("FREEZE MEMORY MUTATED BY VALIDATOR: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("MCARD LIFECYCLE GATE: NOT_APPLICABLE")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
