# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_analysis_feedback.py
"""Compact visible feedback for Planner analysis completion."""

from __future__ import annotations

from pathlib import Path

__all__ = ["format_planner_analysis_completion"]


def format_planner_analysis_completion(report: object, selected_version: str) -> str:
    """Return concise Plan & Actions feedback after read-only AST analysis."""

    target = Path(str(getattr(report, "target_file", "selected module"))).name
    lines = int(getattr(report, "line_count_physical", 0) or 0)
    symbols = len(list(getattr(report, "symbols", ()) or ()))
    public_api = len(list(getattr(report, "public_api_symbols", ()) or ()))
    missing_docs = int(getattr(report, "missing_docstring_count", 0) or 0)
    risks = list(getattr(report, "risk_flags", ()) or ())
    errors = list(getattr(report, "analysis_errors", ()) or ())
    version_label = str(selected_version).replace("_", " ").title()
    rows = [
        "ANALYSIS COMPLETE",
        "Target: " + target,
        "Physical lines: " + str(lines),
        "Top-level symbols: " + str(symbols),
        "Public API symbols: " + str(public_api),
        "Missing docstrings: " + str(missing_docs),
        "Risks: " + (", ".join(str(item) for item in risks) if risks else "<none>"),
        "Selected split version: " + version_label,
    ]
    if errors:
        rows.append("Analysis errors: " + "; ".join(str(item) for item in errors))
    rows.extend(
        [
            "",
            "Detailed AST evidence is available in Input & Analysis.",
            "Click Generate Split Plan to run the selected version route.",
        ]
    )
    return "\n".join(rows)
