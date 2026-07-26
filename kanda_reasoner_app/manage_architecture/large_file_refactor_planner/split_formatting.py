# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/split_formatting.py
"""Text formatting for deterministic split-plan contracts."""
from __future__ import annotations

from .models import RefactorPlan

__all__ = ["format_split_plan"]


def format_split_plan(plan: RefactorPlan) -> str:
    """Return a readable split-plan summary for the GUI."""
    lines = [
        "Split plan contract generated.",
        f"Status: {plan.status}",
        f"Target file: {plan.target_file}",
        f"Source hash: {plan.source_content_hash}",
        "",
        "Public API preservation:",
        f"  Before: {', '.join(plan.public_api_before) or '<none>'}",
        f"  After expected: {', '.join(plan.public_api_after_expected) or '<none>'}",
        "",
        "Planned modules:",
    ]
    for module in plan.proposed_modules:
        lines.extend(
            [
                f"- {module.filename}",
                f"  Role: {module.role}",
                f"  Estimated lines: {module.estimated_lines}",
                f"  Symbols: {', '.join(module.symbols) or '<none>'}",
                f"  Risks: {', '.join(module.risk_flags) or '<none>'}",
                f"  Status: {module.status}",
                f"  Line policy: {module.line_limit_justification}",
            ]
        )
    selection = plan.import_migration.get("heuristic_candidate_selection", {})
    if isinstance(selection, dict) and selection:
        lines.extend(
            [
                "",
                "Heuristic candidate selection:",
                "  Selected: " + str(selection.get("selected_candidate_id", "<none>")),
                "  Strategy: " + str(selection.get("selected_strategy", "<none>")),
            ]
        )
        candidates = selection.get("candidates", [])
        if isinstance(candidates, list):
            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue
                lines.append(
                    "  - "
                    + str(candidate.get("candidate_id", "candidate"))
                    + ": status="
                    + str(candidate.get("status", "unknown"))
                    + "; score="
                    + str(candidate.get("total_score", ""))
                    + "; helpers="
                    + str(len(candidate.get("clusters", [])))
                    + "; responsibility="
                    + str(candidate.get("responsibility_cohesion_score", ""))
                    + "; topology="
                    + str(candidate.get("topology_score", ""))
                    + "; mixed_penalty="
                    + str(candidate.get("mixed_responsibility_penalty", ""))
                    + "; effective_history="
                    + str(candidate.get("historical_cochange_score", ""))
                )

    history = plan.import_migration.get("git_historical_coupling", {})
    if isinstance(history, dict) and history:
        lines.extend(
            [
                "",
                "Git historical coupling:",
                "  Status: " + str(history.get("status", "unknown")),
                "  Source: " + str(history.get("source_relative_path", "<none>")),
                "  Queried clusters: " + str(history.get("queried_cluster_count", 0)),
                "  History commits observed: " + str(history.get("history_commit_count", 0)),
                "  Evidence confidence: " + str(history.get("confidence_label", "none")),
                "  Confidence weight: " + str(history.get("confidence_weight", 0.0)),
                "  Confidence reason: " + str(history.get("confidence_reason", "")),
            ]
        )
        pairs = history.get("pair_affinities", [])
        if isinstance(pairs, list) and pairs:
            lines.append("  Strongest co-change affinities:")
            for item in pairs[:5]:
                if not isinstance(item, dict):
                    continue
                lines.append(
                    "    - "
                    + str(item.get("left_cluster_id", "left"))
                    + " <-> "
                    + str(item.get("right_cluster_id", "right"))
                    + ": raw_score="
                    + str(item.get("score", ""))
                    + "; effective_score="
                    + str(item.get("effective_score", ""))
                    + "; shared_commits="
                    + str(item.get("shared_commit_count", 0))
                )
        warnings = history.get("warnings", [])
        if warnings:
            lines.append("  Warnings: " + ", ".join(str(item) for item in warnings))

    labeling = plan.import_migration.get("responsibility_labeling", {})
    if isinstance(labeling, dict) and labeling:
        lines.extend(["", "Responsibility labeling:"])
        for cluster_id, record in sorted(labeling.items()):
            if not isinstance(record, dict):
                continue
            lines.append(
                "  - "
                + str(record.get("primary_responsibility", "unknown"))
                + ": confidence="
                + str(record.get("confidence", "unknown"))
                + "; score="
                + str(record.get("confidence_score", ""))
            )
            secondary = record.get("secondary_responsibilities", [])
            if secondary:
                lines.append("    Secondary: " + ", ".join(str(item) for item in secondary))
            evidence = record.get("evidence_tokens", [])
            if evidence:
                lines.append("    Evidence: " + ", ".join(str(item) for item in evidence))


    topology = plan.import_migration.get("projected_dependency_topology", {})
    if isinstance(topology, dict) and topology:
        lines.extend(
            [
                "",
                "Projected dependency topology:",
                "  Status: " + str(topology.get("status", "unknown")),
            ]
        )
        order = topology.get("helper_topological_order", [])
        lines.append(
            "  Helper topological order: "
            + (" -> ".join(str(item) for item in order) if order else "<none>")
        )
        edges = topology.get("edges", [])
        lines.append("  Directed edges:")
        if edges:
            lines.extend("    - " + str(edge) for edge in edges)
        else:
            lines.append("    - <none>")
        back_refs = topology.get("facade_back_references", [])
        lines.append("  Facade back-references:")
        if back_refs:
            lines.extend("    - " + str(edge) for edge in back_refs)
        else:
            lines.append("    - <none>")
        helper_cycles = topology.get("helper_cycles", [])
        lines.append("  Helper cycles: " + (str(helper_cycles) if helper_cycles else "<none>"))
        full_cycles = topology.get("full_cycle_components", [])
        lines.append("  Boundary cycle components: " + (str(full_cycles) if full_cycles else "<none>"))

    if isinstance(selection, dict) and selection:
        selected_id = selection.get("selected_candidate_id")
        candidates = selection.get("candidates", [])
        selected = next(
            (item for item in candidates if isinstance(item, dict) and item.get("candidate_id") == selected_id),
            None,
        )
        if isinstance(selected, dict):
            evidence = selected.get("quality_evidence", {})
            mixed = evidence.get("mixed_responsibility_clusters", []) if isinstance(evidence, dict) else []
            lines.extend(["", "Selected candidate quality evidence:"])
            lines.append(
                "  Responsibility cohesion: "
                + str(selected.get("responsibility_cohesion_score", ""))
            )
            lines.append("  Topology score: " + str(selected.get("topology_score", "")))
            lines.append(
                "  Mixed-responsibility penalty: "
                + str(selected.get("mixed_responsibility_penalty", ""))
            )
            if mixed:
                lines.append("  Mixed-responsibility helpers:")
                for item in mixed:
                    if not isinstance(item, dict):
                        continue
                    lines.append(
                        "    - primary="
                        + str(item.get("primary_responsibility", "unknown"))
                        + "; secondary="
                        + ", ".join(str(value) for value in item.get("secondary_responsibilities", []))
                        + "; lines="
                        + str(item.get("estimated_lines", ""))
                        + "; penalty="
                        + str(item.get("penalty", ""))
                    )

    lines.extend(["", "Risks:"])
    if plan.risks:
        lines.extend(f"- {risk}" for risk in plan.risks)
    else:
        lines.append("- <none>")
    lines.extend(["", "Validation blockers:"])
    if plan.validation_blockers:
        lines.extend(f"- {blocker}" for blocker in plan.validation_blockers)
    else:
        lines.append("- <none>")
    lines.extend(
        [
            "",
            "Important:",
            "- This train does not write preview files.",
            "- This train does not create project split files.",
            "- Patch creation remains blocked until preview validation trains.",
        ]
    )
    return "\n".join(lines)
