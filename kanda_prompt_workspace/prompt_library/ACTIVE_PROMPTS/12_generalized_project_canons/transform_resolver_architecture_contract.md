---
prompt_id: transform_resolver_architecture_contract
prompt_code: KPR-12-014
title: Transform Resolver Architecture Contract
version: 2.0.0
status: active
load_type: on_request
owner_box: 12_generalized_project_canons
classification: pure_versioned_transform_resolution_contract
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Transform Resolver Architecture Contract

## Purpose

Resolve a versioned base identity and ordered transform plan against capabilities and policy into a structured operation result without performing the operation.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

## When to load

- Stable identities and selectable transforms must resolve into controlled operations.
- UI, API, plugin, validator or persistence layers risk duplicating transform-selection logic.
- Precedence, capability, conflict or unsupported states need one resolver.

## When not to load

- The task is pipeline lineage/rebuild ownership; use KPR-12-009.
- No transform selection or identity mapping exists.
- Execution rather than resolution is the only concern.

## Authority boundaries

This prompt owns:

- typed/versioned base identity;
- ordered transform plan and parameters;
- capability and applicable-policy inputs;
- precedence, conflict and compatibility resolution;
- structured result states and decision trace;
- resolver profile/version identity.

It delegates:

- operation execution to the runtime owner;
- pipeline lineage/rebuild/invalidation to KPR-12-009;
- UI state and presentation to the UI owner;
- authorization policy to security/domain owners.

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

- base identity and schema/version;
- ordered transforms, parameters and source of selection;
- capability set and policy version;
- precedence/conflict/unsupported rules;
- operation registry and consumer contracts.

## Governing rules

- Keep resolution pure and side-effect-free.
- Return structured states such as RESOLVED, UNSUPPORTED, CONFLICT, AMBIGUOUS, INVALID and STALE rather than silently selecting a fallback.
- Define transform order and precedence explicitly; do not rely on UI click order.
- Include resolver/profile version and a decision trace in the result.
- Do not execute operations, mutate pipelines, write persistence, or rebuild caches inside the resolver.
- Reject stale async results when base identity, transform plan, capability set or policy version changed.
- Bind concrete operations to stable registry identities rather than scattered conditional branches.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `TRANSFORM RESOLUTION RECORD` containing:

- base/plan/capability/policy identities;
- precedence and compatibility rules;
- structured resolution result;
- decision trace and profile version;
- stale-result behavior;
- execution and pipeline handoffs.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO` unless separately granted by Brick Wall.

## Version history

- 2.0.0: expanded input/result states, formalized transform order and precedence, and separated pure resolution from execution and pipeline rebuild.
