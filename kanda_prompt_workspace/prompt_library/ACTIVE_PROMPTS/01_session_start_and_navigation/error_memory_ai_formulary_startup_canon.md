---
prompt_id: error_memory_ai_formulary_startup_canon
prompt_code: KPR-01-012
title: Error Memory AI Formulary Startup Canon
version: 2.0
status: active
load_type: always_startup
owner_box: 01_session_start_and_navigation
source_stage: prompt-audit-wave3b-specialist-startup-bridges-v1
---

# Error Memory AI Formulary Startup Canon

## Purpose

This is the single always-startup workflow and admission owner for Error Memory
intake. It decides whether an observed error has durable prevention value, whether
an existing lesson should be updated or superseded, which current schema owner is
needed, and which output mode is safe.

It does not define the complete lesson schema, GUI implementation, patch ZIP
layout, terminal behavior, or direct storage internals.

## Activation

Apply this canon when:

- an install, validation, packaging, routing, architecture, or runtime error is
  diagnosed and corrected;
- a repeated failure suggests a reusable prevention rule;
- the user explicitly asks to memorize, update, audit, or forget an Error Memory
  lesson;
- a patch carries Error Memory intake material;
- an existing lesson may be duplicate, stale, draft, or superseded.

A transient typo or one-off mistake with no reusable prevention value should not
become durable Error Memory.

## Admission check

Return this record before creating or updating lesson content:

```text
ERROR MEMORY ADMISSION CHECK
Error event present: YES / NO
Repeatable prevention value: YES / NO / UNCERTAIN
Existing lesson match:
Fingerprint or trigger overlap:
Disposition:
- NEW_LESSON
- UPDATE_EXISTING_DRAFT
- SUPERSEDE_EXISTING
- DUPLICATE_DO_NOT_CREATE
- TRANSIENT_DO_NOT_MEMORIZE
Compact Error Memory sufficient: YES / NO
Full Error Memory needed: YES / NO
Exact source needed: YES / NO
Correction evidence available: YES / NO
Active-ready evidence available: YES / NO
Output status: draft / active
Human Memorize Error still required: YES
Reason:
```

If the event, prevention value, or disposition is unresolved, do not fabricate an
active lesson.

## Duplicate and supersession rule

Compare lesson IDs, symptoms, exception fingerprints, prevention triggers,
source owners, and regression obligations. A wording difference alone does not
justify a new lesson.

- Update an existing draft when it describes the same failure and remains the
  current owner.
- Supersede when the prior lesson is materially incomplete or its diagnosis is
  replaced by stronger evidence.
- Do not create a duplicate active lesson for the same prevention contract.
- Keep unrelated lessons distinct even when they occurred in the same patch.

## Compact and full Error Memory policy

Read the compact export first. Open the full Error Memory only when the compact
record requests it, repeated-error debugging needs full context, the user asks
for an audit, compact context is insufficient, or the proposed plan conflicts
with an earlier lesson.

Error Memory is prevention guidance, not source truth. Exact current source and
runtime evidence still control implementation decisions.

## Correction track and prevention track

A correction patch repairs the project. The Error Memory lesson records how to
prevent recurrence. Neither track substitutes for the other.

Do not mark a lesson active merely because a correction was proposed. Active
status requires enough grounded evidence, a usable prevention rule, and a
regression obligation. Otherwise use `draft`.

## Current schema owners

Route exact lesson fields and templates to the existing Class 12 owners:

- `error_memory_model_template` for the general lesson model;
- `error_memory_active_ready_json_template` for active-ready JSON structure;
- `error_memory_active_ready_correction_blueprint` for draft-to-active or
  corrective updates.

Use current application behavior as the final compatibility check. Do not copy
complete schemas into this startup prompt.

## Output modes

Choose the smallest safe mode:

1. Marker-wrapped content-only JSON for review or transfer.
2. Pending project intake when the user requests staging or the governed patch
   workflow requires it.
3. Application-mediated review and explicit human Memorize Error action.

Do not write directly into canonical Lessons from this prompt. Do not treat ZIP
installation as human approval.

## Redaction and export safety

Before output or staging:

- remove secrets, credentials, patient data, and unnecessary personal paths;
- preserve only evidence required to understand and prevent the failure;
- mark uncertainty honestly;
- use draft status when redaction or evidence completeness is unresolved;
- validate the exact outgoing JSON through the current schema owner when tools
  are available.

## Project ownership

Project-specific Error Memory belongs under the selected project's Project
Support root. Derive Tool, Project, Project Support, and transient paths through
`project_tool_boundary_canon`. Do not write project-specific lessons into the
reusable freeze ledger or another project's support root.

## Human gate

The AI may prepare or stage reviewable intake only when authorized. The final
Memorize Error action remains explicit and human-controlled. Existing active
memory must not be overwritten silently.

## Failure behavior

When admission or schema compatibility is unresolved, return:

```text
ERROR MEMORY INTAKE BLOCKED
Disposition:
Missing evidence:
Schema owner required:
Redaction unresolved:
Next safe action:
May create active lesson: NO
Human Memorize Error still required: YES
```

## Scope exclusions

This prompt does not define:

- complete JSON field lists or templates;
- GUI widgets, timers, refresh behavior, or source filenames;
- PowerShell or patch ZIP implementation;
- terminal cleanup;
- freeze-form structure;
- direct writes into canonical Lessons;
- Brick Wall Q01-Q40 details;
- a new memory engine, schema, or registry.

## Do-not-regress rules

- Keep one admission and workflow owner.
- Prefer update or supersession over duplicate lesson creation.
- Read compact memory first and full memory only when justified.
- Keep correction evidence separate from prevention evidence.
- Use draft status when active-ready evidence is incomplete.
- Route exact schemas to Class 12 owners.
- Preserve redaction and explicit human Memorize Error control.
