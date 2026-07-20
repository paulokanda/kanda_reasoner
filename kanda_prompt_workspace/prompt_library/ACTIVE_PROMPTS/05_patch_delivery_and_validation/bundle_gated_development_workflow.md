---
prompt_id: bundle_gated_development_workflow
prompt_code: KPR-05-002
title: Bundle-Gated Development Workflow
version: 2.0
status: active
load_type: routed
owner_box: 05_patch_delivery_and_validation
source_stage: prompt-audit-wave5a-patch-lifecycle-core-v1
---

# Bundle-Gated Development Workflow

## Purpose

Decide whether a governed change needs an installable or distributable release
unit, track that release through its lifecycle, and dispatch each artifact or
gate to its current specialist owner. This prompt owns release lifecycle and
coordination only. It does not authorize coding, define ZIP membership, write
installers, render terminal footers, create freeze forms, or define Error Memory
schemas.

## Activate when

Use when the requested result must be delivered as a patch ZIP, installable
bundle, distributable migration, or other versioned release unit. Use it for an
atomic multi-owner contract migration only when one release unit is required to
keep the public contract coherent.

Do not load for explanation-only work, read-only audit, a local edit that will
not be packaged, or routine use of an already installed feature.

## Required prior evidence

Before release work advances beyond `DRAFT`, obtain current evidence for:

- Brick Wall admission and task-specific implementation authorization;
- exact source and current metadata fingerprints;
- relevant Error Memory and active PIR regression classes;
- one primary box and bounded supporting touches;
- artifact, receiver, installer, validation, and terminal owners;
- current Tool, Active Project, Project Support, and transient-root identity.

A previous release PASS does not authorize a new source state.

## Release unit

A release unit is the smallest installable or distributable change that keeps
one primary responsibility coherent. Separate unrelated concerns. A bounded
atomic migration may include several owners only when splitting it would create
an invalid intermediate public contract. Every supporting touch must identify
its owner, reason, and public contract.

## Release lifecycle

```text
RELEASE WORKFLOW STATUS
Feature ID:
Release unit:
Primary box:
Supporting owners:
Release type:
Installable artifact required: YES / NO
Brick Wall authorization:
Exact source verified:
Relevant Error Memory reviewed:
Active PIR classes reviewed:
Artifact-contract owner:
Receiver-contract owner:
Installer-contract owner:
Validation owner:
Sandbox validation status:
Exact final ZIP contract status:
Windows-local installation status:
Windows-local validation status:
Release disposition:
- NOT_APPLICABLE
- DRAFT
- PACKAGED
- CONTRACT_VALIDATED
- INSTALLED
- LOCALLY_VALIDATED
- REJECTED
- REPAIR_REQUIRED
- FREEZE_ELIGIBLE
- FROZEN
Next safe action:
May release artifact: YES / NO
```

State changes require current evidence. A sandbox or disposable-copy PASS is not
Windows-local installation or validation. Installation success is not validation
success. Validation success is not human freeze confirmation.

## Failure and repair

- Reject unknown source fingerprints, undeclared payload members, unsafe archive
  names, wrong-root writes, and receiver ambiguity before mutation.
- Preserve exact failure phase, exception type, message, and last successful
  marker.
- Repair the smallest failing owner. Do not weaken a baseline allowlist to admit
  an unexplained third state.
- Rollback must restore every changed or deleted file and verify restoration.
- Rebuild the release when source, validator, metadata, routing, or package
  identity changes.

## Specialist dispatch

- Brick Wall: admission, authorization, current gate state, and release decision.
- `project_tool_boundary_canon`: root identities and project-linked transient
  staging.
- Class 04 owners: primary box, supporting touches, placement, and boundaries.
- `implementation_and_delivery_protocol`: surgical payload, baseline policy,
  backup, install transaction, and rollback.
- Patch governance and receiver contracts: exact ZIP membership, extraction,
  intake, and destination proof.
- `pre_output_contract_gates`: final outgoing artifact authorization.
- `terminal_cleanup_contract`: PowerShell prompt and cleanup behavior.
- Validation owners: exact commands, expected markers, and evidence provenance.
- Freeze owners: sidecar intake, Preview, Confirm and Write, and memory placement.
- Error Memory owners: lesson admission, schema, and regression obligations.

## Legacy identity

`kanda_bundle_gated_development_workflow` and the former application-local
`KANDA_BUNDLE_GATED_DEVELOPMENT_WORKFLOW.md` are historical aliases. The only
active owner is this canonical workspace prompt.

## Non-authorization statement

This workflow cannot authorize source writes, patch release, validation claims,
or freeze. It reports lifecycle evidence to Brick Wall and the current
specialist owners.

## Version history

- 2.0: reduced to release lifecycle and specialist dispatch; reconciled the
  duplicate application identity and current governance boundaries.
- 1.x: historical bundle methodology with embedded installer, terminal, freeze,
  Error Memory, and prompt-authoring detail.
