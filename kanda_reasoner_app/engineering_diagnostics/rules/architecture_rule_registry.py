# project-path: kanda_reasoner_app/engineering_diagnostics/rules/architecture_rule_registry.py
"""Deterministic Architecture Review rule defaults for Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["ArchitectureRuleProfile", "architecture_rule_profile"]


@dataclass(frozen=True, slots=True)
class ArchitectureRuleProfile:
    """Auditable default governance classification for one architecture issue."""

    code: str
    priority: str
    severity: str
    category: str
    governance_impact: str
    rationale: str
    suggested_action: str


_HIGH_CODES = frozenset(
    {
        "CIRCULAR_IMPORT",
        "CROSS_BOX_PUBLIC_SYMBOL_COLLISION",
        "DUPLICATE_PUBLIC_SYMBOL",
        "MISSING_PUBLIC_SURFACE_CONTROL",
        "SIDE_EFFECT_ON_IMPORT",
        "WRONG_OWNER_BOX",
    }
)
_MEDIUM_HIGH_CODES = frozenset(
    {
        "DEPRECATED_VARIANT_STILL_REFERENCED",
        "PROJECT_WIDE_AI_CONFUSION",
        "PUBLIC_API_INSTABILITY",
        "SHARED_MUTABLE_STATE_COUPLING",
        "TEST_PROTECTION_GAP",
    }
)


def architecture_rule_profile(code: object, level: object) -> ArchitectureRuleProfile:
    """Return a deterministic default without replacing human governance review."""
    normalized_code = str(code or "ARCHITECTURE_UNKNOWN").strip().upper()
    normalized_level = str(level or "warning").strip().lower()
    if normalized_level == "error" or normalized_code in _HIGH_CODES:
        return ArchitectureRuleProfile(
            normalized_code,
            "high",
            "error",
            "architecture_governance",
            "high",
            "The finding can violate owner, boundary, import, or public-contract safety.",
            "Review the canonical owner and public contract before any source change.",
        )
    if normalized_code in _MEDIUM_HIGH_CODES:
        return ArchitectureRuleProfile(
            normalized_code,
            "medium_high",
            "warning",
            "architecture_protection",
            "medium_high",
            "The finding can weaken lifecycle, public-surface, or regression protection.",
            "Add exact owner evidence and a focused public-contract validation plan.",
        )
    if normalized_code == "DEAD_CODE_UNREACHABLE_FILE":
        return ArchitectureRuleProfile(
            normalized_code,
            "medium",
            "warning",
            "architecture_reachability_evidence",
            "medium",
            "Unreachable active files can confuse developers and automated reasoning.",
            "Confirm entry-point, manifest, public API, or test evidence before cleanup.",
        )
    if normalized_level in ("info", "other"):
        return ArchitectureRuleProfile(
            normalized_code,
            "low",
            "info",
            "architecture_information",
            "low",
            "Informational architecture evidence requires contextual human review.",
            "Review the evidence before deciding whether any governed action is needed.",
        )
    return ArchitectureRuleProfile(
        normalized_code,
        "medium_high",
        "warning",
        "architecture_governance",
        "medium_high",
        "Architecture findings receive elevated governance impact by default.",
        "Review owner, boundary, symbol, and validation-source evidence.",
    )
