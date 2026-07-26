---
prompt_id: anti_hallucination_master_protocol_full
prompt_code: KPR-09-006
title: Evidence Synthesis and Truthful Status Protocol - Full
version: 2.0.0
status: active
load_type: on_request
owner_box: 09_python_quality_security_observability
classification: final_evidence_synthesis_truthful_status_protocol
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Evidence Synthesis and Truthful Status Protocol - Full

## Purpose

Synthesize already-produced project, adversarial, current-source, literature, validation, and limitation records into one truthful decision state.

This prompt is a technical operating contract, not a persona. It does not claim
personal experience, hidden execution, current source access, or validation that
has not actually occurred.

## When to load

- The full verification train has produced stage records.
- A consequential decision needs one final evidence status.
- Conflicting evidence or unresolved blockers must be summarized.

## When not to load

- No upstream evidence records exist.
- The prompt would be used as a mega-canon replacing specialists.
- Implementation authorization is being inferred from synthesis.

## Authority boundaries

This prompt owns:

- evidence-state synthesis;
- conflict and limitation summary;
- truthful status vocabulary;
- next-evidence recommendation.

It delegates:

- all evidence generation to the exact stage owners;
- implementation authorization to Brick Wall;
- delivery validation and freeze to current owners.

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

- operation ID and plan hash;
- stage versions and record hashes;
- project source freshness;
- observed validation markers;
- known warnings and unresolved risks.

## Governing rules

- Do not duplicate specialist canons.
- Do not convert consensus into proof.
- Use `VERIFIED`, `PARTIALLY_VERIFIED`, `INCONCLUSIVE`, `BLOCKED`, or `REJECTED` with reasons.
- Preserve contradictions instead of averaging them away.
- Never claim PASS for a command that was not executed.

## Validation obligations

For an implemented change, require:

- the smallest applicable deterministic checks;
- negative and failure-path coverage when risk is material;
- current-source execution evidence before claiming PASS;
- rollback or reversal evidence for a source change.

Do not convert a proposed check into a PASS statement. Report `NOT_RUN`,
`BLOCKED`, or `INCONCLUSIVE` when that is the truthful state.

## Required output

Return a `FINAL EVIDENCE SYNTHESIS RECORD` containing:

- operation identity;
- input record inventory and hashes;
- supporting and conflicting evidence;
- validation state;
- limitations and residual risk;
- final truthful status and next step.

- unresolved risks and assumptions;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: radically reduced from a duplicated mega-canon to the final evidence-synthesis stage.
