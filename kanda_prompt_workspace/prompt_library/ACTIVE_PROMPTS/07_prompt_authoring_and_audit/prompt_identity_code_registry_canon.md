---
prompt_code: KPR-07-002
prompt_id: prompt_identity_code_registry_canon
title: Prompt Identity Code Registry Canon
version: 2.0
status: active
load_type: routed
owner_box: 07_prompt_authoring_and_audit
---

# Prompt Identity Code Registry Canon

## Purpose

Define stable Prompt Library identity, KPR code allocation, aliases, path continuity, and retirement behavior.

The current library is partially migrated. Metadata distributed with each prompt is the canonical identity source. Do not create a new central registry unless a separately verified problem proves distributed metadata inadequate.

## Identity model

A prompt identity consists of:

1. `prompt_code`: stable human-copyable address when assigned;
2. `prompt_id`: stable machine identity;
3. current canonical path and display title.

Aliases preserve historical IDs, titles, paths, and codes without creating a second active owner.

## Which assets require a KPR code

A KPR code is required for:

- always-startup prompts;
- routed prompts selected directly by code;
- user-facing prompts that must be reliably copy/paste-addressable;
- replacement targets that must preserve a stable redirect.

A code is optional for:

- narrow on-request prompts addressed reliably by prompt ID and path;
- templates, references, metadata-only assets, and folder cards;
- deprecated historical source with no active route.

Do not invent codes during read-only audits. Code assignment requires a reconciliation decision and current uniqueness check.

## Code format

Use:

`KPR-<folder_number>-<sequence>`

Rules:

- folder number matches the current primary ACTIVE_PROMPTS class;
- sequence is three digits;
- codes are never reused after retirement;
- a move across classes requires an explicit compatibility decision;
- aliases and redirects preserve the old address when needed.

## Current stable code examples and Class 07 reservations

- `KPR-03-001 = brick_wall_comprehensive_quality_gate`
- `KPR-03-002 = cooperative_implementation_methodology`
- `KPR-03-003 = freeze_code_intake_and_form_protocol`
- `KPR-03-004 = pre_output_contract_gates`
- `KPR-03-005 = professional_engineering_governance_template`
- `KPR-03-006 = workflow_handoff_template`
- `KPR-07-001 = prompt_insertion_and_router_registration_protocol`
- `KPR-07-002 = prompt_identity_code_registry_canon`

Other Class 07 prompts remain addressable by prompt ID and path until a specific direct-addressability need is approved.

## Canonical metadata identity fields

Use the current metadata schema consistently:

- `prompt_code`, when assigned;
- `prompt_id`;
- `display_name`;
- `filename`;
- `category`;
- `version`;
- `status`;
- `load_type`;
- `owner_box`;
- `canonical_path`;
- `aliases`;
- `source_stage`;
- `updated_for`;
- `trigger_phrases`;
- `required_companion_prompts`.

Source front matter and metadata must agree on assigned code, prompt ID, version, status, load type, and owner.

## Allocation procedure

1. Consume the reconciliation decision explaining why a code is needed.
2. Inspect current metadata, active sources, navigation assets, aliases, replacements, and retired identities.
3. Verify the candidate code is unused and not reserved.
4. Record old and new identity fields.
5. Define compatibility behavior for routes and consumers.
6. Hand the approved identity record to `prompt_insertion_and_router_registration_protocol`.

## Rename, move, split, merge, and replacement

- Rename: keep prompt ID and code when responsibility is continuous; add old title/path aliases.
- Move within the same class: normally retain code and prompt ID; update path and aliases.
- Move across classes: retain or replace the code only through an explicit compatibility decision.
- Split: retain the original identity for the continuing primary responsibility; assign new identities only to genuinely distinct responsibilities.
- Merge: choose one canonical surviving identity; reserve retired codes and add replacement references.
- Replacement: preserve a machine-resolvable redirect from the retired identity.
- Retirement: never reissue the retired code.

## Validation requirements

Verify:

- code format and uniqueness;
- folder-number compatibility;
- source and metadata alignment;
- alias uniqueness and non-circular redirects;
- canonical path existence;
- retired-code reservation;
- route and consumer compatibility;
- no generated artifact treated as canonical source.

## Required output

Return a `PROMPT IDENTITY DECISION` containing:

- prompt ID;
- assigned or retained code, or `NO_CODE_REQUIRED`;
- title and canonical path;
- aliases and retired addresses;
- allocation evidence;
- move/split/merge/replacement behavior;
- affected consumers and routes;
- validation obligations;
- implementation owner: `prompt_insertion_and_router_registration_protocol`;
- source-write authorization: `NO`.

## Authority boundary

This canon does not audit semantic duplication, insert files, register routes, render routing-choice output, regenerate startup delivery, package patches, or freeze changes.
