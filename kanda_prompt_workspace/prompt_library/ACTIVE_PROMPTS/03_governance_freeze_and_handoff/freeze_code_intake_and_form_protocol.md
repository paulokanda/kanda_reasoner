---
prompt_id: freeze_code_intake_and_form_protocol
prompt_code: KPR-03-003
title: Freeze Hint and Form Intake Protocol
version: 2.3
status: active
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: freeze-formulary-unified-json-transport-v1
---

# Freeze Hint and Form Intake Protocol

## Purpose

Own the boundary that carries one validated feature's freeze information into
the selected Active Project's external freeze-intake state. Preserve current
validation evidence, reject stale or ambiguous intake, and keep Preview plus
Confirm and Write explicitly human-controlled.

This prompt does not own patch construction, installation, PowerShell, evidence
merging implementation, Error Memory schemas, or the freeze writer engine.


## Freeze semantic boundary

Freeze is a durable governance register of one already validated effective
implementation state. Its job is to preserve future context: what was validated,
which Box owns it, which paths and contracts must not regress, and which exact
state later sessions may rely on.

Freeze does not implement, repair, execute, or validate the feature. Freeze does
not become a second patch engine, architecture engine, or Error Memory engine.

Default Freeze scope is exactly one effective feature/revision and its current
validated state. Do not synthesize a cumulative or multi-patch Freeze by default.
A cumulative/baseline Freeze is allowed only when the human explicitly requests
and approves that distinct operation before candidate preparation.

`KANDA_FREEZE_HINT.json` is Freeze-intake handoff/evidence when present or when a
Freeze-loader artifact owns it. The existence of a Freeze Hint does not define
whether an ordinary source implementation is valid or capable of being frozen
later; source-patch validation remains owned by Class 05 delivery governance.

## Accepted intake sources

Use only one current feature identity from:

- a validated `KANDA_FREEZE_HINT.json` from the exact current Freeze-intake or release artifact, when that artifact actually provides one;
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

## AI candidate pre-output companion

When the AI is about to emit, approve, correct, or regenerate a local freeze
candidate/form, load `KPR-03-008 freeze_candidate_pre_output_audit` before
output. That specialist owns the zero-trust candidate audit; this intake prompt
remains the owner of validated-feature intake and the human Preview/Confirm
boundary.

Patch-owned `KANDA_FREEZE_HINT.json` and patch-governance forms remain with
their release owner and must not be forced through the manual external-AI
transport schema.

## Canonical generic receive-ready template

This is the canonical manual Freeze GUI blueprint mirrored by the `Get Blueprint
Freeze` button. Use it only after `KPR-03-008 freeze_candidate_pre_output_audit`
has passed. If current receiver/source behavior differs, fail closed and reconcile
this prompt plus the GUI blueprint before emitting a candidate.

<!-- KANDA_FREEZE_GENERIC_TEMPLATE_BEGIN -->
KANDA FREEZE FORM - GENERIC RECEIVE-READY TEMPLATE v4

Use this structure only after the strict pre-output governance audit has passed.

```json
{
  "feature_title": "<EXACT EFFECTIVE NON-SUPERSEDED FEATURE TITLE>",
  "primary_box": "<EXACT PROJECT-RELATIVE OWNING BOX OR PATH>",
  "box_type": "<EXACT SUPPORTED TYPE>",

  "validated_files": [
    "<ONLY FILES ACTUALLY COVERED BY CURRENT VALIDATION>"
  ],

  "generated_files": [],

  "protected_paths": [
    "<EVIDENCE-BACKED PROTECTED PATH>",
    "project_freeze_after_update/frozen_features_memory/"
  ],

  "do_not_regress_rules": [
    "<VALIDATED BEHAVIORAL OR ARCHITECTURAL CONTRACT>",
    "<SECOND VALIDATED CONTRACT>",
    "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.",
    "Do not store project-specific frozen memory inside project_freeze_ledger.",
    "Preview Freeze Entry must remain read-only and must not write files.",
    "Confirm and Write must require explicit human confirmation before writing governed freeze memory.",
    "After a local freeze write, the AI startup freeze context must be refreshed."
  ],

  "validation_evidence_summary": [
    "<EXACT CURRENT FEATURE-SPECIFIC PASS MARKER>",
    "<OTHER EXACT CURRENT VALIDATION MARKER IF GENUINELY PRODUCED>",
    "VALIDATION OK: <EXACT_CURRENT_FEATURE_ID>",
    "STATUS: IN_SYNC"
  ],

  "known_warnings": "<STATE ONLY REAL WARNINGS. DISTINGUISH CURRENT VALIDATION FROM HISTORICAL EVIDENCE. IF AN ORIGINAL PATCH ZIP IS UNAVAILABLE, SAY SO. IF ZIP CONTRACT: PASS WAS NOT GENUINELY PRODUCED FOR THIS EXACT RELEASE, DO NOT CLAIM IT. USE n/a ONLY IF THERE ARE GENUINELY NO MATERIAL WARNINGS.>",

  "planned_next_step": "<ONLY ACTION THAT REMAINS GENUINELY PENDING AFTER THE COMPLETE CURRENT CONFIRM AND WRITE TRANSACTION HAS FINISHED. DO NOT REPEAT PREVIEW, CONFIRM AND WRITE, HINT CONSUMPTION, STARTUP/COMPLIANCE REFRESH, INDEXING, OR ANY WRITER/GUI-OWNED ACTION ALREADY COMPLETED. IF NO IMMEDIATE ACTION REMAINS, STATE A FUTURE DURABLE TRIGGER SUCH AS VERIFYING THIS FROZEN CONTRACT IN A LATER SESSION OR CREATING ANOTHER FREEZE ONLY FOR A SEPARATELY VALIDATED LATER REVISION/CORRECTION.>",

  "notes": "Release owner: <KANDA_TOOL_RELEASE | EXTERNAL_PROJECT_RELEASE | NOT_APPLICABLE>. Effective non-superseded feature: <EXACT_FEATURE_ID>. Governing source patch ZIP: <EXACT_PATCH_ZIP_IF_GENUINELY_KNOWN_OR_n/a>. Governing patch SHA-256: <EXACT_SHA256_IF_GENUINELY_KNOWN_OR_n/a>. <SHORT DURABLE SUMMARY OF WHAT THIS FEATURE FREEZES>. <STATE SUPERSESSION RELATIONSHIP ONLY IF VERIFIED>. Project-specific durable frozen memory belongs under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory and not project_freeze_ledger."
}
```

