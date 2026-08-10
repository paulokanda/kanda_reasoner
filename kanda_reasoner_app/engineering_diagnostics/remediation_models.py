# project-path: kanda_reasoner_app/engineering_diagnostics/remediation_models.py
"""Immutable non-mutating remediation-intent contracts."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "AI_HYPOTHESIS_LABEL",
    "REMEDIATION_ACTION_CLASSES",
    "REMEDIATION_FIX_APPLICABILITY",
    "REMEDIATION_MECHANICAL_SAFETY",
    "REMEDIATION_SEMANTIC_REVIEW",
    "REMEDIATION_TRUST_ORDER",
    "DiagnosticAiHypothesis",
    "DiagnosticRemediationIntent",
    "DiagnosticValidationPlan",
]

AI_HYPOTHESIS_LABEL = "AI-assisted hypothesis"
REMEDIATION_TRUST_ORDER = (
    "TOOL_DETERMINISTIC_METADATA",
    "KANDA_RULE_TEMPLATE",
    "PROJECT_GOVERNANCE_RULE",
    "AI_ASSISTED_HYPOTHESIS",
)
REMEDIATION_ACTION_CLASSES = frozenset(
    {
        "FIX_NOW",
        "PLAN_GOVERNED_WAVE",
        "HUMAN_DECISION_REQUIRED",
        "EVIDENCE_REQUIRED",
        "SAFE_MECHANICAL_FIX_AVAILABLE",
        "DEFERRED_TECHNICAL_DEBT",
        "SUPPRESS_WITH_JUSTIFICATION",
        "DO_NOT_TOUCH",
    }
)
REMEDIATION_FIX_APPLICABILITY = frozenset(
    {"EXACT_FILE", "EXACT_SYMBOL", "PROJECT_GOVERNED", "NOT_APPLICABLE", "UNKNOWN"}
)
REMEDIATION_MECHANICAL_SAFETY = frozenset(
    {
        "SAFE_MECHANICAL",
        "SEMANTIC_REVIEW_REQUIRED",
        "BLOCKED_BY_FREEZE",
        "NOT_MECHANICAL",
        "UNKNOWN",
    }
)
REMEDIATION_SEMANTIC_REVIEW = frozenset(
    {"NOT_REQUIRED", "REQUIRED", "OWNER_REVIEW_REQUIRED"}
)
_UNCERTAINTY = frozenset({"none", "low", "medium", "high"})


def _required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(field_name + " is required.")
    return text


def _optional_text(value: object) -> str:
    return str(value or "").strip()


def _choice(value: object, allowed: frozenset[str], field_name: str) -> str:
    text = _required_text(value, field_name).upper()
    if text not in allowed:
        raise ValueError("Unsupported " + field_name + ": " + text)
    return text


def _unique_text(values: object) -> tuple[str, ...]:
    if values is None:
        return ()
    result: list[str] = []
    for value in tuple(values):
        text = _optional_text(value)
        if text and text not in result:
            result.append(text)
    return tuple(result)


def _uncertainty(value: object) -> str:
    text = _required_text(value, "uncertainty").lower()
    if text not in _UNCERTAINTY:
        raise ValueError("Unsupported uncertainty: " + text)
    return text


@dataclass(frozen=True, slots=True)
class DiagnosticAiHypothesis:
    """Optional human-supplied AI advice retained as the lowest trust layer."""

    text: str
    supporting_issue_fingerprints: tuple[str, ...]
    deterministic_evidence_refs: tuple[str, ...]
    uncertainty: str = "high"
    label: str = AI_HYPOTHESIS_LABEL

    def __post_init__(self) -> None:
        object.__setattr__(self, "text", _required_text(self.text, "AI hypothesis text"))
        object.__setattr__(
            self,
            "supporting_issue_fingerprints",
            _unique_text(self.supporting_issue_fingerprints),
        )
        object.__setattr__(
            self,
            "deterministic_evidence_refs",
            _unique_text(self.deterministic_evidence_refs),
        )
        object.__setattr__(self, "uncertainty", _uncertainty(self.uncertainty))
        object.__setattr__(self, "label", _required_text(self.label, "AI hypothesis label"))
        if self.label != AI_HYPOTHESIS_LABEL:
            raise ValueError("AI advice must be labeled exactly: " + AI_HYPOTHESIS_LABEL)
        if not self.supporting_issue_fingerprints:
            raise ValueError("AI hypothesis requires supporting issue fingerprints.")
        if not self.deterministic_evidence_refs:
            raise ValueError("AI hypothesis requires deterministic evidence references.")


@dataclass(frozen=True, slots=True)
class DiagnosticValidationPlan:
    """Non-executable focused validation and rollback expectations."""

    focused_tests: tuple[str, ...]
    validation_commands: tuple[str, ...]
    rollback_expectation: str
    evidence_required: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "focused_tests", _unique_text(self.focused_tests))
        object.__setattr__(
            self,
            "validation_commands",
            _unique_text(self.validation_commands),
        )
        object.__setattr__(
            self,
            "rollback_expectation",
            _required_text(self.rollback_expectation, "rollback expectation"),
        )
        object.__setattr__(
            self,
            "evidence_required",
            _unique_text(self.evidence_required),
        )
        if not self.focused_tests:
            raise ValueError("Validation plan requires focused tests.")
        if not self.validation_commands:
            raise ValueError("Validation plan requires validation commands.")
        if not self.evidence_required:
            raise ValueError("Validation plan requires evidence expectations.")


@dataclass(frozen=True, slots=True)
class DiagnosticRemediationIntent:
    """One regenerable advice record that can never execute a patch."""

    intent_id: str
    target_issue_fingerprint: str
    action_class: str
    likely_correction: str
    reason: str
    canonical_owner: str
    expected_affected_files: tuple[str, ...]
    frozen_path_impact: str
    governing_freeze_ids: tuple[str, ...]
    required_governed_wave: str
    fix_applicability: str
    mechanical_safety: str
    semantic_review_requirement: str
    validation_plan: DiagnosticValidationPlan
    uncertainty: str
    primary_trust_source: str
    rule_template_id: str
    deterministic_evidence: tuple[str, ...]
    project_governance_rules: tuple[str, ...]
    ai_hypothesis: DiagnosticAiHypothesis | None = None
    executable_patch: bool = False
    source_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name in (
            "intent_id",
            "target_issue_fingerprint",
            "likely_correction",
            "reason",
            "frozen_path_impact",
            "rule_template_id",
        ):
            object.__setattr__(
                self,
                field_name,
                _required_text(getattr(self, field_name), field_name),
            )
        object.__setattr__(
            self,
            "action_class",
            _choice(self.action_class, REMEDIATION_ACTION_CLASSES, "action class"),
        )
        trust = _required_text(self.primary_trust_source, "primary trust source").upper()
        if trust not in REMEDIATION_TRUST_ORDER:
            raise ValueError("Unsupported primary trust source: " + trust)
        object.__setattr__(self, "primary_trust_source", trust)
        object.__setattr__(self, "canonical_owner", _optional_text(self.canonical_owner))
        object.__setattr__(
            self,
            "expected_affected_files",
            _unique_text(self.expected_affected_files),
        )
        object.__setattr__(
            self,
            "governing_freeze_ids",
            _unique_text(self.governing_freeze_ids),
        )
        object.__setattr__(
            self,
            "required_governed_wave",
            _optional_text(self.required_governed_wave),
        )
        object.__setattr__(
            self,
            "fix_applicability",
            _choice(
                self.fix_applicability,
                REMEDIATION_FIX_APPLICABILITY,
                "fix applicability",
            ),
        )
        object.__setattr__(
            self,
            "mechanical_safety",
            _choice(
                self.mechanical_safety,
                REMEDIATION_MECHANICAL_SAFETY,
                "mechanical safety",
            ),
        )
        object.__setattr__(
            self,
            "semantic_review_requirement",
            _choice(
                self.semantic_review_requirement,
                REMEDIATION_SEMANTIC_REVIEW,
                "semantic review requirement",
            ),
        )
        object.__setattr__(self, "uncertainty", _uncertainty(self.uncertainty))
        object.__setattr__(
            self,
            "deterministic_evidence",
            _unique_text(self.deterministic_evidence),
        )
        object.__setattr__(
            self,
            "project_governance_rules",
            _unique_text(self.project_governance_rules),
        )
        if not isinstance(self.validation_plan, DiagnosticValidationPlan):
            raise ValueError("validation_plan must be DiagnosticValidationPlan.")
        if not self.expected_affected_files:
            raise ValueError("Remediation intent requires expected affected files.")
        if not self.deterministic_evidence:
            raise ValueError("Remediation intent requires deterministic evidence.")
        if not self.project_governance_rules:
            raise ValueError("Remediation intent requires Project governance rules.")
        if self.executable_patch or self.source_mutation_allowed:
            raise ValueError("Remediation intents are non-executable and non-mutating.")
        if self.frozen_path_impact in {"FROZEN", "TOUCHES_FROZEN"}:
            if self.action_class in {"FIX_NOW", "SAFE_MECHANICAL_FIX_AVAILABLE"}:
                raise ValueError("Frozen-path rules cannot be overridden by advice.")
            if self.mechanical_safety != "BLOCKED_BY_FREEZE":
                raise ValueError("Frozen-path impact requires BLOCKED_BY_FREEZE.")
        if self.ai_hypothesis is not None:
            if self.target_issue_fingerprint not in (
                self.ai_hypothesis.supporting_issue_fingerprints
            ):
                raise ValueError("AI hypothesis must cite the target issue fingerprint.")
