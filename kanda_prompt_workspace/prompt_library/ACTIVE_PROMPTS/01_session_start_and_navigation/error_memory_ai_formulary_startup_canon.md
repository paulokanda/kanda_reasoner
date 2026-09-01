---
prompt_id: error_memory_ai_formulary_startup_canon
prompt_code: KPR-01-012
title: Error Memory AI Formulary Startup Canon
version: 4.4
status: active
load_type: always_startup
owner_box: 01_session_start_and_navigation
source_stage: error-memory-library-machine-card-decoupling-v1
---

# Error Memory AI Formulary Startup Canon

## Purpose

This is the single always-startup admission and workflow canon for the Error
Memory lesson library.

Error Memory records reusable prevention lessons from demonstrated failures. It
is not the Architecture Review Machine-Card lifecycle and must never be routed
through MCard merely because KANDA Reasoner is the Tool that displays or edits
the lessons.

## Architecture boundary

Keep these concepts separate:

```text
KANDA Reasoner Tool / selected Project lifecycle
-> project_tool_boundary_canon
-> architecture_review_project_card_machine_canon only when its triggers apply

Error Memory
-> reusable library of error and prevention lessons
-> this canon plus the current Error Memory lesson runtime
```

The selected Project may be evidence context for a lesson. It does not turn the
lesson into a Project card, inserted card, Architecture Review target, or MCard
lifecycle object.

KANDA self-hosting may make Tool and selected-Project roots physically equal.
That never collapses the logical Tool and Project roles and does not change Error
Memory into MCard.

## Runtime naming compatibility

Current KANDA source may still contain historical implementation names such as
`kanda_reasoner_app.error_memory_card` or private `_mcard_*` helper filenames.
Those names are compatibility implementation details only.

Do not infer from them that:

- Error Memory is an MCard;
- a lesson has CARD_INSERTED/CARD_EJECTED lifecycle;
- Architecture Review card identity owns Error Memory;
- `card_id` is required for lesson admission or Error Memory ZIP intake;
- KPR-12-005 is an Error Memory owner.

A future source cleanup may rename those implementation files independently.
This canon owns the semantic separation now.

## Activation

Apply this canon when:

- an install, validation, packaging, routing, architecture, runtime, prompt, or
  delivery error is diagnosed and corrected;
- a repeated failure suggests a reusable prevention rule;
- the user asks to memorize, update, audit, retire, delete, forget, export, or
  package an Error Memory lesson;
- a patch carries Error Memory intake material;
- an existing lesson may be duplicate, stale, incomplete, draft, or retired.

A transient typo or one-off mistake with no reusable prevention value should not
become durable Error Memory.

## Lesson-library authority

The current installed Error Memory runtime and current Error Memory GUI behavior
are the compatibility authority for lesson storage and lifecycle.

Canonical stored lesson lifecycle states are:

- `active`;
- `draft`;
- `retired`.

`pending` remains a transport/staging state for `To memorize` intake material.
When a candidate is admitted into the Error Memory tab work surface, normalize
its in-tab review status to `draft` regardless of transport status. Pending is
not the in-tab review state.

Do not create `deprecated` or `superseded` as new lifecycle states. Historical
data may be normalized by the application.

The following fields must not be invented merely to force Tool/Project ownership
into a reusable prevention lesson:

```text
owner_scope
owner_id
owner_slug
owner_root_fingerprint
affected_box
import_provenance
```

`origin` is provenance. `applicability` describes where the lesson is useful.
Neither is MCard authority.

## Admission check

Return this record before creating or updating lesson content:

```text
ERROR MEMORY ADMISSION CHECK
Error event present: YES / NO
Repeatable prevention value: YES / NO / UNCERTAIN
Current lesson ID match:
Fingerprint or prevention-trigger overlap:
Current lifecycle status:
Disposition:
- NEW_PENDING_LESSON
- UPDATE_EXISTING_DRAFT
- RETIRE_EXISTING
- DUPLICATE_DO_NOT_CREATE
- CONFLICT_REQUIRES_HUMAN_REVIEW
- TRANSIENT_DO_NOT_MEMORIZE
Compact lesson-library context sufficient: YES / NO
Full lesson-library context needed: YES / NO
Exact source needed: YES / NO
Correction evidence available: YES / NO
Active-ready evidence available: YES / NO
Candidate status: pending / draft
Intended status after human approval: active / draft
Selected Project relevance: NONE / CONTEXT_ONLY / DIRECT_EVIDENCE
Human Memorize Error still required: YES / NO
Reason:
```

