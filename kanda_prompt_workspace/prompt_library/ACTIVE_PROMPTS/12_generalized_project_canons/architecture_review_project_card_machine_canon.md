# Architecture Review Project Card Machine Canon

Version: 2.0
Status: Active prompt-library canon
Prompt ID: architecture_review_project_card_machine_canon
Prompt code: KPR-12-005
Owner group: 12_generalized_project_canons
Load type: routed

## Purpose

Own the Architecture Review target-card lifecycle and stale-state protection for a source target temporarily loaded into reusable KANDA tooling.

This is a lifecycle specialist. It does not own Tool/Project root resolution, Workbench storage layouts, transaction implementation, refactor architecture, module-size rules, patch delivery, or final coding authorization.

## Core model

```text
KANDA Reasoner Tool = reusable card machine
Active Project = card owner
Selected Architecture Review source target = inserted card
```

Compatibility mnemonic: `Selected large module = inserted card`.

The Tool may read, analyze, plan, preview, apply through an authorized owner, verify, and produce receipts. It never becomes the owner of Project source or durable Project results.

## Required companion owners

- `KPR-12-001 project_tool_boundary_canon`: Tool, Project, Support, transient workspace, and self-hosting identity;
- Brick Wall: final coding and source-write authorization;
- current Workbench/transaction owners: Preview, Shadow, transaction, receipt, lock, and recovery implementation;
- Large Module Refactor Protocol only when the selected target is a large-module refactor.

Do not copy their path or implementation contracts into this canon.

## MCard applicability

MCard applies when Architecture Review state is bound to a selected Project source target across analysis, Planner, Workbench, apply/rollback, receipt, switching, or eject behavior.

One edited file alone does not activate MCard. A prompt-only or documentation-only task may be evidence-backed `NOT_APPLICABLE`.

