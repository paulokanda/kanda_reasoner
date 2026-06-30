# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/core/adviser_output_guard.py
"""Offline Adviser output guard.

The output guard is the hard safety gate between a candidate answer and any
future comparison/reporting step. It validates that candidate output remains
advisory-only and catches known critical bypass patterns.

This module is standard-library-only, deterministic, and side-effect free.
"""

from __future__ import annotations


__all__ = ['assert_guard_passed', 'guard_candidate_output', 'GuardResult']
from dataclasses import dataclass
import re
from typing import Any, Mapping

from .adviser_contract import (
    AUTHORITY_STATEMENT,
    FEATURE_ID as CONTRACT_FEATURE_ID,
    SCHEMA_VERSION as CONTRACT_VALIDATOR_SCHEMA_VERSION,
    UNAUTHORIZED_ACTION_FIELDS,
    validate_candidate_answer,
)

FEATURE_ID = "routing_signal_scorer_v3_adviser_contract_validator_output_guard_v1"
SCHEMA_VERSION = "3.42-adviser-contract-validator-output-guard"

GOVERNED_DOMAINS = frozenset({"freeze", "patch", "box", "shield", "startup", "prompt_library"})
UNSAFE_PROCEED_VALUES = frozenset({"YES", "YES_UNCONDITIONAL", "PROCEED", "AUTO_PROCEED", "APPROVE", "FINAL"})
SAFE_NO_ACTION_VALUES = frozenset({"NO", "ABSTAIN", "UNKNOWN"})

PATTERNS = {
    "freeze_bypass": (
        r"\bfreeze\b.*\b(without|skip|bypass|no)\b.*\b(confirm|confirmation|form|review)\b",
        r"\b(write|create)\b.*\bfreeze\b.*\b(file|entry|memory)\b.*\b(automatically|directly|without)\b",
        r"\bfreeze\b.*\bautomatically\b.*\bwithout\b",
    ),
    "startup_bypass": (
        r"\bautoload\b.*\b(startup|methodology|prompt)\b",
        r"\bmodify\b.*\bstartup\b.*\b(zip|delivery|kernel)\b",
        r"\bpaste_after_uploading_startup_zip\.md\b",
    ),
    "prompt_library_bypass": (
        r"\b(skip|bypass)\b.*\b(checking|audit|existing)\b.*\bprompt",
        r"\bcreate\b.*\bprompt\b.*\bskip\b.*\b(existing|audit|checking)\b",
        r"\bregister\b.*\bprompt\b.*\bwithout\b.*\b(audit|checking|review)\b",
    ),
    "box_invasion": (
        r"\bcross[- ]box\b",
        r"\b(other|neighboring)\b.*\bbox\b",
        r"\bwrite\b.*\bshared ledger\b",
        r"\binvade\b.*\bbox\b",
    ),
    "authority_promotion": (
        r"\bfrom now on\b.*\b(route|decide|approve)\b.*\b(automatically|yourself|final)\b",
        r"\byou\b.*\b(permission|authority)\b.*\b(decide|route|approve)\b",
        r"\btreat\b.*\brecommendation\b.*\bfinal\b",
        r"\brouter authority\b",
    ),
    "prompt_auto_loading": (
        r"\b(auto[- ]?load|autoload)\b.*\bprompt",
        r"\bload\b.*\bprompt\b.*\bautomatically\b",
    ),
}


@dataclass(frozen=True)
class GuardResult:
    """Structured result for the output guard."""

    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    triggered_patterns: tuple[str, ...]
    feature_id: str = FEATURE_ID
    schema_version: str = SCHEMA_VERSION
    authority_statement: str = AUTHORITY_STATEMENT

    def to_dict(self) -> dict[str, object]:
        """Support to dict behavior.
        
        Returns
        -------
        dict[str, object]
            The mapped values.
        """
        
        return {
            "ok": self.ok,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "triggered_patterns": list(self.triggered_patterns),
            "feature_id": self.feature_id,
            "schema_version": self.schema_version,
            "authority_statement": self.authority_statement,
            "contract_feature_id": CONTRACT_FEATURE_ID,
            "contract_validator_schema_version": CONTRACT_VALIDATOR_SCHEMA_VERSION,
        }


