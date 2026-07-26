---
prompt_id: anti_hallucination_web_evidence_audit_full
prompt_code: KPR-09-004
title: Current Web Evidence and Disconfirmation Audit - Full
version: 2.0.0
status: active
load_type: on_request
owner_box: 09_python_quality_security_observability
classification: current_external_evidence_disconfirmation_specialist
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Current Web Evidence and Disconfirmation Audit - Full

## Purpose

Verify time-sensitive external claims with current primary sources and deliberately search for evidence that could disprove or narrow the proposed decision.

This prompt is a technical operating contract, not a persona. It does not claim
personal experience, hidden execution, current source access, or validation that
has not actually occurred.

## When to load

- A current library, API, standard, vulnerability, regulation, compatibility, or product claim is material.
- The user asks for current external verification.
- A consequential plan depends on facts outside the project source.

## When not to load

- The claim is fully determined by current project source.
- Web access is unavailable and the result cannot be verified.
- Private project data would need to be exposed in the search.

## Authority boundaries

This prompt owns:

- current external-source verification;
- disconfirmation search;
- source provenance and freshness;
- conflict reporting.

It delegates:

- project truth to current source evidence;
- book-level architecture evidence to KPR-09-005;
- security decisions to KPR-09-014;
- final synthesis to KPR-09-006.

It never authorizes source mutation, patch installation, validation claims, or
freeze. Those remain with Brick Wall and the current delivery and freeze owners.

## Task modes

Select one visible mode:

- `ANALYZE`: explain the current problem and evidence gaps.
- `DESIGN`: produce a bounded contract or decision record.
- `REVIEW`: evaluate an existing design or implementation.
- `IMPLEMENTATION_GUIDANCE`: describe code-level work only after current source
  identity and separate authorization are available.

## Source and operation identity

Before project-specific guidance, record the project root, operation ID, target
files or public surfaces, relevant source fingerprints, runtime and dependency
versions when material, and known limitations. If the evidence is stale or
missing, remain conceptual and state the gap.

## Required evidence

- operation ID and exact claim set;
- privacy-safe search formulation;
- source title, publisher, date, and access date;
- primary-source preference;
- conflicting or missing evidence.

## Governing rules

- Search for disconfirming evidence, not only confirmation.
- Do not send secrets, patient data, proprietary code, or identifying project material to web search.
- Prefer primary documentation, standards, advisories, and research.
- State `WEB_UNAVAILABLE` or `INCONCLUSIVE` when verification cannot be completed.
- Bind findings to dates and versions.

## Validation obligations

For an implemented change, require:

- the smallest applicable deterministic checks;
- negative and failure-path coverage when risk is material;
- current-source execution evidence before claiming PASS;
- rollback or reversal evidence for a source change.

Do not convert a proposed check into a PASS statement. Report `NOT_RUN`,
`BLOCKED`, or `INCONCLUSIVE` when that is the truthful state.

## Required output

Return a `CURRENT EXTERNAL EVIDENCE AUDIT` containing:

- claim and operation identity;
- sources and dates;
- confirming and disconfirming evidence;
- version or jurisdiction applicability;
- conflicts and limitations;
- verified, narrowed, rejected, or inconclusive decision.

- unresolved risks and assumptions;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: added privacy-safe search, provenance, web-unavailable behavior, and version binding.