## Card and operation identity

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
plan_id
plan_version
preview_id
lifecycle_generation
authorization_identity
transaction_id, when opened
apply_attempt_id, when attempted
rollback_id, when requested
```

`target_freshness_mode` must be explicit: exact content hash, immutable source revision, validated repository commit plus dirty-state record, or another current canonical identity. An unspecified `hash or freshness basis` is invalid.

Every asynchronous result, handoff, Preview, apply, rollback, receipt, and callback must prove the current identity fields relevant to its phase before changing authoritative state.

## Lifecycle state machine

Canonical path:

```text
EMPTY
-> CARD_INSERTED
-> CARD_READ
-> PLAN_READY
-> WORKBENCH_READY
-> PREVIEW_VALIDATED
-> AUTHORIZED
-> APPLYING
-> APPLIED_NOT_VERIFIED
-> VERIFIED_TERMINAL
-> CARD_EJECTED
```

Rollback path:

```text
APPLYING or APPLIED_NOT_VERIFIED
-> ROLLBACK_REQUESTED
-> ROLLBACK_VERIFIED
-> CARD_EJECTED
```

`APPLIED_NOT_VERIFIED` begins after source mutation returns but before post-write verification establishes terminal success.

## Orthogonal operation locks

The lifecycle state is accompanied by explicit locks for:

- AST or architecture audit running;
- Planner worker running;
- Preview generation running;
- apply or rollback running;
- cancellation requested;
- cancellation incomplete;
- unresolved child process or callback;
- open transaction or unresolved apply outcome.

A root switch, target switch, snapshot replacement, or eject remains blocked while an incompatible lock is active.

## Insert rule

Insert only when KPR-12-001 proves the selected target belongs to the current Project source scope, no incompatible transaction or worker is authoritative, and previous card-specific state has been invalidated.

Filesystem containment uses the current public path owner and must account for platform path normalization, links or junctions, alternate separators, traversal, UNC or drive semantics, and revalidation immediately before write.

## Read and plan rules

Reading does not transfer ownership. Planner state remains bound to the current card and operation identity.

Root or target changes invalidate target-specific analysis, candidate, plan, handoff, Preview, authorization, apply, rollback, and callback generations before the new identity becomes authoritative.

Late results from an older generation fail closed and cannot repopulate the UI or durable state.

## Cancellation rule

Invalidating a generation is not sufficient cleanup. The operation owner must request cancellation, stop or join workers and child processes within a bounded policy, release resources and callbacks, and record unresolved termination as a blocking lock.

## Apply and verification rules

MCard may confirm lifecycle readiness but cannot authorize implementation.

Source mutation may begin only after Brick Wall and the owning implementation contracts authorize it. The result enters `APPLIED_NOT_VERIFIED` until current-source verification, required validators, and transaction evidence establish `VERIFIED_TERMINAL`.

## Crash and restart recovery

On restart, the Tool must inspect durable transaction identity before restoring or replacing a card. An open, applying, applied-not-verified, rollback-requested, or conflicting session state blocks normal insert and eject until recovery, verified completion, or verified rollback resolves it.

## Concurrent-session rule

Two sessions must not silently operate on the same card identity. The relevant transaction owner must provide a lease, lock, generation check, compare-and-swap contract, or explicit conflict rejection.

## Switch and eject rules

### Project-root switch

Unload target-specific Tool memory only after workers and transactions permit the switch. Do not delete Project-owned durable results.

### Target switch

Invalidate the previous target's downstream state before the new target becomes authoritative. Retain only Project-scoped caches explicitly proven safe.

### Terminal eject

Terminal eject requires verified completion or verified rollback and no active card lock.

Clear:

- target-specific analysis and selection;
- target-specific Planner and Workbench working state;
- callbacks and worker generations;
- current authorization and apply/rollback working references;
- target-specific GUI selection.

Retain under their canonical Project owners:

- Project source and generated helper files;
- scrubbed durable Preview and evidence;
- terminal transaction history and receipt;
- audit evidence references allowed by retention policy.

Release terminal locks. Do not retain a stale mutation lock merely because historical transaction evidence is retained.

## Evidence safety

Preview, receipts, transactions, and logs may expose proprietary source, local paths, customer or patient data, or secrets. Their implementation owners must apply the Project Support security, redaction, retention, and deletion policy resolved by KPR-12-001.

## Router bridge requirements

```text
MCARD APPLICABILITY AND LIFECYCLE RECORD
Active Project identity proven:
Inserted card target:
Card ownership proven:
Card and operation identity complete:
Target freshness mode and value:
Current lifecycle phase:
Active operation locks:
Async result identity valid:
Cancellation terminal:
Open transaction or unresolved apply outcome:
Switch/eject blocked when required:
Recovery status:
Concurrent-session conflict status:
Write target owner:
Terminal eject condition:
Target-specific Tool state cleared:
Project durable results retained:
Self-hosting logical separation preserved:
Unresolved fields:
MCard lifecycle gate: COMPLETE / NOT_APPLICABLE / BLOCKED
May proceed to the next Brick Wall gate: YES / NO
May begin coding: NO
```

No MCard field independently grants implementation authority.

## Routing triggers

Load for Architecture Review or AST target lifecycle, Planner-to-Workbench identity, root or target switching, stale async results, cancellation, Preview identity, transaction locks, apply/rollback recovery, receipt identity, concurrent sessions, or terminal eject.

## When not to use

Do not load for payment-card discussion, generic UI styling, ordinary Tool/Project identity with no Architecture Review target lifecycle, or a Workbench storage-path question that does not involve card lifecycle.

## Failure patterns

- target outside the current Project scope;
- stale worker repopulates a new root or target;
- same target reused under a different operation or transaction identity;
- apply succeeds locally but verification state is skipped;
- cancellation requested but worker or callback remains authoritative;
- open transaction permits switch or eject;
- restart ignores unresolved durable transaction state;
- two sessions mutate the same card without conflict detection;
- eject deletes Project results or retains target-specific Tool memory;
- MCard claims implementation authority.

## Validation requirements

Focused validation must protect identity and code, lifecycle-state schema, complete operation identity, valid normal and rollback transitions, stale-generation rejection, operation locks, cancellation, recovery, concurrent-session conflict handling, non-destructive terminal eject, unique registration, negative routing, and the machine-readable MCard record.

Runtime lifecycle tests should use a public lifecycle facade or test adapter when available. Direct private-GUI attribute testing may remain only as bounded legacy regression coverage and must not become the canonical contract.

## Do-not-regress rules

- The Tool is the reusable card machine; the Project owns source and durable results.
- Card ownership and freshness must be current and explicit.
- Every async or mutation action is bound to complete operation identity.
- `APPLIED_NOT_VERIFIED` is a reachable post-write state.
- Active workers, cancellation, transactions, or unresolved apply outcomes block incompatible switching and eject.
- Root and target changes invalidate stale generations before new authority.
- Terminal eject clears target-specific Tool state, releases locks, and preserves Project results.
- MCard never authorizes coding or source write.
- KPR-12-001 remains the root and ownership identity owner.

## Version history

- 2.0: narrowed ownership to lifecycle, completed operation identity, made APPLIED_NOT_VERIFIED reachable, added operation locks, cancellation, recovery, concurrency, evidence safety, and non-authorizing gate output.
- 1.0: established the original Architecture Review card-machine model.
