# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_ai_architecture_questions.py
"""Shared architecture questions for bounded local and Web AI planning review."""

from __future__ import annotations

from typing import Any

from .models import MIN_HELPER_PHYSICAL_LINES, RefactorPlan

__all__ = [
    "ARCHITECTURE_REVIEW_QUESTIONS",
    "architecture_review_payload",
]

ARCHITECTURE_REVIEW_QUESTIONS = (
    (
        "tiny_helpers",
        "Which helper modules are below minimum_helper_physical_lines, and which "
        "cohesive existing helper should absorb each one?",
    ),
    (
        "module_count",
        "Can the helper count be reduced while keeping every surviving helper "
        "between the minimum and maximum physical-line limits?",
    ),
    (
        "cohesion",
        "Does each surviving helper represent one coherent architectural "
        "responsibility based on symbol names, references, and dependency evidence?",
    ),
    (
        "dependency_safety",
        "Will any proposed merge or reassignment introduce a circular dependency "
        "between helper modules?",
    ),
    (
        "atomic_clusters",
        "Are all atomic clusters kept together in exactly one helper after the "
        "proposed corrections?",
    ),
    (
        "semantic_names",
        "Do helper filenames communicate real responsibilities instead of generic "
        "serial names such as function_2 or dependency_cluster_3?",
    ),
    (
        "public_facade",
        "Does the correction preserve every public-facade-owned symbol and the "
        "expected public API?",
    ),
    (
        "final_gate",
        "After the corrections, do all helpers satisfy the size gate and is every "
        "remaining architecture warning explicitly justified?",
    ),
)


def architecture_review_payload(plan: RefactorPlan) -> dict[str, Any]:
    """Return concrete questions and size policy for one AI review round."""

    minimum = max(
        MIN_HELPER_PHYSICAL_LINES,
        int(plan.settings.get("minimum_helper_physical_lines", 100)),
    )
    maximum = int(plan.settings.get("maximum_physical_lines", 500))
    return {
        "policy": {
            "minimum_helper_physical_lines": minimum,
            "maximum_physical_lines": maximum,
            "tiny_helpers_are_hard_blockers": True,
            "public_facade_ownership_must_not_change": True,
            "helper_dependency_cycles_are_forbidden": True,
        },
        "questions": [
            {"id": question_id, "question": question}
            for question_id, question in ARCHITECTURE_REVIEW_QUESTIONS
        ],
    }