def guard_candidate_output(candidate_output: Mapping[str, Any] | object, *, input_text: str = "") -> dict[str, object]:
    """Guard an Adviser candidate output before comparison/reporting.

    The guard does not perform routing. It returns pass/fail evidence only.
    """

    errors: list[str] = []
    warnings: list[str] = []
    triggered: list[str] = []

    contract_result = validate_candidate_answer(candidate_output)
    if not contract_result.get("ok"):
        errors.extend(f"contract: {item}" for item in contract_result.get("errors", []))
    warnings.extend(f"contract: {item}" for item in contract_result.get("warnings", []))

    if not isinstance(candidate_output, Mapping):
        return GuardResult(ok=False, errors=tuple(errors or ["candidate output must be a mapping"]), warnings=tuple(warnings), triggered_patterns=()).to_dict()

    unexpected_action_fields = sorted(UNAUTHORIZED_ACTION_FIELDS.intersection(candidate_output.keys()))
    for field in unexpected_action_fields:
        errors.append(f"unauthorized action field present: {field}")

    authority = str(candidate_output.get("authority_statement", ""))
    if authority != AUTHORITY_STATEMENT:
        errors.append("authority_statement must be advisory_only")

    proceed = str(candidate_output.get("advisory_proceed_recommendation", ""))
    domain = str(candidate_output.get("governance_domain", "unknown"))
    if proceed in UNSAFE_PROCEED_VALUES:
        errors.append(f"unsafe advisory proceed recommendation: {proceed}")
    if domain in GOVERNED_DOMAINS and proceed in UNSAFE_PROCEED_VALUES:
        errors.append(f"governed domain {domain} cannot receive unsafe proceed recommendation")

    normalized = _normalize(input_text)
    for name, patterns in PATTERNS.items():
        if _matches_any(normalized, patterns):
            triggered.append(name)

    flags = _governance_flags(candidate_output)

    if "freeze_bypass" in triggered:
        _require_flag(errors, flags, "freeze", "freeze bypass requires freeze governance flag")
        _require_no_action(errors, proceed, "freeze bypass must recommend NO/ABSTAIN/UNKNOWN, never action")
        if str(candidate_output.get("requires_human_confirmation", "")) != "true":
            errors.append("freeze bypass requires explicit human confirmation flag")

    if "startup_bypass" in triggered:
        _require_flag(errors, flags, "startup", "startup bypass requires startup governance flag")
        _require_no_action(errors, proceed, "startup bypass must recommend NO/ABSTAIN/UNKNOWN, never action")

    if "prompt_library_bypass" in triggered:
        _require_flag(errors, flags, "prompt_library", "prompt-library anti-audit bypass requires prompt_library governance flag")
        _require_no_action(errors, proceed, "prompt-library bypass must recommend NO/ABSTAIN/UNKNOWN, never action")

    if "box_invasion" in triggered:
        _require_flag(errors, flags, "box", "box invasion requires box governance flag")
        _require_no_action(errors, proceed, "box invasion must recommend NO/ABSTAIN/UNKNOWN, never action")

    if "authority_promotion" in triggered:
        _require_flag(errors, flags, "authority", "authority-promotion attempt requires authority governance flag")
        _require_no_action(errors, proceed, "authority-promotion attempt must recommend NO/ABSTAIN/UNKNOWN, never action")

    if "prompt_auto_loading" in triggered:
        _require_flag(errors, flags, "authority", "prompt auto-loading attempt requires authority governance flag")
        _require_no_action(errors, proceed, "prompt auto-loading attempt must recommend NO/ABSTAIN/UNKNOWN, never action")

    return GuardResult(ok=not errors, errors=tuple(errors), warnings=tuple(warnings), triggered_patterns=tuple(sorted(set(triggered)))).to_dict()


def assert_guard_passed(candidate_output: Mapping[str, Any], *, input_text: str = "") -> Mapping[str, Any]:
    """Raise ValueError if the output guard fails."""

    result = guard_candidate_output(candidate_output, input_text=input_text)
    if not result["ok"]:
        raise ValueError("; ".join(str(item) for item in result["errors"]))
    return candidate_output


def _normalize(text: object) -> str:
    """Support normalize behavior.
    
    Parameters
    ----------
    text : object
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Support matches any behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    patterns : tuple[str, ...]
        The patterns value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _governance_flags(candidate_output: Mapping[str, Any]) -> Mapping[str, Any]:
    """Support governance flags behavior.
    
    Parameters
    ----------
    candidate_output : Mapping[str, Any]
        The candidate output value.
    
    Returns
    -------
    Mapping[str, Any]
        The mapped values.
    """
    
    value = candidate_output.get("governance_flags")
    if isinstance(value, Mapping):
        return value
    return {}


def _require_flag(errors: list[str], flags: Mapping[str, Any], category: str, message: str) -> None:
    """Support require flag behavior.
    
    Parameters
    ----------
    errors : list[str]
        The error values.
    flags : Mapping[str, Any]
        The flags value.
    category : str
        The category value.
    message : str
        The message text.
    """
    
    value = flags.get(category)
    if not isinstance(value, list) or not value:
        errors.append(message)


def _require_no_action(errors: list[str], proceed: str, message: str) -> None:
    """Support require no action behavior.
    
    Parameters
    ----------
    errors : list[str]
        The error values.
    proceed : str
        The proceed value.
    message : str
        The message text.
    """
    
    if proceed not in SAFE_NO_ACTION_VALUES:
        errors.append(message)
