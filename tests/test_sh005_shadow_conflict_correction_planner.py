from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.source_hygiene.shadow_planner as shadow_planner
from kanda_reasoner_app.source_hygiene.schemas import (
    SourceHygieneFinding,
    SourceHygieneReport,
)
from kanda_reasoner_app.source_hygiene.shadow_planner import (
    ShadowCorrectionPlanItem,
    build_shadow_conflict_plan,
    classify_shadow_finding,
    finding_to_plan_item,
)


def test_shadow_planner_public_contract_exports() -> None:
    expected = {
        "ShadowCorrectionPlanItem",
        "build_shadow_conflict_plan",
        "classify_shadow_finding",
        "finding_to_plan_item",
    }
    assert expected.issubset(set(shadow_planner.__all__))


def test_classifies_low_risk_facade_findings_as_mechanical() -> None:
    finding = SourceHygieneFinding(
        code="FACADE_WITHOUT_ALL",
        path="pkg/__init__.py",
        message="Facade imports public names but lacks __all__.",
        severity="warning",
        confidence="medium",
    )
    item = finding_to_plan_item(finding)
    assert isinstance(item, ShadowCorrectionPlanItem)
    assert item.classification == "safe_mechanical_fix"
    assert "__all__" in item.proposed_action
    assert any("facade" in test.lower() for test in item.required_tests)


def test_duplicate_public_symbols_require_owner_decision() -> None:
    finding = SourceHygieneFinding(
        code="DUPLICATE_PUBLIC_SYMBOL",
        path="<project>",
        message="Duplicate symbol.",
        severity="warning",
        confidence="medium",
        evidence={"symbol": "build_report", "owners": ["a.py", "b.py"]},
    )
    assert classify_shadow_finding(finding) == "requires_owner_decision"
    item = finding_to_plan_item(finding)
    assert "canonical owner" in item.proposed_action
    assert any("Search callers" in test for test in item.required_tests)


def test_build_shadow_conflict_plan_is_read_only_report() -> None:
    audit = SourceHygieneReport(
        project_root="E:\\developer_tools",
        report_type="shadow_conflict_audit",
        summary="audit",
        findings=(
            SourceHygieneFinding(
                code="WILDCARD_IMPORT_IN_FACADE",
                path="pkg/__init__.py",
                message="Wildcard import.",
                severity="warning",
                confidence="high",
            ),
            SourceHygieneFinding(
                code="BEHAVIOR_DEFINED_IN_FACADE",
                path="pkg/__init__.py",
                message="Behavior defined.",
                severity="warning",
                confidence="high",
                evidence={"symbol": "configure"},
            ),
        ),
    )
    plan = build_shadow_conflict_plan(audit)
    data = plan.to_dict()
    assert data["report_type"] == "shadow_conflict_plan"
    assert data["finding_count"] == 2
    assert "safe_mechanical_fix=1" in data["summary"]
    assert "requires_compatibility_facade=1" in data["summary"]
    first = data["findings"][0]
    assert first["code"] == "SHADOW_CORRECTION_PLAN_ITEM"
    assert first["evidence"]["classification"] == "safe_mechanical_fix"


if __name__ == "__main__":
    test_shadow_planner_public_contract_exports()
    test_classifies_low_risk_facade_findings_as_mechanical()
    test_duplicate_public_symbols_require_owner_decision()
    test_build_shadow_conflict_plan_is_read_only_report()
    print("SH005 shadow conflict correction planner tests passed.")