For a transport/staged AI-prepared lesson, `status: pending` remains compatible
with the intake queue. On admission to the Error Memory tab, KANDA must normalize
the visible working lesson to `status: draft` and remove transport-only intended
status from the in-tab review copy. A directly pasted/imported lesson is also
normalized to `draft`, even if the incoming JSON said `active`.

`Memorize Error` is the single human promotion gate: an active-ready in-tab
`draft` is promoted to `active` and saved. An incomplete or invalid draft remains
`draft`, is not consumed as successfully memorized, and must report the missing
active-ready items. `Mark Draft` is not a prerequisite for normal intake; it is
reserved for intentionally persisting or returning a lesson to draft.

Never fabricate an active-ready lesson when evidence is unresolved.

## Duplicate, conflict, edit, and retirement rule

Compare stable lesson IDs, symptoms, exception fingerprints, prevention triggers,
root cause, correct fix, and regression obligations.

- Same lesson ID with materially different content is a conflict.
- Same prevention fingerprint and semantic lesson is a duplicate.
- Update an existing draft only when explicitly authorized.
- Do not silently overwrite active, pending, draft, or retired lessons.
- Retire obsolete durable lessons when their identity must remain known.
- Delete only accidental, test, corrupt, or intentionally unwanted entries.
- A replacement lesson may be recorded as metadata without inventing another
  lifecycle state.

## Compact and full library policy

Read the smallest useful Error Memory context first. Inspect the full lesson
library only when duplicate checking, repeated-error debugging, conflict review,
audit, or the user's request requires it.

Error Memory is prevention guidance, not source truth. Current source, runtime
evidence, validators, and observed behavior control implementation decisions.

### External Project observer scope

For KANDA Reasoner Tool repairs, current compact Error Memory remains a governed
prevention input. For independent external `PROJECT_ACTOR` development, Tool Error
Memory is optional advisory context: use it when supplied and relevant, but its
absence, staleness, or unavailable full ZIP must not block Project source
inspection, coding, testing, validation, release, or rollback. Project-owned
evidence and validators remain authoritative for the Project.

Do not request KANDA Reasoner source or source archives merely to satisfy an Error
Memory lesson while implementing an external Project.

## Correction track and prevention track

A correction patch repairs code, prompts, or workflow behavior. The Error Memory
lesson records how to prevent recurrence. Neither track substitutes for the
other.

A successful correction is evidence, not automatic approval to activate memory.
Incoming or corrected lessons shown in the Error Memory tab remain `draft` until
the human explicitly presses `Memorize Error`.

## Runtime delivery compatibility

The default Error Memory exchange must work in both source/IDE and frozen
PyInstaller runtimes.

A PyInstaller runtime may embed CPython and application modules without exposing
a standalone interpreter executable under `_internal`. Never assume that a
portable package contains any of these executable paths:

```text
_internal/python.exe
_internal/.venv/Scripts/python.exe
_internal/venv/Scripts/python.exe
```

When the running Tool is frozen/PyInstaller, or when no independent external
Tool Python executable has been explicitly verified, do not use an executable
Error Memory intake ZIP that depends on `RUN_INSTALL.ps1`, a packaged Python
loader, or a discovered `TOOL_PYTHON`.

Use the native application-mediated path instead:

```text
marker-wrapped Error Memory lesson
-> Error Memory GUI intake
-> normalized and persisted as draft
-> human review
-> Memorize Error only after approval
```

The GUI may still import a passive lesson ZIP, JSON, TXT, or MD file inside the
already-running application. That in-app import is distinct from the
Python-dependent self-contained execution ZIP and does not require a standalone
`python.exe`.

## Strict pre-output lesson transport gate

Before the AI emits, approves, corrects, or regenerates any Error Memory lesson
that is intended for `Paste error formatted from AI` or equivalent direct GUI
intake, it MUST also apply `KPR-12-003 error_memory_active_ready_json_template`.

This is a final output gate, not a suggestion. A lesson is not receive-ready merely
because its JSON object is semantically correct. The complete visible transport
text must satisfy the current Error Memory receiver contract before it is shown
to the user.

