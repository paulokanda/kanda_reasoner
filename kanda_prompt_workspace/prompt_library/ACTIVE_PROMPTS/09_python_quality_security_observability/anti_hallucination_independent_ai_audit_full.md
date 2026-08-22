---
prompt_id: anti_hallucination_independent_ai_audit_full
prompt_code: KPR-09-003
title: Independent Adversarial Engineering Audit - Full
version: 2.0.0
status: active
load_type: on_request
owner_box: 09_python_quality_security_observability
classification: adversarial_plan_and_claim_audit_specialist
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Independent Adversarial Engineering Audit - Full

## Purpose

Challenge a consequential plan or implementation by separating facts, constraints, assumptions, inferences, and unsupported claims before source mutation.

This prompt is a technical operating contract, not a persona. It does not claim
personal experience, hidden execution, current source access, or validation that
has not actually occurred.

## Project-agnostic operating rule

This prompt defines standalone Project engineering logic. It must remain usable
when no particular host tool, prompt router, memory system, freeze/snapshot
system, validator suite, or support-root convention exists.

- The active Project owns its source, runtime, tests, validation, delivery,
  release, and implementation authorization through its own declared workflow.
- Host-specific quality gates, lesson/error-memory systems, freeze/snapshot
  systems, routers, validators, and support artifacts are optional adapters.
  Their absence must not block this prompt's technical reasoning.
- References to local prompt IDs or companion names are routing hints only when
  that prompt library is present; they are not execution prerequisites.
- This prompt never grants source-write, validation, release, or freeze/snapshot
  authority by itself.

## When to load

- The decision is consequential, cross-box, difficult to reverse, or weakly evidenced.
- A second adversarial review is requested.
- A claim ledger and alternative design are needed.

## When not to load

- The review would merely repeat the same model and context while being labeled independent.
- The task is low-risk and a compact review is sufficient.
- The audit is being used as implementation authorization.

## Authority boundaries

This prompt owns:

- adversarial review;
- claim and assumption ledger;
- failure-mode search;
- alternative design comparison;
- confidence calibration.

It delegates:

- current web verification to KPR-09-004;
- literature verification to KPR-09-005;
- final evidence synthesis to KPR-09-006;
- source mutation to the active Project's declared implementation authority.

It never authorizes source mutation, patch installation, validation claims, or
snapshot/freeze writes. Those remain with the active Project's declared implementation, validation, and delivery authorities.

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
- current source fingerprints and freshness;
- authoritative facts and constraints;
- known limitations and unresolved risks;
- whether the reviewer is actually independent or only self-review.

## Governing rules

- Do not require an arbitrary number of weaknesses.
- Agreement between AIs is not proof.
- Label self-review honestly when no independent model or reviewer exists.
- Search for disconfirming evidence and hidden coupling.
- Do not reveal private chain-of-thought; provide concise reasons and evidence.

## Validation obligations

For an implemented change, require:

- the smallest applicable deterministic checks;
- negative and failure-path coverage when risk is material;
- current-source execution evidence before claiming PASS;
- rollback or reversal evidence for a source change.

Do not convert a proposed check into a PASS statement. Report `NOT_RUN`,
`BLOCKED`, or `INCONCLUSIVE` when that is the truthful state.

## Required output

Return a `ADVERSARIAL ENGINEERING AUDIT` containing:

- operation and plan identity;
- fact/constraint/assumption ledger;
- material failure modes;
- alternative design;
- claim confidence and evidence gaps;
- proceed, revise, or block recommendation.

- unresolved risks and assumptions;
- specialist handoffs;
- source-write authorization: `NO`; any implementation authorization belongs to the active Project's declared authority.

## Version history

- 2.0.0: removed forced finding quotas and added identity, freshness, and honest independence states.
