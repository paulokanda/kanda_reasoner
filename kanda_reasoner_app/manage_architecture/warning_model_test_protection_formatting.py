# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py
"""Format Local-AI TEST_PROTECTION_GAP semantic and sandbox-validation reports."""

from __future__ import annotations

from kanda_reasoner_app.manage_architecture.warning_model_live_audit import (
    ModelApplyVerificationResult,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_apply import (
    ModelTestProtectionApplyResult,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_generation_contract import (
    ACTION_MODEL_TEST_CHANGE,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_resolver import (
    ModelTestProtectionPlan,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_WEB_AI,
)

__all__ = [
    "format_model_apply_verification_result",
    "format_model_test_protection_apply_result",
    "format_model_test_protection_plan",
]


def _decision_lines(item) -> list[str]:
    """Return the stable multi-line projection for one resolver decision."""
    return [
        "- " + item.source_path,
        "  action: " + item.action,
        "  target_test: " + (item.candidate_test_path or "none"),
        "  score: " + str(item.candidate_score),
        "  evidence: " + (", ".join(item.candidate_reasons) or "none"),
        "  reason: " + item.reason,
    ]


def format_model_test_protection_plan(plan: ModelTestProtectionPlan) -> str:
    """Render a non-warning report that cannot be reparsed as audit findings."""
    lines = [
        "TEST PROTECTION GAP LOCAL AI RESOLVER V2",
        "Authority: semantic candidate review plus disposable-project validation; live writes still require explicit human confirmation.",
        "Selected Ollama model: " + plan.model_name,
        "Heuristic safe links: " + str(plan.heuristic_safe_count),
        "Local AI existing-test links: " + str(plan.model_safe_count),
        "Local AI validated test changes: " + str(plan.model_test_change_count),
        "Already protected / re-audit: " + str(plan.already_protected_count),
        "Web AI still required: " + str(plan.web_ai_count),
        "Disposable validation project: " + (plan.sandbox_root or "not used"),
        "",
        "DECISIONS",
    ]
    for item in plan.decisions:
        lines.extend(_decision_lines(item))
    lines.extend(
        [
            "",
            "VALIDATED LOCAL AI TEST CHANGES",
            "These proposals passed static contract gates, targeted pytest, and fresh Architecture Review in the disposable project.",
        ]
    )
    validated = [item for item in plan.decisions if item.action == ACTION_MODEL_TEST_CHANGE]
    if not validated:
        lines.append("- none")
    for item in validated:
        lines.append("- source: " + item.source_path)
        lines.append("  test_change_target: " + item.candidate_test_path)
        lines.append("  evidence: " + ", ".join(item.candidate_reasons))
    lines.extend(
        [
            "",
            "WEB AI REMAINDER",
            "The Local AI lane declined, could not ground, or could not validate the modules below.",
            "Do not create empty tests only to silence the detector.",
        ]
    )
    unresolved = [item for item in plan.decisions if item.action == ACTION_WEB_AI]
    if not unresolved:
        lines.append("- none")
    for item in unresolved:
        lines.append("- source: " + item.source_path)
        lines.append(
            "  public_symbols: " + (", ".join(item.source_public_symbols[:12]) or "none")
        )
        lines.append("  best_candidate_test: " + (item.candidate_test_path or "none"))
        lines.append("  reason: " + item.reason)
    return "\n".join(lines).rstrip() + "\n"


def format_model_test_protection_apply_result(
    result: ModelTestProtectionApplyResult,
) -> str:
    """Render live apply evidence for confirmed Local AI links and test changes."""
    lines = [
        "WARNING LOCAL AI RESOLVER APPLY RESULT",
        "Existing-test links applied: " + str(result.linked_count),
        "Validated test changes applied: " + str(result.mutated_test_count),
        "Total governed changes applied: " + str(result.applied_count),
        "Backup root: " + (result.backup_root or "none"),
        "Changed files:",
    ]
    if not result.changed_files:
        lines.append("- none")
    else:
        lines.extend("- " + path for path in result.changed_files)
    return "\n".join(lines).rstrip() + "\n"


def format_model_apply_verification_result(
    result: ModelApplyVerificationResult,
) -> str:
    """Render actual live writes plus exact-path before/after verification."""
    apply_result = result.apply_result
    lines = [
        "WARNING LOCAL AI RESOLVER VERIFIED APPLY",
        "Files actually changed: " + str(len(apply_result.changed_files)),
        "Existing-test links actually written: " + str(apply_result.linked_count),
        "Validated test mutations actually written: " + str(apply_result.mutated_test_count),
        "Exact source gaps verified resolved: " + str(result.verified_resolved_count),
        "Requested source gaps still present: " + str(len(result.still_present_source_paths)),
        "Newly surfaced paths from fresh audit: " + str(len(result.newly_surfaced_paths)),
        "Backup root: " + (apply_result.backup_root or "none"),
        "",
        "RESOLVED SOURCE PATHS",
    ]
    lines.extend("- " + path for path in result.resolved_source_paths)
    if not result.resolved_source_paths:
        lines.append("- none")
    lines.append("")
    lines.append("STILL PRESENT AFTER APPLY")
    lines.extend("- " + path for path in result.still_present_source_paths)
    if not result.still_present_source_paths:
        lines.append("- none")
    lines.append("")
    lines.append("NEWLY SURFACED AFTER FRESH AUDIT")
    lines.extend("- " + path for path in result.newly_surfaced_paths)
    if not result.newly_surfaced_paths:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"
