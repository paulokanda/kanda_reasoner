# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/llm_formatting.py
"""Text formatting for optional local LLM arbitration results."""
from __future__ import annotations

from .models import LLMArbitrationRequest, LLMArbitrationResult

__all__ = ["format_llm_arbitration_report"]


def format_llm_arbitration_report(
    request: LLMArbitrationRequest,
    result: LLMArbitrationResult,
) -> str:
    """Return a reviewable LLM arbitration summary for the GUI."""
    lines = [
        "LLM arbitration contract generated.",
        "Important:",
        "- This train does not rewrite modules.",
        "- This train does not create patches.",
        "- LLM output is JSON-only and schema validated.",
        "- Invalid or unavailable LLM output falls back to deterministic planning.",
        "",
        "Request:",
        f"- Purpose: {request.purpose}",
        f"- Symbol: {request.symbol_name or '<none>'}",
        f"- Model: {request.model_name or '<not selected>'}",
        f"- Local LLM enabled: {request.local_llm_enabled}",
        f"- Cache key: {request.cache_key}",
        "",
        "Result:",
        f"- Status: {result.status}",
        f"- Selected module: {result.selected_module or '<none>'}",
        f"- Confidence: {result.confidence}",
        f"- fallback used: {result.fallback_used}",
        f"- Rationale: {result.rationale}",
    ]
    if result.warnings:
        lines.append("- Warnings:")
        lines.extend("  - " + warning for warning in result.warnings)
    return "\n".join(lines)