MANDATORY TEMPLATE RULES

1. Never replace unknown information with guessed information.
2. `validated_files` means validated files, not merely related files.
3. For the unified Freeze receiver, `generated_files` must be `[]` when there are no generated files. Never create a synthetic `"n/a"` path entry.
4. `protected_paths` must be evidence-backed and use the verified owner namespace/root convention.
5. `validation_evidence_summary` contains evidence, not rewritten interpretations. Prefer literal validator output when possible.
6. The exact current feature must have `VALIDATION OK: <exact_feature_id>` and `STATUS: IN_SYNC` before the candidate may be emitted.
7. A subordinate checker marker may support the evidence but never substitutes for the exact current-feature marker.
8. Include `ZIP CONTRACT: PASS` only when that exact marker was genuinely produced for the exact release and is applicable to the classified release owner.
9. Historical evidence must be explicitly identifiable as historical when material.
10. Never insert writer-owned fields: `freeze_id`, writer status, writer timestamp/date, owner metadata, durable entry path, `freeze_store_kind`, or `superseded_by`.
11. Before output, inspect the actual current freeze store for an existing same-feature freeze, duplicates, predecessors, superseded entries, conflicting active revisions, and legitimate correction/replacement state.
12. If the required current-state check cannot be performed, stop with `FREEZE CANDIDATE NOT READY`. Do not guess.
13. Classify release provenance as `KANDA_TOOL_RELEASE`, `EXTERNAL_PROJECT_RELEASE`, or `NOT_APPLICABLE` before applying ZIP-specific rules. Never hardcode one release-owner class into a generic template.
14. Resolve every path-bearing field against its actual owner root. Never add or strip `_show_project_to_AI`, `first_prompt_files`, `project_freeze_after_update`, or another prefix by intuition.
15. Treat `KANDA_FREEZE_HINT.json` according to the artifact class: it is governed evidence for a manual candidate, while patch-owned freeze artifacts may have a stricter same-source contract.
16. Before output, strictly parse exactly one JSON object, reject duplicate object keys, reject non-standard `NaN`/`Infinity` constants, verify the exact 11-field schema and field types, and ensure no writer-owned field or chat/tool artifact leaked into the object.
17. Never send a schema-invalid failure object to the Freeze receiver. If a mandatory gate fails, return ordinary chat beginning exactly with `FREEZE CANDIDATE NOT READY` and emit no Freeze JSON candidate.
18. Never send a candidate first and audit it afterward. The candidate shown to the user must already have passed JSON/schema validation, exact feature identity, current freeze-store and supersession audit, validation-evidence and provenance audit, ownership/path audit, complete durable post-write transaction simulation, and a second independent audit.
19. `planned_next_step` must remain true after the full current Confirm and Write transaction returns. It must not repeat Preview, Confirm and Write, automatic hint consumption, startup/compliance refresh, indexing, or another writer/GUI-owned action already completed by that transaction.
20. The canonical AI-produced Freeze candidate is one raw 11-field JSON object with array-valued multiline fields and no mandatory marker or Markdown envelope. Legacy marker/fence input may be accepted by the receiver only as compatibility input.
21. If current receiver/source behavior differs from this template, fail closed and reconcile this prompt plus `Get Blueprint Freeze` before emitting a candidate.
<!-- KANDA_FREEZE_GENERIC_TEMPLATE_END -->

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
- Default Freeze is one exact validated effective implementation state; cumulative/multi-patch Freeze requires prior explicit human approval.
- Freeze Hint is intake evidence/handoff, not the implementation or validation authority for an ordinary source patch.
- Unknown or stale state fails closed.
- Preview remains read-only.
- Confirm and Write remains explicitly human.
- External AI review remains advanced or fallback, not normal freeze authority.
