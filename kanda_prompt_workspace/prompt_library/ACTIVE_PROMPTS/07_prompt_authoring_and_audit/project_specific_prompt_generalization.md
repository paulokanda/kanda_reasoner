---
prompt_id: project_specific_prompt_generalization
title: Project-Specific Prompt Generalization
version: 2.0
status: active
load_type: on_request
owner_box: 07_prompt_authoring_and_audit
---

# Project-Specific Prompt Generalization

## Purpose

Analyze prompt material from another project or domain and determine how its useful behavior can be reused without importing foreign assumptions, private data, stale roots, or duplicate ownership.

This prompt is an analysis specialist. It does not authorize Prompt Library writes.

## Use when

Use this prompt when the source material comes from another project, domain, historical workspace, handoff, roadmap, or prompt system and the task is to:

- extract a reusable engineering pattern;
- remove project-specific contamination;
- decide between a global canon and a project overlay;
- preserve necessary domain constraints while improving reuse;
- recommend reuse, update, registration, reference-only retention, or rejection.

Do not use it for ordinary prompt editing that does not involve external-project or domain-specific material.

## Required context

Before a final decision, inspect:

- the exact source material and its source hash;
- source project, date, authority, and reuse status;
- sensitive or confidential content classification;
- current related Prompt Library prompts, metadata, folder card, and routing assets;
- `prompt_audit_canon` and `prompt_canon_reconciliation_protocol`;
- the current active project, Tool root, Project root, support root, and transient root when paths appear in the source.

## Generalization procedure

1. Record provenance and classify the source as current, historical, advisory, generated, or unknown.
2. Redact credentials, patient information, personal data, proprietary identifiers, and unrelated private paths before reuse.
3. Separate transferable behavior from project-specific nouns, labels, file names, UI text, hardware, regulations, clinical assumptions, and deployment constraints.
4. Preserve a domain constraint when removing it would weaken safety, correctness, or the actual behavior contract.
5. Search existing Prompt Library owners before proposing any new prompt.
6. Apply this preference order:
   - reject as non-transferable or unsafe;
   - use an existing prompt unchanged;
   - keep a project-specific overlay or folder card;
   - update an existing canonical prompt;
   - link or register an existing asset;
   - create a new prompt only when no current owner is sufficient and the gap is verified.
7. Compare the proposed generalized result with the source for semantic loss, false universality, lost exceptions, weakened validation, and changed intent.
8. Dispatch the recommendation to the correct Class 07 owner.

## Result classifications

Use exactly one primary result:

- `REJECTED`
- `REFERENCE_ONLY`
- `USE_EXISTING`
- `PROJECT_OVERLAY`
- `REUSABLE_TEMPLATE`
- `UPDATE_EXISTING`
- `LINK_OR_REGISTER_EXISTING`
- `NEW_PROMPT_CANDIDATE`
- `BLOCKED_NEEDS_EVIDENCE`

`NEW_PROMPT_CANDIDATE` is not implementation authorization.

## Required output

Return a `GENERALIZATION RECORD` containing:

- source identity, authority, date, and hash;
- sensitive-content and redaction decision;
- transferable behavior;
- necessary domain constraints retained;
- contamination removed;
- existing owners inspected;
- semantic-loss findings;
- primary result classification;
- recommended owner and target asset;
- unresolved risks;
- required next Class 07 prompt;
- source-write authorization: `NO`.

## Owner dispatch

- Read-only prompt quality and overlap evidence: `prompt_audit_canon`.
- Create, update, consolidate, deprecate, link, or reject decision: `prompt_canon_reconciliation_protocol`.
- Prompt identity and KPR code: `prompt_identity_code_registry_canon`.
- Authorized source, metadata, folder, and route mutation: `prompt_insertion_and_router_registration_protocol`.
- Installable bundle: Class 05 delivery owners only after authorization.
- Freeze: current freeze owners only after local validation and human confirmation.

## Non-authorization rule

A completed generalization record does not authorize source writes, routing changes, generated-artifact regeneration, patch delivery, or freeze. Brick Wall and the applicable implementation owner must authorize those actions separately.
