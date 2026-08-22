# Architecture Review Project Card Machine Canon

Version: 3.0
Status: Active prompt-library canon
Prompt ID: architecture_review_project_card_machine_canon
Prompt code: KPR-12-005
Owner group: 12_generalized_project_canons
Load type: routed

## Purpose

Define the observer-only lifecycle for an Architecture Review source target. The
selected Project remains the owner of source, execution, validation, release, and
rollback. KANDA Reasoner is the reusable card machine that may read, analyze,
present, and discard observations without becoming a Project implementation
dependency.

## Core model

```text
KANDA Reasoner Tool = reusable observer card machine
Active Project = source owner
Selected Architecture Review source target = inserted read-only card
```

Compatibility mnemonic: `Selected large module = inserted card`.

The Tool may read, analyze, plan, preview, report, and preserve support evidence.
It must not apply Project source changes, install Project patches, execute Project
validation as authority, or roll back Project source.

## Required companion owners

- `KPR-12-001 project_tool_boundary_canon`: Tool, Project, Support, transient, and observer authority;
- Brick Wall: KANDA Tool implementation authorization when KANDA itself is being changed;
- Project-owned IDE/toolchain: external Project editing, testing, validation, release, and rollback;
- Large Module Refactor Protocol only when the selected target is a large-module refactor.

## MCard applicability

MCard applies when Architecture Review state is bound to a selected Project source
target across read, analysis, Planner/Workbench proposal, Preview, report, source
refresh, root/target switching, stale async results, cancellation, or eject.

One edited file alone does not activate MCard. Prompt-only or documentation-only
work may be evidence-backed `NOT_APPLICABLE`.

## Card and observation identity

Every current card binds:

```text
active_project_id
active_project_root_identity
target_relative_path
target_freshness_mode
target_freshness_value
source_snapshot_time
session_id
operation_id
observation_id
lifecycle_generation
analysis_id, when present
report_id, when present
```

Every asynchronous result, handoff, Preview, or report must prove the current
identity fields relevant to its phase before changing Tool-side observation state.

## Observer lifecycle state machine

Canonical path:

```text
EMPTY
-> CARD_INSERTED
-> CARD_READ
-> OBSERVED
-> ANALYSIS_READY
-> REPORT_READY
-> CARD_EJECTED
```

A card may also be ejected from any non-empty observer state. Eject invalidates
the lifecycle generation, cancels or detaches current workers, clears target-bound
Tool state, and discards late results. Eject never requires Project rollback.

There are no external-Project MCard states for `AUTHORIZED`, `APPLYING`,
`APPLIED_NOT_VERIFIED`, `ROLLBACK_REQUESTED`, or `ROLLBACK_VERIFIED`. Those
mutation-oriented states are retired from the observer card lifecycle.

## Read, analyze, and proposal rules

Reading does not transfer ownership. Planner, Workbench, and Preview are read-only
proposal/evidence surfaces for an external Project. They may describe changes for
the Project owner to implement independently, but KANDA does not apply them.

If the IDE or Project toolchain changes the source, the target fingerprint changes.
All target-bound observations, plans, previews, analyses, and reports derived from
the previous fingerprint become stale and must be refreshed before reuse.

Late results from an older generation fail closed and cannot repopulate the UI or
durable support evidence as current.

## Operation locks and cancellation

Observer operations may track audit, analysis, report-generation, cancellation,
or child-process activity. These locks protect Tool state only. They never create
a Project source transaction.

Card eject is always available. The Tool must request cancellation when possible,
invalidate the generation immediately, release callbacks/resources safely, and
ignore any late result. A worker that cannot stop promptly may finish in the
background only if it has no Project write authority and its result is discarded.

## Crash and restart recovery

On restart, KANDA may restore only read-only observation metadata whose source
fingerprint is still current. Otherwise it returns to `CARD_INSERTED` or
`CARD_READ` after re-observation. No Project source rollback or transaction
recovery is owned by MCard.

## Concurrent-session rule

Two KANDA sessions may observe the same Project, but their observation IDs and
lifecycle generations remain independent. They must not overwrite each other's
Tool-side support state without the support owner's normal conflict policy.
Neither session gains Project source-write authority.

## Switch and eject rules

### Project-root or target switch

Invalidate the previous observation generation before the new root or target
becomes authoritative. Retain only Project-scoped caches explicitly proven safe.

### Card eject

Eject may occur from any non-empty observer state. Clear target-specific analysis,
selection, Planner/Workbench proposal state, callbacks, worker generations, and
current Preview/report references.

Retain only independently owned Project source plus durable, scrubbed support
evidence already written through its canonical support owner. Never delete,
restore, or reverse Project source because the card was ejected.

## Evidence safety

Preview, reports, and logs may expose proprietary source, local paths, customer or
patient data, or secrets. Their owners must apply Project Support security,
redaction, retention, and deletion policy resolved by KPR-12-001.

## Router bridge requirements

```text
MCARD APPLICABILITY AND LIFECYCLE RECORD
Active Project identity proven:
Inserted card target:
Card ownership proven:
Target freshness mode and value:
Current observer lifecycle phase:
Observation ID and lifecycle generation:
Active observer locks:
Async result identity valid:
Cancellation/eject status:
Source fingerprint changed since observation: YES / NO
Stale Tool observations invalidated: YES / NO / NOT_APPLICABLE
Target-specific Tool state cleared on eject:
Project source left untouched by KANDA:
Project development remains possible without KANDA: YES / NO
Self-hosting logical separation preserved:
Unresolved fields:
MCard lifecycle gate: COMPLETE / NOT_APPLICABLE / BLOCKED
May proceed to the next Brick Wall gate: YES / NO
May begin coding from MCard: NO
```

No MCard field grants implementation authority.

## Routing triggers

Load for Architecture Review or AST target lifecycle, Planner/Workbench proposal
identity, root or target switching, stale async results, cancellation, source
fingerprint refresh, report identity, or card eject.

## When not to use

Do not load for payment-card discussion, generic UI styling, ordinary Tool/Project
identity with no Architecture Review target lifecycle, or Project implementation
that does not depend on KANDA observation state.

## Failure patterns

- target outside the current Project scope;
- stale worker repopulates a new root or target;
- IDE changes source but old observation remains current;
- card eject waits for or attempts Project rollback;
- KANDA applies a Project proposal;
- KANDA validator or source archive becomes a Project implementation prerequisite;
- eject deletes Project results or retains stale target-specific Tool memory;
- MCard claims implementation authority.

## Validation requirements

Focused validation must protect observer identity, lifecycle schema, source-change
staleness, late-result rejection, cancellation/eject safety, non-destructive eject,
Project-source immutability, KANDA-independent Project development, unique prompt
registration, negative routing, and the machine-readable MCard record.

## Do-not-regress rules

- The Tool is the reusable observer card machine; the Project owns source and durable results.
- MCard never applies, installs, validates-as-authority, or rolls back external Project source.
- Source fingerprint changes invalidate old observation generations.
- Card eject is always available and never requires Project rollback.
- Late results from an ejected or stale generation are discarded.
- Project development remains possible when KANDA is closed, unavailable, or the card is ejected.
- KPR-12-001 remains the root and ownership identity owner.

## Version history

- 3.0: replaced mutation/apply/rollback MCard semantics with the observer-only card lifecycle and guaranteed non-blocking eject.
- 2.0: historical mutation-oriented lifecycle; superseded for external Project observation.
- 1.0: established the original Architecture Review card-machine model.
