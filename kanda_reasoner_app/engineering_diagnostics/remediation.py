# project-path: kanda_reasoner_app/engineering_diagnostics/remediation.py
"""Deterministic non-mutating remediation intents and validation plans."""

from __future__ import annotations

import hashlib
from typing import Mapping

from .bom_adapter import BOM_PRODUCER_ID
from .collectors import (
    ARCHITECTURE_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    SHADOW_PRODUCER_ID,
)
from .enrichment_models import DiagnosticFindingEnrichment
from .fingerprinting import canonical_json
from .grouping_models import DiagnosticGroupRecord
from .lifecycle_models import DiagnosticLifecycleHead
from .models import DiagnosticFindingRecord, DiagnosticRunRecord
from .remediation_models import (
    DiagnosticAiHypothesis,
    DiagnosticRemediationIntent,
    DiagnosticValidationPlan,
)

__all__ = [
    "build_diagnostic_remediation_intent",
    "build_diagnostic_remediation_intents",
]

_TERMINAL_DO_NOT_TOUCH = frozenset(
    {"ACCEPTED_RISK", "FALSE_POSITIVE", "RESOLVED"}
)
_NON_ACTIVE_SCOPES = frozenset(
    {"GENERATED", "REFERENCE", "DEPRECATED", "WORKBENCH", "SNIPPET", "TEMPORARY"}
)
_REVIEW_SCOPES = frozenset({"TEST", "FIXTURE", "PROTOTYPE"})
_FROZEN = frozenset({"FROZEN", "TOUCHES_FROZEN"})


def _text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return _text(value).lower() in {"1", "true", "yes", "on"}


