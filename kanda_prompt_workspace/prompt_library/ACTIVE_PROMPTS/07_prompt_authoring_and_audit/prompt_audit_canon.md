---
prompt_id: prompt_audit_canon
aliases:
  - pyarchitect_prompt_audit_canon
title: Prompt Audit Canon
version: 2.0
status: active
load_type: on_request
owner_box: 07_prompt_authoring_and_audit
---

# Prompt Audit Canon

## Purpose

Provide the canonical read-only method for auditing Prompt Library assets one primary target at a time.

The audit identifies identity drift, duplicated responsibility, conflicting owners, stale references, generated-as-source leakage, lifecycle problems, missing validation, and useful dissonant behavior. It produces evidence and recommendations only.

## Authority boundary

This prompt may inspect source, metadata, fingerprints, routes, generated distributions, validators, Error Memory, freeze context, and related prompts.

It must not modify:

- prompt source or metadata;
- routing, indexes, folder cards, or generated artifacts;
- validators or application code;
- Error Memory or freeze memory;
- project state.

A prompt audit is not implementation authorization.

## One-primary-target rule

1. Open one prompt as the primary audit target.
2. Related prompts may be opened only as comparison evidence.
3. Do not silently convert a related prompt into another primary target.
4. Complete the target report, disposition, fingerprint record, dependency record, and closure record before opening the next primary target.
5. Preserve independent evidence and conclusions for every audited prompt.

## Adaptive sequential batches

Choose the next batch before beginning it:

- 3 prompts for governance-heavy, startup-loaded, routing, freeze, Brick Wall, patch-delivery, or highly interconnected targets;
- 5 prompts for normal complexity;
- up to 8 prompts only for short, isolated targets with clear ownership and few dependencies.

After each batch, record audited targets, dispositions, owner conflicts, dependencies, focused-verification needs, context reliability, and the exact next unopened prompt.

Stop when source identity is unresolved, required evidence is unavailable, two sources appear equally authoritative, context reliability is declining, or safe continuation would require mutation.

## Required evidence

Inspect, when applicable:

- exact canonical source and SHA-256 fingerprint;
- metadata and lifecycle fields;
- aliases, prompt codes, and canonical path;
- folder and group registration;
- human and machine routing;
- generated copies and their generator ownership;
- active references and consumers;
- focused and cumulative validators;
- relevant compact Error Memory lessons;
- latest human-confirmed freeze context;
- current canonical owners for overlapping responsibilities.

Generated artifacts are evidence, not source authority.

## Audit procedure

1. Resolve current Tool, Project, support, and transient roots.
2. Resolve the exact primary source and distinguish canonical, generated, historical, and duplicate copies.
3. Inventory source identity, metadata, size, encoding, version, status, load type, owner, prompt code, routes, validators, and fingerprints.
4. State the prompt's unique capability in one sentence.
5. Identify what the prompt should own and what it must delegate.
6. Compare only with related source actually inspected.
7. Classify each relationship as:
   - `DISTINCT`
   - `PARTIAL_OVERLAP`
   - `SAME_IDEA_CONFLICTING_OWNER`
   - `DUPLICATE`
   - `SUPERSEDED`
   - `UNRESOLVED`
8. Extract useful dissonant logic that must be preserved during reconciliation.
9. Record findings by severity and cite exact evidence.
10. Recommend one lifecycle disposition.
11. Define focused verification required before correction.
12. Close the target formally.

## Disposition vocabulary

Use one primary recommendation:

- `KEEP`
- `UPDATE`
- `CONSOLIDATE`
- `LINK_OR_REGISTER`
- `PROJECT_OVERLAY`
- `REFERENCE_ONLY`
- `DEPRECATE`
- `DELETE_AFTER_MIGRATION`
- `REJECT`
- `BLOCKED_NEEDS_EVIDENCE`

Separate current status from recommended final status. Do not describe a proposed state as already implemented.

## Required audit report

Each report must include:

- audit ID and date;
- prompt filename, prompt ID, prompt code, title, and canonical path;
- source and metadata fingerprints;
- current lifecycle and load type;
- exact sources inspected;
- unique capability assessment;
- positive findings;
- numbered findings with severity and evidence;
- overlap and owner analysis;
- dissonant logic to preserve;
- recommended owner model;
- recommended final structure;
- smallest safe correction plan;
- required validation after correction;
- applicable Error Memory lessons;
- Brick Wall read-only status;
- final disposition;
- human-decision requirement;
- closure record.

## Class 07 dispatch

- External-project abstraction: `project_specific_prompt_generalization`.
- Canonical create/update/consolidate/deprecate decision: `prompt_canon_reconciliation_protocol`.
- Identity or KPR code decision: `prompt_identity_code_registry_canon`.
- Authorized mutation and registration: `prompt_insertion_and_router_registration_protocol`.

## Closure rule

The final line of every primary-target report must state that the target was formally closed and that no source, metadata, routing, generated artifact, validator, Error Memory, freeze memory, or project state was modified during the audit.
