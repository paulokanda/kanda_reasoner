---
prompt_id: data_transform_pipeline_invariants
prompt_code: KPR-12-009
title: Data Transform Pipeline Invariants
version: 2.0.0
status: active
load_type: on_request
owner_box: 12_generalized_project_canons
classification: versioned_data_lineage_canonical_base_derived_output_canon
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Data Transform Pipeline Invariants

## Purpose

Preserve explicit lineage between acquired source, versioned canonical base, transform plan, and derived outputs across batch, incremental, and streaming pipelines.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

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

- Source-to-derived lineage or rebuild correctness is central.
- Transforms can drift, compound, reorder, or invalidate cached outputs.
- A pipeline needs explicit deterministic or nondeterministic modes.

## When not to load

- The task is only resolving UI selections into an operation; use KPR-12-014.
- No source/canonical/derived distinction exists.
- The task is domain policy rather than pipeline lineage.

## Authority boundaries

This prompt owns:

- source, canonical-base and derived-output identity;
- versioned lineage and transform-state provenance;
- rebuild, invalidation and cache-key requirements;
- declared batch, incremental and streaming modes;
- determinism profile and late-data/correction handling.

It delegates:

- transform combination and precedence resolution to KPR-12-014;
- domain invariants to the domain owner;
- storage mechanics to KPR-10-004;
- UI/view state to the relevant presentation owner.

This specialist does not own implementation or release authority. Those remain
with the active Project's declared implementation, validation, and delivery owners.

## Task modes

Choose one visible mode:

- `ANALYZE`: identify the current state, evidence, and gaps.
- `DESIGN`: produce a bounded contract or decision record.
- `REVIEW`: evaluate an existing artifact or implementation.
- `IMPLEMENTATION_GUIDANCE`: describe source work only after exact source and
  separate authorization are available.

## Required evidence

- source and canonical schema versions;
- ordered transform plan and parameters;
- pipeline mode and determinism profile;
- cache/invalidation/rebuild semantics;
- late-arriving data, corrections, deletion and privacy obligations.

## Governing rules

- Do not silently transform a previously derived output as though it were the canonical base.
- Canonical data may change only through an explicit versioned correction, migration, or accepted source update.
- Record whether transform order is commutative, intentionally ordered, or invalid.
- For incremental and streaming modes, define watermark, replay, deduplication, correction and late-data behavior.
- Derived outputs must record source/canonical version, transform-plan identity and implementation/profile version.
- Separate data-affecting state from view-only state.
- Declare nondeterminism, randomness, external model use or environment dependence instead of claiming deterministic rebuilds.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `DATA TRANSFORM LINEAGE RECORD` containing:

- source/canonical/output identities;
- pipeline mode and determinism profile;
- ordered transform plan;
- lineage and cache key;
- rebuild/invalidation/correction behavior;
- resolver and storage handoffs.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO`; any implementation authorization belongs to the active Project's declared authority.

## Version history

- 2.0.0: added versioned provenance, pipeline modes, nondeterminism, late-data, correction, and resolver boundaries.