def _producer_validation(
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    focused = [
        "Reproduce issue " + finding.issue_fingerprint + " with its originating collector.",
        "Run focused tests for the canonical owner before any Patch Preview.",
    ]
    commands = [
        "ENGINEERING_DIAGNOSTICS:RERUN:" + run.producer_id,
        "KANDA:VALIDATE_PROJECT",
    ]
    if run.producer_id == BOM_PRODUCER_ID:
        commands.insert(0, "SOURCE_HYGIENE:BOM_SCAN:" + finding.relative_path)
    elif run.producer_id == RUFF_PRODUCER_ID:
        commands.insert(
            0,
            "RUFF:CHECK_JSON:" + finding.relative_path + ":" + finding.code,
        )
    elif run.producer_id == ARCHITECTURE_PRODUCER_ID:
        commands.insert(0, "ARCHITECTURE_REVIEW:SCAN_PROJECT")
    elif run.producer_id == SHADOW_PRODUCER_ID:
        commands.insert(0, "SOURCE_HYGIENE:SHADOW_AUDIT")
    return tuple(focused), tuple(commands)


def _validation_plan(
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
    enrichment: DiagnosticFindingEnrichment,
) -> DiagnosticValidationPlan:
    focused, commands = _producer_validation(run, finding)
    evidence = [
        "Originating collector completes with compatible coverage.",
        "Issue fingerprint is absent or intentionally retained with reviewed governance.",
        "Validate Project and architecture non-regression complete successfully.",
    ]
    if enrichment.frozen_path.status in _FROZEN:
        commands += ("FREEZE_MEMORY:REVIEW_GOVERNING_ENTRIES",)
        evidence.append("Governed Freeze impact is reviewed before source changes.")
    return DiagnosticValidationPlan(
        focused_tests=focused,
        validation_commands=commands,
        rollback_expectation=(
            "Capture exact original hashes for every affected file and restore them "
            "transactionally if focused or Project validation fails."
        ),
        evidence_required=tuple(evidence),
    )


def _evidence(
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
    enrichment: DiagnosticFindingEnrichment,
    groups: tuple[DiagnosticGroupRecord, ...],
    lifecycle_state: str,
) -> tuple[str, ...]:
    values = [
        "issue_fingerprint=" + finding.issue_fingerprint,
        "producer_id=" + run.producer_id,
        "code=" + finding.code,
        "relative_path=" + finding.relative_path,
        "scope=" + enrichment.scope.classification,
        "frozen_path=" + enrichment.frozen_path.status,
        "owner_status=" + enrichment.owner.status,
        "lifecycle_state=" + lifecycle_state,
    ]
    if enrichment.owner.canonical_owner:
        values.append("canonical_owner=" + enrichment.owner.canonical_owner)
    values.extend("governing_freeze_id=" + item for item in enrichment.frozen_path.governing_freeze_ids)
    values.extend("diagnostic_group=" + group.group_id for group in groups)
    if finding.suggested_action:
        values.append("producer_suggested_action=" + finding.suggested_action)
    for key in ("fix_available", "fix_applicability", "fix_message", "fix_edit_count", "fix_executed"):
        if key in finding.evidence:
            values.append(key + "=" + _text(finding.evidence.get(key)))
    return tuple(values)


def _intent_id(payload: Mapping[str, object]) -> str:
    digest = hashlib.sha256(
        ("engineering-diagnostics-remediation-intent-v1|" + canonical_json(payload)).encode(
            "utf-8"
        )
    ).hexdigest()
    return "remediation-" + digest


def _base_result(
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
    enrichment: DiagnosticFindingEnrichment,
    lifecycle_state: str,
) -> dict[str, object]:
    frozen = enrichment.frozen_path.status
    owner = enrichment.owner
    scope = enrichment.scope.classification
    result: dict[str, object] = {
        "action_class": "EVIDENCE_REQUIRED",
        "likely_correction": finding.suggested_action or "Collect exact evidence before proposing a correction.",
        "reason": "The current evidence does not prove a safe correction.",
        "canonical_owner": owner.canonical_owner,
        "required_governed_wave": "",
        "fix_applicability": "UNKNOWN",
        "mechanical_safety": "UNKNOWN",
        "semantic_review_requirement": "OWNER_REVIEW_REQUIRED",
        "uncertainty": "high",
        "primary_trust_source": "TOOL_DETERMINISTIC_METADATA",
        "rule_template_id": "kanda.remediation.evidence_required.v1",
    }

    if lifecycle_state == "SUPPRESSED":
        result.update(
            action_class="SUPPRESS_WITH_JUSTIFICATION",
            likely_correction="Retain suppression only while its reason and revisit condition remain valid.",
            reason="A human suppression decision is already active and the finding remains searchable.",
            fix_applicability="NOT_APPLICABLE",
            mechanical_safety="NOT_MECHANICAL",
            semantic_review_requirement="REQUIRED",
            uncertainty="low",
            rule_template_id="kanda.remediation.lifecycle.suppressed.v1",
        )
    elif lifecycle_state in _TERMINAL_DO_NOT_TOUCH:
        result.update(
            action_class="DO_NOT_TOUCH",
            likely_correction="Do not prepare a source correction unless the lifecycle decision is reopened.",
            reason="The current human lifecycle state blocks remediation progression.",
            fix_applicability="NOT_APPLICABLE",
            mechanical_safety="NOT_MECHANICAL",
            semantic_review_requirement="REQUIRED",
            uncertainty="low",
            rule_template_id="kanda.remediation.lifecycle.terminal.v1",
        )
    elif lifecycle_state == "DEFERRED":
        result.update(
            action_class="DEFERRED_TECHNICAL_DEBT",
            likely_correction="Continue only in the governed wave recorded by the lifecycle decision.",
            reason="The current human lifecycle state explicitly defers this finding.",
            required_governed_wave="LIFECYCLE_RELATED_WAVE",
            fix_applicability="PROJECT_GOVERNED",
            mechanical_safety="NOT_MECHANICAL",
            semantic_review_requirement="REQUIRED",
            uncertainty="low",
            rule_template_id="kanda.remediation.lifecycle.deferred.v1",
        )
    elif frozen in _FROZEN:
        result.update(
            action_class="PLAN_GOVERNED_WAVE",
            likely_correction=finding.suggested_action or "Plan a corrective governed wave before changing protected source.",
            reason="Current Freeze evidence has higher authority than remediation advice.",
            required_governed_wave="CORRECTIVE_WAVE_REQUIRED",
            fix_applicability="PROJECT_GOVERNED",
            mechanical_safety="BLOCKED_BY_FREEZE",
            semantic_review_requirement="REQUIRED",
            uncertainty="low",
            primary_trust_source="PROJECT_GOVERNANCE_RULE",
            rule_template_id="kanda.remediation.frozen_path.v1",
        )
    elif frozen == "UNKNOWN" or scope == "UNKNOWN":
        result.update(
            reason="Scope or Freeze impact is not proven.",
            rule_template_id="kanda.remediation.unknown_governance.v1",
        )
    elif scope in _NON_ACTIVE_SCOPES:
        result.update(
            action_class="DO_NOT_TOUCH",
            likely_correction="Do not modify this non-active source candidate as canonical code.",
            reason="The deterministic scope classifier does not identify active canonical source.",
            fix_applicability="NOT_APPLICABLE",
            mechanical_safety="NOT_MECHANICAL",
            semantic_review_requirement="REQUIRED",
            uncertainty="low",
            rule_template_id="kanda.remediation.non_active_scope.v1",
        )
    elif scope in _REVIEW_SCOPES:
        result.update(
            action_class="HUMAN_DECISION_REQUIRED",
            reason="Test, fixture, or prototype scope requires semantic owner review.",
            fix_applicability="EXACT_FILE",
            mechanical_safety="SEMANTIC_REVIEW_REQUIRED",
            semantic_review_requirement="REQUIRED",
            uncertainty="medium",
            rule_template_id="kanda.remediation.review_scope.v1",
        )
    elif owner.status == "NEEDS_REVIEW":
        result.update(
            action_class="HUMAN_DECISION_REQUIRED",
            reason="Multiple or non-canonical active owner candidates prevent automatic advice.",
            fix_applicability="UNKNOWN",
            mechanical_safety="SEMANTIC_REVIEW_REQUIRED",
            semantic_review_requirement="OWNER_REVIEW_REQUIRED",
            uncertainty="high",
            rule_template_id="kanda.remediation.owner_review.v1",
        )
    elif owner.status != "READY":
        result.update(
            action_class="EVIDENCE_REQUIRED",
            reason="Canonical ownership is not proven.",
            rule_template_id="kanda.remediation.owner_evidence.v1",
        )
    elif run.producer_id == BOM_PRODUCER_ID:
        result.update(
            action_class="SAFE_MECHANICAL_FIX_AVAILABLE",
            likely_correction=finding.suggested_action or "Remove only the exact UTF-8 BOM from the affected file.",
            reason="BOM evidence identifies one exact active unfrozen file and a canonical owner.",
            fix_applicability="EXACT_FILE",
            mechanical_safety="SAFE_MECHANICAL",
            semantic_review_requirement="NOT_REQUIRED",
            uncertainty="low",
            primary_trust_source="KANDA_RULE_TEMPLATE",
            rule_template_id="kanda.remediation.bom.exact_file.v1",
        )
    elif run.producer_id == RUFF_PRODUCER_ID:
        safe = _bool(finding.evidence.get("fix_available")) and _text(
            finding.evidence.get("fix_applicability")
        ).lower() == "safe"
        if safe:
            result.update(
                action_class="SAFE_MECHANICAL_FIX_AVAILABLE",
                likely_correction=_text(finding.evidence.get("fix_message"))
                or finding.suggested_action
                or "Apply only the exact Ruff-reported safe edit.",
                reason="Ruff reports a safe candidate for one active unfrozen owner; no fix has run.",
                fix_applicability="EXACT_SYMBOL" if finding.symbol_id else "EXACT_FILE",
                mechanical_safety="SAFE_MECHANICAL",
                semantic_review_requirement="NOT_REQUIRED",
                uncertainty="low",
                primary_trust_source="KANDA_RULE_TEMPLATE",
                rule_template_id="kanda.remediation.ruff.safe_fix.v1",
            )
        else:
            result.update(
                action_class="HUMAN_DECISION_REQUIRED",
                reason="Ruff did not prove a safe mechanical edit.",
                fix_applicability="EXACT_SYMBOL" if finding.symbol_id else "EXACT_FILE",
                mechanical_safety="SEMANTIC_REVIEW_REQUIRED",
                semantic_review_requirement="REQUIRED",
                uncertainty="medium",
                rule_template_id="kanda.remediation.ruff.semantic_review.v1",
            )
    elif run.producer_id in {ARCHITECTURE_PRODUCER_ID, SHADOW_PRODUCER_ID}:
        result.update(
            action_class="HUMAN_DECISION_REQUIRED",
            likely_correction=finding.suggested_action or "Review the canonical ownership and boundary evidence before planning a correction.",
            reason="Architecture and Shadow findings describe semantic ownership or boundary behavior.",
            fix_applicability="PROJECT_GOVERNED",
            mechanical_safety="SEMANTIC_REVIEW_REQUIRED",
            semantic_review_requirement="REQUIRED",
            uncertainty="medium",
            primary_trust_source="KANDA_RULE_TEMPLATE",
            rule_template_id="kanda.remediation.semantic_governance.v1",
        )
    return result


def build_diagnostic_remediation_intent(
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
    enrichment: DiagnosticFindingEnrichment,
    groups: tuple[DiagnosticGroupRecord, ...] = (),
    lifecycle_head: DiagnosticLifecycleHead | None = None,
    ai_hypothesis: DiagnosticAiHypothesis | None = None,
) -> DiagnosticRemediationIntent:
    """Build one read-only intent without calling AI or writing Project state."""
    lifecycle_state = lifecycle_head.current_state if lifecycle_head is not None else "OPEN"
    result = _base_result(run, finding, enrichment, lifecycle_state)
    deterministic = _evidence(run, finding, enrichment, groups, lifecycle_state)
    governance = (
        "Remediation intents are advice, not executable patches.",
        "Frozen-path rules override lower-trust remediation advice.",
        "Patch Preview requires separate exact-source governance and human confirmation.",
        "AI-assisted hypotheses cannot override deterministic or Project-governance evidence.",
    )
    payload = {
        "issue": finding.issue_fingerprint,
        "action": result["action_class"],
        "rule": result["rule_template_id"],
        "owner": result["canonical_owner"],
        "path": finding.relative_path,
        "frozen": enrichment.frozen_path.status,
        "freeze_ids": enrichment.frozen_path.governing_freeze_ids,
        "lifecycle": lifecycle_state,
    }
    return DiagnosticRemediationIntent(
        intent_id=_intent_id(payload),
        target_issue_fingerprint=finding.issue_fingerprint,
        action_class=str(result["action_class"]),
        likely_correction=str(result["likely_correction"]),
        reason=str(result["reason"]),
        canonical_owner=str(result["canonical_owner"]),
        expected_affected_files=(finding.relative_path,),
        frozen_path_impact=enrichment.frozen_path.status,
        governing_freeze_ids=enrichment.frozen_path.governing_freeze_ids,
        required_governed_wave=str(result["required_governed_wave"]),
        fix_applicability=str(result["fix_applicability"]),
        mechanical_safety=str(result["mechanical_safety"]),
        semantic_review_requirement=str(result["semantic_review_requirement"]),
        validation_plan=_validation_plan(run, finding, enrichment),
        uncertainty=str(result["uncertainty"]),
        primary_trust_source=str(result["primary_trust_source"]),
        rule_template_id=str(result["rule_template_id"]),
        deterministic_evidence=deterministic,
        project_governance_rules=governance,
        ai_hypothesis=ai_hypothesis,
        executable_patch=False,
        source_mutation_allowed=False,
    )


def build_diagnostic_remediation_intents(
    run: DiagnosticRunRecord,
    findings: tuple[DiagnosticFindingRecord, ...],
    enrichments: tuple[DiagnosticFindingEnrichment, ...],
    group_index: Mapping[str, tuple[DiagnosticGroupRecord, ...]],
    lifecycle_index: Mapping[tuple[str, str], DiagnosticLifecycleHead],
    ai_hypotheses: Mapping[str, DiagnosticAiHypothesis] | None = None,
) -> tuple[DiagnosticRemediationIntent, ...]:
    """Build intents in one pass for high-volume GUI projection."""
    if len(findings) != len(enrichments):
        raise ValueError("findings and enrichments must have equal length.")
    hypotheses = ai_hypotheses or {}
    return tuple(
        build_diagnostic_remediation_intent(
            run,
            finding,
            enrichment,
            tuple(group_index.get(finding.issue_fingerprint, ())),
            lifecycle_index.get(("ISSUE", finding.issue_fingerprint)),
            hypotheses.get(finding.issue_fingerprint),
        )
        for finding, enrichment in zip(findings, enrichments)
    )
