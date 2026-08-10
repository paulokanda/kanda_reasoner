# project-path: kanda_reasoner_app/engineering_diagnostics/rules/ruff_rule_registry.py
"""Deterministic Ruff rule defaults for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "RuffRuleProfile",
    "ruff_rule_profile",
]


@dataclass(frozen=True, slots=True)
class RuffRuleProfile:
    """Deterministic default classification for one Ruff rule."""

    code: str
    priority: str
    severity: str
    category: str
    rationale: str


_EXACT_PROFILES = {
    "F821": RuffRuleProfile(
        "F821",
        "high",
        "error",
        "undefined_name",
        "Undefined names can block imports or runtime execution.",
    ),
    "F822": RuffRuleProfile(
        "F822",
        "high",
        "error",
        "undefined_export",
        "Undefined exports break declared public module contracts.",
    ),
    "F601": RuffRuleProfile(
        "F601",
        "high",
        "error",
        "duplicate_dictionary_key",
        "Repeated dictionary keys silently replace earlier values.",
    ),
    "F811": RuffRuleProfile(
        "F811",
        "medium_high",
        "warning",
        "redefinition",
        "Redefinitions can hide the intended canonical symbol owner.",
    ),
    "E402": RuffRuleProfile(
        "E402",
        "medium_high",
        "warning",
        "import_order",
        "Non-top-level imports may indicate startup or side-effect risks.",
    ),
    "F403": RuffRuleProfile(
        "F403",
        "medium_high",
        "warning",
        "wildcard_import",
        "Wildcard imports obscure public ownership and symbol provenance.",
    ),
    "F401": RuffRuleProfile(
        "F401",
        "medium_low",
        "warning",
        "unused_import",
        "Unused imports can indicate stale dependencies or dead code.",
    ),
    "F841": RuffRuleProfile(
        "F841",
        "medium_low",
        "warning",
        "unused_local",
        "Unused locals can indicate incomplete or stale implementation paths.",
    ),
    "E501": RuffRuleProfile(
        "E501",
        "low",
        "info",
        "formatting",
        "Line length is primarily a maintainability and formatting concern.",
    ),
}


def ruff_rule_profile(code: object) -> RuffRuleProfile:
    """Return one auditable default profile without claiming final truth."""
    normalized = str(code or "RUFF_UNKNOWN").strip().upper() or "RUFF_UNKNOWN"
    profile = _EXACT_PROFILES.get(normalized)
    if profile is not None:
        return profile
    if normalized.startswith(("E", "W")):
        return RuffRuleProfile(
            normalized,
            "low",
            "info",
            "style_or_warning",
            "Default Ruff style or warning classification pending human review.",
        )
    return RuffRuleProfile(
        normalized,
        "medium",
        "warning",
        "ruff_lint",
        "Default Ruff lint classification pending human review.",
    )
