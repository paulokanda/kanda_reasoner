# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_comprehensive_formatting.py
"""Readable formatting for the explicit comprehensive local-AI review stage."""

from __future__ import annotations

from .planner_local_ai_comprehensive_review import (
    ComprehensiveLocalAIReviewResult,
)

__all__ = ["format_comprehensive_local_ai_review"]


def format_comprehensive_local_ai_review(
    result: ComprehensiveLocalAIReviewResult,
) -> str:
    """Return human-readable bounded review evidence."""

    split = result.split_review
    docs = result.docstring_review
    lines = [
        "LOCAL AI COMPREHENSIVE PLANNING REVIEW",
        "Overall status: " + result.status,
        "",
        "Split and ambiguity review:",
        "- Status: " + split.status,
        "- Model: " + (split.model_name or "none - heuristic fallback"),
        "- Rounds: " + str(split.rounds),
        "- Final plan status: " + split.plan.status,
        "- Final selected-version actions applied: " + str(split.corrections_applied),
        "- Rationale: " + (split.rationale or "No rationale returned."),
        "",
        "Docstring review:",
        "- Status: " + docs.status,
        "- Model: " + (docs.model_name or "none - deterministic proposals kept"),
        "- Reviewed targets: " + str(docs.reviewed_count),
        "- Updated targets: " + str(docs.updated_count),
        "- Rationale: " + (docs.rationale or "No rationale returned."),
    ]
    if split.stage_evidence:
        lines.append("")
        lines.append("Staged architecture protocol:")
        lines.extend("- " + stage + ": " + status for stage, status in split.stage_evidence)
    if split.tournament_evidence:
        lines.append("")
        lines.append("Local AI candidate tournament:")
        lines.append("- Selected candidate: " + (split.selected_candidate_id or "none"))
        lines.append("- Baseline score: " + f"{split.baseline_candidate_score:.6f}")
        lines.append("- Selected score: " + f"{split.selected_candidate_score:.6f}")
        lines.append("- Selection: " + (split.tournament_selection_reason or "No selection reason recorded."))
        lines.append(
            "- Candidate exploration actions accepted: "
            + str(split.tournament_candidate_actions_accepted)
        )
        lines.append(
            "- Final selected-version actions applied: " + str(split.corrections_applied)
        )
        for item in split.tournament_evidence:
            lines.append(
                "- "
                + str(item.get("candidate_id", "candidate"))
                + ": status="
                + str(item.get("status", "unknown"))
                + ", score="
                + str(item.get("total_score", "n/a"))
                + ", strategy="
                + str(item.get("strategy", "unknown"))
            )
    if split.architecture_answers:
        lines.append("")
        lines.append("Architecture question answers:")
        lines.extend(
            "- " + key + ": " + value
            for key, value in split.architecture_answers
        )
    if result.warnings:
        lines.append("")
        lines.append("Review notes:")
        lines.extend("- " + item for item in result.warnings)
    lines.extend(
        [
            "",
            "Boundary:",
            "- Local AI may refine only known planning objects.",
            "- All split corrections are deterministically revalidated.",
            "- Docstring updates remain proposals and do not write source.",
        ]
    )
    return "\n".join(lines)
