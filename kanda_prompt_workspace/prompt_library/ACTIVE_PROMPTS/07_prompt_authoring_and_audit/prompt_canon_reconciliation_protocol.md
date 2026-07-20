---
prompt_id: prompt_canon_reconciliation_protocol
title: Prompt Canon Reconciliation Protocol
version: 2.0
status: active
load_type: on_request
owner_box: 07_prompt_authoring_and_audit
---

# Prompt Canon Reconciliation Protocol

## Purpose

Resolve how audited prompt ideas and competing Prompt Library assets should affect the canonical active set without creating duplicate owners or losing useful behavior.

This prompt owns the create-versus-update-versus-link-versus-consolidate lifecycle decision. It does not perform source mutation.

## Required evidence

Before a final decision, require:

- completed audit evidence for the target and relevant overlaps;
- exact current source, metadata, routes, fingerprints, and lifecycle state;
- current owner prompts and public contracts;
- generated-artifact provenance;
- relevant compact Error Memory lessons;
- latest applicable freeze context;
- project-specific generalization record when imported material is involved.

If evidence is stale or ownership cannot be resolved, return `BLOCKED_NEEDS_EVIDENCE`.

## Reconciliation principles

1. Prefer one canonical semantic owner per responsibility.
2. Reuse before adding.
3. Preserve useful dissonant behavior by moving it to the correct owner rather than deleting it silently.
4. Do not create a coordination registry, context engine, or super-prompt merely to manage overlap.
5. Separate global canon, project overlay, template, reference, historical artifact, and generated distribution.
6. Generated copies must derive from canonical source and must not become editing authority.
7. A lifecycle decision does not authorize implementation.

## Decision order

Apply this order and stop at the first sufficient outcome:

1. `REJECT`
2. `REFERENCE_ONLY`
3. `USE_EXISTING_UNCHANGED`
4. `PROJECT_OVERLAY`
5. `UPDATE_EXISTING`
6. `LINK_OR_REGISTER_EXISTING`
7. `CONSOLIDATE_INTO_EXISTING_OWNER`
8. `DEPRECATE_AND_MIGRATE`
9. `DELETE_AFTER_MIGRATION`
10. `CREATE_NEW_PROMPT`

`CREATE_NEW_PROMPT` requires a verified responsibility gap that no current owner can satisfy adequately.

## Owner reconciliation

For every relevant responsibility, record:

- canonical owner;
- source of truth;
- public contract;
- authorized mutation owner;
- consumers;
- competing assets;
- competitor disposition: retire, adapter, distinct responsibility, or unresolved;
- migration and compatibility needs.

No competing prompt may retain independent semantic or mutable-state authority without evidence of a distinct responsibility.

## Identity and lifecycle rules

- Preserve stable `prompt_id` when behavior remains substantially continuous.
- Use aliases for historical identities.
- Request `prompt_identity_code_registry_canon` for code allocation, rename, move, split, merge, replacement, or retirement.
- Activation, validation, freeze eligibility, and frozen state are separate lifecycle dimensions.
- Do not mark a recommendation as active, validated, or frozen before the corresponding action and evidence exist.

## Migration plan

A correction plan must identify:

- exact canonical files to update;
- files to deprecate or delete after migration;
- aliases and replacement references;
- routing and folder registration changes;
- generated artifacts to regenerate through canonical generators;
- validators to update or add;
- compatibility consumers;
- rollback boundary;
- freeze impact.

## Required output

Return a `PROMPT CANON RECONCILIATION RECORD` containing:

- reconciliation ID;
- exact source snapshot and fingerprints;
- prompts and owners compared;
- responsibility matrix;
- dissonant behavior preserved;
- primary lifecycle decision;
- target canonical owner;
- migration plan;
- identity decision required: `YES/NO`;
- insertion/registration required: `YES/NO`;
- startup-maintenance impact: `YES/NO`;
- delivery impact: `YES/NO`;
- freeze impact: `YES/NO`;
- unresolved blockers;
- source-write authorization: `NO`.

## Dispatch

- Prompt quality evidence: `prompt_audit_canon`.
- External-project abstraction: `project_specific_prompt_generalization`.
- Identity and code: `prompt_identity_code_registry_canon`.
- Authorized mutation: `prompt_insertion_and_router_registration_protocol`.
- Release artifacts: current Class 05 delivery owners.
- Freeze: current freeze owners after local validation and human confirmation.

## Non-authorization rule

This protocol produces a governed decision and migration design. Brick Wall must separately authorize implementation against current source before any file is changed.
