---
prompt_id: freeze_code_intake_and_form_protocol
prompt_code: KPR-03-003
title: Freeze Hint and Form Intake Protocol
version: 2.0
status: active
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: prompt-audit-wave4a-governance-freeze-handoff-v1
---

# Freeze Hint and Form Intake Protocol

## Purpose

Own the boundary that carries one validated feature's freeze information into
the selected Active Project's external freeze-intake state. Preserve current
validation evidence, reject stale or ambiguous intake, and keep Preview plus
Confirm and Write explicitly human-controlled.

This prompt does not own patch construction, installation, PowerShell, evidence
merging implementation, Error Memory schemas, or the freeze writer engine.

## Accepted intake sources

Use only one current feature identity from:

- a validated root-level `KANDA_FREEZE_HINT.json` from the exact patch ZIP;
- a current project-owned freeze-hint intake record;
- an explicit manual form completed from verified local evidence.

Do not infer a freeze record from chat memory, terminal appearance, an old ZIP,
a generated startup archive, or a consumed prior identity.

## Freeze intake record

```text
FREEZE INTAKE RECORD
Active Project root:
Project Support root:
Feature ID:
Feature title:
Primary box:
Exact source patch ZIP:
Validated files:
Generated files:
Protected paths:
Do-not-regress rules:
Validation evidence file:
Required VALIDATION OK marker:
Required STATUS: IN_SYNC marker:
Known warnings:
Intake freshness: CURRENT / STALE / UNKNOWN
Prior identity consumed: YES / NO / UNKNOWN
Preview allowed: YES / NO
Confirm and Write still human: YES
Blocking reason:
```

## Intake gates

1. Resolve Tool, Active Project, Project Support, and transient roots through the
   current Tool/Project owner.
2. Match the feature ID, patch identity, validated files, and evidence markers.
3. Require local validation evidence for the current installed source.
4. Reject missing mandatory fields, starter placeholders, stale evidence,
   mismatched patch identity, consumed records, and unlisted source states.
5. Keep failed validation and known warnings visible. Do not rewrite them as
   success.
6. Store project-specific intake only under the selected Project Support owner.
7. Never write project-specific freeze memory into the reusable
   `project_freeze_ledger` blueprint.

## Human freeze boundary

`Preview Freeze Entry` is read-only. It may display the proposed record but must
not write canonical freeze memory.

`Confirm and Write` requires explicit human confirmation after Preview. The AI
must never click, simulate, infer, or report that confirmation.

After a successful local write, refresh the startup freeze context before a new
session relies on it.

## Fail-closed output

```text
FREEZE INTAKE BLOCKED
Feature identity:
Missing or conflicting evidence:
Stale or consumed state:
Next safe action:
Preview allowed: NO
Confirm and Write allowed: NO
```

## Scope exclusions

Route detailed work to its owner:

- patch ZIP and installer: Class 05 delivery owners;
- validation evidence production: the feature validator;
- Error Memory admission: the Error Memory canon;
- documentary routing: durable artifact canon;
- terminal behavior: terminal cleanup contract;
- freeze writer implementation: current application owner.

## Do-not-regress rules

- One current feature identity per intake.
- Unknown or stale state fails closed.
- Preview remains read-only.
- Confirm and Write remains explicitly human.
- External AI review remains advanced or fallback, not normal freeze authority.