When the lesson is ready, the final visible response MUST be exactly:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ ... exactly one valid JSON object ... }
KANDA_ERROR_LESSON_JSON_END
```

Pre-output transport audit requirements:

1. The first visible characters are the literal token
   `KANDA_ERROR_LESSON_JSON_BEGIN`.
2. The last visible characters are the literal token
   `KANDA_ERROR_LESSON_JSON_END`.
3. Each marker occurs exactly once and in the correct order.
4. The content between the markers parses as exactly one JSON object.
5. There is no Markdown code fence, writing-block wrapper, citation, commentary,
   label, heading, or prose before, inside around, or after the transport block.
6. Do not Markdown-escape the marker underscores. Literal forms such as
   `KANDA\_ERROR\_LESSON...` are invalid transport.
7. Do not emit a second JSON object or an explanatory sentence after the end
   marker.
8. Validate the complete outgoing text, not only the inner JSON object.

If the application reports `MCARD_FORMATTED_LESSON_JSON_REQUIRED`, treat that
as a legacy implementation error token for malformed Error Memory lesson
transport. It does NOT route the lesson through Architecture Review MCard. The
correct response is to repair the Error Memory marker-wrapped transport using
KPR-12-003 and the current Error Memory runtime contract.

If the lesson content is not ready, ordinary fail-closed explanation may be
returned. If the lesson content IS ready, no prose may accompany the final
receive-ready block.

## Output modes

Choose the smallest safe mode:

1. Marker-wrapped Error Memory lesson JSON for direct application-mediated
   review. This is the default and the required Portable/FROZEN route.
2. Application-mediated review followed by explicit human `Memorize Error`.
3. A self-contained pending lesson-intake ZIP through
   `KPR-05-008 self_contained_error_memory_lesson_intake_zip` only in
   source/IDE mode after an independent external Tool Python executable has been
   explicitly verified.

Do not route an Error Memory lesson through
`architecture_review_project_card_machine_canon` unless a separate Architecture
Review operation independently triggers that prompt.

## Storage and selected-Project rule

The Error Memory storage owner is the current installed Error Memory runtime.
Do not derive lesson storage from the MCard metaphor.

The selected Project may contribute evidence or relevance context. It must not be
used to reinterpret Error Memory lessons as Project-card lifecycle state.

Error Memory lesson handling must not mutate Active Project selection merely to
read, stage, or review lessons.

## Redaction and export safety

Before output or staging:

- remove secrets, credentials, patient data, and unnecessary personal paths;
- preserve only evidence needed to understand and prevent the failure;
- mark uncertainty honestly;
- keep incomplete candidates as draft;
- keep structured arrays as arrays;
- validate outgoing lesson data against the current Error Memory runtime when
  available.

## Human gate

The AI may prepare or stage reviewable pending transport lessons when authorized.
KANDA normalizes every candidate admitted into the Error Memory tab work surface
to `draft`.

The final `Memorize Error` action remains explicit and human-controlled. It
promotes an active-ready `draft` to `active`. A ZIP installer must never press,
imitate, or call that action and must never turn a new staged lesson directly
into active.

## Failure behavior

When admission, duplicate classification, schema compatibility, or evidence is
unresolved, return:

```text
ERROR MEMORY INTAKE BLOCKED
Disposition:
Missing evidence:
Conflicting lesson ID:
Fingerprint conflict:
Redaction unresolved:
Next safe action:
May stage pending lesson: NO
May create active lesson automatically: NO
Human Memorize Error still required: YES
```

## Scope exclusions

This prompt does not define:

- Architecture Review MCard lifecycle;
- CARD_INSERTED/CARD_EJECTED semantics;
- GUI widget implementation;
- PowerShell or patch ZIP implementation;
- terminal cleanup;
- Freeze-form structure;
- Brick Wall Q01-Q40 details;
- a second Error Memory engine.

## Do-not-regress rules

- Error Memory is a lesson library, not Machine-Card/MCard.
- KPR-12-005 remains the Architecture Review card lifecycle specialist.
- Historical `error_memory_card` or `_mcard_*` module names do not grant MCard
  semantics to Error Memory.
- New AI-created lessons may stage as pending transport, enter the tab as draft, and become active only through human Memorize Error.
- Never silently replace same-ID or same-fingerprint conflicts.
- Keep correction evidence separate from prevention evidence.
- Preserve redaction and export safety.
- Preserve Tool/Project logical separation independently of Error Memory.
- Tool Error Memory must never become an execution prerequisite for independent external Project development.

<!-- KANDA_ADDENDUM:error_memory_ownerless_project_identity_parity:v1r2 -->

## Ownerless Error Memory lesson identity

Error Memory lesson JSON is reusable lesson-library data.

- Project/owner identity fields are not lesson JSON fields.
- Tool or selected Project information is context only and must not be emitted as lesson ownership.
- Historical lessons may still contain legacy identity metadata; compatibility reading does not make that metadata required for new AI output.
