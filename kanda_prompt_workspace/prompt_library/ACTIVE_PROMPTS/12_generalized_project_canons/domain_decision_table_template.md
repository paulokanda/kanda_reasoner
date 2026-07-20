---
prompt_id: domain_decision_table_template
prompt_code: KPR-12-011
title: Versioned Domain Decision Table Template
version: 2.0.0
status: active
load_type: on_request
owner_box: 12_generalized_project_canons
classification: versioned_deterministic_domain_decision_table_template
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Versioned Domain Decision Table Template

## Purpose

Represent multiple discrete domain rules as an explicit, versioned, testable decision table with precedence, coverage, traceability, and controlled unknown behavior.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

## When to load

- Multiple discrete rules must be evaluated consistently.
- Aliases, classifications, contradictions, defaults, or manual review states need a matrix.
- A deterministic decision trace is required.

## When not to load

- The decision is continuous, probabilistic, or better represented by code/model logic.
- Only one simple rule exists.
- Authorization policy or domain meaning has not been defined by its owner.

## Authority boundaries

This prompt owns:

- decision-table identity, version and scope;
- rule IDs, priority and match semantics;
- coverage, exclusivity and default/unknown policy;
- decision trace and effective-date lifecycle;
- table-level test matrix.

It delegates:

- domain meaning and invariants to the domain owner;
- input schema to validation owners;
- override authorization to security/policy owners;
- audit retention and UI presentation to their owners.

Brick Wall and the current patch, validation, terminal, and freeze owners retain
implementation and release authority.

## Task modes

Choose one visible mode:

- `ANALYZE`: identify the current state, evidence, and gaps.
- `DESIGN`: produce a bounded contract or decision record.
- `REVIEW`: evaluate an existing artifact or implementation.
- `IMPLEMENTATION_GUIDANCE`: describe source work only after exact source and
  separate authorization are available.

## Required evidence

- normalized input schema and domain owner;
- rule inventory and precedence basis;
- known overlap/contradiction/default cases;
- effective dates and version compatibility;
- authorized override and trace-retention policy.

## Governing rules

- Every rule must have a stable rule ID, version/effective range, priority and outcome.
- Define exact match semantics and normalization boundaries.
- Prove or explicitly state table completeness and mutual exclusivity; otherwise define conflict and unknown states.
- A default is a policy decision, not a silent implementation convenience.
- Overrides require separate authorization and must not be universally available.
- Freeze, logging, warnings and UI presentation are conditional handoffs, not mandatory table behavior.
- Return a decision trace containing matched rules, precedence, inputs used and final state.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `DOMAIN DECISION TABLE RECORD` containing:

- table identity/version/scope;
- input normalization boundary;
- rules and precedence;
- coverage/conflict/default policy;
- decision trace schema;
- test matrix and lifecycle.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: added rule identity, precedence, coverage, traceability, effective dates, and separated domain policy from table representation.
