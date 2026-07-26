# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_web_ai_prompt.py
"""Self-contained Web AI handoff for one sealed Main Workbench case."""

from __future__ import annotations

from collections.abc import Iterable

from .external_ai_candidate_exchange_contract import CandidateSetIdentity, ExchangeIdentity
from .external_ai_candidate_exchange_prompt import build_external_ai_candidate_review_task

__all__ = ["build_main_workbench_web_ai_task"]


def build_main_workbench_web_ai_task(
    *,
    candidate_identity: CandidateSetIdentity,
    exchange_identity: ExchangeIdentity,
    candidate_files: Iterable[str],
    terminal_status: str,
    blockers: Iterable[str],
) -> str:
    """Return a complete project handoff that assumes no previous chat context."""
    blocker_lines = tuple(sorted({str(item) for item in blockers if str(item)}))
    blocker_text = "\n".join("- " + item for item in blocker_lines) or "- none"
    foundation = build_external_ai_candidate_review_task(
        candidate_identity=candidate_identity,
        exchange_identity=exchange_identity,
        candidate_files=candidate_files,
    )
    introduction = "\n".join(
        [
            "# KANDA Main Workbench Complete Refactor Case",
            "",
            "## Read this context first",
            "",
            "KANDA Reasoner is a reusable Python and PySide6 desktop tool that",
            "analyzes, plans, previews, validates, and safely applies Python refactors.",
            "The next AI has no prior knowledge of this project or conversation.",
            "Use the files in this ZIP as the complete bounded source of context.",
            "The project_source folder contains the bounded Python project tree and",
            "configuration files. The governance folder contains available active",
            "Error Memory lessons and recent frozen-feature entries.",
            "",
            "Ownership model:",
            "- KANDA Reasoner Tool is the reusable card machine.",
            "- The Active Project owns canonical source and durable results.",
            "- The selected target module is the inserted card.",
            "- Workbench Preview is Project-owned candidate evidence, not source truth.",
            "- Tool root and Project root may be physically equal during self-hosting,",
            "  but their logical identities and ownership must remain separate.",
            "",
            "The local deterministic workflow already ran:",
            "Planner handoff -> Plan Intake -> Dependency Readiness -> Real Preview ->",
            "Structural Validation -> Advanced Quality Review when locally reachable.",
            "No canonical Active Project source was changed by Main Workbench.",
            "",
            "Terminal status: " + str(terminal_status),
            "",
            "Current blocker evidence:",
            blocker_text,
            "",
            "## Your role",
            "",
            "Act as an independent senior Python architecture auditor and refactoring",
            "specialist. Audit the entire candidate family and all supplied evidence.",
            "Do not assume the local plan or Preview is correct merely because a local",
            "stage passed. Correct architecture, imports, compatibility, typing, and",
            "behavior where required, but preserve project ownership and lineage.",
            "",
            "## Hard module-size rule",
            "",
            "Every created or materially modified Python source module must contain",
            "101 to 499 physical lines. Do not create filler or arbitrary wrappers.",
            "Merge modules below 101 lines into the most cohesive related owner and",
            "split modules at 500 or more lines along real responsibility boundaries.",
            "",
            "## Required review output",
            "",
            "Explain Structural Review, Risks, Improvements, Corrections, line-rule",
            "compliance, and Final Recommended Logic. Then, when safe, return one",
            "complete cumulative governed KANDA patch ZIP. Do not return only snippets.",
            "",
            "The patch ZIP must preserve the complete source-ready candidate family,",
            "include fail-closed install and validation logic, bind the exact accepted",
            "baseline, and prepare freeze evidence without writing canonical frozen",
            "memory. Preview Freeze Entry remains read-only and Confirm and Write",
            "remains explicitly human-confirmed.",
            "",
            "## Package reading order",
            "",
            "Read EXTERNAL_AI_TASK.md first, then lineage identities, the baseline",
            "target, the complete candidate family, project_source, governance context,",
            "Planner and Workbench context, Structural Validation, AQR evidence, and",
            "the package manifest. Treat",
            "exact source files and hashes as authoritative over summaries.",
            "",
            "## Safety boundaries",
            "",
            "Do not collapse Tool ownership into Active Project ownership, even",
            "when both roots are physically identical. Do not write outside declared",
            "Active Project paths, do not omit candidate-family members, and do not",
            "weaken validation or source-freshness gates to force a passing result.",
            "",
            "If a safe governed patch cannot be produced, return:",
            "GOVERNED RETURN BLOCKED",
            "and identify the exact missing context or unresolved safety blocker.",
            "",
            "---",
            "",
        ]
    )
    return introduction + foundation
