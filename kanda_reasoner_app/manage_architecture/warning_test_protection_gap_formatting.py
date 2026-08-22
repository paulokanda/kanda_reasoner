# project-path: kanda_reasoner_app/manage_architecture/warning_test_protection_gap_formatting.py
"""Format TEST_PROTECTION_GAP specialist plans and apply results."""

from __future__ import annotations

from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_WEB_AI,
    TestProtectionApplyResult,
    TestProtectionGapPlan,
)

__all__ = [
    "format_test_protection_apply_result",
    "format_test_protection_gap_plan",
]


def format_test_protection_gap_plan(plan: TestProtectionGapPlan) -> str:
    """Format a non-reparseable specialist report and bounded Web AI handoff."""
    lines = [
        "TEST PROTECTION GAP HEURISTIC RESOLVER",
        "Authority: specialist analysis; writes require explicit human confirmation.",
        f"Safe existing-test links: {plan.safe_link_count}",
        f"Already protected / re-audit: {plan.already_protected_count}",
        f"Web AI required: {plan.web_ai_count}",
        "",
        "DECISIONS",
    ]
    if not plan.decisions:
        lines.append("- none")
    for item in plan.decisions:
        candidate = item.candidate_test_path or "none"
        reasons = ", ".join(item.candidate_reasons) or "none"
        lines.append(f"- {item.source_path}")
        lines.append(f"  action: {item.action}")
        lines.append(f"  candidate_test: {candidate}")
        lines.append(f"  score: {item.candidate_score}")
        lines.append(f"  evidence: {reasons}")
        lines.append(f"  reason: {item.reason}")

    lines.extend(
        [
            "",
            "WEB AI TEST PROTECTION HANDOFF",
            "Review only unresolved modules listed below.",
            "Design real behavior-focused tests or justify a detector-policy correction.",
            "Do not add empty smoke tests merely to silence the warning.",
        ]
    )
    unresolved = [item for item in plan.decisions if item.action == ACTION_WEB_AI]
    if not unresolved:
        lines.append("- none")
    for item in unresolved:
        symbols = ", ".join(item.source_public_symbols[:12]) or "none"
        lines.append(f"- source: {item.source_path}")
        lines.append(f"  public_symbols: {symbols}")
        lines.append(f"  best_candidate_test: {item.candidate_test_path or 'none'}")
        lines.append(f"  reason: {item.reason}")
    return "\n".join(lines).rstrip() + "\n"


def format_test_protection_apply_result(result: TestProtectionApplyResult) -> str:
    """Format the result of a confirmed heuristic correction application."""
    lines = [
        "TEST PROTECTION GAP APPLY RESULT",
        f"Applied links: {result.applied_count}",
        f"Changed test files: {len(result.changed_files)}",
        f"Backup root: {result.backup_root or 'none'}",
    ]
    if result.proposal_only:
        lines.append("Mode: PROPOSAL_ONLY:SPECTATOR")
        lines.append("Proposed test files: " + str(len(result.proposed_files)))
        lines.extend("- " + path for path in result.proposed_files)
    else:
        for path in result.changed_files:
            lines.append(f"- {path}")
    lines.append("Next action: review proposal evidence; Project source is not mutated.")
    return "\n".join(lines).rstrip() + "\n"
